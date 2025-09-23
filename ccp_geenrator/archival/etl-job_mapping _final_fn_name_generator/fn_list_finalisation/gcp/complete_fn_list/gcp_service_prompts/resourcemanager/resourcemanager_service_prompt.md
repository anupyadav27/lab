# GCP RESOURCEMANAGER Service Compliance Prompt

## Service Information
- **Service Name**: RESOURCEMANAGER
- **Description**: GCP RESOURCEMANAGER Service
- **Total Functions**: 7
- **SDK Client**: resourcemanager_client
- **Service Type**: management

## Function List
The following 7 functions are available for RESOURCEMANAGER compliance checks:

1. `search_resources_fine_grained_access_control_enabled`
2. `resource_namespace_boundaries_created`
3. `resource_manager_project_organization_sharing`
4. `resource_manager_project_organization_association`
5. `resource_manager_account_organization_membership`
6. `dlp_project_sensitive_data_discovery_enabled`
7. `cloudbuild_project_privileged_mode_disabled`


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
3. Follow the naming convention: `resourcemanager_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def resourcemanager_example_function_check():
    """
    Example compliance check for RESOURCEMANAGER service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in resourcemanager check: {e}")
        return False
```

## Notes
- All functions are based on GCP RESOURCEMANAGER API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
