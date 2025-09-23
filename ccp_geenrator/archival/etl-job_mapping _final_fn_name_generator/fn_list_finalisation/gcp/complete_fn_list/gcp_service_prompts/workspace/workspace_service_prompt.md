# GCP WORKSPACE Service Compliance Prompt

## Service Information
- **Service Name**: WORKSPACE
- **Description**: GCP WORKSPACE Service
- **Total Functions**: 16
- **SDK Client**: admin_client
- **Service Type**: workspace

## Function List
The following 16 functions are available for WORKSPACE compliance checks:

1. `workspace_directory_external_access_restricted`
2. `workspace_external_groups_access_restricted`
3. `workspace_mail_protection_against_untrusted_attachments`
4. `workspace_email_anomalous_attachment_protection_enabled`
5. `workspace_mail_encrypted_attachments_protection_enabled`
6. `calendar_web_offline_disabled`
7. `docs_add_ons_disabled`
8. `gmail_pop_imap_access_disabled`
9. `gmail_external_recipient_warnings_enabled`
10. `chat_hangouts_external_filesharing_disabled`
11. `chat_hangouts_internal_filesharing_disabled`
12. `chat_hangouts_external_spaces_restricted`
13. `gmail_spam_filter_internal_senders`
14. `drive_desktop_access_disabled`
15. `chat_incoming_webhooks_disabled`
16. `gmail_quarantine_admin_notifications_enabled`


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
3. Follow the naming convention: `workspace_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def workspace_example_function_check():
    """
    Example compliance check for WORKSPACE service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in workspace check: {e}")
        return False
```

## Notes
- All functions are based on GCP WORKSPACE API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
