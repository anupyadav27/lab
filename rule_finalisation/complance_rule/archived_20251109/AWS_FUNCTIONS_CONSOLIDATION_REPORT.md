# AWS Functions Consolidation Report
**Date:** November 8, 2025
**Analysis Type:** Functional Overlap - Keep Only Distinct Functions by Job

---

## Executive Summary

- **Total compliance controls:** 3907
- **Controls updated:** 450
- **Function consolidations:** 84
- **Final unique functions:** 528
- **Services covered:** 80

---

## Consolidation Decisions

### Rationale
Functions were consolidated based on:
1. **Functional Equivalence** - Multiple functions checking the same AWS configuration
2. **AWS Expert Analysis** - Understanding of actual AWS service behavior
3. **Compliance Overlap** - Analysis of which compliance controls use which functions

### Key Consolidations

#### CLOUDTRAIL

- ❌ `aws_cloudtrail_cloudwatch_logs_enabled`
  - ✅ Consolidated to: `aws_cloudtrail_cloudwatch_logging_enabled`

- ❌ `aws_cloudtrail_config_change_monitoring`
  - ✅ Consolidated to: `aws_cloudtrail_config_changes_monitoring`

- ❌ `aws_cloudtrail_enabled`
  - ✅ Consolidated to: `aws_cloudtrail_multi_region_enabled`

- ❌ `aws_cloudtrail_multi_region_enabled_logging_management_events`
  - ✅ Consolidated to: `aws_cloudtrail_multi_region_enabled`

- ❌ `aws_cloudtrail_s3_data_events_logging_enabled`
  - ✅ Consolidated to: `aws_cloudtrail_s3_dataevents_read_enabled`

- ❌ `aws_cloudtrail_s3_object_level_logging_enabled`
  - ✅ Consolidated to: `aws_cloudtrail_s3_dataevents_read_enabled`

- ❌ `aws_cloudtrail_trail_encryption_at_rest_kms_enabled`
  - ✅ Consolidated to: `aws_cloudtrail_kms_encryption_enabled`

- ❌ `aws_cloudtrail_trail_log_file_validation_check`
  - ✅ Consolidated to: `aws_cloudtrail_log_file_validation_enabled`

- ❌ `aws_cloudtrail_trail_log_file_validation_status_check`
  - ✅ Consolidated to: `aws_cloudtrail_log_file_validation_enabled`

- ❌ `aws_cloudtrail_trail_multi_region_logging_enabled`
  - ✅ Consolidated to: `aws_cloudtrail_multi_region_enabled`

- ❌ `aws_cloudtrail_trail_multi_region_management_logging_enabled`
  - ✅ Consolidated to: `aws_cloudtrail_multi_region_enabled`

- ❌ `aws_cloudtrail_trail_sse_kms_encryption_at_rest_enabled`
  - ✅ Consolidated to: `aws_cloudtrail_kms_encryption_enabled`

- ❌ `aws_cloudtrail_vpc_change_monitoring_configured`
  - ✅ Consolidated to: `aws_cloudtrail_vpc_changes_monitoring_enabled`

#### CLOUDWATCH

- ❌ `aws_cloudwatch_log_group_retention_policy_specific_days_enabled`
  - ✅ Consolidated to: `aws_cloudwatch_log_group_retention`

#### CONFIG

- ❌ `aws_config_configuration_recorder_enabled_in_all_regions`
  - ✅ Consolidated to: `aws_config_recorder_all_regions_enabled`

- ❌ `aws_config_enabled`
  - ✅ Consolidated to: `aws_config_recorder_all_regions_enabled`

- ❌ `aws_config_recorder_status_check_all_regions`
  - ✅ Consolidated to: `aws_config_recorder_all_regions_enabled`

#### DYNAMODB

- ❌ `aws_dynamodb_tables_pitr_enabled`
  - ✅ Consolidated to: `aws_dynamodb_pitr_enabled`

#### EBS

- ❌ `aws_ebs_snapshot_encryption`
  - ✅ Consolidated to: `aws_ec2_ebs_encryption_by_default_enabled`

#### EC2

- ❌ `aws_ec2_default_security_group_restriction_check`
  - ✅ Consolidated to: `aws_ec2_securitygroup_default_restrict_traffic`

- ❌ `aws_ec2_ebs_default_encryption`
  - ✅ Consolidated to: `aws_ec2_ebs_encryption_by_default_enabled`

- ❌ `aws_ec2_ebs_volume_encryption`
  - ✅ Consolidated to: `aws_ec2_ebs_encryption_by_default_enabled`

- ❌ `aws_ec2_ebs_volume_encryption_enabled`
  - ✅ Consolidated to: `aws_ec2_ebs_encryption_by_default_enabled`

- ❌ `aws_ec2_instance_account_imdsv2_enabled`
  - ✅ Consolidated to: `aws_ec2_instance_imdsv2_enabled`

- ❌ `aws_ec2_instance_metadata_service_imdsv2_required`
  - ✅ Consolidated to: `aws_ec2_instance_imdsv2_enabled`

- ❌ `aws_ec2_instance_public_ip`
  - ✅ Consolidated to: `aws_ec2_instance_no_public_ip`

