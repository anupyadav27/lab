# GCP GKE Service Compliance Prompt

## Service Information
- **Service Name**: GKE
- **Description**: GCP GKE Service
- **Total Functions**: 111
- **SDK Client**: container_client
- **Service Type**: compute

## Function List
The following 111 functions are available for GKE compliance checks:

1. `cloudfunctions_function_deployment_strategy_not_always_active`
2. `functions_deployment_strategy_non_default`
3. `dns_dnssec_keysigningkey_no_rsasha1`
4. `gke_worker_nodes_firewall_configured`
5. `gke_cluster_cni_network_policies_supported`
6. `gke_cluster_control_plane_authorized_networks_enabled`
7. `gke_control_plane_authorized_networks_enabled`
8. `gke_cluster_vpc_native_enabled`
9. `gke_workload_identity_no_admin_access`
10. `gke_workload_identity_no_admin_privileges`
11. `gke_workload_identity_dedicated_service_account`
12. `gke_cluster_system_masters_group_restriction`
13. `gke_cluster_binary_authorization_enabled`
14. `gke_kube_proxy_kubeconfig_ownership_root`
15. `gke_kubelet_config_file_root_ownership`
16. `gke_kubelet_anonymous_auth_disabled`
17. `gke_kubelet_client_ca_file_configured`
18. `gke_kubelet_read_only_port_disabled`
19. `gke_kubelet_event_record_qps_set`
20. `gke_kubelet_client_certificate_rotation_enabled`
21. `gke_cluster_rotate_kubelet_server_certificate_enabled`
22. `gke_secrets_access_minimized`
23. `gke_secrets_as_files_preferred`
24. `gke_namespace_isolation_enabled`
25. `gke_namespace_default_usage_restricted`
26. `gke_cluster_node_auto_repair_enabled`
27. `gke_nodes_auto_upgrade_enabled`
28. `gke_node_shielded_secure_boot_enabled`
29. `gke_cluster_private_nodes_enabled`
30. `gke_client_certificates_disabled`
31. `gke_cluster_web_ui_disabled`
32. `gke_cluster_alpha_status_check`
33. `gke_sandbox_enabled_for_untrusted_workloads`
34. `gke_kubelet_kubeconfig_file_ownership_check`
35. `gke_cluster_shielded_nodes_enabled`
36. `gke_nodes_secure_boot_enabled`
37. `gke_pd_cmek_enabled`
38. `gke_cluster_alpha_features_disabled`
39. `gke_cluster_authorization_mode_not_always_allow`
40. `gke_cluster_no_default_service_account`
41. `gke_rbac_users_managed_with_google_groups`
42. `gke_cluster_abac_disabled`
43. `deploymentmanager_deployment_status_deployed`
44. `cloudbuild_first_step_single_deployment`
45. `deploy_stage_single_deployment_limit`
46. `deployment_manager_configurations_non_public`
47. `deployment_manager_configurations_pubsub_notifications_enabled`
48. `deploymentmanager_deployments_pubsub_notifications`
49. `deploymentmanager_configurations_pubsub_notifications_enabled`
50. `cloudbuild_pipeline_first_step_single_deployment`
51. `deploymentmanager_deployments_pubsub_notifications_configured`
52. `deploymentmanager_configurations_pubsub_notifications`
53. `container_registry_vulnerability_scanning_enabled`
54. `container_registry_repository_vulnerability_scanning_enabled`
55. `container_deployment_security_context_defined`
56. `gke_cluster_pod_security_baseline_enforced`
57. `gke_pod_container_security_context_applied`
58. `gke_pod_security_context_applied`
59. `gke_shielded_nodes_integrity_monitoring_enabled`
60. `container_gke_logging_enabled`
61. `container_cluster_logging_enabled`
62. `container_gke_cluster_logging_enabled`
63. `container_pod_logging_configured`
64. `container_gke_logging_configured`
65. `gke_node_auditd_logging_enabled`
66. `container_workload_logging_enabled`
67. `logging_elasticsearch_clusters_log_configuration`
68. `logging_elasticsearch_clusters_configured`
69. `container_pod_logging_configuration_set`
70. `gke_cluster_private_endpoint_enabled_public_access_disabled`
71. `dataproc_clusters_logging_configured`
72. `dataproc_cluster_log_min_duration_statement_disabled`
73. `dataproc_cluster_log_statement_ddl`
74. `dataproc_cluster_public_access_prevention_enabled`
75. `dataproc_cluster_block_public_access_enabled`
76. `dataproc_cluster_node_to_node_encryption_enabled`
77. `dataproc_cluster_kerberos_enabled`
78. `dataproc_cluster_https_tls_enforced`
79. `dataproc_cluster_fine_grained_access_control_enabled`
80. `dataproc_cluster_https_enforced`
81. `dataproc_cluster_cmek_enabled`
82. `dataproc_cluster_encrypted_with_cmek`
83. `gke_cluster_metadata_server_enabled`
84. `container_pod_hostpid_disabled`
85. `container_pod_readonly_root_filesystem`
86. `container_environment_variables_no_secrets`
87. `container_pod_privileged_false`
88. `container_pod_privileged_flag_disabled`
89. `container_pod_run_as_user_defined`
90. `container_pod_run_as_user_specified`
91. `container_pod_read_only_root_filesystem`
92. `container_containers_read_only_root_filesystem`
93. `container_pod_privileged_flag_false`
94. `container_pod_specifications_user_defined`
95. `container_pod_readonly_root_filesystem_enforced`
96. `container_optimized_os_dm_verity_enabled`
97. `container_registry_user_access_minimized`
98. `container_gke_endpoint_private`
99. `container_cluster_endpoint_private`
100. `container_gke_secrets_encrypted_with_kms`
101. `container_gke_clusters_secrets_encrypted_with_kms`
102. `container_cluster_avoid_oldest_supported_version`
103. `container_cluster_supported_kubernetes_version`
104. `container_gke_containers_readonly_root_filesystem`
105. `container_gke_containers_read_only_root_filesystem`
106. `container_gke_cluster_avoid_oldest_supported_version`
107. `container_gke_cluster_supported_version`
108. `gke_pod_service_account_token_mount_restriction`
109. `gke_pod_seccomp_profile_runtime_default`
110. `kubernetes_default_namespace_not_used`
111. `container_gke_shielded_nodes_enabled`


## Compliance Framework Coverage
This service supports compliance checks for:
- **NIST Cybersecurity Framework**
- **PCI DSS v4.0**
- **ISO 27001**
- **SOC 2**
- **GDPR**
- **HIPAA** (where applicable)

## Usage Instructions
1. Use the function names above to create compliance checks
2. Each function should be implemented as a separate compliance rule
3. Follow the naming convention: `gke_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def gke_example_function_check():
    """
    Example compliance check for GKE service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in gke check: {e}")
        return False
```

## Notes
- All functions are based on GCP GKE API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
