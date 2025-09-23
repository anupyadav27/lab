# Azure Azure Frontdoor Service Compliance Prompt

## Service Information
- **Service Name**: FRONTDOOR
- **Display Name**: Azure Frontdoor
- **Total Functions**: 9
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 9 functions are available for Azure Frontdoor compliance checks:

1. `frontdoor_cdn_tls12_enforced`
2. `frontdoor_cdn_minimum_tls12`
3. `frontdoor_profile_waf_policy_association`
4. `frontdoor_cdn_profile_logging_configured`
5. `frontdoor_cdn_endpoint_tls12_enforced`
6. `frontdoor_cdn_profiles_min_tls12_security_policy`
7. `frontdoor_cdn_profiles_custom_ssl_sni_enabled`
8. `frontdoor_cdn_origin_protocol_https_only`
9. `frontdoor_cdn_tls12_protocol`


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
3. Follow the naming convention: `frontdoor_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def frontdoor_example_function_check():
    """
    Example compliance check for Azure Frontdoor service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.frontdoor import FrontdoorManagementClient
        
        # credential = DefaultAzureCredential()
        # client = FrontdoorManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in frontdoor check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Frontdoor
- **SDK Namespace**: azure.mgmt.frontdoor
- **Client Class**: FrontdoorManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Frontdoor API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
