# Azure Azure Resource_Locks Service Compliance Prompt

## Service Information
- **Service Name**: RESOURCE_LOCKS
- **Display Name**: Azure Resource_Locks
- **Total Functions**: 2
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Resource_Locks compliance checks:

1. `azure_resourcelocks_mission_critical_set`
2. `azure_resourcelocks_mission_critical_resources_set`


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
3. Follow the naming convention: `resource_locks_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def resource_locks_example_function_check():
    """
    Example compliance check for Azure Resource_Locks service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.resource_locks import Resource_LocksManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Resource_LocksManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in resource_locks check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Resource_Locks
- **SDK Namespace**: azure.mgmt.resource_locks
- **Client Class**: Resource_LocksManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Resource_Locks API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
