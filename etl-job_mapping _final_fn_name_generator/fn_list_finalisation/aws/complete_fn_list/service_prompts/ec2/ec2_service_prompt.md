# AWS Service Compliance Prompt Template

## SERVICE: ec2
**Functions Count**: 295

---

## INPUT DATA FOR THIS SERVICE

```json
{
  "services": {
    "ec2": {
      "check_functions": [
        "ec2_ami_public",
        "ec2_client_vpn_endpoint_connection_logging_enabled",
        "ec2_ebs_default_encryption",
        "ec2_ebs_public_snapshot",
        "ec2_ebs_snapshot_account_block_public_access",
        "ec2_ebs_snapshots_encrypted",
        "ec2_ebs_volume_encryption",
        "ec2_ebs_volume_protected_by_backup_plan",
        "ec2_ebs_volume_snapshots_exists",
        "ec2_elastic_ip_shodan",
        "ec2_elastic_ip_unassigned",
        "ec2_instance_account_imdsv2_enabled",
        "ec2_instance_detailed_monitoring_enabled",
        "ec2_instance_imdsv2_enabled",
        "ec2_instance_internet_facing_with_instance_profile",
        "ec2_instance_managed_by_ssm",
        "ec2_instance_older_than_specific_days",
        "ec2_instance_paravirtual_type",
        "ec2_instance_port_cassandra_exposed_to_internet",
        "ec2_instance_port_cifs_exposed_to_internet",
        "ec2_instance_port_elasticsearch_kibana_exposed_to_internet",
        "ec2_instance_port_ftp_exposed_to_internet",
        "ec2_instance_port_kafka_exposed_to_internet",
        "ec2_instance_port_kerberos_exposed_to_internet",
        "ec2_instance_port_ldap_exposed_to_internet",
        "ec2_instance_port_memcached_exposed_to_internet",
        "ec2_instance_port_mongodb_exposed_to_internet",
        "ec2_instance_port_mysql_exposed_to_internet",
        "ec2_instance_port_oracle_exposed_to_internet",
        "ec2_instance_port_postgresql_exposed_to_internet",
        "ec2_instance_port_rdp_exposed_to_internet",
        "ec2_instance_port_redis_exposed_to_internet",
        "ec2_instance_port_sqlserver_exposed_to_internet",
        "ec2_instance_port_ssh_exposed_to_internet",
        "ec2_instance_port_telnet_exposed_to_internet",
        "ec2_instance_profile_attached",
        "ec2_instance_public_ip",
        "ec2_instance_secrets_user_data",
        "ec2_instance_uses_single_eni",
        "ec2_launch_template_imdsv2_required",
        "ec2_launch_template_no_public_ip",
        "ec2_launch_template_no_secrets",
        "ec2_networkacl_allow_ingress_any_port",
        "ec2_networkacl_allow_ingress_tcp_port_22",
        "ec2_networkacl_allow_ingress_tcp_port_3389",
        "ec2_networkacl_unused",
        "ec2_securitygroup_allow_ingress_from_internet_to_all_ports",
        "ec2_securitygroup_allow_ingress_from_internet_to_any_port",
        "ec2_securitygroup_allow_ingress_from_internet_to_high_risk_tcp_ports",
        "ec2_securitygroup_allow_ingress_from_internet_to_port_mongodb_27017_27018",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_ftp_port_20_21",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_3389",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_cassandra_7199_9160_8888",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_elasticsearch_kibana_9200_9300_5601",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_kafka_9092",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_memcached_11211",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_mongodb_27017_27018",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_mysql_3306",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_oracle_1521_2483",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_postgres_5432",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_redis_6379",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_sql_server_1433_1434",
        "ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_telnet_23",
        "ec2_securitygroup_allow_wide_open_public_ipv4",
        "ec2_securitygroup_default_restrict_traffic",
        "ec2_securitygroup_from_launch_wizard",
        "ec2_securitygroup_not_used",
        "ec2_securitygroup_with_many_ingress_egress_rules",
        "ec2_transitgateway_auto_accept_vpc_attachments",
        "ec2_ami_naming_convention_check",
        "ec2_ami_encryption_check",
        "ec2_ami_approved_check",
        "ec2_ami_older_than_90_days",
        "ec2_ebs_unused_volumes_check",
        "ec2_organizational_tag_policy_created",
        "ec2_instance_custom_security_group_assigned",
        "ec2_unused_enis_removed",
        "ec2_instance_stopped_for_over_90_days",
        "ec2_ebs_volume_deletion_on_termination",
        "ec2_autoscaling_group_propagate_tags_check",
        "apprunner_source_code_vpc_endpoints_check",
        "ec2_instance_iam_role_check",
        "vpc_flow_logs_enabled",
        "ec2_securitygroup_cifs_access_restricted_to_trusted_networks",
        "ec2_networkacl_allow_ingress_all_protocols",
        "ec2_securitygroup_no_ingress_from_ipv6_all_to_tcp_port_22",
        "ec2_securitygroup_no_ingress_from_ipv6_all_to_tcp_port_3389",
        "ec2_default_security_group_no_inbound_rules",
        "ec2_default_security_group_no_outbound_rules",
        "ec2_vpc_peering_route_table_least_access_check",
        "ec2_vpc_exists_check",
        "ec2_instance_multi_az_deployment_check",
        "ec2_vpc_exists_check",
        "ec2_securitygroup_configure_check",
        "ec2_instance_security_configuration_review",
        "vpc_endpoints_configured_check",
        "security_group_unused_check",
        "documentdb_instance_network_acl_configuration_check",
        "vpc_security_group_inbound_outbound_traffic_check",
        "vpc_subnet_configuration_check",
        "ec2_instance_in_transit_encryption_enabled",
        "ec2_vpc_security_group_rules_check",
        "ec2_vpc_network_acl_rules_check",
        "ec2_instance_data_in_transit_encryption_check",
        "security_group_regular_review",
        "vpc_network_access_logging_enabled",
        "vpc_network_acl_specific_access",
        "ec2_instance_snapshot_exists",
        "vpc_exists_check",
        "rds_security_group_inbound_outbound_rules_check",
        "ec2_deployment_configuration_check",
        "vpc_exists_check",
        "ec2_securitygroup_egress_rules_check",
        "ec2_securitygroup_ingress_rules_check",
        "ec2_instance_latest_patch_version_check",
        "ec2_network_security_group_default_rules_check",
        "ec2_network_acl_default_rules_check",
        "security_networks_regular_review",
        "documentdb_instance_vpc_security_group_inbound_outbound_traffic_check",
        "vpc_security_group_configuration_check",
        "ebs_snapshot_encryption_enabled",
        "vpc_security_group_rules_check",
        "vpc_network_acl_rules_check",
        "vpc_flow_logs_enabled_check",
        "ec2_instance_audit_logging_enabled",
        "security_networks_regular_review",
        "vpc_network_acl_check",
        "vpc_security_group_check",
        "vpc_flow_logs_check",
        "workspaces_traffic_routed_through_nat_gateway",
        "ec2_instance_trusted_device_access_check",
        "ec2_default_ip_access_control_group_disassociated",
        "workspaces_api_requests_vpc_endpoint_check",
        "appstream_vpc_endpoint_check",
        "ec2_instance_session_disconnect_timeout",
        "ec2_instance_session_idle_disconnect_timeout",
        "vpc_internet_gateway_check",
        "vpc_nat_gateway_check",
        "vpc_route_table_internet_access_check",
        "ec2_ami_os_updates_check",
        "ec2_instance_backup_enabled",
        "ec2_instance_with_ebs_check",
        "ec2_security_group_inbound_rules_check",
        "ec2_security_group_outbound_rules_check",
        "ec2_ebs_volume_creation_check",
        "ec2_ebs_volume_encryption_kms_key_check",
        "ec2_ebs_snapshot_creation_check",
        "ec2_resource_tag_based_access_check",
        "efs_security_group_check",
        "efs_network_acl_check",
        "ec2_security_group_associated_with_vpc",
        "ec2_security_group_rules_check",
        "ebs_secure_ports_check",
        "efs_vpc_endpoints_check",
        "fsx_compatible_os_check",
        "ec2_instance_lustre_client_installed",
        "ec2_instance_lustre_client_configured",
        "ec2_ami_kernel_compatibility_check",
        "ec2_ami_kernel_downgrade_prerequisites_check",
        "aws_edr_replication_agent_check",
        "aws_edr_api_endpoints_check",
        "aws_edr_subnet_check",
        "aws_edr_tcp_port_check",
        "ec2_launch_settings_security_configuration_check",
        "ec2_launch_settings_resource_specification_check",
        "ec2_launch_settings_startup_parameters_check",
        "elastic_recovery_instance_drill_execution_check",
        "disaster_recovery_failover_execution_check",
        "disaster_recovery_data_replication_check",
        "ec2_failback_execution_check",
        "ec2_ebs_snapshot_frequency_check",
        "ec2_ebs_snapshot_retention_period_check",
        "ec2_iam_role_configuration_check",
        "efs_network_acl_configuration_check",
        "ec2_security_group_association_check",
        "efs_mount_target_security_group_rules_review",
        "edr_replication_agent_connection_check",
        "edr_staging_area_connectivity_check",
        "edr_ec2_api_endpoint_connectivity_check",
        "ec2_launch_settings_regular_review",
        "aws_elastic_recovery_instance_drill_execution_check",
        "disaster_recovery_failback_execution_check",
        "ec2_instance_role_least_privilege_check",
        "ec2_instance_user_data_banner_check",
        "ec2_instance_idle_session_termination",
        "ec2_vpn_connection_encryption_enabled",
        "ec2_vpn_connection_authorization_check",
        "ec2_wireless_access_configuration_check",
        "ec2_wireless_access_authorization_check",
        "ec2_mobile_device_configuration_check",
        "ec2_mobile_device_authorization_check",
        "ec2_external_system_access_check",
        "ec2_external_system_prohibition_check",
        "ec2_security_group_open_ports_check",
        "ec2_instance_security_group_configuration_check",
        "ec2_instance_unused_ports_check",
        "ec2_instance_inventory_check",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "ec2_security_group_no_public_access",
        "new_function_name_1",
        "vpc_security_group_ruleset_configuration_check",
        "vpc_network_configuration_change_tracking",
        "vpc_network_diagram_accuracy_check",
        "ec2_security_group_approved_ports_check",
        "ec2_security_group_insecure_protocols_check",
        "ec2_security_group_configuration_review",
        "ec2_security_group_configuration_file_integrity_check",
        "ec2_instance_configuration_compliance_check",
        "ec2_instance_default_account_check",
        "ec2_instance_function_isolation_check",
        "ec2_instance_unnecessary_services_disabled_check",
        "ec2_instance_insecure_protocols_disabled",
        "ec2_instance_security_parameters_configured",
        "ec2_instance_non_console_access_encrypted",
        "ec2_instance_default_security_settings_changed",
        "ec2_instance_wireless_encryption_key_rotation",
        "ec2_instance_remote_access_copy_restriction",
        "ec2_disk_level_encryption_check",
        "ec2_disk_encryption_access_control_check",
        "ec2_instance_secure_protocols_enabled",
        "ec2_vpc_wireless_network_security_check",
        "ec2_instance_antivirus_installed",
        "ec2_instance_antimalware_logging_enabled",
        "ec2_instance_antimalware_protection_immutable",
        "ec2_instance_cde_tag_check",
        "ec2_instance_test_data_check",
        "ec2_instance_idle_timeout_check",
        "ec2_security_group_physical_access_control_check",
        "ec2_ebs_volume_secure_deletion_check",
        "ec2_instance_time_synchronization_check",
        "ec2_instance_ntp_configuration_check",
        "ec2_describe_network_interfaces",
        "ec2_list_authorized_wireless_access_points",
        "ec2_vulnerability_scan_results_check",
        "ec2_instance_vulnerability_scan_results_check",
        "ec2_instance_authenticated_scan_configuration_check",
        "ec2_instance_post_change_vulnerability_scan_check",
        "ec2_external_vulnerability_scan_schedule_check",
        "ec2_post_change_external_vulnerability_scan_check",
        "ec2_instance_vulnerability_scan_results_check",
        "ec2_internal_penetration_test_results_check",
        "ec2_external_penetration_test_results_check",
        "ec2_vulnerability_remediation_check",
        "ec2_instance_external_penetration_test_support_check",
        "ec2_instance_ami_latest_version_check",
        "ec2_network_acl_intrusion_detection_enabled",
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
    "description": "ec2 - Compliance Functions Mapping - OPTIMIZED VERSION",
    "total_services": 1,
    "total_check_functions": 295,
    "total_unique_functions": 295,
    "total_duplicates_removed": 0,
    "generated_from": "ec2 compliance functions",
    "last_updated": "[TIMESTAMP]",
    "optimization_notes": "Intelligently categorized functions by cloud security expert analysis, grouped by service, simplified to 4 clear categories with execution types and remediation effort classification"
  },
  "services": {
    "ec2": {
      "service_name": "ec2",
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
      "check_count": 295,
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
