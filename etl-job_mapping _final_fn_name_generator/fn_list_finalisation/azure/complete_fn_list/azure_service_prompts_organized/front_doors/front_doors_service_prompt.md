# Azure Azure Front_Doors Service Compliance Prompt

## Service Information
- **Service Name**: FRONT_DOORS
- **Display Name**: Azure Front_Doors
- **Total Functions**: 4
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 4 functions are available for Azure Front_Doors compliance checks:

1. `frontdoor_cdn_profiles_custom_ssl_sni_configured`
2. `frontdoor_cdn_origin_protocol_policy_https_only`
3. `frontdoor_cdn_profiles_https_enforced`
4. `frontdoor_cdn_https_enforcement`


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
3. Follow the naming convention: `front_doors_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def front_doors_example_function_check():
    """
    Example compliance check for Azure Front_Doors service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.front_doors import Front_DoorsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Front_DoorsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in front_doors check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Front_Doors
- **SDK Namespace**: azure.mgmt.front_doors
- **Client Class**: Front_DoorsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Front_Doors API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
