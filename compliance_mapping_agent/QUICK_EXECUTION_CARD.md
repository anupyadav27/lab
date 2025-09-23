# 🚀 Quick Execution Card
## Compliance Mapping Agent - Sequential Steps

---

## **📋 Execution Order (Follow This Sequence!)**

| Step | File | Purpose | Input | Output |
|------|------|---------|-------|--------|
| **0** | `step-0-README.md` | 📖 Documentation | - | Knowledge |
| **1** | `step-1-PHASE_1_PROMPT.md` | 🔍 Expert Analysis | Compliance JSON + Provider | `phase_1_output.json` |
| **2** | `step-2-PHASE_2_PROMPT.md` | ⚙️ Implementation | Phase 1 + Databases | `phase_2_output.json` |
| **3** | `step-3-PHASE_VALIDATION_PROMPT.md` | ✅ Validation | Phase 1 + Phase 2 + Databases | `validation_report.json` |
| **4** | `step-4-MASTER_COMPLIANCE_MAPPING_PROMPT.md` | 🚀 Complete Process | All Files | Final Mapping |
| **5** | `step-5-execute_compliance_mapping.py` | 🤖 Automation | CLI Args | All Outputs |

---

## **🎯 Quick Start Options**

### **Option A: Master Prompt (Recommended)**
```bash
# Use step-4-MASTER_COMPLIANCE_MAPPING_PROMPT.md
# Complete process in one go
```

### **Option B: Sequential Steps**
```bash
# Step 1: Expert Analysis
# Use: step-1-PHASE_1_PROMPT.md

# Step 2: Implementation  
# Use: step-2-PHASE_2_PROMPT.md

# Step 3: Validation
# Use: step-3-PHASE_VALIDATION_PROMPT.md
```

### **Option C: Automated Script**
```bash
python step-5-execute_compliance_mapping.py \
  --compliance_file "compliance.json" \
  --provider "kubernetes" \
  --assertion_db "assertions.json" \
  --rules_db "rules.json" \
  --matrix_db "matrix.json"
```

---

## **🗄️ Required Databases**

- **Assertion DB**: `assertions_pack_final_2025-09-11T18-41-14.json`
- **Rules DB**: `k8s_rules_v2_final.json` (or cloud-specific)
- **Matrix DB**: `simplified_combined_assertion_matrix_database.json`

---

## **✅ Success Criteria**

- **100% Database Validation**: All references exist in actual databases
- **100% Cross-Reference Alignment**: Phase 1 and Phase 2 perfectly aligned
- **Zero AI Hallucination**: No fake or generated values
- **Executable Implementation**: All checks are technically feasible

---

## **🚫 Critical Rules**

- ❌ **Never skip phases** - Must complete in order
- ❌ **No AI hallucination** - Use `not_available_in_database` for missing values
- ❌ **No cross-reference misalignment** - Phase 1 and Phase 2 must align
- ❌ **No invalid database references** - All values must exist in actual databases

---

**Ready to execute perfect compliance mapping!** 🎯
