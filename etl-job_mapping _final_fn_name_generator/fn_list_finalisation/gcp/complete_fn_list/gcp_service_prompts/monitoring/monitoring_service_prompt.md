# GCP MONITORING Service Compliance Prompt

## Service Information
- **Service Name**: MONITORING
- **Description**: GCP MONITORING Service
- **Total Functions**: 35
- **SDK Client**: monitoring_client
- **Service Type**: monitoring

## Function List
The following 35 functions are available for MONITORING compliance checks:

1. `security_cloud_armor_metrics_enabled`
2. `security_supplier_practices_monitoring`
3. `security_command_center_premises_unauthorized_access_monitoring`
4. `security_command_center_physical_access_monitoring`
5. `security_command_center_vulnerability_monitoring`
6. `security_posture_dashboard_enabled`
7. `monitoring_cloud_armor_security_metrics_enabled`
8. `security_dashboard_reviewed_regularly`
9. `logging_metric_filter_alerts_project_ownership_changes`
10. `logging_project_ownership_change_alert`
11. `logging_project_ownership_metric_filter_alerts_exist`
12. `monitoring_alerts_metric_settings_compliance`
13. `alert_config_government_backed_attacks`
14. `gmail_alert_on_employee_spoofing`
15. `monitoring_system_capacity_forecast`
16. `monitoring_alerts_action_configured`
17. `monitoring_cloud_armor_logging_enabled`
18. `monitoring_cloud_armor_metrics_enabled`
19. `monitoring_resource_metric_alert_exists`
20. `monitoring_alerts_metric_settings`
21. `monitoring_alerts_notification_channels_configured`
22. `monitoring_resource_metric_alert`
23. `monitoring_resources_capacity_alignment`
24. `monitoring_systems_anomalous_behaviour_detection`
25. `monitoring_resources_capacity_management`
26. `monitoring_continuous_monitoring_ens`
27. `logging_audit_config_changes_alerts_exist`
28. `monitoring_systems_performance_capacity_requirements`
29. `monitoring_continuous_monitoring_strategy_implementation`
30. `monitoring_system_information_correlation`
31. `monitoring_alerts_compromise_indicators`
32. `monitoring_system_attack_detection`
33. `monitoring_configuration_management_continuous_monitoring`
34. `logging_login_attempts_monitoring`
35. `certificate_manager_certificates_expiration_monitor`


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
3. Follow the naming convention: `monitoring_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def monitoring_example_function_check():
    """
    Example compliance check for MONITORING service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in monitoring check: {e}")
        return False
```

## Notes
- All functions are based on GCP MONITORING API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
