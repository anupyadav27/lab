"""
Final cleanup of remaining functional duplicates in AWS functions
Based on user's identified duplicates and expert analysis
"""

import csv
import json
from pathlib import Path
from collections import defaultdict

INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv")
OUTPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv")
OUTPUT_JSON = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functions_final_deduplicated.json")

print("=" * 80)
print("FINAL CLEANUP - REMAINING FUNCTIONAL DUPLICATES")
print("=" * 80)
print()

# Define remaining duplicates based on AWS expert analysis
FINAL_CONSOLIDATIONS = {
    # EFS - encryption duplicates (all check same thing)
    "aws_efs_file_system_encryption_at_rest_check": "aws_efs_encryption_at_rest_enabled",
    "aws_efs_file_system_encryption_at_rest_enabled": "aws_efs_encryption_at_rest_enabled",
    
    # EFS - backup duplicates (same check)
    "aws_efs_have_backup_enabled": "aws_efs_backup_enabled",
    
    # EKS - kubelet certificate rotation (duplicate)
    "aws_eks_kubelet_rotate_certificates_check": "aws_eks_kubelet_rotate_certificate_check",
    
    # EC2 - EBS volume encryption variations
    "aws_ec2_ebs_volume_encryption_enabled": "aws_ec2_ebs_volume_encrypted",
    
    # EC2 - instance public IP (naming consistency)
    "aws_ec2_instance_public_ip": "aws_ec2_instance_no_public_ip",
    
    # Lambda - public access variations
    "aws_lambda_function_not_publicly_accessible": "aws_lambda_function_restrict_public_access",
    "aws_lambda_function_public_access_check": "aws_lambda_function_restrict_public_access",
    
    # DynamoDB - PITR duplicate
    "aws_dynamodb_tables_pitr_enabled": "aws_dynamodb_pitr_enabled",
    
    # GuardDuty - enabled check duplicate
    "aws_guardduty_is_enabled": "aws_guardduty_enabled",
    
    # ELB - internet facing check
    "aws_elb_internet_facing": "aws_elb_logging_enabled",  # Actually different - SKIP
    
    # DocumentDB vs DocDB - merge services
    "aws_documentdb_cluster_audit_logging_to_cloudwatch_enabled": "aws_docdb_cluster_monitoring_and_alerting_configured",
    "aws_documentdb_cluster_cloudwatch_log_export": "aws_docdb_cluster_monitoring_and_alerting_configured",
    "aws_documentdb_cluster_encryption_at_rest_enabled": "aws_docdb_cluster_encryption_in_transit_enabled",
    "aws_documentdb_cluster_multi_az_enabled": "aws_docdb_cluster_backup_retention_period_configured",
    "aws_documentdb_cluster_preferred_backup_window_configured": "aws_docdb_cluster_backup_retention_period_configured",
    "aws_documentdb_cluster_storage_encrypted": "aws_docdb_cluster_encryption_in_transit_enabled",
}

# Actually, let's be more careful - only consolidate TRUE functional duplicates
# Remove the ones that are actually different checks
TRUE_CONSOLIDATIONS = {
    # EFS - encryption duplicates (all check EFS encryption at rest)
    "aws_efs_file_system_encryption_at_rest_check": "aws_efs_encryption_at_rest_enabled",
    "aws_efs_file_system_encryption_at_rest_enabled": "aws_efs_encryption_at_rest_enabled",
    
    # EFS - backup duplicates (both check backup enabled)
    "aws_efs_have_backup_enabled": "aws_efs_backup_enabled",
    
    # EKS - kubelet certificate rotation (plural vs singular)
    "aws_eks_kubelet_rotate_certificates_check": "aws_eks_kubelet_rotate_certificate_check",
    
    # EC2 - EBS volume encryption (same check, different naming)
    "aws_ec2_ebs_volume_encryption_enabled": "aws_ec2_ebs_volume_encrypted",
    
    # Lambda - public access (all check same resource policy)
    "aws_lambda_function_not_publicly_accessible": "aws_lambda_function_restrict_public_access",
    "aws_lambda_function_public_access_check": "aws_lambda_function_restrict_public_access",
    
    # DynamoDB - PITR (both check point-in-time recovery)
    "aws_dynamodb_tables_pitr_enabled": "aws_dynamodb_pitr_enabled",
    
    # GuardDuty - enabled check (same check)
    "aws_guardduty_is_enabled": "aws_guardduty_enabled",
}

print("Consolidations to apply:")
for old, new in TRUE_CONSOLIDATIONS.items():
    print(f"  {old}")
    print(f"  → {new}")
    print()

# Process CSV
updated_rows = []
stats = {
    'total_rows': 0,
    'rows_updated': 0,
    'functions_consolidated': 0
}

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        stats['total_rows'] += 1
        row_changed = False
        
        for col in ['aws_checks', 'azure_checks', 'gcp_checks', 'oracle_checks',
                    'ibm_checks', 'alicloud_checks', 'k8s_checks']:
            if row.get(col) and row[col] != 'NA':
                checks = row[col].split(';')
                new_checks = []
                
                for check in checks:
                    check = check.strip()
                    if check in TRUE_CONSOLIDATIONS:
                        new_checks.append(TRUE_CONSOLIDATIONS[check])
                        stats['functions_consolidated'] += 1
                        row_changed = True
                    else:
                        new_checks.append(check)
                
                # Remove duplicates and sort
                unique_checks = sorted(list(set(new_checks)))
                row[col] = '; '.join(unique_checks)
        
        if row_changed:
            stats['rows_updated'] += 1
        
        updated_rows.append(row)

# Write CSV
with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"✅ CSV updated: {OUTPUT_CSV.name}")
print(f"   Rows processed: {stats['total_rows']}")
print(f"   Rows updated: {stats['rows_updated']}")
print(f"   Functions consolidated: {stats['functions_consolidated']}")
print()

# Regenerate final functions JSON
aws_functions_by_service = defaultdict(set)

with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        aws_checks = row.get('aws_checks', '')
        if aws_checks and aws_checks != 'NA':
            functions = [f.strip() for f in aws_checks.split(';') if f.strip()]
            for func in functions:
                if func.startswith('aws_'):
                    parts = func[4:].split('_')
                    if parts:
                        service = parts[0]
                        aws_functions_by_service[service].add(func)

# Convert to sorted dict
final_functions = {
    service: sorted(list(funcs))
    for service, funcs in sorted(aws_functions_by_service.items())
}

with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(final_functions, f, indent=2)

print(f"✅ JSON updated: {OUTPUT_JSON.name}")
print(f"   Services: {len(final_functions)}")
print(f"   Total functions: {sum(len(funcs) for funcs in final_functions.values())}")
print()

print("=" * 80)
print("FINAL CLEANUP COMPLETE!")
print("=" * 80)
print()
print(f"Before: 528 functions")
print(f"After:  {sum(len(funcs) for funcs in final_functions.values())} functions")
print(f"Removed: {len(TRUE_CONSOLIDATIONS)} duplicates")

