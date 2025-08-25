# Azure Azure Identity & Access Management Service Compliance Prompt

## Service Information
- **Service Name**: IDENTITY
- **Display Name**: Azure Identity & Access Management
- **Total Functions**: 204
- **Original Categories**: Identity, Unknown, Identity|Compute
- **Categorization Methods**: sdk_example, function_name

## Function List
The following 204 functions are available for Azure Identity & Access Management compliance checks:

1. `identity_privileged_user_mfa_enabled`
2. `identity_non_privileged_user_mfa_enabled`
3. `identity_auth_mfa_trusted_devices_disabled`
4. `identity_named_locations_defined`
5. `identity_administrative_groups_multi_factor_authentication_policy_exists`
6. `identity_user_mfa_policy_exists`
7. `identity_signin_require_mfa_for_risky`
8. `identity_guest_users_reviewed_regularly`
9. `identity_organization_enforce_bad_password_list`
10. `identity_user_consent_disallow_user_consent`
11. `identity_policy_user_consent_allow_for_verified_publishers`
12. `identity_accesspane_restrict_user_access_to_groups_enabled`
13. `identity_role_assignments_owner_set`
14. `identity_tenant_non_admin_create_restriction_enabled`
15. `identity_guest_users_review_frequency`
16. `identity_user_consent_disallow_consent`
17. `identity_policy_allow_user_consent_for_verified_publishers`
18. `identity_accesspane_restrict_user_access_to_groups`
19. `identity_global_administrator_less_than_five`
20. `identity_non_privileged_user_multi_factor_auth_enabled`
21. `identity_trusted_locations_defined`
22. `identity_admin_group_multi_factor_authentication_policy_exists`
23. `identity_admin_portal_require_mfa`
24. `identity_role_assignments_owner`
25. `identity_virtual_machine_mfa_enabled_access`
26. `azure_identity_global_admin_mfa_hardware_only`
27. `identity_account_manipulation_prevention`
28. `identity_user_creation_prevented`
29. `identity_authentication_mfa_enforcement`
30. `azure_identity_password_brute_force_prevention`
31. `identity_webapp_secure_session_cookies_tokens`
32. `identity_password_policy_enforcement`
33. `identity_role_segregation_enforced`
34. `management_personnel_information_security_policy_compliance`
35. `identity_organization_contact_maintenance_special_interest_groups`
36. `identity_compliance_rules_implementation_status`
37. `identity_personnel_assets_returned_on_termination`
38. `identity_access_control_established`
39. `identity_management_mfa_enforcement`
40. `identity_access_rights_provision_review_modify_remove`
41. `identity_privacy_pii_protection_compliance`
42. `identity_policy_violation_disciplinary_process_formalized_communicated`
43. `identity_user_info_security_responsibilities_enforcement`
44. `identity_personnel_confidentiality_agreement_compliance`
45. `identity_remote_access_security_measures`
46. `identity_personnel_security_event_report_timely`
47. `identity_policy_enforcement_clear_desk_screen_rules`
48. `identity_privileged_access_rights_restriction_management`
49. `identity_topic_policy_access_control_restriction`
50. `identity_code_resources_managed_access`
51. `identity_authentication_secure_state`
52. `identity_system_clocks_synchronised_to_approved_sources`
53. `identity_cryptography_key_management_implementation`
54. `identity_outsourced_system_development_directed_monitored_reviewed`
55. `identity_user_access_authorization_and_removal`
56. `identity_data_protection_officer_maintain_processing_activities_record`
57. `identity_management_system_ceo_participation`
58. `identity_executive_roles_info_protection_allocation`
59. `identity_information_protection_classification_criteria_maintenance`
60. `identity_info_assets_handling_procedures_established_managed`
61. `identity_personnel_security_confidentiality_agreement_signed`
62. `identity_management_system_policy_training_plan_operational`
63. `identity_policy_violation_procedures_established`
64. `identity_outsourcing_protection_measures_established`
65. `identity_user_security_measures_implementation`
66. `identity_protected_areas_access_restriction_and_log_review`
67. `azure_ad_user_unique_and_unpredictable_identifiers`
68. `identity_user_password_management_procedures_implementation`
69. `identity_account_privilege_minimal_separate_control`
70. `identity_user_account_access_record_review`
71. `azure_identity_user_access_restriction_control`
72. `identity_application_access_rights_minimized`
73. `identity_privacy_personal_information_lawful_fair_collection`
74. `identity_data_protection_sensitive_info_consent_obtained`
75. `identity_data_protection_legal_basis_and_security_measures`
76. `identity_third_party_processing_disclosure_required`
77. `identity_data_subject_rights_ensure_prompt_processing`
78. `identity_data_subjects_notification_frequency`
79. `identity_accesscontrol_ephi_access_appropriate`
80. `identity_user_access_rights_modification`
81. `identity_login_attempts_reporting_procedures`
82. `identity_auth_password_secure_management`
83. `identity_system_access_rights_granted_only`
84. `identity_user_identity_unique_naming`
85. `identity_device_admin_rights_disallow_need_to_know_do_basis`
86. `identity_password_complex_lengthy_unique`
87. `identity_system_account_automated_management`
88. `identity_system_account_monitor_atypical_use`
89. `identity_system_account_management_procedures`
90. `identity_system_account_monitoring`
91. `identity_account_management_frequency_review`
92. `identity_user_account_auto_disable_after_90_days`
93. `information_system_enforce_approved_authorizations`
94. `information_system_authorization_enforcement_on_flow_control_policies`
95. `identity_system_access_authorization_separation_of_duties`
96. `information_system_privileged_functions_protection`
97. `identity_user_least_privilege`
98. `identity_user_information_sharing_decision_assistance`
99. `identity_system_user_authentication`
100. `identity_system_password_complexity_lifetime_restriction`
101. `identity_password_authenticators_strength_satisfies_requirements`
102. `identity_system_unique_authentication`
103. `identity_systemdevlifecycle_roles_responsibilities_integration`
104. `azure_ad_account_provisioning`
105. `azure_ad_account_activity_monitoring`
106. `azure_ad_access_policy_enforcement`
107. `azure_ad_role_separation_enforcement`
108. `azure_ad_user_role_assignment_audit`
109. `azure_ad_account_lockout_policy`
110. `azure_ad_login_banner_configuration`
111. `azure_ad_last_logon_notification`
112. `azure_ad_concurrent_session_limit`
113. `azure_ad_user_proximity_lock`
114. `azure_ad_user_session_termination`
115. `azure_ad_user_action_without_authentication`
116. `azure_ad_access_control_decision_enforcement`
117. `azure_ad_assign_authorizing_official`
118. `azure_ad_role_assignment_tracking`
119. `azure_ad_default_account_management`
120. `azure_ad_test_account_cleanup`
121. `azure_ad_access_control_model_definition`
122. `azure_ad_shared_id_usage_monitoring`
123. `azure_ad_shared_id_exception_management`
124. `azure_ad_unique_authentication_per_customer`
125. `azure_ad_user_id_lifecycle_management`
126. `azure_ad_terminate_user_access`
127. `azure_ad_inactive_account_management`
128. `azure_ad_third_party_access_time_restriction`
129. `azure_ad_third_party_access_monitoring`
130. `azure_ad_session_idle_timeout_enforcement`
131. `azure_ad_multi_factor_authentication_enforcement`
132. `azure_ad_authentication_factor_encryption`
133. `azure_ad_user_identity_verification_before_auth_factor_change`
134. `azure_ad_dynamic_security_posture_analysis`
135. `azure_ad_customer_password_guidance`
136. `azure_ad_individual_authentication_factor_assignment`
137. `azure_ad_mfa_non_console_access`
138. `azure_ad_mfa_enforcement_non_console_access`
139. `azure_ad_mfa_enforcement_remote_access`
140. `azure_ad_mfa_configuration_protection`
141. `azure_ad_system_account_interactive_login_restriction`
142. `azure_ad_physical_access_management`
143. `azure_ad_access_revocation_on_termination`
144. `azure_ad_visitor_access_management`
145. `azure_ad_visitor_badge_deactivation`
146. `azure_ad_visitor_log_management`
147. `azure_ad_audit_log_account_changes`
148. `azure_ad_account_authentication_credentials_identification`
149. `azure_ad_identify_sensitive_accounts`
150. `azure_ad_list_user_accounts`
151. `azure_ad_list_authentication_credentials`
152. `azure_ad_check_default_credentials`
153. `azure_ad_check_default_credential_usage`
154. `azure_ad_default_credential_replacement`
155. `azure_ad_default_credential_check`
156. `azure_ad_default_credentials_check`
157. `azure_ad_limit_privilege_access`
158. `azure_ad_default_account_privilege_verification`
159. `azure_ad_api_interface_protection`
160. `azure_ad_default_account_exposed_interface_protection`
161. `azure_ad_user_input_auth_verification`
162. `azure_ad_critical_asset_role_authentication_requirements`
163. `azure_ad_external_mechanism_authentication_guidance`
164. `azure_ad_critical_asset_authentication_enforcement`
165. `azure_ad_sensitive_data_authentication_asset_identification`
166. `azure_ad_critical_asset_authentication`
167. `azure_ad_authentication_mechanism_verification`
168. `azure_ad_external_mechanism_guidance`
169. `azure_ad_unique_identification_enforcement`
170. `azure_ad_unique_identification_guidance`
171. `azure_ad_api_unique_identification_enforcement`
172. `azure_ad_authentication_parameters_unique`
173. `azure_ad_authentication_method_vulnerability_check`
174. `azure_ad_authentication_method_robustness_check`
175. `azure_ad_authentication_method_implementation_check`
176. `azure_ad_authentication_method_evaluation`
177. `azure_ad_authentication_method_implementation_verification`
178. `azure_ad_authentication_strength_evaluation`
179. `azure_ad_authentication_robustness_test`
180. `azure_ad_critical_assets_access_verification`
181. `azure_ad_user_activity_tracking`
182. `azure_ad_authentication_parameters_protection`
183. `azure_ad_authenticate_log_server_access`
184. `azure_ad_enforce_strong_authentication_methods`
185. `azure_ad_enforce_secure_area_authentication`
186. `azure_ad_enforce_fine_grained_access_control`
187. `azure_ad_enforce_authorization_per_request`
188. `azure_ad_enforce_secure_area_access_control`
189. `azure_ad_authenticate_sensitive_functions_resources`
190. `azure_ad_authenticate_user_access`
191. `azure_ad_enforce_authentication_decisions`
192. `azure_ad_authorize_user_access`
193. `azure_ad_enforce_authorization_decisions`
194. `azure_ad_authorize_access_to_interfaces`
195. `azure_ad_authorize_access_to_functions_resources`
196. `azure_ad_enforce_access_control_rules`
197. `azure_ad_sensitive_function_access_authentication`
198. `azure_ad_user_access_authentication`
199. `azure_ad_authentication_strength_check`
200. `azure_ad_secure_area_authentication_enforcement`
201. `azure_ad_authorization_rule_enforcement`
202. `azure_ad_secure_area_access_control_enforcement`
203. `azure_security_file_upload_mitigation`
204. `azure_storage_file_upload_security_controls`


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
3. Follow the naming convention: `identity_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def identity_example_function_check():
    """
    Example compliance check for Azure Identity & Access Management service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.identity import IdentityManagementClient
        
        # credential = DefaultAzureCredential()
        # client = IdentityManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in identity check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Identity & Access Management
- **SDK Namespace**: azure.mgmt.identity
- **Client Class**: IdentityManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Identity & Access Management API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
