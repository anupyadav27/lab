import argparse
import json
import logging
import os
import time
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
def get_final_decision(reviewed_json: Dict, model: str = "gpt-4o") -> str:
    """
    Third AI model makes final decision based on:
    - Original compliance control data
    - First opinion (gpt-4o-mini)
    - Second opinion (GPT-4o review)
    """
    api_key = os.environ["OPENAI_API_KEY"].strip()
    client = OpenAI(api_key=api_key, timeout=60.0)

    # Extract all data
    control_id = reviewed_json.get("control_id", "N/A")
    source = reviewed_json.get("source", "N/A")
    input_row = reviewed_json.get("input_row", {})
    
    # First opinion
    original_assessment = reviewed_json.get("original_assessment", {})
    first_opinion = original_assessment.get("response", "")
    first_model = original_assessment.get("model", "gpt-4o-mini")
    
    # Second opinion
    review = reviewed_json.get("review", {})
    second_opinion = review.get("response", "")
    second_model = review.get("model", "gpt-4o")
    
    system_message = (
        "You are the FINAL DECISION MAKER for Azure compliance control audit classifications. "
        "You will receive compliance control data and TWO AI opinions. "
        "Your job is to analyze ALL information and make the DEFINITIVE decision on: "
        "1) Manual vs Automated approach, "
        "2) If Automated: exact program name in snake_case (azure_<service>_<resource>_<intent>), "
        "3) If Manual: clear step-by-step instructions. "
        "Be authoritative and decisive. This is the FINAL answer."
    )

    user_message = f"""You are making the FINAL DECISION for this Azure compliance control.

╔══════════════════════════════════════════════════════════════════════════════╗
║                         COMPLIANCE CONTROL DATA                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Control ID:    {control_id}
Source:        {source}
Title:         {input_row.get('title', 'N/A')}

Description:   {input_row.get('description', 'N/A')[:500]}

Rationale:     {input_row.get('rationale', 'N/A')[:500]}

Audit Steps:   {input_row.get('audit', 'N/A')[:500]}

Remediation:   {input_row.get('remediation', 'N/A')[:500]}


╔══════════════════════════════════════════════════════════════════════════════╗
║                         FIRST OPINION ({first_model})                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

{first_opinion[:1000]}


╔══════════════════════════════════════════════════════════════════════════════╗
║                    SECOND OPINION - REVIEW ({second_model})                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

{second_opinion[:1000]}


╔══════════════════════════════════════════════════════════════════════════════╗
║                         YOUR FINAL DECISION                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

Analyze ALL the above information and make your FINAL DECISION.

**DECISION CRITERIA:**

1. **Consider ALL Data Sources:**
   - Compliance control description, rationale, audit steps, remediation
   - First AI opinion and reasoning
   - Second AI review and critique
   - Your knowledge of Azure Resource Manager APIs

2. **Azure API Capability Check:**
   ✓ Can this be checked via Azure CLI/PowerShell/SDK/ARM APIs?
   ✓ Are the properties exposed through standard Azure resource APIs?
   ✓ Does it require SSH/node access or visual inspection?

3. **Resolve Disagreements:**
   - If both AIs agree → likely correct
   - If AIs disagree → use your judgment based on Azure API capabilities
   - Prioritize technical accuracy over opinions

4. **Be Decisive:**
   - Choose ONLY Manual OR Automated
   - No "hybrid" or "it depends"
   - Make the call based on what's technically possible


**OUTPUT FORMAT (STRICT):**

**FINAL APPROACH:** [Manual | Automated]

**JUSTIFICATION:**
[2-3 sentences explaining WHY this is your final decision, considering both AI opinions and Azure capabilities]

**CONFIDENCE:** [HIGH | MEDIUM | LOW]

--- IF AUTOMATED ---

**PROGRAM NAME:** 
[Exact function name in snake_case format: azure_<service>_<resource>_<security_intent>]

**AUTOMATION DETAILS:**
- Azure Resource/Service: [e.g., Storage Accounts, Key Vaults, AKS Clusters]
- API/CLI Method: [e.g., az storage account show, Get-AzStorageAccount]
- Properties to Check: [specific JSON paths or properties]
- Pass Criteria: [exact expected values]
- Fail Criteria: [what indicates non-compliance]

--- IF MANUAL ---

**MANUAL STEPS:**
1. [Step-by-step instructions with Azure portal paths or manual verification steps]
2. [What to verify and why automation isn't feasible]
3. [Expected secure configuration]
4. [How to confirm compliance]

**WHY NOT AUTOMATED:**
[Brief explanation why this cannot be automated via Azure APIs]

---

**DISAGREEMENTS RESOLVED:**
[If the two AI opinions differed, explain how you resolved the conflict]

**SOURCE:** {source}
"""

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            max_completion_tokens=2000,
            temperature=0.2,  # Low temperature for consistent decisions
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
        logging.error(f"Final decision API call failed: {e}")
        raise


