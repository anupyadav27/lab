#!/usr/bin/env python3
"""
GCP Compliance Agent - Step 2: Review & Validation
Uses GPT-4o to review initial assessments and validate decisions.
"""

import argparse
import glob
import json
import logging
import os
import time
from typing import Dict
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
    """Call GPT-4o to review the GCP compliance assessment."""
    api_key = os.environ["OPENAI_API_KEY"].strip()
    client = OpenAI(api_key=api_key, timeout=60.0)

    control_id = original_json.get("control_id", "N/A")
    source = original_json.get("source", "GCP CIS")
    original_response = original_json.get("step1_initial_assessment", "")
    input_row = original_json.get("input_row", {})
    
    system_message = (
        "You are a senior GCP security expert reviewing compliance audit decisions made by a junior analyst. "
        "Your job is to validate the audit approach (Manual vs Automated), verify technical accuracy, "
        "and provide a quality score. Be critical but fair. Focus on GCP API capabilities (Google Cloud SDK (gcloud), GCP CLI) and security best practices."
    )

    user_message = f"""You are reviewing an GCP compliance control audit assessment.

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
   - Can this be checked via GCP APIs/Google Cloud SDK (gcloud)/CLI?
   - Consider: GCP SDK capabilities, GCP CLI commands, CloudFormation, GCP Config

2. **TECHNICAL ACCURACY:** [Score 1-10]
   - Are the automation details technically correct?
   - Are Google Cloud SDK (gcloud) methods or CLI commands valid?
   - Are manual steps accurate and complete?
   - Is the program name following convention: gcp_<service>_<resource>_<specific_detailed_security_check>? Is it DESCRIPTIVE and CLEAR about what exactly is being checked (e.g., including 'in_transit', 'at_rest', 'retention_period', 'minimum_version', etc.)?

3. **IMPROVEMENTS:**
   - What could be better?
   - Any missing considerations?
   - Alternative GCP API methods?
   - Better program name suggestion?

4. **CONFIDENCE:** [HIGH | MEDIUM | LOW]
   - Your confidence in this assessment

5. **FINAL RECOMMENDATION:**
   - Keep as-is
   - Modify (explain what)
   - Re-classify (Manual ↔ Automated with justification)

**OUTPUT FORMAT:**
Provide your review in a structured format with clear sections for each point above.
Be specific about GCP services, Google Cloud SDK (gcloud) methods, CLI commands, and technical details.
If you disagree, explain why with GCP API evidence.
"""

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            max_completion_tokens=1500,
            temperature=0.3,
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


def process_json_file(input_path: str, output_dir: str, review_model: str) -> Dict:
    """Process a single JSON file - review and create updated version."""
    
    with open(input_path, "r", encoding="utf-8") as f:
        original_json = json.load(f)
    
    control_id = original_json.get("control_id", "N/A")
    logging.info(f"Reviewing: {control_id}")
    
    try:
        review_text = review_with_gpt4o(original_json, model=review_model)
        
        # Create enhanced JSON with review
        filename_id = original_json.get("unique_id") or control_id
        filename_id = filename_id.replace("/", "_").replace("\\", "_").replace(" ", "_").replace(":", "_")
        
        # Create clean title slug for filename
        title = original_json.get("title", "")
        title_slug = title.lower()[:50].replace(" ", "-").replace("/", "-").replace(":", "").replace("(", "").replace(")", "")
        
        output_filename = f"{filename_id}__{title_slug}.json"
        output_path = os.path.join(output_dir, output_filename)
        
        enhanced_json = {
            **original_json,
            "step2_review": review_text,
            "review_model": review_model,
            "review_timestamp": datetime.now().isoformat(),
        }
        
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(enhanced_json, out, indent=4, ensure_ascii=False)
        
        logging.info(f"✓ Reviewed and saved: {output_path}")
        return {"status": "success", "control_id": control_id}
        
    except Exception as e:
        logging.error(f"✗ Failed to review {control_id}: {e}")
        return {"status": "error", "control_id": control_id, "error": str(e)}


def process_all_jsons(input_dir: str, output_dir: str, review_model: str, max_files: int = None) -> None:
    """Process all JSON files from Step 1."""
    os.makedirs(output_dir, exist_ok=True)
    
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    total = len(json_files)
    
    if max_files:
        json_files = json_files[:max_files]
    
    logging.info("=" * 80)
    logging.info(f"GCP Agent Step 2 - Review & Validation")
    logging.info(f"Input: {input_dir}")
    logging.info(f"Output: {output_dir}")
    logging.info(f"Files to process: {len(json_files)}/{total}")
    logging.info(f"Review model: {review_model}")
    logging.info("=" * 80)
    
    processed = 0
    errors = 0
    
    for idx, json_file in enumerate(json_files, 1):
        logging.info(f"[{idx}/{len(json_files)}] Processing: {os.path.basename(json_file)}")
        
        result = process_json_file(json_file, output_dir, review_model)
        
        if result["status"] == "success":
            processed += 1
        else:
            errors += 1
        
        time.sleep(1.5)
    
    logging.info("=" * 80)
    logging.info(f"✅ Step 2 Complete!")
    logging.info(f"   Processed: {processed}")
    logging.info(f"   Errors: {errors}")
    logging.info(f"   Total: {len(json_files)}")
    logging.info(f"   Output: {output_dir}")
    logging.info("=" * 80)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GCP Compliance Agent - Step 2: Review")
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory with Step 1 JSON outputs"
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_output = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"output_step2_{timestamp}"
    )
    
    parser.add_argument(
        "--output-dir",
        default=default_output,
        help="Directory for reviewed outputs"
    )
    parser.add_argument("--review-model", default="gpt-4o", help="Review model (default: gpt-4o)")
    parser.add_argument("--max-files", type=int, default=None, help="Max files to process")
    return parser.parse_args()


if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY not set in environment")
    
    args = parse_args()
    process_all_jsons(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        review_model=args.review_model,
        max_files=args.max_files,
    )

