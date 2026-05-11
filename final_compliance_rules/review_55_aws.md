# Review: 55 AWS rule renames — compliance intent check

## aws.backup.recovery_points.encryption_enabled
- **Intent:** Check that AWS Backup recovery points are encrypted with a customer-managed key (CMK).
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.backup.recovery_points.encryption`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.backup.resource.vault_encryption_enabled`  — shared: ['encryption']
  - `aws.backup.resource.encryption_enabled`  — shared: ['encryption']
  - `aws.backup.recoverypoint.encryption_at_rest_cmek_if_supported`  — shared: ['encryption']

## aws.backup.recovery_points.minimum_count_configured
- **Intent:** Ensure a minimum number of recovery points exist for critical services.
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.backup.recovery_points.minimum_count`
- **Catalog candidates:** none in scope

## aws.cloudwatch.log_group.kubernetes_audit_configured
- **Intent:** (refined)
- **Frameworks:** CIS  (compliance_count=1)
- **Old ID:** `aws.cloudwatch.log_group.kubernetes_audit`
- **Catalog candidates:** none in scope

## aws.ec2.image.baseline_approved_enforced
- **Intent:** Check that EC2 instances are launched from an approved baseline AMI.; Check that EC2 AMIs are from an approved baseline list.; (refined)
- **Frameworks:** CANADA_PBMM  (compliance_count=2)
- **Old ID:** `aws.ec2.image.baseline_approved`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.ec2.spotinstance.instance_uses_approved_launch_template_configured`  — shared: ['approved']
  - `aws.ec2.launchtemplate.uses_approved_configured`  — shared: ['approved']
  - `aws.ec2.autoscalinggroup.uses_approved_launch_template_configured`  — shared: ['approved']

## aws.ec2.image.scan_on_launch_configured
- **Intent:** Check if EC2 instances are configured to use AMIs with vulnerability scanning enabled or require scanning via Systems Manager.; (refined)
- **Frameworks:** NIST_800_171  (compliance_count=1)
- **Old ID:** `aws.ec2.image.scan_on_launch`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.ec2.spotinstance.instance_uses_approved_launch_template_configured`  — shared: ['launch']
  - `aws.ec2.security_group_from_launch_wizard.launch_wizard_created_configured`  — shared: ['launch']
  - `aws.ec2.resource.launch_template_imdsv2_required`  — shared: ['launch']

## aws.ec2.instance.antivirus_installed_configured
- **Intent:** Check if EC2 instances have an antivirus/anti-malware agent installed and running.; Check if EC2 instances have antivirus/anti-malware agent installed
- **Frameworks:** CANADA_PBMM  (compliance_count=3)
- **Old ID:** `aws.ec2.instance.antivirus_installed`
- **Catalog candidates:** none in scope

## aws.ec2.instance.ebs_encryption_enabled
- **Intent:** Check that EC2 instances use EBS volumes with encryption enabled.
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.ec2.instance.ebs_encryption`
- **Catalog candidates:** none in scope

## aws.ec2.instance.maintenance_behavior_configured
- **Intent:** Check that EC2 instances are configured to stop/terminate rather than hibernate for non-local maintenance.
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.ec2.instance.maintenance_behavior`
- **Catalog candidates:** none in scope

## aws.ec2.instance.patch_management_configured
- **Intent:** Check that EC2 instances have automated patch management enabled via Systems Manager.; Check that EC2 instances have patch management enabled via Syst
- **Frameworks:** CANADA_PBMM  (compliance_count=2)
- **Old ID:** `aws.ec2.instance.patch_management`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.ec2.instance.patch_compliance_status_check`  — shared: ['patch']

## aws.ec2.instance.recovery_behavior_configured
- **Intent:** Check EC2 instances are configured for stop/terminate recovery via termination protection or Auto Scaling.; Check EC2 instances are configured for rec
- **Frameworks:** CANADA_PBMM  (compliance_count=2)
- **Old ID:** `aws.ec2.instance.recovery_behavior`
- **Catalog candidates:** none in scope

## aws.ec2.instance.recovery_instance_configured
- **Intent:** Check that EC2 instances are configured with recovery automation via AWS Systems Manager Automation documents.
- **Frameworks:** CANADA_PBMM  (compliance_count=2)
- **Old ID:** `aws.ec2.instance.recovery_instance`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.ec2.instance.internet_facing_with_instance_profile_configured`  — shared: ['instance']

## aws.ec2.instance.required_ami_configured
- **Intent:** Ensure EC2 instances are launched from approved AMIs only.
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.ec2.instance.required_ami`
- **Catalog candidates:** none in scope

