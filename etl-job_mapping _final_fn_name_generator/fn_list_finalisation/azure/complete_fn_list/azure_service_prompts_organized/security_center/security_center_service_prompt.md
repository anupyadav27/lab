# Azure Azure Security Center Service Compliance Prompt

## Service Information
- **Service Name**: SECURITY_CENTER
- **Display Name**: Azure Security Center
- **Total Functions**: 255
- **Original Categories**: Unknown, Security
- **Categorization Methods**: sdk_example, function_name

## Function List
The following 255 functions are available for Azure Security Center compliance checks:

1. `security_defender_azure_sql_databases_on`
2. `security_defender_containers_enabled`
3. `security_defender_cosmosdb_enabled`
4. `security_defender_cosmosdb_on`
5. `security_defender_for_containers_is_enabled`
6. `security_defender_dns_on`
7. `security_benchmark_policies_not_disabled`
8. `security_defender_easm_enabled`
9. `security_defender_cloud_enabled_central_account`
10. `security_defenses_impairment_prevention`
11. `security_automated_data_collection_detection`
12. `security_software_discovery_controlled_listing`
13. `security_information_classification_based_on_attributes_requirements`
14. `security_supplier_risk_management_procedures_defined_implemented`
15. `security_incident_management_process_definition_communication`
16. `security_event_assessment_categorization`
17. `security_incident_improve_controls`
18. `security_event_evidence_procedure_implementation`
19. `security_info_requirements_identified_documented_updated`
20. `security_secure_areas_entry_controls_protection`
21. `security_physical_design_implementation_status`
22. `security_premises_continuous_monitoring`
23. `security_secure_area_measures_implementation`
24. `security_detection_policies_procedures_tools_implementation_status`
25. `security_risk_assessment_protective_measures_approval`
26. `security_protection_measures_effective_implementation_verification`
27. `security_contract_compliance_inspection`
28. `security_physical_protection_zones_designated_protected`
29. `security_inspection_vulnerability_tracking`
30. `security_incident_response_compliance`
31. `security_antimalware_protection_reporting`
32. `security_incident_response_mitigation_documentation`
33. `security_audit_records_retention_minimum_90_days`
34. `security_incident_handling_automation_enabled`
35. `security_incident_response_automation_increase`
36. `keyvault_cryptographic_keys_managed_according_to_org_requirements`
37. `security_system_component_flaw_remediation_monthly`
38. `security_intrusion_detection_system_configured_state`
39. `security_event_analysis_automation`
40. `security_monitoring_detect_attacks_unauthorized_connections`
41. `integrity_verification_tool_usage_for_software_firmware_info_changes`
42. `security_audit_event_capability`
43. `security_incident_handling_implementation`
44. `azure_security_vulnerability_assessment_plan_update`
45. `azure_security_penetration_testing_schedule`
46. `azure_keyvault_automatic_secret_rotation`
47. `azure_compute_security_parameters_configuration`
48. `azure_keyvault_key_encryption_separation`
49. `azure_keyvault_cryptographic_architecture_report`
50. `azure_keyvault_secure_key_storage`
51. `azure_keyvault_cleartext_access_restriction`
52. `azure_keyvault_minimize_key_locations`
53. `azure_keyvault_generate_strong_keys`
54. `azure_keyvault_secure_key_distribution`
55. `azure_keyvault_manage_key_cryptoperiod`
56. `azure_keyvault_retire_replace_destroy_keys`
57. `azure_keyvault_key_split_knowledge_enforcement`
58. `azure_keyvault_prevent_key_substitution`
59. `azure_keyvault_key_custodian_acknowledgement`
60. `azure_keyvault_customer_key_guidance_distribution`
61. `azure_security_center_antimalware_solution_deployment`
62. `azure_security_center_antimalware_detection_configuration`
63. `azure_security_center_malware_risk_evaluation`
64. `azure_security_center_periodic_evaluation_schedule`
65. `azure_security_center_antimalware_auto_update`
66. `azure_security_center_malware_scan_schedule`
67. `azure_security_center_scan_frequency_management`
68. `azure_security_center_removable_media_scan`
69. `azure_security_center_antimalware_audit_log_retention`
70. `azure_security_center_antimalware_protection_enforcement`
71. `azure_security_center_phishing_detection_protection`
72. `azure_keyvault_password_protection_enforcement`
73. `azure_security_internal_vulnerability_scan`
74. `azure_security_vulnerability_management`
75. `azure_security_authenticated_scan_configure`
76. `azure_security_post_change_vulnerability_scan`
77. `azure_security_external_vulnerability_scan_schedule`
78. `azure_security_external_post_change_scan`
79. `azure_security_penetration_test_results_retention`
80. `azure_security_internal_penetration_testing`
81. `azure_security_external_penetration_testing`
82. `azure_security_vulnerability_remediation_verification`
83. `azure_security_change_detection_mechanism_configured`
84. `azure_security_incident_response_plan_update`
85. `azure_security_sensitive_data_audit`
86. `azure_keyvault_identify_sensitive_keys`
87. `azure_security_sensitive_data_protection_controls`
88. `azure_security_sensitive_data_transaction_identification`
89. `azure_security_cryptographic_implementation_identification`
90. `azure_security_configuration_options_identification`
91. `azure_security_center_get_security_controls`
92. `azure_security_verify_sensitive_data_controls`
93. `azure_security_sensitive_data_identification`
94. `azure_security_sensitive_data_protection_controls_identification`
95. `azure_security_sensitive_data_transaction_types_identification`
96. `azure_security_sensitive_data_cryptographic_implementations_identification`
97. `azure_security_sensitive_data_accounts_credentials_identification`
98. `azure_security_sensitive_data_configuration_options_identification`
99. `azure_security_sensitive_function_resource_identification`
100. `azure_security_third_party_software_compliance_check`
101. `azure_security_sensitive_functions_resources_identification`
102. `azure_security_interface_exposure_verification`
103. `azure_security_external_resource_authentication_verification`
104. `azure_security_sensitive_data_protection_verification`
105. `azure_security_vulnerability_exposure_verification`
106. `azure_security_third_party_module_verification`
107. `azure_security_external_resource_data_protection_verification`
108. `azure_security_controls_initialization_check`
109. `azure_security_controls_user_input_check`
110. `azure_security_controls_initialization_verification`
111. `azure_security_controls_user_input_verification`
112. `azure_keyvault_check_default_keys`
113. `azure_keyvault_check_key_usage`
114. `azure_keyvault_default_key_replacement`
115. `azure_keyvault_default_key_check`
116. `azure_keyvault_key_usage_check`
117. `azure_compute_software_execution_environment_security_check`
118. `azure_keyvault_key_rotation`
119. `azure_keyvault_key_cryptography_verification`
120. `azure_keyvault_cryptography_compliance_verification`
121. `azure_keyvault_cryptography_standard_check`
122. `azure_keyvault_delete_encryption_keys`
123. `azure_keyvault_delete_cryptographic_keys`
124. `azure_security_transient_data_residue_analysis`
125. `azure_security_sensitive_data_leakage_prevention`
126. `azure_security_sensitive_data_exposure_detection`
127. `azure_security_cryptography_protection_methods`
128. `azure_security_sensitive_data_leak_prevention`
129. `azure_security_sensitive_data_residue_check`
130. `azure_security_protection_methods_verification`
131. `azure_security_check_mitigation_status`
132. `azure_security_check_mitigation_controls`
133. `azure_security_check_user_input_mitigation`
134. `azure_security_mitigation_controls_verification`
135. `azure_security_mitigation_controls_default_settings_verification`
136. `azure_security_user_input_authentication_verification`
137. `azure_security_mitigation_status_check`
138. `azure_security_mitigation_guidance_distribution`
139. `azure_security_mitigation_authentication_check`
140. `azure_keyvault_sensitive_data_classification`
141. `azure_keyvault_sensitive_data_identification`
142. `azure_security_critical_assets_access_restriction`
143. `azure_keyvault_cryptography_compliance_check`
144. `azure_compute_execution_environment_security_check`
145. `azure_keyvault_secret_encryption`
146. `azure_security_third_party_software_vulnerability_check`
147. `azure_compute_execution_environment_security_configuration_guidance`
148. `azure_security_data_transmission_encryption_enforcement`
149. `azure_security_strong_cryptography_enforcement_verification`
150. `azure_security_third_party_cryptography_configuration_guidance_check`
151. `azure_security_asymmetric_cryptography_private_key_usage_check`
152. `azure_keyvault_asymmetric_key_confidentiality_check`
153. `azure_keyvault_third_party_cryptography_guidance_check`
154. `azure_security_activity_tracking`
155. `azure_security_activity_tracking_confidential_data_protection`
156. `azure_security_confidential_data_protection`
157. `azure_security_activity_tracking_detail`
158. `azure_security_confidential_data_tracking`
159. `azure_security_anomaly_detection`
160. `azure_security_validate_software_integrity`
161. `azure_security_protect_cryptographic_primitives`
162. `azure_security_protect_stored_values`
163. `azure_security_prevent_brute_force_attacks`
164. `azure_security_software_integrity_check`
165. `azure_security_cryptographic_protection`
166. `azure_security_sensitive_data_protection`
167. `azure_security_brute_force_prevention`
168. `azure_security_anomaly_detection_configuration_change`
169. `azure_security_anomaly_detection_attack_behavior`
170. `azure_security_integrity_check_software_executables`
171. `azure_security_integrity_check_dataset_values`
172. `azure_security_brute_force_attack_prevention`
173. `azure_security_anomaly_detection_protection`
174. `azure_security_integrity_validation`
175. `azure_security_dataset_integrity_validation`
176. `azure_security_third_party_tools_configuration_guidance`
177. `azure_security_software_integrity_validation`
178. `azure_security_software_execution_integrity_check`
179. `azure_security_cryptographic_primitives_protection`
180. `azure_security_dataset_integrity_protection`
181. `azure_security_third_party_attack_detection_configuration`
182. `azure_security_anomaly_detection_configuration`
183. `azure_security_anomaly_detection_alerts`
184. `azure_security_threat_identification`
185. `azure_security_threat_validation`
186. `azure_security_mitigation_implementation`
187. `azure_security_mitigation_validation`
188. `azure_security_threat_assessment`
189. `azure_security_threat_mitigation`
190. `azure_security_release_validation`
191. `azure_security_threat_mitigation_validation`
192. `azure_security_vulnerability_testing_pre_release`
193. `azure_security_vulnerability_ranking_system`
194. `azure_security_vulnerability_remediation_plan`
195. `azure_security_vulnerability_detection_in_third_party_components`
196. `azure_security_vulnerability_remediation_plan_maintenance`
197. `azure_security_vulnerability_classification`
198. `azure_security_software_vulnerability_testing`
199. `azure_security_third_party_component_vulnerability_detection`
200. `azure_security_patch_release_criteria_verification`
201. `azure_security_patch_distribution_verification`
202. `azure_security_patch_update_verification`
203. `azure_security_patch_update_criteria_check`
204. `azure_security_software_update_integrity_verification`
205. `azure_security_software_update_notification`
206. `azure_security_vulnerability_notification`
207. `azure_security_software_update_coverage_verification`
208. `azure_security_software_update_user_input_validation_guidance`
209. `azure_security_software_update_tls_connection_verification`
210. `azure_security_software_update_notification_and_guidance`
211. `azure_security_vulnerability_notification_and_mitigation_guidance`
212. `azure_keyvault_sensitive_data_retention_check`
213. `azure_keyvault_rng_function_verification`
214. `azure_keyvault_cryptography_verification`
215. `azure_keyvault_cryptographic_signature_verification`
216. `azure_keyvault_verify_signature`
217. `azure_keyvault_verify_encryption`
218. `azure_keyvault_verify_rng`
219. `azure_security_remove_test_data_and_accounts`
220. `azure_security_remove_hardcoded_credentials`
221. `azure_security_monitor_vulnerabilities`
222. `azure_security_sbom_generation`
223. `azure_security_sbom_dependency_tracking`
224. `azure_security_sbom_production_dependency_inclusion`
225. `azure_security_sbom_authenticity_verification`
226. `azure_security_enforce_access_control_rules`
227. `azure_security_enforce_secure_area_authentication`
228. `azure_security_enforce_secure_area_authorization`
229. `azure_security_parser_interpreter_restriction`
230. `azure_security_resource_starvation_mitigation`
231. `azure_security_hostile_object_creation_mitigation`
232. `azure_security_cross_origin_resource_sharing_mitigation`
233. `azure_keyvault_self_signed_certificate_limitation`
234. `security_center_system_info_discovery_limitation`
235. `security_center_data_protection_risk_level`
236. `security_center_privileged_access_prevention_review`
237. `security_center_physical_access_prevention`
238. `security_center_system_vulnerabilities_shared`
239. `security_center_user_actions_mitigate_phishing_threats`
240. `security_defender_auto_provisioning_log_analytics_agent_vms_on`
241. `security_center_interpreter_abuse_monitoring_enabled`
242. `security_center_procedures_established_for_incident_management`
243. `defender_cloud_apps_integration_status`
244. `security_center_group_permission_monitoring_status`
245. `security_center_gdpr_compliance_level`
246. `security_center_information_security_review_interval`
247. `security_center_credentials_storage_secure`
248. `securedev_software_systems_rules_established_applied`
249. `security_center_defacement_risk_monitored_state`
250. `security_center_patch_application_status`
251. `security_center_vulnerability_exposure_evaluation`
252. `security_center_threat_info_collection_enablement`
253. `security_center_methods_for_reset_two`
254. `security_center_incident_response_procedures_effectiveness`
255. `security_center_subscription_enabled`


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
3. Follow the naming convention: `security_center_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def security_center_example_function_check():
    """
    Example compliance check for Azure Security Center service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.security_center import Security_CenterManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Security_CenterManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in security_center check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Security Center
- **SDK Namespace**: azure.mgmt.security_center
- **Client Class**: Security_CenterManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Security Center API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
