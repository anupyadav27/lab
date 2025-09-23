# Azure Azure Web_App_Service Service Compliance Prompt

## Service Information
- **Service Name**: WEB_APP_SERVICE
- **Display Name**: Azure Web_App_Service
- **Total Functions**: 1
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Web_App_Service compliance checks:

1. `functionapp_policy_prohibit_public_access_private_endpoint_configured`


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
3. Follow the naming convention: `web_app_service_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def web_app_service_example_function_check():
    """
    Example compliance check for Azure Web_App_Service service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.web_app_service import Web_App_ServiceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Web_App_ServiceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in web_app_service check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Web_App_Service
- **SDK Namespace**: azure.mgmt.web_app_service
- **Client Class**: Web_App_ServiceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Web_App_Service API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
