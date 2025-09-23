# Azure Azure Runbook Service Compliance Prompt

## Service Information
- **Service Name**: RUNBOOK
- **Display Name**: Azure Runbook
- **Total Functions**: 3
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 3 functions are available for Azure Runbook compliance checks:

1. `automation_runbook_self_owned_public_status`
2. `automation_runbook_self_owned_public_state`
3. `automation_runbook_self_owned_public`


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
3. Follow the naming convention: `runbook_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def runbook_example_function_check():
    """
    Example compliance check for Azure Runbook service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.runbook import RunbookManagementClient
        
        # credential = DefaultAzureCredential()
        # client = RunbookManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in runbook check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Runbook
- **SDK Namespace**: azure.mgmt.runbook
- **Client Class**: RunbookManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Runbook API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
