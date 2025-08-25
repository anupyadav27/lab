# Azure Azure Sql_Pools Service Compliance Prompt

## Service Information
- **Service Name**: SQL_POOLS
- **Display Name**: Azure Sql_Pools
- **Total Functions**: 1
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Sql_Pools compliance checks:

1. `synapse_analytics_sql_pool_snapshot_retention_within_limit`


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
3. Follow the naming convention: `sql_pools_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def sql_pools_example_function_check():
    """
    Example compliance check for Azure Sql_Pools service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.sql_pools import Sql_PoolsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Sql_PoolsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in sql_pools check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Sql_Pools
- **SDK Namespace**: azure.mgmt.sql_pools
- **Client Class**: Sql_PoolsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Sql_Pools API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
