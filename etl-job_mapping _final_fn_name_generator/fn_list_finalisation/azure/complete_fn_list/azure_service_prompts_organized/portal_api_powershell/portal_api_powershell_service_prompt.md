# Azure Azure Portal API PowerShell Service Compliance Prompt

## Service Information
- **Service Name**: PORTAL_API_POWERSHELL
- **Display Name**: Azure Portal API PowerShell
- **Total Functions**: 1
- **Original Categories**: Identity
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Portal API PowerShell compliance checks:

1. `azure_portal_api_powershell_microsoft_365_groups_creation_disabled`


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
3. Follow the naming convention: `portal_api_powershell_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def portal_api_powershell_example_function_check():
    """
    Example compliance check for Azure Portal API PowerShell service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.portal_api_powershell import Portal_Api_PowershellManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Portal_Api_PowershellManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in portal_api_powershell check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Portal API PowerShell
- **SDK Namespace**: azure.mgmt.portal_api_powershell
- **Client Class**: Portal_Api_PowershellManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Portal API PowerShell API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
