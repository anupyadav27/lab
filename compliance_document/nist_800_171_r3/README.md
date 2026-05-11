# NIST SP 800-171 Revision 3
## Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations

**Official Publication:** May 2024  
**Source:** https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html  
**Status:** Latest Version (Supersedes Rev 2)  
**DOI:** https://doi.org/10.6028/NIST.SP.800-171r3

---

## Overview

NIST Special Publication 800-171 provides federal agencies with **110 security requirements** for protecting the confidentiality of **Controlled Unclassified Information (CUI)** when the information is resident in nonfederal systems and organizations.

### Key Information

| Aspect | Details |
|--------|---------|
| **Total Requirements** | 110 active requirements (after removing withdrawn) |
| **Control Families** | 17 families (subset of NIST 800-53's 20 families) |
| **Based On** | NIST SP 800-53 Rev 5 Moderate baseline |
| **Purpose** | Protect CUI in nonfederal systems |
| **Mandatory For** | DoD contractors (via DFARS 252.204-7012) |
| **Related To** | CMMC (Cybersecurity Maturity Model Certification) |
| **Replaces** | NIST SP 800-171 Rev 2 (February 2020) |

---

## What is CUI (Controlled Unclassified Information)?

**Definition:** Information that requires safeguarding or dissemination controls pursuant to federal law, regulation, or government-wide policy, but is not classified.

**Examples of CUI:**
- Defense-related technical data
- Export-controlled information
- Critical infrastructure information
- Law enforcement sensitive information
- Privacy information (PII)
- Proprietary business information
- Financial information
- Legal information

**CUI Registry:** https://www.archives.gov/cui/registry/category-list

---

## Audience

### Federal Perspective
- Federal agencies establishing security requirements in contracts
- Contracting officers
- Acquisition professionals
- Program managers managing CUI

### Nonfederal Perspective
- Defense contractors (Defense Industrial Base)
- Federal contractors handling CUI
- Business associates of federal agencies
- System designers and developers
- Security engineers
- System integrators
- Organizations pursuing CMMC certification

---

## 17 Security Requirement Families

| Family Code | Family Name | Requirements (Active) | Key Focus |
|-------------|-------------|----------------------|-----------|
| **AC** | Access Control | 16 (of 22) | User access, least privilege, session management |
| **AT** | Awareness and Training | 2 (of 3) | Security literacy, role-based training |
| **AU** | Audit and Accountability | 8 (of 9) | Event logging, audit records, time stamps |
| **CM** | Configuration Management | 10 (of 12) | Baseline config, change control, least functionality |
| **IA** | Identification and Authentication | 10 (of 12) | MFA, password management, authenticators |
| **IR** | Incident Response | 5 | Incident handling, reporting, testing |
| **MA** | Maintenance | 3 (of 6) | Maintenance tools, remote maintenance |
| **MP** | Media Protection | 8 (of 9) | Media sanitization, marking, transport |
| **PS** | Personnel Security | 2 | Personnel screening, termination |
| **PE** | Physical Protection | 6 (of 8) | Physical access control, monitoring |
| **RA** | Risk Assessment | 3 (of 4) | Risk assessment, vulnerability scanning |
| **CA** | Security Assessment & Monitoring | 4 (of 5) | Security assessment, continuous monitoring |
| **SC** | System and Communications Protection | 10 (of 16) | Boundary protection, encryption, cryptography |
| **SI** | System and Information Integrity | 5 (of 8) | Flaw remediation, malicious code, monitoring |
| **PL** | Planning | 3 | Security policies, system security plan |
| **SA** | System and Services Acquisition | 3 | Security engineering, external services |
| **SR** | Supply Chain Risk Management | 3 | Supply chain risk management (NEW in Rev 3) |

**Total:** 110 active requirements (39 withdrawn from original numbering)

---

## Changes in Revision 3 (May 2024)

### Major Updates

1. **New Family Added:**
   - **SR (Supply Chain Risk Management)** - 3 new requirements
   - 03.17.01: Supply Chain Risk Management Plan
   - 03.17.02: Acquisition Strategies, Tools, and Methods
   - 03.17.03: Supply Chain Requirements and Processes

2. **Requirements Reorganized:**
   - More alignment with NIST 800-53 Rev 5
   - Clearer mapping to parent controls
   - Updated requirement titles and descriptions

3. **Withdrawn Requirements:**
   - 39 requirements marked as "Withdrawn"
   - Functionality moved to other requirements
   - Reduces redundancy

4. **Enhanced Guidance:**
   - More detailed discussion sections
   - Better examples and implementation guidance
   - Improved Organization-Defined Parameters (ODPs)

### Differences from Rev 2

| Aspect | Rev 2 (2020) | Rev 3 (2024) |
|--------|-------------|--------------|
| **Total Requirements** | 110 | 110 (same) |
| **Control Families** | 14 | 17 (added SR, reorganized) |
| **Supply Chain** | Not explicit | Dedicated family (SR) |
| **Alignment** | 800-53 Rev 4 | 800-53 Rev 5 |
| **ODPs** | Limited | Expanded |

---

## Relationship to NIST 800-53

NIST SP 800-171 is a **tailored subset** of NIST SP 800-53 Rev 5:

```
NIST SP 800-53 Rev 5 (1,485 controls)
         ↓ Tailored to
   MODERATE Baseline (~325 controls)
         ↓ Further tailored to
  NIST SP 800-171 Rev 3 (110 requirements)
```

### Tailoring Methodology

Requirements were selected based on:
1. **Focus on CUI confidentiality** (primary objective)
2. **Controls from 800-53 Moderate baseline**
3. **Applicable to nonfederal systems**
4. **Technically implementable by contractors**
5. **Cost-effective for nonfederal organizations**

### Mapping to 800-53

Each 800-171 requirement maps to specific 800-53 controls:

| 800-171 Requirement | Maps to 800-53 Control |
|---------------------|----------------------|
| 03.01.01 (Account Management) | AC-2 |
| 03.05.03 (Multi-Factor Authentication) | IA-2(1), IA-2(2) |
| 03.13.08 (Transmission Confidentiality) | SC-8, SC-28 |
| 03.14.02 (Malicious Code Protection) | SI-3 |

---

## Use Cases & Applications

### 1. **Defense Industrial Base (DIB) Contractors**
- **Mandatory** via DFARS clause 252.204-7012
- Must implement all 110 requirements
- Required for handling CUI in DoD contracts
- Subject to DIBCAC/DCMA assessments

### 2. **CMMC (Cybersecurity Maturity Model Certification)**
- CMMC Level 2 based on 800-171
- 110 practices = 110 NIST 800-171 requirements
- Required for DoD prime and subcontractors
- Third-party assessment organization (C3PAO) certified

### 3. **Federal Civilian Contractors**
- Federal agencies may require 800-171 compliance
- Applies to contracts involving CUI
- May be specified in contract clauses (e.g., FAR 52.204-21)

### 4. **Commercial Organizations**
- Voluntary adoption for enhanced security posture
- "Lighter" alternative to full NIST 800-53
- Industry best practice for protecting sensitive information
- Competitive advantage in federal marketplace

---

## Key Requirements Summary

### High-Impact Requirements (Most Critical)

#### Access Control (AC)
- **03.01.01:** Account Management - Limit access to authorized users
- **03.01.05:** Least Privilege - Operate at lowest necessary privilege
- **03.01.06:** Privileged Accounts - Authorize privileged account access

#### Identification & Authentication (IA)
- **03.05.03:** Multi-Factor Authentication - MFA for local and network access
- **03.05.07:** Password Management - Enforce password complexity

#### Audit & Accountability (AU)
- **03.03.01:** Event Logging - Create and retain audit logs
- **03.03.08:** Protection of Audit Information - Protect audit logs from unauthorized access

#### System & Communications Protection (SC)
- **03.13.01:** Boundary Protection - Monitor and control communications at boundaries
- **03.13.08:** Transmission & Storage Confidentiality - Encrypt CUI in transit and at rest
- **03.13.11:** Cryptographic Protection - Use FIPS-validated cryptography

#### System & Information Integrity (SI)
- **03.14.01:** Flaw Remediation - Identify, report, and correct flaws
- **03.14.02:** Malicious Code Protection - Implement anti-malware mechanisms
- **03.14.06:** System Monitoring - Monitor system to detect attacks

---

## Implementation Guidance

### Step 1: Scope CUI Systems
- Identify systems that process, store, or transmit CUI
- Determine system boundaries
- Document asset inventory

### Step 2: Conduct Gap Assessment
- Assess current security posture against 110 requirements
- Use NIST SP 800-171A for assessment procedures
- Document findings in System Security Plan (SSP)

### Step 3: Develop Plan of Action & Milestones (POA&M)
- Document remediation plans for gaps
- Prioritize by risk
- Set timelines and responsibilities

### Step 4: Implement Controls
- Deploy technical controls (encryption, MFA, logging)
- Establish operational controls (policies, procedures)
- Implement management controls (risk assessment, training)

### Step 5: Document & Maintain
- Maintain System Security Plan (SSP)
- Update POA&M regularly
- Conduct annual assessments

### Step 6: Continuous Monitoring
- Monitor security control effectiveness
- Review audit logs
- Update controls as threats evolve

---

## Compliance Tools & Resources

### Official NIST Resources
1. **NIST SP 800-171 Rev 3** (Main document)
   - https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html

2. **NIST SP 800-171A** (Assessment procedures)
   - Companion document with assessment methodology
   - Procedures to verify requirement implementation

3. **NIST SP 800-172** (Enhanced Security Requirements)
   - Additional requirements for protecting high-value assets
   - Optional but recommended for sensitive CUI

### DoD Resources
4. **DFARS 252.204-7012** (Contract clause)
   - DoD contract clause requiring 800-171 compliance

5. **DIBCAC** (Defense Industrial Base Cybersecurity Assessment Center)
   - Conducts assessments for DIB contractors

6. **CMMC** (Cybersecurity Maturity Model Certification)
   - https://dodcio.defense.gov/CMMC/

---

## Organization-Defined Parameters (ODPs)

Many requirements include **Organization-Defined Parameters** (ODPs) that must be specified by the implementing organization or the federal agency:

**Examples:**
- **03.01.08:** Number of consecutive invalid logon attempts (ODP: typically 3-5)
- **03.01.10:** Time period of inactivity before device lock (ODP: typically 15 minutes)
- **03.03.04:** Personnel to alert in event of audit process failure (ODP: security team)
- **03.11.02:** Time frames for vulnerability remediation (ODP: high=30 days, moderate=90 days)

Federal agencies may specify ODP values in contracts, or contractors must define them.

---

## Files in This Directory

### 1. NIST_SP_800-171_R3_controls.json
Complete JSON database with all 110 requirements organized by family, including:
- Requirement ID
- Title
- Status (active/withdrawn)
- Family mapping

### 2. NIST_SP_800-171_R3_controls.csv
Spreadsheet-friendly format with columns:
- Requirement_ID
- Family_Code
- Family_Name
- Requirement_Title
- Status
- NIST_800-53_Mapping
- Description

### 3. README.md (This File)
Comprehensive documentation including:
- Framework overview
- Use cases
- Implementation guidance
- Change history

---

## Next Steps

To build a full compliance database (like we did for other frameworks):

1. **Extract from Prowler** - Check if Prowler has 800-171 controls
2. **Map to Cloud Providers** - Expand checks to AWS, Azure, GCP, Oracle, IBM, Alicloud
3. **Determine Automation** - Identify which requirements can be automated
4. **Generate Check Database** - Create multi-cloud check implementations
5. **Validate with Azure** - Cross-reference with Azure NIST 800-171 policies (if available)

---

## Comparison with Related Frameworks

| Framework | Controls | Focus | Audience |
|-----------|----------|-------|----------|
| **NIST 800-171** | 110 | CUI Protection | Federal contractors |
| **NIST 800-53** | 1,485 | Comprehensive Security | Federal agencies |
| **CMMC Level 2** | 110 | CUI Protection | DoD contractors |
| **CMMC Level 3** | 110 + 800-172 | Enhanced CUI | High-value DoD |
| **FedRAMP Moderate** | ~325 | Cloud Security | Cloud service providers |

---

## Additional Information

**Authors:**
- Ron Ross (NIST)
- Victoria Pillitteri (NIST)

**Contact:**
- Email: [email protected]
- NIST Computer Security Division
- 100 Bureau Drive, Gaithersburg, MD 20899-8930

**Publication History:**
- **Rev 3:** May 2024 (Current)
- **Rev 2:** February 2020 (Superseded)
- **Rev 1:** December 2016
- **Initial:** June 2015

---

## Keywords

Controlled Unclassified Information, CUI, DFARS, CMMC, Defense Industrial Base, DIB, Executive Order 13556, FIPS 199, FIPS 200, FISMA, nonfederal systems, security assessment, security control, supply chain risk management

---

**Status:** ✅ Documentation Complete  
**Next:** Build multi-cloud compliance database using Prowler + Azure validation  
**Created:** 2025-11-06


