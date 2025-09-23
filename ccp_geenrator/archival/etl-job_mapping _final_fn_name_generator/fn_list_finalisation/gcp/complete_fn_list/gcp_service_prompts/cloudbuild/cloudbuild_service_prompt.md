# GCP CLOUDBUILD Service Compliance Prompt

## Service Information
- **Service Name**: CLOUDBUILD
- **Description**: GCP CLOUDBUILD Service
- **Total Functions**: 1
- **SDK Client**: cloudbuild_client
- **Service Type**: other

## Function List
The following 1 functions are available for CLOUDBUILD compliance checks:

1. `cloudbuild_configuration_privileged_disabled`


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
3. Follow the naming convention: `cloudbuild_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def cloudbuild_example_function_check():
    """
    Example compliance check for CLOUDBUILD service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in cloudbuild check: {e}")
        return False
```

## Notes
- All functions are based on GCP CLOUDBUILD API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
