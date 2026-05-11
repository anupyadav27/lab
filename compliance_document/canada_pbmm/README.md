# Canada PBMM (Protected B, Medium Integrity, Medium Availability)

## Framework Overview

**Official Name:** Government of Canada Security Control Profile for Cloud-based GC Services  
**Security Category:** Protected B, Medium Integrity, Medium Availability (PBMM)  
**Status:** Appendix A replaced by CCCS Medium Cloud Control Profile (ITSP.50.103)  
**Official URL:** https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/cloud-services/government-canada-security-control-profile-cloud-based-it-services.html

## Key Information

### Foundation
The Canada PBMM profile is heavily based on:
- **NIST SP 800-53** (US Federal IT Security Controls)
- **FedRAMP Moderate** (US Federal Cloud Authorization)
- **ITSG-33** (Canadian IT Security Risk Management)

### Alignment
The GC explicitly aligned with **FedRAMP Moderate** to:
- Maximize interoperability of cloud services
- Enable reusability of authorization evidence from CSPs
- Leverage existing US Federal cloud security standards

### Current Status
⚠️ **IMPORTANT:** The original Appendix A (control list) from the 2018 version has been **replaced** by:
- **CCCS Medium Cloud Control Profile**
- Documented in **ITSP.50.103** - "Guidance on the Security Categorization of Cloud-based Services"
- Available from: Canadian Centre for Cyber Security (CCCS)

## Control Families (18 Total)

| Code | Name | CSP | Consumer | Notes |
|------|------|-----|----------|-------|
| **AC** | Access Control | ✓ | ✓ | Shared responsibility |
| **AT** | Awareness and Training | ✓ | ✓ | Shared responsibility |
| **AU** | Audit & Accountability | ✓ | ✓ | Shared responsibility |
| **CA** | Security Assessment | ✓ | ✓ | Shared responsibility |
| **CM** | Configuration Management | ✓ | ✓ | Shared responsibility |
| **CP** | Contingency Planning | ✓ | ✓ | Shared responsibility |
| **IA** | Identification & Authentication | ✓ | ✓ | Shared responsibility |
| **IR** | Incident Response | ✓ | ✓ | Shared responsibility |
| **MA** | Maintenance | ✓ | ✓ | Shared responsibility |
| **MP** | Media Protection | ✓ | ✗ | CSP only |
| **PE** | Physical & Environmental | ✓ | ✗ | CSP only |
| **PL** | Planning | ✓ | ✓ | Shared responsibility |
| **PM** | Program Management | ✓ | ✗ | CSP only |
| **PS** | Personnel Security | ✓ | ✓ | Shared responsibility |
| **RA** | Risk Assessment | ✓ | ✓ | Shared responsibility |
| **SA** | System Acquisition | ✓ | ✓ | Shared responsibility |
| **SC** | System & Comm Protection | ✓ | ✓ | Shared responsibility |
| **SI** | System & Info Integrity | ✓ | ✓ | Shared responsibility |

## Cloud Service Models

### IaaS (Infrastructure as a Service)
- **Consumer:** Manages VMs, OS, applications, data
- **CSP:** Manages virtualization, hardware, facility
- **Shared Controls:** AC, AU, CM, CP, IA, MA, SC, SI

### PaaS (Platform as a Service)
- **Consumer:** Manages applications, partial platform config
- **CSP:** Manages platform, infrastructure, hardware, facility
- **Shared Controls:** AC, AU, CM, CP, IA, MA, SC, SI

### SaaS (Software as a Service)
- **Consumer:** Manages application configuration, users
- **CSP:** Manages applications, platform, infrastructure, hardware, facility
- **Shared Controls:** AC, AU, IA, SC, SI (fewer than IaaS/PaaS)

## Extracted Files

### 1. CANADA_PBMM_FRAMEWORK_INFO.csv
Basic framework metadata and references.

### 2. CANADA_PBMM_CONTROL_FAMILIES.csv
All 18 control families with responsibility allocation by service model.

### 3. CANADA_PBMM_CLOUD_LAYERS.csv
Detailed responsibility matrix by cloud layer and service model.

## Relationship to Other Frameworks

### Strong Alignment
- **FedRAMP Moderate:** Primary alignment target (we already have this!)
- **NIST 800-53 Rev 5:** Foundation controls (we already have this!)
- **ITSG-33:** Canadian adaptation of NIST 800-53

### Key Insight
Since Canada PBMM is explicitly aligned with **FedRAMP Moderate**, and we already have:
- ✅ NIST SP 800-53 Rev 5 (1,485 controls, 9,842 checks)
- ✅ FedRAMP High (410 controls, 3,906 checks)

We can leverage our existing FedRAMP/NIST checks as the foundation for PBMM!

## Next Steps

### Option 1: Use FedRAMP Moderate as Baseline (RECOMMENDED)
Since PBMM explicitly aligns with FedRAMP Moderate:
1. Start with our FedRAMP High controls
2. Filter to Moderate baseline
3. Add any PBMM-specific requirements
4. Map to CCCS control naming

### Option 2: Get CCCS Medium Cloud Control Profile
1. Obtain ITSP.50.103 document from CCCS
2. Extract the Medium Cloud Control Profile (Annex B)
3. Map to our existing NIST/FedRAMP checks
4. Generate PBMM-specific database

### Option 3: Check Prowler Database
1. See if Prowler has PBMM/CCCS controls
2. Extract and expand if available
3. Fall back to FedRAMP mapping if not

## Scope and Applicability

### Applicable To
- Cloud-based GC services and information
- Security category: **Protected B, Medium Integrity, Medium Availability**
- Non-national interest programs/services
- Sensitive government operations (excluding international affairs, defence, federal-provincial affairs)

### Not Applicable To
- National security systems (use higher classification)
- Systems with availability requirements > medium
- Systems handling information > Protected B

## References

1. **Original Document:** https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/cloud-services/government-canada-security-control-profile-cloud-based-it-services.html
2. **FedRAMP:** https://www.fedramp.gov/
3. **NIST SP 800-53:** https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
4. **CCCS ITSP.50.103:** Contact CCCS Public Enquiries

## Notes

- CSPs with Appendix A (v1.1, March 2018) authorizations must contact CCCS for transition requirements
- CCCS provides comparison between old Appendix A and new Medium Cloud Control Profile
- Multi-tenant separation is implicitly expected but not explicitly prescribed in most controls (except AC-4, SC-39, SC-7)

---

**Status:** Framework structure extracted ✅  
**Next:** Check Prowler → Map from FedRAMP → Generate PBMM database  
**Created:** 2025-11-06

