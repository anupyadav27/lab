# Azure Azure Reporting Service Compliance Prompt

## Service Information
- **Service Name**: REPORTING
- **Display Name**: Azure Reporting
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Reporting compliance checks:

1. `reporting_operations_compliance_reflects_management_choices`


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
3. Follow the naming convention: `reporting_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def reporting_example_function_check():
    """
    Example compliance check for Azure Reporting service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.reporting import ReportingManagementClient
        
        # credential = DefaultAzureCredential()
        # client = ReportingManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in reporting check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Reporting
- **SDK Namespace**: azure.mgmt.reporting
- **Client Class**: ReportingManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Reporting API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
