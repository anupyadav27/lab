# GCP SOURCEREPO Service Compliance Prompt

## Service Information
- **Service Name**: SOURCEREPO
- **Description**: GCP SOURCEREPO Service
- **Total Functions**: 2
- **SDK Client**: sourcerepo_client
- **Service Type**: other

## Function List
The following 2 functions are available for SOURCEREPO compliance checks:

1. `source_repositories_url_no_signin_credentials`
2. `source_repositories_url_no_credentials`


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
3. Follow the naming convention: `sourcerepo_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def sourcerepo_example_function_check():
    """
    Example compliance check for SOURCEREPO service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in sourcerepo check: {e}")
        return False
```

## Notes
- All functions are based on GCP SOURCEREPO API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
