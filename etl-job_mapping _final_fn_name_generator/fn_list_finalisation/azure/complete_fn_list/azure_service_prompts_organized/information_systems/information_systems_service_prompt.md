# Azure Azure Information_Systems Service Compliance Prompt

## Service Information
- **Service Name**: INFORMATION_SYSTEMS
- **Display Name**: Azure Information_Systems
- **Total Functions**: 2
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Information_Systems compliance checks:

1. `information_systems_security_requirements_applied`
2. `information_systems_assets_change_management_impact_analysis`


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
3. Follow the naming convention: `information_systems_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def information_systems_example_function_check():
    """
    Example compliance check for Azure Information_Systems service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.information_systems import Information_SystemsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Information_SystemsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in information_systems check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Information_Systems
- **SDK Namespace**: azure.mgmt.information_systems
- **Client Class**: Information_SystemsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Information_Systems API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
