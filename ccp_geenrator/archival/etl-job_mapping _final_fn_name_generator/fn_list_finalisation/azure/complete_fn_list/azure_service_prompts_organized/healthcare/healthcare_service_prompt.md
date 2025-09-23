# Azure Azure Healthcare Service Compliance Prompt

## Service Information
- **Service Name**: HEALTHCARE
- **Display Name**: Azure Healthcare
- **Total Functions**: 6
- **Original Categories**: Identity, Security
- **Categorization Methods**: sdk_example

## Function List
The following 6 functions are available for Azure Healthcare compliance checks:

1. `healthcare_workforce_authorization_supervision`
2. `healthcare_workforce_member_terminate_access`
3. `healthcare_ephi_access_authorization_consistency`
4. `healthcare_ehri_logging_monitoring_mechanism`
5. `healthcare_protect_electronic_phi_from_alteration_destruction`
6. `healthcare_apis_workforce_ephi_access_control`


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
3. Follow the naming convention: `healthcare_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def healthcare_example_function_check():
    """
    Example compliance check for Azure Healthcare service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.healthcare import HealthcareManagementClient
        
        # credential = DefaultAzureCredential()
        # client = HealthcareManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in healthcare check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Healthcare
- **SDK Namespace**: azure.mgmt.healthcare
- **Client Class**: HealthcareManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Healthcare API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
