# Azure Azure Endpoints Service Compliance Prompt

## Service Information
- **Service Name**: ENDPOINTS
- **Display Name**: Azure Endpoints
- **Total Functions**: 2
- **Original Categories**: Network, Network|Storage|Identity
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Endpoints compliance checks:

1. `cdn_endpoint_non_default_ssl_certificate`
2. `cdn_blobstorage_managed_identity_auth_configured`


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
3. Follow the naming convention: `endpoints_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def endpoints_example_function_check():
    """
    Example compliance check for Azure Endpoints service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.endpoints import EndpointsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = EndpointsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in endpoints check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Endpoints
- **SDK Namespace**: azure.mgmt.endpoints
- **Client Class**: EndpointsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Endpoints API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
