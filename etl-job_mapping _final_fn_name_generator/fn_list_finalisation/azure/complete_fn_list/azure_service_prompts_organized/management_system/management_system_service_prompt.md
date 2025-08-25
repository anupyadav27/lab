# Azure Azure Management_System Service Compliance Prompt

## Service Information
- **Service Name**: MANAGEMENT_SYSTEM
- **Display Name**: Azure Management_System
- **Total Functions**: 5
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 5 functions are available for Azure Management_System compliance checks:

1. `management_system_set_scope_documentation`
2. `management_system_resource_allocation_effectiveness`
3. `management_system_info_services_status_documentation_review`
4. `management_system_operational_activities_recorded_tracked_reviewed_managed`
5. `management_system_audit_annual_independent_expertise`


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
3. Follow the naming convention: `management_system_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def management_system_example_function_check():
    """
    Example compliance check for Azure Management_System service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.management_system import Management_SystemManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Management_SystemManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in management_system check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Management_System
- **SDK Namespace**: azure.mgmt.management_system
- **Client Class**: Management_SystemManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Management_System API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
