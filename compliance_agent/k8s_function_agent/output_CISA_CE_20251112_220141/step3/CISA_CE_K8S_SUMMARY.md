# K8s Function Generation Summary - CISA_CE
Generated: 2025-11-12 22:14:40

## Statistics
- Total controls processed: 22
- Approved: 0
- Approved with changes: 14
- Rejected: 0
- Not applicable: 8
- Errors: 0
- Total K8s functions generated: 46
- Unique K8s functions: 36

## K8s Functions by Category

### ADMISSION
- k8s_admission_controller_image_policy_configured
- k8s_admission_controller_image_security_scanning_enabled

### APISERVER
- k8s_apiserver_oidc_mfa_enabled
- k8s_apiserver_oidc_mfa_enforced

### AUDIT
- k8s_audit_log_network_activity_captured
- k8s_audit_log_retention_configured
- k8s_audit_logging_enabled

### CLUSTER
- k8s_cluster_version_upgrade_policy_configured

### CONFIG
- k8s_config_namespace_assets_inventory_maintained
- k8s_config_node_assets_inventory_maintained
- k8s_config_pod_assets_inventory_maintained
- k8s_config_service_assets_inventory_maintained

### ETCD
- k8s_etcd_backup_configured
- k8s_etcd_backup_retention_policy_defined
- k8s_etcd_backup_schedule_automated
- k8s_etcd_encryption_enabled
- k8s_etcd_tls_enabled

### IMAGE
- k8s_image_pull_policy_always
- k8s_image_scan_on_admission

### NETWORKPOLICY
- k8s_networkpolicy_default_deny_egress
- k8s_networkpolicy_default_deny_ingress
- k8s_networkpolicy_inventory_documented

### NODE
- k8s_node_auto_upgrade_enabled

### POD
- k8s_pod_security_standard_restricted

### RBAC
- k8s_rbac_least_privilege_enforcement
- k8s_rbac_no_cluster_admin_binding
- k8s_rbac_oidc_mfa_enforced
- k8s_rbac_role_binding_least_privilege
- k8s_rbac_role_binding_review
- k8s_rbac_service_account_inactive_cleanup
- k8s_rbac_service_account_least_privilege
- k8s_rbac_user_access_inventory_documented
- k8s_rbac_user_access_review_policy

### SECRET
- k8s_secret_encryption_at_rest_enabled
- k8s_secret_not_in_env_variables

### SERVICE
- k8s_service_type_not_nodeport
