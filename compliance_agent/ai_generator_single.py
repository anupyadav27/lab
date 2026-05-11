#!/usr/bin/env python3
"""
AI-Powered GCP & Azure Function Generator - Single Framework
Process one compliance framework at a time for focused AI context
"""
import csv
import json
import os
import sys
from openai import OpenAI

# Initialize OpenAI client (strip any whitespace/newlines from API key)
api_key = os.getenv('OPENAI_API_KEY', '').strip()
client = OpenAI(api_key=api_key)

# Service mapping knowledge base
SERVICE_MAPPING_GUIDE = """
Common Cloud Service Equivalents:

AWS → GCP → Azure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
CloudFront → Cloud CDN → Azure CDN

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

def generate_equivalent_functions(reference_functions, context="", framework=""):
    """
    Use OpenAI to generate GCP and Azure equivalent functions
    """
    prompt = f"""You are a cloud compliance expert specializing in {framework} compliance framework.

{SERVICE_MAPPING_GUIDE}

Context: {context}

Reference Functions (from AWS/IBM/Alicloud/Oracle):
{chr(10).join(f"- {func}" for func in reference_functions)}

Generate EXACT equivalent functions for GCP and Azure following these STRICT rules:

1. **Function Format**: <csp>_<service>_<check_name>
   - Example: aws_cloudtrail_enabled → gcp_logging_enabled, azure_monitor_enabled

2. **Service Mapping**: Use the service mapping guide above
   - CloudTrail → Cloud Logging (GCP), Azure Monitor (Azure)
   - S3 → Cloud Storage (GCP), Azure Storage (Azure)

3. **Check Name**: Keep semantic meaning, not literal translation
   - kms_encryption_enabled → kms_encryption_enabled (GCP), keyvault_encryption_enabled (Azure)
   - multi_region_enabled → multi_region_enabled (both)

4. **Compliance Intent**: Maintain the SAME security check purpose
   - If checking encryption at rest → ensure equivalent check exists
   - If checking logging enabled → ensure equivalent logging check

