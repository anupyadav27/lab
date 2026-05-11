#!/usr/bin/env python3
"""
K8s Function Generator - Step 1: Generate K8s Functions
Analyzes existing CSP compliance checks and generates equivalent K8s function names.
Uses GPT-4o for intelligent mapping from cloud controls to K8s security controls.
"""

import argparse
import csv
import json
import logging
import os
import time
from typing import Dict, List
from datetime import datetime
from pathlib import Path

import openai
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# K8s Security Knowledge Base
K8S_SECURITY_DOMAINS = """
KUBERNETES SECURITY ARCHITECTURE:

1. **RBAC & Access Control**
   Cloud: IAM roles, policies, users, groups
   K8s: Roles, ClusterRoles, RoleBindings, ClusterRoleBindings, ServiceAccounts
   Pattern: k8s_rbac_<check>
   Examples: k8s_rbac_no_cluster_admin_binding, k8s_rbac_least_privilege_enforcement, k8s_rbac_service_account_token_automount_disabled

2. **Network Security**
   Cloud: Security groups, NACLs, VPC rules
   K8s: NetworkPolicies, Ingress/Egress rules
   Pattern: k8s_networkpolicy_<check>
   Examples: k8s_networkpolicy_default_deny_ingress, k8s_networkpolicy_default_deny_egress, k8s_networkpolicy_pod_selector_defined

3. **Secrets Management & Encryption**
   Cloud: KMS, Key Vault, Secrets Manager
   K8s: Secrets, etcd encryption, external secret managers
   Pattern: k8s_secret_<check> or k8s_etcd_<check>
   Examples: k8s_secret_encryption_at_rest_enabled, k8s_etcd_encryption_enabled, k8s_secret_not_in_env_variables

4. **Audit & Logging**
   Cloud: CloudTrail, Activity Log, Audit logs
   K8s: Kubernetes Audit Logs, API server audit policy
   Pattern: k8s_audit_<check>
   Examples: k8s_audit_logging_enabled, k8s_audit_log_retention_configured, k8s_audit_policy_captures_metadata

5. **Pod Security**
   Cloud: VM/instance security configurations
   K8s: PodSecurityPolicy (deprecated), PodSecurityStandards, SecurityContext
   Pattern: k8s_pod_<check>
   Examples: k8s_pod_security_policy_privileged_disabled, k8s_pod_host_network_disabled, k8s_pod_security_context_non_root

6. **API Server Security**
   Cloud: API Gateway configurations
   K8s: API Server flags, authentication, authorization
   Pattern: k8s_apiserver_<check>
   Examples: k8s_apiserver_authentication_enabled, k8s_apiserver_authorization_mode_rbac, k8s_apiserver_anonymous_auth_disabled

7. **Image Security**
   Cloud: Container registry scanning
   K8s: Image admission policies, scanning integration
   Pattern: k8s_image_<check>
   Examples: k8s_image_scan_on_admission, k8s_image_pull_policy_always, k8s_image_vulnerability_scanning_enabled

8. **etcd Security**
   Cloud: Database encryption, backup
   K8s: etcd encryption, TLS, backup
   Pattern: k8s_etcd_<check>
   Examples: k8s_etcd_encryption_enabled, k8s_etcd_tls_enabled, k8s_etcd_backup_configured

9. **Ingress & Service Mesh**
   Cloud: Load balancers, TLS termination
   K8s: Ingress controllers, Service mesh (Istio/Linkerd)
   Pattern: k8s_ingress_<check> or k8s_service_<check>
   Examples: k8s_ingress_tls_enabled, k8s_service_type_not_nodeport, k8s_ingress_controller_waf_enabled

10. **Admission Control**
    Cloud: Policy enforcement engines
    K8s: Admission Controllers, OPA/Gatekeeper, ValidatingWebhooks
    Pattern: k8s_admission_<check>
    Examples: k8s_admission_controller_pod_security_enabled, k8s_admission_webhook_configured, k8s_admission_deny_latest_image_tag

NAMING GUIDELINES:
✓ Use descriptive, specific names: k8s_rbac_cluster_admin_role_not_used (GOOD) vs k8s_rbac_check (BAD)
✓ Follow pattern: k8s_<resource>_<check_description>
✓ Be consistent with similar checks
✓ Avoid compliance numbers in names
✓ Use underscores, all lowercase
✓ Make it clear what passes/fails

NOT APPLICABLE TO K8S:
✗ Cloud-specific managed services (e.g., specific database services)
✗ Cloud billing/cost management
✗ Cloud-specific monitoring beyond K8s scope
✗ Physical datacenter controls
✗ Some infrastructure-level controls
"""

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(4),
    retry=retry_if_exception_type((openai.APIError, openai.APIConnectionError, openai.RateLimitError))
)
def generate_k8s_functions(control_data: Dict, framework_name: str) -> Dict:
    """Generate K8s functions for a compliance control using GPT-4o."""
    api_key = os.environ["OPENAI_API_KEY"].strip()
    client = OpenAI(api_key=api_key, timeout=90.0)
    
    control_id = control_data.get('id') or control_data.get('Control_ID') or control_data.get('Requirement_ID') or control_data.get('Article_ID', 'Unknown')
    title = control_data.get('title') or control_data.get('Title', '')
    description = control_data.get('description') or control_data.get('Section', '') or control_data.get('Description', '')
    automation_type = control_data.get('automation_type') or control_data.get('Automation_Type', 'manual')
    
    # Collect CSP checks
    csp_checks = []
    for field in ['AWS_Checks', 'Azure_Checks', 'GCP_Checks', 'Oracle_Checks', 'IBM_Checks', 'Alicloud_Checks',
                  'aws_checks', 'azure_checks', 'gcp_checks', 'oracle_checks', 'ibm_checks', 'alicloud_checks']:
        checks = control_data.get(field, '')
        if checks and checks.strip():
            csp_checks.extend([c.strip() for c in checks.split(';') if c.strip()])
    
    # If manual or no checks, skip
    if automation_type.lower() != 'automated' or not csp_checks:
        return {
            "control_id": control_id,
            "k8s_applicable": False,
            "k8s_functions": [],
            "reasoning": "Not automated or no CSP checks available",
            "confidence": "N/A"
        }
    
    control_json = json.dumps(control_data, indent=2)
    csp_sample = '\n'.join([f"  - {check}" for check in csp_checks[:15]])  # Show up to 15 checks
    
    system_message = (
        "You are an expert Kubernetes security architect and compliance specialist. "
        "Your task is to analyze cloud security compliance controls and generate equivalent Kubernetes security check functions. "
        "You have deep knowledge of: K8s RBAC, NetworkPolicies, PodSecurityPolicies/Standards, API server security, "
        "etcd security, admission controllers, service mesh security, and K8s security best practices. "
        "You understand how cloud IAM maps to K8s RBAC, cloud network security to NetworkPolicies, etc."
    )
    
    user_message = f"""FRAMEWORK: {framework_name}
CONTROL: {control_id} - {title}

{K8S_SECURITY_DOMAINS}

CONTROL DETAILS:
{control_json}

CSP SECURITY CHECKS (Sample):
{csp_sample}

TASK:
Analyze this compliance control and generate equivalent Kubernetes security check function names.

DECISION PROCESS:
1. **Understand the Control**: What security requirement is being validated?
2. **Map to K8s Domain**: Which K8s security domain(s) does this apply to?
3. **Check K8s Applicability**: Can this be validated in a K8s environment?
4. **Generate Functions**: Create 1-4 specific K8s function names

EXAMPLES OF GOOD MAPPINGS:
- IAM admin privileges → k8s_rbac_no_cluster_admin_binding, k8s_rbac_least_privilege_enforcement
- Network open to internet → k8s_networkpolicy_default_deny_ingress, k8s_service_type_loadbalancer_restricted
- Encryption at rest → k8s_secret_encryption_at_rest_enabled, k8s_etcd_encryption_enabled
- Audit logging → k8s_audit_logging_enabled, k8s_audit_log_retention_configured
- MFA for users → k8s_rbac_oidc_authentication_configured (if applicable)
- Pod running as root → k8s_pod_security_context_non_root, k8s_pod_security_standard_restricted

OUTPUT REQUIREMENTS:
Return JSON with:
{{
  "k8s_applicable": true/false,
  "k8s_functions": ["list of 1-4 specific function names"],
  "reasoning": "Brief explanation of mapping logic or why not applicable",
  "confidence": "HIGH/MEDIUM/LOW"
}}

CONFIDENCE LEVELS:
- HIGH: Direct K8s equivalent exists (e.g., RBAC checks, NetworkPolicies)
- MEDIUM: K8s has related controls but not exact match
- LOW: Tangentially related or requires custom implementation

IF NOT APPLICABLE:
Set k8s_applicable=false and explain why (e.g., "Cloud-specific billing service", "Physical security control", etc.)

Generate the K8s functions now:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=1000
        )
        
        result = json.loads(response.choices[0].message.content)
        result["control_id"] = control_id
        result["title"] = title
        result["timestamp"] = datetime.now().isoformat()
        
        return result
        
    except Exception as e:
        logging.error(f"Error generating K8s functions for {control_id}: {str(e)}")
        return {
            "control_id": control_id,
            "title": title,
            "k8s_applicable": False,
            "k8s_functions": [],
            "reasoning": f"Error during generation: {str(e)}",
            "confidence": "ERROR",
            "timestamp": datetime.now().isoformat()
        }


def process_compliance_csv(input_csv: str, output_dir: str, framework_name: str):
    """Process compliance CSV and generate K8s functions."""
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Processing {framework_name}: {input_csv}")
    
    # Read CSV
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        controls = list(reader)
    
    logging.info(f"Found {len(controls)} controls")
    
    # Process each control
    results = []
    automated_count = 0
    k8s_applicable_count = 0
    
    for idx, control in enumerate(controls, 1):
        control_id = control.get('id') or control.get('Control_ID') or control.get('Requirement_ID') or control.get('Article_ID', f'Control_{idx}')
        
        logging.info(f"[{idx}/{len(controls)}] Processing: {control_id}")
        
        result = generate_k8s_functions(control, framework_name)
        results.append(result)
        
        # Save individual result
        output_file = Path(output_dir) / f"{control_id.replace('.', '_').replace('/', '_')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        if result.get('k8s_applicable'):
            k8s_applicable_count += 1
        
        # Rate limiting
        time.sleep(0.5)
    
    # Summary
    logging.info(f"\n{'='*80}")
    logging.info(f"STEP 1 COMPLETE - {framework_name}")
    logging.info(f"  Total controls: {len(controls)}")
    logging.info(f"  K8s applicable: {k8s_applicable_count}")
    logging.info(f"  Results saved to: {output_dir}")
    logging.info(f"{'='*80}\n")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Generate K8s functions for compliance controls - Step 1')
    parser.add_argument('--input', required=True, help='Input CSV file path')
    parser.add_argument('--output-dir', required=True, help='Output directory for JSON results')
    parser.add_argument('--framework', required=True, help='Framework name (e.g., NIST_800-171, HIPAA, GDPR)')
    
    args = parser.parse_args()
    
    if not os.getenv('OPENAI_API_KEY'):
        logging.error("OPENAI_API_KEY environment variable not set")
        return 1
    
    process_compliance_csv(args.input, args.output_dir, args.framework)
    return 0


if __name__ == "__main__":
    exit(main())

