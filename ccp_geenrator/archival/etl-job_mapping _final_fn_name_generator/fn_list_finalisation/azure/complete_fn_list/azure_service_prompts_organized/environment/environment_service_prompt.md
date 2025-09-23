# Azure Azure Environment Service Compliance Prompt

## Service Information
- **Service Name**: ENVIRONMENT
- **Display Name**: Azure Environment
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Environment compliance checks:

1. `environment_separation_security`


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
3. Follow the naming convention: `environment_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def environment_example_function_check():
    """
    Example compliance check for Azure Environment service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.environment import EnvironmentManagementClient
        
        # credential = DefaultAzureCredential()
        # client = EnvironmentManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in environment check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Environment
- **SDK Namespace**: azure.mgmt.environment
- **Client Class**: EnvironmentManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Environment API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
