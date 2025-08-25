# Azure Azure Cosmosdb Service Compliance Prompt

## Service Information
- **Service Name**: COSMOSDB
- **Display Name**: Azure Cosmosdb
- **Total Functions**: 16
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 16 functions are available for Azure Cosmosdb compliance checks:

1. `cosmosdb_manualbackup_public_accessibility`
2. `cosmosdb_backup_public_accessibility`
3. `cosmosdb_cluster_monitor_log_export_enabled`
4. `cosmosdb_mongodb_cluster_diagnostic_settings_audit_logs`
5. `cosmosdb_cluster_audit_log_export_enabled`
6. `cosmosdb_mongodb_cluster_diagnostic_settings_audit_logs_enabled`
7. `cosmosdb_snapshot_public_access`
8. `cosmosdb_table_backup_plan_coverage`
9. `cosmosdb_cluster_retention_period_minimum_days`
10. `cosmosdb_accelerator_cluster_tls_encryption`
11. `cosmosdb_table_pitr_enabled`
12. `cosmosdb_mongodb_api_storage_encryption_enabled`
13. `cosmosdb_table_encryption_with_managed_hsm_key_presence`
14. `cosmosdb_sql_database_storage_encryption_enabled`
15. `cosmosdb_cluster_automatic_backups_encrypted`
16. `cosmosdb_cluster_azure_monitor_log_export_enabled`


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
3. Follow the naming convention: `cosmosdb_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def cosmosdb_example_function_check():
    """
    Example compliance check for Azure Cosmosdb service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.cosmosdb import CosmosdbManagementClient
        
        # credential = DefaultAzureCredential()
        # client = CosmosdbManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in cosmosdb check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Cosmosdb
- **SDK Namespace**: azure.mgmt.cosmosdb
- **Client Class**: CosmosdbManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Cosmosdb API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
