#!/usr/bin/env python3
"""
AI-Powered GCP & Azure Function Generator
Uses OpenAI to intelligently create cloud-equivalent compliance functions
"""
import csv
import json
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Service mapping knowledge base
SERVICE_MAPPING_GUIDE = """
Common Cloud Service Equivalents:

AWS → GCP → Azure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CloudTrail → Cloud Logging → Azure Monitor
CloudWatch → Cloud Monitoring → Azure Monitor
S3 → Cloud Storage → Azure Storage (Blob)
IAM → IAM → Microsoft Entra (formerly Azure AD) / IAM
EC2 → Compute Engine → Virtual Machines
RDS → Cloud SQL → Azure SQL Database
KMS → Cloud KMS → Azure Key Vault
VPC → VPC → Virtual Network
ELB/ELB v2 → Cloud Load Balancing → Azure Load Balancer
Lambda → Cloud Functions → Azure Functions
GuardDuty → Security Command Center → Microsoft Defender
SecurityHub → Security Command Center → Microsoft Defender
Config → Cloud Asset Inventory → Azure Policy / Config
SNS → Pub/Sub → Service Bus
DynamoDB → Cloud Datastore/Firestore → Cosmos DB
EFS → Filestore → Azure Files
EMR → Dataproc → HDInsight
EKS → GKE → AKS
Redshift → BigQuery → Azure Synapse
SageMaker → Vertex AI → Azure ML
OpenSearch → Elasticsearch Service → Azure Search
ACM → Certificate Manager → Key Vault
API Gateway → API Gateway → API Management
SSM → Secret Manager → Automation / Key Vault

CSP-Specific Services:
IBM Activity Tracker → GCP Cloud Logging → Azure Monitor
IBM COS → GCP Cloud Storage → Azure Storage
IBM VSI → GCP Compute Engine → Azure VM
Oracle Audit → GCP Cloud Logging → Azure Monitor
Oracle Compute → GCP Compute Engine → Azure VM
Oracle Identity → GCP IAM → Microsoft Entra
Oracle Object Storage → GCP Cloud Storage → Azure Storage
Oracle VCN → GCP VPC → Azure Virtual Network
Alicloud ActionTrail → GCP Cloud Logging → Azure Monitor
Alicloud ECS → GCP Compute Engine → Azure VM
Alicloud OSS → GCP Cloud Storage → Azure Storage
Alicloud RAM → GCP IAM → Microsoft Entra
Alicloud CloudMonitor → GCP Monitoring → Azure Monitor
Alicloud Threat Detection → GCP SCC → Microsoft Defender
"""

def generate_equivalent_functions(aws_functions, context=""):
    """
    Use OpenAI to generate GCP and Azure equivalent functions
    """
    prompt = f"""You are a cloud compliance expert. Given AWS compliance check functions, generate equivalent GCP and Azure functions.

{SERVICE_MAPPING_GUIDE}

Context: {context}

AWS Functions:
{chr(10).join(f"- {func}" for func in aws_functions)}

Generate equivalent functions following these rules:
1. Function format: <csp>_<service>_<check_name>
2. Keep check names semantically equivalent
3. Use appropriate service names for each cloud
4. Maintain the same security check logic intent
5. If a check doesn't apply to a cloud, explain why

Return JSON format:
{{
  "gcp_functions": [list of GCP function names],
  "azure_functions": [list of Azure function names],
  "notes": "Any important differences or caveats"
}}
"""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a cloud security compliance expert specializing in multi-cloud function mapping."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )
    
    return json.loads(response.choices[0].message.content)

