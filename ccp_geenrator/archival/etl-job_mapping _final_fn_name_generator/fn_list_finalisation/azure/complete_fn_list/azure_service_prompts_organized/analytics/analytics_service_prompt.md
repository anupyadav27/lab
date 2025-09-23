# Azure Azure Analytics Service Compliance Prompt

## Service Information
- **Service Name**: ANALYTICS
- **Display Name**: Azure Analytics
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Analytics compliance checks:

1. `analytics_system_activity_records_review_implementation`


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
3. Follow the naming convention: `analytics_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def analytics_example_function_check():
    """
    Example compliance check for Azure Analytics service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.analytics import AnalyticsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = AnalyticsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in analytics check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Analytics
- **SDK Namespace**: azure.mgmt.analytics
- **Client Class**: AnalyticsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Analytics API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
