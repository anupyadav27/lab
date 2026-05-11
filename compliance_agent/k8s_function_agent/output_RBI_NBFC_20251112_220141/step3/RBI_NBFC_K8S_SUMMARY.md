# K8s Function Generation Summary - RBI_NBFC
Generated: 2025-11-12 22:11:34

## Statistics
- Total controls processed: 37
- Approved: 0
- Approved with changes: 16
- Rejected: 0
- Not applicable: 21
- Errors: 0
- Total K8s functions generated: 55
- Unique K8s functions: 43

## K8s Functions by Category

### ADMISSION
- k8s_admission_controller_antimalware_policies_enforced
- k8s_admission_controller_pod_security_enabled
- k8s_admission_webhook_authentication_enabled

### APISERVER
- k8s_apiserver_authentication_enabled
- k8s_apiserver_authorization_mode_rbac
- k8s_apiserver_tls_enabled

### AUDIT
- k8s_audit_incident_notification_configured
- k8s_audit_incident_response_admission_controller_enabled
- k8s_audit_incident_response_policy_configured
- k8s_audit_log_file_validation_enabled
- k8s_audit_log_retention_configured
- k8s_audit_logging_enabled
- k8s_audit_policy_captures_metadata

### CLUSTER
- k8s_cluster_resource_monitoring_enabled

### CONTROL
- k8s_control_plane_patch_compliance

### ETCD
- k8s_etcd_backup_and_restore_tested
- k8s_etcd_backup_configured
- k8s_etcd_encryption_enabled
- k8s_etcd_patch_compliance
- k8s_etcd_tls_enabled

### IMAGE
- k8s_image_latest_tag_avoidance
- k8s_image_scan_on_admission
- k8s_image_vulnerability_scanning_enabled

### INGRESS
- k8s_ingress_tls_enabled

### NETWORKPOLICY
- k8s_networkpolicy_default_deny_egress
- k8s_networkpolicy_default_deny_ingress
- k8s_networkpolicy_flow_logs_enabled
- k8s_networkpolicy_restrict_rdp_access
- k8s_networkpolicy_restrict_ssh_access

### NODE
- k8s_node_os_patch_compliance
- k8s_node_resource_monitoring_enabled

### PERSISTENT
- k8s_persistent_volume_snapshot_enabled

### POD
- k8s_pod_disaster_recovery_policy_defined
- k8s_pod_horizontal_autoscaler_enabled
- k8s_pod_resource_limits_configured
- k8s_pod_security_standard_restricted

### RBAC
- k8s_rbac_least_privilege_enforcement
- k8s_rbac_no_cluster_admin_binding
- k8s_rbac_oidc_authentication_configured
- k8s_rbac_service_account_token_automount_disabled

### SECRET
- k8s_secret_encryption_at_rest_enabled
- k8s_secret_not_in_env_variables

### VOLUME
- k8s_volume_snapshot_enabled
