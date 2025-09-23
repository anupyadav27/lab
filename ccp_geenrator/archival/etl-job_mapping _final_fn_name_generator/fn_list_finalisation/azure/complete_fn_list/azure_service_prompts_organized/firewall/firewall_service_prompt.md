# Azure Azure Firewall Service Compliance Prompt

## Service Information
- **Service Name**: FIREWALL
- **Display Name**: Azure Firewall
- **Total Functions**: 1
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Firewall compliance checks:

1. `firewall_policy_user_defined_default_stateless_action_full_packets`


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
3. Follow the naming convention: `firewall_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def firewall_example_function_check():
    """
    Example compliance check for Azure Firewall service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.firewall import FirewallManagementClient
        
        # credential = DefaultAzureCredential()
        # client = FirewallManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in firewall check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Firewall
- **SDK Namespace**: azure.mgmt.firewall
- **Client Class**: FirewallManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Firewall API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
