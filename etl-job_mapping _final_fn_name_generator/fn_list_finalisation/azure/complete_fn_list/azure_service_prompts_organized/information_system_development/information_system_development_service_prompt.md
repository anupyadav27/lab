# Azure Azure Information_System_Development Service Compliance Prompt

## Service Information
- **Service Name**: INFORMATION_SYSTEM_DEVELOPMENT
- **Display Name**: Azure Information_System_Development
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Information_System_Development compliance checks:

1. `information_system_development_secure_principles_applied`


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
3. Follow the naming convention: `information_system_development_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def information_system_development_example_function_check():
    """
    Example compliance check for Azure Information_System_Development service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.information_system_development import Information_System_DevelopmentManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Information_System_DevelopmentManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in information_system_development check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Information_System_Development
- **SDK Namespace**: azure.mgmt.information_system_development
- **Client Class**: Information_System_DevelopmentManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Information_System_Development API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