- ❌ `aws_ec2_security_group_ingress_ssh_rdp_restricted`
  - ✅ Consolidated to: `aws_ec2_securitygroup_ssh_restricted`

- ❌ `aws_ec2_securitygroup_allow_ingress_from_internet_to_any_port`
  - ✅ Consolidated to: `aws_ec2_securitygroup_allow_ingress_from_internet_to_all_ports`

- ❌ `aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22`
  - ✅ Consolidated to: `aws_ec2_securitygroup_ssh_restricted`

- ❌ `aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_3389`
  - ✅ Consolidated to: `aws_ec2_securitygroup_rdp_restricted`

- ❌ `aws_ec2_securitygroup_allow_wide_open_public_ipv4`
  - ✅ Consolidated to: `aws_ec2_securitygroup_allow_ingress_from_internet_to_all_ports`

- ❌ `aws_ec2_securitygroup_default_restricted`
  - ✅ Consolidated to: `aws_ec2_securitygroup_default_restrict_traffic`

#### EKS

- ❌ `aws_eks_cluster_kms_cmk_encryption_in_secrets_enabled`
  - ✅ Consolidated to: `aws_eks_cluster_secrets_encryption_kms_cmk`

- ❌ `aws_eks_cluster_not_publicly_accessible`
  - ✅ Consolidated to: `aws_eks_cluster_endpoint_access_check`

#### GUARDDUTY

- ❌ `aws_guardduty_is_enabled`
  - ✅ Consolidated to: `aws_guardduty_enabled`

#### IAM

- ❌ `aws_iam_access_key_rotation_check`
  - ✅ Consolidated to: `aws_iam_access_key_rotation_90_days_check`

- ❌ `aws_iam_password_policy_compliance`
  - ✅ Consolidated to: `aws_iam_password_policy_minimum_length_14`

- ❌ `aws_iam_password_policy_minimum_length_check`
  - ✅ Consolidated to: `aws_iam_password_policy_minimum_length_14`

- ❌ `aws_iam_password_policy_password_reuse_prevention_check`
  - ✅ Consolidated to: `aws_iam_password_policy_minimum_length_14`

- ❌ `aws_iam_password_policy_prevent_password_reuse_min_24`
  - ✅ Consolidated to: `aws_iam_password_policy_minimum_length_14`

- ❌ `aws_iam_password_policy_strong`
  - ✅ Consolidated to: `aws_iam_password_policy_minimum_length_14`

- ❌ `aws_iam_role_awssupport_access_policy_check`
  - ✅ Consolidated to: `aws_iam_role_awssupport_access_policy_attachment`

- ❌ `aws_iam_root_hardware_mfa_check`
  - ✅ Consolidated to: `aws_iam_root_hardware_mfa_enabled`

- ❌ `aws_iam_root_mfa_status_check`
  - ✅ Consolidated to: `aws_iam_root_mfa_enabled`

- ❌ `aws_iam_root_user_access_key_check`
  - ✅ Consolidated to: `aws_iam_no_root_access_key`

- ❌ `aws_iam_root_user_access_keys_existence_check`
  - ✅ Consolidated to: `aws_iam_no_root_access_key`

- ❌ `aws_iam_root_user_mfa_check`
  - ✅ Consolidated to: `aws_iam_root_mfa_enabled`

- ❌ `aws_iam_rotate_access_key_90_days`
  - ✅ Consolidated to: `aws_iam_access_key_rotation_90_days_check`

- ❌ `aws_iam_user_console_password_mfa_check`
  - ✅ Consolidated to: `aws_iam_user_mfa_enabled_console_access`

- ❌ `aws_iam_user_credentials_unused_for_45_days_disabled`
  - ✅ Consolidated to: `aws_iam_user_credentials_unused_45_days_disabled`

- ❌ `aws_iam_user_group_membership`
  - ✅ Consolidated to: `aws_iam_user_in_group`

- ❌ `aws_iam_user_mfa_enabled`
  - ✅ Consolidated to: `aws_iam_user_mfa_enabled_console_access`

- ❌ `aws_iam_user_mfa_status_check_for_console_access`
  - ✅ Consolidated to: `aws_iam_user_mfa_enabled_console_access`

- ❌ `aws_iam_user_permissions_group_only_check`
  - ✅ Consolidated to: `aws_iam_user_in_group`

- ❌ `aws_iam_user_permissions_group_only_compliance`
  - ✅ Consolidated to: `aws_iam_user_in_group`

- ❌ `aws_iam_user_unused_credentials`
  - ✅ Consolidated to: `aws_iam_user_credentials_unused_45_days_disabled`

- ❌ `aws_iam_user_unused_credentials_disabled`
  - ✅ Consolidated to: `aws_iam_user_credentials_unused_45_days_disabled`

#### KMS

- ❌ `aws_kms_key_rotation_enabled`
  - ✅ Consolidated to: `aws_kms_cmk_rotation_enabled`

- ❌ `aws_kms_symmetric_cmk_rotation_enabled`
  - ✅ Consolidated to: `aws_kms_cmk_rotation_enabled`

