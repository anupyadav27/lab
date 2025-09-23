# Azure Azure Project_Management Service Compliance Prompt

## Service Information
- **Service Name**: PROJECT_MANAGEMENT
- **Display Name**: Azure Project_Management
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Project_Management compliance checks:

1. `project_management_security_integration`


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
3. Follow the naming convention: `project_management_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def project_management_example_function_check():
    """
    Example compliance check for Azure Project_Management service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.project_management import Project_ManagementManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Project_ManagementManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in project_management check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Project_Management
- **SDK Namespace**: azure.mgmt.project_management
- **Client Class**: Project_ManagementManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Project_Management API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
