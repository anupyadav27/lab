# Azure Azure Vaults Service Compliance Prompt

## Service Information
- **Service Name**: VAULTS
- **Display Name**: Azure Vaults
- **Total Functions**: 3
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 3 functions are available for Azure Vaults compliance checks:

1. `keyvault_logging_enabled_state`
2. `keyvault_vault_is_recoverable`
3. `keyvault_supported_services_auto_key_rotation_enabled`


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
3. Follow the naming convention: `vaults_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def vaults_example_function_check():
    """
    Example compliance check for Azure Vaults service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.vaults import VaultsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = VaultsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in vaults check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Vaults
- **SDK Namespace**: azure.mgmt.vaults
- **Client Class**: VaultsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Vaults API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
