# Azure Azure Get_Blob_Container_Properties() Service Compliance Prompt

## Service Information
- **Service Name**: GET_BLOB_CONTAINER_PROPERTIES
- **Display Name**: Azure Get_Blob_Container_Properties()
- **Total Functions**: 6
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 6 functions are available for Azure Get_Blob_Container_Properties() compliance checks:

1. `storage_blob_container_public_access_disabled`
2. `storage_blob_container_immutable_enabled`
3. `storage_blob_container_versioning_immutable_storage`
4. `storage_blob_container_has_lifecycle_management_policy`
5. `storage_blob_container_versioning_lifecycle_policy`
6. `storage_blob_container_lifecycle_management_policy_active`


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
3. Follow the naming convention: `get_blob_container_properties_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def get_blob_container_properties_example_function_check():
    """
    Example compliance check for Azure Get_Blob_Container_Properties() service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.get_blob_container_properties import Get_Blob_Container_PropertiesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Get_Blob_Container_PropertiesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in get_blob_container_properties check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Get_Blob_Container_Properties()
- **SDK Namespace**: azure.mgmt.get_blob_container_properties
- **Client Class**: Get_Blob_Container_PropertiesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Get_Blob_Container_Properties() API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