- ❌ `aws_kms_symmetric_key_rotation_enabled`
  - ✅ Consolidated to: `aws_kms_cmk_rotation_enabled`

#### LAMBDA

- ❌ `aws_lambda_function_not_publicly_accessible`
  - ✅ Consolidated to: `aws_lambda_function_restrict_public_access`

- ❌ `aws_lambda_function_public_access_check`
  - ✅ Consolidated to: `aws_lambda_function_restrict_public_access`

#### RDS

- ❌ `aws_rds_aurora_backup_enabled`
  - ✅ Consolidated to: `aws_rds_instance_backup_enabled`

- ❌ `aws_rds_auto_minor_version_upgrade`
  - ✅ Consolidated to: `aws_rds_instance_auto_minor_version_upgrade_check`

- ❌ `aws_rds_backup_enabled`
  - ✅ Consolidated to: `aws_rds_instance_backup_enabled`

- ❌ `aws_rds_instance_encryption_at_rest_enabled`
  - ✅ Consolidated to: `aws_rds_instance_storage_encrypted`

- ❌ `aws_rds_instance_encryption_enabled`
  - ✅ Consolidated to: `aws_rds_instance_storage_encrypted`

- ❌ `aws_rds_instance_multi_az_compliance_check`
  - ✅ Consolidated to: `aws_rds_instance_multi_az`

- ❌ `aws_rds_instance_public_access_check`
  - ✅ Consolidated to: `aws_rds_instance_no_public_access`

- ❌ `aws_rds_multi_az_enabled`
  - ✅ Consolidated to: `aws_rds_instance_multi_az`

- ❌ `aws_rds_storage_encrypted`
  - ✅ Consolidated to: `aws_rds_instance_storage_encrypted`

#### REDSHIFT

- ❌ `aws_redshift_cluster_encrypted_at_rest`
  - ✅ Consolidated to: `aws_redshift_cluster_encrypted`

#### S3

- ❌ `aws_s3_bucket_cross_region_replication`
  - ✅ Consolidated to: `aws_s3_bucket_replication_enabled`

- ❌ `aws_s3_bucket_default_encryption`
  - ✅ Consolidated to: `aws_s3_bucket_encryption_enabled`

- ❌ `aws_s3_bucket_default_kms_encryption`
  - ✅ Consolidated to: `aws_s3_bucket_encryption_enabled`

- ❌ `aws_s3_bucket_logging_enabled`
  - ✅ Consolidated to: `aws_s3_bucket_server_access_logging_enabled`

- ❌ `aws_s3_bucket_object_versioning`
  - ✅ Consolidated to: `aws_s3_bucket_versioning_enabled`

- ❌ `aws_s3_bucket_policy_in_transit_http_access_denied`
  - ✅ Consolidated to: `aws_s3_bucket_secure_transport_policy`

- ❌ `aws_s3_bucket_policy_public_write_access`
  - ✅ Consolidated to: `aws_s3_account_level_public_access_blocks`

- ❌ `aws_s3_bucket_public_access`
  - ✅ Consolidated to: `aws_s3_account_level_public_access_blocks`

- ❌ `aws_s3_cloudtrail_bucket_logging_enabled`
  - ✅ Consolidated to: `aws_s3_cloudtrail_bucket_access_logging_enabled`

- ❌ `aws_s3_public_access_block_check`
  - ✅ Consolidated to: `aws_s3_account_level_public_access_blocks`

#### SECURITYHUB

- ❌ `aws_securityhub_enabled`
  - ✅ Consolidated to: `aws_securityhub_hub_enabled_in_all_regions`

- ❌ `aws_securityhub_hub_status_check`
  - ✅ Consolidated to: `aws_securityhub_hub_enabled_in_all_regions`

---

## Final Function Count by Service

| Service | Function Count |
|---------|---------------|
| No checks defined | 1 |
| accessanalyzer | 2 |
| account | 5 |
| acm | 1 |
| apigateway | 9 |
| apigatewayv2 | 1 |
| appstream | 1 |
| appsync | 1 |
| athena | 2 |
| autoscaling | 4 |
| backup | 12 |
| bedrock | 2 |
| cloudfront | 8 |
| cloudtrail | 29 |
| cloudwatch | 25 |
| codeartifact | 1 |
| codebuild | 8 |
| config | 2 |
| datasync | 1 |
| directconnect | 2 |
| directoryservice | 2 |
| dms | 5 |
| docdb | 6 |
| documentdb | 6 |
| drs | 1 |
| dynamodb | 10 |
| ebs | 1 |
| ec2 | 81 |
| ecr | 4 |
| ecs | 5 |
| edr | 1 |
| efs | 8 |
| eip | 1 |
| eks | 9 |
| elastic | 1 |
| elasticache | 5 |
| elasticbeanstalk | 2 |
| elb | 6 |
| elbv2 | 9 |
| emr | 3 |
| eventbridge | 1 |
| firehose | 1 |
| fsx | 4 |
| glacier | 1 |
| glue | 11 |
| guardduty | 6 |
| iam | 46 |
| inspector | 1 |
| kafka | 3 |
| keyspaces | 2 |
| kinesis | 2 |
| kms | 9 |
| lambda | 16 |
| mq | 3 |
| neptune | 12 |
| networkfirewall | 3 |
| opensearch | 10 |
| organizations | 2 |
| qldb | 5 |
| rds | 27 |
| redshift | 10 |
| route53 | 1 |
| s3 | 16 |
| sagemaker | 8 |
| secretsmanager | 1 |
| securityhub | 1 |
| servicecatalog | 1 |
| shield | 1 |
| sns | 3 |
| sqs | 2 |
| ssm | 3 |
| stepfunctions | 1 |
| storagegateway | 1 |
| timestream | 6 |
| transfer | 1 |
| vpc | 16 |
| waf | 1 |
| wafv2 | 2 |
| wellarchitected | 1 |
| workspaces | 4 |

