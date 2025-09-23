# Azure Azure Sql_Servers Service Compliance Prompt

## Service Information
- **Service Name**: SQL_SERVERS
- **Display Name**: Azure Sql_Servers
- **Total Functions**: 2
- **Original Categories**: Identity, Security
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Sql_Servers compliance checks:

1. `sql_server_defender_on_for_critical_servers`
2. `sqlserver_azuread_authentication_configured`


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
3. Follow the naming convention: `sql_servers_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def sql_servers_example_function_check():
    """
    Example compliance check for Azure Sql_Servers service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.sql_servers import Sql_ServersManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Sql_ServersManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in sql_servers check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Sql_Servers
- **SDK Namespace**: azure.mgmt.sql_servers
- **Client Class**: Sql_ServersManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Sql_Servers API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
