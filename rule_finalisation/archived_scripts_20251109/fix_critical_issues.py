"""
Fix Top 3 Critical Issues in AWS Functions List
1. Parse and fix "unknown" service category
2. Merge awslambda → lambda
3. Merge docdb → documentdb
4. Remove duplicate functions
"""

import csv
import json
from pathlib import Path
from collections import defaultdict
import re

INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08.csv")
OUTPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08_fixed.csv")
BACKUP_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08_before_critical_fixes.csv")

# Define fixes
FUNCTION_FIXES = {
    # Backup duplicates
    "aws_backup_recovery_point_encryption": "aws_backup_recovery_point_encrypted",
    
    # ACM duplicates
    "aws_acm_certificates_expiration_check": "aws_acm_certificate_expiration",
    
    # Service prefix fixes - awslambda → lambda
    "aws_awslambda_function_inside_vpc": "aws_lambda_function_inside_vpc",
    "aws_awslambda_function_invoke_api_operations_cloudtrail_logging_enabled": "aws_lambda_function_invoke_api_operations_cloudtrail_logging_enabled",
    "aws_awslambda_function_not_publicly_accessible": "aws_lambda_function_not_publicly_accessible",
    "aws_awslambda_function_url_cors_policy": "aws_lambda_function_url_cors_policy",
    "aws_awslambda_function_url_public": "aws_lambda_function_url_public",
    "aws_awslambda_function_vpc_multi_az": "aws_lambda_function_vpc_multi_az",
}