---

## Analysis Details

### Cloudtrail Cloudwatch Integration

**Description:** CloudTrail logs integrated with CloudWatch

**Functions Analyzed:** 2

- ✅ `aws_cloudtrail_cloudwatch_logging_enabled` (kept)
- ❌ `aws_cloudtrail_cloudwatch_logs_enabled` → `aws_cloudtrail_cloudwatch_logging_enabled`

**Rationale:** Same check, different naming

### Cloudtrail Config Changes

**Description:** Monitor AWS Config configuration changes

**Functions Analyzed:** 2

- ❌ `aws_cloudtrail_config_change_monitoring` → `aws_cloudtrail_config_changes_monitoring`
- ✅ `aws_cloudtrail_config_changes_monitoring` (kept)

**Rationale:** Identical function, singular vs plural naming

### Cloudtrail Enabled

**Description:** Ensure CloudTrail is enabled and properly configured

**Functions Analyzed:** 5

- ❌ `aws_cloudtrail_enabled` → `aws_cloudtrail_multi_region_enabled`
- ✅ `aws_cloudtrail_multi_region_enabled` (kept)
- ❌ `aws_cloudtrail_trail_multi_region_logging_enabled` → `aws_cloudtrail_multi_region_enabled`
- ❌ `aws_cloudtrail_multi_region_enabled_logging_management_events` → `aws_cloudtrail_multi_region_enabled`
- ❌ `aws_cloudtrail_trail_multi_region_management_logging_enabled` → `aws_cloudtrail_multi_region_enabled`

**Rationale:** Multi-region CloudTrail enables single-region by default. Checking multi-region is sufficient.

### Cloudtrail Kms Encryption

**Description:** CloudTrail log encryption with KMS

**Functions Analyzed:** 3

- ✅ `aws_cloudtrail_kms_encryption_enabled` (kept)
- ❌ `aws_cloudtrail_trail_encryption_at_rest_kms_enabled` → `aws_cloudtrail_kms_encryption_enabled`
- ❌ `aws_cloudtrail_trail_sse_kms_encryption_at_rest_enabled` → `aws_cloudtrail_kms_encryption_enabled`

**Rationale:** All check the same thing - KMS encryption for CloudTrail

### Cloudtrail Log Validation

**Description:** CloudTrail log file integrity validation

**Functions Analyzed:** 3

- ✅ `aws_cloudtrail_log_file_validation_enabled` (kept)
- ❌ `aws_cloudtrail_trail_log_file_validation_check` → `aws_cloudtrail_log_file_validation_enabled`
- ❌ `aws_cloudtrail_trail_log_file_validation_status_check` → `aws_cloudtrail_log_file_validation_enabled`

**Rationale:** All verify log file validation is enabled

### Cloudtrail S3 Data Events

**Description:** S3 object-level logging via CloudTrail

**Functions Analyzed:** 4

- ❌ `aws_cloudtrail_s3_data_events_logging_enabled` → `aws_cloudtrail_s3_dataevents_read_enabled`
- ❌ `aws_cloudtrail_s3_object_level_logging_enabled` → `aws_cloudtrail_s3_dataevents_read_enabled`
- ✅ `aws_cloudtrail_s3_dataevents_read_enabled` (kept)
- ✅ `aws_cloudtrail_s3_dataevents_write_enabled` (kept)

**Rationale:** Read and write are distinct permissions. The generic 'data_events' checks are redundant if you have both read/write.

### Cloudtrail Vpc Changes

**Description:** Monitor VPC configuration changes

**Functions Analyzed:** 2

- ❌ `aws_cloudtrail_vpc_change_monitoring_configured` → `aws_cloudtrail_vpc_changes_monitoring_enabled`
- ✅ `aws_cloudtrail_vpc_changes_monitoring_enabled` (kept)

**Rationale:** Same monitoring, different naming convention

### Cloudwatch Log Retention

**Description:** CloudWatch Log Groups have retention policy

**Functions Analyzed:** 2

- ✅ `aws_cloudwatch_log_group_retention` (kept)
- ❌ `aws_cloudwatch_log_group_retention_policy_specific_days_enabled` → `aws_cloudwatch_log_group_retention`

**Rationale:** Generic check is sufficient, covers all retention periods

### Config Enabled

**Description:** AWS Config enabled

**Functions Analyzed:** 4

