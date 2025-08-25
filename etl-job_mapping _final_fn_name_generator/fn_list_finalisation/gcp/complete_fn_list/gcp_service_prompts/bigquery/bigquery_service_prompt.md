# GCP BIGQUERY Service Compliance Prompt

## Service Information
- **Service Name**: BIGQUERY
- **Description**: GCP BIGQUERY Service
- **Total Functions**: 72
- **SDK Client**: bigquery_client
- **Service Type**: data

## Function List
The following 72 functions are available for BIGQUERY compliance checks:

1. `dns_managed_zones_query_logging_enabled`
2. `dns_public_hosted_zones_query_logging_enabled`
3. `dns_public_managed_zones_query_logging_enabled`
4. `logging_dns_query_logging_enabled`
5. `iam_backup_vault_immutable_policy`
6. `bigquery_table_data_masking_policy`
7. `bigquery_tables_data_masking_policy`
8. `bigquery_datasets_vpc_service_controls_enabled`
9. `bigquery_dataset_authorized_networks_enabled`
10. `network_dns_managed_zones_query_logging_enabled`
11. `dms_migration_jobs_no_public_access`
12. `dms_migration_jobs_non_public`
13. `bigquery_dataset_encryption_with_specified_kms_key`
14. `bigquery_dataset_encryption_with_kms_key`
15. `dms_migration_jobs_logging_enabled_with_valid_severity`
16. `dms_migration_jobs_logging_enabled_valid_severity`
17. `bigquery_dataset_audit_logging_enabled_to_specific_bucket`
18. `bigquery_dataset_audit_logging_configured_to_storage_bucket`
19. `bigquery_dataset_audit_logging_enabled_to_specified_bucket`
20. `bigquery_dataset_audit_logs_exported_to_storage`
21. `bigquery_dataset_disable_legacy_sql`
22. `firestore_bigtable_encryption_with_kms`
23. `firestore_bigtable_tables_pitr_enabled`
24. `firestore_bigtable_table_encrypted_with_kms`
25. `iam_service_accounts_acceptable_use_documented`
26. `bigquery_tables_encrypted_with_cmek`
27. `bigquery_tables_access_control_policies`
28. `bigquery_tables_resident_registration_number_restriction`
29. `bigquery_tables_minimal_personal_info_collection`
30. `bigquery_table_data_classification_verified`
31. `gke_kubelet_make_iptables_util_chains_true`
32. `bigquery_datasets_information_quality_maintenance`
33. `bigquery_dataset_require_ssl`
34. `bigquery_dataset_no_public_access`
35. `bigquery_reservation_capacity_commitment_enabled`
36. `bigquery_dataset_no_public_viewer_access`
37. `bigquery_dataset_encryption_in_transit_required`
38. `bigquery_datasets_enforce_secure_connections`
39. `bigquery_dataset_encryption_at_rest_enabled`
40. `bigquery_datasets_require_ssl`
41. `bigquery_dataset_tls_encryption_required`
42. `bigquery_datasets_automatic_upgrades_enabled`
43. `bigquery_service_enforce_tls_ssl`
44. `bigquery_datasets_encryption_in_transit_required`
45. `bigquery_dataset_automatic_upgrade_enabled`
46. `bigquery_datasets_data_mining_protection`
47. `bigquery_datasets_use_cmek`
48. `bigquery_datasets_use_cmek_encryption`
49. `bigquery_datasets_no_public_access`
50. `bigquery_datasets_default_cmek_specified`
51. `bigquery_data_classification_ensured`
52. `bigquery_datasets_encryption_cmek_enabled`
53. `bigquery_datasets_maintain_processing_records`
54. `bigquery_datasets_minimal_personal_info_collection`
55. `bigquery_datasets_consent_management`
56. `bigquery_datasets_personal_info_accuracy_management`
57. `bigquery_datasets_pseudonymization_procedures_implemented`
58. `bigquery_dataset_encryption_audit_logging_enabled`
59. `bigquery_datasets_audit_logging_enabled`
60. `bigquery_dataset_encryption_and_audit_logging_enabled`
61. `bigquery_dataset_encryption_and_logging_compliance`
62. `bigquery_datasets_audit_logging_enabled_destination_matched`
63. `bigquery_dataset_encryption_and_auditing_enabled`
64. `bigquery_dataset_encryption_and_logging_configured`
65. `bigquery_dataset_encryption_and_audit_logging`
66. `bigquery_dataset_audit_logging_enabled`
67. `bigquery_dataset_audit_logging_enabled_specific_location`
68. `bigquery_dataset_audit_logging_enabled_destination_matched`
69. `bigquery_dataset_encryption_auditing_enabled`
70. `bigquery_dataset_audit_logging_configured`
71. `bigquery_dataset_encryption_and_logging_enabled`
72. `bigquery_log_min_duration_statement_disabled`


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
3. Follow the naming convention: `bigquery_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def bigquery_example_function_check():
    """
    Example compliance check for BIGQUERY service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in bigquery check: {e}")
        return False
```

## Notes
- All functions are based on GCP BIGQUERY API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
