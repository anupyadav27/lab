# Azure Azure Key_Vault Service Compliance Prompt

## Service Information
- **Service Name**: KEY_VAULT
- **Display Name**: Azure Key_Vault
- **Total Functions**: 6
- **Original Categories**: Identity, Security
- **Categorization Methods**: sdk_example

## Function List
The following 6 functions are available for Azure Key_Vault compliance checks:

1. `keyvault_key_rotation_compliance`
2. `keyvault_non_rbac_key_expiration_set`
3. `azure_ad_keyvault_inline_policy_blocked_actions`
4. `keyvault_secret_rotation_frequency_limit`
5. `healthcare_ephi_encryption_decryption`
6. `system_implements_fips_validated_cryptography`


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
3. Follow the naming convention: `key_vault_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def key_vault_example_function_check():
    """
    Example compliance check for Azure Key_Vault service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.key_vault import Key_VaultManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Key_VaultManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in key_vault check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Key_Vault
- **SDK Namespace**: azure.mgmt.key_vault
- **Client Class**: Key_VaultManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Key_Vault API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
