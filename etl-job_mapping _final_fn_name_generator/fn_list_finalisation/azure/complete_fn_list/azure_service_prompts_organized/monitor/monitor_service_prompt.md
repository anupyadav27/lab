# Azure Azure Monitor Service Compliance Prompt

## Service Information
- **Service Name**: MONITOR
- **Display Name**: Azure Monitor
- **Total Functions**: 51
- **Original Categories**: Compute, Storage, Unknown, Security
- **Categorization Methods**: sdk_example, function_name

## Function List
The following 51 functions are available for Azure Monitor compliance checks:

1. `monitor_diagnostic_setting_exists`
2. `monitor_diagnostic_setting_appropriate_categories`
3. `monitor_activity_log_alert_policy_assignment`
4. `monitor_activity_log_alert_policy_assignment_deletion`
5. `monitor_activity_log_alert_network_security_group_create_update`
6. `monitor_activity_log_alert_delete_network_security_group`
7. `monitor_activity_log_alert_security_solution_create_update`
8. `monitor_activity_log_alert_delete_security_solution`
9. `monitor_alert_sqlserver_firewall_rule_update_create`
10. `monitor_alert_delete_sqlserver_firewall_rule_exists`
11. `monitor_activity_log_alert_public_ip_address_update_create`
12. `monitor_activity_log_alert_delete_public_ip`
13. `monitor_subscription_activity_logs_diagnostic_setting_exists`
14. `monitor_diagnostic_setting_category_capture`
15. `monitor_alert_policy_assignment_existence`
16. `monitor_activity_log_alert_delete_policy_assignment`
17. `monitor_activity_log_alert_create_update_nsg`
18. `monitor_alert_create_update_sqlserver_fr`
19. `monitor_blob_storage_diagnostic_setting_exists`
20. `monitor_alerts_action_group_configured`
21. `monitor_metric_alert_configured_resource`
22. `monitor_storageaccount_diagnosticsetting_blobstorage_events`
23. `monitor_alert_sqlserver_enabled`
24. `monitor_diagnostic_setting_security_best_practices`
25. `monitor_log_analytics_workspace_keyvault_encryption`
26. `activity_logs_keyvault_sse_enabled`
27. `monitor_log_analytics_workspace_retention_greater_than_min_or_365`
28. `virtual_machine_diagnostics_enabled`
29. `virtual_machine_diagnostic_settings_enabled`
30. `monitor_alerts_metric_settings_set`
31. `monitor_alerts_metric_name_settings`
32. `monitor_events_persistence_privilege_elevation`
33. `monitor_alert_threat_intelligence_collection`
34. `monitor_network_system_application_anomalous_behaviour`
35. `azure_info_sys_define_monitor_requirements`
36. `information_system_account_actions_audit_notification`
37. `system_audit_event_capabilities`
38. `information_system_audit_record_generation`
39. `information_system_alert_on_compromise_indicators`
40. `azure_monitor_audit_log_event_details`
41. `azure_monitor_alert_on_audit_log_failure`
42. `azure_monitor_continuous_control_assessment`
43. `azure_monitor_configure_intrusion_detection_alerts`
44. `azure_monitor_audit_logs_enabled`
45. `azure_monitor_user_access_logging_enabled`
46. `azure_monitor_admin_access_logging_enabled`
47. `azure_monitor_audit_log_access_logging_enabled`
48. `azure_monitor_invalid_access_attempts_logging_enabled`
49. `azure_monitor_audit_log_status_changes`
50. `azure_monitor_system_object_changes`
51. `azure_monitor_detailed_audit_event_logging`


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
3. Follow the naming convention: `monitor_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def monitor_example_function_check():
    """
    Example compliance check for Azure Monitor service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.monitor import MonitorManagementClient
        
        # credential = DefaultAzureCredential()
        # client = MonitorManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in monitor check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Monitor
- **SDK Namespace**: azure.mgmt.monitor
- **Client Class**: MonitorManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Monitor API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
