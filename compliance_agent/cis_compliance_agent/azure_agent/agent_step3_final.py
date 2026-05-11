#!/usr/bin/env python3
"""
Azure Compliance Agent - Step 3: Final Decision
Third AI (GPT-4o) makes authoritative final decision based on all data.
"""

import argparse
import re
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
def get_final_decision(reviewed_json: Dict, model: str = "gpt-4o") -> str:
    """Third AI model makes final Azure compliance decision."""
    api_key = os.environ["OPENAI_API_KEY"].strip()
    client = OpenAI(api_key=api_key, timeout=60.0)

    control_id = reviewed_json.get("control_id", "N/A")
    source = reviewed_json.get("source", "Azure CIS")
    input_row = reviewed_json.get("input_row", {})
    
    first_opinion = reviewed_json.get("step1_initial_assessment", "")
    second_opinion = reviewed_json.get("step2_review", "")
    
    system_message = (
        "You are the FINAL DECISION MAKER for Azure compliance control audit classifications. "
        "You will receive Azure compliance control data and TWO AI opinions. "
        "Your job is to analyze ALL information and make the DEFINITIVE decision on: "
        "1) Manual vs Automated approach, "
        "2) If Automated: exact program name in snake_case (azure_<service>_<resource>_<intent>), "
        "3) If Manual: clear step-by-step instructions. "
        "Be authoritative and decisive. This is the FINAL answer."
    )

    user_message = f"""You are making the FINAL DECISION for this Azure compliance control.

╔══════════════════════════════════════════════════════════════════════════════╗
║                         AZURE COMPLIANCE CONTROL DATA                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Control ID:    {control_id}
Source:        {source}
Title:         {input_row.get('title', 'N/A')}

Description:   {input_row.get('description', 'N/A')[:500]}

Rationale:     {input_row.get('rationale', 'N/A')[:500]}

Audit Steps:   {input_row.get('audit', 'N/A')[:500]}

Remediation:   {input_row.get('remediation', 'N/A')[:500]}


╔══════════════════════════════════════════════════════════════════════════════╗
║                         FIRST OPINION (gpt-4o-mini)                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

{first_opinion[:1500]}


╔══════════════════════════════════════════════════════════════════════════════╗
║                    SECOND OPINION - REVIEW (GPT-4o)                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

{second_opinion[:1500]}


╔══════════════════════════════════════════════════════════════════════════════╗
║                         YOUR FINAL DECISION                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

Analyze ALL the above information and make your FINAL DECISION.

**DECISION CRITERIA:**

1. **Consider ALL Data Sources:**
   - Azure compliance control description, rationale, audit steps, remediation
   - First AI opinion and reasoning
   - Second AI review and critique
   - Your knowledge of Azure APIs (Azure SDK for Python, Azure CLI)

2. **Azure API Capability Check:**
   ✓ Can this be checked via Azure SDK/Azure CLI/ARM templates/Azure Policy?
   ✓ Are the properties exposed through Azure SDK APIs?
   ✓ Does it require SSH to VMs/RDP or manual inspection?

3. **Resolve Disagreements:**
   - If both AIs agree → likely correct
   - If AIs disagree → use your judgment based on Azure API capabilities
   - Prioritize technical accuracy over opinions

4. **Be Decisive:**
   - Choose ONLY Manual OR Automated
   - No "hybrid" or "it depends"
   - Make the call based on what's technically possible with Azure APIs


**OUTPUT FORMAT (STRICT):**

**FINAL APPROACH:** [Manual | Automated]

**JUSTIFICATION:**
[2-3 sentences explaining WHY this is your final decision, considering both AI opinions and Azure capabilities]

**CONFIDENCE:** [HIGH | MEDIUM | LOW]

--- IF AUTOMATED ---

**PROGRAM NAME:** 
[Exact function name in snake_case format: azure_<service>_<resource>_<specific_detailed_security_check>. Be DESCRIPTIVE - include specifics like 'encryption_in_transit', 'backup_retention_period', 'minimum_tls_version', 'mfa_enabled', etc.]

**AUTOMATION DETAILS:**
- Azure Resource/Service: [e.g., Storage Accounts, Entra ID Policies, Virtual Machines, AKS Clusters]
- API/CLI Method: [e.g., Azure SDK StorageManagementClient, az storage account show, az aks show]
- Properties to Check: [specific response fields or properties]
- Pass Criteria: [exact expected values]
- Fail Criteria: [what indicates non-compliance]

--- IF MANUAL ---

**MANUAL STEPS:**
1. [Step-by-step instructions with Azure Portal paths or manual verification steps]
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
            temperature=0.2,
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


def process_reviewed_file(input_path: str, output_dir: str, decision_model: str) -> Dict:
    """Process a reviewed file and get final decision from third AI."""
    
    with open(input_path, "r", encoding="utf-8") as f:
        reviewed_json = json.load(f)
    
    control_id = reviewed_json.get("control_id", "N/A")
    logging.info(f"Final decision for: {control_id}")
    
    try:
        final_decision_text = get_final_decision(reviewed_json, model=decision_model)
        
        # Extract key fields from final decision
        lines = final_decision_text.split('\n')
        approach = "Unknown"
        confidence = "MEDIUM"
        program_name = ""
        
        for line in lines:
            if line.startswith("**FINAL APPROACH:**"):
                approach = line.split("**FINAL APPROACH:**")[1].strip().split()[0]
            elif line.startswith("**CONFIDENCE:**"):
                confidence = line.split("**CONFIDENCE:**")[1].strip().split()[0]
            elif line.startswith("**PROGRAM NAME:**"):
                program_name = line.split("**PROGRAM NAME:**")[1].strip()

        # Fallback: try to extract a plausible azure_* snake_case program name from the decision text
        if approach.lower() == "automated" and not program_name:
            candidates = re.findall(r"\bazure_[a-z0-9_]{8,}\b", final_decision_text)
            # Prefer names that look like azure_<svc>_<resource>_<intent> (>= 3 underscores)
            candidates = [c for c in candidates if c.count('_') >= 3]
            if candidates:
                program_name = candidates[0]
        
        # Sanitize filename
        filename_id = reviewed_json.get("unique_id") or control_id
        filename_id = filename_id.replace("/", "_").replace("\\", "_").replace(" ", "_").replace(":", "_")
        
        title = reviewed_json.get("title", "")
        title_slug = title.lower()[:50].replace(" ", "-").replace("/", "-").replace(":", "").replace("(", "").replace(")", "")
        
        output_filename = f"{filename_id}__{title_slug}.json"
        output_path = os.path.join(output_dir, output_filename)
        
        final_json = {
            **reviewed_json,
            "step3_final_decision": {
                "decision_text": final_decision_text,
                "final_approach": approach,
                "confidence": confidence,
                "program_name": program_name if approach.lower() == "automated" else "",
                "model": decision_model,
                "timestamp": datetime.now().isoformat(),
            }
        }
        
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(final_json, out, indent=4, ensure_ascii=False)
        
        logging.info(f"✓ Final decision saved: {output_path}")
        return {"status": "success", "control_id": control_id}
        
    except Exception as e:
        logging.error(f"✗ Failed final decision for {control_id}: {e}")
        return {"status": "error", "control_id": control_id, "error": str(e)}


def process_all_reviewed(input_dir: str, output_dir: str, decision_model: str, max_files: int = None) -> None:
    """Process all reviewed JSON files from Step 2."""
    os.makedirs(output_dir, exist_ok=True)
    
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    total = len(json_files)
    
    if max_files:
        json_files = json_files[:max_files]
    
    logging.info("=" * 80)
    logging.info(f"Azure Agent Step 3 - Final Decision")
    logging.info(f"Input: {input_dir}")
    logging.info(f"Output: {output_dir}")
    logging.info(f"Files to process: {len(json_files)}/{total}")
    logging.info(f"Decision model: {decision_model}")
    logging.info("=" * 80)
    
    processed = 0
    errors = 0
    
    for idx, json_file in enumerate(json_files, 1):
        logging.info(f"[{idx}/{len(json_files)}] Processing: {os.path.basename(json_file)}")
        
        result = process_reviewed_file(json_file, output_dir, decision_model)
        
        if result["status"] == "success":
            processed += 1
        else:
            errors += 1
        
        time.sleep(1.5)
    
    logging.info("=" * 80)
    logging.info(f"✅ Step 3 Complete!")
    logging.info(f"   Processed: {processed}")
    logging.info(f"   Errors: {errors}")
    logging.info(f"   Total: {len(json_files)}")
    logging.info(f"   Output: {output_dir}")
    logging.info("=" * 80)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Azure Compliance Agent - Step 3: Final Decision")
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory with Step 2 reviewed outputs"
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_output = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"output_step3_{timestamp}"
    )
    
    parser.add_argument(
        "--output-dir",
        default=default_output,
        help="Directory for final decision outputs"
    )
    parser.add_argument("--decision-model", default="gpt-4o-mini", help="Decision model (default: gpt-4o-mini)")
    parser.add_argument("--max-files", type=int, default=None, help="Max files to process")
    return parser.parse_args()


if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY not set in environment")
    
    args = parse_args()
    process_all_reviewed(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        decision_model=args.decision_model,
        max_files=args.max_files,
    )
