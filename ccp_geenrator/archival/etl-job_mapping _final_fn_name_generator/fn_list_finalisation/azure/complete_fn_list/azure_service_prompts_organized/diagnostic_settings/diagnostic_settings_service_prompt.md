# Azure Azure Diagnostic_Settings Service Compliance Prompt

## Service Information
- **Service Name**: DIAGNOSTIC_SETTINGS
- **Display Name**: Azure Diagnostic_Settings
- **Total Functions**: 4
- **Original Categories**: Storage, Security
- **Categorization Methods**: sdk_example

## Function List
The following 4 functions are available for Azure Diagnostic_Settings compliance checks:

1. `monitor_blob_storage_diagnostic_setting_presence`
2. `monitor_diagnostic_settings_send_logs_to_log_analytics`
3. `monitor_blob_storage_diagnostic_settings_exist`
4. `monitor_diagnostic_setting_logs_to_log_analytics`


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
3. Follow the naming convention: `diagnostic_settings_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def diagnostic_settings_example_function_check():
    """
    Example compliance check for Azure Diagnostic_Settings service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.diagnostic_settings import Diagnostic_SettingsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Diagnostic_SettingsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in diagnostic_settings check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Diagnostic_Settings
- **SDK Namespace**: azure.mgmt.diagnostic_settings
- **Client Class**: Diagnostic_SettingsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Diagnostic_Settings API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
