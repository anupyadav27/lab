# Azure Azure Blob_Container Service Compliance Prompt

## Service Information
- **Service Name**: BLOB_CONTAINER
- **Display Name**: Azure Blob_Container
- **Total Functions**: 2
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Blob_Container compliance checks:

1. `storage_blob_container_keyvault_encryption`
2. `storage_offsite_assets_protected`


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
3. Follow the naming convention: `blob_container_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def blob_container_example_function_check():
    """
    Example compliance check for Azure Blob_Container service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.blob_container import Blob_ContainerManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Blob_ContainerManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in blob_container check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Blob_Container
- **SDK Namespace**: azure.mgmt.blob_container
- **Client Class**: Blob_ContainerManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Blob_Container API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
