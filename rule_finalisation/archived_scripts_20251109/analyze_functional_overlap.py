"""
Deep Functional Analysis of AWS Functions
Analyze which functions perform the same JOB (not just similar names)
Focus on identifying truly redundant checks vs. complementary checks
"""

import csv
import json
from pathlib import Path
from collections import defaultdict

INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08_fixed.csv")
OUTPUT_JSON = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functional_overlap_analysis.json")

print("=" * 80)
print("AWS FUNCTIONS - DEEP FUNCTIONAL OVERLAP ANALYSIS")
print("=" * 80)
print()

# Collect all AWS functions with their compliance mappings
function_compliance = defaultdict(set)
function_count = defaultdict(int)

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        unique_id = row.get('unique_compliance_id', '')
        aws_checks = row.get('aws_checks', '')
        
        if aws_checks and aws_checks != 'NA':
            functions = [f.strip() for f in aws_checks.split(';') if f.strip()]
            for func in functions:
                function_compliance[func].add(unique_id)
                function_count[func] += 1

print(f"Total unique AWS functions: {len(function_compliance)}")
print()

# Define functional groups - functions that do the SAME job
functional_groups = {
    "cloudtrail_enabled": {
        "description": "Ensure CloudTrail is enabled and properly configured",
        "functions": [
            "aws_cloudtrail_enabled",
            "aws_cloudtrail_multi_region_enabled",
            "aws_cloudtrail_trail_multi_region_logging_enabled",
            "aws_cloudtrail_multi_region_enabled_logging_management_events",
            "aws_cloudtrail_trail_multi_region_management_logging_enabled"
        ],
        "recommendation": "Keep: aws_cloudtrail_multi_region_enabled (most comprehensive)",
        "rationale": "Multi-region CloudTrail enables single-region by default. Checking multi-region is sufficient."
    },
    
    "cloudtrail_cloudwatch_integration": {
        "description": "CloudTrail logs integrated with CloudWatch",
        "functions": [
            "aws_cloudtrail_cloudwatch_logging_enabled",
            "aws_cloudtrail_cloudwatch_logs_enabled"
        ],
        "recommendation": "Keep: aws_cloudtrail_cloudwatch_logging_enabled",
        "rationale": "Same check, different naming"
    },
    
    "cloudtrail_config_changes": {
        "description": "Monitor AWS Config configuration changes",
        "functions": [
            "aws_cloudtrail_config_change_monitoring",
            "aws_cloudtrail_config_changes_monitoring"
        ],
        "recommendation": "Keep: aws_cloudtrail_config_changes_monitoring",
        "rationale": "Identical function, singular vs plural naming"
    },
    
    "cloudtrail_vpc_changes": {
        "description": "Monitor VPC configuration changes",
        "functions": [
            "aws_cloudtrail_vpc_change_monitoring_configured",
            "aws_cloudtrail_vpc_changes_monitoring_enabled"
        ],
        "recommendation": "Keep: aws_cloudtrail_vpc_changes_monitoring_enabled",
        "rationale": "Same monitoring, different naming convention"
    },
    
    "cloudtrail_s3_data_events": {
        "description": "S3 object-level logging via CloudTrail",
        "functions": [
            "aws_cloudtrail_s3_data_events_logging_enabled",
            "aws_cloudtrail_s3_object_level_logging_enabled",
            "aws_cloudtrail_s3_dataevents_read_enabled",
            "aws_cloudtrail_s3_dataevents_write_enabled"
        ],
        "recommendation": "Keep: aws_cloudtrail_s3_dataevents_read_enabled, aws_cloudtrail_s3_dataevents_write_enabled (both needed for granularity)",
        "rationale": "Read and write are distinct permissions. The generic 'data_events' checks are redundant if you have both read/write."
    },
    
    "cloudtrail_kms_encryption": {
        "description": "CloudTrail log encryption with KMS",
        "functions": [
            "aws_cloudtrail_kms_encryption_enabled",
            "aws_cloudtrail_trail_encryption_at_rest_kms_enabled",
            "aws_cloudtrail_trail_sse_kms_encryption_at_rest_enabled"
        ],
        "recommendation": "Keep: aws_cloudtrail_kms_encryption_enabled",
        "rationale": "All check the same thing - KMS encryption for CloudTrail"
    },
    
    "cloudtrail_log_validation": {
        "description": "CloudTrail log file integrity validation",
        "functions": [
            "aws_cloudtrail_log_file_validation_enabled",
            "aws_cloudtrail_trail_log_file_validation_check",
            "aws_cloudtrail_trail_log_file_validation_status_check"
        ],
        "recommendation": "Keep: aws_cloudtrail_log_file_validation_enabled",
        "rationale": "All verify log file validation is enabled"
    },
    
    "s3_bucket_encryption": {
        "description": "S3 bucket encryption at rest",
        "functions": [
            "aws_s3_bucket_default_encryption",
            "aws_s3_bucket_encryption_enabled",
            "aws_s3_bucket_kms_encryption",
            "aws_s3_bucket_default_kms_encryption"
        ],
        "recommendation": "Keep: aws_s3_bucket_encryption_enabled (any encryption), aws_s3_bucket_kms_encryption (specifically KMS)",
        "rationale": "Two levels: (1) Is encryption enabled at all? (2) Is it KMS specifically?"
    },
    
    "s3_bucket_logging": {
        "description": "S3 bucket access logging",
        "functions": [
            "aws_s3_bucket_logging_enabled",
            "aws_s3_bucket_server_access_logging_enabled"
        ],
        "recommendation": "Keep: aws_s3_bucket_server_access_logging_enabled (more specific)",
        "rationale": "Same check, more explicit naming preferred"
    },
    
    "s3_bucket_versioning": {
        "description": "S3 bucket versioning enabled",
        "functions": [
            "aws_s3_bucket_versioning_enabled",
            "aws_s3_bucket_object_versioning"
        ],
        "recommendation": "Keep: aws_s3_bucket_versioning_enabled",
        "rationale": "Same check, versioning is at bucket level not object level (misleading name)"
    },
    
    "s3_bucket_replication": {
        "description": "S3 bucket cross-region replication",
        "functions": [
            "aws_s3_bucket_cross_region_replication",
            "aws_s3_bucket_replication_enabled"
        ],
        "recommendation": "Keep: aws_s3_bucket_replication_enabled (covers both CRR and SRR)",
        "rationale": "Replication can be cross-region or same-region; generic check is better"
    },
    
    "s3_public_access": {
        "description": "S3 bucket public access controls",
        "functions": [
            "aws_s3_bucket_public_access",
            "aws_s3_bucket_public_read_prohibited",
            "aws_s3_bucket_public_write_prohibited",
            "aws_s3_bucket_policy_public_write_access",
            "aws_s3_account_level_public_access_blocks",
            "aws_s3_public_access_block_check"
        ],
        "recommendation": "Keep: aws_s3_account_level_public_access_blocks (account-level), aws_s3_bucket_public_read_prohibited, aws_s3_bucket_public_write_prohibited (bucket-level granular)",
        "rationale": "Account-level blocks are different from bucket-level. Need both read and write checks."
    },
    
    "s3_secure_transport": {
        "description": "S3 bucket requires HTTPS/TLS",
        "functions": [
            "aws_s3_bucket_secure_transport_policy",
            "aws_s3_bucket_policy_in_transit_http_access_denied"
        ],
        "recommendation": "Keep: aws_s3_bucket_secure_transport_policy",
        "rationale": "Same policy check, different naming"
    },
    
    "s3_cloudtrail_bucket_logging": {
        "description": "CloudTrail S3 bucket has access logging",
        "functions": [
            "aws_s3_cloudtrail_bucket_access_logging_enabled",
            "aws_s3_cloudtrail_bucket_logging_enabled"
        ],
        "recommendation": "Keep: aws_s3_cloudtrail_bucket_access_logging_enabled",
        "rationale": "More specific naming for CloudTrail bucket logging"
    },
    
    "iam_root_mfa": {
        "description": "Root account MFA enabled",
        "functions": [
            "aws_iam_root_mfa_enabled",
            "aws_iam_root_mfa_status_check",
            "aws_iam_root_user_mfa_check"
        ],
        "recommendation": "Keep: aws_iam_root_mfa_enabled",
        "rationale": "All check root MFA status"
    },
    
    "iam_root_hardware_mfa": {
        "description": "Root account hardware MFA (not virtual)",
        "functions": [
            "aws_iam_root_hardware_mfa_enabled",
            "aws_iam_root_hardware_mfa_check"
        ],
        "recommendation": "Keep: aws_iam_root_hardware_mfa_enabled",
        "rationale": "Same check, different naming"
    },
    
    "iam_root_access_keys": {
        "description": "Root account access keys should not exist",
        "functions": [
            "aws_iam_no_root_access_key",
            "aws_iam_root_user_access_key_check",
            "aws_iam_root_user_access_keys_existence_check"
        ],
        "recommendation": "Keep: aws_iam_no_root_access_key",
        "rationale": "Most concise naming, same check"
    },
    
    "iam_user_mfa": {
        "description": "IAM users with console access have MFA",
        "functions": [
            "aws_iam_user_mfa_enabled",
            "aws_iam_user_mfa_enabled_console_access",
            "aws_iam_user_mfa_status_check_for_console_access",
            "aws_iam_user_console_password_mfa_check"
        ],
        "recommendation": "Keep: aws_iam_user_mfa_enabled_console_access",
        "rationale": "Specifically checks console access users (most accurate)"
    },
    
    "iam_access_key_rotation": {
        "description": "IAM access keys rotated regularly",
        "functions": [
            "aws_iam_access_key_rotation_90_days_check",
            "aws_iam_access_key_rotation_check",
            "aws_iam_rotate_access_key_90_days"
        ],
        "recommendation": "Keep: aws_iam_access_key_rotation_90_days_check",
        "rationale": "Specific 90-day requirement is CIS benchmark standard"
    },
    
    "iam_unused_credentials": {
        "description": "IAM users with unused credentials",
        "functions": [
            "aws_iam_user_credentials_unused_45_days_disabled",
            "aws_iam_user_credentials_unused_for_45_days_disabled",
            "aws_iam_user_unused_credentials",
            "aws_iam_user_unused_credentials_disabled"
        ],
        "recommendation": "Keep: aws_iam_user_credentials_unused_45_days_disabled",
        "rationale": "45 days is the standard threshold"
    },
    
    "iam_user_in_groups": {
        "description": "IAM users should be in groups, not have direct policies",
        "functions": [
            "aws_iam_user_in_group",
            "aws_iam_user_group_membership",
            "aws_iam_user_permissions_group_only_check",
            "aws_iam_user_permissions_group_only_compliance"
        ],
        "recommendation": "Keep: aws_iam_user_in_group (checks group membership), aws_iam_policy_attached_only_to_group_or_roles (checks no direct policies)",
        "rationale": "Two distinct checks: (1) Is user in a group? (2) Does user have direct policies?"
    },
    
    "iam_password_policy": {
        "description": "IAM password policy compliance",
        "functions": [
            "aws_iam_password_policy_compliance",
            "aws_iam_password_policy_strong",
            "aws_iam_password_policy_minimum_length_14",
            "aws_iam_password_policy_minimum_length_check",
            "aws_iam_password_policy_expires_passwords_within_90_days_or_less",
            "aws_iam_password_policy_password_reuse_prevention_check",
            "aws_iam_password_policy_prevent_password_reuse_min_24",
            "aws_iam_password_policy_reuse_24",
            "aws_iam_user_password_policy_complex"
        ],
        "recommendation": "Keep: aws_iam_password_policy_minimum_length_14, aws_iam_password_policy_expires_passwords_within_90_days_or_less, aws_iam_password_policy_reuse_24, aws_iam_user_password_policy_complex",
        "rationale": "Each checks a specific password policy requirement: length, expiry, reuse, complexity"
    },
    
    "iam_support_role": {
        "description": "AWS Support access role exists",
        "functions": [
            "aws_iam_role_awssupport_access_policy_attachment",
            "aws_iam_role_awssupport_access_policy_check"
        ],
        "recommendation": "Keep: aws_iam_role_awssupport_access_policy_attachment",
        "rationale": "Same check, slightly different naming"
    },
    
    "iam_access_analyzer": {
        "description": "IAM Access Analyzer enabled",
        "functions": [
            "aws_iam_access_analyzer_active_status_all_regions",
            "aws_iam_access_analyzer_external_access_enabled_all_regions"
        ],
        "recommendation": "Keep: Both - different checks",
        "rationale": "First checks if active, second checks if external access analysis is on"
    },
    
    "ec2_ebs_encryption": {
        "description": "EBS volumes encrypted",
        "functions": [
            "aws_ec2_ebs_default_encryption",
            "aws_ec2_ebs_encryption_by_default_enabled",
            "aws_ec2_ebs_volume_encrypted",
            "aws_ec2_ebs_volume_encryption",
            "aws_ec2_ebs_volume_encryption_enabled",
            "aws_ec2_ebs_snapshots_encrypted",
            "aws_ebs_snapshot_encryption"
        ],
        "recommendation": "Keep: aws_ec2_ebs_encryption_by_default_enabled (account default), aws_ec2_ebs_volume_encrypted (per-volume), aws_ec2_ebs_snapshots_encrypted (snapshots)",
        "rationale": "Three distinct checks: default setting, individual volumes, snapshots"
    },
    
    "ec2_ebs_public": {
        "description": "EBS snapshots not public",
        "functions": [
            "aws_ec2_ebs_public_snapshot",
            "aws_ec2_ebs_snapshot_account_block_public_access"
        ],
        "recommendation": "Keep: Both - different levels",
        "rationale": "First checks individual snapshots, second checks account-level block setting"
    },
    
    "ec2_imdsv2": {
        "description": "EC2 Instance Metadata Service v2 required",
        "functions": [
            "aws_ec2_instance_imdsv2_enabled",
            "aws_ec2_instance_metadata_service_imdsv2_required",
            "aws_ec2_instance_account_imdsv2_enabled",
            "aws_ec2_launch_template_imdsv2_required"
        ],
        "recommendation": "Keep: aws_ec2_instance_imdsv2_enabled (running instances), aws_ec2_launch_template_imdsv2_required (launch templates)",
        "rationale": "Need to check both running instances and launch templates separately"
    },
    
    "ec2_public_ip": {
        "description": "EC2 instances should not have public IPs",
        "functions": [
            "aws_ec2_instance_public_ip",
            "aws_ec2_instance_no_public_ip",
            "aws_ec2_launch_template_no_public_ip"
        ],
        "recommendation": "Keep: aws_ec2_instance_no_public_ip (instances), aws_ec2_launch_template_no_public_ip (templates)",
        "rationale": "Check both instances and templates; naming should be consistent (no_public_ip)"
    },
    
    "ec2_default_security_group": {
        "description": "Default security group restricts all traffic",
        "functions": [
            "aws_ec2_default_security_group_restriction_check",
            "aws_ec2_securitygroup_default_restrict_traffic",
            "aws_ec2_securitygroup_default_restricted"
        ],
        "recommendation": "Keep: aws_ec2_securitygroup_default_restrict_traffic",
        "rationale": "All check default SG is locked down"
    },
    
    "ec2_sg_ssh_restricted": {
        "description": "Security groups don't allow SSH from internet",
        "functions": [
            "aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22",
            "aws_ec2_securitygroup_ssh_restricted",
            "aws_ec2_security_group_ingress_ssh_rdp_restricted"
        ],
        "recommendation": "Keep: aws_ec2_securitygroup_ssh_restricted (SSH), aws_ec2_securitygroup_rdp_restricted (RDP separately)",
        "rationale": "SSH and RDP are different protocols, check separately"
    },
    
    "ec2_sg_rdp_restricted": {
        "description": "Security groups don't allow RDP from internet",
        "functions": [
            "aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_3389",
            "aws_ec2_securitygroup_rdp_restricted"
        ],
        "recommendation": "Keep: aws_ec2_securitygroup_rdp_restricted",
        "rationale": "Consolidated port check into named function"
    },
    
    "ec2_sg_unrestricted": {
        "description": "Security groups don't allow unrestricted access",
        "functions": [
            "aws_ec2_securitygroup_allow_ingress_from_internet_to_all_ports",
            "aws_ec2_securitygroup_allow_ingress_from_internet_to_any_port",
            "aws_ec2_securitygroup_allow_wide_open_public_ipv4"
        ],
        "recommendation": "Keep: aws_ec2_securitygroup_allow_ingress_from_internet_to_all_ports",
        "rationale": "All check for 0.0.0.0/0 on all ports"
    },
    
    "rds_encryption": {
        "description": "RDS instance storage encrypted",
        "functions": [
            "aws_rds_instance_encryption_at_rest_enabled",
            "aws_rds_instance_encryption_enabled",
            "aws_rds_instance_storage_encrypted",
            "aws_rds_storage_encrypted",
            "aws_rds_cluster_storage_encrypted"
        ],
        "recommendation": "Keep: aws_rds_instance_storage_encrypted (instances), aws_rds_cluster_storage_encrypted (clusters)",
        "rationale": "Instance and cluster encryption are separate checks"
    },
    
    "rds_backup": {
        "description": "RDS automated backups enabled",
        "functions": [
            "aws_rds_backup_enabled",
            "aws_rds_instance_backup_enabled",
            "aws_rds_aurora_backup_enabled",
            "aws_rds_backup_retention_period"
        ],
        "recommendation": "Keep: aws_rds_instance_backup_enabled (checks enabled), aws_rds_backup_retention_period (checks >= 7 days)",
        "rationale": "Two checks: is backup on, and is retention sufficient"
    },
    
    "rds_multi_az": {
        "description": "RDS Multi-AZ enabled",
        "functions": [
            "aws_rds_instance_multi_az",
            "aws_rds_instance_multi_az_compliance_check",
            "aws_rds_multi_az_enabled",
            "aws_rds_cluster_multi_az"
        ],
        "recommendation": "Keep: aws_rds_instance_multi_az (instances), aws_rds_cluster_multi_az (clusters)",
        "rationale": "Instance and cluster are different resource types"
    },
    
    "rds_public_access": {
        "description": "RDS instances not publicly accessible",
        "functions": [
            "aws_rds_instance_no_public_access",
            "aws_rds_instance_public_access_check"
        ],
        "recommendation": "Keep: aws_rds_instance_no_public_access",
        "rationale": "Same check, consistent naming"
    },
    
    "rds_cloudwatch_logs": {
        "description": "RDS logs exported to CloudWatch",
        "functions": [
            "aws_rds_instance_integration_cloudwatch_logs",
            "aws_rds_cluster_integration_cloudwatch_logs"
        ],
        "recommendation": "Keep: Both",
        "rationale": "Instance and cluster logs are configured separately"
    },
    
    "rds_version_upgrade": {
        "description": "RDS auto minor version upgrade enabled",
        "functions": [
            "aws_rds_auto_minor_version_upgrade",
            "aws_rds_instance_auto_minor_version_upgrade_check"
        ],
        "recommendation": "Keep: aws_rds_instance_auto_minor_version_upgrade_check",
        "rationale": "More specific naming"
    },
    
    "lambda_public_access": {
        "description": "Lambda functions not publicly accessible",
        "functions": [
            "aws_lambda_function_not_publicly_accessible",
            "aws_lambda_function_public_access_check",
            "aws_lambda_function_restrict_public_access"
        ],
        "recommendation": "Keep: aws_lambda_function_restrict_public_access",
        "rationale": "Most explicit naming about what should be done"
    },
    
    "lambda_vpc": {
        "description": "Lambda functions inside VPC",
        "functions": [
            "aws_lambda_function_inside_vpc"
        ],
        "recommendation": "Keep: aws_lambda_function_inside_vpc",
        "rationale": "Only one function for this check"
    },
    
    "kms_key_rotation": {
        "description": "KMS CMK automatic rotation enabled",
        "functions": [
            "aws_kms_cmk_rotation_enabled",
            "aws_kms_key_rotation_enabled",
            "aws_kms_symmetric_cmk_rotation_enabled",
            "aws_kms_symmetric_key_rotation_enabled"
        ],
        "recommendation": "Keep: aws_kms_cmk_rotation_enabled",
        "rationale": "CMK is the correct term (Customer Master Key); symmetric is implied for rotation"
    },
    
    "cloudwatch_log_encryption": {
        "description": "CloudWatch Log Groups encrypted with KMS",
        "functions": [
            "aws_cloudwatch_log_group_kms_encryption_enabled"
        ],
        "recommendation": "Keep: aws_cloudwatch_log_group_kms_encryption_enabled",
        "rationale": "Only function for this check"
    },
    
    "cloudwatch_log_retention": {
        "description": "CloudWatch Log Groups have retention policy",
        "functions": [
            "aws_cloudwatch_log_group_retention",
            "aws_cloudwatch_log_group_retention_policy_specific_days_enabled"
        ],
        "recommendation": "Keep: aws_cloudwatch_log_group_retention",
        "rationale": "Generic check is sufficient, covers all retention periods"
    },
    
    "vpc_flow_logs": {
        "description": "VPC Flow Logs enabled",
        "functions": [
            "aws_vpc_flow_logs_enabled",
            "aws_ec2_vpc_flow_logging_reject_enabled"
        ],
        "recommendation": "Keep: Both",
        "rationale": "First checks if enabled, second checks if REJECT traffic is logged (more stringent)"
    },
    
    "guardduty_enabled": {
        "description": "GuardDuty enabled",
        "functions": [
            "aws_guardduty_enabled",
            "aws_guardduty_is_enabled"
        ],
        "recommendation": "Keep: aws_guardduty_enabled",
        "rationale": "Same check, simpler naming"
    },
    
    "config_enabled": {
        "description": "AWS Config enabled",
        "functions": [
            "aws_config_enabled",
            "aws_config_recorder_all_regions_enabled",
            "aws_config_configuration_recorder_enabled_in_all_regions",
            "aws_config_recorder_status_check_all_regions"
        ],
        "recommendation": "Keep: aws_config_recorder_all_regions_enabled",
        "rationale": "Most specific - Config must be in all regions"
    },
    
    "securityhub_enabled": {
        "description": "Security Hub enabled",
        "functions": [
            "aws_securityhub_enabled",
            "aws_securityhub_hub_enabled_in_all_regions",
            "aws_securityhub_hub_status_check"
        ],
        "recommendation": "Keep: aws_securityhub_hub_enabled_in_all_regions",
        "rationale": "Security Hub should be enabled in all regions"
    },
    
    "elb_logging": {
        "description": "ELB access logging enabled",
        "functions": [
            "aws_elb_logging_enabled",
            "aws_elbv2_logging_enabled"
        ],
        "recommendation": "Keep: Both",
        "rationale": "Classic ELB vs ALB/NLB are different services"
    },
    
    "elb_ssl": {
        "description": "ELB uses SSL/TLS listeners",
        "functions": [
            "aws_elb_ssl_listeners",
            "aws_elbv2_insecure_ssl_ciphers"
        ],
        "recommendation": "Keep: Both",
        "rationale": "First checks SSL is used, second checks ciphers are secure"
    },
    
    "dynamodb_encryption": {
        "description": "DynamoDB tables encrypted",
        "functions": [
            "aws_dynamodb_encryption_enabled",
            "aws_dynamodb_tables_kms_cmk_encryption_enabled"
        ],
        "recommendation": "Keep: Both",
        "rationale": "First checks any encryption, second checks KMS CMK specifically"
    },
    
    "dynamodb_pitr": {
        "description": "DynamoDB point-in-time recovery enabled",
        "functions": [
            "aws_dynamodb_pitr_enabled",
            "aws_dynamodb_tables_pitr_enabled"
        ],
        "recommendation": "Keep: aws_dynamodb_pitr_enabled",
        "rationale": "Same check, redundant naming"
    },
    
    "eks_secrets_encryption": {
        "description": "EKS secrets encrypted with KMS CMK",
        "functions": [
            "aws_eks_cluster_kms_cmk_encryption_in_secrets_enabled",
            "aws_eks_cluster_secrets_encryption_kms_cmk"
        ],
        "recommendation": "Keep: aws_eks_cluster_secrets_encryption_kms_cmk",
        "rationale": "Shorter, clearer naming"
    },
    
    "eks_public_endpoint": {
        "description": "EKS cluster endpoint not publicly accessible",
        "functions": [
            "aws_eks_cluster_not_publicly_accessible",
            "aws_eks_cluster_endpoint_access_check"
        ],
        "recommendation": "Keep: aws_eks_cluster_endpoint_access_check",
        "rationale": "More nuanced - checks endpoint access configuration, not just public/private"
    },
    
    "acm_certificate_expiration": {
        "description": "ACM certificates expiring soon",
        "functions": [
            "aws_acm_certificate_expiration"
        ],
        "recommendation": "Keep: aws_acm_certificate_expiration",
        "rationale": "Only function after consolidation"
    },
    
    "redshift_encryption": {
        "description": "Redshift cluster encrypted",
        "functions": [
            "aws_redshift_cluster_encrypted",
            "aws_redshift_cluster_encrypted_at_rest"
        ],
        "recommendation": "Keep: aws_redshift_cluster_encrypted",
        "rationale": "At-rest is implied for Redshift encryption"
    },
    
    "redshift_audit_logging": {
        "description": "Redshift audit logging enabled",
        "functions": [
            "aws_redshift_cluster_audit_logging"
        ],
        "recommendation": "Keep: aws_redshift_cluster_audit_logging",
        "rationale": "Only function for this check"
    },
}

