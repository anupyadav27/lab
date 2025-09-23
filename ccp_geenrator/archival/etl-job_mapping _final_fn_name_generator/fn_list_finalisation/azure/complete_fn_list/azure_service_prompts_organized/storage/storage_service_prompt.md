# Azure Azure Storage Service Compliance Prompt

## Service Information
- **Service Name**: STORAGE
- **Display Name**: Azure Storage
- **Total Functions**: 174
- **Original Categories**: Security, Storage, Unknown, Storage|Security, Storage|Network
- **Categorization Methods**: sdk_example, function_name

## Function List
The following 174 functions are available for Azure Storage compliance checks:

1. `storage_defender_on_state`
2. `storage_secure_transfer_enable`
3. `storage_account_infrastructure_encryption_enabled`
4. `storage_account_access_keys_regeneration`
5. `storage_queue_service_enable_logging_read_write_delete`
6. `storage_shared_access_signature_token_expiry_within_hour`
7. `storage_blobcontainer_public_access_disabled`
8. `storage_account_default_network_access_deny`
9. `storage_account_trusted_services_access_enabled`
10. `storage_blob_service_logging_enabled_read_write_delete`
11. `storage_table_service_logging_enabled_read_write_delete`
12. `storage_account_minimum_tls_version_1_2`
13. `storage_container_activity_logs_not_public`
14. `storage_account_activity_logs_cmk_encryption_enabled`
15. `storage_disk_encryption_with_cmk`
16. `storage_vhd_encryption_enabled`
17. `storage_account_key_rotation_reminders_enabled`
18. `storage_queue_enable_logging_for_read_write_delete`
19. `storage_sas_token_expiry_within_hour`
20. `storage_account_public_network_access_disabled`
21. `storage_account_private_endpoint_access`
22. `storage_blob_soft_delete_enabled`
23. `storage_table_service_enable_logging_for_read_write_delete`
24. `storage_cross_tenant_replication_disabled`
25. `storage_blob_disable_anonymous_access`
26. `storage_account_activity_logs_cmk_encryption`
27. `storage_disk_cmk_encryption`
28. `storage_disk_encryption_with_cmk_unattached`
29. `storage_blob_enforce_https`
30. `storage_account_sftp_unencrypted_connections`
31. `storage_blob_access_public_access_disabled`
32. `storage_account_public_access_block_configured`
33. `storage_blob_access_public_disabled`
34. `storage_account_logging_enabled`
35. `storage_managed_disk_snapshot_no_public_access`
36. `storage_files_access_points_enforced_root_directory`
37. `storage_files_access_points_enforce_user_identity`
38. `storage_fileshare_netappfilesystem_backup_plan_coverage`
39. `storage_fileshare_netappfile_backup_plan_coverage`
40. `storage_blob_container_backup_policy_coverage`
41. `storage_container_policy_cross_tenant_permission_limit`
42. `storage_account_event_grid_notifications_enabled`
43. `storage_blob_enforce_secure_transfer`
44. `storage_managed_disks_default_encryption`
45. `storage_files_encryption_key_vault_managed_keys`
46. `storage_managed_disks_encryption_key_compliance`
47. `storage_blob_container_encryption_enabled_or_deny_unencrypted_put_object`
48. `storage_account_container_no_user_acl`
49. `storage_account_container_access_restriction`
50. `storage_container_policy_cross_tenant_permission_limitation`
51. `storage_manageddisks_default_encryption_enabled`
52. `storage_managed_disk_encryption_with_cmk`
53. `storage_blob_container_default_encryption_enabled_or_deny_unencrypted_put`
54. `storage_container_policy_cross_tenant_permission_restriction`
55. `storage_manageddisk_snapshot_private_access`
56. `storage_backup_transfer_detection`
57. `storage_cloud_storage_no_public_unauthenticated_access`
58. `storage_information_repositories_external_sharing_disable`
59. `storage_file_data_destruction_prevention`
60. `storage_data_encryption_prevent_adversaries`
61. `storage_cloud_infrastructure_discovery_restriction`
62. `storage_records_protection_status`
63. `storage_media_life_cycle_managed_according_to_org_classification`
64. `storage_media_data_removal_before_disposal`
65. `storage_information_deletion_on_requirement_end`
66. `storage_backup_maintenance_and_testing_frequency`
67. `storage_protected_information_assets_role_based_access_control`
68. `storage_application_restriction_enforced_software_change_detection_enabled_change_control_process_defined_antivirus_anti_malware_implementation_scanned_assets_for_malware`
69. `storage_environment_restore_update_patch_config`
70. `storage_confidential_info_retention_protection`
71. `storage_confidential_info_destruction_end_of_retention`
72. `storage_encryption_policies_compliance_with_legal_requirements`
73. `storage_test_data_protection_measures`
74. `storage_backup_procedures_implementation_status`
75. `storage_log_retention_secure_management`
76. `storage_information_assets_secure_reuse_disposal`
77. `storage_removable_media_secure_location`
78. `storage_policy_retention_destruction_safety_completeness`
79. `storage_personal_info_limit_retention_separation`
80. `storage_procedure_data_restoration_implementation`
81. `storage_ephi_transmission_security_guard`
82. `storage_healthinfo_secure_transmission_tracking`
83. `storage_server_patch_status_tracking_defender_antivirus_protection`
84. `storage_backup_periodic_offline`
85. `storage_backup_audit_records_weekly_different_system`
86. `storage_system_daily_incremental_weekly_full_backup`
87. `storage_backup_protection_status`
88. `azure_storage_security_attribute_association`
89. `azure_storage_public_access_review`
90. `azure_storage_allocate_audit_log_capacity`
91. `azure_storage_pan_detection_preprod`
92. `azure_storage_media_physical_security`
93. `azure_storage_offline_backup_security`
94. `azure_storage_audit_log_access_control`
95. `azure_storage_file_integrity_monitoring`
96. `azure_storage_pan_detection_response`
97. `azure_storage_identify_sensitive_data`
98. `azure_storage_sensitive_data_identification`
99. `azure_storage_sensitive_data_location_identification`
100. `azure_security_sensitive_data_storage_location`
101. `azure_security_sensitive_data_storage_location_identification`
102. `azure_storage_sensitive_data_storage_location`
103. `azure_storage_default_sas_token_replacement`
104. `azure_storage_default_sas_token_check`
105. `azure_storage_limit_resource_access`
106. `azure_storage_sensitive_data_retention_period`
107. `azure_storage_sensitive_data_retention_justification`
108. `azure_storage_sensitive_data_debugging_protection`
109. `azure_storage_sensitive_data_user_configurable_retention`
110. `azure_storage_sensitive_data_retention_limit`
111. `azure_storage_sensitive_data_deletion_after_debugging`
112. `azure_storage_sensitive_data_retention_control`
113. `azure_storage_sensitive_data_deletion_after_closure`
114. `azure_storage_data_retention_configurable`
115. `azure_storage_data_retention_justification`
116. `azure_storage_debugging_data_protection`
117. `azure_storage_debugging_data_removal`
118. `azure_storage_transient_data_deletion_trigger`
119. `azure_storage_transient_data_retention_justification`
120. `azure_storage_transient_data_in_memory_check`
121. `azure_storage_debugging_state_termination`
122. `azure_storage_transient_data_retention_limit`
123. `azure_storage_secure_transient_data_deletion`
124. `azure_storage_transient_data_retention_control`
125. `azure_storage_transient_data_secure_deletion`
126. `azure_storage_data_encryption_at_rest`
127. `azure_storage_data_encryption_in_transit`
128. `azure_storage_data_encryption_verification`
129. `azure_storage_data_encryption_check`
130. `azure_storage_secure_data_deletion`
131. `azure_storage_data_residue_forensic_check`
132. `azure_storage_detect_data_residue`
133. `azure_storage_secure_deletion`
134. `azure_storage_check_residual_data`
135. `azure_storage_transient_data_deletion`
136. `azure_storage_swap_file_data_cleanup`
137. `azure_storage_transient_data_deletion_verification`
138. `azure_storage_data_structure_analysis`
139. `azure_storage_swap_file_encryption`
140. `azure_storage_data_leakage_prevention`
141. `azure_storage_sensitive_data_encryption_check`
142. `azure_storage_encryption_verification`
143. `azure_storage_index_token_generation_verification`
144. `azure_storage_tokenization_validation`
145. `azure_storage_sensitive_data_encryption`
146. `azure_storage_data_transmission_encryption_check`
147. `azure_storage_data_encryption_pre_transmission`
148. `azure_storage_asset_access_tracking`
149. `azure_storage_activity_record_protection`
150. `azure_storage_external_logging_system_integration`
151. `azure_storage_activity_records_protection`
152. `azure_storage_secure_activity_records`
153. `azure_storage_append_only_access_control`
154. `azure_storage_unique_dataset_name_protection`
155. `azure_storage_dataset_integrity_check`
156. `azure_storage_prevent_overwrite_existing_datasets`
157. `azure_storage_handle_dataset_access_failure`
158. `azure_storage_sensitive_data_retention_check`
159. `azure_storage_secure_delete_cardholder_data`
160. `azure_storage_mask_pan_display`
161. `azure_storage_render_pan_unreadable`
162. `azure_storage_prevent_pan_correlation`
163. `azure_storage_secure_deletion_after_retention`
164. `azure_storage_prevent_pan_reconstruction`
165. `azure_storage_secure_deletion_after_retention_period`
166. `azure_storage_token_truncate_pan_correlation_prevention`
167. `azure_storage_pan_masking`
168. `azure_storage_pan_unreadable_storage`
169. `azure_storage_pan_unreadable_export`
170. `azure_storage_secure_deletion_guidance`
171. `azure_storage_data_deletion_after_retention_period`
172. `azure_storage_account_data_sharing_verification`
173. `azure_storage_file_signature_verification`
174. `azure_storage_blob_cryptographic_signature_check`


## Compliance Framework Coverage
This service supports compliance checks for:
- **NIST Cybersecurity Framework**
- **PCI DSS v4.0**
- **ISO 27001**
- **SOC 2**
- **GDPR**
- **HIPAA** (where applicable)
- **Azure Security Benchmark**

## Usage Instructions
1. Use the function names above to create compliance checks
2. Each function should be implemented as a separate compliance rule
3. Follow the naming convention: `storage_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def storage_example_function_check():
    """
    Example compliance check for Azure Storage service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.storage import StorageManagementClient
        
        # credential = DefaultAzureCredential()
        # client = StorageManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in storage check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Storage
- **SDK Namespace**: azure.mgmt.storage
- **Client Class**: StorageManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Storage API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
