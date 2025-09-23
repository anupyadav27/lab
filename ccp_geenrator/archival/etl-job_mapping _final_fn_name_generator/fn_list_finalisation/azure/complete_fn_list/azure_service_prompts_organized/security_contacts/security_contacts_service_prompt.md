# Azure Azure Security_Contacts Service Compliance Prompt

## Service Information
- **Service Name**: SECURITY_CONTACTS
- **Display Name**: Azure Security_Contacts
- **Total Functions**: 3
- **Original Categories**: Security
- **Categorization Methods**: sdk_example

## Function List
The following 3 functions are available for Azure Security_Contacts compliance checks:

1. `security_contact_additional_email_addresses_configured`
2. `security_contact_information_provided`
3. `defender_additional_email_security_contact`


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
3. Follow the naming convention: `security_contacts_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def security_contacts_example_function_check():
    """
    Example compliance check for Azure Security_Contacts service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.security_contacts import Security_ContactsManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Security_ContactsManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in security_contacts check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Security_Contacts
- **SDK Namespace**: azure.mgmt.security_contacts
- **Client Class**: Security_ContactsManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Security_Contacts API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
