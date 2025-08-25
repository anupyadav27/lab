# Azure Azure Resource_Management Service Compliance Prompt

## Service Information
- **Service Name**: RESOURCE_MANAGEMENT
- **Display Name**: Azure Resource_Management
- **Total Functions**: 1
- **Original Categories**: Compute, Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Resource_Management compliance checks:

1. `arm_template_event_notification_destination`


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
3. Follow the naming convention: `resource_management_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def resource_management_example_function_check():
    """
    Example compliance check for Azure Resource_Management service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.resource_management import Resource_ManagementManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Resource_ManagementManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in resource_management check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Resource_Management
- **SDK Namespace**: azure.mgmt.resource_management
- **Client Class**: Resource_ManagementManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Resource_Management API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
