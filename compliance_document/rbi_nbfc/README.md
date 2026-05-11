# RBI NBFC IT Framework Controls

## Overview

The **Reserve Bank of India (RBI) Master Direction on Information Technology Framework for the NBFC Sector** provides comprehensive guidelines for IT governance, information security, cyber security, and business continuity for Non-Banking Financial Companies (NBFCs) in India.

This framework is mandatory for NBFCs operating in India and establishes baseline IT standards based on asset size.

## Framework Details

- **Source**: Reserve Bank of India (RBI)
- **Document**: Master Direction - Information Technology Framework for the NBFC Sector
- **Official Link**: [RBI Notification](https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=10999&Mode=0)
- **Azure Reference**: [Azure Policy for RBI ITF NBFC](https://learn.microsoft.com/en-us/azure/governance/policy/samples/rbi-itf-nbfc-2017)
- **Date Issued**: June 8, 2017
- **Total Controls**: 37
- **Applicability**: All NBFCs (Non-Banking Financial Companies) in India

## Framework Structure

The RBI NBFC IT Framework is organized into 7 main sections:

### 1. **IT Governance** (4 controls)
Establishes governance structure and leadership roles for IT management.

**Key Requirements:**
- Board Approved IT Strategy (aligned with business strategy)
- IT Strategy Committee of the Board (ITSC)
- Chief Information Officer (CIO) designation
- Chief Information Security Officer (CISO) designation (separate from CIO)

**Applicability**: NBFCs with asset size ≥ ₹ 500 crore

### 2. **Information and Cyber Security** (12 controls)
Comprehensive security requirements covering policies, controls, and incident management.

**Key Requirements:**
- Information Security Policy (Board approved)
- Cyber Security Policy
- Cyber Crisis Management Plan
- Cyber Incident Reporting to RBI
- Access Control mechanisms
- Patch Management
- Anti-Malware Protection
- Network Security (Firewalls, IDS/IPS)
- Encryption (data at rest and in transit)
- Secure Software Development
- Mobile Financial Services Security
- Social Media Usage Policy

**Applicability**: All NBFCs (some controls specific to larger NBFCs)

### 3. **IT Operations** (5 controls)
Operational controls for day-to-day IT management.

**Key Requirements:**
- Change Management process
- Capacity Management
- Incident Management
- System and Data Backup
- Logging and Monitoring

**Applicability**: All NBFCs

### 4. **IS Audit** (3 controls)
Requirements for independent auditing of IT systems and controls.

**Key Requirements:**
- Annual IS Audit (by independent auditors)
- Comprehensive IS Audit Scope
- Use of Computer Assisted Audit Techniques (CAATs)

**Applicability**: NBFCs with asset size ≥ ₹ 500 crore

**Note**: Auditors qualified as CISA (Certified Information Systems Auditor) or CISM (Certified Information Security Manager) are preferred.

### 5. **Business Continuity Planning** (4 controls)
Requirements for ensuring business resilience and disaster recovery.

**Key Requirements:**
- Business Continuity Plan (Board approved)
- Business Impact Analysis
- Disaster Recovery Site (for critical systems)
- Annual BCP Testing

**Applicability**: All NBFCs

### 6. **IT Services Outsourcing** (4 controls)
Governance and risk management for IT outsourcing arrangements.

**Key Requirements:**
- IT Outsourcing Policy (Board approved)
- Comprehensive Outsourcing Contracts
- Outsourcing Risk Management
- Service Provider BCP requirements

**Applicability**: NBFCs outsourcing IT services

### 7. **Requirements for Smaller NBFCs** (5 controls)
Simplified requirements for NBFCs with asset size below ₹ 500 crore.

**Key Requirements:**
- Basic IT Policy (Board approved)
- Basic Security Controls
- Data Backup arrangements
- Basic BCP
- Regulatory Reporting capability (COSMOS returns)

**Applicability**: NBFCs with asset size < ₹ 500 crore

## Applicability by NBFC Size

### Large NBFCs (Asset Size ≥ ₹ 500 crore)

**Must Comply With:**
- All 37 controls
- Full IT Governance structure (ITSC, CIO, CISO)
- Annual IS Audit mandatory
- Comprehensive BCP with DR site
- Secure Software Development practices
- Advanced monitoring and security controls

**Total Controls**: 32 (including 27 general + 5 size-specific)

### Smaller NBFCs (Asset Size < ₹ 500 crore)

**Must Comply With:**
- 20 controls (15 general + 5 simplified)
- Board approved IT Policy (simplified)
- Basic security controls
- Basic BCP with annual testing
- Data backup arrangements
- Regulatory reporting capability

**Progressive Scaling**: IT systems should be scaled up as size and complexity increases.

## Control Categories

| Category | Controls | Description |
|----------|----------|-------------|
| **IT Governance** | 5 | Board oversight, IT strategy, CIO/CISO roles |
| **Information Security** | 13 | Policies, access control, encryption, security controls |
| **IT Operations** | 7 | Change management, backup, monitoring, incident mgmt |
| **IT Outsourcing** | 4 | Outsourcing governance and risk management |
| **Business Continuity** | 5 | BCP, DR, business impact analysis |
| **IS Audit** | 3 | Annual audit, scope, CAATs |
| **Total** | **37** | |

## Key Mandatory Requirements

### For All NBFCs

1. **Information Security Policy** - Board approved, reviewed annually
2. **Cyber Security Policy** - Detection, prevention, response, recovery
3. **Cyber Incident Reporting** - Immediate reporting to RBI
4. **Access Control** - User authentication, RBAC, privileged access management
5. **Patch Management** - Timely patching with testing
6. **Anti-Malware** - Deployed and regularly updated
7. **Network Security** - Firewalls, IDS/IPS, segmentation
8. **Encryption** - Data at rest and in transit
9. **Backup** - Regular automated backups with testing
10. **BCP** - Board approved with annual testing
11. **Logging & Monitoring** - Comprehensive logs with regular review

### For Large NBFCs (≥ ₹ 500 crore)

12. **IT Strategy** - Board approved, aligned with business
13. **ITSC** - IT Strategy Committee with 2+ Board members
14. **CIO** - Senior official reporting to MD/CEO
15. **CISO** - Separate from CIO with adequate authority
16. **Cyber Crisis Management Plan** - Board approved
17. **Annual IS Audit** - By independent external auditors
18. **DR Site** - Backup site for critical systems
19. **Secure Development** - Secure coding, testing, vulnerability assessments
20. **Capacity Management** - Monitoring and planning

## Special Requirements

### Mobile Financial Services
NBFCs offering mobile financial services must implement:
- Multi-factor authentication
- Secure communication channels
- Device binding
- Transaction limits

### Social Media Usage
NBFCs using social media officially must have:
- Approved social media policy
- Authorized personnel only
- Channel monitoring
- Incident response procedures

### IT Outsourcing
NBFCs outsourcing IT services must:
- Obtain Board approval for outsourcing policy
- Conduct due diligence on service providers
- Have comprehensive written agreements
- Retain audit rights (for NBFC and RBI)
- Ensure service provider has adequate BCP

## Cyber Incident Reporting

NBFCs must report **significant cyber incidents** to RBI immediately.

**What to Report:**
- Unauthorized access to systems/data
- Data breaches
- Ransomware attacks
- DDoS attacks
- Significant service disruptions
- Any incident impacting customer data or services

**Reporting Timeline**: Immediate (as soon as incident is detected)

## IS Audit Requirements (Large NBFCs)

### Frequency
- **Annual IS Audit** is mandatory
- Report submitted to Board and RBI

### Auditor Qualifications
- Independent external auditors
- CISA (Certified Information Systems Auditor) or
- CISM (Certified Information Security Manager) preferred

### Audit Scope
Must cover:
1. IT Governance assessment
2. Information and Cyber Security controls
3. IT Operations review
4. Regulatory compliance verification
5. Business Continuity Planning
6. IT Outsourcing arrangements

### Use of CAATs
Auditors should use Computer Assisted Audit Techniques in:
- Revenue leakage detection
- Treasury functions assessment
- Control weakness impact analysis
- AML transaction monitoring
- High-volume transaction areas

## Implementation Timeline

**For NBFCs with asset size < ₹ 500 crore:**
- Basic IT systems and policies: By September 30, 2018
- Progressive scaling as size increases

**For NBFCs with asset size ≥ ₹ 500 crore:**
- Full compliance with all requirements: Immediate
- Annual IS Audit: Starting from FY following notification

## Azure Cloud Compliance

Microsoft Azure provides a compliance offering for RBI NBFC IT Framework.

**Reference**: [Azure Policy for RBI ITF NBFC](https://learn.microsoft.com/en-us/azure/governance/policy/samples/rbi-itf-nbfc-2017?context=%2Fazure%2Fgovernance%2Fpolicy%2Fcontext%2Fpolicy-context)

Azure policies can help NBFCs:
- Implement required security controls
- Monitor compliance continuously
- Generate audit reports
- Ensure encryption standards
- Manage access controls
- Monitor cyber security posture

## Comparison with Other Frameworks

The RBI NBFC IT Framework aligns with international standards:

| Framework | Alignment |
|-----------|-----------|
| **ISO 27001** | Information security management |
| **NIST Cybersecurity Framework** | Identify, Protect, Detect, Respond, Recover |
| **COBIT** | IT governance and management |
| **PCI DSS** | Payment card data security (if applicable) |
| **GDPR** | Data protection (for international operations) |

## Key Governance Bodies

### IT Strategy Committee (ITSC)
**Composition:**
- At least 2 Board members
- At least 1 member with technology expertise
- CIO as permanent invitee

**Responsibilities:**
- Approve IT strategy and policies
- Monitor IT risk and security
- Oversee IT investments
- Review IS Audit reports
- Ensure compliance with RBI directions

**Meeting Frequency**: At least once every quarter

### Chief Information Officer (CIO)
**Requirements:**
- Senior level official
- Direct reporting to MD/CEO
- Part of Top Management

**Responsibilities:**
- IT strategy formulation and execution
- IT risk management
- BCP monitoring
- IT operations oversight
- Coordination with CISO

### Chief Information Security Officer (CISO)
**Requirements:**
- Separate from CIO
- Adequate independence and authority

**Responsibilities:**
- Information security strategy
- Cyber security implementation
- Security incident management
- Security policy enforcement
- Security awareness programs

## Files in This Directory

### 1. RBI_NBFC_IT_Framework_Controls.json
Complete control database in JSON format with detailed requirements.

**Structure:**
```json
{
  "1.1": {
    "section": "1. IT Governance",
    "control_id": "1.1",
    "title": "Board Approved IT Strategy",
    "description": "...",
    "category": "IT Governance",
    "applicability": "NBFCs with asset size ≥ ₹ 500 crore",
    "requirements": [...]
  }
}
```

### 2. RBI_NBFC_IT_Framework_Controls.csv
Tabular export of all controls for easy reference and reporting.

**Columns:**
- Control_ID
- Section
- Title
- Description
- Category
- Applicability
- Requirements

## Implementation Guidance

### Phase 1: Assessment (Months 1-2)
1. Determine your NBFC's asset size category
2. Identify applicable controls
3. Conduct gap analysis against current state
4. Prioritize remediation based on risk

### Phase 2: Governance (Months 2-3)
1. Establish ITSC (if required)
2. Designate CIO and CISO
3. Develop Board-approved IT Strategy
4. Create Information Security Policy
5. Develop Cyber Security Policy

### Phase 3: Security Implementation (Months 3-6)
1. Implement access controls
2. Deploy security tools (firewall, IDS/IPS, anti-malware)
3. Establish patch management process
4. Implement encryption for sensitive data
5. Set up logging and monitoring

### Phase 4: Operations (Months 4-6)
1. Establish change management process
2. Implement backup procedures
3. Set up incident management
4. Develop capacity management (if required)
5. Create operational runbooks

### Phase 5: BCP & DR (Months 5-7)
1. Conduct Business Impact Analysis
2. Develop Business Continuity Plan
3. Establish DR site (if required)
4. Test BCP scenarios
5. Document and train staff

### Phase 6: Audit & Compliance (Ongoing)
1. Conduct annual IS Audit (if required)
2. Address audit findings
3. Report to Board and RBI
4. Continuous monitoring and improvement
5. Update policies and procedures

## Penalties for Non-Compliance

RBI may take regulatory action for non-compliance, including:
- Monetary penalties
- Restrictions on business activities
- Directions for immediate remediation
- Supervisory actions
- In severe cases: License cancellation

## Additional Resources

- **RBI Official Website**: [www.rbi.org.in](https://www.rbi.org.in)
- **RBI Cyber Security Circulars**: Check RBI notifications regularly
- **CERT-In**: [www.cert-in.org.in](https://www.cert-in.org.in) (for cyber incident response)
- **ISO 27001 Standard**: Information security management
- **NIST Cybersecurity Framework**: [www.nist.gov/cyberframework](https://www.nist.gov/cyberframework)

## FAQs

**Q: What is the asset size threshold for full compliance?**  
A: NBFCs with asset size ≥ ₹ 500 crore must comply with all requirements including IT governance structure and annual IS Audit.

**Q: Can smaller NBFCs outsource IT entirely?**  
A: Yes, but they remain accountable and must ensure outsourcing contracts include required controls and audit rights.

**Q: How soon must cyber incidents be reported to RBI?**  
A: Immediately upon detection of significant cyber incidents.

**Q: Can CIO and CISO be the same person?**  
A: No, for NBFCs ≥ ₹ 500 crore, CISO must be separate from CIO to ensure independence.

**Q: Is annual IS Audit mandatory for all NBFCs?**  
A: Only for NBFCs with asset size ≥ ₹ 500 crore. Smaller NBFCs should conduct periodic reviews.

**Q: What happens if we don't have a DR site?**  
A: Large NBFCs must "consider" DR sites - it's not absolute mandate but must be risk-assessed and justified.

**Q: Do we need to inform RBI before outsourcing?**  
A: The framework requires Board approval and proper contracts, but doesn't mandate prior RBI approval. However, RBI must have audit access to service provider.

## Document Status

- **Last Updated**: November 2025
- **Version**: 1.0
- **Source Document Date**: June 8, 2017
- **Status**: Active and Mandatory

---

**Disclaimer**: This is a reference document for the RBI NBFC IT Framework. NBFCs should refer to the official RBI Master Direction and consult with legal/compliance advisors for implementation.

