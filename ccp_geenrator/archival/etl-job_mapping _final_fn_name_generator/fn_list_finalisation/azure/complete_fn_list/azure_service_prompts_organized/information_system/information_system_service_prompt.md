# Azure Azure Information_System Service Compliance Prompt

## Service Information
- **Service Name**: INFORMATION_SYSTEM
- **Display Name**: Azure Information_System
- **Total Functions**: 8
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 8 functions are available for Azure Information_System compliance checks:

1. `information_system_security_requirements_compliance_correction`
2. `information_system_essential_capabilities_only`
3. `information_system_user_interface_separation`
4. `information_system_prevent_unauthorized_transfer_shared_resources`
5. `information_system_crypto_prevent_unauthorized_disclosure`
6. `information_system_security_event_integrity_monthly`
7. `information_system_handling_retention_compliance`
8. `information_system_configuration_baseline_maintained`


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
3. Follow the naming convention: `information_system_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def information_system_example_function_check():
    """
    Example compliance check for Azure Information_System service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.information_system import Information_SystemManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Information_SystemManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in information_system check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Information_System
- **SDK Namespace**: azure.mgmt.information_system
- **Client Class**: Information_SystemManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Information_System API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
