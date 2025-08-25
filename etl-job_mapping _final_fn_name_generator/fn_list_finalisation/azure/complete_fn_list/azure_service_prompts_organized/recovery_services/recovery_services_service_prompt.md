# Azure Azure Recovery_Services Service Compliance Prompt

## Service Information
- **Service Name**: RECOVERY_SERVICES
- **Display Name**: Azure Recovery_Services
- **Total Functions**: 4
- **Original Categories**: Storage, Security
- **Categorization Methods**: sdk_example

## Function List
The following 4 functions are available for Azure Recovery_Services compliance checks:

1. `azure_recovery_services_vault_disaster_recovery_plan`
2. `disaster_recovery_strategy_plan_test_supplement`
3. `azure_recovery_system_state_reconstitution`
4. `information_system_recovery_state`


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
3. Follow the naming convention: `recovery_services_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def recovery_services_example_function_check():
    """
    Example compliance check for Azure Recovery_Services service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.recovery_services import Recovery_ServicesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Recovery_ServicesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in recovery_services check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Recovery_Services
- **SDK Namespace**: azure.mgmt.recovery_services
- **Client Class**: Recovery_ServicesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Recovery_Services API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
