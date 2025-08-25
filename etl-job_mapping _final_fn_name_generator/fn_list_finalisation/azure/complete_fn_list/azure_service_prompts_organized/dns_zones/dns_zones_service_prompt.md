# Azure Azure Dns_Zones Service Compliance Prompt

## Service Information
- **Service Name**: DNS_ZONES
- **Display Name**: Azure Dns_Zones
- **Total Functions**: 1
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Dns_Zones compliance checks:

1. `dns_public_zones_dns_query_logging_enabled`


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
3. Follow the naming convention: `dns_zones_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def dns_zones_example_function_check():
    """
    Example compliance check for Azure Dns_Zones service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.dns_zones import Dns_ZonesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Dns_ZonesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in dns_zones check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Dns_Zones
- **SDK Namespace**: azure.mgmt.dns_zones
- **Client Class**: Dns_ZonesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Dns_Zones API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
