# Azure Azure Securitycenter Service Compliance Prompt

## Service Information
- **Service Name**: SECURITYCENTER
- **Display Name**: Azure Securitycenter
- **Total Functions**: 4
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 4 functions are available for Azure Securitycenter compliance checks:

1. `securitycenter_system_location_discovery_monitored_state`
2. `securitycenter_supplier_security_practices_regular_monitoring`
3. `security_incident_response_roles_assignment`
4. `securitycenter_information_protection_measures_established`


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
3. Follow the naming convention: `securitycenter_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def securitycenter_example_function_check():
    """
    Example compliance check for Azure Securitycenter service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.securitycenter import SecuritycenterManagementClient
        
        # credential = DefaultAzureCredential()
        # client = SecuritycenterManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in securitycenter check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Securitycenter
- **SDK Namespace**: azure.mgmt.securitycenter
- **Client Class**: SecuritycenterManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Securitycenter API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
