# RBI NBFC IT Framework Compliance Agent

## Overview

This compliance agent provides automated security checks and manual control guidance for the **Reserve Bank of India (RBI) IT Framework for Non-Banking Financial Companies (NBFCs)**. The agent maps RBI controls to cloud-native security checks across 6 cloud providers.

## Framework Details

- **Source**: Reserve Bank of India (RBI)
- **Document**: Master Direction - Information Technology Framework for the NBFC Sector
- **Date Issued**: June 8, 2017
- **RBI Reference**: [Official Notification](https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=10999&Mode=0)
- **Azure Policy Reference**: [Azure RBI NBFC Policies](https://learn.microsoft.com/en-us/azure/governance/policy/samples/rbi-itf-nbfc-2017)
- **Total Controls**: 37
- **Automated Controls**: 16 (43.2%)
- **Manual Controls**: 21 (56.8%)
- **Total Checks**: 354 (across 6 cloud providers)

## Automation Strategy

### Automated Controls (43.2%)

Controls that can be continuously monitored through technical checks:

**Information and Cyber Security (7 automated):**
- Access Control (5 checks)
- Patch Management (4 checks)
- Anti-Malware Protection (3 checks)
- Network Security (5 checks)
- Encryption (5 checks)
- Secure Software Development (3 checks)
- Mobile Financial Services Security (3 checks)

**IT Operations (5 automated - 100%):**
- Change Management (3 checks)
- Capacity Management (3 checks)
- Incident Management (3 checks)
- System and Data Backup (5 checks)
- Logging and Monitoring (5 checks)

**Business Continuity (1 automated):**
- Disaster Recovery Site (3 checks)

**Smaller NBFCs (3 automated):**
- Basic Security (3 checks)
- Backup (3 checks)
- Regulatory Reporting (3 checks)

### Manual Controls (56.8%)

Controls requiring human judgment, organizational processes, or documentation review:

**IT Governance (4 manual - 100%):**
- Board Approved IT Strategy
- IT Strategy Committee
- CIO Designation
- CISO Designation

**Information Security (5 manual):**
- Information Security Policy
- Cyber Security Policy
- Cyber Crisis Management Plan
- Cyber Incident Reporting Process
- Social Media Usage Policy

**IS Audit (3 manual - 100%):**
- Annual IS Audit
- IS Audit Scope
- CAATs Usage

**Business Continuity (3 manual):**
- Business Continuity Plan
- Business Impact Analysis
- BCP Testing

**IT Outsourcing (4 manual - 100%):**
- IT Outsourcing Policy
- Outsourcing Contracts
- Outsourcing Risk Management
- Service Provider BCP

**Smaller NBFCs (2 manual):**
- IT Policy
- BCP Documentation

## Check Coverage by Section

| Section | Controls | Automated | Manual | Automation % | Total Checks |
|---------|----------|-----------|--------|--------------|--------------|
| IT Governance | 4 | 0 | 4 | 0% | 0 |
| Information & Cyber Security | 12 | 7 | 5 | 58% | 168 |
| IT Operations | 5 | 5 | 0 | 100% | 114 |
| IS Audit | 3 | 0 | 3 | 0% | 0 |
| Business Continuity | 4 | 1 | 3 | 25% | 18 |
| IT Outsourcing | 4 | 0 | 4 | 0% | 0 |
| Smaller NBFCs | 5 | 3 | 2 | 60% | 54 |
| **Total** | **37** | **16** | **21** | **43.2%** | **354** |

## Cloud Provider Coverage

All automated checks are available across 6 cloud providers:

1. **AWS** - Amazon Web Services (59 checks)
2. **Azure** - Microsoft Azure (59 checks)
3. **GCP** - Google Cloud Platform (59 checks)
4. **Oracle** - Oracle Cloud Infrastructure (59 checks)
5. **IBM** - IBM Cloud (59 checks)
6. **Alicloud** - Alibaba Cloud (59 checks)

**Total Multi-Cloud Checks**: 354

## Check Naming Convention

All checks follow the standard format: `{provider}_{service}_{check_description}`

### Examples by Control

**2.5 Access Control:**
- AWS: `aws_iam_user_mfa_enabled`
- Azure: `azure_entra_user_mfa_enabled`
- GCP: `gcp_iam_user_mfa_enabled`
- Oracle: `oracle_identity_user_mfa_enabled`

**2.8 Network Security:**
- AWS: `aws_ec2_securitygroup_ssh_restricted`
- Azure: `azure_vm_securitygroup_ssh_restricted`
- GCP: `gcp_compute_securitygroup_ssh_restricted`

**2.9 Encryption:**
- AWS: `aws_s3_bucket_encryption_enabled`
- Azure: `azure_storage_bucket_encryption_enabled`
- GCP: `gcp_gcs_bucket_encryption_enabled`

## Azure Policy Mapping

This agent references Azure Policy samples for RBI NBFC compliance. Key mappings:

### Access Control (2.5)
- MFA should be enabled on accounts with write permissions
- MFA should be enabled on accounts with owner permissions
- A maximum of 3 owners should be designated for your subscription

### Patch Management (2.6)
- System updates should be installed on your machines
- Vulnerabilities in security configuration should be remedied

### Anti-Malware (2.7)
- Endpoint protection should be installed on your machines
- Monitor missing Endpoint Protection in Azure Security Center

### Network Security (2.8)
- All network ports should be restricted
- Internet-facing virtual machines should be protected with network security groups
- Management ports should be closed on your virtual machines

### Encryption (2.9)
- Transparent Data Encryption on SQL databases should be enabled
- Storage accounts should use customer-managed key for encryption
- Disk encryption should be applied on virtual machines

### Backup (3.4)
- Azure Backup should be enabled for Virtual Machines
- Long-term geo-redundant backup should be enabled for databases

### Logging (3.5)
- Audit diagnostic setting
- Activity log should be retained for at least one year

## Key Automated Checks by Control

### 2.5 Access Control
1. `iam_user_mfa_enabled` - Multi-factor authentication for users
2. `iam_root_mfa_enabled` - MFA for root/admin accounts
3. `iam_password_policy_compliance` - Strong password policies
4. `iam_no_admin_policy` - No overly permissive policies
5. `iam_user_unused_credentials` - Remove unused access

### 2.6 Patch Management
1. `ec2_patch_compliance` - OS patch compliance
2. `rds_auto_minor_version_upgrade` - Database auto-patching
3. `elasticbeanstalk_managed_updates_enabled` - Application patching
4. `redshift_cluster_maintenance_settings` - Data warehouse patching

### 2.7 Anti-Malware Protection
1. `guardduty_enabled` - Threat detection enabled
2. `guardduty_no_high_severity_findings` - No critical threats
3. `securityhub_enabled` - Security monitoring active

### 2.8 Network Security
1. `ec2_securitygroup_ssh_restricted` - SSH access restricted
2. `ec2_securitygroup_rdp_restricted` - RDP access restricted
3. `ec2_securitygroup_common_ports_restricted` - Common ports secured
4. `vpc_flow_logs_enabled` - Network traffic logging
5. `ec2_networkacl_unrestricted_ingress` - Network ACL hardening

### 2.9 Encryption
1. `s3_bucket_encryption_enabled` - Storage encryption
2. `rds_storage_encrypted` - Database encryption
3. `ec2_ebs_volume_encrypted` - Disk encryption
4. `kms_key_rotation_enabled` - Key rotation active
5. `dynamodb_encryption_enabled` - NoSQL encryption

### 3.4 System and Data Backup
1. `backup_plan_min_retention` - Backup retention policies
2. `ec2_backup_enabled` - VM backups configured
3. `rds_backup_enabled` - Database backups active
4. `dynamodb_pitr_enabled` - Point-in-time recovery
5. `s3_bucket_versioning_enabled` - Object versioning

### 3.5 Logging and Monitoring
1. `cloudtrail_enabled` - Audit trail enabled
2. `cloudtrail_multi_region_enabled` - Multi-region logging
3. `cloudtrail_cloudwatch_logs_enabled` - Log centralization
4. `vpc_flow_logs_enabled` - Network flow logging
5. `s3_bucket_logging_enabled` - Access logging

### 5.3 Disaster Recovery Site
1. `rds_multi_az_enabled` - Database high availability
2. `s3_bucket_replication_enabled` - Cross-region replication
3. `dynamodb_global_tables_enabled` - Global data distribution

## Use Cases

### 1. NBFC Compliance Assessment
Evaluate current IT security posture against RBI mandates for NBFCs of all sizes.

### 2. Cloud Migration Planning
Assess security controls before and after migrating to cloud infrastructure.

### 3. Continuous Compliance Monitoring
Implement automated checks for ongoing compliance verification.

### 4. IS Audit Preparation
Use automated checks to prepare for annual IS Audit requirements (for large NBFCs).

### 5. Board Reporting
Generate compliance status reports for Board and IT Strategy Committee.

### 6. RBI Inspection Readiness
Maintain evidence of compliance for regulatory inspections.

## Implementation Guide

### For Large NBFCs (Asset Size ≥ ₹ 500 crore)

**Phase 1: Governance Setup (Months 1-2)**
1. Establish IT Strategy Committee (ITSC)
2. Designate CIO and CISO
3. Develop Board-approved IT Strategy
4. Create comprehensive security policies

**Phase 2: Automated Controls (Months 2-4)**
1. Deploy automated checks (16 controls, 354 checks)
2. Implement:
   - Access control mechanisms
   - Patch management processes
   - Anti-malware solutions
   - Network security controls
   - Encryption standards
   - Backup procedures
   - Logging and monitoring

**Phase 3: Manual Controls (Months 3-6)**
1. Document policies and procedures
2. Conduct Business Impact Analysis
3. Develop Cyber Crisis Management Plan
4. Establish incident reporting procedures
5. Create BCP with DR site planning

**Phase 4: Audit & Compliance (Month 6+)**
1. Engage independent IS Auditors (CISA/CISM)
2. Conduct annual IS Audit
3. Submit reports to Board and RBI
4. Implement remediation actions

### For Smaller NBFCs (Asset Size < ₹ 500 crore)

**Phase 1: Basic Setup (Month 1)**
1. Develop Board-approved IT Policy
2. Implement basic security controls

**Phase 2: Automated Checks (Months 2-3)**
1. Deploy simplified automated checks (3 controls):
   - Basic security (password policies, MFA, SSH restriction)
   - Backup procedures
   - Regulatory reporting capability

**Phase 3: Documentation (Months 3-4)**
1. Create basic BCP
2. Establish backup testing procedures
3. Ensure COSMOS reporting capability

**Phase 4: Progressive Scaling**
1. Monitor asset size growth
2. Scale up controls as organization expands
3. Transition to full compliance as threshold is crossed

## Files

### 1. RBI_NBFC_audit_results.json
Complete compliance database with all controls and automated checks.

**Structure:**
```json
{
  "id": "2_5",
  "control_id": "2.5",
  "title": "Access Control",
  "section": "2. Information and Cyber Security",
  "category": "Information Security",
  "automation_type": "automated",
  "azure_policies": [...],
  "cloud_implementations": {
    "aws": { "checks": [...] },
    "azure": { "checks": [...] },
    ...
  }
}
```

### 2. RBI_NBFC_controls_with_checks.csv
Tabular export of all controls with checks for each cloud provider.

**Columns:**
- Control_ID
- Title
- Section
- Category
- Automation_Type
- AWS_Checks (semicolon-separated)
- Azure_Checks
- GCP_Checks
- Oracle_Checks
- IBM_Checks
- Alicloud_Checks
- Total_Checks

## Integration with Cloud Platforms

### AWS
Use AWS Config Rules, Security Hub, and GuardDuty to implement checks.

### Azure
Leverage Azure Policy for continuous compliance monitoring.
- Reference: [Azure RBI NBFC Policies](https://learn.microsoft.com/en-us/azure/governance/policy/samples/rbi-itf-nbfc-2017)

### GCP
Use Security Command Center and Cloud Security Scanner.

### Multi-Cloud
Deploy checks consistently across all providers using Infrastructure as Code (Terraform, CloudFormation, ARM templates).

## Reporting

### Board Reports
Generate quarterly reports for ITSC showing:
- Compliance status by control
- Automated check results
- Manual control review status
- Remediation progress

### RBI Reporting
Maintain evidence for:
- Cyber incident reporting (immediate)
- Annual IS Audit reports
- Policy compliance documentation

### Audit Evidence
Collect and maintain:
- Automated check logs
- Policy documentation
- BCP test results
- Incident response records
- Outsourcing contracts and reviews

## Key Differences from Other Frameworks

### vs. NIST 800-53
- **RBI NBFC**: India-specific for financial sector
- **Focus**: IT governance, cyber security, BCP
- **Applicability**: Size-based (₹ 500 crore threshold)
- **Audit**: Annual IS Audit mandatory for large NBFCs

### vs. PCI DSS
- **RBI NBFC**: Broader IT framework (not just payments)
- **Scope**: All IT operations and governance
- **Sector**: NBFCs specifically

### vs. ISO 27001
- **RBI NBFC**: Regulatory mandate (not voluntary)
- **Penalties**: RBI can impose sanctions
- **Reporting**: Direct reporting to regulator

## Critical Compliance Points

### 1. Cyber Incident Reporting
**Mandatory**: Immediate reporting of significant cyber incidents to RBI

### 2. Board Oversight
All major policies must be Board-approved:
- IT Strategy
- Information Security Policy
- Cyber Security Policy
- BCP
- IT Outsourcing Policy

### 3. Annual IS Audit (Large NBFCs)
- Independent external auditors
- CISA/CISM qualification preferred
- Report to Board and RBI

### 4. Separation of Roles
- CIO and CISO must be separate persons
- CISO must have adequate independence

### 5. Regulatory Reporting
IT systems must support timely and accurate COSMOS returns to RBI

## Penalties for Non-Compliance

RBI may impose:
- Monetary penalties
- Business restrictions
- Enhanced supervision
- Show cause notices
- In severe cases: Registration cancellation

## Support and Resources

### Official Resources
- **RBI**: [www.rbi.org.in](https://www.rbi.org.in)
- **CERT-In**: [www.cert-in.org.in](https://www.cert-in.org.in)
- **NCIIPC**: National Critical Information Infrastructure Protection Centre

### Cloud Provider Resources
- **AWS**: AWS Config, Security Hub
- **Azure**: [Azure RBI NBFC Policies](https://learn.microsoft.com/en-us/azure/governance/policy/samples/rbi-itf-nbfc-2017)
- **GCP**: Security Command Center

### Professional Certifications
- **CISA**: Certified Information Systems Auditor
- **CISM**: Certified Information Security Manager
- **CISSP**: Certified Information Systems Security Professional

## FAQs

**Q: Is this agent suitable for both large and small NBFCs?**  
A: Yes. The agent includes controls for both categories with clear applicability markers.

**Q: How often should automated checks run?**  
A: Daily or continuous monitoring recommended for critical security controls.

**Q: Can this replace the annual IS Audit?**  
A: No. Automated checks complement but don't replace the mandatory IS Audit by independent auditors.

**Q: What if we operate across multiple clouds?**  
A: The agent provides equivalent checks for all 6 major cloud providers for consistent compliance.

**Q: How do we handle manual controls?**  
A: Manual controls require documentation review, policy verification, and governance process assessment.

**Q: What about outsourced IT operations?**  
A: NBFCs remain accountable. Ensure contracts include required controls and RBI audit rights.

## Version History

- **v1.0** (November 2025): Initial release
  - 37 controls mapped
  - 16 automated, 21 manual
  - 354 checks across 6 cloud providers
  - Azure policy references included

## License and Disclaimer

This compliance agent is for reference purposes. NBFCs should:
- Consult with legal and compliance advisors
- Refer to official RBI Master Direction
- Engage qualified IS Auditors
- Customize based on specific business context

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Status**: Production Ready ✅

