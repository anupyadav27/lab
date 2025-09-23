# Azure Azure Postgresql Service Compliance Prompt

## Service Information
- **Service Name**: POSTGRESQL
- **Display Name**: Azure Postgresql
- **Total Functions**: 8
- **Original Categories**: Compute, Storage, Network
- **Categorization Methods**: sdk_example

## Function List
The following 8 functions are available for Azure Postgresql compliance checks:

1. `postgresql_database_server_enforce_ssl_enabled`
2. `postgresql_database_server_log_checkpoints_on`
3. `postgresql_database_server_log_connections_on`
4. `postgresql_database_server_log_disconnections_on`
5. `postgresql_database_server_connection_throttling_on`
6. `postgresql_database_server_log_retention_days_greater_than_three`
7. `postgresql_database_server_disallow_azure_services_access`
8. `postgresql_database_server_enable_infrastructure_double_encryption`


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
3. Follow the naming convention: `postgresql_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def postgresql_example_function_check():
    """
    Example compliance check for Azure Postgresql service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.postgresql import PostgresqlManagementClient
        
        # credential = DefaultAzureCredential()
        # client = PostgresqlManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in postgresql check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Postgresql
- **SDK Namespace**: azure.mgmt.postgresql
- **Client Class**: PostgresqlManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Postgresql API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
