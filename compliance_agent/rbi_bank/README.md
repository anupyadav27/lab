# RBI IT Framework for Banks v2016 Compliance Agent

## Overview

This compliance agent provides automated security checks and manual control guidance for the **Reserve Bank of India (RBI) IT Framework for Banks v2016**. The agent maps RBI controls to cloud-native security checks across 6 cloud providers.

## Framework Details

- **Source**: Reserve Bank of India (RBI)
- **Document**: Master Direction - Information Technology Governance, Risk, Controls and Assurance Practices (ITGRCA)
- **Version**: 2016
- **RBI Reference**: [RBI Official Website](https://www.rbi.org.in)
- **Azure Policy Reference**: [Azure RBI IT Framework for Banks](https://learn.microsoft.com/en-us/azure/governance/policy/samples/rbi-itf-banks-2016)
- **AWS Reference**: [AWS Config Best Practices for RBI MD-ITF](https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-rbi-md-itf.html)
- **Total Controls**: 27
- **Automated Controls**: 20 (74.1%)
- **Manual Controls**: 7 (25.9%)
- **Total Checks**: 432 (across 6 cloud providers)

## Automation Strategy

### Automated Controls (74.1%)

High automation rate for technical security controls:

**Authentication (2 controls):**
- SSH Key Authentication (3 checks)
- Guest Account Management (3 checks)

**Network Security (2 controls):**
- Network Inventory Management (3 checks)
- Network Access Controls (5 checks)

**Information Security (2 controls - out of 3):**
- Access Control Management (5 checks)
- Data Encryption (5 checks)

**Logging and Monitoring (2 controls):**
- Audit Logging (5 checks)
- Security Monitoring (4 checks)

**Backup and Recovery (2 controls):**
- Data Backup (5 checks)
- Disaster Recovery (3 checks)

**Database Security (2 controls):**
- Database Encryption (4 checks)
- Database Access Control (3 checks)

**Additional Automated:**
- Patch Management (3 checks)
- Certificate Management (2 checks)
- Container Security (3 checks)
- Key Vault Management (3 checks)
- API Security (3 checks)
- Change Management (3 checks)
- Incident Management (3 checks)
- Data Privacy (4 checks)

### Manual Controls (25.9%)

Controls requiring human judgment and organizational processes:

**IT Governance (2 controls):**
- IT Governance Framework
- IT Strategy

**Information Security (1 control):**
- Information Security Policy

**Business Continuity (2 controls):**
- Business Continuity Plan
- BCP Testing

**Risk Management (1 control):**
- Vendor Risk Assessment

**IS Audit (1 control):**
- IS Audit Requirements

## Check Coverage by Category

| Category | Controls | Automated | Manual | Automation % | Total Checks |
|----------|----------|-----------|--------|--------------|--------------|
| Authentication | 2 | 2 | 0 | 100% | 36 |
| Network Security | 2 | 2 | 0 | 100% | 48 |
| Information Security | 8 | 5 | 3 | 62.5% | 132 |
| IT Operations | 4 | 4 | 0 | 100% | 72 |
| Business Continuity | 4 | 2 | 2 | 50% | 48 |
| IT Governance | 2 | 0 | 2 | 0% | 0 |
| Risk Management | 1 | 0 | 1 | 0% | 0 |
| IS Audit | 1 | 0 | 1 | 0% | 0 |
| **Total** | **27** | **20** | **7** | **74.1%** | **432** |

## Cloud Provider Coverage

All automated checks are available across 6 cloud providers:

1. **AWS** - Amazon Web Services (72 checks)
2. **Azure** - Microsoft Azure (72 checks)
3. **GCP** - Google Cloud Platform (72 checks)
4. **Oracle** - Oracle Cloud Infrastructure (72 checks)
5. **IBM** - IBM Cloud (72 checks)
6. **Alicloud** - Alibaba Cloud (72 checks)

**Total Multi-Cloud Checks**: 432

## Azure Policy Mapping

This agent leverages Azure Policy samples for RBI IT Framework for Banks. Key mappings:

### Authentication (9.1, 9.3)
- Authentication to Linux machines should require SSH keys
- Guest accounts with owner permissions should be removed
- Guest accounts with read permissions should be removed
- Guest accounts with write permissions should be removed

### Data Encryption (3.3, 8.1)
- Transparent Data Encryption on SQL databases should be enabled
- Storage accounts should use customer-managed key for encryption
- Disk encryption should be applied on virtual machines

### Certificate Management (7.1)
- Certificates should have the specified maximum validity period
- Certificates should not expire within the specified number of days

### Container Security (10.1)
- Container registries should be encrypted with customer-managed key

### Key Management (11.1)
- Key vaults should have deletion protection enabled
- Key vaults should have soft delete enabled

### Patch Management (21.2)
- Hotpatch should be enabled for Windows Server Azure Edition VMs

## Key Automated Checks by Control

### 9.1 Authentication Framework
1. `ec2_instance_ssh_key_authentication` - SSH key-based authentication
2. `ec2_securitygroup_ssh_restricted` - SSH access restricted
3. `iam_no_root_access_key` - No root access keys

### 9.3 Guest Account Management
1. `iam_user_unused_credentials` - Remove unused credentials
2. `iam_no_guest_accounts_with_permissions` - No guest accounts
3. `iam_user_group_membership` - Proper group membership

### 3.2 Access Control Management
1. `iam_user_mfa_enabled` - MFA for users
2. `iam_root_mfa_enabled` - MFA for root
3. `iam_password_policy_compliance` - Strong passwords
4. `iam_no_admin_policy` - No overly permissive policies
5. `iam_user_no_inline_policies` - No inline policies

### 3.3 Data Encryption
1. `s3_bucket_encryption_enabled` - Storage encryption
2. `rds_storage_encrypted` - Database encryption
3. `ec2_ebs_volume_encrypted` - Disk encryption
4. `dynamodb_encryption_enabled` - NoSQL encryption
5. `kms_key_rotation_enabled` - Key rotation

### 4.3 Network Access Controls
1. `ec2_securitygroup_default_restricted` - Default security group restricted
2. `ec2_securitygroup_ssh_restricted` - SSH restricted
3. `ec2_securitygroup_rdp_restricted` - RDP restricted
4. `vpc_flow_logs_enabled` - Network flow logging
5. `ec2_networkacl_unrestricted_ingress` - Network ACL hardening

### 5.1 Audit Logging
1. `cloudtrail_enabled` - Audit trail enabled
2. `cloudtrail_multi_region_enabled` - Multi-region logging
3. `cloudtrail_log_file_validation_enabled` - Log integrity
4. `cloudwatch_log_group_retention` - Log retention
5. `s3_bucket_logging_enabled` - Access logging

### 5.2 Security Monitoring
1. `guardduty_enabled` - Threat detection
2. `securityhub_enabled` - Security hub
3. `vpc_flow_logs_enabled` - Flow logs
4. `cloudwatch_alarm_configured` - Alerting

### 6.1 Data Backup
1. `backup_plan_min_retention` - Backup retention
2. `ec2_backup_enabled` - VM backups
3. `rds_backup_enabled` - Database backups
4. `dynamodb_pitr_enabled` - Point-in-time recovery
5. `s3_bucket_versioning_enabled` - Object versioning

### 6.2 Disaster Recovery
1. `rds_multi_az_enabled` - High availability
2. `s3_bucket_replication_enabled` - Cross-region replication
3. `dynamodb_global_tables_enabled` - Global distribution

### 8.1 Database Encryption
1. `rds_storage_encrypted` - RDS encryption
2. `rds_instance_backup_encrypted` - Backup encryption
3. `dynamodb_encryption_enabled` - DynamoDB encryption
4. `redshift_cluster_encrypted` - Data warehouse encryption

### 8.2 Database Access Control
1. `rds_instance_no_public_access` - No public database access
2. `redshift_cluster_public_access` - Data warehouse not public
3. `rds_instance_iam_authentication_enabled` - IAM authentication

### 17.1 Customer Data Protection
1. `s3_bucket_public_read_prohibited` - No public read
2. `s3_bucket_public_write_prohibited` - No public write
3. `rds_instance_no_public_access` - Database not public
4. `ec2_instance_no_public_ip` - Compute not public

## Use Cases

### 1. Banking Sector Compliance
Assess IT security posture against RBI mandates for banks operating in India.

### 2. Financial Services Audit
Prepare for IS audits and regulatory inspections by RBI.

### 3. Cloud Banking Infrastructure
Validate security controls for cloud-based banking systems.

### 4. Third-Party Risk Assessment
Evaluate vendor compliance with RBI framework requirements.

### 5. Digital Banking Security
Ensure security standards for online and mobile banking platforms.

### 6. Core Banking Modernization
Assess security during core banking system migration to cloud.

## Implementation Guide

### For Large Banks

**Phase 1: Governance (Months 1-2)**
1. Establish IT governance framework
2. Develop RBI-compliant IT strategy
3. Create comprehensive security policies
4. Set up Board oversight mechanisms

**Phase 2: Authentication & Access (Months 2-3)**
1. Implement MFA across all systems
2. Deploy SSH key authentication
3. Remove guest accounts and unused credentials
4. Establish role-based access controls
5. Deploy automated checks (36 authentication checks)

**Phase 3: Network Security (Months 3-4)**
1. Implement network segmentation
2. Configure security groups and ACLs
3. Enable VPC flow logs
4. Deploy automated checks (48 network checks)

**Phase 4: Data Protection (Months 4-6)**
1. Enable encryption at rest and in transit
2. Implement key management
3. Configure database encryption
4. Deploy automated checks (132 information security checks)

**Phase 5: Operations & Monitoring (Months 5-7)**
1. Enable comprehensive logging
2. Deploy security monitoring tools
3. Configure automated backups
4. Establish DR procedures
5. Deploy automated checks (72 operations checks)

**Phase 6: Compliance & Audit (Month 7+)**
1. Conduct IS audit
2. Generate compliance reports
3. Document manual controls
4. Continuous monitoring

### For Regional/Smaller Banks

**Phased Approach:**
1. Start with critical controls (authentication, encryption, backup)
2. Deploy high-priority automated checks
3. Gradually expand coverage
4. Scale based on regulatory requirements

## Files

### 1. RBI_BANK_audit_results.json
Complete compliance database with all controls and automated checks.

**Structure:**
```json
{
  "id": "9_1",
  "control_id": "9.1",
  "title": "Authentication Framework - SSH Key Authentication",
  "section": "9. Authentication Framework for Customers",
  "category": "Authentication",
  "automation_type": "automated",
  "azure_policies": [...],
  "cloud_implementations": {
    "aws": { "checks": [...] },
    ...
  }
}
```

### 2. RBI_BANK_controls_with_checks.csv
Tabular export for compliance tracking and reporting.

## Integration with Cloud Platforms

### AWS
- AWS Config Rules
- AWS Security Hub
- AWS GuardDuty
- Reference: [AWS RBI MD-ITF Best Practices](https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-rbi-md-itf.html)

### Azure
- Azure Policy
- Azure Security Center
- Azure Sentinel
- Reference: [Azure RBI Banks Policy](https://learn.microsoft.com/en-us/azure/governance/policy/samples/rbi-itf-banks-2016)

### GCP
- Security Command Center
- Cloud Security Scanner
- Cloud Asset Inventory

### Multi-Cloud
Deploy checks using Infrastructure as Code (Terraform, CloudFormation, ARM templates).

## Reporting

### RBI Reporting
- IS Audit reports
- Cyber incident reporting
- Policy compliance documentation
- Security posture reports

### Board Reports
- Quarterly compliance status
- Risk assessment summaries
- Incident reports
- Audit findings

### Audit Evidence
- Automated check logs
- Policy documents
- Change logs
- Incident response records
- BCP test results

## Key Differences from RBI NBFC Framework

| Aspect | RBI Bank | RBI NBFC |
|--------|----------|----------|
| **Applicability** | All banks in India | NBFCs (size-based) |
| **Automation** | 74.1% | 43.2% |
| **Total Controls** | 27 | 37 |
| **Total Checks** | 432 | 354 |
| **Focus** | Banking operations | NBFC operations |
| **Governance** | Bank Board | ITSC for large NBFCs |
| **Special Requirements** | Customer authentication | COSMOS reporting |

## Critical Compliance Points

### 1. Customer Authentication
Mandatory strong authentication for digital banking services.

### 2. Data Encryption
All customer data must be encrypted at rest and in transit.

### 3. Audit Logging
Comprehensive logging of all system and user activities.

### 4. Incident Management
Immediate reporting of significant cyber incidents to RBI.

### 5. Business Continuity
Tested BCP with DR capabilities for critical banking systems.

### 6. IS Audit
Annual independent IS audit with report to Board and RBI.

### 7. Third-Party Risk
Vendor risk assessment for all IT service providers.

## Penalties for Non-Compliance

RBI may impose:
- Monetary penalties
- Business restrictions
- Enhanced regulatory supervision
- In severe cases: Banking license suspension/cancellation

## Support and Resources

### Official Resources
- **RBI**: [www.rbi.org.in](https://www.rbi.org.in)
- **CERT-In**: [www.cert-in.org.in](https://www.cert-in.org.in)
- **IBA**: Indian Banks' Association

### Cloud Provider Resources
- **AWS**: [RBI MD-ITF Best Practices](https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-rbi-md-itf.html)
- **Azure**: [RBI Banks Policy](https://learn.microsoft.com/en-us/azure/governance/policy/samples/rbi-itf-banks-2016)

### Professional Certifications
- **CISA**: Certified Information Systems Auditor
- **CISM**: Certified Information Security Manager
- **CISSP**: Certified Information Systems Security Professional
- **DISA**: Diploma in Information Systems Audit (ICAI)

## FAQs

**Q: Is this applicable to all banks in India?**  
A: Yes, all scheduled commercial banks, cooperative banks, and regional rural banks.

**Q: How does this differ from RBI NBFC framework?**  
A: Higher automation (74% vs 43%), focus on banking-specific controls like customer authentication.

**Q: Can foreign banks use this?**  
A: Yes, foreign banks operating in India must comply with RBI IT framework.

**Q: What about digital-only banks?**  
A: Fully applicable, with additional focus on cloud security and API security controls.

**Q: How often should automated checks run?**  
A: Daily or continuous monitoring for critical controls.

**Q: What about core banking systems?**  
A: Framework applies to all IT systems including core banking, but implementation may vary by architecture.

## Version History

- **v1.0** (November 2025): Initial release
  - 27 controls mapped
  - 20 automated, 7 manual
  - 432 checks across 6 cloud providers
  - Azure and AWS policy references

## License and Disclaimer

This compliance agent is for reference purposes. Banks should:
- Consult with legal and compliance teams
- Refer to official RBI Master Direction
- Engage qualified IS Auditors (CISA/CISM/DISA)
- Customize based on specific banking operations

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Status**: Production Ready ✅

