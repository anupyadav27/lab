# Azure Azure Account Service Compliance Prompt

## Service Information
- **Service Name**: ACCOUNT
- **Display Name**: Azure Account
- **Total Functions**: 1
- **Original Categories**: Identity
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Account compliance checks:

1. `azure_account_mfa_hardware_device_global_admin`


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
3. Follow the naming convention: `account_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def account_example_function_check():
    """
    Example compliance check for Azure Account service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.account import AccountManagementClient
        
        # credential = DefaultAzureCredential()
        # client = AccountManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in account check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Account
- **SDK Namespace**: azure.mgmt.account
- **Client Class**: AccountManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Account API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
