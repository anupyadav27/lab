# K8s Function Generation Summary - CANADA_PBMM
Generated: 2025-11-12 23:06:19

## Statistics
- Total controls processed: 156
- Approved: 0
- Approved with changes: 34
- Rejected: 0
- Not applicable: 122
- Errors: 0
- Total K8s functions generated: 124
- Unique K8s functions: 75

## K8s Functions by Category

### ADMISSION
- k8s_admission_controller_change_control_enabled
- k8s_admission_controller_image_vulnerability_scanning_enabled
- k8s_admission_controller_patch_management_policy_enforced
- k8s_admission_controller_security_event_alerting
- k8s_admission_controller_security_policy_enabled
- k8s_admission_controller_vulnerability_policy_enforced
- k8s_admission_webhook_security_policy_configured

### APISERVER
- k8s_apiserver_audit_log_backup_configured
- k8s_apiserver_audit_logging_enabled
- k8s_apiserver_audit_policy_configured
- k8s_apiserver_authentication_enabled
- k8s_apiserver_authorization_mode_rbac
- k8s_apiserver_automatic_upgrade_enabled
- k8s_apiserver_rate_limiting_enabled
- k8s_apiserver_secure_configuration_enabled
- k8s_apiserver_tls_enabled

### AUDIT
- k8s_audit_configuration_change_logged
- k8s_audit_incident_response_policy_configured
- k8s_audit_log_alerts_configured
- k8s_audit_log_analysis_configured
- k8s_audit_log_backup_configured
- k8s_audit_log_file_validation_enabled
- k8s_audit_log_format_json
- k8s_audit_log_high_severity_event_detection
- k8s_audit_log_integrity_verification_enabled
- k8s_audit_log_retention_configured
- k8s_audit_logging_enabled
- k8s_audit_logging_network_policy_changes
- k8s_audit_policy_captures_metadata
- k8s_audit_policy_configured
- k8s_audit_policy_metadata_capture
- k8s_audit_policy_metadata_capture_enabled
- k8s_audit_policy_metadata_captured
- k8s_audit_policy_timestamps_included

### CLUSTER
- k8s_cluster_backup_and_restore_procedures_documented

### ETCD
- k8s_etcd_backup_configured
- k8s_etcd_encryption_at_rest_enabled
- k8s_etcd_encryption_enabled
- k8s_etcd_tls_enabled

### IMAGE
- k8s_image_vulnerability_scanning_enabled

### INGRESS
- k8s_ingress_tls_enabled

### NETWORKPOLICY
- k8s_networkpolicy_default_deny_egress
- k8s_networkpolicy_default_deny_ingress
- k8s_networkpolicy_encryption_in_transit_enabled
- k8s_networkpolicy_internal_traffic_restricted
- k8s_networkpolicy_monitoring_enabled
- k8s_networkpolicy_restrict_public_ip_access
- k8s_networkpolicy_suspicious_activity_monitoring

### NODE
- k8s_node_labeling_for_inventory_tracking

### PERSISTENTVOLUME
- k8s_persistentvolume_backup_policy_defined

### POD
- k8s_pod_backup_annotation_present
- k8s_pod_disaster_recovery_policy_defined
- k8s_pod_labeling_for_inventory_tracking
- k8s_pod_resource_limits_set
- k8s_pod_security_standard_restricted
- k8s_pod_security_standard_vulnerability_checks

### RBAC
- k8s_rbac_change_control_role_defined
- k8s_rbac_least_privilege_enforcement
- k8s_rbac_no_cluster_admin_binding
- k8s_rbac_no_default_service_account_usage
- k8s_rbac_oidc_authentication_configured
- k8s_rbac_role_binding_least_privilege
- k8s_rbac_separation_of_duties_enforced
- k8s_rbac_service_account_inactive_cleanup
- k8s_rbac_service_account_token_automount_disabled
- k8s_rbac_unique_service_account_per_pod
- k8s_rbac_unused_role_cleanup
- k8s_rbac_user_access_review_scheduled

### RESOURCE
- k8s_resource_annotations_for_inventory_metadata

### SECRET
- k8s_secret_backup_configured
- k8s_secret_encryption_at_rest_enabled
- k8s_secret_external_manager_configured
- k8s_secret_rotation_policy_configured

### SERVICE
- k8s_service_mesh_mtls_enabled
- k8s_service_type_loadbalancer_restricted
