#!/usr/bin/env python3
"""
Test script to run K8s function generation on a single framework
"""
import csv
import json
import os
import sys
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

K8S_MAPPING_GUIDE = """
Kubernetes Security Concepts & Compliance Mapping:

1. **RBAC & Access Control**
   - IAM/Identity → K8s RBAC (Roles, ClusterRoles, RoleBindings)
   - Function pattern: k8s_rbac_<check_type>

2. **Network Security**
   - Security Groups → NetworkPolicies
   - Function pattern: k8s_networkpolicy_<check_type>

3. **Secrets & Encryption**
   - KMS/Secrets → K8s Secrets, encryption at rest
   - Function pattern: k8s_secret_<check_type>

4. **Audit & Logging**
   - CloudTrail/Audit logs → K8s Audit logs
   - Function pattern: k8s_audit_<check_type>

5. **Pod Security**
   - EC2/VM security → PodSecurityPolicy, SecurityContext
   - Function pattern: k8s_pod_<check_type>

6. **API Server Security**
   - API Gateway → API Server configuration
   - Function pattern: k8s_apiserver_<check_type>

Naming Convention:
- Format: k8s_<resource>_<check_type>
- Examples: k8s_rbac_least_privilege, k8s_networkpolicy_deny_default, k8s_secret_encryption_enabled
"""

def generate_k8s_functions(control_id, title, aws_checks="", oracle_checks=""):
    """Generate K8s functions"""
    all_checks = []
    for checks in [aws_checks, oracle_checks]:
        if checks and checks.strip():
            all_checks.extend([c.strip() for c in checks.split(';') if c.strip()])
    
    if not all_checks:
        return []
    
    prompt = f"""Generate Kubernetes-equivalent compliance check functions.

{K8S_MAPPING_GUIDE}

Control: {control_id} - {title}
CSP Checks: {', '.join(all_checks[:5])}

Return JSON: {{"k8s_functions": ["list"], "reasoning": "brief explanation"}}

Rules:
- Use pattern: k8s_<resource>_<check_type>
- Return 1-3 most relevant functions
- Return empty list if not applicable to K8s
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Kubernetes security expert."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=500
        )
        
        result = json.loads(response.choices[0].message.content)
        print(f"  Result: {result}")
        return result.get("k8s_functions", [])
    
    except Exception as e:
        print(f"  Error: {str(e)}")
        return []

# Test with GDPR
csv_path = '/Users/apple/Desktop/compliance_Database/compliance_agent/gdpr/GDPR_controls_with_checks.csv'

print(f"Testing with: {csv_path}\n")

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Found {len(rows)} rows\n")

# Test on first automated row
for row in rows[:5]:  # Test first 5 rows
    if row.get('Automation_Type', '').lower() == 'automated':
        control_id = row.get('Article_ID', '')
        title = row.get('Title', '')
        aws_checks = row.get('AWS_Checks', '')
        oracle_checks = row.get('Oracle_Checks', '')
        
        print(f"\n{'='*80}")
        print(f"Control: {control_id}")
        print(f"Title: {title[:80]}")
        print(f"AWS Checks (sample): {aws_checks[:150]}...")
        print(f"\nGenerating K8s functions...")
        
        k8s_funcs = generate_k8s_functions(control_id, title, aws_checks, oracle_checks)
        print(f"K8s Functions: {k8s_funcs}")
        
        break  # Just test one for now