- ❌ `aws_config_enabled` → `aws_config_recorder_all_regions_enabled`
- ✅ `aws_config_recorder_all_regions_enabled` (kept)
- ❌ `aws_config_configuration_recorder_enabled_in_all_regions` → `aws_config_recorder_all_regions_enabled`
- ❌ `aws_config_recorder_status_check_all_regions` → `aws_config_recorder_all_regions_enabled`

**Rationale:** Most specific - Config must be in all regions

### Dynamodb Encryption

**Description:** DynamoDB tables encrypted

**Functions Analyzed:** 2

- ✅ `aws_dynamodb_encryption_enabled` (kept)
- ✅ `aws_dynamodb_tables_kms_cmk_encryption_enabled` (kept)

**Rationale:** First checks any encryption, second checks KMS CMK specifically

### Dynamodb Pitr

**Description:** DynamoDB point-in-time recovery enabled

**Functions Analyzed:** 2

- ✅ `aws_dynamodb_pitr_enabled` (kept)
- ❌ `aws_dynamodb_tables_pitr_enabled` → `aws_dynamodb_pitr_enabled`

**Rationale:** Same check, redundant naming

### Ec2 Default Security Group

**Description:** Default security group restricts all traffic

**Functions Analyzed:** 3

- ❌ `aws_ec2_default_security_group_restriction_check` → `aws_ec2_securitygroup_default_restrict_traffic`
- ✅ `aws_ec2_securitygroup_default_restrict_traffic` (kept)
- ❌ `aws_ec2_securitygroup_default_restricted` → `aws_ec2_securitygroup_default_restrict_traffic`

**Rationale:** All check default SG is locked down

### Ec2 Ebs Encryption

**Description:** EBS volumes encrypted

**Functions Analyzed:** 7

- ❌ `aws_ec2_ebs_default_encryption` → `aws_ec2_ebs_encryption_by_default_enabled`
- ✅ `aws_ec2_ebs_encryption_by_default_enabled` (kept)
- ✅ `aws_ec2_ebs_volume_encrypted` (kept)
- ❌ `aws_ec2_ebs_volume_encryption` → `aws_ec2_ebs_encryption_by_default_enabled`
- ❌ `aws_ec2_ebs_volume_encryption_enabled` → `aws_ec2_ebs_encryption_by_default_enabled`
- ✅ `aws_ec2_ebs_snapshots_encrypted` (kept)
- ❌ `aws_ebs_snapshot_encryption` → `aws_ec2_ebs_encryption_by_default_enabled`

**Rationale:** Three distinct checks: default setting, individual volumes, snapshots

### Ec2 Ebs Public

**Description:** EBS snapshots not public

**Functions Analyzed:** 2

- ✅ `aws_ec2_ebs_public_snapshot` (kept)
- ✅ `aws_ec2_ebs_snapshot_account_block_public_access` (kept)

**Rationale:** First checks individual snapshots, second checks account-level block setting

### Ec2 Imdsv2

**Description:** EC2 Instance Metadata Service v2 required

**Functions Analyzed:** 4

- ✅ `aws_ec2_instance_imdsv2_enabled` (kept)
- ❌ `aws_ec2_instance_metadata_service_imdsv2_required` → `aws_ec2_instance_imdsv2_enabled`
- ❌ `aws_ec2_instance_account_imdsv2_enabled` → `aws_ec2_instance_imdsv2_enabled`
- ✅ `aws_ec2_launch_template_imdsv2_required` (kept)

**Rationale:** Need to check both running instances and launch templates separately

### Ec2 Public Ip

**Description:** EC2 instances should not have public IPs

**Functions Analyzed:** 3

- ❌ `aws_ec2_instance_public_ip` → `aws_ec2_instance_no_public_ip`
- ✅ `aws_ec2_instance_no_public_ip` (kept)
- ✅ `aws_ec2_launch_template_no_public_ip` (kept)

**Rationale:** Check both instances and templates; naming should be consistent (no_public_ip)

### Ec2 Sg Rdp Restricted

**Description:** Security groups don't allow RDP from internet

**Functions Analyzed:** 2

- ❌ `aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_3389` → `aws_ec2_securitygroup_rdp_restricted`
- ✅ `aws_ec2_securitygroup_rdp_restricted` (kept)

**Rationale:** Consolidated port check into named function

### Ec2 Sg Ssh Restricted

**Description:** Security groups don't allow SSH from internet

**Functions Analyzed:** 3

- ❌ `aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22` → `aws_ec2_securitygroup_ssh_restricted`
- ✅ `aws_ec2_securitygroup_ssh_restricted` (kept)
- ❌ `aws_ec2_security_group_ingress_ssh_rdp_restricted` → `aws_ec2_securitygroup_ssh_restricted`

**Rationale:** SSH and RDP are different protocols, check separately

### Ec2 Sg Unrestricted

**Description:** Security groups don't allow unrestricted access

**Functions Analyzed:** 3

- ✅ `aws_ec2_securitygroup_allow_ingress_from_internet_to_all_ports` (kept)
- ❌ `aws_ec2_securitygroup_allow_ingress_from_internet_to_any_port` → `aws_ec2_securitygroup_allow_ingress_from_internet_to_all_ports`
- ❌ `aws_ec2_securitygroup_allow_wide_open_public_ipv4` → `aws_ec2_securitygroup_allow_ingress_from_internet_to_all_ports`

