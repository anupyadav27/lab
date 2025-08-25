# Azure Azure Policies Service Compliance Prompt

## Service Information
- **Service Name**: POLICIES
- **Display Name**: Azure Policies
- **Total Functions**: 8
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 8 functions are available for Azure Policies compliance checks:

1. `azure_policies_facilities_protection_from_utilities_failures`
2. `azure_policies_configurations_established_documented_implemented_monitored_reviewed`
3. `policies_identify_information_requirements_data_sources_processing_quality_maintenance`
4. `azure_policies_risk_assessment_comprehensiveness`
5. `policies_separation_of_duties_established_applied_or_supplemented`
6. `azure_policies_personal_information_regularly_managed`
7. `azure_policies_personal_information_abroad_transfer_protection`
8. `azure_policies_unauthorized_components_detection_interval`


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
3. Follow the naming convention: `policies_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def policies_example_function_check():
    """
    Example compliance check for Azure Policies service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.policies import PoliciesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = PoliciesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in policies check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Policies
- **SDK Namespace**: azure.mgmt.policies
- **Client Class**: PoliciesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Policies API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
