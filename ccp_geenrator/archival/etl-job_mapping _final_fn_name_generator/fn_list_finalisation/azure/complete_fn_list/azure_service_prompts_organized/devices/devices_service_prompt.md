# Azure Azure Devices Service Compliance Prompt

## Service Information
- **Service Name**: DEVICES
- **Display Name**: Azure Devices
- **Total Functions**: 1
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Devices compliance checks:

1. `endpoint_device_information_protection`


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
3. Follow the naming convention: `devices_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def devices_example_function_check():
    """
    Example compliance check for Azure Devices service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.devices import DevicesManagementClient
        
        # credential = DefaultAzureCredential()
        # client = DevicesManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in devices check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Devices
- **SDK Namespace**: azure.mgmt.devices
- **Client Class**: DevicesManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Devices API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
