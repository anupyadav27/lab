# Azure Azure Ai_Search Service Compliance Prompt

## Service Information
- **Service Name**: AI_SEARCH
- **Display Name**: Azure Ai_Search
- **Total Functions**: 2
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Ai_Search compliance checks:

1. `ai_search_node_end_to_end_encryption_enabled`
2. `ai_search_node_encryption_enabled`


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
3. Follow the naming convention: `ai_search_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def ai_search_example_function_check():
    """
    Example compliance check for Azure Ai_Search service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.ai_search import Ai_SearchManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Ai_SearchManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in ai_search check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Ai_Search
- **SDK Namespace**: azure.mgmt.ai_search
- **Client Class**: Ai_SearchManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Ai_Search API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
