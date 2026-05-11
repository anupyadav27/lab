#!/usr/bin/env python3
"""
AI-Powered K8s Function Generator for Non-CIS Compliance Frameworks
Generates K8s equivalent functions based on existing CSP checks
"""
import csv
import json
import os
import sys
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# K8s mapping knowledge base
K8S_MAPPING_GUIDE = """
Kubernetes Security Concepts & Compliance Mapping:

1. **RBAC & Access Control**
   - IAM/Identity → K8s RBAC (Roles, ClusterRoles, RoleBindings)
   - User/Group Access → ServiceAccounts, RBAC policies
   - Function pattern: k8s_rbac_<check_type>

2. **Network Security**
   - Security Groups → NetworkPolicies
   - VPC/Network → NetworkPolicies, PodSecurityPolicy
   - Function pattern: k8s_networkpolicy_<check_type>

3. **Secrets & Encryption**
   - KMS/Secrets → K8s Secrets, encryption at rest
   - Certificate Management → cert-manager, TLS secrets
   - Function pattern: k8s_secret_<check_type>

4. **Audit & Logging**
   - CloudTrail/Audit logs → K8s Audit logs
   - Logging → Pod logs, cluster logging
   - Function pattern: k8s_audit_<check_type>

5. **Pod Security**
   - EC2/VM security → PodSecurityPolicy, SecurityContext
   - Container security → Pod security standards
   - Function pattern: k8s_pod_<check_type>

6. **API Server Security**
   - API Gateway → API Server configuration
   - Authentication → API server auth mechanisms
   - Function pattern: k8s_apiserver_<check_type>

7. **Configuration Management**
   - Config Recorder → ConfigMaps, admission controllers
   - Policy enforcement → OPA, Gatekeeper
   - Function pattern: k8s_config_<check_type>

8. **Image Security**
   - ECR/Container Registry → Image scanning, admission
   - Image policies → ImagePolicyWebhook
   - Function pattern: k8s_image_<check_type>

9. **etcd Security**
   - Database encryption → etcd encryption at rest
   - Database backup → etcd backup and HA
   - Function pattern: k8s_etcd_<check_type>

10. **Service Mesh & Ingress**
    - Load Balancer → Ingress controllers, Service mesh
    - TLS/SSL → Ingress TLS, mTLS
    - Function pattern: k8s_ingress_<check_type> or k8s_service_<check_type>

Naming Convention:
- Format: k8s_<resource>_<check_type>
- Examples:
  * k8s_rbac_least_privilege_enforcement
  * k8s_networkpolicy_deny_default_ingress
  * k8s_pod_security_policy_privileged_disabled
  * k8s_apiserver_authentication_enabled
  * k8s_secret_encryption_at_rest_enabled
  * k8s_audit_logging_enabled
  * k8s_image_scan_on_admission
  * k8s_etcd_encryption_enabled

Important Guidelines:
- Use descriptive names that reflect the check purpose
- Focus on K8s-native security controls
- Some cloud-specific checks may not have K8s equivalents
- K8s has different security models than cloud platforms
"""