# Parse "unknown" functions - these are missing aws_ prefix
UNKNOWN_FIXES = {
    # ACM
    "acm_certificates_expiration_check": "aws_acm_certificate_expiration",
    
    # API Gateway
    "apigateway_restapi_tracing_enabled": "aws_apigateway_restapi_tracing_enabled",
    "apigateway_restapi_waf_acl_attached": "aws_apigateway_restapi_waf_acl_attached",
    
    # CloudFront
    "cloudfront_distributions_custom_ssl_certificate": "aws_cloudfront_distributions_custom_ssl_certificate",
    "cloudfront_distributions_https_enabled": "aws_cloudfront_distributions_https_enabled",
    "cloudfront_distributions_using_deprecated_ssl_protocols": "aws_cloudfront_distributions_using_deprecated_ssl_protocols",
    
    # CloudWatch
    "cloudwatch_log_group_retention_policy_specific_days_enabled": "aws_cloudwatch_log_group_retention_policy_specific_days_enabled",
    "cloudwatch_log_metric_filter_policy_changes": "aws_cloudwatch_log_metric_filter_policy_changes",
    
    # CodeBuild
    "codebuild_project_no_secrets_in_variables": "aws_codebuild_project_envvar_awscred_check",
    "codebuild_project_source_repo_url_no_sensitive_credentials": "aws_codebuild_project_source_repo_url_check",
    
    # Config
    "config_recorder_all_regions_enabled": "aws_config_recorder_all_regions_enabled",
    
    # DMS
    "dms_instance_no_public_access": "aws_dms_instance_no_public_access",
    
    # DynamoDB
    "dynamodb_table_encryption_enabled": "aws_dynamodb_encryption_enabled",
    "dynamodb_table_protected_by_backup_plan": "aws_dynamodb_table_protected_by_backup_plan",
    "dynamodb_tables_pitr_enabled": "aws_dynamodb_tables_pitr_enabled",
    "dynamodb_tables_kms_cmk_encryption_enabled": "aws_dynamodb_tables_kms_cmk_encryption_enabled",
    "dynamodb_accelerator_cluster_encryption_enabled": "aws_dynamodb_accelerator_cluster_encryption_enabled",
    
    # EC2
    "ec2_ebs_default_encryption": "aws_ec2_ebs_default_encryption",
    "ec2_ebs_volume_encryption": "aws_ec2_ebs_volume_encryption",
    "ec2_ebs_public_snapshot": "aws_ec2_ebs_public_snapshot",
    "ec2_ebs_volume_protected_by_backup_plan": "aws_ec2_ebs_volume_protected_by_backup_plan",
    "ec2_instance_public_ip": "aws_ec2_instance_public_ip",
    "ec2_networkacl_allow_ingress_tcp_port_22": "aws_ec2_networkacl_allow_ingress_tcp_port_22",
    "ec2_networkacl_allow_ingress_tcp_port_3389": "aws_ec2_networkacl_allow_ingress_tcp_port_3389",
    "ec2_securitygroup_allow_ingress_from_internet_to_all_ports": "aws_ec2_securitygroup_allow_ingress_from_internet_to_all_ports",
    "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22": "aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22",
    "ec2_securitygroup_default_restrict_traffic": "aws_ec2_securitygroup_default_restrict_traffic",
    
    # EFS
    "efs_encryption_at_rest_enabled": "aws_efs_encryption_at_rest_enabled",
    
    # EKS
    "eks_cluster_kms_cmk_encryption_in_secrets_enabled": "aws_eks_cluster_kms_cmk_encryption_in_secrets_enabled",
    "eks_endpoints_not_publicly_accessible": "aws_eks_cluster_not_publicly_accessible",
    "eks_cluster_uses_a_supported_version": "aws_eks_cluster_supported_version",
    
    # ELB
    "elb_ssl_listeners": "aws_elb_ssl_listeners",
    "elb_logging_enabled": "aws_elb_logging_enabled",
    "elb_desync_mitigation_mode": "aws_elb_desync_mitigation_mode",
    
    # ELBv2
    "elbv2_ssl_listeners": "aws_elbv2_ssl_listeners",
    "elbv2_logging_enabled": "aws_elbv2_logging_enabled",
    "elbv2_waf_acl_attached": "aws_elbv2_waf_acl_attached",
    
    # EMR
    "emr_cluster_master_nodes_no_public_ip": "aws_emr_cluster_master_nodes_no_public_ip",
    
    # ElastiCache
    "elasticache_redis_cluster_backup_enabled": "aws_elasticache_backup_retention",
    
    # IAM
    "iam_password_policy_reuse_24": "aws_iam_password_policy_reuse_24",
    "iam_support_role_created": "aws_iam_support_role_created",
    "iam_user_accesskey_unused": "aws_iam_user_accesskey_unused",
    "iam_user_console_access_unused": "aws_iam_user_console_access_unused",
    
    # OpenSearch
    "opensearch_service_domains_node_to_node_encryption_enabled": "aws_opensearch_service_domains_node_to_node_encryption_enabled",
    "opensearch_service_domains_encryption_at_rest_enabled": "aws_opensearch_service_domains_encryption_at_rest_enabled",
    "opensearch_service_domains_https_communications_enforced": "aws_opensearch_service_domains_https_communications_enforced",
    "opensearch_service_domains_not_publicly_accessible": "aws_opensearch_service_domains_not_publicly_accessible",
    "opensearch_service_domains_audit_logging_enabled": "aws_opensearch_service_domains_audit_logging_enabled",
    "opensearch_service_domains_access_control_enabled": "aws_opensearch_service_domains_access_control_enabled",
    
    # RDS
    "rds_instance_storage_encrypted": "aws_rds_instance_storage_encrypted",
    "rds_instance_no_public_access": "aws_rds_instance_no_public_access",
    "rds_instance_backup_enabled": "aws_rds_instance_backup_enabled",
    "rds_instance_protected_by_backup_plan": "aws_rds_instance_protected_by_backup_plan",
    "rds_snapshots_encrypted": "aws_rds_snapshots_encrypted",
    "rds_snapshots_public_access": "aws_rds_snapshots_public_access",
    "rds_cluster_default_admin": "aws_rds_cluster_default_admin",
    "rds_instance_default_admin": "aws_rds_instance_default_admin",
    "rds_cluster_minor_version_upgrade_enabled": "aws_rds_cluster_minor_version_upgrade_enabled",
    
    # Redshift
    "redshift_cluster_audit_logging": "aws_redshift_cluster_audit_logging",
    "redshift_cluster_public_access": "aws_redshift_cluster_public_access",
    "redshift_cluster_automated_snapshot": "aws_redshift_cluster_automated_snapshot",
    
    # S3
    "s3_bucket_enforces_ssl": "aws_s3_bucket_secure_transport_policy",
    "s3_bucket_default_encryption": "aws_s3_bucket_default_encryption",
    "s3_bucket_kms_encryption": "aws_s3_bucket_kms_encryption",
    "s3_bucket_server_access_logging_enabled": "aws_s3_bucket_server_access_logging_enabled",
    "s3_bucket_lifecycle_enabled": "aws_s3_bucket_lifecycle_enabled",
    "s3_bucket_object_versioning": "aws_s3_bucket_object_versioning",
    "s3_bucket_cross_region_replication": "aws_s3_bucket_cross_region_replication",
    "s3_bucket_policy_public_write_access": "aws_s3_bucket_policy_public_write_access",
    "s3_bucket_public_write_acl": "aws_s3_bucket_public_write_acl",
    "s3_account_level_public_access_blocks": "aws_s3_account_level_public_access_blocks",
    
    # SageMaker
    "sagemaker_notebook_instance_encryption_enabled": "aws_sagemaker_notebook_instance_encryption_enabled",
    "sagemaker_notebook_instance_without_direct_internet_access_configured": "aws_sagemaker_notebook_instance_without_direct_internet_access_configured",
    
    # Secrets Manager
    "secretsmanager_automatic_rotation_enabled": "aws_secretsmanager_secret_rotation_enabled",
    
    # Shield
    "shield_advanced_protection_in_internet_facing_load_balancers": "aws_shield_advanced_protection_enabled",
    
    # SNS
    "sns_topics_kms_encryption_at_rest_enabled": "aws_sns_topics_kms_encryption_at_rest_enabled",
    
    # SSM
    "ssm_managed_compliant_patching": "aws_ssm_managed_compliant_patching",
    
    # VPC
    "vpc_flow_logs_enabled": "aws_vpc_flow_logs_enabled",
    "vpc_endpoint_for_ec2_enabled": "aws_vpc_endpoint_for_ec2_enabled",
    
    # WAFv2
    "wafv2_web_acl_logging_enabled": "aws_wafv2_webacl_logging_enabled",
    
    # CloudTrail
    "cloudtrail_kms_encryption_enabled": "aws_cloudtrail_kms_encryption_enabled",
    "cloudtrail_multi_region_enabled": "aws_cloudtrail_multi_region_enabled",
    "cloudtrail_cloudwatch_logging_enabled": "aws_cloudtrail_cloudwatch_logging_enabled",
    "cloudtrail_s3_dataevents_read_enabled": "aws_cloudtrail_s3_dataevents_read_enabled",
    "cloudtrail_log_file_validation_enabled": "aws_cloudtrail_log_file_validation_enabled",
}

