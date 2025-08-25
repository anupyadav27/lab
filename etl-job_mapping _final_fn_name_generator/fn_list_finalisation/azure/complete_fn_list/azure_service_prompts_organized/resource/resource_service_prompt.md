# Azure Azure Resource Service Compliance Prompt

## Service Information
- **Service Name**: RESOURCE
- **Display Name**: Azure Resource
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Resource compliance checks:

1. `monitor_resource_enable_logging_all_services`


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
3. Follow the naming convention: `resource_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def resource_example_function_check():
    """
    Example compliance check for Azure Resource service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.resource import ResourceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = ResourceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in resource check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Resource
- **SDK Namespace**: azure.mgmt.resource
- **Client Class**: ResourceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Resource API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
