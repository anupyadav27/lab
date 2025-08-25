# GCP STORAGE Service Compliance Prompt

## Service Information
- **Service Name**: STORAGE
- **Description**: GCP STORAGE Service
- **Total Functions**: 152
- **SDK Client**: storage_client
- **Service Type**: storage

## Function List
The following 152 functions are available for STORAGE compliance checks:

1. `storage_objects_restrict_operational_access`
2. `storage_backup_iam_policy_prevent_deletion`
3. `storage_bucket_retention_policy_minimum_period`
4. `storage_backup_retention_policy_minimum_period`
5. `storage_bucket_versioning_lifecycle_policy_configured`
6. `storage_bucket_policy_restrict_blocklisted_actions`
7. `storage_bucket_policy_restrict_inter_account_permissions`
8. `storage_bucket_https_policy_enforced`
9. `storage_object_retention_policy_compliance`
10. `storage_bucket_versioning_lifecycle_policy_enabled`
11. `storage_bucket_lifecycle_policy_enabled`
12. `storage_bucket_retention_policy_enforced`
13. `storage_backup_policy_frequency_and_retention_compliance`
14. `storage_backup_retention_policy_compliant`
15. `storage_bucket_retention_policy_compliance`
16. `storage_bucket_versioning_retention_policy_configured`
17. `storage_backup_vault_prevent_deletion_policy`
18. `storage_bucket_iam_policy_prevent_deletion`
19. `storage_bucket_policy_restrict_cross_project_actions`
20. `storage_bucket_iam_policy_prevent_object_deletion`
21. `storage_bucket_policy_no_inter_account_permissions`
22. `storage_bucket_iam_policy_restrict_cross_project_actions`
23. `storage_bucket_iam_policy_restrict_blocklisted_actions`
24. `storage_bucket_iam_policy_restrict_inter_account_permissions`
25. `storage_bucket_policy_no_inter_project_permissions`
26. `storage_backup_iam_policy_protect_deletion`
27. `storage_backup_retention_policy_enforced`
28. `storage_buckets_https_only_policy`
29. `storage_bucket_policy_enforce_ssl_tls`
30. `storage_object_retention_policy_enforced`
31. `storage_bucket_backup_retention_policy_compliance`
32. `storage_backup_vault_deny_policy_enforced`
33. `storage_bucket_policy_restrict_cross_account_actions`
34. `storage_bucket_policy_restrict_cross_project_blocklist_actions`
35. `storage_bucket_iam_policy_absent`
36. `storage_bucket_policy_no_interproject_permissions`
37. `storage_bucket_retention_policy_enabled`
38. `storage_bucket_retention_policy_configured_with_lock`
39. `storage_objects_retention_policy_enforced`
40. `storage_bucket_lifecycle_rule_configured`
41. `storage_bucket_permissions_restrict_inter_account`
42. `storage_bucket_disallow_acl_user_permissions`
43. `logging_storage_iam_permission_change_alerts_exist`
44. `storage_project_public_access_prevention_configured`
45. `cloudbuild_project_storage_logs_encryption_enabled`
46. `storage_project_public_access_prevention`
47. `gmail_comprehensive_mail_storage_enabled`
48. `gke_secrets_external_storage`
49. `external_secret_storage_considered`
50. `secret_manager_external_secret_storage`
51. `kubernetes_external_secret_storage`
52. `storage_bucket_iam_change_alert`
53. `monitoring_storage_bucket_iam_change_alert`
54. `storage_objects_confidentiality_protection`
55. `storage_objects_confidential_destruction`
56. `storage_bucket_encryption_enabled`
57. `storage_bucket_iam_https_required`
58. `storage_bucket_endpoint_protocol_gs`
59. `storage_access_points_block_public_access_enabled`
60. `storage_bucket_no_public_access`
61. `storage_bucket_no_public_read_access`
62. `storage_bucket_no_public_write_access`
63. `storage_bucket_public_access_prevention_enabled`
64. `storage_bucket_public_access_restricted`
65. `storage_bucket_uniform_access_enabled`
66. `storage_bucket_uniform_access_controls_enabled`
67. `storage_bucket_logging_enabled`
68. `storage_bucket_object_versioning_enabled`
69. `storage_buckets_public_access_restricted`
70. `storage_bucket_backup_plan_enforced`
71. `cdn_distribution_storage_origin_service_account_configured`
72. `storage_bucket_non_public_access`
73. `storage_bucket_versioning_enabled_with_minimum_retention`
74. `storage_bucket_object_change_notifications_enabled`
75. `storage_bucket_notifications_enabled`
76. `storage_bucket_protocol_no_ftp`
77. `storage_bucket_ssl_tls_enforced`
78. `storage_recovery_point_retention_compliance`
79. `storage_backup_plan_frequency_and_retention_compliance`
80. `firestore_database_storage_encryption_enabled`
81. `storage_bucket_default_encryption_enabled`
82. `storage_bucket_encryption_with_kms`
83. `storage_bucket_enforce_ssl_tls`
84. `storage_bucket_no_user_acl`
85. `storage_bucket_access_restricted`
86. `storage_bucket_no_user_acls`
87. `storage_bucket_object_versioning_enabled_with_iam_policies`
88. `storage_bucket_versioning_authentication_required`
89. `storage_bucket_versioning_enabled_minimum_retention`
90. `storage_bucket_notifications_configured`
91. `storage_server_protocol_ftp_disabled`
92. `cloudbuild_storage_logs_encryption_enabled`
93. `storage_bucket_disallow_user_acls`
94. `storage_bucket_encrypted_with_kms`
95. `storage_bucket_object_versioning_enabled_iam_configured`
96. `storage_bucket_information_labelling_procedures`
97. `storage_objects_protected_from_unauthorized_access`
98. `storage_media_lifecycle_management`
99. `storage_objects_deletion_when_no_longer_required`
100. `storage_buckets_backup_maintenance`
101. `storage_objects_protection_management`
102. `storage_buckets_intellectual_property_protection`
103. `storage_buckets_protected_from_unauthorized_access`
104. `storage_buckets_offsite_protection`
105. `storage_objects_protected_management`
106. `storage_objects_cleanup`
107. `storage_buckets_backup_protection`
108. `storage_buckets_backup_enabled`
109. `storage_objects_document_cleanup`
110. `storage_objects_encryption_enabled`
111. `storage_bucket_cross_account_exfiltration_prevention`
112. `storage_objects_automated_collection_prevention`
113. `storage_buckets_external_sharing_disabled`
114. `storage_bucket_data_staging_prevention`
115. `storage_objects_integrity_preserved`
116. `storage_objects_access_restriction`
117. `storage_bucket_cross_account_exfiltration_prevent`
118. `storage_objects_automated_data_collection_prevention`
119. `storage_bucket_external_sharing_disabled`
120. `storage_objects_integrity_ensured`
121. `storage_objects_access_restricted`
122. `storage_buckets_data_minimization_default_access`
123. `storage_buckets_encryption_enforced`
124. `storage_buckets_test_data_protection`
125. `storage_buckets_backup_procedures`
126. `storage_buckets_secure_disposal_procedures`
127. `storage_bucket_secure_removable_media_storage`
128. `storage_buckets_personal_info_management`
129. `storage_objects_separate_personal_information`
130. `storage_objects_data_subject_rights_management`
131. `storage_bucket_ephemeral_encryption`
132. `storage_buckets_maintain_retrievable_copies`
133. `storage_buckets_data_restoration_procedures`
134. `storage_bucket_ephemeral_access_procedure`
135. `storage_buckets_protect_ephi`
136. `storage_bucket_integrity_ensured`
137. `storage_bucket_integrity_protection`
138. `storage_objects_offline_backup`
139. `storage_objects_retention_compliance`
140. `logging_auditlog_cloudstorage_dataevents_enabled`
141. `logging_log_buckets_cmek_encrypted`
142. `logging_log_buckets_encrypted_with_kms_key`
143. `logging_log_bucket_encryption_kms_key`
144. `logging_log_bucket_retention_period_greater_than_minimum`
145. `logging_logbucket_retention_period_greater_than_minimum`
146. `logging_logbucket_retention_period_greater_than_365_days`
147. `logging_log_bucket_retention_period_enforced`
148. `logging_audit_config_storage_data_events_enabled`
149. `logging_auditlog_cloudstorage_data_events_enabled`
150. `logging_log_bucket_retention_period_greater_than_365_days`
151. `logging_logbucket_retention_period_compliant`
152. `logging_metric_filter_alerts_for_storage_iam_changes`


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
3. Follow the naming convention: `storage_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def storage_example_function_check():
    """
    Example compliance check for STORAGE service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in storage check: {e}")
        return False
```

## Notes
- All functions are based on GCP STORAGE API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
