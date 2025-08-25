# Azure Azure Dms Service Compliance Prompt

## Service Information
- **Service Name**: DMS
- **Display Name**: Azure Dms
- **Total Functions**: 2
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Dms compliance checks:

1. `dms_replication_task_events_logging_enabled_with_valid_severity`
2. `dms_replication_task_events_logging_severity_is_valid`


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
3. Follow the naming convention: `dms_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def dms_example_function_check():
    """
    Example compliance check for Azure Dms service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.dms import DmsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = DmsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in dms check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Dms
- **SDK Namespace**: azure.mgmt.dms
- **Client Class**: DmsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Dms API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
