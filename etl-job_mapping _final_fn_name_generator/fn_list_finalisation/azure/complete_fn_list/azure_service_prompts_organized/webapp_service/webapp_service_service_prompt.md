# Azure Azure Webapp_Service Service Compliance Prompt

## Service Information
- **Service Name**: WEBAPP_SERVICE
- **Display Name**: Azure Webapp_Service
- **Total Functions**: 2
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Webapp_Service compliance checks:

1. `webapp_php_latest_version`
2. `webapp_java_latest_version`


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
3. Follow the naming convention: `webapp_service_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def webapp_service_example_function_check():
    """
    Example compliance check for Azure Webapp_Service service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.webapp_service import Webapp_ServiceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Webapp_ServiceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in webapp_service check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Webapp_Service
- **SDK Namespace**: azure.mgmt.webapp_service
- **Client Class**: Webapp_ServiceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Webapp_Service API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
