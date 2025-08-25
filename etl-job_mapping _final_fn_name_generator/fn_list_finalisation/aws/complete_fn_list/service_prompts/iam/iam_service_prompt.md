# AWS Service Compliance Prompt Template

## SERVICE: iam
**Functions Count**: 178

---

## INPUT DATA FOR THIS SERVICE

```json
{
  "services": {
    "iam": {
      "check_functions": [
        "iam_administrator_access_with_mfa",
        "iam_avoid_root_usage",
        "iam_aws_attached_policy_no_administrative_privileges",
        "iam_check_saml_providers_sts",
        "iam_customer_attached_policy_no_administrative_privileges",
        "iam_customer_unattached_policy_no_administrative_privileges",
        "iam_group_administrator_access_policy",
        "iam_inline_policy_allows_privilege_escalation",
        "iam_inline_policy_no_administrative_privileges",
        "iam_inline_policy_no_full_access_to_cloudtrail",
        "iam_inline_policy_no_full_access_to_kms",
        "iam_no_custom_policy_permissive_role_assumption",
        "iam_no_expired_server_certificates_stored",
        "iam_no_root_access_key",
        "iam_password_policy_expires_passwords_within_90_days_or_less",
        "iam_password_policy_lowercase",
        "iam_password_policy_minimum_length_14",
        "iam_password_policy_number",
        "iam_password_policy_reuse_24",
        "iam_password_policy_symbol",
        "iam_password_policy_uppercase",
        "iam_policy_allows_privilege_escalation",
        "iam_policy_attached_only_to_group_or_roles",
        "iam_policy_cloudshell_admin_not_attached",
        "iam_policy_no_full_access_to_cloudtrail",
        "iam_policy_no_full_access_to_kms",
        "iam_role_administratoraccess_policy",
        "iam_role_cross_account_readonlyaccess_policy",
        "iam_role_cross_service_confused_deputy_prevention",
        "iam_root_credentials_management_enabled",
        "iam_root_hardware_mfa_enabled",
        "iam_root_mfa_enabled",
        "iam_rotate_access_key_90_days",
        "iam_securityaudit_role_created",
        "iam_support_role_created",
        "iam_user_accesskey_unused",
        "iam_user_administrator_access_policy",
        "iam_user_console_access_unused",
        "iam_user_hardware_mfa_enabled",
        "iam_user_mfa_enabled_console_access",
        "iam_user_no_setup_initial_access_key",
        "iam_user_two_active_access_key",
        "iam_user_with_temporary_credentials",
        "iam_role_usage_audit",
        "iam_role_cluster_admin_check",
        "iam_role_minimize_wildcard_use",
        "iam_default_service_accounts_activity_check",
        "batch_roles_cross_service_deputy_prevention",
        "iam_role_cluster_admin_usage_check",
        "ecr_cluster_service_account_read_only_access",
        "iam_root_user_access_key_check",
        "iam_root_account_mfa_enabled",
        "iam_root_account_hardware_mfa_enabled",
        "iam_root_user_activity_check",
        "iam_root_user_mfa_enabled_check",
        "iam_password_policy_prevent_reuse_check",
        "iam_user_console_password_mfa_enabled",
        "iam_user_access_key_creation_check",
        "iam_user_console_password_check",
        "iam_user_credentials_unused_check",
        "iam_user_single_active_access_key_check",
        "iam_access_keys_rotation_check",
        "iam_user_group_only_permissions_check",
        "iam_policy_no_full_admin_privileges",
        "iam_user_no_full_admin_privileges",
        "iam_group_no_full_admin_privileges",
        "iam_role_no_full_admin_privileges",
        "iam_role_exists_for_aws_support",
        "iam_role_policy_for_aws_support",
        "iam_role_permissions_policy_check",
        "iam_ssl_certificate_expiration_check",
        "iam_accessanalyzer_enabled_all_regions",
        "iam_users_managed_centralized_check",
        "iam_policy_check_restricted_access",
        "iam_user_policy_attachment_check",
        "iam_roles_exist",
        "iam_policies_exist",
        "iam_user_access_keys_rotation_check",
        "iam_user_mfa_enabled",
        "root_account_mfa_enabled",
        "iam_user_password_authentication_enabled",
        "iam_user_access_control_policy_attached",
        "iam_user_permissions_review",
        "iam_users_exist",
        "iam_roles_exist",
        "iam_policies_exist",
        "iam_groups_exist",
        "iam_role_acl_check",
        "iam_user_acl_check",
        "iam_user_access_key_rotation_check",
        "iam_password_policy_check",
        "iam_mfa_enabled_check",
        "iam_role_unused_check",
        "neptune_db_cluster_iam_policies_check",
        "iam_role_regular_review",
        "authentication_settings_regular_review",
        "timestream_resource_iam_policy_check",
        "iam_role_authentication_check",
        "iam_role_authorization_check",
        "qldb_iam_policy_check",
        "qldb_cross_service_access_check",
        "iam_roles_and_policies_existence_check",
        "iam_user_least_privilege_policy_check",
        "iam_role_least_privilege_policy_check",
        "iam_mfa_enabled_for_all_users",
        "iam_user_existence_check",
        "iam_policy_existence_check",
        "iam_role_existence_check",
        "iam_user_mfa_enabled_check",
        "iam_role_assume_policy_check",
        "iam_timestream_access_control_check",
        "iam_timestream_authentication_check",
        "timestream_access_permissions_review",
        "iam_user_authentication_check",
        "iam_role_policy_check",
        "workspaces_iam_administration_defined",
        "iam_device_trust_check",
        "iam_user_invitation_domain_check",
        "iam_user_invite_external_users_check",
        "iam_role_maximum_session_duration_check",
        "awsbackup_access_credentials_management_check",
        "awsbackup_user_awareness_check",
        "iam_policy_creation_check",
        "iam_policy_permission_check",
        "iam_policy_condition_check",
        "iam_role_for_backup_exists",
        "awsbackup_service_linked_role_exists",
        "awsbackup_service_linked_role_permissions_check",
        "ec2_instance_iam_policy_least_privilege_check",
        "ec2_instance_iam_mfa_enforced_check",
        "iam_user_creation_check",
        "iam_group_creation_check",
        "iam_policy_granularity_check",
        "iam_policy_tag_based_access_check",
        "iam_account_password_policy_check",
        "efs_iam_policy_check",
        "iam_elastic_disaster_recovery_replication_permissions_check",
        "iam_elastic_disaster_recovery_failback_permissions_check",
        "elastic_disaster_recovery_iam_configuration_check",
        "elastic_disaster_recovery_mfa_enforcement_check",
        "ec2_iam_policy_least_privilege_check",
        "iam_list_groups_check",
        "iam_policy_efs_access_point_check",
        "aws_edr_iam_permissions_check",
        "aws_edr_iam_users_check",
        "aws_edr_iam_least_privilege_policy_check",
        "aws_edr_iam_mfa_enforced_check",
        "aws_edr_iam_role_for_automated_process_check",
        "aws_edr_iam_policy_regular_review_check",
        "iam_user_account_activity_monitoring",
        "iam_user_account_review",
        "iam_policy_access_enforcement_check",
        "iam_role_separation_of_duties_check",
        "iam_user_concurrent_session_limit_check",
        "iam_user_inventory_check",
        "iam_role_pan_display_access_check",
        "iam_access_control_pre_production_check",
        "iam_role_separation_check",
        "iam_access_control_model_check",
        "iam_shared_credentials_usage_check",
        "iam_service_provider_unique_authentication_check",
        "iam_user_lifecycle_management_check",
        "iam_terminated_user_access_revocation_check",
        "iam_inactive_user_account_check",
        "iam_user_access_last_used_check",
        "iam_password_policy_encryption_check",
        "iam_user_identity_verification_before_modification",
        "iam_user_account_lockout_policy_check",
        "iam_user_password_reset_policy_check",
        "iam_user_password_complexity_policy_check",
        "iam_user_password_history_policy_check",
        "iam_user_password_policy_check",
        "iam_user_password_policy_check",
        "iam_user_mfa_device_check",
        "iam_admin_mfa_enforced_check",
        "iam_user_password_policy_check",
        "iam_admin_actions_logging_enabled",
        "iam_invalid_login_attempts_logging_enabled",
      ]
    }
  }
}
```

