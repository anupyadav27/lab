# Azure Azure Defender_For_Servers Service Compliance Prompt

## Service Information
- **Service Name**: DEFENDER_FOR_SERVERS
- **Display Name**: Azure Defender_For_Servers
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Defender_For_Servers compliance checks:

1. `defender_for_servers_data_deletion_prevention_enabled`


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
3. Follow the naming convention: `defender_for_servers_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def defender_for_servers_example_function_check():
    """
    Example compliance check for Azure Defender_For_Servers service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.defender_for_servers import Defender_For_ServersManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Defender_For_ServersManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in defender_for_servers check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Defender_For_Servers
- **SDK Namespace**: azure.mgmt.defender_for_servers
- **Client Class**: Defender_For_ServersManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Defender_For_Servers API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
