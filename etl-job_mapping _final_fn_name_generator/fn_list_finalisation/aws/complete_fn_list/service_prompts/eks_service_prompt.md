# AWS Service Compliance Prompt Template

## SERVICE: eks
**Functions Count**: 59

---

## INPUT DATA FOR THIS SERVICE

```json
{
  "services": {
    "eks": {
      "check_functions": [
        "eks_cluster_kms_cmk_encryption_in_secrets_enabled",
        "eks_cluster_network_policy_enabled",
        "eks_cluster_not_publicly_accessible",
        "eks_cluster_private_nodes_enabled",
        "eks_cluster_uses_a_supported_version",
        "eks_control_plane_logging_all_types_enabled",
        "eks_control_plane_logs_exported",
        "eks_kubeconfig_file_permissions_check",
        "eks_kubelet_kubeconfig_file_ownership_check",
        "eks_kubelet_config_file_permission_check",
        "eks_kubelet_config_file_ownership_check",
        "kubelet_server_anonymous_auth_disabled",
        "kubernetes_cluster_authorization_mode_check",
        "eks_cluster_client_ca_file_configured",
        "kubelet_make_iptables_util_chains_check",
        "kubelet_config_event_record_qps_check",
        "eks_cluster_rotate_certificates_check",
        "eks_cluster_rotate_kubelet_server_certificate_enabled",
        "eks_secrets_access_restriction",
        "kubernetes_clusterrole_minimize_wildcard_use",
        "eks_namespace_minimize_pod_creation_access",
        "eks_pod_security_policy_enforcement",
        "kubernetes_pod_service_account_token_mount_check",
        "eks_cluster_access_manager_api_enabled",
        "eks_cluster_access_manager_api_access_policies_assigned",
        "eks_cluster_access_manager_api_audit",
        "eks_cluster_limit_bind_permission",
        "eks_cluster_limit_impersonate_permission",
        "eks_cluster_limit_escalate_permission",
        "eks_pod_security_policy_no_privileged_containers",
        "eks_cni_plugin_supports_network_policies",
        "kubernetes_namespace_network_policy_defined",
        "kubernetes_secrets_as_files_preferred",
        "eks_namespace_isolation_check",
        "eks_default_namespace_usage_check",
        "eks_service_account_dedicated_check",
        "eks_cluster_secrets_encryption_check",
        "eks_cluster_control_plane_endpoint_private_access",
        "eks_cluster_private_endpoint_enabled",
        "eks_cluster_network_policy_type",
        "eks_cluster_network_policy_ip_tables_rules",
        "eks_cluster_iam_authenticator_enabled",
        "eks_control_plane_logs_exported_to_cloudwatch",
        "eks_api_server_audit_logs_recorded",
        "eks_kubeconfig_file_permission_check",
        "eks_secrets_encryption_check",
        "eks_namespace_pod_creation_access_restriction",
        "eks_pod_security_policies_enforced",
        "eks_pod_service_account_token_mount_check",
        "eks_cluster_access_manager_api_simplified_access_management",
        "eks_cluster_access_manager_api_enhanced_security_controls",
        "eks_cluster_access_manager_api_improved_visibility_and_auditing",
        "eks_cluster_cni_plugin_network_policies_support",
        "eks_namespace_network_policy_check",
        "eks_image_vulnerability_scanning_check",
        "eks_cluster_public_access_disabled",
        "eks_cluster_nodes_private_ip_only",
        "eks_cluster_network_policy_appropriate",
        "eks_rbac_users_managed_with_iam_authenticator",
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
    "description": "eks - Compliance Functions Mapping - OPTIMIZED VERSION",
    "total_services": 1,
    "total_check_functions": 59,
    "total_unique_functions": 59,
    "total_duplicates_removed": 0,
    "generated_from": "eks compliance functions",
    "last_updated": "[TIMESTAMP]",
    "optimization_notes": "Intelligently categorized functions by cloud security expert analysis, grouped by service, simplified to 4 clear categories with execution types and remediation effort classification"
  },
  "services": {
    "eks": {
      "service_name": "eks",
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
      "check_count": 59,
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