---

## COMPLIANCE TRANSFORMATION PROMPT

You are an expert compliance and security engineer tasked with creating a comprehensive, descriptive functional database from a raw function list. Your goal is to transform a simple list of functions into a structured, categorized, and well-documented database that can be used for compliance scanning, security auditing, and automated remediation.

## TASK REQUIREMENTS

### 1. FUNCTION CATEGORIZATION
Categorize each function into exactly ONE of these 4 categories:
- **`config`** - Configuration settings, policies, rules, security controls, encryption settings, access controls, compliance requirements
- **`monitoring`** - Monitoring, alerting, notifications, health checks, performance monitoring
- **`backup`** - Backup, recovery, disaster recovery, snapshot management
- **`logging`** - Logging, audit trails, access logs, activity recording

### 2. EXECUTION TYPE CLASSIFICATION
Classify each function's execution type:
- **`Code Executable`** - Can be automated via API calls, scripts, or programmatic means
- **`Manual Effort`** - Requires human intervention, review, or manual configuration
- **`Hybrid Approach`** - Combination of automated detection and manual review

### 3. REMEDIATION EFFORT CLASSIFICATION
Classify remediation effort as:
- **`Programmable`** - Can be automated or scripted
- **`Manual`** - Requires manual intervention

### 4. DUPLICATE FUNCTION HANDLING
For duplicate functions (same purpose, different names):
- Set `"category": "DUPLICATE"`
- Add `"replacement_function": "function_name_to_use_instead"`
- Keep `description` clean and functional (no duplicate info)
- Count in `duplicates_found` for the service

