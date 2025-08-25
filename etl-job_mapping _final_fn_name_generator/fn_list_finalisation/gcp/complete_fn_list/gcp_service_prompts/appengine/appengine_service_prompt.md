# GCP APPENGINE Service Compliance Prompt

## Service Information
- **Service Name**: APPENGINE
- **Description**: GCP APPENGINE Service
- **Total Functions**: 8
- **SDK Client**: appengine_client
- **Service Type**: compute

## Function List
The following 8 functions are available for APPENGINE compliance checks:

1. `workspace_marketplace_apps_access_restricted`
2. `workspace_less_secure_app_access_disabled`
3. `workspace_app_usage_report_reviewed`
4. `appengine_environment_automatic_updates_enabled`
5. `third_party_applications_periodic_review`
6. `app_engine_application_automatic_updates_enabled`
7. `app_engine_application_https_enforced`
8. `chat_apps_installation_disabled`


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
3. Follow the naming convention: `appengine_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def appengine_example_function_check():
    """
    Example compliance check for APPENGINE service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in appengine check: {e}")
        return False
```

## Notes
- All functions are based on GCP APPENGINE API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
