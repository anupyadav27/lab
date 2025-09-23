# Azure Azure Virtual_Networks Service Compliance Prompt

## Service Information
- **Service Name**: VIRTUAL_NETWORKS
- **Display Name**: Azure Virtual_Networks
- **Total Functions**: 3
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 3 functions are available for Azure Virtual_Networks compliance checks:

1. `network_vnet_private_endpoint_exists_for_service`
2. `network_vnet_private_endpoint_required`
3. `network_vnet_flow_logs_enabled`


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
3. Follow the naming convention: `virtual_networks_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def virtual_networks_example_function_check():
    """
    Example compliance check for Azure Virtual_Networks service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.virtual_networks import Virtual_NetworksManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Virtual_NetworksManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in virtual_networks check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Virtual_Networks
- **SDK Namespace**: azure.mgmt.virtual_networks
- **Client Class**: Virtual_NetworksManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Virtual_Networks API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