# Analyze actual compliance overlap
overlap_analysis = {}
for group_name, group_data in functional_groups.items():
    functions = group_data['functions']
    
    # Check if these functions exist in our dataset
    existing_functions = [f for f in functions if f in function_compliance]
    
    if not existing_functions:
        continue
    
    # Calculate compliance overlap
    compliance_sets = [function_compliance[f] for f in existing_functions]
    
    if len(compliance_sets) > 1:
        # Find common compliance IDs
        common = set.intersection(*compliance_sets)
        total_unique = set.union(*compliance_sets)
        overlap_pct = (len(common) / len(total_unique) * 100) if total_unique else 0
    else:
        common = compliance_sets[0] if compliance_sets else set()
        total_unique = compliance_sets[0] if compliance_sets else set()
        overlap_pct = 100
    
    overlap_analysis[group_name] = {
        "description": group_data['description'],
        "functions_found": existing_functions,
        "functions_count": len(existing_functions),
        "recommendation": group_data['recommendation'],
        "rationale": group_data['rationale'],
        "compliance_overlap_pct": round(overlap_pct, 1),
        "common_controls": len(common),
        "total_controls": len(total_unique),
        "verdict": "HIGH_OVERLAP" if overlap_pct > 80 else "MEDIUM_OVERLAP" if overlap_pct > 50 else "DISTINCT"
    }

