# GCP DATATRANSFER Service Compliance Prompt

## Service Information
- **Service Name**: DATATRANSFER
- **Description**: GCP DATATRANSFER Service
- **Total Functions**: 7
- **SDK Client**: datatransfer_client
- **Service Type**: data

## Function List
The following 7 functions are available for DATATRANSFER compliance checks:

1. `workspace_session_control_configured`
2. `calendar_primary_external_sharing_configured`
3. `calendar_primary_internal_sharing_configured`
4. `calendar_external_invitation_warnings_configured`
5. `calendar_secondary_external_sharing_configured`
6. `calendar_secondary_internal_sharing_configured`
7. `os_config_duplicate_gid_check`


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
3. Follow the naming convention: `datatransfer_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def datatransfer_example_function_check():
    """
    Example compliance check for DATATRANSFER service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in datatransfer check: {e}")
        return False
```

## Notes
- All functions are based on GCP DATATRANSFER API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