def process_framework(csv_path, json_path, framework_name):
    """
    Process a single framework (NIST, GDPR, or HIPAA)
    """
    print(f"\n{'='*80}")
    print(f"Processing: {framework_name}")
    print(f"{'='*80}")
    
    # Read CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Read JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    enhanced_rows = []
    enhanced_json = []
    total_requirements = len(rows)
    
    for idx, row in enumerate(rows, 1):
        req_id = row.get('Requirement_ID', row.get('Control_ID', row.get('Article_ID', 'Unknown')))
        print(f"\n[{idx}/{total_requirements}] Processing: {req_id}")
        
        # Check automation type
        automation_type = row.get('Automation_Type', '').strip().lower()
        
        # Get AWS, IBM, Alicloud, Oracle functions
        aws_checks = row.get('AWS_Checks', '').strip()
        ibm_checks = row.get('IBM_Checks', '').strip()
        alicloud_checks = row.get('Alicloud_Checks', '').strip()
        oracle_checks = row.get('Oracle_Checks', '').strip()
        
        # Parse functions
        aws_funcs = [f.strip() for f in aws_checks.split(';') if f.strip() and f.strip() not in ['', 'N/A', 'None']]
        ibm_funcs = [f.strip() for f in ibm_checks.split(';') if f.strip() and f.strip() not in ['', 'N/A', 'None']]
        alicloud_funcs = [f.strip() for f in alicloud_checks.split(';') if f.strip() and f.strip() not in ['', 'N/A', 'None']]
        oracle_funcs = [f.strip() for f in oracle_checks.split(';') if f.strip() and f.strip() not in ['', 'N/A', 'None']]
        
        # Handle MANUAL requirements
        if automation_type == 'manual':
            print("  📋 MANUAL requirement - no automated checks should exist")
            
            # Validate that AWS also doesn't have functions (data integrity check)
            if aws_funcs:
                print(f"  ⚠️  WARNING: Manual requirement has AWS functions - DATA INCONSISTENCY!")
                print(f"      AWS functions found: {', '.join(aws_funcs[:3])}...")
            
            # Ensure GCP and Azure are empty for manual requirements
            row['GCP_Checks'] = ''
            row['Azure_Checks'] = ''
            enhanced_rows.append(row)
            continue
        
        # Skip if no reference functions found
        if not aws_funcs and not ibm_funcs and not alicloud_funcs:
            print("  ⚠️  No functions found, skipping...")
            row['GCP_Checks'] = ''
            row['Azure_Checks'] = ''
            enhanced_rows.append(row)
            continue
        
        # Create context for AI
        context = f"""
        Requirement: {row.get('Title', '')}
        Description: {row.get('Section', '')}
        """
        
        # Use AWS as primary, fallback to IBM/Alicloud/Oracle
        reference_functions = aws_funcs if aws_funcs else (ibm_funcs if ibm_funcs else (alicloud_funcs if alicloud_funcs else oracle_funcs))
        
        try:
            # Generate equivalents using AI
            result = generate_equivalent_functions(reference_functions, context)
            
            # Update CSV row
            row['GCP_Checks'] = '; '.join(result['gcp_functions'])
            row['Azure_Checks'] = '; '.join(result['azure_functions'])
            
            # Update total count
            current_total = int(row.get('Total_Checks', 0))
            new_total = current_total + len(result['gcp_functions']) + len(result['azure_functions'])
            row['Total_Checks'] = str(new_total)
            
            print(f"  ✅ Generated {len(result['gcp_functions'])} GCP + {len(result['azure_functions'])} Azure functions")
            if result.get('notes'):
                print(f"  📝 Note: {result['notes']}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            row['GCP_Checks'] = ''
            row['Azure_Checks'] = ''
        
        enhanced_rows.append(row)
    
    return enhanced_rows, enhanced_json

def main():
    print("=" * 80)
    print("AI-POWERED GCP & AZURE FUNCTION GENERATOR")
    print("=" * 80)
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("\n❌ ERROR: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        return
    
    frameworks = [
        {
            'name': 'NIST 800-171',
            'csv': 'nist_800_171/NIST_800-171_R2_controls_with_checks.csv',
            'json': 'nist_800_171/NIST_800-171_R2_audit_results.json',
            'output_csv': 'nist_800_171/NIST_800-171_R2_controls_with_checks_ENHANCED.csv',
            'output_json': 'nist_800_171/NIST_800-171_R2_audit_results_ENHANCED.json'
        },
        {
            'name': 'GDPR',
            'csv': 'gdpr/GDPR_controls_with_checks.csv',
            'json': 'gdpr/GDPR_audit_results.json',
            'output_csv': 'gdpr/GDPR_controls_with_checks_ENHANCED.csv',
            'output_json': 'gdpr/GDPR_audit_results_ENHANCED.json'
        },
        {
            'name': 'HIPAA',
            'csv': 'hipaa/HIPAA_controls_with_checks.csv',
            'json': 'hipaa/HIPAA_audit_results.json',
            'output_csv': 'hipaa/HIPAA_controls_with_checks_ENHANCED.csv',
            'output_json': 'hipaa/HIPAA_audit_results_ENHANCED.json'
        }
    ]
    
    summary = {
        'total_requirements': 0,
        'manual_requirements': 0,
        'automated_requirements': 0,
        'enhanced_requirements': 0,
        'data_inconsistencies': 0
    }
    
    for framework in frameworks:
        enhanced_rows, enhanced_json = process_framework(
            framework['csv'],
            framework['json'],
            framework['name']
        )
        
        # Count statistics
        for row in enhanced_rows:
            summary['total_requirements'] += 1
            automation_type = row.get('Automation_Type', '').strip().lower()
            
            if automation_type == 'manual':
                summary['manual_requirements'] += 1
                # Check for data inconsistency
                aws_checks = row.get('AWS_Checks', '').strip()
                aws_funcs = [f.strip() for f in aws_checks.split(';') if f.strip() and f.strip() not in ['', 'N/A', 'None']]
                if aws_funcs:
                    summary['data_inconsistencies'] += 1
            elif automation_type == 'automated':
                summary['automated_requirements'] += 1
                # Check if GCP/Azure were populated
                gcp_checks = row.get('GCP_Checks', '').strip()
                azure_checks = row.get('Azure_Checks', '').strip()
                if gcp_checks or azure_checks:
                    summary['enhanced_requirements'] += 1
        
        # Save enhanced CSV
        with open(framework['output_csv'], 'w', encoding='utf-8', newline='') as f:
            if enhanced_rows:
                writer = csv.DictWriter(f, fieldnames=enhanced_rows[0].keys())
                writer.writeheader()
                writer.writerows(enhanced_rows)
        
        print(f"\n✅ Saved: {framework['output_csv']}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 ENHANCEMENT SUMMARY")
    print("=" * 80)
    print(f"Total Requirements:       {summary['total_requirements']}")
    print(f"  └─ Manual:              {summary['manual_requirements']} (no functions generated)")
    print(f"  └─ Automated:           {summary['automated_requirements']}")
    print(f"     └─ Enhanced:         {summary['enhanced_requirements']} (GCP/Azure added)")
    
    if summary['data_inconsistencies'] > 0:
        print(f"\n⚠️  Data Inconsistencies:   {summary['data_inconsistencies']}")
        print(f"    Manual requirements with AWS functions - needs review!")
    else:
        print(f"\n✅ Data Consistency:      All manual requirements have no functions")
    
    print("\n" + "=" * 80)
    print("✅ ENHANCEMENT COMPLETE!")
    print("=" * 80)

if __name__ == '__main__':
    main()

