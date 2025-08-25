# GCP KMS Service Compliance Prompt

## Service Information
- **Service Name**: KMS
- **Description**: GCP KMS Service
- **Total Functions**: 38
- **SDK Client**: kms_client
- **Service Type**: security

## Function List
The following 38 functions are available for KMS compliance checks:

1. `cloudbuild_trigger_artifacts_encryption_enabled`
2. `opensearch_domain_encryption_at_rest_enabled`
3. `network_vpc_encryption_for_data_transmission`
4. `network_cdn_encryption_to_custom_origins`
5. `network_cdn_origin_encryption_enforced`
6. `network_cdn_origin_encryption_required`
7. `network_cdn_encryption_to_custom_backends`
8. `network_cdn_traffic_encryption_custom_origins`
9. `network_cdn_traffic_encryption_to_custom_origins`
10. `network_cdn_origin_protocol_encryption`
11. `network_cdn_traffic_encryption_enforced`
12. `network_cdn_encryption_enforced`
13. `network_payment_systems_authentication_encryption`
14. `network_vpc_encryption_enabled`
15. `network_transmission_encryption_ensure`
16. `pubsub_topic_encryption_in_transit_enforced`
17. `pubsub_topic_encryption_google_managed`
18. `pubsub_topic_encryption_with_kms`
19. `cloudbuild_artifact_encryption_enabled`
20. `pubsub_topic_encrypted_with_kms`
21. `secretmanager_secret_cmek_encryption`
22. `marketplace_elasticsearch_node_to_node_encryption_enabled`
23. `memorystore_redis_encryption_at_rest_enabled`
24. `memorystore_redis_replication_encryption_in_transit_enabled`
25. `memorystore_redis_transit_encryption_enabled`
26. `memorystore_redis_encryption_in_transit_enabled`
27. `search_nodes_encryption_enabled`
28. `memorystore_redis_in_transit_encryption_enabled`
29. `filestore_fileshare_encryption_with_kms`
30. `cloudbuild_project_gcs_logs_encryption_enabled`
31. `monitoring_elasticsearch_node_to_node_encryption_enabled`
32. `cloudbuild_gcs_logs_encryption_enabled`
33. `logging_audit_logging_kms_encryption_configured`
34. `logging_audit_logs_encryption_with_kms`
35. `logging_audit_logs_kms_encryption_configured`
36. `logging_configuration_kms_encryption_enabled`
37. `logging_auditlogs_encryption_kms_configured`
38. `logging_cloudkms_encryption_configured`


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
3. Follow the naming convention: `kms_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def kms_example_function_check():
    """
    Example compliance check for KMS service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in kms check: {e}")
        return False
```

## Notes
- All functions are based on GCP KMS API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
