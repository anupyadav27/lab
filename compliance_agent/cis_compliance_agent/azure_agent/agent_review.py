import argparse
import json
import logging
import os
import time
import hashlib
from typing import Dict, Optional
from datetime import datetime

import openai
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@retry(
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(4),
    retry=retry_if_exception_type((openai.APIError, openai.APIConnectionError, openai.RateLimitError))
)
def review_with_gpt4o(original_json: Dict, model: str = "gpt-4o") -> str:
    """Call GPT-4o to review the original assessment and provide validation."""
    api_key = os.environ["OPENAI_API_KEY"].strip()
    client = OpenAI(api_key=api_key, timeout=60.0)

    # Extract key information from original JSON
    control_id = original_json.get("id", "N/A")
    source = original_json.get("source", "N/A")
    original_response = original_json.get("gpt_response", "")
    input_row = original_json.get("input_row", {})
    
    system_message = (
        "You are a senior Azure security expert reviewing compliance audit decisions made by a junior analyst. "
        "Your job is to validate the audit approach (Manual vs Automated), verify technical accuracy, "
        "and provide a quality score. Be critical but fair. Focus on Azure API capabilities and security best practices."
    )

    user_message = f"""You are reviewing a compliance control audit assessment.

**CONTROL INFORMATION:**
- ID: {control_id}
- Source: {source}
- Title: {input_row.get('title', 'N/A')}
- Description: {input_row.get('description', 'N/A')[:500]}

**ORIGINAL ASSESSMENT:**
{original_response}

**YOUR REVIEW TASK:**
Validate the assessment and provide:

1. **APPROACH VALIDATION:** [AGREE | DISAGREE | PARTIALLY_AGREE]
   - Is Manual vs Automated classification correct?
   - Can this be checked via Azure APIs/CLI?
   - Consider: ARM APIs, Azure CLI, PowerShell cmdlets, SDK capabilities

2. **TECHNICAL ACCURACY:** [Score 1-10]
   - Are the automation details technically correct?
   - Are manual steps accurate and complete?
   - Is the program name following convention: azure_<service>_<resource>_<security_intent>?

3. **IMPROVEMENTS:**
   - What could be better?
   - Any missing considerations?
   - Alternative approach suggestions?

4. **CONFIDENCE:** [HIGH | MEDIUM | LOW]
   - Your confidence in this assessment

5. **FINAL RECOMMENDATION:**
   - Keep as-is
   - Modify (explain what)
   - Re-classify (Manual ↔ Automated with justification)

**OUTPUT FORMAT:**
Provide your review in a structured format with clear sections for each point above.
Be specific about Azure services, APIs, and technical details.
If you disagree, explain why with Azure API evidence.
"""

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            max_completion_tokens=1500,
            temperature=0.3,  # Lower for more consistent reviews
        )
        
        if not resp or not getattr(resp, "choices", None):
            raise ValueError("No choices in OpenAI response")

        choice = resp.choices[0]
        message = choice.message if choice.message else None
        if not message:
            raise ValueError("No message in first choice")
        
        content = getattr(message, "content", None)
        if not content or content.strip() == "":
            raise ValueError("Empty message content in OpenAI response")
            
        return content.strip()
        
    except Exception as e:
        logging.error(f"Review API call failed: {e}")
        raise


def generate_unique_id(original_json: Dict) -> str:
    """Generate a unique ID for the reviewed file to avoid conflicts."""
    # Use control_id + source + title hash for uniqueness
    input_row = original_json.get("input_row", {})
    control_id = original_json.get("id", "unknown")
    source = original_json.get("source", "unknown")
    title = input_row.get("title", "")
    unique_id_field = input_row.get("unique_id", "")
    
    # If unique_id exists in input_row, use it
    if unique_id_field:
        return unique_id_field.replace("/", "_").replace("\\", "_").replace(" ", "_")
    
    # Otherwise, create hash-based unique ID
    # Combine control_id + source + first 30 chars of title
    title_slug = title.lower().replace(" ", "_").replace("/", "_")[:30]
    combined = f"{control_id}_{source}_{title}"
    hash_suffix = hashlib.md5(combined.encode()).hexdigest()[:8]
    
    return f"{control_id}_{hash_suffix}"