## aws.ec2.instance.time_sync_configured
- **Intent:** Check if EC2 instances are configured to use Amazon Time Sync Service or equivalent.; (refined)
- **Frameworks:** PCI_DSS  (compliance_count=1)
- **Old ID:** `aws.ec2.instance.time_sync`
- **Catalog candidates:** none in scope

## aws.ec2.instance.vulnerability_scan_enabled
- **Intent:** check if EC2 instances have vulnerability findings from AWS Inspector or similar service
- **Frameworks:** PCI_DSS  (compliance_count=1)
- **Old ID:** `aws.ec2.instance.vulnerability_scan`
- **Catalog candidates:** none in scope

## aws.ec2.securitygroup.allow_wide_open_public_ipv4_restricted
- **Intent:** CC6.6 The entity implements logical access security measures to protect against
- **Frameworks:** ISO27001_2022;SOC2  (compliance_count=5)
- **Old ID:** `aws.ec2.securitygroup.allow_wide_open_public_ipv4`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.ec2.subnet.public_subnets_use_nacl_restrictions_configured`  — shared: ['public']
  - `aws.ec2.subnet.public_s_use_nacl_restrictions_configured`  — shared: ['public']
  - `aws.ec2.spotinstance.no_public_ip_assigned_configured`  — shared: ['public']

## aws.ec2.volume.delete_on_termination_configured
- **Intent:** (refined); Check that EBS volumes are configured to be deleted on instance termination.
- **Frameworks:** NIST_800_171  (compliance_count=1)
- **Old ID:** `aws.ec2.volume.delete_on_termination`
- **Catalog candidates:** none in scope

## aws.ec2.vpc_peering_connection.require_encryption_enabled
- **Intent:** Check that VPC peering connections require encryption for data in transit.
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.ec2.vpc_peering_connection.require_encryption`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.ec2.vpnconnection.ike_phase_encryption_strong_configured`  — shared: ['encryption']
  - `aws.ec2.volume.encryption_at_rest_enabled`  — shared: ['encryption']
  - `aws.ec2.snapshot.encryption_at_rest_enabled`  — shared: ['encryption']

## aws.eks.cluster.namespace_default_configured
- **Intent:** (refined)
- **Frameworks:** CIS  (compliance_count=1)
- **Old ID:** `aws.eks.cluster.namespace_default`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.eks.cluster.default_service_account_automount_disabled`  — shared: ['default']

## aws.eks.cluster.pod_security_policy_configured
- **Intent:** (refined)
- **Frameworks:** CIS  (compliance_count=1)
- **Old ID:** `aws.eks.cluster.pod_security_policy`
- **Catalog candidates:** none in scope

## aws.eks.cluster.rbac_managed_configured
- **Intent:** PARTIAL: aws.eks.cluster.rbac_managed ||| verifies RBAC is enabled but not specific Google Groups integration
- **Frameworks:** CIS  (compliance_count=1)
- **Old ID:** `aws.eks.cluster.rbac_managed`
- **Catalog candidates:** none in scope

## aws.eks.node_group.kubelet_config_ownership_enforced
- **Intent:** (refined)
- **Frameworks:** CIS  (compliance_count=1)
- **Old ID:** `aws.eks.node_group.kubelet_config_ownership`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.eks.resource.node_kubelet_read_only_port_configured`  — shared: ['kubelet']
  - `aws.eks.resource.kubelet_event_record_qps_configured`  — shared: ['kubelet']

## aws.eks.node_group.kubelet_config_permissions_restricted
- **Intent:** Check that the kubelet configuration file on EKS worker nodes has permissions set to 644 or more restrictive.; (refined)
- **Frameworks:** CIS;CIS_AWS  (compliance_count=2)
- **Old ID:** `aws.eks.node_group.kubelet_config_permissions`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.eks.resource.node_kubelet_read_only_port_configured`  — shared: ['kubelet']
  - `aws.eks.resource.kubelet_event_record_qps_configured`  — shared: ['kubelet']
  - `aws.eks.addon.no_privileged_permissions_configured`  — shared: ['permissions']

## aws.eks.pod.security_context_configured
- **Intent:** (refined)
- **Frameworks:** CIS  (compliance_count=1)
- **Old ID:** `aws.eks.pod.security_context`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.eks.api.pod_security_level_restricted`  — shared: ['security']
  - `aws.eks.api.pod_security_admission_restricted_default_configured`  — shared: ['security']

## aws.eks.pod_security_policy.allow_privilege_escalation_restricted
- **Intent:** (refined)
- **Frameworks:** CIS  (compliance_count=1)
- **Old ID:** `aws.eks.pod_security_policy.allow_privilege_escalation`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.eks.api.privilege_escalation_denied_configured`  — shared: ['escalation', 'privilege']

