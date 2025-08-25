# Azure Azure Queue Service Compliance Prompt

## Service Information
- **Service Name**: QUEUE
- **Display Name**: Azure Queue
- **Total Functions**: 1
- **Original Categories**: Network
- **Categorization Methods**: sdk_example

## Function List
The following 1 functions are available for Azure Queue compliance checks:

1. `servicebus_endpoints_messages_delivery_status_logging_enabled`


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
3. Follow the naming convention: `queue_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def queue_example_function_check():
    """
    Example compliance check for Azure Queue service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.queue import QueueManagementClient
        
        # credential = DefaultAzureCredential()
        # client = QueueManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in queue check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Queue
- **SDK Namespace**: azure.mgmt.queue
- **Client Class**: QueueManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Queue API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
