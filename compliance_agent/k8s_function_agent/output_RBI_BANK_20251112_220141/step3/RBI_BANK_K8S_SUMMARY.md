# K8s Function Generation Summary - RBI_BANK
Generated: 2025-11-12 22:07:43

## Statistics
- Total controls processed: 27
- Approved: 2
- Approved with changes: 18
- Rejected: 0
- Not applicable: 7
- Errors: 0
- Total K8s functions generated: 71
- Unique K8s functions: 53

## K8s Functions by Category

### ADMISSION
- k8s_admission_controller_change_management_enabled
- k8s_admission_controller_security_policy_enabled
- k8s_admission_webhook_configured

### APISERVER
- k8s_apiserver_anonymous_auth_disabled
- k8s_apiserver_authorization_mode_rbac
- k8s_apiserver_backup_configured
- k8s_apiserver_ssh_access_disabled
- k8s_apiserver_tls_enabled

### AUDIT
- k8s_audit_log_file_validation_enabled
- k8s_audit_log_retention_configured
- k8s_audit_logging_enabled
- k8s_audit_policy_metadata_captured

### CLUSTER
- k8s_cluster_backup_and_restore_tested

### CONTROL
- k8s_control_plane_auto_upgrade_enabled

### DISASTER
- k8s_disaster_recovery_plan_documented

### ETCD
- k8s_etcd_backup_configured
- k8s_etcd_backup_retention_policy_set
- k8s_etcd_encryption_enabled
- k8s_etcd_snapshot_schedule_defined
- k8s_etcd_tls_enabled

### IMAGE
- k8s_image_latest_tag_prohibited
- k8s_image_pull_policy_always
- k8s_image_scan_on_admission
- k8s_image_vulnerability_scanning_enabled

### MONITORING
- k8s_monitoring_alerts_configured

### NETWORKPOLICY
- k8s_networkpolicy_default_deny_egress
- k8s_networkpolicy_default_deny_ingress
- k8s_networkpolicy_external_access_restricted
- k8s_networkpolicy_flow_logs_enabled
- k8s_networkpolicy_inventory_documented
- k8s_networkpolicy_no_public_access
- k8s_networkpolicy_restrict_rdp
- k8s_networkpolicy_restrict_ssh
- k8s_networkpolicy_ssh_restricted
- k8s_networkpolicy_unused_policies_removed

### NODE
- k8s_node_os_patch_management_enabled

### RBAC
- k8s_rbac_change_management_roles_defined
- k8s_rbac_database_access_restricted
- k8s_rbac_least_privilege_enforcement
- k8s_rbac_no_cluster_admin_binding
- k8s_rbac_no_guest_service_accounts
- k8s_rbac_no_root_access_key
- k8s_rbac_service_account_least_privilege_enforced
- k8s_rbac_service_account_token_automount_disabled
- k8s_rbac_service_account_usage_audited

### SECRET
- k8s_secret_certificate_expiration_monitoring_enabled
- k8s_secret_certificate_renewal_process_defined
- k8s_secret_certificate_revocation_list_configured
- k8s_secret_database_credentials_encrypted
- k8s_secret_encryption_at_rest_enabled
- k8s_secret_rotation_policy_configured

### SERVICE
- k8s_service_type_not_nodeport

### WORKER
- k8s_worker_node_auto_upgrade_enabled
