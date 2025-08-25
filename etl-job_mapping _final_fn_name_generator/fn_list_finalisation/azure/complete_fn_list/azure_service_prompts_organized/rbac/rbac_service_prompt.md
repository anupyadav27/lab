# Azure Azure Rbac Service Compliance Prompt

## Service Information
- **Service Name**: RBAC
- **Display Name**: Azure Rbac
- **Total Functions**: 8
- **Original Categories**: Identity
- **Categorization Methods**: sdk_example

## Function List
The following 8 functions are available for Azure Rbac compliance checks:

1. `rbac_assignment_has_specific_role_definition`
2. `rbac_custom_roles_assigned_to_ad_role`
3. `rbac_role_definition_unrestricted_permissions`
4. `rbac_role_assignment_no_inline_policy`
5. `rbac_assignment_has_specific_role`
6. `rbac_role_unrestricted_permissions`
7. `rbac_assignment_role_definition_non_compliant`
8. `rbac_role_assignment_unauthorized_entity`


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
3. Follow the naming convention: `rbac_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def rbac_example_function_check():
    """
    Example compliance check for Azure Rbac service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.rbac import RbacManagementClient
        
        # credential = DefaultAzureCredential()
        # client = RbacManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in rbac check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Rbac
- **SDK Namespace**: azure.mgmt.rbac
- **Client Class**: RbacManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Rbac API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
