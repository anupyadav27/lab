# Azure Azure Functionapp Service Compliance Prompt

## Service Information
- **Service Name**: FUNCTIONAPP
- **Display Name**: Azure Functionapp
- **Total Functions**: 2
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Functionapp compliance checks:

1. `functionapp_settings_match_expected`
2. `functionapp_policy_prohibit_public_access_with_private_endpoints_or_access_restrictions`


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
3. Follow the naming convention: `functionapp_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def functionapp_example_function_check():
    """
    Example compliance check for Azure Functionapp service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.functionapp import FunctionappManagementClient
        
        # credential = DefaultAzureCredential()
        # client = FunctionappManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in functionapp check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Functionapp
- **SDK Namespace**: azure.mgmt.functionapp
- **Client Class**: FunctionappManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Functionapp API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