def generate_k8s_functions(control_id, title, description, aws_checks="", azure_checks="", gcp_checks="", 
                           oracle_checks="", ibm_checks="", alicloud_checks=""):
    """
    Use OpenAI to generate K8s equivalent functions based on CSP checks and control description
    """
    # Combine all CSP checks
    all_csp_checks = []
    for checks in [aws_checks, azure_checks, gcp_checks, oracle_checks, ibm_checks, alicloud_checks]:
        if checks and checks.strip():
            all_csp_checks.extend([c.strip() for c in checks.split(';') if c.strip()])
    
    # If no CSP checks, skip
    if not all_csp_checks:
        return []
    
    prompt = f"""You are a Kubernetes security expert. Generate Kubernetes-equivalent compliance check functions based on cloud provider checks and control requirements.

{K8S_MAPPING_GUIDE}

Control ID: {control_id}
Control Title: {title}
Control Description: {description[:500] if description else "N/A"}

Cloud Provider Checks:
{chr(10).join(f"- {check}" for check in all_csp_checks[:10])}  # Limit to first 10 for brevity

Task:
Generate equivalent Kubernetes security check function names that would validate the same security requirements in a Kubernetes environment.

Rules:
1. Follow the naming pattern: k8s_<resource>_<check_type>
2. Be descriptive and specific about what is being checked
3. Use K8s-native resources (RBAC, NetworkPolicy, PodSecurityPolicy, etc.)
4. If a check doesn't apply to K8s (e.g., cloud-specific service), return empty list
5. Focus on automatable checks that can be verified through kubectl or K8s API
6. Return 1-5 most relevant K8s functions (don't over-generate)

Return JSON format:
{{
  "k8s_functions": ["list of K8s function names"],
  "reasoning": "Brief explanation of why these functions were chosen or if N/A"
}}

Example outputs:
- For IAM privilege checks: ["k8s_rbac_no_cluster_admin_binding", "k8s_rbac_least_privilege_enforcement"]
- For network security: ["k8s_networkpolicy_default_deny_ingress", "k8s_networkpolicy_default_deny_egress"]
- For encryption: ["k8s_secret_encryption_at_rest_enabled", "k8s_etcd_encryption_enabled"]
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Kubernetes security and compliance expert specializing in translating cloud security controls to K8s equivalents."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=800
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("k8s_functions", [])
    
    except Exception as e:
        print(f"  ⚠️  Error generating K8s functions for {control_id}: {str(e)}")
        return []

def process_csv_file(csv_path):
    """
    Process a compliance CSV file and add K8s_Checks column
    """
    print(f"\n📄 Processing: {csv_path}")
    
    # Read the CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    
    if not rows:
        print("  ⚠️  Empty CSV file, skipping")
        return
    
    # Check if K8s_Checks column already exists
    if 'K8s_Checks' in fieldnames:
        print("  ℹ️  K8s_Checks column already exists, skipping")
        return
    
    # Determine position to insert K8s_Checks (after Alicloud_Checks, before Total_Checks)
    insert_position = len(fieldnames) - 1 if 'Total_Checks' in fieldnames else len(fieldnames)
    new_fieldnames = list(fieldnames[:insert_position]) + ['K8s_Checks'] + list(fieldnames[insert_position:])
    
    print(f"  ✓ Found {len(rows)} controls")
    
    # Process each row
    updated_rows = []
    automated_count = 0
    k8s_generated_count = 0
    
    for idx, row in enumerate(rows, 1):
        # Check if automated
        automation_type = row.get('Automation_Type', row.get('automation_type', '')).lower()
        
        if automation_type != 'automated':
            # Manual or empty - no K8s checks
            row['K8s_Checks'] = ''
            updated_rows.append(row)
            continue
        
        automated_count += 1
        
        # Get control details
        control_id = row.get('Control_ID', row.get('Requirement_ID', row.get('Article_ID', row.get('id', ''))))
        title = row.get('Title', row.get('title', ''))
        description = row.get('Section', row.get('Description', row.get('description', '')))
        
        # Get CSP checks
        aws_checks = row.get('AWS_Checks', row.get('aws_checks', ''))
        azure_checks = row.get('Azure_Checks', row.get('azure_checks', ''))
        gcp_checks = row.get('GCP_Checks', row.get('gcp_checks', ''))
        oracle_checks = row.get('Oracle_Checks', row.get('oracle_checks', ''))
        ibm_checks = row.get('IBM_Checks', row.get('ibm_checks', ''))
        alicloud_checks = row.get('Alicloud_Checks', row.get('alicloud_checks', ''))
        
        print(f"  🔄 [{idx}/{len(rows)}] Generating K8s functions for: {control_id} - {title[:60]}")
        
        # Generate K8s functions
        k8s_functions = generate_k8s_functions(
            control_id, title, description,
            aws_checks, azure_checks, gcp_checks,
            oracle_checks, ibm_checks, alicloud_checks
        )
        
        if k8s_functions:
            row['K8s_Checks'] = '; '.join(k8s_functions)
            k8s_generated_count += 1
            print(f"     ✓ Generated {len(k8s_functions)} K8s function(s)")
        else:
            row['K8s_Checks'] = ''
            print(f"     - No K8s equivalent")
        
        updated_rows.append(row)
    
    # Update Total_Checks if it exists
    if 'Total_Checks' in new_fieldnames:
        for row in updated_rows:
            if row.get('K8s_Checks'):
                k8s_count = len([f for f in row['K8s_Checks'].split(';') if f.strip()])
                current_total = int(row.get('Total_Checks', 0))
                row['Total_Checks'] = str(current_total + k8s_count)
    
    # Write back to CSV
    output_path = csv_path.replace('.csv', '_WITH_K8S.csv')
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)
    
    print(f"\n  ✅ Complete!")
    print(f"     - Total controls: {len(rows)}")
    print(f"     - Automated controls: {automated_count}")
    print(f"     - K8s functions generated: {k8s_generated_count}")
    print(f"     - Output saved to: {output_path}")

def main():
    """Main execution"""
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Define compliance frameworks to process (excluding CIS)
    compliance_frameworks = [
        'nist_800_171/NIST_800-171_R2_controls_with_checks.csv',
        'hipaa/HIPAA_controls_with_checks.csv',
        'gdpr/GDPR_controls_with_checks.csv',
        'pci_compliance_agent/PCI_controls_with_checks.csv',
        'soc2/SOC2_controls_with_checks.csv',
        'iso27001-2022/ISO27001_2022_controls_with_checks.csv',
        'FedRamp/FedRAMP_controls_with_checks.csv',
        'nist_complaince_agent/NIST_controls_with_checks.csv',
        'rbi_bank/RBI_BANK_controls_with_checks.csv',
        'rbi_nbfc/RBI_NBFC_controls_with_checks.csv',
        'cisa_ce/CISA_CE_controls_with_checks.csv',
        'canada_pbmm/CANADA_PBMM_controls_with_checks.csv',
    ]
    
    base_path = Path(__file__).parent
    
    print("=" * 80)
    print("🚀 K8s Function Generator for Non-CIS Compliance Frameworks")
    print("=" * 80)
    
    for framework in compliance_frameworks:
        csv_path = base_path / framework
        if csv_path.exists():
            try:
                process_csv_file(str(csv_path))
            except Exception as e:
                print(f"\n❌ Error processing {framework}: {str(e)}")
                import traceback
                traceback.print_exc()
        else:
            print(f"\n⚠️  File not found: {csv_path}")
    
    print("\n" + "=" * 80)
    print("✅ All frameworks processed!")
    print("=" * 80)

if __name__ == "__main__":
    main()

