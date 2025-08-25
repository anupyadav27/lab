# GCP DATASTREAM Service Compliance Prompt

## Service Information
- **Service Name**: DATASTREAM
- **Description**: GCP DATASTREAM Service
- **Total Functions**: 4
- **SDK Client**: datastream_client
- **Service Type**: data

## Function List
The following 4 functions are available for DATASTREAM compliance checks:

1. `gmail_send_tls_connection_enabled`
2. `dms_connection_profiles_non_public`
3. `streaming_connection_idle_timeout_set`
4. `dms_connections_ssl_configured`


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
3. Follow the naming convention: `datastream_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def datastream_example_function_check():
    """
    Example compliance check for DATASTREAM service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in datastream check: {e}")
        return False
```

## Notes
- All functions are based on GCP DATASTREAM API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
