# Azure Azure DevOps Service Compliance Prompt

## Service Information
- **Service Name**: DEVOPS
- **Display Name**: Azure DevOps
- **Total Functions**: 10
- **Original Categories**: Compute, Security, Storage, DevOps, Identity
- **Categorization Methods**: sdk_example

## Function List
The following 10 functions are available for Azure DevOps compliance checks:

1. `devops_repository_no_embedded_credentials`
2. `devops_pipeline_project_environment_log_enabled`
3. `devops_pipeline_project_environment_log_option_enabled`
4. `devops_pipeline_project_artifacts_encryption_enabled`
5. `devops_project_no_plaintext_credentials`
6. `devops_pipeline_blob_storage_logs_encryption_enabled`
7. `devops_pipelines_deployment_stage_limit`
8. `devops_pipelines_single_deployment_limit`
9. `devops_pipeline_environment_privileged_mode_enabled`
10. `devops_security_testing_implementation`


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
3. Follow the naming convention: `devops_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def devops_example_function_check():
    """
    Example compliance check for Azure DevOps service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.devops import DevopsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = DevopsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in devops check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure DevOps
- **SDK Namespace**: azure.mgmt.devops
- **Client Class**: DevopsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure DevOps API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
