#!/usr/bin/env python3
"""
Kubernetes Compliance Agent - Step 1: Initial Assessment
Uses gpt-4o-mini to analyze Kubernetes CIS compliance controls and determine audit approach.
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
    """Call OpenAI for initial Kubernetes compliance assessment."""
    api_key = os.environ["OPENAI_API_KEY"].strip()
    client = OpenAI(api_key=api_key, timeout=60.0)

    source_value = row.get("source") or row.get("framework") or row.get("standard") or "Kubernetes CIS"
    row_json = json.dumps(row, ensure_ascii=False, indent=2)
    
    system_message = (
        "You are an enterprise-grade Kubernetes security expert and CSPM engine. "
        "Default to Automated whenever a control can be evaluated via Kubernetes APIs, kubectl, or controller/state configs. "
        "Only choose Manual when verification truly requires human judgement or in-guest OS access not exposed via the Kubernetes API."
    )

    user_message = f"""Source: {source_value}

Input Control (JSON):
{row_json}

INSTRUCTIONS:
Analyze this Kubernetes compliance control using ALL available data to determine the optimal audit approach.

DECISION PROCESS:
1. Read ALL fields: id, title, description, rationale, audit, remediation, impact, references
2. If audit is weak, use description + remediation + references
3. Map the control to Kubernetes API objects, flags, or policies
4. If kubectl or the Kubernetes API exposes the property → Automated
5. Use concrete kubectl/API calls and object fields when Automated
6. Choose Manual ONLY if it requires subjective review or non-API host access

**AUDIT APPROACH:** [Choose ONE: Manual | Automated]

**APPROACH DECISION:**
- **Automated:** Verifiable via Kubernetes API/kubectl/controller config without human judgement
  Examples (Kubernetes-specific):
  - API server flags (anonymous-auth, basic-auth, admission plugins, audit logging)
  - Kubelet config (read-only-port, anonymous-auth, TLS settings)
  - RBAC (ClusterRole/Role/Binding presence, wildcard usage restrictions)
  - Pod Security Admission/PSP replacements (privileged, hostPID/IPC/Network)
  - NetworkPolicy defaults and namespace isolation
  - Etcd encryption config, audit policy file refs (from API server args)
  
- **Manual:** Requires subjective visual review or host/OS checks not available via Kubernetes API
  Examples: Business policy wording, application-level logic, in-pod file content review

DECISION CRITERIA (Use ALL to decide):
✓ Can Kubernetes APIs query this property? → Automated
✓ Is this a standard Kubernetes service property (encryption, logging, access control, network rules)? → Automated
✓ Does kubectl SDK have methods to check this? → Automated
✓ Does Kubernetes CLI have commands to retrieve this? → Automated
✓ Does it require SSH/RDP to instances? → Manual
✓ Does audit mention kubectl/Kubernetes CLI commands? → Automated
✓ Is it about IAM, S3, EC2, VPC, CloudTrail, Config, KMS, etc.? → Automated (Kubernetes APIs expose these)
✓ Is it about application code, OS configs, or visual review? → Manual

IMPORTANT - Policy vs. Technical Distinction:
⚠️ If rationale mentions "organizational policy" or "business decision" → This is POLICY guidance, NOT technical limitation
⚠️ Focus on: Can the property be queried via Kubernetes APIs/kubectl/CLI?
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
1. [Exact step with Kubernetes Console path or CLI command]
2. [What to verify/validate]
3. [Expected secure configuration]
4. [How to confirm compliance]

NOTE: Do NOT include a program name or automation details for Manual approach.

**PROGRAM NAME:** (Required ONLY for Automated approach)
Generate an enterprise CSPM-style function name in snake_case following this pattern:
k8s_<service>_<resource>_<specific_security_check>

**CRITICAL NAMING RULES:**
1. Be descriptive and clear – the name must self-document the exact check
2. Format: k8s_<resource>_<specific_security_check>
3. Resource: valid Kubernetes component/resource (api_server, kubelet, rbac, network_policy, pod_security, etc.)
4. Security intent: include specifics like minimum_tls_version, privileged_containers_restricted, default_deny_ingress
5. Do NOT include compliance numbers; do NOT use non-K8s resources like "account" [[memory:8432258]]

**✅ GOOD Examples (CLEAR & DESCRIPTIVE):**
- k8s_api_server_anonymous_auth_disabled
- k8s_api_server_admission_plugins_required_set
- k8s_kubelet_read_only_port_disabled
- k8s_rbac_wildcard_permissions_restricted
- k8s_network_policy_default_deny_ingress_configured
- k8s_pod_security_privileged_containers_restricted

**❌ BAD Examples (TOO VAGUE):**
- k8s_storage_bucket_encryption_enabled (vague - encryption of what? in transit? at rest?)
- k8s_instance_backup_enabled (vague - just enabled or specific retention?)

**Key Principle:** BE SPECIFIC! If checking TLS version, say "minimum_tls_version". If checking encryption in transit vs at rest, specify it. If checking retention period, say "retention_period". The function name should be self-documenting.


**AUTOMATION DETAILS:** (Required ONLY for Automated approach)
Describe what the automated program would check:
- Kubernetes API calls or kubectl SDK methods to use
- Kubernetes CLI commands (if applicable)
- Specific resources to enumerate (accounts, regions, buckets, instances, etc.)
- Exact configuration properties/settings to validate
- Clear Pass/Fail criteria with expected values
- Example: "Use kubectl s3.get_bucket_encryption() to verify ServerSideEncryptionConfiguration exists"

NOTE: Do NOT include automation details for Manual approach.

**SOURCE:** {source_value}

IMPORTANT RULES:
- If Manual: Include ONLY Manual Steps. NO Program Name. NO Automation Details.
- If Automated: Include ONLY Program Name and Automation Details. NO Manual Steps.
- Choose either Manual OR Automated - never both, never mix sections.
- Use ALL CSV fields before deciding - don't rely on just one field.
- If data is incomplete, use your Kubernetes knowledge to fill gaps."""

    def _create(model_name: str):
        return client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            max_completion_tokens=1500,
            temperature=0.2,
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
    """Process Kubernetes compliance CSV and generate initial assessments."""
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Kubernetes Agent Step 1 - Initial Assessment")
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
                source_value = row.get("source") or row.get("framework") or "Kubernetes CIS"
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
    parser = argparse.ArgumentParser(description="Kubernetes Compliance Agent - Step 1: Initial Assessment")
    parser.add_argument("--csv", default="k8s_controls.csv", help="Path to Kubernetes compliance CSV")
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

