# Azure Azure Managed_Disks Service Compliance Prompt

## Service Information
- **Service Name**: MANAGED_DISKS
- **Display Name**: Azure Managed_Disks
- **Total Functions**: 1
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Managed_Disks compliance checks:

1. `azure_managed_disks_backup_policy_coverage`


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
3. Follow the naming convention: `managed_disks_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def managed_disks_example_function_check():
    """
    Example compliance check for Azure Managed_Disks service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.managed_disks import Managed_DisksManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Managed_DisksManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in managed_disks check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Managed_Disks
- **SDK Namespace**: azure.mgmt.managed_disks
- **Client Class**: Managed_DisksManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Managed_Disks API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
