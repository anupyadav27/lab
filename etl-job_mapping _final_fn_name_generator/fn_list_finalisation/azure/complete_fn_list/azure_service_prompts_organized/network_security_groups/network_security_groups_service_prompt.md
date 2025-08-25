# Azure Azure Network_Security_Groups Service Compliance Prompt

## Service Information
- **Service Name**: NETWORK_SECURITY_GROUPS
- **Display Name**: Azure Network_Security_Groups
- **Total Functions**: 1
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Network_Security_Groups compliance checks:

1. `network_security_group_flow_log_retention_greater_than_90_days`


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
3. Follow the naming convention: `network_security_groups_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def network_security_groups_example_function_check():
    """
    Example compliance check for Azure Network_Security_Groups service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.network_security_groups import Network_Security_GroupsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Network_Security_GroupsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in network_security_groups check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Network_Security_Groups
- **SDK Namespace**: azure.mgmt.network_security_groups
- **Client Class**: Network_Security_GroupsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Network_Security_Groups API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
