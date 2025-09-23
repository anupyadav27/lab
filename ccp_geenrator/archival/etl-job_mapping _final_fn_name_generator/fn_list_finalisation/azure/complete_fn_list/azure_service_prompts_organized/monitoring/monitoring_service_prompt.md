# Azure Azure Monitoring Service Compliance Prompt

## Service Information
- **Service Name**: MONITORING
- **Display Name**: Azure Monitoring
- **Total Functions**: 3
- **Original Categories**: Compute, Security
- **Categorization Methods**: sdk_example

## Function List
The following 3 functions are available for Azure Monitoring compliance checks:

1. `monitor_cloud_services_enumeration`
2. `monitor_and_adjust_resource_capacity`
3. `organization_continuous_monitoring_strategy_implementation`


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
3. Follow the naming convention: `monitoring_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def monitoring_example_function_check():
    """
    Example compliance check for Azure Monitoring service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.monitoring import MonitoringManagementClient
        
        # credential = DefaultAzureCredential()
        # client = MonitoringManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in monitoring check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Monitoring
- **SDK Namespace**: azure.mgmt.monitoring
- **Client Class**: MonitoringManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Monitoring API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
