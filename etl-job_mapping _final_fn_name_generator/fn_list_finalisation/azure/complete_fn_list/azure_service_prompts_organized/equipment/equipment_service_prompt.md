# Azure Azure Equipment Service Compliance Prompt

## Service Information
- **Service Name**: EQUIPMENT
- **Display Name**: Azure Equipment
- **Total Functions**: 2
- **Original Categories**: Compute, Security
- **Categorization Methods**: sdk_example

## Function List
The following 2 functions are available for Azure Equipment compliance checks:

1. `equipment_sited_securely_protected`
2. `equipment_maintenance_status_ensures_availability_integrity_confidentiality`


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
3. Follow the naming convention: `equipment_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def equipment_example_function_check():
    """
    Example compliance check for Azure Equipment service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.equipment import EquipmentManagementClient
        
        # credential = DefaultAzureCredential()
        # client = EquipmentManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in equipment check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Equipment
- **SDK Namespace**: azure.mgmt.equipment
- **Client Class**: EquipmentManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Equipment API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
