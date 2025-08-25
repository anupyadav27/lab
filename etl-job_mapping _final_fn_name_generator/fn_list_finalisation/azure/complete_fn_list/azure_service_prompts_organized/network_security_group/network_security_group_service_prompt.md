# Azure Azure Network_Security_Group Service Compliance Prompt

## Service Information
- **Service Name**: NETWORK_SECURITY_GROUP
- **Display Name**: Azure Network_Security_Group
- **Total Functions**: 1
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Network_Security_Group compliance checks:

1. `network_security_flow_analysis_timeliness`


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
3. Follow the naming convention: `network_security_group_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def network_security_group_example_function_check():
    """
    Example compliance check for Azure Network_Security_Group service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.network_security_group import Network_Security_GroupManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Network_Security_GroupManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in network_security_group check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Network_Security_Group
- **SDK Namespace**: azure.mgmt.network_security_group
- **Client Class**: Network_Security_GroupManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Network_Security_Group API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
