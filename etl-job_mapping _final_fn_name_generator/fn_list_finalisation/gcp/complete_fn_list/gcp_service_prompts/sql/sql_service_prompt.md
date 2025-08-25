# GCP SQL Service Compliance Prompt

## Service Information
- **Service Name**: SQL
- **Description**: GCP SQL Service
- **Total Functions**: 63
- **SDK Client**: sqladmin_client
- **Service Type**: data

## Function List
The following 63 functions are available for SQL compliance checks:

1. `sql_backups_non_public`
2. `sql_databases_included_in_backup_plans`
3. `sql_database_backups_encrypted`
4. `sql_database_automated_backups_enabled`
5. `firestore_database_backups_non_public`
6. `firestore_database_network_encryption_enabled`
7. `sql_database_users_default_only`
8. `sql_mysql_insights_enabled`
9. `sql_mysql_audit_logging_enabled`
10. `cloudsql_redis_ssl_encryption_enabled`
11. `sql_mysql_audit_log_insights_enabled`
12. `cloudsql_postgresql_enable_pgaudit_flag`
13. `sql_database_trace_flag_3625_on`
14. `sql_database_contained_authentication_disabled`
15. `sql_cloudsql_cross_db_ownership_chaining_off`
16. `sql_database_no_public_ip_whitelist`
17. `sql_database_no_public_ip`
18. `sql_postgresql_log_error_verbosity_default_or_stricter`
19. `sql_postgresql_log_connections_enabled`
20. `sql_postgresql_log_disconnections_enabled`
21. `sql_postgresql_log_statement_flag_set`
22. `sql_postgresql_log_min_messages_warning`
23. `sql_postgresql_log_min_error_statement_set_to_error`
24. `sql_postgresql_log_min_duration_statement_disabled`
25. `cloudsql_postgresql_enable_pgaudit_on`
26. `sql_cloudsqlserver_external_scripts_disabled`
27. `sql_cloud_sql_server_remote_access_off`
28. `sql_postgresql_log_error_verbosity_default`
29. `sql_database_user_connections_non_limiting`
30. `sql_database_user_options_disabled`
31. `sql_cloudsql_contained_database_authentication_off`
32. `sql_database_user_connections_limit_set`
33. `firestore_database_pitr_enabled`
34. `firestore_database_retention_period_enforced`
35. `firestore_database_retention_period_compliant`
36. `firestore_database_retention_period_set`
37. `firestore_spanner_databases_pitr_enabled`
38. `firestore_database_encryption_enabled`
39. `firestore_database_tls_enabled`
40. `firestore_database_encryption_with_kms`
41. `firestore_database_encryption_status`
42. `firestore_database_encryption_status_enabled`
43. `firestore_database_transport_security_enabled`
44. `firestore_databases_encryption_enabled`
45. `logging_cloudsql_logging_enabled_with_valid_severity`
46. `firestore_database_stackdriver_logging_enabled`
47. `sql_mysql_log_export_configured`
48. `logging_database_migration_logging_enabled_with_valid_severity`
49. `sql_logs_enabled`
50. `sql_replication_logging_enabled_valid_severity`
51. `sql_mysql_audit_logs_enabled`
52. `logging_cloudsql_audit_logs_severity_enabled`
53. `sql_mysql_log_publishing_enabled`
54. `sql_mysql_audit_logs_exported`
55. `sql_databases_logging_enabled`
56. `firestore_database_audit_logging_enabled`
57. `sql_mysql_log_export_enabled`
58. `logging_cloudsql_auditlogs_severity_enabled`
59. `sql_mysql_audit_logs_export_configured`
60. `sql_replication_logging_severity_enabled`
61. `cloudsql_mysql_log_export_configured`
62. `sql_database_logging_enabled`
63. `logging_sql_log_statement_ddl_recommended`


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
3. Follow the naming convention: `sql_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def sql_example_function_check():
    """
    Example compliance check for SQL service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in sql check: {e}")
        return False
```

## Notes
- All functions are based on GCP SQL API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
