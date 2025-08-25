# Azure Azure Humanresources Service Compliance Prompt

## Service Information
- **Service Name**: HUMANRESOURCES
- **Display Name**: Azure Humanresources
- **Total Functions**: 1
- **Original Categories**: Identity
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Humanresources compliance checks:

1. `humanresources_personnel_background_verification_proportional_to_risks`


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
3. Follow the naming convention: `humanresources_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def humanresources_example_function_check():
    """
    Example compliance check for Azure Humanresources service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.humanresources import HumanresourcesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = HumanresourcesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in humanresources check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Humanresources
- **SDK Namespace**: azure.mgmt.humanresources
- **Client Class**: HumanresourcesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Humanresources API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
