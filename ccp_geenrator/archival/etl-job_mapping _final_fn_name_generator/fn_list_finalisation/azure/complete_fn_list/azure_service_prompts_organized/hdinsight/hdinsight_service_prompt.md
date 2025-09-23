# Azure Azure Hdinsight Service Compliance Prompt

## Service Information
- **Service Name**: HDINSIGHT
- **Display Name**: Azure Hdinsight
- **Total Functions**: 8
- **Original Categories**: Compute, Security, Network
- **Categorization Methods**: sdk_example

## Function List
The following 8 functions are available for Azure Hdinsight compliance checks:

1. `hdinsight_cluster_esp_kerberos_auth_enabled`
2. `hdinsight_cluster_public_network_access_disabled_nsg_inbound_traffic_limited`
3. `hdinsight_cluster_public_network_access_disabled`
4. `hdinsight_cluster_public_network_access_disabled_nsg_port_restriction`
5. `hdinsight_cluster_esp_kerberos_enabled`
6. `hdinsight_cluster_public_access_disabled_nsg_inbound_traffic_limited`
7. `hdinsight_cluster_esp_kerberos_auth_configured`
8. `hdinsight_cluster_public_access_disabled_nsg_port_restriction`


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
3. Follow the naming convention: `hdinsight_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def hdinsight_example_function_check():
    """
    Example compliance check for Azure Hdinsight service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.hdinsight import HdinsightManagementClient
        
        # credential = DefaultAzureCredential()
        # client = HdinsightManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in hdinsight check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Hdinsight
- **SDK Namespace**: azure.mgmt.hdinsight
- **Client Class**: HdinsightManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Hdinsight API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