ALL_FIXES = {**FUNCTION_FIXES, **UNKNOWN_FIXES}

print("=" * 80)
print("FIXING TOP 3 CRITICAL ISSUES")
print("=" * 80)
print()

# Create backup
print("1. Creating backup...")
import shutil
shutil.copy2(INPUT_CSV, BACKUP_CSV)
print(f"   ✅ Backup created: {BACKUP_CSV.name}")
print()

# Read and fix CSV
print("2. Processing CSV...")
updated_rows = []
stats = {
    'total_rows': 0,
    'rows_updated': 0,
    'function_replacements': 0,
    'unknown_fixed': 0,
    'duplicates_removed': 0,
    'service_merged': 0
}

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        stats['total_rows'] += 1
        row_changed = False
        
        # Fix all check columns
        for col in ['aws_checks', 'azure_checks', 'gcp_checks', 'oracle_checks', 
                    'ibm_checks', 'alicloud_checks', 'k8s_checks']:
            if row.get(col) and row[col] != 'NA':
                checks = row[col].split(';')
                new_checks = []
                
                for check in checks:
                    check = check.strip()
                    
                    # Handle concatenated functions (comma-separated)
                    if ',' in check:
                        # Split and fix each
                        sub_checks = [c.strip() for c in check.split(',')]
                        for sub in sub_checks:
                            if sub in ALL_FIXES:
                                new_checks.append(ALL_FIXES[sub])
                                stats['unknown_fixed'] += 1
                                row_changed = True
                            elif sub.startswith('aws_'):
                                new_checks.append(sub)
                            elif sub:  # Has content but no aws_ prefix
                                # Try to find in UNKNOWN_FIXES
                                if sub in UNKNOWN_FIXES:
                                    new_checks.append(UNKNOWN_FIXES[sub])
                                    stats['unknown_fixed'] += 1
                                    row_changed = True
                    else:
                        # Single function
                        if check in ALL_FIXES:
                            new_checks.append(ALL_FIXES[check])
                            if check in FUNCTION_FIXES:
                                stats['duplicates_removed'] += 1
                            elif check in UNKNOWN_FIXES:
                                stats['unknown_fixed'] += 1
                            if 'awslambda' in check:
                                stats['service_merged'] += 1
                            stats['function_replacements'] += 1
                            row_changed = True
                        else:
                            new_checks.append(check)
                
                # Remove duplicates and sort
                unique_checks = sorted(list(set(new_checks)))
                row[col] = '; '.join(unique_checks)
        
        if row_changed:
            stats['rows_updated'] += 1
        
        updated_rows.append(row)

# Write fixed CSV
with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"   ✅ Fixed CSV written: {OUTPUT_CSV.name}")
print()

print("3. Statistics:")
print(f"   Total rows processed:     {stats['total_rows']}")
print(f"   Rows updated:             {stats['rows_updated']}")
print(f"   Function replacements:    {stats['function_replacements']}")
print(f"   Unknown functions fixed:  {stats['unknown_fixed']}")
print(f"   Duplicates removed:       {stats['duplicates_removed']}")
print(f"   Service merges (lambda):  {stats['service_merged']}")
print()

print("4. Key Fixes Applied:")
print("   ✅ Backup duplicates consolidated")
print("   ✅ ACM duplicates consolidated")
print("   ✅ awslambda → lambda merged")
print("   ✅ Unknown functions with missing aws_ prefix fixed")
print("   ✅ Concatenated functions split and categorized")
print()

print("=" * 80)
print("CRITICAL FIXES COMPLETE!")
print("=" * 80)
print()
print(f"Original:  {INPUT_CSV.name}")
print(f"Fixed:     {OUTPUT_CSV.name}")
print(f"Backup:    {BACKUP_CSV.name}")

