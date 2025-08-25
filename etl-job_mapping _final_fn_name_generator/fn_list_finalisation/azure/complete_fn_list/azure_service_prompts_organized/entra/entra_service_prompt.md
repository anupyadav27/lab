# Azure Azure Entra Service Compliance Prompt

## Service Information
- **Service Name**: ENTRA
- **Display Name**: Azure Entra
- **Total Functions**: 2
- **Original Categories**: Identity, Security
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Entra compliance checks:

1. `entra_admin_center_restrict_access`
2. `entra_device_registration_require_mfa`


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
3. Follow the naming convention: `entra_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def entra_example_function_check():
    """
    Example compliance check for Azure Entra service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.entra import EntraManagementClient
        
        # credential = DefaultAzureCredential()
        # client = EntraManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in entra check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Entra
- **SDK Namespace**: azure.mgmt.entra
- **Client Class**: EntraManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Entra API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
