# AWS Service Compliance Prompt Template

## SERVICE: rds
**Functions Count**: 83

---

## INPUT DATA FOR THIS SERVICE

```json
{
  "services": {
    "rds": {
      "check_functions": [
        "rds_cluster_backtrack_enabled",
        "rds_cluster_copy_tags_to_snapshots",
        "rds_cluster_critical_event_subscription",
        "rds_cluster_default_admin",
        "rds_cluster_deletion_protection",
        "rds_cluster_iam_authentication_enabled",
        "rds_cluster_integration_cloudwatch_logs",
        "rds_cluster_minor_version_upgrade_enabled",
        "rds_cluster_multi_az",
        "rds_cluster_non_default_port",
        "rds_cluster_protected_by_backup_plan",
        "rds_cluster_storage_encrypted",
        "rds_instance_backup_enabled",
        "rds_instance_certificate_expiration",
        "rds_instance_copy_tags_to_snapshots",
        "rds_instance_critical_event_subscription",
        "rds_instance_default_admin",
        "rds_instance_deletion_protection",
        "rds_instance_deprecated_engine_version",
        "rds_instance_enhanced_monitoring_enabled",
        "rds_instance_event_subscription_parameter_groups",
        "rds_instance_event_subscription_security_groups",
        "rds_instance_iam_authentication_enabled",
        "rds_instance_inside_vpc",
        "rds_instance_integration_cloudwatch_logs",
        "rds_instance_minor_version_upgrade_enabled",
        "rds_instance_multi_az",
        "rds_instance_no_public_access",
        "rds_instance_non_default_port",
        "rds_instance_protected_by_backup_plan",
        "rds_instance_storage_encrypted",
        "rds_instance_transport_encrypted",
        "rds_snapshots_encrypted",
        "rds_snapshots_public_access",
        "rds_instance_encryption_at_rest_enabled",
        "rds_instance_auto_minor_version_upgrade_enabled",
        "rds_instance_public_access_check",
        "rds_instance_security_group_update_check",
        "rds_multi_az_deployment_check",
        "aurora_instance_storage_encrypted",
        "aurora_instance_ssl_encryption_enabled",
        "rds_database_audit_logging_enabled",
        "aurora_password_rotation_check",
        "aurora_iam_least_privilege_policy_check",
        "aurora_database_user_role_least_privilege_check",
        "rds_aurora_automatic_backups_enabled",
        "rds_aurora_backup_retention_period_configured",
        "rds_database_engine_check",
        "rds_instance_multi_az_deployment_check",
        "rds_instance_ssl_encryption_enabled",
        "rds_instance_security_configuration_review",
        "rds_instance_in_transit_encryption_enabled",
        "rds_instance_encryption_enabled",
        "rds_instance_in_transit_encryption_enabled",
        "rds_audit_logging_enabled",
        "rds_instance_data_in_transit_encryption_check",
        "rds_instance_security_group_assigned",
        "aurora_data_in_transit_encryption_check",
        "aurora_database_audit_logging_enabled",
        "aurora_automatic_backups_enabled",
        "aurora_backup_retention_period_configured",
        "rds_deployment_configuration_check",
        "database_access_control_check",
        "database_authentication_check",
        "rds_instance_latest_patch_version_check",
        "rds_instance_backup_retention_period",
        "rds_instance_audit_logging_enabled",
        "rds_instance_session_disconnect_timeout",
        "rds_instance_session_idle_disconnect_timeout",
        "rds_failback_execution_check",
        "rds_instance_parameter_group_settings_check",
        "rds_instance_inventory_check",
        "rds_instance_insecure_protocols_disabled",
        "rds_instance_security_parameters_configured",
        "rds_instance_sad_storage_check",
        "rds_instance_track_data_storage_check",
        "rds_instance_sad_encryption_check",
        "rds_instance_sad_storage_check",
        "rds_instance_pan_unreadable_check",
        "rds_instance_cde_tag_check",
        "rds_instance_test_accounts_check",
        "rds_user_access_logging_enabled",
        "rds_instance_pan_detection_enabled",
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
    "description": "rds - Compliance Functions Mapping - OPTIMIZED VERSION",
    "total_services": 1,
    "total_check_functions": 83,
    "total_unique_functions": 83,
    "total_duplicates_removed": 0,
    "generated_from": "rds compliance functions",
    "last_updated": "[TIMESTAMP]",
    "optimization_notes": "Intelligently categorized functions by cloud security expert analysis, grouped by service, simplified to 4 clear categories with execution types and remediation effort classification"
  },
  "services": {
    "rds": {
      "service_name": "rds",
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
      "check_count": 83,
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
