# Azure Azure Database Services Service Compliance Prompt

## Service Information
- **Service Name**: DATABASE_SERVICES
- **Display Name**: Azure Database Services
- **Total Functions**: 7
- **Original Categories**: Identity, Security, Unknown, Network
- **Categorization Methods**: sdk_example, function_name

## Function List
The following 7 functions are available for Azure Database Services compliance checks:

1. `database_firewall_custom_unrestricted_access`
2. `database_instance_public_access_disabled`
3. `database_instance_public_network_access_disabled`
4. `database_postgresql_mysql_aad_authentication_enabled`
5. `azure_sql_data_mining_prevention`
6. `azure_sql_database_data_encryption_verification`
7. `azure_sql_sensitive_data_retention_check`


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
3. Follow the naming convention: `database_services_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def database_services_example_function_check():
    """
    Example compliance check for Azure Database Services service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.database_services import Database_ServicesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Database_ServicesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in database_services check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Database Services
- **SDK Namespace**: azure.mgmt.database_services
- **Client Class**: Database_ServicesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Database Services API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
