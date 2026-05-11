# K8s Function Generation Summary - SOC2
Generated: 2025-11-12 22:21:22

## Statistics
- Total controls processed: 25
- Approved: 0
- Approved with changes: 25
- Rejected: 0
- Not applicable: 0
- Errors: 0
- Total K8s functions generated: 97
- Unique K8s functions: 55

## K8s Functions by Category

### ADMISSION
- k8s_admission_controller_anomaly_detection_enabled
- k8s_admission_controller_change_management_enabled
- k8s_admission_controller_change_management_enforced
- k8s_admission_controller_incident_response_policy_enabled
- k8s_admission_controller_pod_security_enabled
- k8s_admission_controller_policy_violation_alerts_enabled
- k8s_admission_controller_privilege_escalation_prevention
- k8s_admission_controller_security_event_detection
- k8s_admission_controller_security_incident_response_enabled
- k8s_admission_controller_vulnerability_scanning_enabled

### APISERVER
- k8s_apiserver_anonymous_auth_disabled
- k8s_apiserver_audit_logging_enabled

### AUDIT
- k8s_audit_change_management_logging_enabled
- k8s_audit_configuration_change_detection_enabled
- k8s_audit_log_retention_configured
- k8s_audit_log_retention_policy_configured
- k8s_audit_logging_enabled
- k8s_audit_policy_captures_metadata

### CLUSTER
- k8s_cluster_autoscaler_enabled

### ETCD
- k8s_etcd_backup_configured
- k8s_etcd_encryption_enabled
- k8s_etcd_snapshot_retention_policy_configured

### HPA
- k8s_hpa_configured_for_workloads

### IMAGE
- k8s_image_vulnerability_scanning_enabled

### INGRESS
- k8s_ingress_tls_enabled

### NETWORKPOLICY
- k8s_networkpolicy_anomaly_detection_enabled
- k8s_networkpolicy_change_audit_enabled
- k8s_networkpolicy_change_monitoring_enabled
- k8s_networkpolicy_default_deny_egress
- k8s_networkpolicy_default_deny_ingress
- k8s_networkpolicy_monitoring_alerts_configured
- k8s_networkpolicy_monitoring_enabled

### NODE
- k8s_node_resource_utilization_monitored

### POD
- k8s_pod_resource_requests_and_limits_set
- k8s_pod_security_context_non_root
- k8s_pod_security_standard_restricted
- k8s_pod_termination_grace_period_set

### RBAC
- k8s_rbac_access_review_process
- k8s_rbac_change_management_policy_configured
- k8s_rbac_incident_response_team_access_configured
- k8s_rbac_least_privilege_enforcement
- k8s_rbac_no_cluster_admin_binding
- k8s_rbac_role_binding_audit_enabled
- k8s_rbac_role_binding_review
- k8s_rbac_role_change_audit_enabled
- k8s_rbac_role_separation_of_duties
- k8s_rbac_service_account_management
- k8s_rbac_service_account_management_review
- k8s_rbac_service_account_privilege_restriction
- k8s_rbac_user_registration_authorization_review

### SECRET
- k8s_secret_backup_and_recovery_enabled
- k8s_secret_encryption_at_rest_enabled
- k8s_secret_not_in_env_variables
- k8s_secret_rotation_policy_configured

### SERVICE
- k8s_service_type_loadbalancer_restricted
