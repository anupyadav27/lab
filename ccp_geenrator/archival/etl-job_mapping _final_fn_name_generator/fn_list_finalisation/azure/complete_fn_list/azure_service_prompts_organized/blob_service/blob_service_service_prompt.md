# Azure Azure Blob_Service Service Compliance Prompt

## Service Information
- **Service Name**: BLOB_SERVICE
- **Display Name**: Azure Blob_Service
- **Total Functions**: 2
- **Original Categories**: Storage
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Blob_Service compliance checks:

1. `storage_source_programs_authorized_access_only`
2. `storage_electronic_protected_health_info_backup_maintenance`


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
3. Follow the naming convention: `blob_service_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def blob_service_example_function_check():
    """
    Example compliance check for Azure Blob_Service service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.blob_service import Blob_ServiceManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Blob_ServiceManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in blob_service check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Blob_Service
- **SDK Namespace**: azure.mgmt.blob_service
- **Client Class**: Blob_ServiceManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Blob_Service API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
