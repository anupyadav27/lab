# Azure Azure Machinelearning Service Compliance Prompt

## Service Information
- **Service Name**: MACHINELEARNING
- **Display Name**: Azure Machinelearning
- **Total Functions**: 8
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 8 functions are available for Azure Machinelearning compliance checks:

1. `machinelearning_workspace_notebook_internet_access_disabled`
2. `machinelearning_workspace_notebook_instance_internet_disabled`
3. `machinelearning_workspace_notebook_instance_in_vnet_or_approved_subnet`
4. `machinelearning_workspace_notebook_instance_in_approved_vnet_or_subnet`
5. `machinelearning_workspace_notebook_instance_vnet_or_approved_subnet`
6. `machinelearning_compute_instance_no_admin_access`
7. `machinelearning_computeinstance_adminaccess_disabled`
8. `machinelearning_workspace_notebook_internet_disabled`


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
3. Follow the naming convention: `machinelearning_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def machinelearning_example_function_check():
    """
    Example compliance check for Azure Machinelearning service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.machinelearning import MachinelearningManagementClient
        
        # credential = DefaultAzureCredential()
        # client = MachinelearningManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in machinelearning check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Machinelearning
- **SDK Namespace**: azure.mgmt.machinelearning
- **Client Class**: MachinelearningManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Machinelearning API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
