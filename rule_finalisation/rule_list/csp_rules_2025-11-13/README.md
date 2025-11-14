# CSP Rule Lists - Complete Package
**Generated**: November 13, 2025  
**Source**: `consolidated_compliance_rules_FINAL.csv` (uniform format columns only)

---

## 📁 Directory Structure

```
csp_rules_2025-11-13/
├── aws/                    (7 files)
├── azure/                  (7 files)
├── gcp/                    (7 files)
├── oracle/                 (7 files)
├── ibm/                    (7 files)
├── alicloud/               (7 files)
├── k8s/                    (7 files) ← NEW!
├── ALL_CSP_SUMMARY_2025-11-13.md
├── MAPPING_SUMMARY_2025-11-13.md
└── README.md
```

**Total**: 7 CSPs × 7 files + 2 summaries + 1 README = **52 files**

---

## 📊 CSP Statistics

| CSP | Functions | Services | Compliance IDs | Avg Compliance/Function |
|-----|-----------|----------|----------------|------------------------|
| AWS | 716 | 128 | 960 | 6.1 |
| Azure | 888 | 102 | 1,093 | 4.7 |
| GCP | 654 | 73 | 913 | 5.7 |
| Oracle | 1,175 | 136 | 874 | 4.4 |
| IBM | 959 | 134 | 934 | 5.5 |
| Alicloud | 904 | 134 | 905 | 5.8 |
| **K8s** | **526** | **39** | **747** | **4.5** |
| **TOTAL** | **5,822** | **746** | **~6,400** | **~5.2** |

---

## 📄 Files Per CSP (7 each)

### 1. Service-Based Files (4)

**`<csp>_rules_simple_<date>.json`**
- Service → List of functions
- Quick reference lookup

**`<csp>_rules_by_service_<date>.json`**
- Detailed metadata structure
- Complete service information

**`<csp>_rules_unique_<date>.json`**
- Flat sorted list
- All unique functions

**`<csp>_services_summary_<date>.json`**
- Service statistics
- Function counts

### 2. Compliance Mapping Files (3) ← NEW!

**`<csp>_function_to_compliance_mapping_<date>.json`**
- **Format**: Function → List of Compliance IDs
- **Purpose**: Find all compliance requirements using a function
- **Example**:
```json
{
  "k8s.rbac.least_privilege_enforcement": [
    "canada_pbmm_moderate_multi_cloud_CCCS_AC-5_0005",
    "hipaa_multi_cloud_164_308_a_1_ii_b_0002",
    "nist_800_171_r2_multi_cloud_3_1_5_...",
    ... (114 compliance IDs total)
  ]
}
```

**`<csp>_compliance_to_function_mapping_<date>.json`**
- **Format**: Compliance ID → List of Functions
- **Purpose**: Find all functions needed for a compliance requirement
- **Example**:
```json
{
  "hipaa_multi_cloud_164_308_a_3_i_0004": [
    "k8s.rbac.no_cluster_admin_binding",
    "k8s.rbac.least_privilege_enforcement",
    "k8s.rbac.service_account_token_automount_disabled",
    "k8s.rbac.role_binding_review"
  ]
}
```

**`<csp>_function_compliance_detailed_<date>.json`**
- **Format**: Function → Detailed compliance metadata
- **Purpose**: Get complete context for each function
- **Example**:
```json
{
  "k8s.rbac.least_privilege_enforcement": {
    "function": "k8s.rbac.least_privilege_enforcement",
    "total_compliance_mappings": 114,
    "compliance_items": [
      {
        "compliance_id": "hipaa_multi_cloud_164_308_a_1_ii_b_0002",
        "framework": "HIPAA",
        "requirement_id": "164_308_a_1_ii_b",
        "requirement_name": "Risk Management",
        "automation_type": "automated",
        "technology": "MULTI_CLOUD"
      },
      ...
    ]
  }
}
```

---

## 🎯 Usage Examples

### Find Compliance IDs for a Function

```python
import json

# Load mapping
with open('k8s/k8s_function_to_compliance_mapping_2025-11-13.json') as f:
    mapping = json.load(f)

# Find which compliances use this function
func = 'k8s.rbac.least_privilege_enforcement'
compliance_ids = mapping[func]
print(f"{func} is used in {len(compliance_ids)} compliance requirements")
```

