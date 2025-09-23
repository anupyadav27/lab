# Azure Azure Sqlserver Service Compliance Prompt

## Service Information
- **Service Name**: SQLSERVER
- **Display Name**: Azure Sqlserver
- **Total Functions**: 2
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Sqlserver compliance checks:

1. `sqlserver_auditing_on`
2. `sqlserver_auditing_retention_greater_than_90_days`


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
3. Follow the naming convention: `sqlserver_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def sqlserver_example_function_check():
    """
    Example compliance check for Azure Sqlserver service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.sqlserver import SqlserverManagementClient
        
        # credential = DefaultAzureCredential()
        # client = SqlserverManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in sqlserver check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Sqlserver
- **SDK Namespace**: azure.mgmt.sqlserver
- **Client Class**: SqlserverManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Sqlserver API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