**Rationale:** All check for 0.0.0.0/0 on all ports

### Eks Public Endpoint

**Description:** EKS cluster endpoint not publicly accessible

**Functions Analyzed:** 2

- ❌ `aws_eks_cluster_not_publicly_accessible` → `aws_eks_cluster_endpoint_access_check`
- ✅ `aws_eks_cluster_endpoint_access_check` (kept)

**Rationale:** More nuanced - checks endpoint access configuration, not just public/private

### Eks Secrets Encryption

**Description:** EKS secrets encrypted with KMS CMK

**Functions Analyzed:** 2

- ❌ `aws_eks_cluster_kms_cmk_encryption_in_secrets_enabled` → `aws_eks_cluster_secrets_encryption_kms_cmk`
- ✅ `aws_eks_cluster_secrets_encryption_kms_cmk` (kept)

**Rationale:** Shorter, clearer naming

### Elb Logging

**Description:** ELB access logging enabled

**Functions Analyzed:** 2

- ✅ `aws_elb_logging_enabled` (kept)
- ✅ `aws_elbv2_logging_enabled` (kept)

**Rationale:** Classic ELB vs ALB/NLB are different services

### Elb Ssl

**Description:** ELB uses SSL/TLS listeners

**Functions Analyzed:** 2

- ✅ `aws_elb_ssl_listeners` (kept)
- ✅ `aws_elbv2_insecure_ssl_ciphers` (kept)

**Rationale:** First checks SSL is used, second checks ciphers are secure

### Guardduty Enabled

**Description:** GuardDuty enabled

**Functions Analyzed:** 2

- ✅ `aws_guardduty_enabled` (kept)
- ❌ `aws_guardduty_is_enabled` → `aws_guardduty_enabled`

**Rationale:** Same check, simpler naming

### Iam Access Analyzer

**Description:** IAM Access Analyzer enabled

**Functions Analyzed:** 2

- ✅ `aws_iam_access_analyzer_active_status_all_regions` (kept)
- ✅ `aws_iam_access_analyzer_external_access_enabled_all_regions` (kept)

**Rationale:** First checks if active, second checks if external access analysis is on

### Iam Access Key Rotation

**Description:** IAM access keys rotated regularly

**Functions Analyzed:** 3

- ✅ `aws_iam_access_key_rotation_90_days_check` (kept)
- ❌ `aws_iam_access_key_rotation_check` → `aws_iam_access_key_rotation_90_days_check`
- ❌ `aws_iam_rotate_access_key_90_days` → `aws_iam_access_key_rotation_90_days_check`

**Rationale:** Specific 90-day requirement is CIS benchmark standard

### Iam Password Policy

**Description:** IAM password policy compliance

**Functions Analyzed:** 9

- ❌ `aws_iam_password_policy_compliance` → `aws_iam_password_policy_minimum_length_14`
- ❌ `aws_iam_password_policy_strong` → `aws_iam_password_policy_minimum_length_14`
- ✅ `aws_iam_password_policy_minimum_length_14` (kept)
- ❌ `aws_iam_password_policy_minimum_length_check` → `aws_iam_password_policy_minimum_length_14`
- ✅ `aws_iam_password_policy_expires_passwords_within_90_days_or_less` (kept)
- ❌ `aws_iam_password_policy_password_reuse_prevention_check` → `aws_iam_password_policy_minimum_length_14`
- ❌ `aws_iam_password_policy_prevent_password_reuse_min_24` → `aws_iam_password_policy_minimum_length_14`
- ✅ `aws_iam_password_policy_reuse_24` (kept)
- ✅ `aws_iam_user_password_policy_complex` (kept)

**Rationale:** Each checks a specific password policy requirement: length, expiry, reuse, complexity

### Iam Root Access Keys

**Description:** Root account access keys should not exist

**Functions Analyzed:** 3

- ✅ `aws_iam_no_root_access_key` (kept)
- ❌ `aws_iam_root_user_access_key_check` → `aws_iam_no_root_access_key`
- ❌ `aws_iam_root_user_access_keys_existence_check` → `aws_iam_no_root_access_key`

**Rationale:** Most concise naming, same check

### Iam Root Hardware Mfa

**Description:** Root account hardware MFA (not virtual)

**Functions Analyzed:** 2

- ✅ `aws_iam_root_hardware_mfa_enabled` (kept)
- ❌ `aws_iam_root_hardware_mfa_check` → `aws_iam_root_hardware_mfa_enabled`

**Rationale:** Same check, different naming

### Iam Root Mfa

**Description:** Root account MFA enabled

**Functions Analyzed:** 3

- ✅ `aws_iam_root_mfa_enabled` (kept)
- ❌ `aws_iam_root_mfa_status_check` → `aws_iam_root_mfa_enabled`
- ❌ `aws_iam_root_user_mfa_check` → `aws_iam_root_mfa_enabled`

**Rationale:** All check root MFA status

### Iam Support Role

**Description:** AWS Support access role exists

**Functions Analyzed:** 2

