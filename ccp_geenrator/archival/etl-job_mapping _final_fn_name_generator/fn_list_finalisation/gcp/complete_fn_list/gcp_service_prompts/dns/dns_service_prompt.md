# GCP DNS Service Compliance Prompt

## Service Information
- **Service Name**: DNS
- **Description**: GCP DNS Service
- **Total Functions**: 30
- **SDK Client**: dns_client
- **Service Type**: networking

## Function List
The following 30 functions are available for DNS compliance checks:

1. `logging_audit_records_weekly_backup`
2. `workspace_email_domain_dmarc_configured`
3. `workspace_domain_delegation_review`
4. `workspace_email_domain_spf_record_configured`
5. `logging_cloud_search_domain_logging_enabled`
6. `logging_dns_queries_enabled`
7. `drive_domain_document_sharing_allowlist`
8. `drive_file_share_warning_allowlisted_domain`
9. `chat_external_domain_restriction`
10. `cloudsearch_domain_https_tls_enforced`
11. `cloudsearch_domain_https_enforced`
12. `search_domain_https_enforced`
13. `user_warning_prompt_untrusted_domains`
14. `gsuite_domain_spoofing_protection_enabled`
15. `dns_zone_dnssec_rsasha1_not_used`
16. `cloud_dns_dnssec_enabled`
17. `mail_domain_dkim_enabled`
18. `elastic_domain_fine_grained_access_control_enabled`
19. `elasticsearch_domain_fine_grained_access_control_enabled`
20. `network_cloud_search_domain_private`
21. `network_vpc_private_dns_enabled`
22. `network_vpc_dns_resolution_enabled`
23. `network_dns_dnssec_enabled`
24. `network_dnssec_algorithm_recommended`
25. `network_vpc_dns_logging_enabled`
26. `network_dnssec_algorithm_recommendation`
27. `network_vpc_secure_zone_data_control`
28. `logging_audit_logs_continuous_recording`
29. `logging_information_system_activity_recording`
30. `logging_audit_records_processing_capability`


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
3. Follow the naming convention: `dns_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def dns_example_function_check():
    """
    Example compliance check for DNS service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in dns check: {e}")
        return False
```

## Notes
- All functions are based on GCP DNS API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
