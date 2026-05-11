# K8s Function Generation Summary - PCI_DSS
Generated: 2025-11-12 23:26:09

## Statistics
- Total controls processed: 205
- Approved: 0
- Approved with changes: 73
- Rejected: 0
- Not applicable: 132
- Errors: 0
- Total K8s functions generated: 247
- Unique K8s functions: 88

## K8s Functions by Category

### ADMISSION
- k8s_admission_controller_change_management_enforced
- k8s_admission_controller_security_audit_enabled
- k8s_admission_controller_security_enabled
- k8s_admission_deny_sensitive_env_variables

### APISERVER
- k8s_apiserver_audit_logging_enabled
- k8s_apiserver_audit_policy_captures_metadata
- k8s_apiserver_audit_policy_configured
- k8s_apiserver_tls_enabled

### AUDIT
- k8s_audit_change_management_logging_enabled
- k8s_audit_invalid_access_attempts_logged
- k8s_audit_log_access_events_captured
- k8s_audit_log_access_review
- k8s_audit_log_creation_deletion_events_enabled
- k8s_audit_log_integrity_enabled
- k8s_audit_log_invalid_access_attempts_configured
- k8s_audit_log_retention_configured
- k8s_audit_log_retention_period_configured
- k8s_audit_log_retention_policy_configured
- k8s_audit_logging_enabled
- k8s_audit_policy_captures_all_actions
- k8s_audit_policy_captures_auth_changes
- k8s_audit_policy_captures_failed_authentication
- k8s_audit_policy_captures_metadata
- k8s_audit_policy_captures_security_events
- k8s_audit_policy_captures_user_access
- k8s_audit_policy_change_detection_enabled
- k8s_audit_policy_change_events_logged
- k8s_audit_policy_change_logging_enabled
- k8s_audit_policy_metadata_capture_enabled
- k8s_audit_policy_metadata_captured
- k8s_audit_policy_system_level_event_logging
- k8s_audit_user_activity_logging_enabled

### CERTIFICATE
- k8s_certificate_expiration_check

### CLUSTER
- k8s_cluster_supported_version
- k8s_cluster_version_supported

### ETCD
- k8s_etcd_backup_configured
- k8s_etcd_backup_encryption_enabled
- k8s_etcd_encryption_enabled
- k8s_etcd_tls_enabled

### IMAGE
- k8s_image_vulnerability_scanning_enabled

### INGRESS
- k8s_ingress_certificate_expiration_check
- k8s_ingress_controller_ssl_protocols_check
- k8s_ingress_controller_tls_enforced
- k8s_ingress_controller_tls_protocols_configured
- k8s_ingress_controller_waf_enabled
- k8s_ingress_tls_certificate_expiration_check
- k8s_ingress_tls_enabled
- k8s_ingress_tls_enforced

### NETWORKPOLICY
- k8s_networkpolicy_default_deny_egress
- k8s_networkpolicy_default_deny_ingress
- k8s_networkpolicy_flow_logs_enabled
- k8s_networkpolicy_internet_facing_protection
- k8s_networkpolicy_logging_enabled
- k8s_networkpolicy_restrict_egress_to_internet
- k8s_networkpolicy_restrict_external_access
- k8s_networkpolicy_restrict_ingress_ports

### NODE
- k8s_node_os_patch_compliance
- k8s_node_os_patches_applied
- k8s_node_os_patching_compliance

### POD
- k8s_pod_backup_annotation_present
- k8s_pod_persistent_volume_backup_configured
- k8s_pod_security_context_non_root
- k8s_pod_security_patches_applied
- k8s_pod_security_patching_compliance
- k8s_pod_security_standard_restricted

### RBAC
- k8s_rbac_change_management_roles_defined
- k8s_rbac_inactive_user_cleanup
- k8s_rbac_least_privilege_enforcement
- k8s_rbac_no_cluster_admin_binding
- k8s_rbac_role_binding_scope_limited
- k8s_rbac_service_account_management_review
- k8s_rbac_service_account_scope_limited
- k8s_rbac_service_account_token_automount_disabled
- k8s_rbac_user_access_review

### SECRET
- k8s_secret_backup_policy_configured
- k8s_secret_encryption_at_rest_enabled
- k8s_secret_external_manager_configured
- k8s_secret_git_repo_url_no_sensitive_credentials
- k8s_secret_minimize_key_storage_locations
- k8s_secret_no_sensitive_data_in_env
- k8s_secret_tls_certificates_expiration_check

### SERVICE
- k8s_service_mesh_mutual_tls_enabled
- k8s_service_mesh_security_enabled
- k8s_service_mesh_tls_certificate_expiration_check
- k8s_service_mesh_tls_enforced
- k8s_service_type_loadbalancer_restricted
- k8s_service_type_not_nodeport

### SOFTWARE
- k8s_software_patch_management_enabled
