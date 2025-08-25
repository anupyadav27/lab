# Azure Azure Apim Service Compliance Prompt

## Service Information
- **Service Name**: APIM
- **Display Name**: Azure Apim
- **Total Functions**: 9
- **Original Categories**: Security, Network
- **Categorization Methods**: sdk_example

## Function List
The following 9 functions are available for Azure Apim compliance checks:

1. `apim_api_endpoint_type_match`
2. `apim_api_waf_policy_association`
3. `apim_services_ai_tracing_enabled`
4. `apim_api_stage_ssl_certificate_associated`
5. `apim_api_stage_ssl_certificate_configured`
6. `apim_api_stage_ssl_certificate_presence`
7. `apim_services_logging_enabled_error_information`
8. `apim_services_logging_level_set`
9. `apim_services_access_logging_enabled`


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
3. Follow the naming convention: `apim_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def apim_example_function_check():
    """
    Example compliance check for Azure Apim service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.apim import ApimManagementClient
        
        # credential = DefaultAzureCredential()
        # client = ApimManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in apim check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Apim
- **SDK Namespace**: azure.mgmt.apim
- **Client Class**: ApimManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Apim API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
