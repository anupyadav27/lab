# Azure Azure Namespace Service Compliance Prompt

## Service Information
- **Service Name**: NAMESPACE
- **Display Name**: Azure Namespace
- **Total Functions**: 2
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Namespace compliance checks:

1. `servicebus_namespace_diagnostic_logging_enabled_azmon_storage`
2. `servicebus_namespace_diagnostic_logging_enabled_azmon_azure_storage`


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
3. Follow the naming convention: `namespace_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def namespace_example_function_check():
    """
    Example compliance check for Azure Namespace service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.namespace import NamespaceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = NamespaceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in namespace check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Namespace
- **SDK Namespace**: azure.mgmt.namespace
- **Client Class**: NamespaceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Namespace API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