- ✅ `aws_iam_role_awssupport_access_policy_attachment` (kept)
- ❌ `aws_iam_role_awssupport_access_policy_check` → `aws_iam_role_awssupport_access_policy_attachment`

**Rationale:** Same check, slightly different naming

### Iam Unused Credentials

**Description:** IAM users with unused credentials

**Functions Analyzed:** 4

- ✅ `aws_iam_user_credentials_unused_45_days_disabled` (kept)
- ❌ `aws_iam_user_credentials_unused_for_45_days_disabled` → `aws_iam_user_credentials_unused_45_days_disabled`
- ❌ `aws_iam_user_unused_credentials` → `aws_iam_user_credentials_unused_45_days_disabled`
- ❌ `aws_iam_user_unused_credentials_disabled` → `aws_iam_user_credentials_unused_45_days_disabled`

**Rationale:** 45 days is the standard threshold

### Iam User In Groups

**Description:** IAM users should be in groups, not have direct policies

**Functions Analyzed:** 4

- ✅ `aws_iam_user_in_group` (kept)
- ❌ `aws_iam_user_group_membership` → `aws_iam_user_in_group`
- ❌ `aws_iam_user_permissions_group_only_check` → `aws_iam_user_in_group`
- ❌ `aws_iam_user_permissions_group_only_compliance` → `aws_iam_user_in_group`

**Rationale:** Two distinct checks: (1) Is user in a group? (2) Does user have direct policies?

### Iam User Mfa

**Description:** IAM users with console access have MFA

**Functions Analyzed:** 4

- ❌ `aws_iam_user_mfa_enabled` → `aws_iam_user_mfa_enabled_console_access`
- ✅ `aws_iam_user_mfa_enabled_console_access` (kept)
- ❌ `aws_iam_user_mfa_status_check_for_console_access` → `aws_iam_user_mfa_enabled_console_access`
- ❌ `aws_iam_user_console_password_mfa_check` → `aws_iam_user_mfa_enabled_console_access`

**Rationale:** Specifically checks console access users (most accurate)

### Kms Key Rotation

**Description:** KMS CMK automatic rotation enabled

**Functions Analyzed:** 4

- ✅ `aws_kms_cmk_rotation_enabled` (kept)
- ❌ `aws_kms_key_rotation_enabled` → `aws_kms_cmk_rotation_enabled`
- ❌ `aws_kms_symmetric_cmk_rotation_enabled` → `aws_kms_cmk_rotation_enabled`
- ❌ `aws_kms_symmetric_key_rotation_enabled` → `aws_kms_cmk_rotation_enabled`

**Rationale:** CMK is the correct term (Customer Master Key); symmetric is implied for rotation

### Lambda Public Access

**Description:** Lambda functions not publicly accessible

**Functions Analyzed:** 3

- ❌ `aws_lambda_function_not_publicly_accessible` → `aws_lambda_function_restrict_public_access`
- ❌ `aws_lambda_function_public_access_check` → `aws_lambda_function_restrict_public_access`
- ✅ `aws_lambda_function_restrict_public_access` (kept)

**Rationale:** Most explicit naming about what should be done

### Rds Backup

**Description:** RDS automated backups enabled

**Functions Analyzed:** 4

- ❌ `aws_rds_backup_enabled` → `aws_rds_instance_backup_enabled`
- ✅ `aws_rds_instance_backup_enabled` (kept)
- ❌ `aws_rds_aurora_backup_enabled` → `aws_rds_instance_backup_enabled`
- ✅ `aws_rds_backup_retention_period` (kept)

**Rationale:** Two checks: is backup on, and is retention sufficient

### Rds Cloudwatch Logs

**Description:** RDS logs exported to CloudWatch

**Functions Analyzed:** 2

- ✅ `aws_rds_instance_integration_cloudwatch_logs` (kept)
- ✅ `aws_rds_cluster_integration_cloudwatch_logs` (kept)

**Rationale:** Instance and cluster logs are configured separately

### Rds Encryption

**Description:** RDS instance storage encrypted

**Functions Analyzed:** 5

- ❌ `aws_rds_instance_encryption_at_rest_enabled` → `aws_rds_instance_storage_encrypted`
- ❌ `aws_rds_instance_encryption_enabled` → `aws_rds_instance_storage_encrypted`
- ✅ `aws_rds_instance_storage_encrypted` (kept)
- ❌ `aws_rds_storage_encrypted` → `aws_rds_instance_storage_encrypted`
- ✅ `aws_rds_cluster_storage_encrypted` (kept)

**Rationale:** Instance and cluster encryption are separate checks

### Rds Multi Az

**Description:** RDS Multi-AZ enabled

**Functions Analyzed:** 4

- ✅ `aws_rds_instance_multi_az` (kept)
- ❌ `aws_rds_instance_multi_az_compliance_check` → `aws_rds_instance_multi_az`
- ❌ `aws_rds_multi_az_enabled` → `aws_rds_instance_multi_az`
- ✅ `aws_rds_cluster_multi_az` (kept)

**Rationale:** Instance and cluster are different resource types

### Rds Public Access

**Description:** RDS instances not publicly accessible

**Functions Analyzed:** 2

- ✅ `aws_rds_instance_no_public_access` (kept)
- ❌ `aws_rds_instance_public_access_check` → `aws_rds_instance_no_public_access`

