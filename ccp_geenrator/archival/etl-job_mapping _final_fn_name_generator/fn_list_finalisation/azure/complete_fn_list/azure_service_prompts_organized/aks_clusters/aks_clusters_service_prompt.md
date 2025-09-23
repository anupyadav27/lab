# Azure Azure Aks_Clusters Service Compliance Prompt

## Service Information
- **Service Name**: AKS_CLUSTERS
- **Display Name**: Azure Aks_Clusters
- **Total Functions**: 2
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Aks_Clusters compliance checks:

1. `aks_apiserver_public_access_disabled`
2. `aks_clusters_secrets_encryption_keyvault_cmk`


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
3. Follow the naming convention: `aks_clusters_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def aks_clusters_example_function_check():
    """
    Example compliance check for Azure Aks_Clusters service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.aks_clusters import Aks_ClustersManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Aks_ClustersManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in aks_clusters check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Aks_Clusters
- **SDK Namespace**: azure.mgmt.aks_clusters
- **Client Class**: Aks_ClustersManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Aks_Clusters API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
