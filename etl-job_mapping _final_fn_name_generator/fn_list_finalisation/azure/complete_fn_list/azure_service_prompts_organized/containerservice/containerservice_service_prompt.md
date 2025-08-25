# Azure Azure Containerservice Service Compliance Prompt

## Service Information
- **Service Name**: CONTAINERSERVICE
- **Display Name**: Azure Containerservice
- **Total Functions**: 8
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 8 functions are available for Azure Containerservice compliance checks:

1. `aks_cluster_logging_enabled`
2. `aks_container_readonly_root_filesystem`
3. `aks_container_read_only_root_filesystem`
4. `aks_cluster_oldest_supported_version`
5. `aks_cluster_supported_version`
6. `aks_pod_non_root_user`
7. `aks_podspec_privileged_false`
8. `aks_pods_non_root_user`


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
3. Follow the naming convention: `containerservice_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def containerservice_example_function_check():
    """
    Example compliance check for Azure Containerservice service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.containerservice import ContainerserviceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = ContainerserviceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in containerservice check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Containerservice
- **SDK Namespace**: azure.mgmt.containerservice
- **Client Class**: ContainerserviceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Containerservice API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
