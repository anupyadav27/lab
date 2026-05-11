import argparse
import csv
import json
import logging
import os
import time
from typing import Dict, Optional

import openai
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@retry(
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(4),
    retry=retry_if_exception_type((openai.APIError, openai.APIConnectionError, openai.RateLimitError))
)
def call_openai_with_full_row(row: Dict[str, str], model: str, fallback_model: Optional[str]) -> str:
    """Call the Chat Completions API with the full CSV row (as JSON) and return text output."""
    api_key = os.environ["OPENAI_API_KEY"].strip()
    os.environ["OPENAI_API_KEY"] = api_key
    client = OpenAI(api_key=api_key, timeout=60.0)

    # Build enterprise-grade CSPM audit instruction
    source_value = row.get("source") or row.get("framework") or row.get("standard") or ""
    row_json = json.dumps(row, ensure_ascii=False)
    
    system_message = (
        "You are an enterprise-grade Cloud Security Posture Management (CSPM) compliance audit engine for Azure resources. "
        "Analyze compliance controls and determine the optimal audit approach following industry standards used by tools like Wiz, Orca, and Prowler. "
        "Use ALL available fields (description, rationale, audit, remediation, impact, references) to make informed decisions. "
        "If any field is missing or unclear, use your knowledge of Azure APIs and the referenced documentation to determine if the control is API-checkable."
    )

    user_message = f"""Source: {source_value}

Input Control (JSON):
{row_json}

INSTRUCTIONS:
Analyze the control using ALL available data to determine the optimal audit approach.

DECISION PROCESS:
1. Read ALL fields: description, rationale, audit, remediation, impact, references
2. If audit field is empty/incomplete, analyze description + remediation + references
3. Consider Azure architecture: What Azure APIs exist for this resource type?
4. Use your training knowledge + referenced documentation URLs
5. Make an informed decision based on complete context

**AUDIT APPROACH:** [Choose ONE: Manual | Automated]

**APPROACH DECISION:**
- **Automated:** Control can be fully verified via Azure Resource Manager APIs/CLI/SDK/PowerShell
  Examples: Storage account properties, network rules, encryption settings, backup vault configs
  
- **Manual:** Control requires human judgment, SSH access, or checks not exposed via Azure APIs
  Examples: SAS token policy review, node file system access, visual portal inspection

DECISION CRITERIA (Use ALL to decide):
✓ Can Azure ARM APIs query this property? → Automated
✓ Is this a standard Azure resource property (encryption, networkAcls, publicAccess, etc.)? → Automated
✓ Does it require SSH/file system access to nodes? → Manual
✓ Does audit mention API/CLI commands? → Automated
✓ Is it about encryption/network/backup/access control settings? → Automated (Azure APIs expose these)
✓ Is it about SAS token policies, content inspection, or visual review? → Manual

IMPORTANT - Policy vs. Technical Distinction:
⚠️ If rationale mentions "remains Manual due to limited scope" or "organizational capacity" → This is POLICY guidance, NOT technical limitation
⚠️ Ignore policy-related "Manual" mentions in rationale - focus on: Can the property be queried via Azure APIs?
⚠️ Examples that are ALWAYS Automated:
   - Encryption settings (keySource: Microsoft.Storage vs Microsoft.Keyvault)
   - Network access rules (publicNetworkAccess, defaultAction)
   - Backup vault configurations (softDelete, immutability)
   - Key Vault properties (any Key Vault setting)
⚠️ Examples that are ALWAYS Manual:
   - SAS token expiry policy review (not exposed via API)
   - SSH to Kubernetes nodes for file checks
   - Visual portal inspection with human judgment

**MANUAL STEPS:** (Required for Manual approach)
Provide detailed, step-by-step manual verification instructions:
1. [Exact step with Azure portal path or CLI command]
2. [What to verify/validate]
3. [Expected secure configuration]
4. [How to confirm compliance]

NOTE: Do NOT include a program name for Manual approach. Programs are only for Automated checks.

**PROGRAM NAME:** (Required ONLY for Automated approach)
Generate an enterprise CSPM-style function name in snake_case following this pattern:
azure_<service>_<resource>_<security_intent>

Examples:
- azure_aks_diagnostics_audit_logs_enabled
- azure_kubernetes_rbac_least_privilege_enforced
- azure_aks_network_policy_configured
- azure_keyvault_secrets_rotation_enabled
- azure_storage_account_https_only_enabled

Rules for program names:
- Start with 'azure_'
- Use actual Azure service name (aks, keyvault, storage, vm, network, etc.)
- Include specific resource type if applicable
- End with clear security intent (enabled/disabled/enforced/configured/restricted/verified)
- Keep concise but descriptive (max 6-7 words)
- Use snake_case throughout

**AUTOMATION DETAILS:** (Required ONLY for Automated approach)
Describe what the automated program would check:
- Azure Resource Manager APIs or Azure CLI commands to use
- Specific resources to enumerate (subscriptions, resource groups, clusters, etc.)
- Exact configuration properties/settings to validate
- Clear Pass/Fail criteria with expected values
- Example API endpoint or CLI command

NOTE: Do NOT include automation details for Manual approach.

**SOURCE:** {source_value}

IMPORTANT RULES:
- If Manual: Include ONLY Manual Steps. NO Program Name. NO Automation Details.
- If Automated: Include ONLY Program Name and Automation Details. NO Manual Steps.
- Choose either Manual OR Automated - never both, never mix sections."""

    def _create(model_name: str):
        return client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            max_completion_tokens=1200,
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
        logging.error(f"Model: {model}")
        logging.error(f"System message length: {len(system_message)}")
        logging.error(f"User message length: {len(user_message)}")
        raise

    if not resp or not getattr(resp, "choices", None):
        logging.error(f"Response object: {resp}")
        raise ValueError("No choices in OpenAI response")

    choice = resp.choices[0]
    finish_reason = getattr(choice, 'finish_reason', None)
    logging.info(f"Choice finish_reason: {finish_reason}")
    
    message = choice.message if choice.message else None
    if not message:
        raise ValueError("No message in first choice")
    
    # Try multiple content accessors
    content = getattr(message, "content", None)
    
    # Check annotations field for GPT-5 responses
    annotations = getattr(message, "annotations", [])
    if annotations:
        logging.info(f"Found {len(annotations)} annotations")
        # Try extracting text from annotations
        for ann in annotations:
            ann_text = getattr(ann, "text", None) or getattr(ann, "content", None)
            if ann_text:
                content = (content or "") + "\n" + str(ann_text)
    
    if not content or content.strip() == "":
        # Check for refusal or other fields
        refusal = getattr(message, "refusal", None)
        if refusal:
            raise ValueError(f"Model refused: {refusal}")
        logging.error(f"Finish reason: {finish_reason}")
        logging.error(f"Message object: {message}")
        logging.error(f"Message dict: {message.model_dump() if hasattr(message, 'model_dump') else 'N/A'}")
        raise ValueError("Empty message content in OpenAI response")
    return content.strip()


