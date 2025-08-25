# Azure Azure Security_Zones Service Compliance Prompt

## Service Information
- **Service Name**: SECURITY_ZONES
- **Display Name**: Azure Security_Zones
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Security_Zones compliance checks:

1. `security_zone_movement_control_established`


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
3. Follow the naming convention: `security_zones_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def security_zones_example_function_check():
    """
    Example compliance check for Azure Security_Zones service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.security_zones import Security_ZonesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Security_ZonesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in security_zones check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Security_Zones
- **SDK Namespace**: azure.mgmt.security_zones
- **Client Class**: Security_ZonesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Security_Zones API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
