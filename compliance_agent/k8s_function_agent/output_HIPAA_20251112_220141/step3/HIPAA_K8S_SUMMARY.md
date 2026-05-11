# K8s Function Generation Summary - HIPAA
Generated: 2025-11-12 22:29:22

## Statistics
- Total controls processed: 32
- Approved: 0
- Approved with changes: 31
- Rejected: 0
- Not applicable: 1
- Errors: 0
- Total K8s functions generated: 112
- Unique K8s functions: 58

## K8s Functions by Category

### ADMISSION
- k8s_admission_controller_pod_security_enabled
- k8s_admission_controller_policy_enforcement_enabled
- k8s_admission_controller_security_incident_detection_enabled
- k8s_admission_controller_security_policies_enabled
- k8s_admission_webhook_policy_enforced

### APISERVER
- k8s_apiserver_anonymous_auth_disabled
- k8s_apiserver_audit_logging_enabled
- k8s_apiserver_authentication_enabled
- k8s_apiserver_authorization_mode_rbac
- k8s_apiserver_backup_configured
- k8s_apiserver_encryption_provider_configured
- k8s_apiserver_high_availability_configured

### AUDIT
- k8s_audit_emergency_access_logging_enabled
- k8s_audit_log_authentication_failures
- k8s_audit_log_integrity_validation_enabled
- k8s_audit_log_integrity_verification_enabled
- k8s_audit_log_retention_configured
- k8s_audit_logging_enabled
- k8s_audit_policy_captures_metadata
- k8s_audit_policy_captures_security_events
- k8s_audit_policy_metadata_captured
- k8s_audit_risk_analysis_policy_configured

### CLUSTER
- k8s_cluster_backup_and_restore_tested
- k8s_cluster_disaster_recovery_plan_documented

### DISASTER
- k8s_disaster_recovery_plan_documented

### ETCD
- k8s_etcd_backup_configured
- k8s_etcd_encryption_enabled

### IMAGE
- k8s_image_vulnerability_scanning_enabled

### INGRESS
- k8s_ingress_tls_enabled

### NAMESPACE
- k8s_namespace_dedicated_for_clearinghouse

### NETWORKPOLICY
- k8s_networkpolicy_default_deny_egress
- k8s_networkpolicy_default_deny_ingress
- k8s_networkpolicy_isolate_healthcare_clearinghouse
- k8s_networkpolicy_monitoring_enabled
- k8s_networkpolicy_risk_assessment_configured
- k8s_networkpolicy_secure_transport_policy

### NODE
- k8s_node_auto_repair_enabled

### PERSISTENT
- k8s_persistent_volume_backup_enabled

### POD
- k8s_pod_disaster_recovery_plan_documented
- k8s_pod_security_standard_restricted
- k8s_pod_security_standard_restricted_for_clearinghouse

### RBAC
- k8s_rbac_emergency_access_role_configured
- k8s_rbac_least_privilege_enforcement
- k8s_rbac_least_privilege_for_clearinghouse
- k8s_rbac_no_cluster_admin_binding
- k8s_rbac_no_shared_service_accounts
- k8s_rbac_oidc_authentication_configured
- k8s_rbac_role_binding_cleanup_on_termination
- k8s_rbac_role_binding_review
- k8s_rbac_service_account_revocation_on_termination
- k8s_rbac_service_account_token_automount_disabled
- k8s_rbac_unique_service_account_per_user
- k8s_rbac_user_access_review
- k8s_rbac_user_access_revocation_on_termination
- k8s_rbac_user_identity_audit_enabled

### SECRET
- k8s_secret_emergency_access_credentials_protected
- k8s_secret_encryption_at_rest_enabled

### SERVICE
- k8s_service_mesh_mtls_enabled
