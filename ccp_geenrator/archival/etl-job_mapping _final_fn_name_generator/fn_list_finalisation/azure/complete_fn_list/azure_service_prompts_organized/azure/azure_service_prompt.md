# Azure Azure Azure Service Compliance Prompt

## Service Information
- **Service Name**: AZURE
- **Display Name**: Azure Azure
- **Total Functions**: 5
- **Original Categories**: Identity, Security
- **Categorization Methods**: sdk_example

## Function List
The following 5 functions are available for Azure Azure compliance checks:

1. `azure_rbac_role_assignment_no_inline_permissions`
2. `azure_rbac_role_assignment_no_inline_policy`
3. `azure_rbac_no_inline_policy_in_role_assignment`
4. `azure_rbac_no_inline_policy`
5. `azure_information_processing_facilities_change_management_compliance`


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
3. Follow the naming convention: `azure_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def azure_example_function_check():
    """
    Example compliance check for Azure Azure service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.azure import AzureManagementClient
        
        # credential = DefaultAzureCredential()
        # client = AzureManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in azure check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Azure
- **SDK Namespace**: azure.mgmt.azure
- **Client Class**: AzureManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Azure API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
