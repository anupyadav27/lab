# K8s Function Generation Summary - NIST_800_171
Generated: 2025-11-12 22:54:57

## Statistics
- Total controls processed: 50
- Approved: 1
- Approved with changes: 46
- Rejected: 0
- Not applicable: 3
- Errors: 0
- Total K8s functions generated: 170
- Unique K8s functions: 78

## K8s Functions by Category

### ADMISSION
- k8s_admission_controller_antivirus_enabled
- k8s_admission_controller_incident_reporting_enabled
- k8s_admission_controller_pod_security_enabled
- k8s_admission_controller_restrict_user_installed_software
- k8s_admission_controller_security_alerts_enabled
- k8s_admission_controller_security_policy_enabled
- k8s_admission_controller_security_updates_applied
- k8s_admission_controller_software_whitelist_enabled
- k8s_admission_controller_vulnerability_policy_enforced
- k8s_admission_controller_vulnerability_scan_on_admission
- k8s_admission_controller_vulnerability_scanning_enabled

### APISERVER
- k8s_apiserver_audit_logging_enabled
- k8s_apiserver_audit_policy_configured
- k8s_apiserver_authentication_enabled
- k8s_apiserver_authentication_mfa_enabled
- k8s_apiserver_authorization_mode_rbac
- k8s_apiserver_fips_tls_enabled
- k8s_apiserver_secure_configuration_applied
- k8s_apiserver_security_updates_applied
- k8s_apiserver_tls_enabled

### AUDIT
- k8s_audit_admission_webhook_logging_enabled
- k8s_audit_configuration_changes_logged
- k8s_audit_log_failure_alert_configured
- k8s_audit_log_protection_configured
- k8s_audit_log_retention_configured
- k8s_audit_logging_enabled
- k8s_audit_policy_captures_metadata
- k8s_audit_policy_captures_privileged_actions
- k8s_audit_policy_metadata_captured
- k8s_audit_policy_review_scheduled
- k8s_audit_software_installation_logging_enabled
- k8s_audit_vulnerability_remediation_logged

### CONFIG
- k8s_config_baseline_policies_applied

### ETCD
- k8s_etcd_encryption_enabled
- k8s_etcd_fips_encryption_enabled
- k8s_etcd_tls_enabled

### EVENT
- k8s_event_alerting_system_configured

### IMAGE
- k8s_image_pull_policy_always
- k8s_image_scan_on_admission
- k8s_image_vulnerability_scanning_enabled

### INGRESS
- k8s_ingress_logging_enabled
- k8s_ingress_tls_enabled

### MONITORING
- k8s_monitoring_prometheus_alerts_configured

### NETWORKPOLICY
- k8s_networkpolicy_default_deny_egress
- k8s_networkpolicy_default_deny_ingress
- k8s_networkpolicy_documentation_up_to_date
- k8s_networkpolicy_egress_restricted_to_security_services
- k8s_networkpolicy_monitoring_enabled
- k8s_networkpolicy_restrict_external_access
- k8s_networkpolicy_restrict_remote_access

### NODE
- k8s_node_labels_inventory_maintained

### POD
- k8s_pod_host_network_disabled
- k8s_pod_labels_inventory_maintained
- k8s_pod_security_context_non_root
- k8s_pod_security_context_readonly_rootfs
- k8s_pod_security_standard_restricted

### RBAC
- k8s_rbac_audit_log_access_restricted
- k8s_rbac_documentation_up_to_date
- k8s_rbac_inactive_service_account_disabled
- k8s_rbac_least_privilege_enforcement
- k8s_rbac_no_cluster_admin_binding
- k8s_rbac_oidc_authentication_configured
- k8s_rbac_role_separation_enforced
- k8s_rbac_separate_user_and_admin_roles
- k8s_rbac_service_account_least_privilege
- k8s_rbac_service_account_restricted_roles
- k8s_rbac_service_account_token_automount_disabled
- k8s_rbac_service_account_token_expiration_configured
- k8s_rbac_user_access_review_policy_implemented
- k8s_rbac_user_action_audit_enabled

### SECRET
- k8s_secret_encryption_at_rest_enabled
- k8s_secret_fips_encryption_at_rest_enabled
- k8s_secret_transmission_tls_enabled

### SERVICE
- k8s_service_mesh_mtls_enabled
- k8s_service_mesh_traffic_encryption_enabled
- k8s_service_mtls_enabled
- k8s_service_type_loadbalancer_restricted
- k8s_service_type_not_nodeport
