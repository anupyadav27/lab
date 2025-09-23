# Azure Azure Keyvault Service Compliance Prompt

## Service Information
- **Service Name**: KEYVAULT
- **Display Name**: Azure Keyvault
- **Total Functions**: 17
- **Original Categories**: Identity, Security
- **Categorization Methods**: sdk_example

## Function List
The following 17 functions are available for Azure Keyvault compliance checks:

1. `defender_keyvault_enabled`
2. `keyvault_private_endpoint_used`
3. `azure_keyvault_rbac_enabled`
4. `keyvault_managed_ca_root_ca_disabled`
5. `keyvault_key_rbac_blocked_actions`
6. `keyvault_key_not_scheduled_for_deletion`
7. `keyvault_key_rbac_no_blocked_actions`
8. `keyvault_key_ml_endpoint_configuration`
9. `keyvault_ml_notebook_instance_keyvaultkeyid_specified`
10. `keyvault_key_rbac_blocked_actions_disallowed`
11. `keyvault_managed_ca_disabled_root_ca_status`
12. `keyvault_secret_rotation_frequency`
13. `keyvault_secret_unused_days`
14. `keyvault_key_ml_endpoint_configuration_exists`
15. `keyvault_ml_notebook_keyvaultkeyid_specified`
16. `keyvault_personal_information_handling_minimized_key_personnel`
17. `keyvault_ephi_encryption_enabled`


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
3. Follow the naming convention: `keyvault_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def keyvault_example_function_check():
    """
    Example compliance check for Azure Keyvault service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.keyvault import KeyvaultManagementClient
        
        # credential = DefaultAzureCredential()
        # client = KeyvaultManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in keyvault check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Keyvault
- **SDK Namespace**: azure.mgmt.keyvault
- **Client Class**: KeyvaultManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Keyvault API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
