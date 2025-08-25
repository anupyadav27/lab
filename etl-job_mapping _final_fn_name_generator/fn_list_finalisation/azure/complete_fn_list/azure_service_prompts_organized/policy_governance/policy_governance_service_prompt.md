# Azure Azure Policy & Governance Service Compliance Prompt

## Service Information
- **Service Name**: POLICY_GOVERNANCE
- **Display Name**: Azure Policy & Governance
- **Total Functions**: 14
- **Original Categories**: Identity, Security
- **Categorization Methods**: sdk_example

## Function List
The following 14 functions are available for Azure Policy & Governance compliance checks:

1. `azure_portal_api_powershell_security_groups_creation_disabled`
2. `policy_asc_default_settings_enabled`
3. `policy_vm_vnet_name_match`
4. `azure_policy_valid_accounts_restriction_status`
5. `security_policy_compliance_review_frequency`
6. `policy_fraud_risk_assessment_incentives_pressures_opportunities_attitudes_rationalizations_it_access_risk`
7. `policy_environment_business_model_leadership_systems_vendor_relationships_assessment`
8. `policy_management_board_assessment_communication_monitoring`
9. `policy_defconfig_standards_monitoring_change_detection_unauthorized_components_vulnerability_scans`
10. `policy_gdpr_compliance_implementation`
11. `organization_info_protection_policy_documentation_communication`
12. `policy_implementation_identification_and_training`
13. `policy_protection_information_review_revision_tracking`
14. `policy_resident_registration_numbers_processing_control`


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
3. Follow the naming convention: `policy_governance_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def policy_governance_example_function_check():
    """
    Example compliance check for Azure Policy & Governance service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.policy_governance import Policy_GovernanceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Policy_GovernanceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in policy_governance check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Policy & Governance
- **SDK Namespace**: azure.mgmt.policy_governance
- **Client Class**: Policy_GovernanceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Policy & Governance API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
