# Top 50 quick-win rules (high impact × low complexity)

Build these first — each unlocks 3+ compliance controls and is L1/L2/L4 complexity.

| Rank | Rule | CSP | Complexity | Severity | Controls | Frameworks |
|------|------|-----|------------|----------|---------:|------------|
| 1 | `ibm.security_advisor.is_enabled` | ibm | L1_API_BOOLEAN | MEDIUM | 70 | CANADA_PBMM;FedRAMP_Moderate;HIPAA;NIST_800_171;NIST_800_53 |
| 2 | `ibm.iam.account.password_policy_minimum_length_configured` | ibm | L2_API_CONFIG | MEDIUM | 69 | CANADA_PBMM;FedRAMP_Moderate;HIPAA;NIST_800_171;NIST_800_53 |
| 3 | `alicloud.ram.password.policy_minimum_length_check` | alicloud | L2_API_CONFIG | MEDIUM | 68 | CANADA_PBMM;CIS_ALICLOUD;FedRAMP_Moderate;NIST_800_171;NIST_800_53 |
| 4 | `gcp.securitycenter.scc.is_enabled` | gcp | L1_API_BOOLEAN | MEDIUM | 63 | CANADA_PBMM;CIS_OCI;FedRAMP_Moderate;NIST_800_53 |
| 5 | `ibm.activity_tracker.log_file_validation_enabled` | ibm | L1_API_BOOLEAN | MEDIUM | 53 | CANADA_PBMM;FedRAMP_Moderate;NIST_800_53 |
| 6 | `alicloud.securitycenter.service.is_activated_check` | alicloud | L2_API_CONFIG | MEDIUM | 53 | CIS_AZURE;FedRAMP_Moderate;NIST_800_53 |
| 7 | `ibm.iam.password_policy_reuse_prevention_configured` | ibm | L2_API_CONFIG | MEDIUM | 42 | CIS_OCI;FedRAMP_Moderate;HIPAA;NIST_800_171;NIST_800_53 |
| 8 | `ibm.iam.password.policy_expires_passwords_within_90_days_or_less_configured` | ibm | L2_API_CONFIG | MEDIUM | 41 | CIS_OCI;FedRAMP_Moderate;NIST_800_171;NIST_800_53;PCI_DSS |
| 9 | `ibm.iam.password.policy_symbol_configured` | ibm | L2_API_CONFIG | MEDIUM | 38 | CANADA_PBMM;CISA_CE;FedRAMP_Moderate;HIPAA;NIST_800_171 |
| 10 | `gcp.securitycenter.scanner.enabled` | gcp | L2_API_CONFIG | MEDIUM | 36 | FedRAMP_Moderate;NIST_800_171;NIST_800_53 |
| 11 | `alicloud.ram.password.policy_lowercase_check` | alicloud | L2_API_CONFIG | MEDIUM | 35 | CIS_ALICLOUD;FedRAMP_Moderate;NIST_800_171;NIST_800_53 |
| 12 | `alicloud.ram.password.policy_require_numbers_check` | alicloud | L2_API_CONFIG | MEDIUM | 35 | CIS_ALICLOUD;FedRAMP_Moderate;NIST_800_171;NIST_800_53 |
| 13 | `alicloud.ram.password.policy_require_uppercase_configured` | alicloud | L2_API_CONFIG | MEDIUM | 35 | CIS_ALICLOUD;FedRAMP_Moderate;NIST_800_171;NIST_800_53 |
| 14 | `alicloud.ram.password.policy_require_symbols_configured` | alicloud | L2_API_CONFIG | MEDIUM | 34 | CIS_ALICLOUD;FedRAMP_Moderate;NIST_800_53 |
| 15 | `azure.keyvault.vault.access_policy_configured` | azure | L2_API_CONFIG | MEDIUM | 31 | CANADA_PBMM;CIS_ALICLOUD;CIS_GCP;CIS_IBM;CIS_K8S |
| 16 | `ibm.iam.role.least_privilege_enforced` | ibm | L2_API_CONFIG | MEDIUM | 28 | CANADA_PBMM;CIS_AWS;CIS_AZURE;CIS_OCI;NIST_800_171 |
| 17 | `gcp.logging.sink.destination_and_filter_configured` | gcp | L2_API_CONFIG | MEDIUM | 24 | CANADA_PBMM;CIS_ALICLOUD;NIST_800_171;NIST_800_53 |
| 18 | `gcp.iam.account.password_policy_minimum_length_configured` | gcp | L2_API_CONFIG | MEDIUM | 22 | CANADA_PBMM;CIS_OCI;PCI_DSS |
| 19 | `alicloud.ram.user.unused_credentials_configured` | alicloud | L2_API_CONFIG | MEDIUM | 21 | CANADA_PBMM;CISA_CE;CIS_OCI;FedRAMP_Moderate;NIST_800_171 |
| 20 | `ibm.iam.user.unused_credentials_configured` | ibm | L2_API_CONFIG | MEDIUM | 21 | CANADA_PBMM;CISA_CE;CIS_OCI;FedRAMP_Moderate;HIPAA |
| 21 | `azure.backup.recovery_vault.configured` | azure | L2_API_CONFIG | MEDIUM | 19 | CANADA_PBMM;NIST_800_53 |
| 22 | `alicloud.ram.user.console_access_unused_disabled` | alicloud | L1_API_BOOLEAN | MEDIUM | 18 | CANADA_PBMM;FedRAMP_Moderate;NIST_800_171;NIST_800_53 |
| 23 | `ibm.activity_tracker.route.is_configured` | ibm | L2_API_CONFIG | MEDIUM | 16 | CANADA_PBMM;CIS_ALICLOUD;CIS_K8S;CIS_OCI;NIST_800_171 |
| 24 | `ibm.security_advisor.enabled` | ibm | L2_API_CONFIG | MEDIUM | 14 | CANADA_PBMM;FedRAMP_Moderate;HIPAA;NIST_800_171;NIST_800_53 |
| 25 | `alicloud.ram.policy.external_entities_configured` | alicloud | L4_POLICY_PARSE | MEDIUM | 14 | CANADA_PBMM;CIS_IBM;FedRAMP_Moderate;NIST_800_53 |
| 26 | `k8s.rbac.rolebinding.external_subjects_configured` | k8s | L2_API_CONFIG | MEDIUM | 13 | CANADA_PBMM;CIS_GCP;FedRAMP_Moderate;NIST_800_53 |
| 27 | `ibm.iam.authorization_policy.external_principals_configured` | ibm | L4_POLICY_PARSE | MEDIUM | 13 | CANADA_PBMM;CIS_OCI;FedRAMP_Moderate;NIST_800_53 |
| 28 | `alicloud.kms.key.automatic_rotation_enabled` | alicloud | L1_API_BOOLEAN | HIGH | 12 | CANADA_PBMM;CIS_GCP;CIS_IBM;CIS_K8S;NIST_800_53 |
| 29 | `alicloud.ram.policy.overly_permissive_configured` | alicloud | L2_API_CONFIG | MEDIUM | 12 | CANADA_PBMM;CIS_AZURE;CIS_GCP;CIS_OCI;FedRAMP_Moderate |
| 30 | `azure.authorization.role_assignment.external_tenants_configured` | azure | L2_API_CONFIG | MEDIUM | 12 | CANADA_PBMM;FedRAMP_Moderate;NIST_800_53 |
| 31 | `gcp.iam.policy_binding.external_principals_configured` | gcp | L4_POLICY_PARSE | MEDIUM | 12 | CANADA_PBMM;FedRAMP_Moderate;NIST_800_53 |
| 32 | `alicloud.ram.password.policy_compliance_enabled` | alicloud | L1_API_BOOLEAN | MEDIUM | 11 | CISA_CE;CIS_ALICLOUD;CIS_OCI;NIST_800_171;PCI_DSS |
| 33 | `azure.compute.vm.inventory_enabled` | azure | L1_API_BOOLEAN | MEDIUM | 11 | CANADA_PBMM;CIS_OCI;NIST_800_53 |
| 34 | `aws.kms.key.key_manager_configured` | aws | L2_API_CONFIG | HIGH | 11 | CANADA_PBMM;CIS_ALICLOUD;CIS_GCP;CIS_IBM;CIS_K8S |
| 35 | `ibm.activity_tracker.kms_encryption_enabled` | ibm | L1_API_BOOLEAN | HIGH | 10 | FedRAMP_Moderate;NIST_800_53 |
| 36 | `aws.guardduty.detector.status_configured` | aws | L2_API_CONFIG | MEDIUM | 9 | CANADA_PBMM |
| 37 | `oci.identity.policy.statements_external_entities_configured` | oracle | L4_POLICY_PARSE | MEDIUM | 9 | CANADA_PBMM;FedRAMP_Moderate;NIST_800_53 |
| 38 | `alicloud.ram.user.mfa_enabled` | alicloud | L1_API_BOOLEAN | HIGH | 8 | CANADA_PBMM;CISA_CE;CIS_OCI;FedRAMP_Moderate |
| 39 | `azure.compute.virtual_machine.image_baseline_enabled` | azure | L1_API_BOOLEAN | MEDIUM | 8 | CANADA_PBMM |
| 40 | `alicloud.ecs.instance.baseline_image_configured` | alicloud | L2_API_CONFIG | MEDIUM | 8 | CANADA_PBMM |
| 41 | `alicloud.kms.key.expiration_set` | alicloud | L2_API_CONFIG | HIGH | 8 | CIS_K8S;FedRAMP_Moderate;NIST_800_53 |
| 42 | `azure.iam.role.least_privilege_enforced` | azure | L2_API_CONFIG | MEDIUM | 8 | CANADA_PBMM;CIS_ALICLOUD;CIS_AWS;CIS_OCI;FedRAMP_Moderate |
| 43 | `ibm.iam.no.root_access_key_configured` | ibm | L2_API_CONFIG | HIGH | 8 | CANADA_PBMM;CIS_OCI;FedRAMP_Moderate;NIST_800_53 |
| 44 | `alicloud.oss.bucket.versioning_enabled` | alicloud | L1_API_BOOLEAN | MEDIUM | 7 | CANADA_PBMM;CIS_AWS;CIS_AZURE;SOC2 |
| 45 | `ibm.cos.bucket.versioning_enabled` | ibm | L1_API_BOOLEAN | MEDIUM | 6 | CANADA_PBMM;CIS_AWS;CIS_AZURE;SOC2 |
| 46 | `ibm.iam.user.mfa_enabled` | ibm | L1_API_BOOLEAN | HIGH | 6 | CANADA_PBMM;CIS_GCP;CIS_OCI |
| 47 | `aws.ec2.instance.required_ami_configured` | aws | L2_API_CONFIG | MEDIUM | 6 | CANADA_PBMM |
| 48 | `azure.keyvault.key.key_type_configured` | azure | L2_API_CONFIG | MEDIUM | 6 | CANADA_PBMM;CIS_GCP;CIS_IBM;FedRAMP_Moderate;NIST_800_53 |
| 49 | `ibm.activity_tracker.event_routing.enabled` | ibm | L2_API_CONFIG | MEDIUM | 6 | CANADA_PBMM;CIS_ALICLOUD;CIS_K8S;NIST_800_171 |
| 50 | `ibm.cos.bucket.tls_policy_configured` | ibm | L2_API_CONFIG | HIGH | 6 | CANADA_PBMM;CIS_AWS;NIST_800_171 |
