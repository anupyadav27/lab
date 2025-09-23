# AWS Service Compliance Prompt Template

## SERVICE: cloudwatch
**Functions Count**: 68

---

## INPUT DATA FOR THIS SERVICE

```json
{
  "services": {
    "cloudwatch": {
      "check_functions": [
        "cloudwatch_alarm_actions_alarm_state_configured",
        "cloudwatch_alarm_actions_enabled",
        "cloudwatch_changes_to_network_acls_alarm_configured",
        "cloudwatch_changes_to_network_gateways_alarm_configured",
        "cloudwatch_changes_to_network_route_tables_alarm_configured",
        "cloudwatch_changes_to_vpcs_alarm_configured",
        "cloudwatch_cross_account_sharing_disabled",
        "cloudwatch_log_group_kms_encryption_enabled",
        "cloudwatch_log_group_no_secrets_in_logs",
        "cloudwatch_log_group_not_publicly_accessible",
        "cloudwatch_log_group_retention_policy_specific_days_enabled",
        "cloudwatch_log_metric_filter_and_alarm_for_aws_config_configuration_changes_enabled",
        "cloudwatch_log_metric_filter_and_alarm_for_cloudtrail_configuration_changes_enabled",
        "cloudwatch_log_metric_filter_authentication_failures",
        "cloudwatch_log_metric_filter_aws_organizations_changes",
        "cloudwatch_log_metric_filter_disable_or_scheduled_deletion_of_kms_cmk",
        "cloudwatch_log_metric_filter_for_s3_bucket_policy_changes",
        "cloudwatch_log_metric_filter_policy_changes",
        "cloudwatch_log_metric_filter_root_usage",
        "cloudwatch_log_metric_filter_security_group_changes",
        "cloudwatch_log_metric_filter_sign_in_without_mfa",
        "cloudwatch_log_metric_filter_unauthorized_api_calls",
        "cloudwatch_alarm_for_root_account_usage",
        "iam_policy_change_cloudwatch_alarm_enabled",
        "cloudwatch_security_group_changes_alarm_configured",
        "cloudwatch_vpc_changes_metric_filter_and_alarm",
        "cloudwatch_alarm_for_aws_organizations_changes",
        "cloudwatch_log_group_all_services_logging_enabled",
        "cloudwatch_alarm_all_services_alarm_configured",
        "memorydb_cluster_alerting_enabled",
        "cloudwatch_timestream_metrics_monitoring_enabled",
        "cloudwatch_timestream_events_monitoring_enabled",
        "cloudwatch_timestream_logs_monitoring_enabled",
        "qldb_monitor_logs_for_suspicious_activity",
        "qldb_monitor_logs_for_errors",
        "cloudwatch_alarm_for_unusual_events",
        "cloudwatch_alarm_for_resource_threshold",
        "cloudwatch_alarm_for_qldb",
        "cloudwatch_ec2_ebs_alarm_configuration_check",
        "cloudwatch_ec2_ebs_activity_monitoring_check",
        "edr_alerts_check",
        "edr_incident_reports_check",
        "cloudwatch_edr_metrics_monitoring_enabled",
        "cloudwatch_edr_metrics_anomaly_detection",
        "edr_alerts_and_reports_check",
        "cloudwatch_edr_metrics_detailed_logging_enabled",
        "cloudwatch_edr_metrics_regular_review",
        "cloudwatch_log_group_storage_capacity_check",
        "cloudwatch_alarm_for_audit_logging_failures",
        "cloudwatch_continuous_monitoring_strategy_check",
        "cloudwatch_log_pan_masking_check",
        "cloudwatch_log_group_physical_access_monitoring_enabled",
        "cloudwatch_log_group_integrity_check",
        "cloudwatch_log_group_daily_review_check",
        "cloudwatch_log_automation_check",
        "cloudwatch_log_group_periodic_review_check",
        "cloudwatch_log_group_review_frequency_check",
        "cloudwatch_log_group_anomaly_detection_enabled",
        "cloudwatch_log_group_immediate_availability_check",
        "cloudwatch_log_metric_filter_time_changes",
        "cloudwatch_alarm_for_security_control_failures",
        "cloudwatch_alarm_for_critical_security_control_failures",
        "cloudwatch_alarm_for_security_failure_response",
        "cloudwatch_intrusion_detection_alerts_configured",
        "cloudwatch_malware_communication_detection_configured",
        "cloudwatch_file_integrity_monitoring_configured",
        "cloudwatch_log_review_frequency_check",
        "cloudwatch_incident_response_plan_update_check",
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
    "description": "cloudwatch - Compliance Functions Mapping - OPTIMIZED VERSION",
    "total_services": 1,
    "total_check_functions": 68,
    "total_unique_functions": 68,
    "total_duplicates_removed": 0,
    "generated_from": "cloudwatch compliance functions",
    "last_updated": "[TIMESTAMP]",
    "optimization_notes": "Intelligently categorized functions by cloud security expert analysis, grouped by service, simplified to 4 clear categories with execution types and remediation effort classification"
  },
  "services": {
    "cloudwatch": {
      "service_name": "cloudwatch",
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
      "check_count": 68,
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
