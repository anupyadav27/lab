# Azure Azure Keys Service Compliance Prompt

## Service Information
- **Service Name**: KEYS
- **Display Name**: Azure Keys
- **Total Functions**: 4
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 4 functions are available for Azure Keys compliance checks:

1. `keyvault_rbac_key_has_expiration`
2. `keyvault_rbac_key_expiration_set`
3. `keyvault_cryptographic_keys_secure_management`
4. `keyvault_cryptographic_keys_managed_in_line_with_org_requirements`


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
3. Follow the naming convention: `keys_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def keys_example_function_check():
    """
    Example compliance check for Azure Keys service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.keys import KeysManagementClient
        
        # credential = DefaultAzureCredential()
        # client = KeysManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in keys check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Keys
- **SDK Namespace**: azure.mgmt.keys
- **Client Class**: KeysManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Keys API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