## aws.guardduty.detector.status_configured
- **Intent:** check that AWS GuardDuty is enabled and monitoring the account/region; check that AWS GuardDuty is enabled and monitoring; Check that AWS GuardDuty is
- **Frameworks:** CANADA_PBMM  (compliance_count=9)
- **Old ID:** `aws.guardduty.detector.status`
- **Catalog candidates:** none in scope

## aws.iam.account_password_policy.no_anonymous_access_enforced
- **Intent:** Ensure IAM account password policy disables anonymous authentication
- **Frameworks:** CIS_AWS  (compliance_count=1)
- **Old ID:** `aws.iam.account_password_policy.no_anonymous_access`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.iam.user.single_active_access_key_configured`  — shared: ['access']
  - `aws.iam.user.single_active_access_key_audit_configured`  — shared: ['access']
  - `aws.iam.user.mfa_enabled_console_access`  — shared: ['access']

## aws.iam.account_password_policy.maximum_password_attempts_configured
- **Intent:** Check AWS account password policy sets a low max failed attempts.; (refined)
- **Frameworks:** NIST_800_171  (compliance_count=1)
- **Old ID:** `aws.iam.account_password_policy.maximum_password_attempts`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.iam.user.password_policy_complex_configured`  — shared: ['password']
  - `aws.iam.user.console_password_present_only_if_required`  — shared: ['password']
  - `aws.iam.cloudtrail.update_account_password_policy`  — shared: ['password']

## aws.iam.password_policy.hide_password_feedback_configured
- **Intent:** Check IAM password policy does not reveal password details on failure.
- **Frameworks:** NIST_800_171  (compliance_count=1)
- **Old ID:** `aws.iam.password_policy.hide_password_feedback`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.iam.user.password_policy_complex_configured`  — shared: ['password']
  - `aws.iam.user.console_password_present_only_if_required`  — shared: ['password']
  - `aws.iam.cloudtrail.update_account_password_policy`  — shared: ['password']

## aws.iam.policy.action_configured
- **Intent:** Check IAM policies for unauthorized maintenance tool actions; (refined)
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.iam.policy.action`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.iam.policy.no_action_star_on_resource_star_configured`  — shared: ['action']

## aws.iam.policy.change_approval_configured
- **Intent:** Check that IAM policy changes require approval via a service control policy or similar guardrail.
- **Frameworks:** NIST_800_171  (compliance_count=1)
- **Old ID:** `aws.iam.policy.change_approval`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.iam.policy.versioning_and_change_audit_enabled`  — shared: ['change']

## aws.iam.policy.condition_external_accounts_configured
- **Intent:** Check IAM policies for conditions restricting use to external AWS accounts.
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.iam.policy.condition_external_accounts`
- **Catalog candidates:** none in scope

## aws.iam.policy.condition_source_ip_configured
- **Intent:** Check IAM policies for maintenance actions to ensure they require a source IP from an approved network.; (refined)
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.iam.policy.condition_source_ip`
- **Catalog candidates:** none in scope

## aws.iam.policy.deny_maintenance_tools_restricted
- **Intent:** Check IAM policies for explicit denies on actions used by unauthorized maintenance tools.; Check IAM policies for explicit denies on maintenance tool
- **Frameworks:** CANADA_PBMM  (compliance_count=2)
- **Old ID:** `aws.iam.policy.deny_maintenance_tools`
- **Catalog candidates:** none in scope

