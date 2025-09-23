# Azure Azure Virtual_Machines Service Compliance Prompt

## Service Information
- **Service Name**: VIRTUAL_MACHINES
- **Display Name**: Azure Virtual_Machines
- **Total Functions**: 7
- **Original Categories**: Compute, Identity|Compute
- **Categorization Methods**: sdk_example

## Function List
The following 7 functions are available for Azure Virtual_Machines compliance checks:

1. `azure_virtual_machine_backup_policy_coverage`
2. `virtual_machine_detailed_monitoring_enabled`
3. `vm_application_installation_with_version_and_platform`
4. `azure_vm_installed_applications_with_min_version_and_platform`
5. `vm_managed_identity_attached`
6. `virtual_machine_managed_identity_attached`
7. `virtual_machine_metadata_service_imdsv2_http_tokens_required`


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
3. Follow the naming convention: `virtual_machines_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def virtual_machines_example_function_check():
    """
    Example compliance check for Azure Virtual_Machines service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.virtual_machines import Virtual_MachinesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Virtual_MachinesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in virtual_machines check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Virtual_Machines
- **SDK Namespace**: azure.mgmt.virtual_machines
- **Client Class**: Virtual_MachinesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Virtual_Machines API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
