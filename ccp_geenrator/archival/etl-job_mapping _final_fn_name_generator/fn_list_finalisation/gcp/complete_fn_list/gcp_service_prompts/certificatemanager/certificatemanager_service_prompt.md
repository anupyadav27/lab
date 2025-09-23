# GCP CERTIFICATEMANAGER Service Compliance Prompt

## Service Information
- **Service Name**: CERTIFICATEMANAGER
- **Description**: GCP CERTIFICATEMANAGER Service
- **Total Functions**: 2
- **SDK Client**: certificatemanager_client
- **Service Type**: security

## Function List
The following 2 functions are available for CERTIFICATEMANAGER compliance checks:

1. `certificate_manager_certificates_expiration_within_days`
2. `certificate_manager_certificates_expiration_check`


## Compliance Framework Coverage
This service supports compliance checks for:
- **NIST Cybersecurity Framework**
- **PCI DSS v4.0**
- **ISO 27001**
- **SOC 2**
- **GDPR**
- **HIPAA** (where applicable)

## Usage Instructions
1. Use the function names above to create compliance checks
2. Each function should be implemented as a separate compliance rule
3. Follow the naming convention: `certificatemanager_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def certificatemanager_example_function_check():
    """
    Example compliance check for CERTIFICATEMANAGER service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in certificatemanager check: {e}")
        return False
```

## Notes
- All functions are based on GCP CERTIFICATEMANAGER API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
