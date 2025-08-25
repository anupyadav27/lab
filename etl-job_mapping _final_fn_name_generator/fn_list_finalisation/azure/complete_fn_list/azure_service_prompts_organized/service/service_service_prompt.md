# Azure Azure Service Service Compliance Prompt

## Service Information
- **Service Name**: SERVICE
- **Display Name**: Azure Service
- **Total Functions**: 5
- **Original Categories**: Identity, Security
- **Categorization Methods**: sdk_example

## Function List
The following 5 functions are available for Azure Service compliance checks:

1. `webapp_client_certificates_enabled`
2. `cloud_service_dashboard_secured_state`
3. `org_implement_intellectual_property_rights_protection`
4. `information_processing_facilities_documentation_availability`
5. `info_systems_arrangement_protection`


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
3. Follow the naming convention: `service_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def service_example_function_check():
    """
    Example compliance check for Azure Service service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.service import ServiceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = ServiceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in service check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Service
- **SDK Namespace**: azure.mgmt.service
- **Client Class**: ServiceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Service API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
