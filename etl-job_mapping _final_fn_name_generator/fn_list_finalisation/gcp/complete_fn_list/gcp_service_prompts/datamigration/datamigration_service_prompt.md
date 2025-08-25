# GCP DATAMIGRATION Service Compliance Prompt

## Service Information
- **Service Name**: DATAMIGRATION
- **Description**: GCP DATAMIGRATION Service
- **Total Functions**: 2
- **SDK Client**: datamigration_client
- **Service Type**: data

## Function List
The following 2 functions are available for DATAMIGRATION compliance checks:

1. `datamigration_redis_tls_enabled`
2. `datamigration_redis_tls_ssl_enabled`


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
3. Follow the naming convention: `datamigration_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def datamigration_example_function_check():
    """
    Example compliance check for DATAMIGRATION service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in datamigration check: {e}")
        return False
```

## Notes
- All functions are based on GCP DATAMIGRATION API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
