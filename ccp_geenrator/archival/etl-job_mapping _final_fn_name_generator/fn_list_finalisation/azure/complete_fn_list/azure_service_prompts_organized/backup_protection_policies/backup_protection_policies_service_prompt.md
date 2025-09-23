# Azure Azure Backup_Protection_Policies Service Compliance Prompt

## Service Information
- **Service Name**: BACKUP_PROTECTION_POLICIES
- **Display Name**: Azure Backup_Protection_Policies
- **Total Functions**: 2
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Backup_Protection_Policies compliance checks:

1. `storage_fileshare_included_in_backup_policy`
2. `storage_fileshares_backup_policy_coverage`


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
3. Follow the naming convention: `backup_protection_policies_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def backup_protection_policies_example_function_check():
    """
    Example compliance check for Azure Backup_Protection_Policies service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.backup_protection_policies import Backup_Protection_PoliciesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Backup_Protection_PoliciesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in backup_protection_policies check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Backup_Protection_Policies
- **SDK Namespace**: azure.mgmt.backup_protection_policies
- **Client Class**: Backup_Protection_PoliciesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Backup_Protection_Policies API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