### Find Functions for a Compliance Requirement

```python
# Load reverse mapping
with open('k8s/k8s_compliance_to_function_mapping_2025-11-13.json') as f:
    mapping = json.load(f)

# Get all K8s functions for HIPAA requirement
compliance_id = 'hipaa_multi_cloud_164_308_a_3_i_0004'
functions = mapping[compliance_id]
print(f"HIPAA 164.308(a)(3)(i) requires {len(functions)} K8s functions:")
for func in functions:
    print(f"  - {func}")
```

### Get Detailed Context

```python
# Load detailed mapping
with open('k8s/k8s_function_compliance_detailed_2025-11-13.json') as f:
    mapping = json.load(f)

# Get all compliance context for a function
func = 'k8s.rbac.least_privilege_enforcement'
details = mapping[func]
print(f"Function: {details['function']}")
print(f"Used in {details['total_compliance_mappings']} compliance requirements:")
for item in details['compliance_items'][:5]:
    print(f"  - {item['framework']}: {item['requirement_name']}")
```

---

## 📈 Top K8s Functions by Compliance Usage

Based on the mappings, here are the most widely used K8s functions:

1. **k8s.rbac.least_privilege_enforcement** - Used in 114 compliance requirements
2. **k8s.audit.logging_enabled** - Used in ~100 compliance requirements
3. **k8s.networkpolicy.default_deny_ingress** - Used in ~90 compliance requirements
4. **k8s.secret.encryption_at_rest_enabled** - Used in ~85 compliance requirements
5. **k8s.apiserver.audit_logging_enabled** - Used in ~80 compliance requirements

---

## 🔍 Data Source

**All rule IDs extracted from uniform format columns:**
- `aws_uniform_format` → `aws.service.resource.check`
- `azure_uniform_format` → `azure.service.resource.check`
- `gcp_uniform_format` → `gcp.service.resource.check`
- `oracle_uniform_format` → `oracle.service.resource.check`
- `ibm_uniform_format` → `ibm.service.resource.check`
- `alicloud_uniform_format` → `alicloud.service.resource.check`
- `k8s_uniform_format` → `k8s.service.resource.check`

**NOT from raw check columns** (e.g., `aws_checks` with underscores)

---

## 📦 Complete File List Per CSP

Each CSP has **7 files**:

### Service-Based (4 files)
1. `simple` - Quick lookup
2. `by_service` - Detailed structure
3. `unique` - Flat list
4. `services_summary` - Statistics

### Compliance Mapping (3 files)
5. `function_to_compliance_mapping` - Function → Compliance IDs
6. `compliance_to_function_mapping` - Compliance ID → Functions
7. `function_compliance_detailed` - Function → Full compliance context

---

## 🎁 Benefits

### Traceability
- Know which compliance requirements use each function
- Track function usage across frameworks

### Impact Analysis
- Understand impact of changing a function
- See which compliances would be affected

### Coverage Analysis
- Identify most critical functions (used in many compliances)
- Prioritize implementation by compliance coverage

### Development Planning
- Know which functions to implement first
- Understand compliance dependencies

### Reporting
- Generate compliance coverage reports
- Show which requirements are met by which functions

---

## 📊 Statistics Summary

### Total Across All CSPs
- **Unique Functions**: 5,822
- **Services**: 746
- **Compliance IDs**: ~6,400
- **Function→Compliance Mappings**: ~30,000+

### K8s Specifically
- **Functions**: 526
- **Services**: 39
- **Compliance IDs**: 747
- **Mappings**: 2,380
- **Coverage**: K8s functions map to 747 different compliance requirements across 13 frameworks

---

## 🏆 Completion Status

✅ All 7 CSPs processed  
✅ All rule lists generated (service-based)  
✅ All compliance mappings created  
✅ All files organized by CSP  
✅ Summary reports generated  
✅ Complete documentation  

**TOTAL FILES**: 52 (7 CSPs × 7 files + 2 summaries + 1 README)

---

**Generated from consolidated compliance database with complete K8s integration!**  
**All functions extracted from uniform format columns for consistency.**
