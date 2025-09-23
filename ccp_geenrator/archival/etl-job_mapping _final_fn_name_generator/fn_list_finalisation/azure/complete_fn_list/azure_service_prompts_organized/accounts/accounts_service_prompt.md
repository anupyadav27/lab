# Azure Azure Accounts Service Compliance Prompt

## Service Information
- **Service Name**: ACCOUNTS
- **Display Name**: Azure Accounts
- **Total Functions**: 2
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Accounts compliance checks:

1. `purview_account_automated_sensitive_data_discovery_enabled_administrator`
2. `purview_account_status_enabled_per_region`


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
3. Follow the naming convention: `accounts_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def accounts_example_function_check():
    """
    Example compliance check for Azure Accounts service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.accounts import AccountsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = AccountsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in accounts check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Accounts
- **SDK Namespace**: azure.mgmt.accounts
- **Client Class**: AccountsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Accounts API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
