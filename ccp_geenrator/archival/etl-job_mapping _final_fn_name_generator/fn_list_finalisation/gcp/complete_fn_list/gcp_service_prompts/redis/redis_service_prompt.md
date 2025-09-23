# GCP REDIS Service Compliance Prompt

## Service Information
- **Service Name**: REDIS
- **Description**: GCP REDIS Service
- **Total Functions**: 3
- **SDK Client**: redis_client
- **Service Type**: other

## Function List
The following 3 functions are available for REDIS compliance checks:

1. `memorystore_redis_backup_frequency_compliant`
2. `memorystore_redis_backup_frequency_meets_retention`
3. `memorystore_redis_automatic_updates_enabled`


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
3. Follow the naming convention: `redis_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def redis_example_function_check():
    """
    Example compliance check for REDIS service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in redis check: {e}")
        return False
```

## Notes
- All functions are based on GCP REDIS API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
