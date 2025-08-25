# Azure Azure Security_Groups Service Compliance Prompt

## Service Information
- **Service Name**: SECURITY_GROUPS
- **Display Name**: Azure Security_Groups
- **Total Functions**: 2
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Security_Groups compliance checks:

1. `network_security_group_udp_access_restricted`
2. `network_security_group_ssh_access_restricted`


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
3. Follow the naming convention: `security_groups_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def security_groups_example_function_check():
    """
    Example compliance check for Azure Security_Groups service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.security_groups import Security_GroupsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Security_GroupsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in security_groups check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Security_Groups
- **SDK Namespace**: azure.mgmt.security_groups
- **Client Class**: Security_GroupsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Security_Groups API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