### 5. SERVICE CATEGORIZATION
Group services into logical categories like:
- Security & Identity
- Compute
- Storage & Database
- Networking & Content Delivery
- Management & Governance
- Analytics
- Machine Learning
- Developer Tools
- End-User Computing
- Application Integration

## OUTPUT STRUCTURE

Create a JSON file with this exact structure:

```json
{
  "scan_metadata": {
    "description": "iam - Compliance Functions Mapping - OPTIMIZED VERSION",
    "total_services": 1,
    "total_check_functions": 178,
    "total_unique_functions": 178,
    "total_duplicates_removed": 0,
    "generated_from": "iam compliance functions",
    "last_updated": "[TIMESTAMP]",
    "optimization_notes": "Intelligently categorized functions by cloud security expert analysis, grouped by service, simplified to 4 clear categories with execution types and remediation effort classification"
  },
  "services": {
    "iam": {
      "service_name": "iam",
      "service_category": "[SERVICE_CATEGORY]",
      "check_functions": [
        {
          "function_name": "function_name",
          "category": "config|monitoring|backup|logging|DUPLICATE",
          "execution_type": "Code Executable - <description>|Manual Effort - <description>|Hybrid Approach - <description>",
          "description": "Clear, concise description of what the function does",
          "remediation_effort": "Programmable|Manual",
          "replacement_function": "function_name_to_use" // ONLY for duplicates
        }
      ],
      "check_count": 178,
      "duplicates_found": 0
    }
  },
  "category_summary": {
    "config": 0,
    "monitoring": 0,
    "backup": 0,
    "logging": 0
  },
  "execution_type_summary": {
    "code_executable": 0,
    "manual_effort": 0,
    "hybrid_approach": 0
  },
  "duplicate_analysis": {
    "total_duplicates_found": 0,
    "duplicate_categories": {
      "exact_name_duplicates": 0,
      "functional_duplicates": 0,
      "similar_purpose_duplicates": 0
    },
    "services_with_most_duplicates": []
  }
}
```

## QUALITY REQUIREMENTS

### 1. DESCRIPTIONS
- Write clear, actionable descriptions
- Focus on what the function checks/validates
- Use consistent language and terminology
- Keep descriptions under 100 characters when possible

### 2. CATEGORIZATION ACCURACY
- **config**: Any setting, policy, rule, or configuration that needs to be set
- **monitoring**: Any check that involves watching, alerting, or continuous observation
- **backup**: Any function related to data protection, recovery, or preservation
- **logging**: Any function that records, tracks, or audits activities

### 3. DUPLICATE DETECTION
- Identify functions with the same purpose but different names
- Choose the most descriptive/clear function name as the replacement
- Mark duplicates clearly with category "DUPLICATE"
- Provide exact replacement function name

### 4. EXECUTION TYPE ACCURACY
- **Code Executable**: Functions that can be checked via API, CLI, or automated tools
- **Manual Effort**: Functions requiring human review, policy analysis, or manual verification
- **Hybrid Approach**: Functions that combine automated detection with manual review

## EXAMPLE TRANSFORMATION

**Input Function**: `s3_bucket_public_access_block`

**Output**:
```json
{
  "function_name": "s3_bucket_public_access_block",
  "category": "config",
  "execution_type": "Code Executable - API call to check S3 bucket public access settings",
  "description": "Ensures S3 buckets have public access blocked",
  "remediation_effort": "Programmable"
}
```

## IMPORTANT NOTES

- Every function must have exactly one category
- Duplicates must be clearly marked with replacement functions
- Descriptions should be functional, not technical implementation details
- Maintain consistency in naming and formatting throughout
- Focus on practical usability for compliance and security teams
- Process ALL functions in the input data. Do not skip any.
- Keep the EXACT original function names from the input

Please process the provided function list and create a comprehensive, well-structured database following these specifications.
