# Azure Azure Info_System Service Compliance Prompt

## Service Information
- **Service Name**: INFO_SYSTEM
- **Display Name**: Azure Info_System
- **Total Functions**: 2
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Info_System compliance checks:

1. `info_system_dos_attack_protection`
2. `info_system_confidentiality_integrity_protection_at_rest`


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
3. Follow the naming convention: `info_system_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def info_system_example_function_check():
    """
    Example compliance check for Azure Info_System service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.info_system import Info_SystemManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Info_SystemManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in info_system check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Info_System
- **SDK Namespace**: azure.mgmt.info_system
- **Client Class**: Info_SystemManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Info_System API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
