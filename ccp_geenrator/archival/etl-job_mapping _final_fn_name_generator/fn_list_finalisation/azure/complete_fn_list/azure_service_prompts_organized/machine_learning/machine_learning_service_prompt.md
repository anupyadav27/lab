# Azure Azure Machine_Learning Service Compliance Prompt

## Service Information
- **Service Name**: MACHINE_LEARNING
- **Display Name**: Azure Machine_Learning
- **Total Functions**: 3
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 3 functions are available for Azure Machine_Learning compliance checks:

1. `machine_learning_workspace_notebook_instance_in_vnet_or_approved_subnet`
2. `machine_learning_workspace_notebook_instance_vnet_or_approved_subnet_deployment`
3. `machine_learning_compute_instance_admin_access_disabled`


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
3. Follow the naming convention: `machine_learning_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def machine_learning_example_function_check():
    """
    Example compliance check for Azure Machine_Learning service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.machine_learning import Machine_LearningManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Machine_LearningManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in machine_learning check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Machine_Learning
- **SDK Namespace**: azure.mgmt.machine_learning
- **Client Class**: Machine_LearningManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Machine_Learning API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
