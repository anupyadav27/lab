# CISA Cyber Essentials Compliance Database

## Overview

The **CISA Cyber Essentials** is a guide developed by the Cybersecurity & Infrastructure Security Agency (CISA) to help organizations build a culture of cyber readiness. It provides practical, actionable steps that organizations of all sizes can take to improve their cybersecurity posture.

This compliance database provides automated security checks mapped to CISA Cyber Essentials controls across 6 cloud providers.

## Framework Details

- **Source**: CISA (Cybersecurity & Infrastructure Security Agency)
- **Official Reference**: [CISA Cyber Essentials](https://www.cisa.gov/cyber-essentials)
- **AWS Config Reference**: [Operational Best Practices for CISA CE](https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-cisa-ce.html)
- **Total Controls**: 22
- **Automated Controls**: 15 (68.2%)
- **Manual Controls**: 7 (31.8%)
- **Total Checks**: 366 (across 6 cloud providers)

## Framework Structure

CISA Cyber Essentials organizes controls into 6 essential elements:

### 1. **Yourself - The Leader** (Manual)
Drive cybersecurity strategy, investment, and culture

### 2. **Your Staff - The Users** (5 controls - Manual)
- Develop security awareness
- Learn about phishing and business email compromise
- Maintain cybersecurity awareness
- Leverage cybersecurity training
- Identify training resources

### 3. **Your Systems - What Makes You Operational** (3 controls - Automated)
- Maintain hardware/software inventories
- Maintain network connection inventories
- Maintain information inventories

### 4. **Your Surroundings - The Digital Workplace** (4 controls - Automated)
- Multi-factor authentication
- Least privilege access
- Strong password policies
- User lifecycle management

### 5. **Your Data - What the Business is Built On** (4 controls - Automated)
- Network monitoring
- Data protection and encryption
- Malware protection
- Automated backups

### 6. **Your Crisis Response** (2 controls - Manual)
- Incident response planning
- Business impact assessments

### 7. **Booting Up: Things to Do First** (4 controls - Automated)
- Automated backups
- Multi-factor authentication
- Patch management
- Secure configurations

## Automation Strategy

### Automated Controls (68.2%)
Controls that can be continuously monitored through technical checks:
- Asset inventory and management
- Multi-factor authentication enforcement
- Patch compliance
- Backup configurations
- Security configurations
- Access control policies
- Network monitoring
- Data encryption
- Malware protection

### Manual Controls (31.8%)
Controls requiring human judgment and organizational processes:
- Security awareness programs
- Cybersecurity training
- Incident response planning
- Business continuity planning
- Leadership commitment to cybersecurity

## Cloud Provider Coverage

This database provides equivalent security checks across 6 cloud providers:

1. **AWS** - Amazon Web Services
2. **Azure** - Microsoft Azure
3. **GCP** - Google Cloud Platform
4. **Oracle** - Oracle Cloud Infrastructure
5. **IBM** - IBM Cloud
6. **Alicloud** - Alibaba Cloud

### Check Naming Convention

All checks follow the standard format: `{provider}_{service}_{check_description}`

**Examples:**
- AWS: `aws_iam_user_mfa_enabled`
- Azure: `azure_entra_user_mfa_enabled`
- GCP: `gcp_iam_user_mfa_enabled`
- Oracle: `oracle_identity_user_mfa_enabled`
- IBM: `ibm_iam_user_mfa_enabled`
- Alicloud: `alicloud_ram_user_mfa_enabled`

## AWS Config Rules Mapping

This database leverages AWS Config Rules as the foundation for check definitions. Key mappings include:

### Identity & Access Management
- `iam-user-mfa-enabled` → `iam_user_mfa_enabled`
- `mfa-enabled-for-iam-console-access` → `iam_console_mfa_enabled`
- `root-account-mfa-enabled` → `iam_root_mfa_enabled`
- `iam-policy-no-statements-with-admin-access` → `iam_no_admin_policy`
- `iam-user-no-policies-check` → `iam_user_no_inline_policies`

### Backup & Recovery
- `backup-plan-min-frequency-and-min-retention-check` → `backup_plan_min_retention`
- `db-instance-backup-enabled` → `rds_instance_backup_enabled`
- `dynamodb-pitr-enabled` → `dynamodb_pitr_enabled`

### Monitoring & Logging
- `cloudtrail-enabled` → `cloudtrail_enabled`
- `guardduty-enabled-centralized` → `guardduty_enabled`
- `vpc-flow-logs-enabled` → `vpc_flow_logs_enabled`

### Security Configurations
- `ec2-instance-no-public-ip` → `ec2_instance_no_public_ip`
- `restricted-ssh` → `ec2_securitygroup_ssh_restricted`
- `s3-bucket-server-side-encryption-enabled` → `s3_bucket_encryption_enabled`

## Statistics

### Controls by Category

| Category | Controls | Automated | Manual |
|----------|----------|-----------|--------|
| Your Staff | 5 | 0 | 5 |
| Your Systems | 3 | 3 | 0 |
| Your Surroundings | 4 | 4 | 0 |
| Your Data | 4 | 4 | 0 |
| Booting Up | 4 | 4 | 0 |
| Your Crisis Response | 2 | 0 | 2 |
| **Total** | **22** | **15** | **7** |

### Checks per Cloud Provider

| Provider | Checks | Coverage |
|----------|--------|----------|
| AWS | 61 | 100% |
| Azure | 61 | 100% |
| GCP | 61 | 100% |
| Oracle | 61 | 100% |
| IBM | 61 | 100% |
| Alicloud | 61 | 100% |
| **Total** | **366** | **6 providers** |

### Top Control Areas by Check Count

1. **Booting Up-1** (Backups): 9 checks
2. **Your Systems-1** (Asset Inventory): 7 checks
3. **Your Data-2** (Data Protection): 5 checks
4. **Booting Up-4** (Secure Configurations): 5 checks
5. **Your Data-1** (Network Monitoring): 5 checks
6. **Your Data-4** (Automated Backups): 5 checks

## Use Cases

### 1. Small Business Cybersecurity
CISA CE is designed for organizations of all sizes, with particular focus on small and medium businesses that may not have dedicated cybersecurity teams.

### 2. Cybersecurity Maturity Assessment
Use as a baseline assessment to measure and improve organizational cybersecurity posture.

### 3. Employee Awareness Programs
Manual controls provide guidance for building security awareness and training programs.

### 4. Cloud Security Hardening
Automated checks ensure consistent security configurations across cloud environments.

### 5. Incident Response Preparation
Crisis response controls guide development of incident response and business continuity plans.

## Files

### 1. CISA_CE_audit_results.json
Complete compliance database with all controls and checks in JSON format.

**Structure:**
```json
{
  "id": "your_staff_1",
  "control_id": "Your Staff-1",
  "title": "Develop a culture of awareness...",
  "category": "Your Staff",
  "automation_type": "manual",
  "cloud_implementations": {
    "aws": { "checks": [...] },
    "azure": { "checks": [...] },
    ...
  }
}
```

### 2. CISA_CE_controls_with_checks.csv
Tabular export of all controls with associated checks for each cloud provider.

**Columns:**
- Control_ID
- Title
- Category
- Automation_Type
- AWS_Checks (semicolon-separated)
- Azure_Checks
- GCP_Checks
- Oracle_Checks
- IBM_Checks
- Alicloud_Checks
- Total_Checks

## Implementation Guide

### Step 1: Assess Current State
Review each control and evaluate your organization's current compliance status.

### Step 2: Prioritize Based on Risk
Focus first on:
1. **Booting Up** controls (foundational security)
2. **Your Surroundings** (access control)
3. **Your Data** (data protection)

### Step 3: Implement Automated Checks
Deploy automated checks for the 15 automated controls across your cloud environments.

### Step 4: Develop Manual Processes
For the 7 manual controls:
- Establish security awareness programs
- Create training curricula
- Develop incident response plans
- Conduct business impact assessments

### Step 5: Continuous Monitoring
- Run automated checks regularly (daily/weekly)
- Update training materials quarterly
- Review and test incident response plans annually

## Key Recommendations

### For Leadership
1. **Invest in Cybersecurity** - Allocate budget for tools, training, and personnel
2. **Build Trusted Networks** - Join ISACs and industry groups
3. **Lead by Example** - Champion cybersecurity culture from the top

### For IT Teams
1. **Automate Where Possible** - Use these checks to implement continuous compliance
2. **Maintain Inventories** - Know what's on your network
3. **Enable MFA Everywhere** - Start with privileged accounts, expand to all users
4. **Backup Religiously** - Test restoration regularly

### For All Staff
1. **Stay Aware** - Participate in security awareness training
2. **Report Suspicious Activity** - Know who to contact
3. **Use Strong Authentication** - Enable MFA, use password managers
4. **Think Before Clicking** - Verify suspicious emails

## Compliance Mapping

CISA Cyber Essentials aligns with other frameworks:

- **NIST Cybersecurity Framework** - Core functions (Identify, Protect, Detect, Respond, Recover)
- **CIS Controls** - Foundational security practices
- **ISO 27001** - Information security management
- **NIST 800-53** - Federal security controls
- **SOC 2** - Service organization controls

## Additional Resources

- **CISA Official Site**: https://www.cisa.gov/cyber-essentials
- **AWS Config Best Practices**: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-cisa-ce.html
- **Cyber Readiness Institute**: https://cyberreadinessinstitute.org/
- **Small Business Cybersecurity**: https://www.sba.gov/business-guide/manage-your-business/stay-safe-cybersecurity-threats

## Build Information

- **Build Date**: November 2025
- **Source Data**: AWS Config Conformance Pack for CISA CE
- **Check Mapping**: Based on AWS Config rules with multi-cloud equivalents
- **Methodology**: AWS Config rule → check name → multi-cloud mapping
- **Validation**: Cross-referenced with official CISA Cyber Essentials guide

## Notes

1. **Process Checks**: Some controls (like security awareness programs) are marked as "Process Check" in AWS Config - these are manual controls requiring organizational processes.

2. **Shared Responsibility**: Remember that cloud security is a shared responsibility. These checks validate cloud resource configurations, but organizations are responsible for:
   - Application security
   - Data classification
   - Employee training
   - Incident response execution

3. **Context Matters**: Automated checks detect configuration issues, but human judgment is needed to:
   - Assess risk in organizational context
   - Determine appropriate remediation
   - Balance security with business needs

4. **Continuous Improvement**: Cybersecurity is an ongoing journey. Regularly review and update your compliance posture as threats evolve.

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Status**: Production Ready ✅

