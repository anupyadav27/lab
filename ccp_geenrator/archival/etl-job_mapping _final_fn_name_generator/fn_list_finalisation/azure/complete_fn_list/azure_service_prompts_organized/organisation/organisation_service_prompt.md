# Azure Azure Organisation Service Compliance Prompt

## Service Information
- **Service Name**: ORGANISATION
- **Display Name**: Azure Organisation
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Organisation compliance checks:

1. `organisation_info_transfer_rules_in_place`


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
3. Follow the naming convention: `organisation_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def organisation_example_function_check():
    """
    Example compliance check for Azure Organisation service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.organisation import OrganisationManagementClient
        
        # credential = DefaultAzureCredential()
        # client = OrganisationManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in organisation check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Organisation
- **SDK Namespace**: azure.mgmt.organisation
- **Client Class**: OrganisationManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Organisation API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
