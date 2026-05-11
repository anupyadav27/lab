#!/usr/bin/env python3
"""
Alibaba Cloud Compliance Agent - Step 1: Initial Assessment
Uses gpt-4o-mini to analyze Alibaba Cloud CIS compliance controls and determine audit approach.
"""

import argparse
import csv
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
def call_openai_initial_assessment(row: Dict[str, str], model: str, fallback_model: Optional[str]) -> str:
    """Call OpenAI for initial Alibaba Cloud compliance assessment."""
    api_key = os.environ["OPENAI_API_KEY"].strip()
    client = OpenAI(api_key=api_key, timeout=60.0)

    source_value = row.get("source") or row.get("framework") or row.get("standard") or "Alibaba Cloud CIS"
    row_json = json.dumps(row, ensure_ascii=False, indent=2)
    
    system_message = (
        "You are an enterprise-grade Cloud Security Posture Management (CSPM) compliance audit engine for Alibaba Cloud resources. "
        "Analyze Alibaba Cloud CIS compliance controls and determine the optimal audit approach following industry standards used by tools like Prowler, ScoutSuite, and CloudSploit. "
        "Use ALL available fields (description, rationale, audit, remediation, impact, references) to make informed decisions. "
        "If any field is missing or unclear, use your knowledge of Alibaba Cloud APIs (Aliyun CLI, Alibaba Cloud CLI) and the referenced documentation to determine if the control is API-checkable."
    )

    user_message = f"""Source: {source_value}

Input Control (JSON):
{row_json}

INSTRUCTIONS:
Analyze this Alibaba Cloud compliance control using ALL available data to determine the optimal audit approach.

DECISION PROCESS:
1. Read ALL fields: id, title, description, rationale, audit, remediation, impact, references
2. If audit field is empty/incomplete, analyze description + remediation + references
3. Consider Alibaba Cloud architecture: What Alibaba Cloud APIs exist for this resource/service?
4. Use your training knowledge of Alibaba Cloud services + Aliyun CLI SDK + Alibaba Cloud CLI commands
5. Reference any documentation URLs provided
6. Make an informed decision based on complete context

**AUDIT APPROACH:** [Choose ONE: Manual | Automated]

**APPROACH DECISION:**
- **Automated:** Control can be fully verified via Alibaba Cloud APIs/Aliyun CLI/Alibaba Cloud CLI/CloudFormation
  Examples: S3 bucket policies, IAM password policies, EC2 security groups, CloudTrail logs, KMS encryption
  
- **Manual:** Control requires human judgment, SSH access to instances, or checks not exposed via Alibaba Cloud APIs
  Examples: Application-level configs, OS-level SSH checks, content inspection, organizational policies

DECISION CRITERIA (Use ALL to decide):
✓ Can Alibaba Cloud APIs query this property? → Automated
✓ Is this a standard Alibaba Cloud service property (encryption, logging, access control, network rules)? → Automated
✓ Does Aliyun CLI SDK have methods to check this? → Automated
✓ Does Alibaba Cloud CLI have commands to retrieve this? → Automated
✓ Does it require SSH/RDP to instances? → Manual
✓ Does audit mention Aliyun CLI/Alibaba Cloud CLI commands? → Automated
✓ Is it about IAM, S3, EC2, VPC, CloudTrail, Config, KMS, etc.? → Automated (Alibaba Cloud APIs expose these)
✓ Is it about application code, OS configs, or visual review? → Manual

IMPORTANT - Policy vs. Technical Distinction:
⚠️ If rationale mentions "organizational policy" or "business decision" → This is POLICY guidance, NOT technical limitation
⚠️ Focus on: Can the property be queried via Alibaba Cloud APIs/Aliyun CLI/CLI?
⚠️ Examples that are ALWAYS Automated:
   - S3 bucket encryption, versioning, logging, public access settings
   - IAM password policies, MFA settings, access keys rotation
   - EC2 security groups, instance metadata service settings
   - CloudTrail logging, KMS key rotation
   - VPC flow logs, network ACLs, security groups
   - RDS encryption, backup settings
⚠️ Examples that are ALWAYS Manual:
   - Application-level security controls
   - SSH to EC2 instances for OS-level checks
   - Visual inspection with human judgment
   - Content review of S3 objects

**MANUAL STEPS:** (Required for Manual approach ONLY)
Provide detailed, step-by-step manual verification instructions:
1. [Exact step with Alibaba Cloud Console path or CLI command]
2. [What to verify/validate]
3. [Expected secure configuration]
4. [How to confirm compliance]

NOTE: Do NOT include a program name or automation details for Manual approach.

**PROGRAM NAME:** (Required ONLY for Automated approach)
Generate an enterprise CSPM-style function name in snake_case following this pattern:
ali_<service>_<resource>_<specific_security_check>

**CRITICAL NAMING RULES:**
1. **Be DESCRIPTIVE and CLEAR** - The name should tell exactly what security aspect is being checked
2. **Format**: ali_<service>_<resource>_<detailed_security_intent>
3. **Service**: Cloud service name
4. **Resource**: Specific resource type
5. **Security Intent**: Be specific about WHAT is being checked - include details like "in_transit", "at_rest", "minimum_version", "retention_period", etc.

**✅ GOOD Examples (CLEAR & DESCRIPTIVE):**
- ali_oss_bucket_encryption_at_rest_enabled
- ali_ram_password_policy_minimum_length_enforced
- ali_ecs_instance_security_group_unrestricted_access
- ali_rds_instance_ssl_encryption_enabled
- ali_ack_cluster_network_policy_enabled

**❌ BAD Examples (TOO VAGUE):**
- ali_storage_bucket_encryption_enabled (vague - encryption of what? in transit? at rest?)
- ali_instance_backup_enabled (vague - just enabled or specific retention?)

**Key Principle:** BE SPECIFIC! If checking TLS version, say "minimum_tls_version". If checking encryption in transit vs at rest, specify it. If checking retention period, say "retention_period". The function name should be self-documenting.


**AUTOMATION DETAILS:** (Required ONLY for Automated approach)
Describe what the automated program would check:
- Alibaba Cloud API calls or Aliyun CLI SDK methods to use
- Alibaba Cloud CLI commands (if applicable)
- Specific resources to enumerate (accounts, regions, buckets, instances, etc.)
- Exact configuration properties/settings to validate
- Clear Pass/Fail criteria with expected values
- Example: "Use Aliyun CLI s3.get_bucket_encryption() to verify ServerSideEncryptionConfiguration exists"

NOTE: Do NOT include automation details for Manual approach.

**SOURCE:** {source_value}

IMPORTANT RULES:
- If Manual: Include ONLY Manual Steps. NO Program Name. NO Automation Details.
- If Automated: Include ONLY Program Name and Automation Details. NO Manual Steps.
- Choose either Manual OR Automated - never both, never mix sections.
- Use ALL CSV fields before deciding - don't rely on just one field.
- If data is incomplete, use your Alibaba Cloud knowledge to fill gaps."""

    def _create(model_name: str):
        return client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            max_completion_tokens=1500,
        )

    try:
        resp = _create(model)
    except openai.NotFoundError:
        if fallback_model:
            logging.warning(f"Primary model '{model}' not found. Falling back to '{fallback_model}'.")
            resp = _create(fallback_model)
        else:
            raise
    except openai.BadRequestError as e:
        logging.error(f"BadRequestError: {e}")
        raise

    if not resp or not getattr(resp, "choices", None):
        raise ValueError("No choices in OpenAI response")

    choice = resp.choices[0]
    message = choice.message if choice.message else None
    if not message:
        raise ValueError("No message in first choice")
    
    content = getattr(message, "content", None)
    if not content or content.strip() == "":
        refusal = getattr(message, "refusal", None)
        if refusal:
            raise ValueError(f"Model refused: {refusal}")
        raise ValueError("Empty message content in OpenAI response")
    
    return content.strip()


