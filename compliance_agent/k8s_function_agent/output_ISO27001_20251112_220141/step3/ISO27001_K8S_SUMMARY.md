# K8s Function Generation Summary - ISO27001
Generated: 2025-11-12 22:44:04

## Statistics
- Total controls processed: 99
- Approved: 1
- Approved with changes: 40
- Rejected: 0
- Not applicable: 58
- Errors: 0
- Total K8s functions generated: 157
- Unique K8s functions: 75

## K8s Functions by Category

### ADMISSION
- k8s_admission_controller_incident_response_policy_enforced
- k8s_admission_controller_pod_security_enabled
- k8s_admission_controller_security_event_detection
- k8s_admission_controller_supplier_service_change_management
- k8s_admission_data_masking_policy_enforced
- k8s_admission_threat_detection_webhook_configured
- k8s_admission_webhook_logging_enabled

### APISERVER
- k8s_apiserver_audit_logging_enabled
- k8s_apiserver_authentication_enabled
- k8s_apiserver_authorization_mode_rbac
- k8s_apiserver_tls_enabled

### AUDIT
- k8s_audit_incident_response_policy_configured
- k8s_audit_log_encryption_enabled
- k8s_audit_log_high_severity_alerts_configured
- k8s_audit_log_integrity_enabled
- k8s_audit_log_retention_configured
- k8s_audit_logging_enabled
- k8s_audit_logging_policies_documented
- k8s_audit_policy_captures_metadata
- k8s_audit_policy_metadata_captured
- k8s_audit_supplier_service_changes_logged
- k8s_audit_threat_detection_enabled

### CLUSTER
- k8s_cluster_multi_zone_deployment_enabled

### ETCD
- k8s_etcd_backup_configured
- k8s_etcd_backup_encryption_enabled
- k8s_etcd_data_retention_policy_configured
- k8s_etcd_encryption_enabled

### IMAGE
- k8s_image_scan_on_admission
- k8s_image_vulnerability_scanning_enabled

### INGRESS
- k8s_ingress_tls_enabled
- k8s_ingress_waf_enabled

### NETWORKPOLICY
- k8s_networkpolicy_default_deny_egress
- k8s_networkpolicy_default_deny_ingress
- k8s_networkpolicy_flow_logging_enabled
- k8s_networkpolicy_monitoring_enabled
- k8s_networkpolicy_namespace_isolation
- k8s_networkpolicy_no_public_access
- k8s_networkpolicy_policies_documented
- k8s_networkpolicy_restrict_external_access
- k8s_networkpolicy_restrict_internet_access
- k8s_networkpolicy_supplier_service_monitoring_enabled
- k8s_networkpolicy_threat_detection_traffic_monitoring
- k8s_networkpolicy_web_traffic_restricted

### NODE
- k8s_node_autoscaling_enabled

### PERSISTENT
- k8s_persistent_volume_multi_zone_replication

### POD
- k8s_pod_anti_affinity_configured
- k8s_pod_backup_annotation_present
- k8s_pod_backup_policy_configured
- k8s_pod_finalizer_configured
- k8s_pod_security_context_non_root
- k8s_pod_termination_grace_period_configured

### RBAC
- k8s_rbac_audit_access_logging_enabled
- k8s_rbac_incident_response_role_defined
- k8s_rbac_least_privilege_enforcement
- k8s_rbac_no_cluster_admin_binding
- k8s_rbac_no_single_user_full_control
- k8s_rbac_oidc_authentication_configured
- k8s_rbac_policies_documented
- k8s_rbac_role_binding_least_privilege
- k8s_rbac_role_binding_review_enabled
- k8s_rbac_role_binding_separation
- k8s_rbac_role_binding_to_specific_namespaces
- k8s_rbac_segregation_of_duties_enforced
- k8s_rbac_separation_of_duties_enforced
- k8s_rbac_service_account_privileges_restricted
- k8s_rbac_service_account_token_automount_disabled

### SECRET
- k8s_secret_data_masking_policy_enforced
- k8s_secret_encryption_at_rest_enabled
- k8s_secret_lifecycle_management_enabled
- k8s_secret_management_policies_documented

### SERVICE
- k8s_service_mesh_mtls_enabled
- k8s_service_mesh_threat_detection_integrated
- k8s_service_mesh_web_filtering_enabled
- k8s_service_type_loadbalancer_restricted
- k8s_service_type_not_nodeport
