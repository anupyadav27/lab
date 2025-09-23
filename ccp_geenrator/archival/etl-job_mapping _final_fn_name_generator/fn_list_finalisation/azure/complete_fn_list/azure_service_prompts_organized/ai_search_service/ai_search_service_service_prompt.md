# Azure Azure Ai_Search_Service Service Compliance Prompt

## Service Information
- **Service Name**: AI_SEARCH_SERVICE
- **Display Name**: Azure Ai_Search_Service
- **Total Functions**: 3
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 3 functions are available for Azure Ai_Search_Service compliance checks:

1. `ai_search_service_https_enforcement_tls_version`
2. `ai_search_service_https_enforced_tls_compliant`
3. `ai_search_service_https_enforcement_tls_compliance`


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
3. Follow the naming convention: `ai_search_service_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def ai_search_service_example_function_check():
    """
    Example compliance check for Azure Ai_Search_Service service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.ai_search_service import Ai_Search_ServiceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Ai_Search_ServiceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in ai_search_service check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Ai_Search_Service
- **SDK Namespace**: azure.mgmt.ai_search_service
- **Client Class**: Ai_Search_ServiceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Ai_Search_Service API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
