# Azure Azure Defender Service Compliance Prompt

## Service Information
- **Service Name**: DEFENDER
- **Display Name**: Azure Defender
- **Total Functions**: 20
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 20 functions are available for Azure Defender compliance checks:

1. `defender_servers_on_state`
2. `defender_databases_set_on`
3. `defender_sql_servers_on_machines_status`
4. `defender_open_source_relational_databases_enabled`
5. `defender_dns_on_state`
6. `defender_resource_manager_is_on`
7. `defender_recommendation_system_updates_completed`
8. `defender_log_analytics_agent_vms_auto_provisioning_on`
9. `defender_auto_provisioning_vulnerability_assessment_machines_on`
10. `defender_containers_components_auto_provisioning_on`
11. `defender_security_contact_additional_email_configured`
12. `defender_cloud_apps_integration_status`
13. `defender_endpoint_integration_with_defender_cloud_selected`
14. `defender_servers_set_on`
15. `defender_sql_databases_managed_instance_on_state`
16. `defender_sql_server_machines_on`
17. `defender_vulnerability_assessment_machines_auto_provisioning_on`
18. `defender_cloud_apps_integration_selected`
19. `defender_endpoint_integration_with_cloud_selected`
20. `defender_coopted_systems_availability_prevention`


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
3. Follow the naming convention: `defender_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def defender_example_function_check():
    """
    Example compliance check for Azure Defender service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.defender import DefenderManagementClient
        
        # credential = DefaultAzureCredential()
        # client = DefenderManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in defender check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Defender
- **SDK Namespace**: azure.mgmt.defender
- **Client Class**: DefenderManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Defender API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
