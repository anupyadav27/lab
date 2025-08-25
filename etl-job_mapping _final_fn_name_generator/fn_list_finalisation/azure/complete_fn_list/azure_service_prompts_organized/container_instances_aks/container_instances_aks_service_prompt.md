# Azure Azure Container_Instances_Aks Service Compliance Prompt

## Service Information
- **Service Name**: CONTAINER_INSTANCES_AKS
- **Display Name**: Azure Container_Instances_Aks
- **Total Functions**: 2
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Container_Instances_Aks compliance checks:

1. `container_instances_aks_no_secrets_as_env_vars`
2. `container_instances_aks_no_secrets_in_env_vars`


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
3. Follow the naming convention: `container_instances_aks_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def container_instances_aks_example_function_check():
    """
    Example compliance check for Azure Container_Instances_Aks service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.container_instances_aks import Container_Instances_AksManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Container_Instances_AksManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in container_instances_aks check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Container_Instances_Aks
- **SDK Namespace**: azure.mgmt.container_instances_aks
- **Client Class**: Container_Instances_AksManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Container_Instances_Aks API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