# Save analysis
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(overlap_analysis, f, indent=2)

print(f"✅ Analysis saved: {OUTPUT_JSON.name}")
print()

# Summary
high_overlap = [g for g, d in overlap_analysis.items() if d['verdict'] == 'HIGH_OVERLAP']
medium_overlap = [g for g, d in overlap_analysis.items() if d['verdict'] == 'MEDIUM_OVERLAP']
distinct = [g for g, d in overlap_analysis.items() if d['verdict'] == 'DISTINCT']

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total functional groups analyzed: {len(overlap_analysis)}")
print(f"HIGH OVERLAP (>80%):    {len(high_overlap)} groups")
print(f"MEDIUM OVERLAP (50-80%): {len(medium_overlap)} groups")
print(f"DISTINCT (<50%):        {len(distinct)} groups")
print()

print("TOP 10 HIGH OVERLAP GROUPS (Consolidation Recommended):")
print("-" * 80)
high_overlap_sorted = sorted(
    [(g, overlap_analysis[g]) for g in high_overlap],
    key=lambda x: x[1]['compliance_overlap_pct'],
    reverse=True
)

for i, (group, data) in enumerate(high_overlap_sorted[:10], 1):
    print(f"{i}. {group}")
    print(f"   Overlap: {data['compliance_overlap_pct']}% ({data['functions_count']} functions)")
    print(f"   Recommendation: {data['recommendation']}")
    print()

print("=" * 80)
print(f"Full analysis: {OUTPUT_JSON.name}")

