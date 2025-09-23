# Azure Azure Purview Service Compliance Prompt

## Service Information
- **Service Name**: PURVIEW
- **Display Name**: Azure Purview
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Purview compliance checks:

1. `purview_administrator_automated_sensitive_data_discovery_enabled`


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
3. Follow the naming convention: `purview_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def purview_example_function_check():
    """
    Example compliance check for Azure Purview service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.purview import PurviewManagementClient
        
        # credential = DefaultAzureCredential()
        # client = PurviewManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in purview check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Purview
- **SDK Namespace**: azure.mgmt.purview
- **Client Class**: PurviewManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Purview API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
