# GCP LOADBALANCER Service Compliance Prompt

## Service Information
- **Service Name**: LOADBALANCER
- **Description**: GCP LOADBALANCER Service
- **Total Functions**: 1
- **SDK Client**: compute_client
- **Service Type**: networking

## Function List
The following 1 functions are available for LOADBALANCER compliance checks:

1. `gmail_user_auto_forwarding_disabled`


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
3. Follow the naming convention: `loadbalancer_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def loadbalancer_example_function_check():
    """
    Example compliance check for LOADBALANCER service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in loadbalancer check: {e}")
        return False
```

## Notes
- All functions are based on GCP LOADBALANCER API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
