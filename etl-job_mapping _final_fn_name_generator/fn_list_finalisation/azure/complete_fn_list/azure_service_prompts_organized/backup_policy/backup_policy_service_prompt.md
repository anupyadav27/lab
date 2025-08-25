# Azure Azure Backup_Policy Service Compliance Prompt

## Service Information
- **Service Name**: BACKUP_POLICY
- **Display Name**: Azure Backup_Policy
- **Total Functions**: 2
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Backup_Policy compliance checks:

1. `backup_policy_compliant_frequency_retention`
2. `backup_policy_required_frequency_retention`


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
3. Follow the naming convention: `backup_policy_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def backup_policy_example_function_check():
    """
    Example compliance check for Azure Backup_Policy service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.backup_policy import Backup_PolicyManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Backup_PolicyManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in backup_policy check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Backup_Policy
- **SDK Namespace**: azure.mgmt.backup_policy
- **Client Class**: Backup_PolicyManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Backup_Policy API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
