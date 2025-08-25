# GCP RUN Service Compliance Prompt

## Service Information
- **Service Name**: RUN
- **Description**: GCP RUN Service
- **Total Functions**: 8
- **SDK Client**: run_client
- **Service Type**: compute

## Function List
The following 8 functions are available for RUN compliance checks:

1. `workspace_service_access_restricted`
2. `appengine_service_cloud_armor_association`
3. `certificate_authority_service_root_ca_disabled`
4. `dms_private_service_no_public_access`
5. `google_sites_service_status_off`
6. `cloud_run_service_latest_platform_version`
7. `cloud_run_service_readonly_filesystem_enforced`
8. `cloud_run_service_platform_latest_version`


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
3. Follow the naming convention: `run_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def run_example_function_check():
    """
    Example compliance check for RUN service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in run check: {e}")
        return False
```

## Notes
- All functions are based on GCP RUN API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
