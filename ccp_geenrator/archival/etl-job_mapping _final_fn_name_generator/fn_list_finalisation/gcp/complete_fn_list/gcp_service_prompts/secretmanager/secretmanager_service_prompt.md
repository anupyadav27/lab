# GCP SECRETMANAGER Service Compliance Prompt

## Service Information
- **Service Name**: SECRETMANAGER
- **Description**: GCP SECRETMANAGER Service
- **Total Functions**: 11
- **SDK Client**: secretmanager_client
- **Service Type**: security

## Function List
The following 11 functions are available for SECRETMANAGER compliance checks:

1. `secretmanager_secret_cmek_encrypted`
2. `secretmanager_secret_accessed_within_days`
3. `secretmanager_secret_rotation_enabled_within_max_frequency`
4. `secretmanager_secret_rotation_enabled`
5. `secretmanager_secret_rotation_enabled_max_frequency`
6. `secretmanager_secret_recent_rotation`
7. `secretmanager_secrets_accessed_within_days`
8. `secretmanager_secret_rotation_enabled_with_max_frequency`
9. `secrets_manager_secret_access_minimized`
10. `secrets_as_files_preferred`
11. `secrets_access_minimized`


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
3. Follow the naming convention: `secretmanager_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def secretmanager_example_function_check():
    """
    Example compliance check for SECRETMANAGER service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in secretmanager check: {e}")
        return False
```

## Notes
- All functions are based on GCP SECRETMANAGER API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
