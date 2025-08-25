# Azure Azure Monitoring_Tool Service Compliance Prompt

## Service Information
- **Service Name**: MONITORING_TOOL
- **Display Name**: Azure Monitoring_Tool
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Monitoring_Tool compliance checks:

1. `monitoring_tool_correlation_systemwide`


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
3. Follow the naming convention: `monitoring_tool_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def monitoring_tool_example_function_check():
    """
    Example compliance check for Azure Monitoring_Tool service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.monitoring_tool import Monitoring_ToolManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Monitoring_ToolManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in monitoring_tool check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Monitoring_Tool
- **SDK Namespace**: azure.mgmt.monitoring_tool
- **Client Class**: Monitoring_ToolManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Monitoring_Tool API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
