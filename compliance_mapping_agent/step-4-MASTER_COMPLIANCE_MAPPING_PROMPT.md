# MASTER COMPLIANCE MAPPING PROMPT
## Complete 3-Phase Process for Perfect Compliance Mapping

---

## 🎯 MASTER OBJECTIVE

**Purpose**: Execute a perfect compliance mapping process with zero AI hallucination, complete database validation, and perfect cross-reference alignment.

**Process**: 3 sequential phases that must be completed in order:
1. **Phase 1**: Provider Expert Review
2. **Phase 2**: Implementation Classification  
3. **Phase Validation**: Quality Assurance

---

## 📋 MASTER INPUT REQUIREMENTS

### **Required Files**
- **COMPLIANCE JSON**: Path to the compliance framework JSON file
- **CLOUD PROVIDER**: Specify which provider (AWS/GCP/Azure/Kubernetes)
- **ASSERTION DATABASE**: `assertions_pack_final_2025-09-11T18-41-14.json`
- **RULES DATABASE**: `k8s_rules_v2_final.json` (or cloud-specific equivalent)
- **MATRIX DATABASE**: `simplified_combined_assertion_matrix_database.json`

### **Optional Context**
- **COMPLIANCE DOCUMENT MAPPING INDEX**: Table of contents with assessment types

---

## 🔄 MASTER PROCESS FLOW

### **PHASE 1: PROVIDER EXPERT REVIEW**
**Duration**: Complete analysis of all controls
**Objective**: Define HOW to check compliance from technical expert perspective

#### **Phase 1 Tasks**
1. **Expert Analysis**: Analyze each control as a cloud/K8s expert
2. **Audit Approach**: Define step-by-step technical approach
3. **API Feasibility**: Assess automation potential
4. **Recommendations**: Provide technical recommendations
5. **Dangerous Patterns**: Identify what constitutes violations
6. **Validation Strategy**: Define overall compliance validation approach

#### **Phase 1 Output**
```json
[
  {
    "control_id": "1.1.1",
    "control_title": "Control title",
    "provider_expert_recommendation": {
      "expert_analysis": "Technical analysis",
      "audit_approach": ["Step 1", "Step 2"],
      "api_feasibility": "fully_automated|partially_automated|manual_only",
      "recommended_method": "programmatic|manual|hybrid",
      "apis_to_check": ["API endpoints"],
      "kubectl_commands": ["Commands"],
      "dangerous_patterns": {
        "pattern_name": "Violation pattern",
        "detection_method": "Detection approach",
        "validation_logic": "Validation logic"
      },
      "validation_strategy": "Overall strategy"
    }
  }
]
```

---

### **PHASE 2: IMPLEMENTATION CLASSIFICATION**
**Duration**: Implement Phase 1 recommendations
**Objective**: Create executable compliance checks with database mapping

#### **Phase 2 Tasks**
1. **Review Phase 1**: Use Phase 1 output as input
2. **Determine Check Type**: Based on Phase 1 API feasibility
3. **Map to Databases**: Validate all references against actual databases
4. **Create Compliance Checks**: Implement programmatic/manual/hybrid checks
5. **Cross-Reference**: Ensure Phase 1 and Phase 2 alignment
6. **Database Validation**: Verify all values exist in actual databases

#### **Phase 2 Output**
```json
[
  {
    "control_id": "1.1.1",
    "control_title": "Control title",
    "provider_expert_recommendation": {
      // Copy from Phase 1
    },
    "check_type": "programmatic|manual|hybrid",
    "compliance_checks": [
      {
        "check_name": "Check name",
        "check_description": "Check description",
        "check_methods": [
          {
            "programmatic_check": { /* or manual_check */ }
          }
        ]
      }
    ]
  }
]
```

---

### **PHASE VALIDATION: QUALITY ASSURANCE**
**Duration**: Comprehensive validation
**Objective**: Ensure perfect alignment and zero AI hallucination

#### **Validation Tasks**
1. **Cross-Reference Validation**: Phase 1 ↔ Phase 2 alignment
2. **Database Validation**: All references against actual databases
3. **Implementation Consistency**: Check type matches feasibility
4. **Quality Assurance**: No AI hallucination or fake values
5. **Final Report**: Comprehensive validation results

#### **Validation Output**
```json
{
  "validation_summary": {
    "total_controls": 50,
    "validated_controls": 50,
    "cross_reference_issues": 0,
    "database_validation_issues": 0,
    "implementation_consistency_issues": 0,
    "overall_status": "✅ PASS"
  },
  "detailed_validation": [ /* Detailed results */ ]
}
```

---

## 🚀 EXECUTION INSTRUCTIONS

