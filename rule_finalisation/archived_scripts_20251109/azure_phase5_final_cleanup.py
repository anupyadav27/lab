#!/usr/bin/env python3
"""
Azure Phase 5: Final Cleanup
Apply remaining 16 consolidations identified in analysis
"""
import csv
import json
from collections import defaultdict

INPUT_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
OUTPUT_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

print("=" * 80)
print("AZURE PHASE 5: FINAL CLEANUP (16 remaining consolidations)")
print("=" * 80)
print()

# Final consolidation mapping for remaining 16 functions
final_mapping = {
    # SSM → Automation (Azure doesn't have SSM)
    "azure_compute_instance_managed_by_ssm": "azure_compute_vm_managed_by_automation",
    "azure_vm_instance_managed_by_ssm": "azure_compute_vm_managed_by_automation",
    
    # Active Directory → AD (remaining 3 functions)
    "azure_active_directory_root_hardware_mfa_enabled": "azure_ad_root_hardware_mfa_enabled",
    "azure_active_directory_rotate_access_key_90_days": "azure_ad_rotate_access_key_90_days",
    "azure_active_directory_password_policy_reuse_24": "azure_ad_password_policy_reuse_24",
    
    # CloudWatch → Monitor
    "azure_search_service_domains_cloudwatch_logging_enabled": "azure_search_service_domains_logging_enabled",
    "azure_log_cloudwatch_logs_enabled": "azure_monitor_logging_enabled",
    
    # Storage bucket → account (remaining)
    "azure_storage_bucket_public_read_prohibited": "azure_storage_account_public_read_prohibited",
    "azure_storage_bucket_public_write_prohibited": "azure_storage_account_public_write_prohibited",
    "azure_storage_bucket_versioning_enabled": "azure_storage_account_versioning_enabled",
    "azure_storage_account_s3_bucket_encryption_enabled": "azure_storage_account_encryption_enabled",
    "azure_storage_bucket_replication_enabled": "azure_storage_account_replication_enabled",
    "azure_storage_bucket_default_kms_encryption": "azure_storage_account_default_encryption",
    
    # EBS → Disk
    "azure_vm_ebs_volume_encrypted": "azure_vm_disk_encrypted",
    
    # SQL instance → database (remaining)
    "azure_sql_rds_instance_encryption_enabled": "azure_sql_database_encryption_at_rest_enabled",
    "azure_sql_instance_backup_encrypted": "azure_sql_database_backup_encrypted",
    "azure_sql_instance_iam_authentication_enabled": "azure_sql_database_ad_authentication_enabled",
}

print(f"Loaded {len(final_mapping)} final consolidation mappings")
print()

# Track statistics
replacements_made = defaultdict(int)
rows_updated = 0

# Read and process CSV
print("Step 1: Processing CSV...")
rows = []
with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        row_modified = False
        azure_checks = row.get('azure_checks', '')
        
        if azure_checks and azure_checks != 'NA':
            # Split functions
            funcs = [f.strip() for f in azure_checks.split(';') if f.strip()]
            new_funcs = []
            
            for func in funcs:
                if func in final_mapping:
                    new_func = final_mapping[func]
                    new_funcs.append(new_func)
                    replacements_made[f"{func} → {new_func}"] += 1
                    row_modified = True
                else:
                    new_funcs.append(func)
            
            # Remove duplicates and sort
            new_funcs = sorted(list(set(new_funcs)))
            row['azure_checks'] = '; '.join(new_funcs)
            
            # Recalculate total_checks
            all_checks = []
            for field in ['aws_checks', 'azure_checks', 'gcp_checks', 'oracle_checks', 
                         'ibm_checks', 'alicloud_checks', 'k8s_checks']:
                checks = row.get(field, '')
                if checks and checks != 'NA':
                    all_checks.extend([c.strip() for c in checks.split(';') if c.strip()])
            row['total_checks'] = str(len(set(all_checks)))
            
            if row_modified:
                rows_updated += 1
        
        rows.append(row)

print(f"✓ Processed {len(rows)} rows")
print(f"✓ Updated {rows_updated} rows with Azure consolidations")
print()

# Write updated CSV
print("Step 2: Writing updated CSV...")
with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Updated CSV saved: {OUTPUT_CSV}")
print()

# Generate report
print("=" * 80)
print("PHASE 5 CONSOLIDATION REPORT")
print("=" * 80)
print()

print(f"Total consolidation mappings:  {len(final_mapping)}")
print(f"Rows updated:                  {rows_updated}")
print(f"Total replacements made:       {sum(replacements_made.values())}")
print()

if replacements_made:
    print("All replacements:")
    for replacement, count in sorted(replacements_made.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {count:3d}x  {replacement}")
else:
    print("⚠️  No replacements made - functions may have been already consolidated")

print()

# Save detailed report
report = {
    'metadata': {
        'phase': 5,
        'date': '2025-11-09',
        'status': 'complete'
    },
    'statistics': {
        'consolidation_mappings': len(final_mapping),
        'rows_updated': rows_updated,
        'total_replacements': sum(replacements_made.values())
    },
    'replacements': dict(replacements_made),
    'mapping_applied': final_mapping
}

report_file = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/azure_phase5_final_cleanup_report.json"
with open(report_file, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print(f"✓ Detailed report saved: {report_file}")
print()
print("=" * 80)
print("✅ AZURE PHASE 5 COMPLETE! All Azure consolidations applied.")
print("=" * 80)

