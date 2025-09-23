# Azure Azure Container_Registry Service Compliance Prompt

## Service Information
- **Service Name**: CONTAINER_REGISTRY
- **Display Name**: Azure Container_Registry
- **Total Functions**: 1
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Container_Registry compliance checks:

1. `acr_repository_scan_on_push_or_continuous`


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
3. Follow the naming convention: `container_registry_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def container_registry_example_function_check():
    """
    Example compliance check for Azure Container_Registry service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.container_registry import Container_RegistryManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Container_RegistryManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in container_registry check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Container_Registry
- **SDK Namespace**: azure.mgmt.container_registry
- **Client Class**: Container_RegistryManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Container_Registry API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