def process_csv(
    csv_path: str,
    output_dir: str,
    max_rows: Optional[int],
    model: str,
    fallback_model: Optional[str],
) -> None:
    """Process Alibaba Cloud compliance CSV and generate initial assessments."""
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Alibaba Cloud Agent Step 1 - Initial Assessment")
    logging.info(f"Using output folder: {output_dir}")

    processed = 0
    errors = 0
    consecutive_errors = 0
    max_consecutive_errors = 5

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if max_rows is not None and count >= max_rows:
                break

            control_id = row.get("id") or row.get("control_id") or f"row_{count+1}"
            
            # Use unique_id for filename to avoid overwrites
            filename_id = row.get("unique_id") or control_id
            # Sanitize filename
            filename_id = filename_id.replace("/", "_").replace("\\", "_").replace(" ", "_").replace(":", "_")

            logging.info(f"[{count+1}] Processing: {control_id}")

            try:
                response_text = call_openai_initial_assessment(
                    row=row, 
                    model=model, 
                    fallback_model=fallback_model
                )
                consecutive_errors = 0

                out_path = os.path.join(output_dir, f"{filename_id}.json")
                source_value = row.get("source") or row.get("framework") or "Alibaba Cloud CIS"
                payload = {
                    "control_id": control_id,
                    "unique_id": row.get("unique_id"),
                    "source": source_value,
                    "title": row.get("title", ""),
                    "input_row": row,
                    "step1_initial_assessment": response_text,
                    "timestamp": datetime.now().isoformat(),
                    "model": model,
                }
                with open(out_path, "w", encoding="utf-8") as out:
                    json.dump(payload, out, indent=4, ensure_ascii=False)
                
                logging.info(f"✓ Saved: {out_path}")
                processed += 1
                
            except Exception as e:
                logging.error(f"✗ Failed: {control_id}: {e}")
                errors += 1
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    logging.error("Too many consecutive errors, stopping early")
                    break
                time.sleep(3)

            time.sleep(1.5)
            count += 1

    logging.info("=" * 80)
    logging.info(f"✅ Step 1 Complete!")
    logging.info(f"   Processed: {processed}")
    logging.info(f"   Errors: {errors}")
    logging.info(f"   Total: {count}")
    logging.info(f"   Output: {output_dir}")
    logging.info("=" * 80)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Alibaba Cloud Compliance Agent - Step 1: Initial Assessment")
    parser.add_argument("--csv", default="alicloud_controls.csv", help="Path to Alibaba Cloud compliance CSV")
    parser.add_argument("--max-rows", type=int, default=None, help="Max rows to process")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_output = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        f"output_step1_{timestamp}"
    )
    
    parser.add_argument(
        "--output-dir",
        default=default_output,
        help="Directory for initial assessment outputs",
    )
    parser.add_argument("--model", default="gpt-4.1", help="Primary model name")
    parser.add_argument("--fallback-model", default="gpt-4.1", help="Fallback model")
    return parser.parse_args()


if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY not set in environment")
    
    args = parse_args()
    process_csv(
        csv_path=args.csv,
        output_dir=args.output_dir,
        max_rows=args.max_rows,
        model=args.model,
        fallback_model=args.fallback_model,
    )

