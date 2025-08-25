# Azure Azure Container_Groups Service Compliance Prompt

## Service Information
- **Service Name**: CONTAINER_GROUPS
- **Display Name**: Azure Container_Groups
- **Total Functions**: 1
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Container_Groups compliance checks:

1. `aci_container_instance_latest_platform_version`


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
3. Follow the naming convention: `container_groups_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def container_groups_example_function_check():
    """
    Example compliance check for Azure Container_Groups service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.container_groups import Container_GroupsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Container_GroupsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in container_groups check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Container_Groups
- **SDK Namespace**: azure.mgmt.container_groups
- **Client Class**: Container_GroupsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Container_Groups API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
