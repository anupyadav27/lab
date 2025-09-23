# Azure Azure Networking Service Compliance Prompt

## Service Information
- **Service Name**: NETWORK
- **Display Name**: Azure Networking
- **Total Functions**: 135
- **Original Categories**: Unknown, Network|Security, Network
- **Categorization Methods**: sdk_example, function_name

## Function List
The following 135 functions are available for Azure Networking compliance checks:

1. `network_security_group_flow_log_analytics`
2. `network_rdp_internet_access_restricted`
3. `network_ssh_internet_access_restricted`
4. `network_http_internet_access_restriction`
5. `network_networkwatcher_enabled`
6. `network_publicip_periodic_evaluation`
7. `network_bastion_host_exists`
8. `network_security_group_flow_logs_to_log_analytics`
9. `network_load_balancer_ssl_policy_compliance`
10. `network_application_gateway_front_door_https_listener_configured`
11. `network_nsgs_restricted_inbound_traffic_ports`
12. `vpn_virtual_wan_user_access_all_false`
13. `network_virtualwanhub_auto_accept_shared_connections_disabled`
14. `app_gateway_load_balancer_listener_azure_key_vault_certificates`
15. `network_nsgs_restrict_inbound_ssh`
16. `network_vnet_gateway_authorized_attachment`
17. `network_nsg_no_unrestricted_inbound_traffic_on_default_ports`
18. `network_route_table_no_public_routes_to_internet`
19. `network_security_groups_associated_with_subnet_or_interface`
20. `network_virtualnetworkpeering_dns_resolution_enabled`
21. `vpn_virtual_wan_user_access_all_disabled`
22. `network_appgateway_loadbalancer_uses_keyvault_certificates`
23. `network_route_table_no_public_internet_gateway`
24. `network_nsg_associated_with_subnet_or_nic`
25. `network_nsgs_restrict_unauthorized_ports`
26. `application_gateway_load_balancer_listener_azure_key_vault_certificates`
27. `network_route_table_no_public_routes_to_igw`
28. `network_security_group_association_required`
29. `network_vpn_site_to_site_tunnels_connected`
30. `network_nsg_associated_with_subnet_or_interface`
31. `network_vpn_site_to_site_tunnels_are_connected`
32. `vm_vmss_network_interface_no_public_ip`
33. `appgateway_loadbalancer_listener_azurekeyvault_certificates`
34. `network_nsg_association_required`
35. `network_loadbalancer_user_defined_desync_mitigation_mode`
36. `vpn_gateway_diagnostic_logging_for_client_connections`
37. `network_load_balancer_application_gateway_diagnostic_logs_enabled`
38. `network_firewall_logging_enabled`
39. `network_loadbalancer_user_defined_desync_mitigation`
40. `vpn_gateway_diagnostic_logging_enabled_for_client_connections`
41. `vpn_gateway_client_connection_diagnostic_logging`
42. `vpn_gateway_diagnostic_logging_client_connections_enabled`
43. `network_vpngateway_diagnostic_logging_enabled`
44. `vpn_gateway_diagnostic_logging_enabled`
45. `network_application_gateway_front_door_load_balancer_public_ip_ddos_protection_waf_policy_association`
46. `network_application_gateway_https_listener_configured`
47. `application_gateway_http_listener_https_redirection`
48. `network_appgateway_loadbalancer_azurekeyvault_certificates`
49. `application_gateway_load_balancer_listener_azure_key_vault_certificate`
50. `network_appgateway_loadbalancer_azurekeyvault_certificates_configured`
51. `network_application_gateway_load_balancer_azure_key_vault_certificates_configured`
52. `network_applicationgateway_waf_enabled`
53. `waf_policy_associated_application_gateway_api_management_front_door`
54. `application_gateway_waf_enabled`
55. `network_waf_policy_associated_with_resource`
56. `azure_ddos_protection_drt_access_configured`
57. `network_ddos_protection_drt_access_configured`
58. `network_ddosprotection_drt_access_configured`
59. `network_load_balancer_ssl_listeners_custom_ssl_policy`
60. `azure_ddosprotection_drt_access_configured`
61. `vpn_gateway_connection_logs_enabled`
62. `network_firewall_internet_facing_systems_secure`
63. `network_interface_promiscuous_mode_disabled`
64. `network_flow_log_restricted_protocol_exfiltration`
65. `network_endpoint_dos_protection_enabled`
66. `network_service_dos_protection_enabled`
67. `network_networkwatcher_enabled_state`
68. `network_cable_protection_status`
69. `network_system_data_leakage_prevention`
70. `network_security_control`
71. `network_service_security_implementation_monitoring`
72. `network_web_access_manage_external_content_exposure`
73. `network_security_restriction_protection_additional_auth_boundary_systems`
74. `network_data_transmission_encryption_restriction_mobile_device_protection`
75. `network_security_group_ip_management_device_authentication`
76. `network_wireless_ensure_protection_measures`
77. `azure_remote_access_protective_measures_implementation`
78. `network_firewall_internet_access_restriction`
79. `network_secure_transmission_policy_established`
80. `network_device_access_control_established_periodically`
81. `network_firewall_highest_security_level_and_critical_devices_evaluation`
82. `network_rdp_disabled_approved_only`
83. `network_privileged_accounts_mfa_implementation`
84. `network_system_limit_external_connections`
85. `network_boundary_protection_implementation`
86. `network_remote_access_systems_authorization_enforced`
87. `network_firewall_dos_protection_employed`
88. `network_private_endpoint_secure_access`
89. `azure_network_information_flow_control`
90. `azure_network_privacy_attribute_association`
91. `azure_network_internal_connection_authorization`
92. `azure_network_configure_tls_enforcement`
93. `azure_network_nsg_ruleset_configuration_check`
94. `azure_network_change_control_enforcement`
95. `azure_network_diagram_maintenance`
96. `azure_network_insecure_protocols_detection`
97. `azure_network_encryption_enforcement`
98. `azure_network_wireless_defaults_check`
99. `azure_network_wireless_key_rotation`
100. `azure_network_jack_access_control`
101. `azure_network_hardware_access_control`
102. `azure_network_wireless_access_point_detection`
103. `azure_network_authorized_wireless_inventory_maintenance`
104. `azure_network_segmentation_testing`
105. `azure_network_segmentation_penetration_test_schedule`
106. `azure_network_customer_penetration_test_support`
107. `azure_network_intrusion_detection_configuration`
108. `azure_network_covert_communication_detection`
109. `azure_network_intrusion_detection_alerts_configured`
110. `azure_network_unauthorized_wireless_access_detection`
111. `azure_network_identify_sensitive_data_transmission`
112. `azure_network_side_channel_attack_protection`
113. `azure_network_secure_transmission_credentials`
114. `azure_network_secure_transmission_enforcement`
115. `azure_network_secure_transmission`
116. `azure_network_secure_transmission_verification`
117. `azure_network_endpoint_authentication_verification`
118. `azure_network_secure_endpoint_authentication`
119. `azure_network_secure_data_transmission_verification`
120. `azure_network_secure_transmission_of_tracking_data`
121. `azure_network_secure_transmission_to_log_storage`
122. `azure_network_secure_data_transmission`
123. `azure_network_verify_communication_methods`
124. `azure_network_enforce_secure_area_authentication`
125. `azure_network_enforce_secure_area_authorization`
126. `azure_network_restrict_interface_access`
127. `azure_network_restrict_function_resource_access`
128. `azure_network_enforce_fine_grained_access_control`
129. `azure_network_restrict_internet_accessible_interfaces`
130. `azure_network_enforce_authorization_rules`
131. `azure_network_sensitive_resource_access_authorization`
132. `azure_network_secure_area_enforcement`
133. `azure_network_cross_origin_access_restrictions`
134. `azure_network_tls_cipher_suite_enforcement`
135. `azure_network_mutual_authentication_enforcement`


## Compliance Framework Coverage
This service supports compliance checks for:
- **NIST Cybersecurity Framework**
- **PCI DSS v4.0**
- **ISO 27001**
- **SOC 2**
- **GDPR**
- **HIPAA** (where applicable)
- **Azure Security Benchmark**

## Usage Instructions
1. Use the function names above to create compliance checks
2. Each function should be implemented as a separate compliance rule
3. Follow the naming convention: `network_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def network_example_function_check():
    """
    Example compliance check for Azure Networking service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.network import NetworkManagementClient
        
        # credential = DefaultAzureCredential()
        # client = NetworkManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in network check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Networking
- **SDK Namespace**: azure.mgmt.network
- **Client Class**: NetworkManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Networking API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
