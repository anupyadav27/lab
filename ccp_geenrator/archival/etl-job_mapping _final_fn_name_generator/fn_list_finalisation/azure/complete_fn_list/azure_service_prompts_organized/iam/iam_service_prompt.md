# Azure Azure Iam Service Compliance Prompt

## Service Information
- **Service Name**: IAM
- **Display Name**: Azure Iam
- **Total Functions**: 4
- **Original Categories**: Identity
- **Categorization Methods**: sdk_example

## Function List
The following 4 functions are available for Azure Iam compliance checks:

1. `iam_subscription_roles_no_custom_admin`
2. `iam_subscription_roles_owner_custom_has_resource_lock_permissions`
3. `iam_custom_role_resource_lock_admin_permissions`
4. `iam_user_registration_minimum_access_rights`


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
3. Follow the naming convention: `iam_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def iam_example_function_check():
    """
    Example compliance check for Azure Iam service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.iam import IamManagementClient
        
        # credential = DefaultAzureCredential()
        # client = IamManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in iam check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Iam
- **SDK Namespace**: azure.mgmt.iam
- **Client Class**: IamManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Iam API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
