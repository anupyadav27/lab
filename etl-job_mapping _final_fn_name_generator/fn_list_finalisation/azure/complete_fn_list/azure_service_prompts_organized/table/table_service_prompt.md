# Azure Azure Table Service Compliance Prompt

## Service Information
- **Service Name**: TABLE
- **Display Name**: Azure Table
- **Total Functions**: 2
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Table compliance checks:

1. `cosmosdb_table_encryption_status_enabled`
2. `cosmosdb_table_encryption_enabled`


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
3. Follow the naming convention: `table_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def table_example_function_check():
    """
    Example compliance check for Azure Table service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.table import TableManagementClient
        
        # credential = DefaultAzureCredential()
        # client = TableManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in table check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Table
- **SDK Namespace**: azure.mgmt.table
- **Client Class**: TableManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Table API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
