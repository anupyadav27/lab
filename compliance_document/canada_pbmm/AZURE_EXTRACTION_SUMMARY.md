# Canada PBMM - Azure Policy Extraction

## Summary

✅ **YES! The Azure link provides actual controls with IDs!**

**Azure Link:** https://learn.microsoft.com/en-us/azure/governance/policy/samples/canada-federal-pbmm

## What We Found

### From Original Canadian Government Link
❌ **Framework structure only** - No actual control list
- Control families (18 families: AC, AT, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PM, PS, RA, SA, SC, SI)
- Responsibility matrices (CSP vs Consumer)
- Cloud service model layers (IaaS/PaaS/SaaS)
- **NOTE:** Appendix A (control list) was replaced by CCCS Medium Cloud Control Profile (ITSP.50.103)

### From Azure Documentation
✅ **Actual controls with IDs!**
- Control IDs in format: `CCCS {FAMILY}-{NUMBER}` or `CCCS {FAMILY}-{NUMBER}({ENHANCEMENT})`
- Azure Policy mappings for each control
- Control descriptions and requirements

## Extracted Controls (27 Total)

### Control Families Represented:
1. **Access Control (AC)** - 4 controls
2. **Audit and Accountability (AU)** - 5 controls
3. **Configuration Management (CM)** - 1 control
4. **Identification and Authentication (IA)** - 5 controls
5. **System and Communications Protection (SC)** - 8 controls
6. **System and Information Integrity (SI)** - 4 controls

### Sample Controls:
```
CCCS AC-2      - Account Management
CCCS AC-2(7)   - Account Management | Role-Based Schemes
CCCS AC-4      - Information Flow Enforcement
CCCS SC-8(1)   - Transmission Confidentiality and Integrity | Cryptographic Protection
CCCS SC-28     - Protection of Information at Rest
CCCS SI-2      - Flaw Remediation
CCCS SI-4      - Information System Monitoring
```

## Control ID Format

Canada PBMM uses **CCCS** prefix + **NIST 800-53 control numbering**:
- `CCCS AC-2` = NIST AC-2 (Account Management)
- `CCCS AC-2(7)` = NIST AC-2(7) (Role-Based Schemes enhancement)
- `CCCS SC-28` = NIST SC-28 (Protection of Information at Rest)

**This confirms:** Canada PBMM is directly based on NIST 800-53 controls!

## Azure Policy Mappings

Azure provides specific policy definitions for each control:

### Example: CCCS AC-2 (Account Management)
- 5 Azure Policy definitions
- Policies cover:
  - Removing blocked accounts with owner permissions
  - Removing blocked accounts with read/write permissions
  - Removing guest accounts with various permission levels

### Example: CCCS SC-8(1) (Transmission Protection)
- 8 Azure Policy definitions
- Policies cover:
  - HTTPS enforcement for App Services
  - HTTPS enforcement for Function Apps
  - SSL enforcement for Azure Cache for Redis
  - Secure transfer to storage accounts
  - TLS configuration for Windows machines

## Key Insight

Since Canada PBMM controls use the **exact same numbering as NIST 800-53**, we can:

1. ✅ Use our existing **NIST 800-53 Rev 5 database** (1,485 controls, 9,842 checks)
2. ✅ Filter to the controls that Canada PBMM actually uses
3. ✅ Add CCCS prefix and PBMM-specific metadata
4. ✅ Validate automation decisions using Azure's policy mappings

## Limitations

The Azure documentation shows only a **subset** of controls:
- **Visible:** 27 controls across 6 families
- **Expected:** PBMM likely has 300-400 controls (similar to FedRAMP Moderate)
- **Reason:** Azure page only shows controls with Azure Policy mappings

To get the **complete control list**, we need:
1. CCCS Medium Cloud Control Profile (ITSP.50.103 Annex B) - official document
2. OR - Map from FedRAMP Moderate baseline (since explicitly aligned)
3. OR - Extract more from Azure (if they have additional pages)

## Recommended Approach

### Option 1: Use FedRAMP Moderate as Foundation ⭐RECOMMENDED
Since Canada PBMM explicitly aligns with FedRAMP Moderate:
1. Take our **FedRAMP High** database (410 controls)
2. Filter to **FedRAMP Moderate** baseline (~325 controls)
3. Rename control IDs: `AC-2` → `CCCS AC-2`
4. Add PBMM-specific metadata
5. Validate with Azure policies where available

**Advantages:**
- Fast (reuse existing database)
- Accurate (official alignment)
- Comprehensive (full control set)

### Option 2: Start with Azure + Expand from NIST
1. Use the 27 controls from Azure as seed
2. Map back to our NIST database
3. Identify related controls
4. Expand to full PBMM profile using NIST Moderate baseline

**Advantages:**
- Azure-validated automation decisions
- Direct policy mappings available

### Option 3: Request CCCS Document
1. Contact CCCS Public Enquiries
2. Obtain ITSP.50.103 document
3. Extract Annex B (Medium Cloud Control Profile)
4. Map to our existing checks

**Advantages:**
- Official and authoritative
- Most accurate

## Next Steps

**Immediate:** Extract more controls from Azure (check if there are more sections)
**Then:** Proceed with Option 1 (FedRAMP Moderate mapping) or Option 2 (Azure + NIST expansion)

## Files Created

1. ✅ `CANADA_PBMM_FRAMEWORK_INFO.csv` - Framework metadata
2. ✅ `CANADA_PBMM_CONTROL_FAMILIES.csv` - 18 control families
3. ✅ `CANADA_PBMM_CLOUD_LAYERS.csv` - Responsibility matrices
4. ✅ `CANADA_PBMM_CONTROLS_FROM_AZURE.csv` - 27 extracted controls
5. ✅ `README.md` - Framework documentation
6. ✅ `AZURE_EXTRACTION_SUMMARY.md` - This file

---

**Status:** ✅ Controls extracted from Azure  
**Count:** 27 controls (subset)  
**Source:** https://learn.microsoft.com/en-us/azure/governance/policy/samples/canada-federal-pbmm  
**Next:** Expand to full control set using FedRAMP/NIST mapping

