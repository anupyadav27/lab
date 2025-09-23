# Azure Azure Synapse_Analytics Service Compliance Prompt

## Service Information
- **Service Name**: SYNAPSE_ANALYTICS
- **Display Name**: Azure Synapse_Analytics
- **Total Functions**: 7
- **Original Categories**: Storage, Security, Network
- **Categorization Methods**: sdk_example

## Function List
The following 7 functions are available for Azure Synapse_Analytics compliance checks:

1. `synapse_analytics_dedicated_sql_pools_public_network_access_disabled`
2. `synapse_analytics_sql_pool_private_link_enabled`
3. `synapse_analytics_sql_pool_public_network_access_disabled`
4. `synapse_analytics_audit_logging_storage_account_match`
5. `synapse_analytics_encryption_audit_logging_enabled`
6. `synapse_analytics_cluster_encryption_with_specific_keyvault_key`
7. `synapse_analytics_cluster_encrypted_with_specific_keyvault_key`


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
3. Follow the naming convention: `synapse_analytics_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def synapse_analytics_example_function_check():
    """
    Example compliance check for Azure Synapse_Analytics service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.synapse_analytics import Synapse_AnalyticsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Synapse_AnalyticsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in synapse_analytics check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Synapse_Analytics
- **SDK Namespace**: azure.mgmt.synapse_analytics
- **Client Class**: Synapse_AnalyticsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Synapse_Analytics API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
