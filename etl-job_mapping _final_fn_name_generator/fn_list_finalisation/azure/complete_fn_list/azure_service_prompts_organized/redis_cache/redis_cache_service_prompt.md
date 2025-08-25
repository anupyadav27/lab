# Azure Azure Redis_Cache Service Compliance Prompt

## Service Information
- **Service Name**: REDIS_CACHE
- **Display Name**: Azure Redis_Cache
- **Total Functions**: 7
- **Original Categories**: Storage, Network
- **Categorization Methods**: sdk_example

## Function List
The following 7 functions are available for Azure Redis_Cache compliance checks:

1. `redis_cache_custom_vnet_integration`
2. `redis_cache_instance_custom_vnet_integration`
3. `redis_cache_backup_retention_greater_than_required`
4. `redis_cache_replication_groups_non_ssl_port_disabled`
5. `redis_cache_replication_groups_encryption_at_rest_enabled`
6. `redis_cache_replication_groups_encryption_at_rest_enabled_and_key_vault_key_match`
7. `redis_cache_replication_group_non_ssl_port_disabled`


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
3. Follow the naming convention: `redis_cache_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def redis_cache_example_function_check():
    """
    Example compliance check for Azure Redis_Cache service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.redis_cache import Redis_CacheManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Redis_CacheManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in redis_cache check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Redis_Cache
- **SDK Namespace**: azure.mgmt.redis_cache
- **Client Class**: Redis_CacheManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Redis_Cache API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