### **Step 1: Execute Phase 1**
```bash
# Use Phase 1 prompt
python execute_phase_1.py \
  --compliance_file "compliance_framework.json" \
  --provider "kubernetes" \
  --output "phase_1_output.json"
```

### **Step 2: Execute Phase 2**
```bash
# Use Phase 2 prompt with Phase 1 output
python execute_phase_2.py \
  --phase_1_output "phase_1_output.json" \
  --assertion_db "assertions_pack_final_2025-09-11T18-41-14.json" \
  --rules_db "k8s_rules_v2_final.json" \
  --matrix_db "simplified_combined_assertion_matrix_database.json" \
  --output "phase_2_output.json"
```

### **Step 3: Execute Validation**
```bash
# Use Validation prompt
python execute_validation.py \
  --phase_1_output "phase_1_output.json" \
  --phase_2_output "phase_2_output.json" \
  --databases "assertion_db, rules_db, matrix_db" \
  --output "validation_report.json"
```

---

## ✅ MASTER QUALITY CHECKLIST

### **Phase 1 Quality**
- [ ] Expert analysis covers all compliance requirements
- [ ] Audit approach is technically feasible
- [ ] API feasibility assessment is accurate
- [ ] Dangerous patterns are clearly defined
- [ ] Validation strategy is comprehensive

### **Phase 2 Quality**
- [ ] All Phase 1 recommendations are implemented
- [ ] Check type matches API feasibility
- [ ] All database references are valid
- [ ] Cross-reference alignment is maintained
- [ ] Implementation is executable

### **Validation Quality**
- [ ] Perfect cross-reference alignment
- [ ] All database references validated
- [ ] Implementation consistency verified
- [ ] Zero AI hallucination confirmed
- [ ] Final output is production-ready

---

## 🎯 SUCCESS CRITERIA

### **Perfect Execution**
- **Phase 1**: Complete expert analysis for all controls
- **Phase 2**: Perfect implementation with database validation
- **Validation**: Zero issues, perfect alignment
- **Final Output**: Production-ready compliance mapping

### **Quality Metrics**
- **100% Database Validation**: All references exist in actual databases
- **100% Cross-Reference Alignment**: Phase 1 and Phase 2 perfectly aligned
- **Zero AI Hallucination**: No fake or generated values
- **Executable Implementation**: All checks are technically feasible

---

## 🚫 MASTER ANTI-PATTERNS

### **Critical Mistakes to Avoid**
- ❌ **Skipping Phases**: Must complete all 3 phases in order
- ❌ **AI Hallucination**: Never generate fake database values
- ❌ **Cross-Reference Misalignment**: Phase 1 and Phase 2 must align
- ❌ **Invalid Database References**: All values must exist in actual databases
- ❌ **Implementation Contradictions**: Check type must match feasibility

### **Auto-Fail Conditions**
- Any phase skipped or incomplete
- AI hallucination detected
- Cross-reference misalignment
- Invalid database references
- Implementation contradictions

---

## 📊 MASTER OUTPUT STRUCTURE

### **Final Deliverable**
```json
{
  "master_output": {
    "metadata": {
      "compliance_framework": "CIS Kubernetes Benchmark V1.8.0",
      "cloud_provider": "kubernetes",
      "total_controls": 50,
      "phase_1_completed": true,
      "phase_2_completed": true,
      "validation_completed": true,
      "overall_status": "✅ PASS"
    },
    "phase_1_results": [ /* Phase 1 output */ ],
    "phase_2_results": [ /* Phase 2 output */ ],
    "validation_results": { /* Validation output */ },
    "final_compliance_mapping": [ /* Final production-ready mapping */ ]
  }
}
```

---

## 🔧 MASTER TOOLS

### **Validation Commands**
```bash
# Check overall status
grep -c "✅ PASS" master_output.json

# Verify no AI hallucination
grep -c "not_available_in_database" master_output.json

# Validate database references
python validate_all_databases.py master_output.json

# Check cross-reference alignment
python validate_cross_reference.py master_output.json
```

---

## 🎯 MASTER SUCCESS METRICS

### **Perfect Execution Indicators**
- **Phase 1**: All controls have comprehensive expert analysis
- **Phase 2**: All controls have executable implementation
- **Validation**: Zero issues found, perfect alignment
- **Final Output**: Production-ready compliance mapping

### **Quality Assurance**
- **Database Consistency**: 100% valid references
- **Cross-Reference Alignment**: Perfect Phase 1 ↔ Phase 2 alignment
- **Implementation Feasibility**: All checks are executable
- **Zero Hallucination**: No fake or generated values

---

**This master prompt ensures perfect compliance mapping with zero AI hallucination and complete database validation across all cloud providers!**