def process_reviewed_file(
    input_path: str,
    output_dir: str,
    decision_model: str,
) -> Dict:
    """Process a reviewed file and get final decision from third AI."""
    
    # Read reviewed JSON
    with open(input_path, "r") as f:
        reviewed_json = json.load(f)
    
    control_id = reviewed_json.get("control_id", "N/A")
    unique_id = reviewed_json.get("unique_id", control_id)
    
    logging.info(f"Final decision for: {control_id}")
    
    try:
        # Get final decision from third AI
        final_decision = get_final_decision(reviewed_json, model=decision_model)
        
        # Create final JSON with all three opinions
        final_json = {
            "unique_id": unique_id,
            "control_id": control_id,
            "source": reviewed_json.get("source"),
            "input_row": reviewed_json.get("input_row"),
            
            # Three AI opinions
            "first_opinion": {
                "model": reviewed_json.get("original_assessment", {}).get("model", "gpt-4o-mini"),
                "response": reviewed_json.get("original_assessment", {}).get("response", "")
            },
            "second_opinion": {
                "model": reviewed_json.get("review", {}).get("model", "gpt-4o"),
                "response": reviewed_json.get("review", {}).get("response", ""),
                "reviewed_at": reviewed_json.get("review", {}).get("reviewed_at")
            },
            "final_decision": {
                "model": decision_model,
                "decision_maker": "Third AI - Final Authority",
                "response": final_decision,
                "decided_at": datetime.utcnow().isoformat()
            },
            
            "metadata": {
                "reviewed_file": os.path.basename(input_path),
                "final_version": "1.0",
                "three_model_consensus": True
            }
        }
        
        # Write final decision
        output_path = os.path.join(output_dir, f"{unique_id}.json")
        with open(output_path, "w") as out:
            json.dump(final_json, out, indent=4, ensure_ascii=False)
        
        logging.info(f"✓ Final decision saved: {output_path}")
        return {"status": "success", "unique_id": unique_id}
        
    except Exception as e:
        logging.error(f"✗ Failed final decision for {control_id}: {e}")
        return {"status": "error", "error": str(e)}


def process_all_reviewed_files(
    input_dir: str,
    output_dir: str,
    decision_model: str,
    max_files: Optional[int] = None,
) -> None:
    """Process all reviewed files and get final decisions."""
    
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Output directory: {output_dir}")
    logging.info(f"Decision model: {decision_model}")
    
    # Collect all reviewed JSON files
    if not os.path.exists(input_dir):
        logging.error(f"Input directory not found: {input_dir}")
        return
    
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.json')]
    logging.info(f"Found {len(files)} reviewed files")
    
    if max_files:
        files = files[:max_files]
        logging.info(f"Limited to first {max_files} files")
    
    # Process each file
    processed = 0
    errors = 0
    consecutive_errors = 0
    max_consecutive_errors = 5
    
    for idx, file_path in enumerate(files, 1):
        logging.info(f"[{idx}/{len(files)}] Processing: {os.path.basename(file_path)}")
        
        result = process_reviewed_file(file_path, output_dir, decision_model)
        
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
        time.sleep(1.2)
    
    logging.info("=" * 80)
    logging.info(f"✅ Final Decisions Complete!")
    logging.info(f"   Processed: {processed}")
    logging.info(f"   Errors: {errors}")
    logging.info(f"   Total: {len(files)}")
    logging.info(f"   Output: {output_dir}")
    logging.info("=" * 80)


def parse_args():
    parser = argparse.ArgumentParser(description="Third AI makes final compliance decisions")
    parser.add_argument(
        "--input-dir",
        default="output_reviewed_20251026_195327",
        help="Input directory with reviewed JSONs"
    )
    parser.add_argument(
        "--output-dir",
        default=f"output_final_decisions_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        help="Output directory for final decisions"
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="Model for final decisions (default: gpt-4o)"
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
    logging.info("🎯 FINAL DECISION MAKER - THIRD AI MODEL")
    logging.info("=" * 80)
    logging.info(f"Input directory: {args.input_dir}")
    logging.info(f"Output directory: {args.output_dir}")
    logging.info(f"Decision model: {args.model}")
    logging.info("=" * 80)
    logging.info("")
    logging.info("📋 Process:")
    logging.info("   1️⃣  First Opinion:  gpt-4o-mini (original assessment)")
    logging.info("   2️⃣  Second Opinion: GPT-4o (review & validation)")
    logging.info("   3️⃣  Final Decision: GPT-4o (this run - authoritative)")
    logging.info("=" * 80)
    
    process_all_reviewed_files(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        decision_model=args.model,
        max_files=args.max_files,
    )


if __name__ == "__main__":
    main()

