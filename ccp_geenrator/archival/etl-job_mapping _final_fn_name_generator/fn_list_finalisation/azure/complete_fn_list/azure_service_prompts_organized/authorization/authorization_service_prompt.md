# Azure Azure Authorization Service Compliance Prompt

## Service Information
- **Service Name**: AUTHORIZATION
- **Display Name**: Azure Authorization
- **Total Functions**: 5
- **Original Categories**: Identity
- **Categorization Methods**: sdk_example

## Function List
The following 5 functions are available for Azure Authorization compliance checks:

1. `rbac_custom_roles_grant_all_actions`
2. `rbac_role_assignment_to_unauthorized_entity`
3. `rbac_custom_role_grant_all_actions`
4. `azure_rbac_role_assignment_unauthorized_entity`
5. `rbac_custom_role_full_access`


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
3. Follow the naming convention: `authorization_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def authorization_example_function_check():
    """
    Example compliance check for Azure Authorization service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.authorization import AuthorizationManagementClient
        
        # credential = DefaultAzureCredential()
        # client = AuthorizationManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in authorization check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Authorization
- **SDK Namespace**: azure.mgmt.authorization
- **Client Class**: AuthorizationManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Authorization API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
