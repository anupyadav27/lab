# Azure Azure Api_Management Service Compliance Prompt

## Service Information
- **Service Name**: API_MANAGEMENT
- **Display Name**: Azure Api_Management
- **Total Functions**: 4
- **Original Categories**: Security, Network
- **Categorization Methods**: sdk_example

## Function List
The following 4 functions are available for Azure Api_Management compliance checks:

1. `api_management_api_stage_waf_web_acl_configuration`
2. `api_management_api_stage_waf_web_acl_is_expected`
3. `api_management_rest_apis_application_insights_tracing_enabled`
4. `api_management_api_operations_caching_encryption_enabled`


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
3. Follow the naming convention: `api_management_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def api_management_example_function_check():
    """
    Example compliance check for Azure Api_Management service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.api_management import Api_ManagementManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Api_ManagementManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in api_management check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Api_Management
- **SDK Namespace**: azure.mgmt.api_management
- **Client Class**: Api_ManagementManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Api_Management API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
