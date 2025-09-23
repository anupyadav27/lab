# Azure Azure Backup_Plan Service Compliance Prompt

## Service Information
- **Service Name**: BACKUP_PLAN
- **Display Name**: Azure Backup_Plan
- **Total Functions**: 1
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Backup_Plan compliance checks:

1. `cosmosdb_table_backup_plan_inclusion`


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
3. Follow the naming convention: `backup_plan_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def backup_plan_example_function_check():
    """
    Example compliance check for Azure Backup_Plan service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.backup_plan import Backup_PlanManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Backup_PlanManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in backup_plan check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Backup_Plan
- **SDK Namespace**: azure.mgmt.backup_plan
- **Client Class**: Backup_PlanManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Backup_Plan API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
