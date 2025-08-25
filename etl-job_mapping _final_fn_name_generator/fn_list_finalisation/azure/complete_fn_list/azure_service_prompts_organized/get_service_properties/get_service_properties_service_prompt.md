# Azure Azure Get_Service_Properties() Service Compliance Prompt

## Service Information
- **Service Name**: GET_SERVICE_PROPERTIES
- **Display Name**: Azure Get_Service_Properties()
- **Total Functions**: 3
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 3 functions are available for Azure Get_Service_Properties() compliance checks:

1. `aisearch_service_end_to_end_encryption_enabled`
2. `cognitive_search_domain_rbac_enabled`
3. `cognitive_search_domain_advanced_security_enabled`


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
3. Follow the naming convention: `get_service_properties_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def get_service_properties_example_function_check():
    """
    Example compliance check for Azure Get_Service_Properties() service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.get_service_properties import Get_Service_PropertiesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Get_Service_PropertiesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in get_service_properties check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Get_Service_Properties()
- **SDK Namespace**: azure.mgmt.get_service_properties
- **Client Class**: Get_Service_PropertiesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Get_Service_Properties() API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