**Rationale:** Same check, consistent naming

### Rds Version Upgrade

**Description:** RDS auto minor version upgrade enabled

**Functions Analyzed:** 2

- ❌ `aws_rds_auto_minor_version_upgrade` → `aws_rds_instance_auto_minor_version_upgrade_check`
- ✅ `aws_rds_instance_auto_minor_version_upgrade_check` (kept)

**Rationale:** More specific naming

### Redshift Encryption

**Description:** Redshift cluster encrypted

**Functions Analyzed:** 2

- ✅ `aws_redshift_cluster_encrypted` (kept)
- ❌ `aws_redshift_cluster_encrypted_at_rest` → `aws_redshift_cluster_encrypted`

**Rationale:** At-rest is implied for Redshift encryption

### S3 Bucket Encryption

**Description:** S3 bucket encryption at rest

**Functions Analyzed:** 4

- ❌ `aws_s3_bucket_default_encryption` → `aws_s3_bucket_encryption_enabled`
- ✅ `aws_s3_bucket_encryption_enabled` (kept)
- ✅ `aws_s3_bucket_kms_encryption` (kept)
- ❌ `aws_s3_bucket_default_kms_encryption` → `aws_s3_bucket_encryption_enabled`

**Rationale:** Two levels: (1) Is encryption enabled at all? (2) Is it KMS specifically?

### S3 Bucket Logging

**Description:** S3 bucket access logging

**Functions Analyzed:** 2

- ❌ `aws_s3_bucket_logging_enabled` → `aws_s3_bucket_server_access_logging_enabled`
- ✅ `aws_s3_bucket_server_access_logging_enabled` (kept)

**Rationale:** Same check, more explicit naming preferred

### S3 Bucket Replication

**Description:** S3 bucket cross-region replication

**Functions Analyzed:** 2

- ❌ `aws_s3_bucket_cross_region_replication` → `aws_s3_bucket_replication_enabled`
- ✅ `aws_s3_bucket_replication_enabled` (kept)

**Rationale:** Replication can be cross-region or same-region; generic check is better

### S3 Bucket Versioning

**Description:** S3 bucket versioning enabled

**Functions Analyzed:** 2

- ✅ `aws_s3_bucket_versioning_enabled` (kept)
- ❌ `aws_s3_bucket_object_versioning` → `aws_s3_bucket_versioning_enabled`

**Rationale:** Same check, versioning is at bucket level not object level (misleading name)

### S3 Cloudtrail Bucket Logging

**Description:** CloudTrail S3 bucket has access logging

**Functions Analyzed:** 2

- ✅ `aws_s3_cloudtrail_bucket_access_logging_enabled` (kept)
- ❌ `aws_s3_cloudtrail_bucket_logging_enabled` → `aws_s3_cloudtrail_bucket_access_logging_enabled`

**Rationale:** More specific naming for CloudTrail bucket logging

### S3 Public Access

**Description:** S3 bucket public access controls

**Functions Analyzed:** 6

- ❌ `aws_s3_bucket_public_access` → `aws_s3_account_level_public_access_blocks`
- ✅ `aws_s3_bucket_public_read_prohibited` (kept)
- ✅ `aws_s3_bucket_public_write_prohibited` (kept)
- ❌ `aws_s3_bucket_policy_public_write_access` → `aws_s3_account_level_public_access_blocks`
- ✅ `aws_s3_account_level_public_access_blocks` (kept)
- ❌ `aws_s3_public_access_block_check` → `aws_s3_account_level_public_access_blocks`

**Rationale:** Account-level blocks are different from bucket-level. Need both read and write checks.

### S3 Secure Transport

**Description:** S3 bucket requires HTTPS/TLS

**Functions Analyzed:** 2

- ✅ `aws_s3_bucket_secure_transport_policy` (kept)
- ❌ `aws_s3_bucket_policy_in_transit_http_access_denied` → `aws_s3_bucket_secure_transport_policy`

**Rationale:** Same policy check, different naming

### Securityhub Enabled

**Description:** Security Hub enabled

**Functions Analyzed:** 3

- ❌ `aws_securityhub_enabled` → `aws_securityhub_hub_enabled_in_all_regions`
- ✅ `aws_securityhub_hub_enabled_in_all_regions` (kept)
- ❌ `aws_securityhub_hub_status_check` → `aws_securityhub_hub_enabled_in_all_regions`

**Rationale:** Security Hub should be enabled in all regions

### Vpc Flow Logs

**Description:** VPC Flow Logs enabled

**Functions Analyzed:** 2

- ✅ `aws_vpc_flow_logs_enabled` (kept)
- ✅ `aws_ec2_vpc_flow_logging_reject_enabled` (kept)

**Rationale:** First checks if enabled, second checks if REJECT traffic is logged (more stringent)

---

## Files Generated

1. **consolidated_compliance_rules_FINAL.csv** - Final consolidated compliance CSV
2. **aws_functions_final_deduplicated.json** - Deduplicated functions by service
3. **AWS_FUNCTIONS_CONSOLIDATION_REPORT.md** - This report

---

*End of Report*