# GCP PUBSUB Service Compliance Prompt

## Service Information
- **Service Name**: PUBSUB
- **Description**: GCP PUBSUB Service
- **Total Functions**: 13
- **SDK Client**: pubsub_client
- **Service Type**: other

## Function List
The following 13 functions are available for PUBSUB compliance checks:

1. `gmail_enhanced_pre_delivery_message_scanning_enabled`
2. `pubsub_subscription_audit_logging_enabled`
3. `pubsub_service_logging_enabled`
4. `pubsub_topic_delivery_status_logging_enabled`
5. `logging_pubsub_audit_logging_enabled`
6. `pubsub_topic_logging_enabled`
7. `logging_pubsub_audit_logs_enabled`
8. `pubsub_subscription_logging_enabled`
9. `pubsub_topic_audit_logging_enabled`
10. `pubsub_topic_audit_logs_enabled`
11. `pubsub_service_audit_logging_enabled`
12. `pubsub_topic_logging_delivery_status_enabled`
13. `logging_log_min_messages_set_to_error`


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
3. Follow the naming convention: `pubsub_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def pubsub_example_function_check():
    """
    Example compliance check for PUBSUB service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in pubsub check: {e}")
        return False
```

## Notes
- All functions are based on GCP PUBSUB API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
