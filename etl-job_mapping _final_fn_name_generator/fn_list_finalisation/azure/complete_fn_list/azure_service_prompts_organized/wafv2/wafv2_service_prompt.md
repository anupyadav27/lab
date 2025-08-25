# Azure Azure Wafv2 Service Compliance Prompt

## Service Information
- **Service Name**: WAFV2
- **Display Name**: Azure Wafv2
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Wafv2 compliance checks:

1. `wafv2_web_acl_contains_rules_or_groups`


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
3. Follow the naming convention: `wafv2_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def wafv2_example_function_check():
    """
    Example compliance check for Azure Wafv2 service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.wafv2 import Wafv2ManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Wafv2ManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in wafv2 check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Wafv2
- **SDK Namespace**: azure.mgmt.wafv2
- **Client Class**: Wafv2ManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Wafv2 API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