5. **Service Differences**: Note any significant differences
   - Example: Azure uses TDE for SQL encryption vs AWS RDS encryption

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "gcp_functions": ["list", "of", "gcp", "functions"],
  "azure_functions": ["list", "of", "azure", "functions"],
  "notes": "Brief explanation of any significant differences or mappings"
}}
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using mini for faster and cheaper processing
        messages=[
            {"role": "system", "content": f"You are a cloud security compliance expert specializing in {framework} framework mapping across AWS, GCP, and Azure."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2  # Lower temperature for more consistent results
    )
    
    return json.loads(response.choices[0].message.content)

def process_framework(csv_path, framework_name):
    """
    Process a single framework
    """
    print(f"\n{'='*80}")
    print(f"Processing: {framework_name}")
    print(f"{'='*80}")
    
    # Read CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    enhanced_rows = []
    total_requirements = len(rows)
    
    # Statistics
    stats = {
        'total': total_requirements,
        'manual': 0,
        'automated': 0,
        'enhanced': 0,
        'skipped': 0,
        'errors': 0,
        'inconsistencies': []
    }
    
    for idx, row in enumerate(rows, 1):
        req_id = row.get('Requirement_ID', row.get('Control_ID', row.get('Article_ID', 'Unknown')))
        print(f"\n[{idx}/{total_requirements}] {req_id}")
        
        # Check automation type
        automation_type = row.get('Automation_Type', '').strip().lower()
        
        # Get reference functions from all CSPs
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
            print("  📋 MANUAL requirement - no automated checks")
            stats['manual'] += 1
            
            # Validate data consistency
            if aws_funcs:
                print(f"  ⚠️  DATA INCONSISTENCY: Manual requirement has AWS functions!")
                print(f"      Functions: {', '.join(aws_funcs[:2])}...")
                stats['inconsistencies'].append({
                    'req_id': req_id,
                    'issue': 'Manual requirement with AWS functions',
                    'functions': aws_funcs[:3]
                })
            
            # Ensure empty for GCP/Azure
            row['GCP_Checks'] = ''
            row['Azure_Checks'] = ''
            enhanced_rows.append(row)
            continue
        
        # Skip if no reference functions
        if not aws_funcs and not ibm_funcs and not alicloud_funcs and not oracle_funcs:
            print("  ⚠️  No reference functions found - skipping")
            stats['skipped'] += 1
            row['GCP_Checks'] = ''
            row['Azure_Checks'] = ''
            enhanced_rows.append(row)
            continue
        
        stats['automated'] += 1
        
        # Use AWS as primary, fallback to others
        reference_functions = aws_funcs or ibm_funcs or alicloud_funcs or oracle_funcs
        
        # Create rich context for AI
        context = f"""
        Compliance Framework: {framework_name}
        Requirement Title: {row.get('Title', '')}
        Requirement Section: {row.get('Section', '')}
        Automation Type: automated
        Reference CSPs: {', '.join([csp for csp, funcs in [('AWS', aws_funcs), ('IBM', ibm_funcs), ('Alicloud', alicloud_funcs), ('Oracle', oracle_funcs)] if funcs])}
        """
        
        try:
            # Generate equivalents using AI
            print(f"  🤖 Generating from {len(reference_functions)} reference function(s)...")
            result = generate_equivalent_functions(reference_functions, context, framework_name)
            
            # Update CSV row
            gcp_funcs = result.get('gcp_functions', [])
            azure_funcs = result.get('azure_functions', [])
            
            row['GCP_Checks'] = '; '.join(gcp_funcs)
            row['Azure_Checks'] = '; '.join(azure_funcs)
            
            # Update total count
            current_total = int(row.get('Total_Checks', 0))
            new_total = current_total + len(gcp_funcs) + len(azure_funcs)
            row['Total_Checks'] = str(new_total)
            
            print(f"  ✅ Generated {len(gcp_funcs)} GCP + {len(azure_funcs)} Azure functions")
            if result.get('notes'):
                print(f"  📝 {result['notes']}")
            
            stats['enhanced'] += 1
            
        except Exception as e:
            error_msg = str(e)
            # Show more details for connection/auth errors
            if 'Connection' in error_msg or 'authentication' in error_msg or 'Incorrect API key' in error_msg:
                print(f"  ❌ ERROR: {error_msg}")
                print(f"      Please verify your OPENAI_API_KEY is correct")
            else:
                print(f"  ❌ ERROR: {error_msg}")
            stats['errors'] += 1
            row['GCP_Checks'] = ''
            row['Azure_Checks'] = ''
        
        enhanced_rows.append(row)
    
    return enhanced_rows, stats

def main():
    if len(sys.argv) < 2:
        print("=" * 80)
        print("AI-POWERED GCP & AZURE FUNCTION GENERATOR - SINGLE FRAMEWORK")
        print("=" * 80)
        print("\nUsage:")
        print("  python3 ai_generator_single.py <framework>")
        print("\nFrameworks:")
        print("  nist    - NIST 800-171 (50 requirements)")
        print("  gdpr    - GDPR (3 requirements)")
        print("  hipaa   - HIPAA (32 requirements)")
        print("\nExample:")
        print("  python3 ai_generator_single.py nist")
        print("\n" + "=" * 80)
        return
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("\n❌ ERROR: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        return
    
    framework_arg = sys.argv[1].lower()
    
    frameworks = {
        'nist': {
            'name': 'NIST 800-171',
            'csv': 'nist_800_171/NIST_800-171_R2_controls_with_checks.csv',
            'output_csv': 'nist_800_171/NIST_800-171_R2_controls_with_checks_ENHANCED.csv',
        },
        'gdpr': {
            'name': 'GDPR',
            'csv': 'gdpr/GDPR_controls_with_checks.csv',
            'output_csv': 'gdpr/GDPR_controls_with_checks_ENHANCED.csv',
        },
        'hipaa': {
            'name': 'HIPAA',
            'csv': 'hipaa/HIPAA_controls_with_checks.csv',
            'output_csv': 'hipaa/HIPAA_controls_with_checks_ENHANCED.csv',
        }
    }
    
    if framework_arg not in frameworks:
        print(f"\n❌ ERROR: Unknown framework '{framework_arg}'")
        print(f"Valid options: {', '.join(frameworks.keys())}")
        return
    
    framework = frameworks[framework_arg]
    
    print("=" * 80)
    print(f"AI-POWERED GENERATION: {framework['name']}")
    print("=" * 80)
    print(f"Input:  {framework['csv']}")
    print(f"Output: {framework['output_csv']}")
    print("=" * 80)
    
    # Process framework
    enhanced_rows, stats = process_framework(
        framework['csv'],
        framework['name']
    )
    
    # Save enhanced CSV
    with open(framework['output_csv'], 'w', encoding='utf-8', newline='') as f:
        if enhanced_rows:
            writer = csv.DictWriter(f, fieldnames=enhanced_rows[0].keys())
            writer.writeheader()
            writer.writerows(enhanced_rows)
    
    # Print summary
    print("\n" + "=" * 80)
    print(f"📊 {framework['name'].upper()} - ENHANCEMENT SUMMARY")
    print("=" * 80)
    print(f"Total Requirements:       {stats['total']}")
    print(f"  ├─ Manual:              {stats['manual']} (no functions generated)")
    print(f"  ├─ Automated:           {stats['automated']}")
    print(f"  │  ├─ Enhanced:         {stats['enhanced']} ✅")
    print(f"  │  ├─ Skipped:          {stats['skipped']}")
    print(f"  │  └─ Errors:           {stats['errors']}")
    
    if stats['inconsistencies']:
        print(f"\n⚠️  Data Inconsistencies Found: {len(stats['inconsistencies'])}")
        for item in stats['inconsistencies'][:5]:  # Show first 5
            print(f"  - {item['req_id']}: {item['issue']}")
        if len(stats['inconsistencies']) > 5:
            print(f"  ... and {len(stats['inconsistencies']) - 5} more")
    else:
        print(f"\n✅ Data Consistency: OK")
    
    # Calculate coverage
    if stats['automated'] > 0:
        coverage = round((stats['enhanced'] / stats['automated']) * 100, 1)
        print(f"\n📈 Coverage: {coverage}% of automated requirements enhanced")
    
    print(f"\n✅ Output saved: {framework['output_csv']}")
    print("=" * 80)

if __name__ == '__main__':
    main()