## aws.iam.policy.principal_condition_configured
- **Intent:** Check IAM policies for nonlocal maintenance sessions require MFA or other strong authentication.
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.iam.policy.principal_condition`
- **Catalog candidates:** none in scope

## aws.iam.role.trust_policy_boundary_configured
- **Intent:** Check IAM roles have a permissions boundary limiting trust policy modifications.; (refined)
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.iam.role.trust_policy_boundary`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.iam.role.trust_principals_allowlist_only_configured`  — shared: ['trust']
  - `aws.iam.role.trust_external_id_or_audience_required`  — shared: ['trust']
  - `aws.iam.role.awssupport_access_policy_attachment_configured`  — shared: ['policy']

## aws.iam.role.trust_policy_change_control_configured
- **Intent:** Check that IAM role trust policies are not changed without approval.; (refined)
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.iam.role.trust_policy_change_control`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.iam.role.trust_principals_allowlist_only_configured`  — shared: ['trust']
  - `aws.iam.role.trust_external_id_or_audience_required`  — shared: ['trust']
  - `aws.iam.role.awssupport_access_policy_attachment_configured`  — shared: ['policy']

## aws.iam.role.trust_policy_external_principals_configured
- **Intent:** Check IAM role trust policies for unauthorized external principals.
- **Frameworks:** CANADA_PBMM  (compliance_count=2)
- **Old ID:** `aws.iam.role.trust_policy_external_principals`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.iam.role.trust_principals_allowlist_only_configured`  — shared: ['principals', 'trust']
  - `aws.iam.role.trust_external_id_or_audience_required`  — shared: ['external', 'trust']
  - `aws.iam.role.awssupport_access_policy_attachment_configured`  — shared: ['policy']

## aws.iam.role.trust_policy_token_actions_configured
- **Intent:** Check IAM role trust policies for unnecessary sts:AssumeRoleWithWebIdentity or sts:AssumeRoleWithSAML actions.
- **Frameworks:** CIS_AWS  (compliance_count=1)
- **Old ID:** `aws.iam.role.trust_policy_token_actions`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.iam.role.trust_principals_allowlist_only_configured`  — shared: ['trust']
  - `aws.iam.role.trust_external_id_or_audience_required`  — shared: ['trust']
  - `aws.iam.role.awssupport_access_policy_attachment_configured`  — shared: ['policy']

## aws.inspector.assessment.enabled
- **Intent:** (refined)
- **Frameworks:** CIS  (compliance_count=1)
- **Old ID:** `aws.inspector.assessment.enabled`
- **Catalog candidates:** none in scope

## aws.kms.key.key_manager_configured
- **Intent:** (refined); Check that KMS customer-managed keys have a defined key manager (IAM user/role) for key usage authorization.; Check that KMS customer-manag
- **Frameworks:** CANADA_PBMM;NIST_800_171  (compliance_count=4)
- **Old ID:** `aws.kms.key.key_manager`
- **Catalog candidates:** none in scope

## aws.organizations.account.status_configured
- **Intent:** check that all member accounts in the organization are active and monitored
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.organizations.account.status`
- **Catalog candidates:** none in scope

## aws.rds.db_instance.automated_backups_configured
- **Intent:** Check RDS instance automated backup retention period is configured
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.rds.db_instance.automated_backups`
- **Catalog candidates:** none in scope

## aws.securityhub.findings.periodic_assessment_configured
- **Intent:** Check that AWS Security Hub is enabled and configured to periodically generate findings for security controls.
- **Frameworks:** NIST_800_171  (compliance_count=1)
- **Old ID:** `aws.securityhub.findings.periodic_assessment`
- **Catalog candidates:** none in scope

## aws.ssm.parameter.permissions_configured
- **Intent:** (refined)
- **Frameworks:** CIS  (compliance_count=1)
- **Old ID:** `aws.ssm.parameter.permissions`
- **Catalog candidates:** none in scope

## aws.vpc.network_acl.deny_all_ingress_restricted
- **Intent:** Check that a VPC network ACL denies all inbound traffic by default.
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.vpc.network_acl.deny_all_ingress`
- **Catalog candidates (same scope, shared tokens):**
  - `aws.vpc.nacl_ingress_restricted_ports_22_3389.nacl_ingress_restricted_ports_22_3389_configured`  — shared: ['ingress']
  - `aws.vpc.cloudtrail.sg_all_ports_open`  — shared: ['all']

## aws.vpc.network_acl.rule_action_configured
- **Intent:** Check that VPC Network ACL rules enforce allowed traffic flows (deny by default, explicit allow rules).
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.vpc.network_acl.rule_action`
- **Catalog candidates:** none in scope

## aws.vpc.peering_connection.require_acceptance_configured
- **Intent:** Check that VPC peering connections require manual acceptance.
- **Frameworks:** CANADA_PBMM  (compliance_count=1)
- **Old ID:** `aws.vpc.peering_connection.require_acceptance`
- **Catalog candidates:** none in scope

## aws.vpn.client_endpoint.split_tunnel_configured
- **Intent:** check that AWS Client VPN endpoints do not have split tunneling enabled; (refined)
- **Frameworks:** NIST_800_171  (compliance_count=1)
- **Old ID:** `aws.vpn.client_endpoint.split_tunnel`
- **Catalog candidates:** none in scope

