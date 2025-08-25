# Azure Azure Functions Service Compliance Prompt

## Service Information
- **Service Name**: FUNCTIONS
- **Display Name**: Azure Functions
- **Total Functions**: 2
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Functions compliance checks:

1. `functions_compute_platform_deployment_group_non_default_configuration`
2. `functions_compute_platform_non_default_deployment`


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
3. Follow the naming convention: `functions_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def functions_example_function_check():
    """
    Example compliance check for Azure Functions service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.functions import FunctionsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = FunctionsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in functions check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Functions
- **SDK Namespace**: azure.mgmt.functions
- **Client Class**: FunctionsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Functions API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
