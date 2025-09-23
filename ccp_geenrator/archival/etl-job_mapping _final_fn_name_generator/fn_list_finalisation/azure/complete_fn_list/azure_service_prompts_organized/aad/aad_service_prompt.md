# Azure Azure Aad Service Compliance Prompt

## Service Information
- **Service Name**: AAD
- **Display Name**: Azure Aad
- **Total Functions**: 6
- **Original Categories**: Identity
- **Categorization Methods**: sdk_example

## Function List
The following 6 functions are available for Azure Aad compliance checks:

1. `aad_cosmosdb_account_rbac_authentication`
2. `aad_user_membership_in_ad_group`
3. `aad_user_group_membership`
4. `aad_user_no_direct_roles_or_permissions`
5. `aad_user_membership_status`
6. `aad_global_administrator_mfa_required`


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
3. Follow the naming convention: `aad_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def aad_example_function_check():
    """
    Example compliance check for Azure Aad service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.aad import AadManagementClient
        
        # credential = DefaultAzureCredential()
        # client = AadManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in aad check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Aad
- **SDK Namespace**: azure.mgmt.aad
- **Client Class**: AadManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Aad API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
