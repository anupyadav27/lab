# Azure Azure Web_Application_Firewall Service Compliance Prompt

## Service Information
- **Service Name**: WEB_APPLICATION_FIREWALL
- **Display Name**: Azure Web_Application_Firewall
- **Total Functions**: 5
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 5 functions are available for Azure Web_Application_Firewall compliance checks:

1. `waf_global_rule_has_conditions`
2. `waf_global_rule_conditions_presence`
3. `waf_rule_group_metrics_collection_enabled`
4. `wafv2_rule_group_rules_present`
5. `waf_v2_rule_group_rules_presence`


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
3. Follow the naming convention: `web_application_firewall_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def web_application_firewall_example_function_check():
    """
    Example compliance check for Azure Web_Application_Firewall service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.web_application_firewall import Web_Application_FirewallManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Web_Application_FirewallManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in web_application_firewall check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Web_Application_Firewall
- **SDK Namespace**: azure.mgmt.web_application_firewall
- **Client Class**: Web_Application_FirewallManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Web_Application_Firewall API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
