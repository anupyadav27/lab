# AWS Service Compliance Prompt Template

## SERVICE: s3
**Functions Count**: 70

---

## INPUT DATA FOR THIS SERVICE

```json
{
  "services": {
    "s3": {
      "check_functions": [
        "s3_access_point_public_access_block",
        "s3_account_level_public_access_blocks",
        "s3_bucket_acl_prohibited",
        "s3_bucket_cross_account_access",
        "s3_bucket_cross_region_replication",
        "s3_bucket_default_encryption",
        "s3_bucket_event_notifications_enabled",
        "s3_bucket_kms_encryption",
        "s3_bucket_level_public_access_block",
        "s3_bucket_lifecycle_enabled",
        "s3_bucket_no_mfa_delete",
        "s3_bucket_object_lock",
        "s3_bucket_object_versioning",
        "s3_bucket_policy_public_write_access",
        "s3_bucket_public_access",
        "s3_bucket_public_list_acl",
        "s3_bucket_public_write_acl",
        "s3_bucket_secure_transport_policy",
        "s3_bucket_server_access_logging_enabled",
        "s3_multi_region_access_point_public_access_block",
        "s3_bucket_policy_deny_http_requests",
        "s3_bucket_data_discovery",
        "s3_bucket_data_security",
        "s3_bucket_block_public_access_enabled",
        "s3_account_block_public_access_enabled",
        "s3_bucket_encryption_at_rest_enabled",
        "s3_bucket_encryption_enabled",
        "s3_bucket_in_transit_encryption_enabled",
        "s3_bucket_encryption_enabled",
        "s3_bucket_in_transit_encryption_enabled",
        "s3_audit_logging_enabled",
        "s3_bucket_encryption_enabled",
        "s3_bucket_data_in_transit_encryption_check",
        "s3_bucket_encryption_enabled",
        "s3_bucket_encryption_enabled",
        "s3_bucket_versioning_enabled",
        "s3_data_in_transit_encryption_check",
        "s3_bucket_security_configuration_review",
        "s3_bucket_audit_logging_enabled",
        "s3_bucket_backup_enabled",
        "s3_bucket_policy_granularity_check",
        "s3_bucket_secure_ports_check",
        "s3_bucket_exists_for_fsx",
        "s3_bucket_cache_export_check",
        "s3_bucket_public_access_block",
        "s3_bucket_access_logging_enabled",
        "s3_bucket_lifecycle_configuration_check",
        "s3_bucket_unique_check",
        "s3_bucket_direct_upload_check",
        "s3_bucket_storage_class_configured",
        "disaster_recovery_failover_test_documentation_check",
        "s3_failback_execution_check",
        "s3_secure_ports_check",
        "s3_bucket_logging_enabled",
        "edr_s3_connectivity_check",
        "disaster_recovery_failback_data_integrity_check",
        "s3_object_metadata_security_attributes_check",
        "s3_bucket_sharing_authorization_check",
        "s3_bucket_sharing_mechanism_check",
        "s3_bucket_public_access_check",
        "s3_bucket_inventory_check",
        "s3_bucket_data_retention_policy_check",
        "s3_bucket_no_card_verification_code_storage",
        "s3_bucket_no_pin_storage",
        "s3_bucket_sad_encryption_check",
        "s3_bucket_sad_storage_check",
        "s3_bucket_cardholder_data_inventory_check",
        "s3_bucket_lifecycle_policy_for_log_backup",
        "s3_bucket_change_detection_enabled",
        "s3_bucket_pan_detection_enabled",
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
    "description": "s3 - Compliance Functions Mapping - OPTIMIZED VERSION",
    "total_services": 1,
    "total_check_functions": 70,
    "total_unique_functions": 70,
    "total_duplicates_removed": 0,
    "generated_from": "s3 compliance functions",
    "last_updated": "[TIMESTAMP]",
    "optimization_notes": "Intelligently categorized functions by cloud security expert analysis, grouped by service, simplified to 4 clear categories with execution types and remediation effort classification"
  },
  "services": {
    "s3": {
      "service_name": "s3",
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
      "check_count": 70,
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
