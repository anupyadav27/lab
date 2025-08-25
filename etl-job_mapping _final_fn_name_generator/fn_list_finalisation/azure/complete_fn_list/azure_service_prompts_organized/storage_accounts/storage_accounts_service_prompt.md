# Azure Azure Storage_Accounts Service Compliance Prompt

## Service Information
- **Service Name**: STORAGE_ACCOUNTS
- **Display Name**: Azure Storage_Accounts
- **Total Functions**: 1
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Storage_Accounts compliance checks:

1. `storage_account_enable_key_rotation_reminders`


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
3. Follow the naming convention: `storage_accounts_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def storage_accounts_example_function_check():
    """
    Example compliance check for Azure Storage_Accounts service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.storage_accounts import Storage_AccountsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Storage_AccountsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in storage_accounts check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Storage_Accounts
- **SDK Namespace**: azure.mgmt.storage_accounts
- **Client Class**: Storage_AccountsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Storage_Accounts API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
