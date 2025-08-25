# Azure Azure Application_Gateway Service Compliance Prompt

## Service Information
- **Service Name**: APPLICATION_GATEWAY
- **Display Name**: Azure Application_Gateway
- **Total Functions**: 5
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 5 functions are available for Azure Application_Gateway compliance checks:

1. `application_gateway_ssl_certificate_from_key_vault`
2. `application_gateway_front_door_ssl_listener_predefined_policy`
3. `application_gateway_front_door_ssl_listener_predefined_policy_match`
4. `application_gateway_uses_key_vault_ssl`
5. `application_gateway_uses_key_vault_certificates`


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
3. Follow the naming convention: `application_gateway_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def application_gateway_example_function_check():
    """
    Example compliance check for Azure Application_Gateway service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.application_gateway import Application_GatewayManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Application_GatewayManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in application_gateway check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Application_Gateway
- **SDK Namespace**: azure.mgmt.application_gateway
- **Client Class**: Application_GatewayManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Application_Gateway API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
