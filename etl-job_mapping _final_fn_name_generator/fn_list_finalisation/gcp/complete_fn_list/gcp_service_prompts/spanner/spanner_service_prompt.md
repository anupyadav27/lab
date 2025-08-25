# GCP SPANNER Service Compliance Prompt

## Service Information
- **Service Name**: SPANNER
- **Description**: GCP SPANNER Service
- **Total Functions**: 1
- **SDK Client**: spanner_client
- **Service Type**: data

## Function List
The following 1 functions are available for SPANNER compliance checks:

1. `firestore_spanner_backups_non_public`


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
3. Follow the naming convention: `spanner_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def spanner_example_function_check():
    """
    Example compliance check for SPANNER service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in spanner check: {e}")
        return False
```

## Notes
- All functions are based on GCP SPANNER API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
