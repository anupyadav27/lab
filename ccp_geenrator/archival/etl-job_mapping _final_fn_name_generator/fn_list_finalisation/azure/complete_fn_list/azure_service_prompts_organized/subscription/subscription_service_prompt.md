# Azure Azure Subscription Service Compliance Prompt

## Service Information
- **Service Name**: SUBSCRIPTION
- **Display Name**: Azure Subscription
- **Total Functions**: 3
- **Original Categories**: Identity
- **Categorization Methods**: sdk_example

## Function List
The following 3 functions are available for Azure Subscription compliance checks:

1. `subscription_aad_directory_permit_no_one`
2. `azure_subscription_root_user_no_access_key`
3. `subscription_root_user_no_access_key`


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
3. Follow the naming convention: `subscription_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def subscription_example_function_check():
    """
    Example compliance check for Azure Subscription service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.subscription import SubscriptionManagementClient
        
        # credential = DefaultAzureCredential()
        # client = SubscriptionManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in subscription check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Subscription
- **SDK Namespace**: azure.mgmt.subscription
- **Client Class**: SubscriptionManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Subscription API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
