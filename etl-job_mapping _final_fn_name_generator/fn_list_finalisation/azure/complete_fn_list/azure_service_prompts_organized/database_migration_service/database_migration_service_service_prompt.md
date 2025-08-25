# Azure Azure Database_Migration_Service Service Compliance Prompt

## Service Information
- **Service Name**: DATABASE_MIGRATION_SERVICE
- **Display Name**: Azure Database_Migration_Service
- **Total Functions**: 5
- **Original Categories**: Compute, Network
- **Categorization Methods**: sdk_example

## Function List
The following 5 functions are available for Azure Database_Migration_Service compliance checks:

1. `dms_instance_public_access_enabled`
2. `dms_instance_public_access_disabled`
3. `dms_endpoints_ssl_connection_configured`
4. `dms_redis_endpoint_tls_encryption_enabled`
5. `dms_replication_task_logging_severity_enabled`


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
3. Follow the naming convention: `database_migration_service_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def database_migration_service_example_function_check():
    """
    Example compliance check for Azure Database_Migration_Service service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.database_migration_service import Database_Migration_ServiceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Database_Migration_ServiceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in database_migration_service check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Database_Migration_Service
- **SDK Namespace**: azure.mgmt.database_migration_service
- **Client Class**: Database_Migration_ServiceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Database_Migration_Service API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
