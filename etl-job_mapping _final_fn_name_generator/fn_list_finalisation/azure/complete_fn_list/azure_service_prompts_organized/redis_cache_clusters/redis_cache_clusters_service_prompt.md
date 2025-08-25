# Azure Azure Redis_Cache_Clusters Service Compliance Prompt

## Service Information
- **Service Name**: REDIS_CACHE_CLUSTERS
- **Display Name**: Azure Redis_Cache_Clusters
- **Total Functions**: 2
- **Original Categories**: Compute, Storage
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Redis_Cache_Clusters compliance checks:

1. `redis_cache_cluster_encryption_enabled`
2. `redis_cache_cluster_auto_minor_version_upgrade_enabled`


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
3. Follow the naming convention: `redis_cache_clusters_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def redis_cache_clusters_example_function_check():
    """
    Example compliance check for Azure Redis_Cache_Clusters service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.redis_cache_clusters import Redis_Cache_ClustersManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Redis_Cache_ClustersManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in redis_cache_clusters check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Redis_Cache_Clusters
- **SDK Namespace**: azure.mgmt.redis_cache_clusters
- **Client Class**: Redis_Cache_ClustersManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Redis_Cache_Clusters API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
