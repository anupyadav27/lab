# GCP VPC Service Compliance Prompt

## Service Information
- **Service Name**: VPC
- **Description**: GCP VPC Service
- **Total Functions**: 324
- **SDK Client**: compute_client
- **Service Type**: networking

## Function List
The following 324 functions are available for VPC compliance checks:

1. `network_vpn_tunnels_operational_status`
2. `network_load_balancer_security_operations_access_configured`
3. `network_firewall_boundary_protection`
4. `network_https_load_balancer_redirect_configured`
5. `network_cdn_no_deprecated_ssl_protocols`
6. `network_cdn_tls_minimum_version_enforced`
7. `network_cdn_custom_ssl_sni_enabled`
8. `network_cdn_https_enforced`
9. `network_load_balancer_ssl_https_configured`
10. `network_firewall_restrict_inbound_ports`
11. `network_endpoints_api_backend_type_compliance`
12. `network_endpoints_ssl_certificate_required`
13. `network_cdn_ssl_certificate_non_default`
14. `network_vpn_authorization_no_access_all`
15. `network_vpc_peering_autoacceptsharedattachments_disabled`
16. `network_elasticsearch_vpc_configured`
17. `network_load_balancer_backend_ssl_google_managed`
18. `network_external_https_load_balancer_ssl_certificates_google_managed`
19. `network_firewall_ssh_incoming_restricted`
20. `network_nat_gateway_authorized_vpc`
21. `network_cloud_function_vpc_enabled`
22. `network_firewall_restrict_ssh_rdp_ingress`
23. `network_firewall_rule_fragmented_packets_action_compliant`
24. `network_vpc_service_controls_stateful_or_stateless_rules_associated`
25. `network_firewall_rule_contains_rules`
26. `network_vpc_subnet_no_public_routes`
27. `network_cloud_search_private_endpoint`
28. `network_vpc_private_google_access_point_required`
29. `network_firewall_associated_with_subnet`
30. `network_vpc_private_google_access_enabled`
31. `network_firewall_rules_restrict_inbound_ports`
32. `network_api_gateway_ssl_certificate_associated`
33. `network_endpoints_associated_with_armor_policies`
34. `network_cdn_ssl_certificate_custom`
35. `network_memorystore_custom_vpc_required`
36. `network_elasticsearch_vpc_enforced`
37. `network_load_balancer_google_managed_certificates`
38. `network_classic_load_balancer_ssl_certificates_google_managed`
39. `network_firewall_incoming_ssh_disabled`
40. `network_vpc_secure_configuration`
41. `network_vpc_cloud_nat_authorized`
42. `network_firewall_fragmented_packets_user_defined_action`
43. `network_routes_no_public_internet_access`
44. `network_vpc_private_service_connection_required`
45. `network_firewall_associated_with_network`
46. `network_waf_rule_has_conditions`
47. `network_api_gateway_ssl_certificate_required`
48. `network_interconnect_vpn_autoacceptsharedattachments_enabled`
49. `network_redis_custom_vpc_configured`
50. `network_google_cloud_search_vpc_configured`
51. `network_load_balancer_backend_ssl_certificate_validity`
52. `network_load_balancer_ssl_certificate_google_managed`
53. `network_firewall_block_public_access`
54. `network_firewall_ssh_ingress_denied`
55. `network_nat_gateway_authorized_vpc_association`
56. `network_vpc_firewall_stateless_default_action_fragmented_packets_configured`
57. `network_firewall_rules_associated_with_stateful_or_stateless`
58. `network_route_no_public_cidr`
59. `network_searchservice_private_endpoint`
60. `network_vpc_private_service_connection_exists`
61. `network_firewall_associated_with_vpc`
62. `network_firewall_restrict_unrestricted_inbound_ports`
63. `network_vpn_tunnels_established_state`
64. `network_vpc_cloud_nat_configured`
65. `network_routes_no_public_cidr_to_cloud_router_or_vpn_gateway`
66. `network_vpn_tunnels_active_status`
67. `network_endpoints_associated_with_cloud_armor`
68. `network_interconnect_autoacceptsharedattachments_enabled`
69. `network_elasticsearch_private_endpoint`
70. `network_load_balancer_backends_use_gcm_ssl_certificates`
71. `network_external_https_load_balancer_ssl_certificate_google_managed`
72. `network_firewall_ssh_incoming_disabled`
73. `network_vpc_authorized_internet_access`
74. `network_firewall_fragmented_packets_default_action`
75. `network_vpc_connector_associated_services`
76. `network_vpc_routes_no_public_igw`
77. `network_elasticsearch_vpc_enforcement`
78. `network_firewall_rule_association_required`
79. `network_vpn_tunnels_running_state`
80. `network_firewall_rule_has_targets`
81. `network_memorystore_custom_vpc_subnet`
82. `network_cloud_router_authorized_vpc_association`
83. `network_route_no_public_cie`
84. `network_cdn_cloud_armor_association`
85. `network_vpn_autotunnel_enabled`
86. `network_load_balancer_backend_ssl_certificate_google_managed`
87. `network_firewall_rule_deny_ssh`
88. `network_cloud_router_authorized_vpc_attachment`
89. `network_firewall_rule_fragmented_packets_default_action`
90. `network_routes_no_public_cloud_router`
91. `network_ai_platform_notebooks_vpc_compliance`
92. `network_vpc_private_service_access_required`
93. `network_waf_firewall_rules_present`
94. `network_load_balancer_desync_mitigation_mode_configured`
95. `network_cdn_logging_configured`
96. `network_vpn_logging_enabled`
97. `network_load_balancer_logging_enabled`
98. `network_firewall_logging_enabled`
99. `network_vpc_flow_logs_enabled`
100. `network_load_balancer_session_affinity_configured`
101. `network_cdn_logging_enabled`
102. `network_vpc_logging_enabled`
103. `network_load_balancer_access_logs_enabled`
104. `network_https_load_balancer_desync_mitigation_mode_configured`
105. `network_vpn_tunnel_logging_enabled`
106. `network_load_balancer_desync_mitigation_configured`
107. `network_cdn_access_logs_configured`
108. `network_vpc_service_controls_logging_enabled`
109. `network_load_balancer_connection_draining_configured`
110. `network_vpc_firewall_logging_enabled`
111. `network_security_policies_logging_destination_match`
112. `network_firewall_block_public_ingress_except_ssh`
113. `network_cdn_signed_urls_enabled`
114. `network_cloud_armor_metrics_enabled`
115. `network_load_balancer_cloud_armor_protection`
116. `network_load_balancer_cdn_armor_protection`
117. `network_load_balancer_https_redirection_configured`
118. `network_cdn_backend_tls_minimum_protocol_enforced`
119. `network_cdn_ssl_sni_enabled`
120. `network_load_balancer_ssl_https_listeners_configured`
121. `network_firewall_restrict_incoming_traffic`
122. `network_cdn_origin_ssl_protocols_no_sslv3`
123. `network_ssl_certificates_expiration_within_days`
124. `network_cdn_certificate_custom_ssl`
125. `network_load_balancer_backend_ssl_certificate_manager`
126. `network_load_balancer_ssl_certificates_google_managed`
127. `network_load_balancer_backend_ssl_certificate_trusted`
128. `network_vpc_firewall_block_public_access`
129. `network_https_load_balancer_ssl_certificates_google_managed`
130. `network_load_balancer_ssl_certificate_required`
131. `network_load_balancer_backend_https_google_managed_ssl`
132. `network_https_load_balancer_ssl_certificate_google_managed`
133. `network_ssl_certificates_expiration_compliance`
134. `network_load_balancer_backends_use_gcp_certificates`
135. `network_endpoint_ssl_certificate_required`
136. `network_https_load_balancer_ssl_tls_certificate_compliance`
137. `network_global_load_balancer_ssl_certificates_google_managed`
138. `network_load_balancer_backend_ssl_certificate_compliance`
139. `network_ssl_certificates_expiration_monitor`
140. `network_load_balancer_backend_google_managed_ssl_required`
141. `network_cdn_backendservice_non_default_ssl_certificate`
142. `network_load_balancer_backend_certificate_manager_enforced`
143. `network_ssl_certificates_expiry_within_days`
144. `network_cdn_ssl_protocols_no_sslv3`
145. `network_load_balancer_https_enforced`
146. `network_load_balancer_backend_ssl_certificate_configured`
147. `network_external_load_balancer_ssl_certificates_google_managed`
148. `network_load_balancer_https_ssl_configured`
149. `network_cdn_backends_no_deprecated_ssl`
150. `network_load_balancer_enforce_https`
151. `network_load_balancer_ssl_backend_services_configured`
152. `network_cdn_backends_logging_configured`
153. `network_load_balancer_armor_enabled`
154. `network_cloud_armor_security_team_access_configured`
155. `network_google_cloud_armor_security_team_access_configured`
156. `network_cdn_distribution_no_deprecated_ssl`
157. `network_tcp_udp_load_balancer_ssl_certificates_google_managed`
158. `network_vpn_authorization_no_allow_all`
159. `network_vpn_auto_accept_disabled`
160. `network_cloud_search_vpc_enforced`
161. `network_load_balancer_ssl_google_managed_certificates`
162. `network_firewall_disallow_ingress_ssh`
163. `network_cloud_router_associated_authorized_vpc`
164. `network_firewall_restrict_ingress_ssh_rdp`
165. `network_firewallrule_associated_with_ingress_or_egress`
166. `network_routes_no_public_cidr_to_cloud_router_nat`
167. `network_vpc_private_service_access_configured`
168. `network_firewall_rule_associated_with_network`
169. `network_firewall_block_public_access_enabled`
170. `network_https_load_balancer_https_redirect_configured`
171. `network_cdn_origin_ssl_protocols_non_deprecated`
172. `network_cdn_https_enforcement`
173. `network_elasticsearch_https_enforced`
174. `network_firewall_rules_restrict_unrestricted_ports`
175. `network_cdn_custom_ssl_certificate_required`
176. `network_firewall_rule_fragmented_packets_action`
177. `network_vpc_service_controls_stateful_stateless_association`
178. `network_cloud_search_vpc_enforcement`
179. `network_vpc_private_google_access_point_exists`
180. `network_memorystore_custom_vpc_configured`
181. `network_vpc_configuration_pci_compliance`
182. `network_firewall_rule_fragmented_packets_action_compliance`
183. `network_route_no_public_internet_gateway`
184. `network_waf_rule_conditions_present`
185. `network_cloud_search_vpc_configured`
186. `network_load_balancer_backend_ssl_certificate_valid`
187. `network_nat_gateway_associated_authorized_vpc`
188. `network_routes_no_public_cidr`
189. `network_load_balancer_backends_ssl_certificates_configured`
190. `network_vpc_access_connector_associated_services`
191. `network_firewall_rule_association_enforced`
192. `network_firewall_rule_has_target`
193. `network_api_association_with_cloud_armor`
194. `network_cdn_associated_with_cloud_armor`
195. `network_dms_private_services_no_public_access`
196. `network_firewall_deny_ssh`
197. `network_vpc_private_service_access_connection_required`
198. `network_firewall_rule_association_with_vpc`
199. `network_waf_contains_firewall_rules`
200. `network_firewall_block_public_ingress`
201. `network_cdn_distribution_authorized_service_account`
202. `network_firewall_restrict_incoming_traffic_ports`
203. `network_load_balancer_backend_https_certificates_google_managed`
204. `network_https_load_balancer_backend_ssl_tls_certificate_google_managed`
205. `network_endpoints_ssl_certificate_associated`
206. `network_cdn_ssl_protocols_non_deprecated`
207. `network_load_balancer_https_ssl_certificate_configured`
208. `network_load_balancer_ssl_backend_services`
209. `network_firewall_rules_priority_order`
210. `network_google_cloud_armor_sirt_access_configured`
211. `network_load_balancer_https_redirect_configured`
212. `network_tcp_udp_load_balancer_ssl_certificate_google_managed`
213. `network_cloud_armor_security_ops_access_configured`
214. `network_load_balancer_backend_ssl_certificates_configured`
215. `network_firewall_rule_associated_with_ingress_or_egress`
216. `network_route_no_public_cidr_to_cloud_router_or_nat`
217. `network_transfer_agreements_implemented`
218. `network_vpc_remote_access_security_measures`
219. `network_vpc_entry_control`
220. `network_facility_physical_security_implemented`
221. `network_vpc_data_protection`
222. `network_vpc_data_leakage_prevention`
223. `network_services_security_mechanisms_implemented`
224. `network_firewall_external_access_restriction`
225. `network_transfer_facility_rules_implemented`
226. `network_devices_data_leakage_prevention`
227. `network_vpc_security_enforced`
228. `network_vpc_external_access_restriction`
229. `network_vpc_rigorous_segregation`
230. `network_firewall_whitelist_enforced`
231. `network_vpc_system_interconnection`
232. `network_vpc_secure_perimeter`
233. `network_vpc_private_networks`
234. `network_vpc_information_flow_separation`
235. `network_vpc_logical_segmentation`
236. `network_vpc_advanced_segmentation`
237. `network_vpc_physical_segmentation`
238. `network_vpc_interconnection_points`
239. `network_load_balancer_web_protection`
240. `network_vpc_ddos_protection`
241. `network_vpc_strict_segregation`
242. `network_vpc_private_state`
243. `network_vpc_no_insecure_configurations`
244. `network_firewall_rules_ensure_integrity`
245. `network_vpc_promiscuous_mode_disabled`
246. `network_vpc_restrict_protocol_exfiltration`
247. `network_firewall_endpoint_dos_protection`
248. `network_vpc_bandwidth_protection`
249. `network_vpc_no_open_ports`
250. `network_connections_restricted_access`
251. `network_vpc_prevent_protocol_exfiltration`
252. `network_vpc_dos_protection_enabled`
253. `network_vpc_services_exposure`
254. `network_vpc_no_public_access`
255. `network_vpc_disable_promiscuous_mode`
256. `network_vpc_exfiltration_prevention`
257. `network_vpc_dos_protection`
258. `network_vpc_services_exposure_prevention`
259. `network_connections_list_restriction`
260. `network_https_load_balancer_logging_enabled`
261. `network_vpc_metric_filter_alarm_established`
262. `network_vpc_firewall_rule_change_alert`
263. `network_vpc_no_legacy_networks`
264. `network_firewall_rules_restrict_rdp_internet_access`
265. `network_firewall_rules_restrict_ssh_ingress`
266. `network_vpc_no_default_network`
267. `network_vpc_subnet_flow_logs_enabled`
268. `network_iap_firewall_restriction`
269. `network_load_balancer_secure_connections`
270. `network_firewall_restrict_public_access`
271. `network_firewall_log_metric_alerts_exist`
272. `network_vpc_default_network_absent`
273. `network_vpc_legacy_networks_absent`
274. `network_firewall_ssh_restricted`
275. `network_firewall_rdp_restricted`
276. `network_load_balancer_disallow_weak_ssl_policies`
277. `network_iap_google_ip_traffic_allowed`
278. `network_vpc_metric_filter_alarm`
279. `network_project_no_default_network`
280. `network_iap_user_access_restriction`
281. `network_connections_secure_by_default`
282. `network_vpc_firewall_log_metric_filter_alerts_exist`
283. `network_iap_google_ip_only`
284. `network_project_no_legacy_networks`
285. `network_iap_firewall_restriction_enforced`
286. `network_subnet_flow_logs_enabled`
287. `network_iap_google_ip_restriction`
288. `network_cables_protection_ensured`
289. `network_vpc_access_controls_enforced`
290. `network_vpc_wireless_security_measures`
291. `network_vpc_remote_access_protection`
292. `network_vpc_restrict_internet_access`
293. `network_vpc_external_server_protection`
294. `network_device_access_control_measures`
295. `network_firewall_high_security_configuration`
296. `network_vpc_enforce_information_flow_control`
297. `network_vpc_remote_access_control`
298. `network_vpc_limit_external_connections`
299. `network_vpc_boundary_protection`
300. `network_vpc_transmission_confidentiality_integrity`
301. `network_vpc_session_authenticity_protected`
302. `network_intrusion_detection_system_configuration`
303. `network_vpc_intranode_visibility_enabled`
304. `network_default_network_existence`
305. `network_icmp_redirects_disabled`
306. `network_source_routed_packets_not_accepted`
307. `network_icmp_redirects_not_accepted`
308. `network_icmp_secure_redirects_not_accepted`
309. `network_packet_suspicious_logging_enabled`
310. `network_icmp_broadcast_requests_ignored`
311. `network_icmp_ignore_bogus_error_responses`
312. `network_ipv6_router_advertisements_not_accepted`
313. `network_interface_ipv6_loopback_traffic_configured`
314. `network_firewall_ipv6_outbound_established_connections_configured`
315. `network_loopback_traffic_configured`
316. `ai_platform_notebook_vpc_compliance`
317. `ai_platform_notebook_vpc_subnet_compliance`
318. `network_vpc_route_change_alert`
319. `network_traffic_monitoring_unusual_activity`
320. `logging_vpc_route_change_alerts_exist`
321. `logging_vpc_log_metric_filter_alerts_exist`
322. `logging_vpc_log_metric_filter_and_alerts_exist`
323. `logging_vpc_network_log_metric_filter_alerts_exist`
324. `logging_network_flow_analysis`


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
3. Follow the naming convention: `vpc_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def vpc_example_function_check():
    """
    Example compliance check for VPC service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in vpc check: {e}")
        return False
```

## Notes
- All functions are based on GCP VPC API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
