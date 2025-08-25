# Azure Azure System Service Compliance Prompt

## Service Information
- **Service Name**: SYSTEM
- **Display Name**: Azure System
- **Total Functions**: 11
- **Original Categories**: Compute, Security
- **Categorization Methods**: sdk_example

## Function List
The following 11 functions are available for Azure System compliance checks:

1. `system_application_controls_utility_programs_restriction`
2. `system_time_synchronization_maintenance`
3. `system_remote_access_control_monitoring`
4. `system_implement_cryptographic_protection_for_remote_sessions`
5. `system_audit_info_protection`
6. `system_network_audit_record_generation_capability`
7. `system_network_access_multifactor_authentication_privileged_nonprivileged`
8. `system_lifecycle_management_security_incorporation`
9. `system_component_service_configuration_management_integrity_control`
10. `system_transmitted_information_confidentiality_integrity_protection`
11. `system_protect_communications_sessions_authenticity`


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
3. Follow the naming convention: `system_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def system_example_function_check():
    """
    Example compliance check for Azure System service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.system import SystemManagementClient
        
        # credential = DefaultAzureCredential()
        # client = SystemManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in system check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure System
- **SDK Namespace**: azure.mgmt.system
- **Client Class**: SystemManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure System API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
