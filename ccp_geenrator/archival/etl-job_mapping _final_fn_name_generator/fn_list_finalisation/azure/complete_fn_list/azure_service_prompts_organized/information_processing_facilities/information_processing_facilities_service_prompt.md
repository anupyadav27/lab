# Azure Azure Information_Processing_Facilities Service Compliance Prompt

## Service Information
- **Service Name**: INFORMATION_PROCESSING_FACILITIES
- **Display Name**: Azure Information_Processing_Facilities
- **Total Functions**: 1
- **Original Categories**: Compute
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Information_Processing_Facilities compliance checks:

1. `information_processing_facilities_sufficient_redundancy`


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
3. Follow the naming convention: `information_processing_facilities_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def information_processing_facilities_example_function_check():
    """
    Example compliance check for Azure Information_Processing_Facilities service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.information_processing_facilities import Information_Processing_FacilitiesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Information_Processing_FacilitiesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in information_processing_facilities check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Information_Processing_Facilities
- **SDK Namespace**: azure.mgmt.information_processing_facilities
- **Client Class**: Information_Processing_FacilitiesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Information_Processing_Facilities API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
