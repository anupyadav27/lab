# Azure Azure Registries Service Compliance Prompt

## Service Information
- **Service Name**: REGISTRIES
- **Display Name**: Azure Registries
- **Total Functions**: 2
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Registries compliance checks:

1. `acr_private_repository_lifecycle_policy_presence`
2. `acr_repository_lifecycle_policy_presence`


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
3. Follow the naming convention: `registries_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def registries_example_function_check():
    """
    Example compliance check for Azure Registries service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.registries import RegistriesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = RegistriesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in registries check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Registries
- **SDK Namespace**: azure.mgmt.registries
- **Client Class**: RegistriesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Registries API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
