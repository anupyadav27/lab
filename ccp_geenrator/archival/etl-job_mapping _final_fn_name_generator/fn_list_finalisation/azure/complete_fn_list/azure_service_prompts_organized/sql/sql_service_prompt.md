# Azure Azure Sql Service Compliance Prompt

## Service Information
- **Service Name**: SQL
- **Display Name**: Azure Sql
- **Total Functions**: 26
- **Original Categories**: Identity, Storage, Security, Network
- **Categorization Methods**: sdk_example

## Function List
The following 26 functions are available for Azure Sql compliance checks:

1. `sql_database_no_any_ip_ingress`
2. `sql_server_tde_protector_encrypted_with_cmk`
3. `sql_server_azuread_admin_configured`
4. `sql_database_data_encryption_on`
5. `sql_server_vulnerability_assessment_storage_account_set`
6. `sqlserver_vulnerabilityassessment_periodic_recurring_scans_on`
7. `sqlserver_vulnerability_assessment_scan_reports_configured`
8. `sqlserver_vulnerabilityassessment_email_notifications_admins_set`
9. `sql_server_tde_protector_encryption_cmk`
10. `sql_database_monitor_logs_enabled`
11. `sql_database_backup_not_public`
12. `sql_database_cluster_automatic_backup_policy_protected`
13. `sql_database_backup_enabled_retention_period_window`
14. `azure_sql_database_in_backup_policy`
15. `sql_managed_instance_backup_policy_inclusion`
16. `sql_database_encryption_at_rest_enabled`
17. `sql_database_backup_encryption_enabled`
18. `sql_database_storage_encryption_enabled`
19. `sql_database_auto_minor_version_upgrade_enabled`
20. `sql_database_managed_instance_aad_authentication_enabled`
21. `sql_database_aad_authentication_enabled`
22. `sql_database_encrypted_at_rest`
23. `sql_database_data_masking_compliance_with_policy_and_business_reqs`
24. `sql_database_table_info_access_control_policies`
25. `sqlserver_auditing_on`
26. `monitor_alert_sqlserver_enabled`


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
3. Follow the naming convention: `sql_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def sql_example_function_check():
    """
    Example compliance check for Azure Sql service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.sql import SqlManagementClient
        
        # credential = DefaultAzureCredential()
        # client = SqlManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in sql check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Sql
- **SDK Namespace**: azure.mgmt.sql
- **Client Class**: SqlManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Sql API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