def process_csv(
    csv_path: str,
    output_dir: str,
    max_rows: Optional[int],
    model: str,
    fallback_model: Optional[str],
) -> None:
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Using output folder: {output_dir}")

    processed = 0
    errors = 0
    consecutive_errors = 0
    max_consecutive_errors = 5

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if max_rows is not None and count >= max_rows:
                break

            control_id = row.get("id") or row.get("control_id")
            if not control_id:
                # fallback slug from title
                title = (row.get("title") or "untitled").lower().replace(" ", "_").replace("/", "_")
                control_id = f"row_{count+1}_{title[:30]}"

            # Use unique_id for filename to avoid overwrites
            filename_id = row.get("unique_id") or control_id
            # Sanitize filename
            filename_id = filename_id.replace("/", "_").replace("\\", "_").replace(" ", "_")

            logging.info(f"Processing: {control_id}")

            try:
                response_text = call_openai_with_full_row(row=row, model=model, fallback_model=fallback_model)
                consecutive_errors = 0

                out_path = os.path.join(output_dir, f"{filename_id}.json")
                payload = {
                    "id": control_id,
                    "source": row.get("source") or row.get("framework") or row.get("standard"),
                    "input_row": row,
                    "gpt_response": response_text,
                }
                with open(out_path, "w") as out:
                    json.dump(payload, out, indent=4, ensure_ascii=False)
                logging.info(f"Wrote: {out_path}")
                processed += 1
            except Exception as e:
                logging.error(f"Failed: {control_id}: {e}")
                errors += 1
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    logging.error("Too many consecutive errors, stopping early")
                    break
                time.sleep(3)

            time.sleep(1.5)
            count += 1

    logging.info(f"Done. Processed={processed} Errors={errors} Total={count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Azure compliance audit agent (Responses API)")
    parser.add_argument("--csv", default="controls_batch_cleaned.csv", help="Path to CSV input (use cleaned version without assessment column)")
    parser.add_argument("--max-rows", type=int, default=None, help="Max rows to process")
    
    # Default output dir with timestamp version
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_output = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"output_v{timestamp}")
    
    parser.add_argument(
        "--output-dir",
        default=default_output,
        help="Directory to write per-row JSON outputs (defaults to output_v{timestamp})",
    )
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"), help="Primary model name")
    parser.add_argument(
        "--fallback-model",
        default=os.environ.get("OPENAI_FALLBACK_MODEL", "gpt-4o-mini"),
        help="Fallback model name if primary is unavailable",
    )
    return parser.parse_args()


if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY not set in environment")
    os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"].strip()

    args = parse_args()
    process_csv(
        csv_path=args.csv,
        output_dir=args.output_dir,
        max_rows=args.max_rows,
        model=args.model,
        fallback_model=args.fallback_model,
    )


