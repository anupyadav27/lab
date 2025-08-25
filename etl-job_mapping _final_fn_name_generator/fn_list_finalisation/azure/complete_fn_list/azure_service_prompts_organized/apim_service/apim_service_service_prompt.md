# Azure Azure Apim_Service Service Compliance Prompt

## Service Information
- **Service Name**: APIM_SERVICE
- **Display Name**: Azure Apim_Service
- **Total Functions**: 4
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 4 functions are available for Azure Apim_Service compliance checks:

1. `apim_service_access_logging_enabled`
2. `apim_service_diagnostic_logging_enabled`
3. `apim_service_application_insights_tracing_enabled`
4. `apim_service_ai_tracing_enabled`


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
3. Follow the naming convention: `apim_service_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def apim_service_example_function_check():
    """
    Example compliance check for Azure Apim_Service service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.apim_service import Apim_ServiceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Apim_ServiceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in apim_service check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Apim_Service
- **SDK Namespace**: azure.mgmt.apim_service
- **Client Class**: Apim_ServiceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Apim_Service API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
