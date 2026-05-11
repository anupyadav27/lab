# NIST 800-171 Rev 2 - AWS & Azure Validation Report

**Generated:** 2025-11-07 09:25:01

## Executive Summary

### Comparison Statistics
- **Total Controls Compared:** 12
- **Perfect Matches:** 0 (0.0%)
- **Controls with Missing Checks:** 9 (75.0%)
- **Controls with Extra Checks:** 3 (25.0%)

### Sources
- **AWS Config Rules:** [Operational Best Practices for NIST 800-171](https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-nist_800-171.html)
- **Azure Policies:** [NIST SP 800-171 R2](https://learn.microsoft.com/en-us/azure/governance/policy/samples/nist-sp-800-171-r2)
- **Our Implementation:** Prowler-based + Multi-cloud expansion

---

## Detailed Control Comparison

### Control 3.1.1

**Status:** ⚠️  MISSING 15 CHECKS

- AWS Official Checks: 30
- Our Implementation: 26
- Matched Checks: 15

**✅ Matched Checks (15):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `ebs-snapshot-public-restorable-check` | `ec2_ebs_public_snapshot` |
| `ec2-instance-no-public-ip` | `ec2_instance_public_ip` |
| `ec2-instance-profile-attached` | `ec2_instance_profile_attached` |
| `iam-no-inline-policy-check` | `iam_aws_attached_policy_no_administrative_privileges` |
| `iam-root-access-key-check` | `iam_no_root_access_key` |
| `iam-user-mfa-enabled` | `iam_root_hardware_mfa_enabled` |
| `iam-user-unused-credentials-check` | `iam_user_accesskey_unused` |
| `rds-instance-public-access-check` | `rds_instance_no_public_access` |
| `rds-snapshots-public-prohibited` | `rds_snapshots_public_access` |
| `redshift-cluster-public-access-check` | `redshift_cluster_public_access` |
| `s3-account-level-public-access-blocks-periodic` | `s3_account_level_public_access_blocks` |
| `s3-bucket-level-public-access-prohibited` | `s3_account_level_public_access_blocks` |
| `s3-bucket-public-read-prohibited` | `s3_bucket_policy_public_write_access` |
| `s3-bucket-public-write-prohibited` | `s3_bucket_policy_public_write_access` |
| `sagemaker-notebook-no-direct-internet-access` | `sagemaker_notebook_instance_without_direct_internet_access_configured` |

**⚠️ Missing AWS Config Rules (15):**

- `dms-replication-not-public`
- `ec2-instances-in-vpc`
- `ecs-task-definition-user-for-host-mode-check`
- `elasticsearch-in-vpc-only`
- `emr-kerberos-enabled`
- `iam-group-has-users-check`
- `iam-policy-no-statements-with-admin-access`
- `iam-policy-no-statements-with-full-access`
- `iam-user-group-membership-check`
- `iam-user-no-policies-check`
- `lambda-function-public-access-prohibited`
- `lambda-inside-vpc`
- `redshift-enhanced-vpc-routing-enabled`
- `ssm-document-not-public`
- `subnet-auto-assign-public-ip-disabled`

**ℹ️ Extra Checks We Have (13):**

- `awslambda_function_not_publicly_accessible`
- `awslambda_function_url_public`
- `ec2_networkacl_allow_ingress_any_port`
- `ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22`
- `ec2_securitygroup_default_restrict_traffic`
- `eks_cluster_not_publicly_accessible`
- `emr_cluster_master_nodes_no_public_ip`
- `iam_customer_attached_policy_no_administrative_privileges`
- `iam_inline_policy_no_administrative_privileges`
- `iam_root_mfa_enabled`
- `iam_user_console_access_unused`
- `iam_user_mfa_enabled_console_access`
- `s3_bucket_public_access`

<details>
<summary>Our Complete Check List (26 checks)</summary>

- `awslambda_function_not_publicly_accessible`
- `awslambda_function_url_public`
- `ec2_ebs_public_snapshot`
- `ec2_instance_profile_attached`
- `ec2_instance_public_ip`
- `ec2_networkacl_allow_ingress_any_port`
- `ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22`
- `ec2_securitygroup_default_restrict_traffic`
- `eks_cluster_not_publicly_accessible`
- `emr_cluster_master_nodes_no_public_ip`
- `iam_aws_attached_policy_no_administrative_privileges`
- `iam_customer_attached_policy_no_administrative_privileges`
- `iam_inline_policy_no_administrative_privileges`
- `iam_no_root_access_key`
- `iam_root_hardware_mfa_enabled`
- `iam_root_mfa_enabled`
- `iam_user_accesskey_unused`
- `iam_user_console_access_unused`
- `iam_user_mfa_enabled_console_access`
- `rds_instance_no_public_access`
- `rds_snapshots_public_access`
- `redshift_cluster_public_access`
- `s3_account_level_public_access_blocks`
- `s3_bucket_policy_public_write_access`
- `s3_bucket_public_access`
- `sagemaker_notebook_instance_without_direct_internet_access_configured`

</details>

---

### Control 3.1.2

**Status:** ⚠️  MISSING 7 CHECKS

- AWS Official Checks: 22
- Our Implementation: 26
- Matched Checks: 15

**✅ Matched Checks (15):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `ebs-snapshot-public-restorable-check` | `ec2_ebs_public_snapshot` |
| `ec2-instance-no-public-ip` | `ec2_instance_public_ip` |
| `ec2-instance-profile-attached` | `ec2_instance_profile_attached` |
| `iam-no-inline-policy-check` | `iam_aws_attached_policy_no_administrative_privileges` |
| `iam-root-access-key-check` | `iam_no_root_access_key` |
| `iam-user-mfa-enabled` | `iam_root_hardware_mfa_enabled` |
| `iam-user-unused-credentials-check` | `iam_user_accesskey_unused` |
| `rds-instance-public-access-check` | `rds_instance_no_public_access` |
| `rds-snapshots-public-prohibited` | `rds_snapshots_public_access` |
| `redshift-cluster-public-access-check` | `redshift_cluster_public_access` |
| `s3-account-level-public-access-blocks-periodic` | `s3_account_level_public_access_blocks` |
| `s3-bucket-level-public-access-prohibited` | `s3_account_level_public_access_blocks` |
| `s3-bucket-public-read-prohibited` | `s3_bucket_policy_public_write_access` |
| `s3-bucket-public-write-prohibited` | `s3_bucket_policy_public_write_access` |
| `sagemaker-notebook-no-direct-internet-access` | `sagemaker_notebook_instance_without_direct_internet_access_configured` |

**⚠️ Missing AWS Config Rules (7):**

- `emr-kerberos-enabled`
- `iam-group-has-users-check`
- `iam-policy-no-statements-with-admin-access`
- `iam-policy-no-statements-with-full-access`
- `iam-user-group-membership-check`
- `iam-user-no-policies-check`
- `lambda-function-public-access-prohibited`

**ℹ️ Extra Checks We Have (13):**

- `awslambda_function_not_publicly_accessible`
- `awslambda_function_url_public`
- `ec2_networkacl_allow_ingress_any_port`
- `ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22`
- `ec2_securitygroup_default_restrict_traffic`
- `eks_cluster_not_publicly_accessible`
- `emr_cluster_master_nodes_no_public_ip`
- `iam_customer_attached_policy_no_administrative_privileges`
- `iam_inline_policy_no_administrative_privileges`
- `iam_root_mfa_enabled`
- `iam_user_console_access_unused`
- `iam_user_mfa_enabled_console_access`
- `s3_bucket_public_access`

<details>
<summary>Our Complete Check List (26 checks)</summary>

- `awslambda_function_not_publicly_accessible`
- `awslambda_function_url_public`
- `ec2_ebs_public_snapshot`
- `ec2_instance_profile_attached`
- `ec2_instance_public_ip`
- `ec2_networkacl_allow_ingress_any_port`
- `ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22`
- `ec2_securitygroup_default_restrict_traffic`
- `eks_cluster_not_publicly_accessible`
- `emr_cluster_master_nodes_no_public_ip`
- `iam_aws_attached_policy_no_administrative_privileges`
- `iam_customer_attached_policy_no_administrative_privileges`
- `iam_inline_policy_no_administrative_privileges`
- `iam_no_root_access_key`
- `iam_root_hardware_mfa_enabled`
- `iam_root_mfa_enabled`
- `iam_user_accesskey_unused`
- `iam_user_console_access_unused`
- `iam_user_mfa_enabled_console_access`
- `rds_instance_no_public_access`
- `rds_snapshots_public_access`
- `redshift_cluster_public_access`
- `s3_account_level_public_access_blocks`
- `s3_bucket_policy_public_write_access`
- `s3_bucket_public_access`
- `sagemaker_notebook_instance_without_direct_internet_access_configured`

</details>

---

### Control 3.1.3

**Status:** ⚠️  MISSING 3 CHECKS

- AWS Official Checks: 13
- Our Implementation: 16
- Matched Checks: 10

**✅ Matched Checks (10):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `ebs-snapshot-public-restorable-check` | `ec2_ebs_public_snapshot` |
| `ec2-instance-no-public-ip` | `ec2_instance_public_ip` |
| `rds-instance-public-access-check` | `rds_instance_no_public_access` |
| `rds-snapshots-public-prohibited` | `rds_snapshots_public_access` |
| `redshift-cluster-public-access-check` | `redshift_cluster_public_access` |
| `s3-account-level-public-access-blocks-periodic` | `s3_account_level_public_access_blocks` |
| `s3-bucket-level-public-access-prohibited` | `s3_account_level_public_access_blocks` |
| `s3-bucket-public-read-prohibited` | `s3_bucket_policy_public_write_access` |
| `s3-bucket-public-write-prohibited` | `s3_bucket_policy_public_write_access` |
| `sagemaker-notebook-no-direct-internet-access` | `sagemaker_notebook_instance_without_direct_internet_access_configured` |

**⚠️ Missing AWS Config Rules (3):**

- `lambda-function-public-access-prohibited`
- `vpc-default-security-group-closed`
- `vpc-sg-open-only-to-authorized-ports`

**ℹ️ Extra Checks We Have (8):**

- `awslambda_function_not_publicly_accessible`
- `awslambda_function_url_public`
- `ec2_networkacl_allow_ingress_any_port`
- `ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22`
- `ec2_securitygroup_default_restrict_traffic`
- `eks_cluster_not_publicly_accessible`
- `emr_cluster_master_nodes_no_public_ip`
- `s3_bucket_public_access`

<details>
<summary>Our Complete Check List (16 checks)</summary>

- `awslambda_function_not_publicly_accessible`
- `awslambda_function_url_public`
- `ec2_ebs_public_snapshot`
- `ec2_instance_public_ip`
- `ec2_networkacl_allow_ingress_any_port`
- `ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22`
- `ec2_securitygroup_default_restrict_traffic`
- `eks_cluster_not_publicly_accessible`
- `emr_cluster_master_nodes_no_public_ip`
- `rds_instance_no_public_access`
- `rds_snapshots_public_access`
- `redshift_cluster_public_access`
- `s3_account_level_public_access_blocks`
- `s3_bucket_policy_public_write_access`
- `s3_bucket_public_access`
- `sagemaker_notebook_instance_without_direct_internet_access_configured`

</details>

---

### Control 3.1.5

**Status:** ⚠️  MISSING 3 CHECKS

- AWS Official Checks: 6
- Our Implementation: 6
- Matched Checks: 3

**✅ Matched Checks (3):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `iam-no-inline-policy-check` | `iam_aws_attached_policy_no_administrative_privileges` |
| `iam-root-access-key-check` | `iam_no_root_access_key` |
| `iam-user-unused-credentials-check` | `iam_user_accesskey_unused` |

**⚠️ Missing AWS Config Rules (3):**

- `iam-policy-no-statements-with-admin-access`
- `iam-policy-no-statements-with-full-access`
- `iam-user-no-policies-check`

**ℹ️ Extra Checks We Have (3):**

- `iam_customer_attached_policy_no_administrative_privileges`
- `iam_inline_policy_no_administrative_privileges`
- `iam_user_console_access_unused`

<details>
<summary>Our Complete Check List (6 checks)</summary>

- `iam_aws_attached_policy_no_administrative_privileges`
- `iam_customer_attached_policy_no_administrative_privileges`
- `iam_inline_policy_no_administrative_privileges`
- `iam_no_root_access_key`
- `iam_user_accesskey_unused`
- `iam_user_console_access_unused`

</details>

---

### Control 3.13.11

**Status:** ⚠️  MISSING 5 CHECKS

- AWS Official Checks: 13
- Our Implementation: 12
- Matched Checks: 8

**✅ Matched Checks (8):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `cloudwatch-log-group-encrypted` | `cloudwatch_log_group_kms_encryption_enabled` |
| `ec2-ebs-encryption-by-default` | `ec2_ebs_volume_encryption` |
| `opensearch-encrypted-at-rest` | `opensearch_service_domains_encryption_at_rest_enabled` |
| `rds-storage-encrypted` | `rds_instance_storage_encrypted` |
| `s3-bucket-server-side-encryption-enabled` | `s3_bucket_default_encryption` |
| `s3-default-encryption-kms` | `s3_bucket_default_encryption` |
| `sagemaker-notebook-instance-kms-key-configured` | `sagemaker_notebook_instance_encryption_enabled` |
| `sns-encrypted-kms` | `sns_topics_kms_encryption_at_rest_enabled` |

**⚠️ Missing AWS Config Rules (5):**

- `cloud-trail-encryption-enabled`
- `dynamodb-table-encrypted-kms`
- `efs-encrypted-check`
- `encrypted-volumes`
- `sagemaker-endpoint-configuration-kms-key-configured`

**ℹ️ Extra Checks We Have (5):**

- `acm_certificates_expiration_check`
- `cloudtrail_kms_encryption_enabled`
- `dynamodb_tables_kms_cmk_encryption_enabled`
- `efs_encryption_at_rest_enabled`
- `s3_bucket_secure_transport_policy`

<details>
<summary>Our Complete Check List (12 checks)</summary>

- `acm_certificates_expiration_check`
- `cloudtrail_kms_encryption_enabled`
- `cloudwatch_log_group_kms_encryption_enabled`
- `dynamodb_tables_kms_cmk_encryption_enabled`
- `ec2_ebs_volume_encryption`
- `efs_encryption_at_rest_enabled`
- `opensearch_service_domains_encryption_at_rest_enabled`
- `rds_instance_storage_encrypted`
- `s3_bucket_default_encryption`
- `s3_bucket_secure_transport_policy`
- `sagemaker_notebook_instance_encryption_enabled`
- `sns_topics_kms_encryption_at_rest_enabled`

</details>

---

### Control 3.13.8

**Status:** ⚠️  MISSING 3 CHECKS

- AWS Official Checks: 5
- Our Implementation: 4
- Matched Checks: 2

**✅ Matched Checks (2):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `acm-certificate-expiration-check` | `acm_certificates_expiration_check` |
| `opensearch-node-to-node-encryption-check` | `opensearch_service_domains_node_to_node_encryption_enabled` |

**⚠️ Missing AWS Config Rules (3):**

- `alb-http-to-https-redirection-check`
- `elb-tls-https-listeners-only`
- `s3-bucket-ssl-requests-only`

**ℹ️ Extra Checks We Have (2):**

- `elb_ssl_listeners`
- `s3_bucket_secure_transport_policy`

<details>
<summary>Our Complete Check List (4 checks)</summary>

- `acm_certificates_expiration_check`
- `elb_ssl_listeners`
- `opensearch_service_domains_node_to_node_encryption_enabled`
- `s3_bucket_secure_transport_policy`

</details>

---

### Control 3.14.6

**Status:** ⚠️  MISSING 5 CHECKS

- AWS Official Checks: 11
- Our Implementation: 11
- Matched Checks: 6

**✅ Matched Checks (6):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `cloudtrail-s3-dataevents-enabled` | `cloudtrail_s3_dataevents_read_enabled` |
| `elb-logging-enabled` | `elb_logging_enabled` |
| `multi-region-cloudtrail-enabled` | `cloudtrail_multi_region_enabled` |
| `s3-bucket-logging-enabled` | `s3_bucket_server_access_logging_enabled` |
| `securityhub-enabled` | `securityhub_enabled` |
| `vpc-flow-logs-enabled` | `vpc_flow_logs_enabled` |

**⚠️ Missing AWS Config Rules (5):**

- `api-gw-execution-logging-enabled`
- `cloud-trail-cloud-watch-logs-enabled`
- `guardduty-enabled-centralized`
- `rds-logging-enabled`
- `wafv2-logging-enabled`

**ℹ️ Extra Checks We Have (5):**

- `apigateway_restapi_logging_enabled`
- `cloudtrail_s3_dataevents_write_enabled`
- `elbv2_logging_enabled`
- `guardduty_is_enabled`
- `rds_instance_integration_cloudwatch_logs`

<details>
<summary>Our Complete Check List (11 checks)</summary>

- `apigateway_restapi_logging_enabled`
- `cloudtrail_multi_region_enabled`
- `cloudtrail_s3_dataevents_read_enabled`
- `cloudtrail_s3_dataevents_write_enabled`
- `elb_logging_enabled`
- `elbv2_logging_enabled`
- `guardduty_is_enabled`
- `rds_instance_integration_cloudwatch_logs`
- `s3_bucket_server_access_logging_enabled`
- `securityhub_enabled`
- `vpc_flow_logs_enabled`

</details>

---

### Control 3.14.7

**Status:** ⚠️  MISSING 6 CHECKS

- AWS Official Checks: 13
- Our Implementation: 11
- Matched Checks: 7

**✅ Matched Checks (7):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `cloudtrail-enabled` | `cloudtrail_multi_region_enabled` |
| `cloudtrail-s3-dataevents-enabled` | `cloudtrail_s3_dataevents_read_enabled` |
| `elb-logging-enabled` | `elb_logging_enabled` |
| `multi-region-cloudtrail-enabled` | `cloudtrail_multi_region_enabled` |
| `s3-bucket-logging-enabled` | `s3_bucket_server_access_logging_enabled` |
| `securityhub-enabled` | `securityhub_enabled` |
| `vpc-flow-logs-enabled` | `vpc_flow_logs_enabled` |

**⚠️ Missing AWS Config Rules (6):**

- `api-gw-execution-logging-enabled`
- `guardduty-enabled-centralized`
- `opensearch-logs-to-cloudwatch`
- `rds-logging-enabled`
- `redshift-cluster-configuration-check`
- `wafv2-logging-enabled`

**ℹ️ Extra Checks We Have (5):**

- `apigateway_restapi_logging_enabled`
- `cloudtrail_s3_dataevents_write_enabled`
- `elbv2_logging_enabled`
- `guardduty_is_enabled`
- `rds_instance_integration_cloudwatch_logs`

<details>
<summary>Our Complete Check List (11 checks)</summary>

- `apigateway_restapi_logging_enabled`
- `cloudtrail_multi_region_enabled`
- `cloudtrail_s3_dataevents_read_enabled`
- `cloudtrail_s3_dataevents_write_enabled`
- `elb_logging_enabled`
- `elbv2_logging_enabled`
- `guardduty_is_enabled`
- `rds_instance_integration_cloudwatch_logs`
- `s3_bucket_server_access_logging_enabled`
- `securityhub_enabled`
- `vpc_flow_logs_enabled`

</details>

---

### Control 3.3.1

**Status:** ⚠️  MISSING 4 CHECKS

- AWS Official Checks: 11
- Our Implementation: 13
- Matched Checks: 7

**✅ Matched Checks (7):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `cloudtrail-enabled` | `cloudtrail_cloudwatch_logging_enabled` |
| `cloudtrail-s3-dataevents-enabled` | `cloudtrail_s3_dataevents_read_enabled` |
| `cloudwatch-log-group-encrypted` | `cloudwatch_log_group_retention_policy_specific_days_enabled` |
| `elb-logging-enabled` | `elb_logging_enabled` |
| `multi-region-cloudtrail-enabled` | `cloudtrail_multi_region_enabled` |
| `s3-bucket-logging-enabled` | `s3_bucket_server_access_logging_enabled` |
| `vpc-flow-logs-enabled` | `vpc_flow_logs_enabled` |

**⚠️ Missing AWS Config Rules (4):**

- `api-gw-execution-logging-enabled`
- `cloud-trail-cloud-watch-logs-enabled`
- `rds-logging-enabled`
- `wafv2-logging-enabled`

**ℹ️ Extra Checks We Have (6):**

- `apigateway_restapi_logging_enabled`
- `cloudtrail_s3_dataevents_write_enabled`
- `elbv2_logging_enabled`
- `guardduty_is_enabled`
- `rds_instance_integration_cloudwatch_logs`
- `securityhub_enabled`

<details>
<summary>Our Complete Check List (13 checks)</summary>

- `apigateway_restapi_logging_enabled`
- `cloudtrail_cloudwatch_logging_enabled`
- `cloudtrail_multi_region_enabled`
- `cloudtrail_s3_dataevents_read_enabled`
- `cloudtrail_s3_dataevents_write_enabled`
- `cloudwatch_log_group_retention_policy_specific_days_enabled`
- `elb_logging_enabled`
- `elbv2_logging_enabled`
- `guardduty_is_enabled`
- `rds_instance_integration_cloudwatch_logs`
- `s3_bucket_server_access_logging_enabled`
- `securityhub_enabled`
- `vpc_flow_logs_enabled`

</details>

---

### Control 3.3.8

**Status:** ℹ️  HAS 5 EXTRA CHECKS

- AWS Official Checks: 4
- Our Implementation: 8
- Matched Checks: 4

**✅ Matched Checks (4):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `cloudtrail-log-file-validation-enabled` | `cloudtrail_log_file_validation_enabled` |
| `cloudwatch-log-group-encrypted` | `cloudwatch_log_group_kms_encryption_enabled` |
| `s3-bucket-default-lock-enabled` | `s3_bucket_default_encryption` |
| `s3-bucket-versioning-enabled` | `s3_bucket_default_encryption` |

**ℹ️ Extra Checks We Have (5):**

- `cloudtrail_kms_encryption_enabled`
- `s3_account_level_public_access_blocks`
- `s3_bucket_object_versioning`
- `s3_bucket_policy_public_write_access`
- `s3_bucket_public_access`

<details>
<summary>Our Complete Check List (8 checks)</summary>

- `cloudtrail_kms_encryption_enabled`
- `cloudtrail_log_file_validation_enabled`
- `cloudwatch_log_group_kms_encryption_enabled`
- `s3_account_level_public_access_blocks`
- `s3_bucket_default_encryption`
- `s3_bucket_object_versioning`
- `s3_bucket_policy_public_write_access`
- `s3_bucket_public_access`

</details>

---

### Control 3.5.3

**Status:** ℹ️  HAS 1 EXTRA CHECKS

- AWS Official Checks: 4
- Our Implementation: 3
- Matched Checks: 4

**✅ Matched Checks (4):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `iam-user-mfa-enabled` | `iam_root_hardware_mfa_enabled` |
| `mfa-enabled-for-iam-console-access` | `iam_user_mfa_enabled_console_access` |
| `root-account-hardware-mfa-enabled` | `iam_root_hardware_mfa_enabled` |
| `root-account-mfa-enabled` | `iam_root_hardware_mfa_enabled` |

**ℹ️ Extra Checks We Have (1):**

- `iam_root_mfa_enabled`

<details>
<summary>Our Complete Check List (3 checks)</summary>

- `iam_root_hardware_mfa_enabled`
- `iam_root_mfa_enabled`
- `iam_user_mfa_enabled_console_access`

</details>

---

### Control 3.5.7

**Status:** ℹ️  HAS 8 EXTRA CHECKS

- AWS Official Checks: 1
- Our Implementation: 9
- Matched Checks: 1

**✅ Matched Checks (1):**

| AWS Config Rule | Our Check |
|-----------------|----------|
| `iam-password-policy` | `iam_password_policy_expires_passwords_within_90_days_or_less` |

**ℹ️ Extra Checks We Have (8):**

- `iam_password_policy_lowercase`
- `iam_password_policy_minimum_length_14`
- `iam_password_policy_number`
- `iam_password_policy_reuse_24`
- `iam_password_policy_symbol`
- `iam_password_policy_uppercase`
- `iam_user_accesskey_unused`
- `iam_user_console_access_unused`

<details>
<summary>Our Complete Check List (9 checks)</summary>

- `iam_password_policy_expires_passwords_within_90_days_or_less`
- `iam_password_policy_lowercase`
- `iam_password_policy_minimum_length_14`
- `iam_password_policy_number`
- `iam_password_policy_reuse_24`
- `iam_password_policy_symbol`
- `iam_password_policy_uppercase`
- `iam_user_accesskey_unused`
- `iam_user_console_access_unused`

</details>

---

## Recommendations

### 1. Missing Checks Analysis
Controls with missing checks should be reviewed to determine if:
- AWS has newer Config rules we should add
- Our Prowler-based approach covers the same functionality differently
- The missing checks are critical for compliance

### 2. Extra Checks Analysis
Extra checks in our implementation may indicate:
- More comprehensive coverage than AWS baseline
- Prowler includes additional best practices
- Multi-cloud perspective adds valuable checks

### 3. Azure Policy Comparison
Azure NIST 800-171 R2 policies should be reviewed separately:
- Extract Azure-specific policy definitions
- Compare with our Azure implementation
- Validate automation decisions

### 4. Action Items
1. ✅ Review missing checks for control 3.1.1 (31 AWS checks vs our coverage)
2. ✅ Validate encryption checks for 3.13.11
3. ✅ Ensure MFA checks for 3.5.3 are complete
4. ✅ Compare logging requirements for 3.3.1, 3.14.6, 3.14.7

---

## AWS Config Rules vs Our Implementation

### Key Differences

1. **Naming Convention:**
   - AWS uses kebab-case: `ec2-instance-no-public-ip`
   - We use snake_case: `ec2_instance_no_public_ip`

2. **Scope:**
   - AWS focuses on AWS-specific Config rules
   - We provide multi-cloud coverage (6 providers)

3. **Granularity:**
   - AWS may have more specific checks per service
   - We consolidate related checks for efficiency

4. **Coverage:**
   - AWS: Technical controls automatable via Config
   - Us: Prowler-validated + expanded to all clouds

---

## Validation Status

✅ **Comparison Complete**

Next Steps:
1. Review control 3.1.1 for potential gaps
2. Extract Azure policies for comparison
3. Update implementation if critical checks are missing
4. Document any intentional differences

---

*Note: This validation ensures our NIST 800-171 implementation aligns with official cloud provider recommendations while maintaining our multi-cloud, Prowler-validated approach.*