def process_json_file(
    input_path: str,
    output_dir: str,
    review_model: str,
) -> Dict:
    """Process a single JSON file - review and create updated version."""
    
    # Read original JSON
    with open(input_path, "r") as f:
        original_json = json.load(f)
    
    control_id = original_json.get("id", "N/A")
    logging.info(f"Reviewing: {control_id}")
    
    try:
        # Get GPT-4o review
        review_response = review_with_gpt4o(original_json, model=review_model)
        
        # Generate unique ID for output file
        unique_id = generate_unique_id(original_json)
        
        # Create enhanced JSON with review
        enhanced_json = {
            "unique_id": unique_id,
            "control_id": control_id,
            "source": original_json.get("source"),
            "original_assessment": {
                "model": "gpt-4o-mini",
                "response": original_json.get("gpt_response")
            },
            "review": {
                "model": review_model,
                "reviewer": "gpt-4o",
                "response": review_response,
                "reviewed_at": datetime.utcnow().isoformat()
            },
            "input_row": original_json.get("input_row"),
            "metadata": {
                "original_file": os.path.basename(input_path),
                "review_version": "1.0"
            }
        }
        
        # Write to output directory with unique ID
        output_path = os.path.join(output_dir, f"{unique_id}.json")
        with open(output_path, "w") as out:
            json.dump(enhanced_json, out, indent=4, ensure_ascii=False)
        
        logging.info(f"✓ Reviewed and saved: {output_path}")
        return {"status": "success", "unique_id": unique_id}
        
    except Exception as e:
        logging.error(f"✗ Failed to review {control_id}: {e}")
        return {"status": "error", "error": str(e)}


def process_all_jsons(
    input_folders: list,
    output_dir: str,
    review_model: str,
    max_files: Optional[int] = None,
) -> None:
    """Process all JSON files from input folders."""
    
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Output directory: {output_dir}")
    logging.info(f"Review model: {review_model}")
    
    # Collect all JSON files from input folders
    all_files = []
    for folder in input_folders:
        if os.path.exists(folder):
            files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.json')]
            all_files.extend(files)
            logging.info(f"Found {len(files)} files in {folder}")
    
    logging.info(f"Total files to review: {len(all_files)}")
    
    if max_files:
        all_files = all_files[:max_files]
        logging.info(f"Limited to first {max_files} files")
    
    # Process each file
    processed = 0
    errors = 0
    consecutive_errors = 0
    max_consecutive_errors = 5
    
    for idx, file_path in enumerate(all_files, 1):
        logging.info(f"[{idx}/{len(all_files)}] Processing: {os.path.basename(file_path)}")
        
        result = process_json_file(file_path, output_dir, review_model)
        
        if result["status"] == "success":
            processed += 1
            consecutive_errors = 0
        else:
            errors += 1
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                logging.error("Too many consecutive errors, stopping")
                break
        
        # Rate limiting
        time.sleep(1.0)
    
    logging.info("=" * 80)
    logging.info(f"✅ Review Complete!")
    logging.info(f"   Processed: {processed}")
    logging.info(f"   Errors: {errors}")
    logging.info(f"   Total: {len(all_files)}")
    logging.info(f"   Output: {output_dir}")
    logging.info("=" * 80)


def parse_args():
    parser = argparse.ArgumentParser(description="Review compliance audit JSONs with GPT-4o")
    parser.add_argument(
        "--input-folders",
        nargs="+",
        default=["output_v20251026_160817", "output_missing_final"],
        help="Input folders containing JSON files to review"
    )
    parser.add_argument(
        "--output-dir",
        default=f"output_reviewed_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        help="Output directory for reviewed JSONs"
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="Review model to use (default: gpt-4o)"
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Maximum number of files to process (for testing)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    
    logging.info("=" * 80)
    logging.info("🔍 COMPLIANCE AUDIT REVIEW AGENT")
    logging.info("=" * 80)
    logging.info(f"Input folders: {args.input_folders}")
    logging.info(f"Output directory: {args.output_dir}")
    logging.info(f"Review model: {args.model}")
    logging.info("=" * 80)
    
    process_all_jsons(
        input_folders=args.input_folders,
        output_dir=args.output_dir,
        review_model=args.model,
        max_files=args.max_files,
    )


if __name__ == "__main__":
    main()

