# PHASE 2: IMPLEMENTATION CLASSIFICATION PROMPT
## Determine HOW to Implement Phase 1 Requirements

---

## 🎯 PHASE 2 OBJECTIVE

**Purpose**: Take Phase 1 expert analysis and determine the actual implementation approach, mapping to real databases and APIs.

**What You're Doing**:
- Taking Phase 1 recommendations and implementing them
- Classifying as programmatic/manual/hybrid based on actual feasibility
- Mapping to real databases and APIs
- Creating executable compliance checks
- Ensuring cross-reference alignment with Phase 1

**What You're NOT Doing**:
- Not redoing the expert analysis (use Phase 1 output)
- Not changing the technical approach (implement Phase 1 recommendations)

---

## 📋 INPUT REQUIREMENTS

### **Required Files**
- **PHASE 1 OUTPUT**: The expert analysis from Phase 1
- **ASSERTION DATABASE**: `assertions_pack_final_2025-09-11T18-41-14.json`
- **RULES DATABASE**: `k8s_rules_v2_final.json` (or cloud-specific equivalent)
- **MATRIX DATABASE**: `simplified_combined_assertion_matrix_database.json`
- **CLOUD PROVIDER**: Same as Phase 1

---

## 🔄 PHASE 2 TASK INSTRUCTIONS

For **EACH CONTROL** from Phase 1 output:

### **1. Review Phase 1 Analysis**
- Read the `provider_expert_recommendation` from Phase 1
- Understand the technical requirements and approach
- Note the API feasibility assessment

### **2. Determine Check Type**
Based on Phase 1 `api_feasibility`:
```json
{
  "check_type": "programmatic|manual|hybrid"
}
```

### **3. Map to Databases**
For each field, check against actual databases:

#### **Database Validation Process**
1. **Service Name**: Look in `simplified_combined_assertion_matrix_database.json`
   - If found: Use exact value from database
   - If not found: Use `not_available_in_database`

2. **Resource Type**: Look in `k8s_rules_v2_final.json` (or cloud-specific database)
   - If found: Use exact value from database
   - If not found: Use `not_available_in_database`

3. **Assertion ID**: Look in `assertions_pack_final_2025-09-11T18-41-14.json`
   - If found: Use exact value from database
   - If not found: Use `not_available_in_database`

4. **Rule ID**: Look in `k8s_rules_v2_final.json` (or cloud-specific database)
   - If found: Use exact value from database
   - If not found: Use `not_available_in_database`

#### **Critical Rule: ZERO TOLERANCE for Fake Values**
- **NEVER** generate or create values that don't exist in databases
- **ALWAYS** use `not_available_in_database` if value is not found
- **VALIDATE** every value against actual database entries
- **REPORT** any missing values clearly

### **4. Field Path Mapping & Condition Generation**
Before creating compliance checks, determine the specific field paths and validation conditions:

#### **Field Path Mapping Rules**
Based on control content, map to specific Kubernetes resource fields:

| Control Type | Field Path | Endpoint | Purpose |
|--------------|------------|----------|---------|
| **Admission Controllers** | `spec.containers[0].args[]` | `/api/v1/pods` | Check API server admission controller args |
| **RBAC Roles/Bindings** | `subjects[]` | `/apis/rbac.authorization.k8s.io/v1/clusterrolebindings` | Check role binding subjects |
| **Pod Security Context** | `spec.containers[].securityContext.privileged` | `/api/v1/pods` | Check container security settings |
| **Network Policies** | `spec.egress[]` | `/apis/networking.k8s.io/v1/networkpolicies` | Check network policy rules |
| **Service Accounts** | `spec.serviceAccountName` | `/api/v1/pods` | Check service account assignments |
| **Resource Limits** | `spec.containers[].resources.limits` | `/api/v1/pods` | Check resource constraints |
| **Authentication** | `spec.containers[0].args[]` | `/api/v1/pods` | Check auth configuration |
| **File Permissions** | `manual_check_required` | `manual_inspection` | Manual file system check |

#### **Condition Generation Rules**
For each field path, create specific validation conditions:

```json
{
  "field": "spec.containers[0].args[]",
  "operator": "contains",
  "value": "DenyServiceExternalIPs",
  "description": "Validates that DenyServiceExternalIPs admission controller is enabled in API server configuration to prevent external IP assignments to services"
}
```

**Operator Types:**
- `contains`: Field contains specific value (for arrays/strings)
- `equals`: Field exactly matches value
- `not_contains`: Field does not contain value
- `exists`: Field exists (boolean check)
- `less_than`: Numeric comparison
- `greater_than`: Numeric comparison

**Value Examples:**
- `"DenyServiceExternalIPs"` - Specific admission controller name
- `"false"` - Boolean value for security settings
- `"system:anonymous"` - Specific user/group name
- `"cluster-admin"` - Specific role name
- `"600"` - File permission value

#### **Common Field Mapping Patterns**

**Admission Controllers:**
```json
{
  "field": "spec.containers[0].args[]",
  "operator": "contains",
  "value": "DenyServiceExternalIPs",
  "description": "Validates admission controller is enabled"
}
```

**RBAC Role Bindings:**
```json
{
  "field": "subjects[].name",
  "operator": "not_contains", 
  "value": "system:anonymous",
  "description": "Prevents anonymous access to privileged roles"
}
```

**Pod Security Context:**
```json
{
  "field": "spec.containers[].securityContext.privileged",
  "operator": "equals",
  "value": "false",
  "description": "Ensures containers run without privileged access"
}
```

**Resource Limits:**
```json
{
  "field": "spec.containers[].resources.limits.cpu",
  "operator": "exists",
  "value": "true",
  "description": "Validates CPU limits are set for all containers"
}
```

**Network Policies:**
```json
{
  "field": "spec.egress[].to[].namespaceSelector",
  "operator": "exists",
  "value": "true", 
  "description": "Ensures network policies have proper egress rules"
}
```

### **5. Create Compliance Checks Structure**
Based on `check_type`, create the appropriate structure:

#### **Programmatic Check Structure**
```json
{
  "check_type": "programmatic",
  "compliance_checks": [
    {
      "check_name": "Automated API Check",
      "check_description": "Programmatic validation via APIs",
      "check_methods": [
        {
          "programmatic_check": {
            "automation_level": "PROGRAMMATIC",
            "method": "Real kubectl command or API call from Phase 1",
            "description": "What this check validates",
            "expected_result": "Expected outcome",
            "api_details": {
              "provider": "k8s|aws|gcp|azure",
              "service_name": "From matrix database or not_available_in_database",
              "resource_type": "From rules database or not_available_in_database",
              "resource_field_path": "Specific Kubernetes field path (e.g., spec.containers[0].args[], subjects[], spec.securityContext.privileged)",
              "endpoint": "Real API endpoint from Phase 1",
              "assertion_id": "From assertion database or not_available_in_database",
              "rule_id": "From rules database or not_available_in_database",
              "conditions_map": [
                {
                  "field": "Specific field path that contains the configuration being validated",
                  "operator": "contains|equals|not_contains|exists|less_than|greater_than",
                  "value": "Exact expected value or pattern to validate",
                  "description": "Detailed explanation of what this condition validates and why it's important for compliance"
                }
              ]
            }
          }
        }
      ]
    }
  ]
}
```

#### **Manual Check Structure**
```json
{
  "check_type": "manual",
  "compliance_checks": [
    {
      "check_name": "Manual Review",
      "check_description": "Manual validation process",
      "check_methods": [
        {
          "manual_check": {
            "automation_level": "MANUAL",
            "method": "Manual procedure from Phase 1 audit_approach",
            "description": "What needs manual verification",
            "expected_result": "Expected outcome",
            "manual_review": {
              "required": true,
              "who": "Team assignment (e.g., Platform Security | Cluster Admin)",
              "why": "Why automation is not possible (from Phase 1 api_feasibility)",
              "procedure": ["Step-by-step from Phase 1 audit_approach"],
              "acceptance_criteria": "Clear success criteria",
              "artifacts_to_attach": ["Required documentation"],
              "timebox_minutes": "Realistic time estimates"
            }
          }
        }
      ]
    }
  ]
}
```

#### **Hybrid Check Structure**
```json
{
  "check_type": "hybrid",
  "compliance_checks": [
    {
      "check_name": "Programmatic Component",
      "check_description": "Automated part of validation",
      "check_methods": [
        {
          "programmatic_check": { /* Programmatic structure */ }
        }
      ]
    },
    {
      "check_name": "Manual Component",
      "check_description": "Manual part of validation",
      "check_methods": [
        {
          "manual_check": { /* Manual structure */ }
        }
      ]
    }
  ]
}
```

---

## 🔗 CROSS-REFERENCE VALIDATION

### **Phase 1 ↔ Phase 2 Alignment**
Ensure these alignments:

1. **API Details** implement **Expert Analysis** recommendations
2. **Conditions Map** validate **Dangerous Patterns** from Phase 1
3. **Validation Strategy** drives **Check Methods** structure
4. **Kubectl Commands** match **API Details** endpoints
5. **Audit Approach** becomes **Manual Procedures**

### **Database Consistency**
- **Service Name**: Must exist in matrix database or `not_available_in_database`
- **Resource Type**: Must exist in rules database or `not_available_in_database`
- **Assertion ID**: Must exist in assertion database or `not_available_in_database`
- **Rule ID**: Must exist in rules database or `not_available_in_database`

### **Database Feedback Validation**
For each control, validate database references and provide feedback:

```json
{
 
    "resource_type": {
      "value": "k8s.rbac.role",
      "status": "✅ FOUND in rules database",
      "database_source": "k8s_rules_v2_final.json"
    }
  
}
```

#### **Missing Value Example**
```json
{
  "database_validation_feedback": {
    "service_name": {
      "value": "not_available_in_database",
      "status": "❌ NOT FOUND in matrix database",
      "database_source": "k8s_rules_v2_final.json",
      "reason": "No matching service found for this control type"
    }
  }
}
```

---

## 📝 OUTPUT FORMAT

### **Complete Phase 2 Output Schema**
```json
[
  {
    "control_id": "1.1.1",
    "control_title": "Ensure that the API server pod specification file permissions are set to 600 or more restrictive",
    "provider_expert_recommendation": {
      // Copy from Phase 1 output
    },
    "check_type": "manual",
    "compliance_checks": [
      {
        "check_name": "File Permission Validation",
        "check_description": "Manual validation of file system permissions on master nodes",
        "check_methods": [
          {
            "manual_check": {
              "automation_level": "MANUAL",
              "method": "SSH to master nodes and check file permissions",
              "description": "Validate API server configuration file permissions",
              "expected_result": "All files have 600 or more restrictive permissions",
              "manual_review": {
                "required": true,
                "who": "Platform Security | Cluster Admin",
                "why": "File system permissions cannot be checked via Kubernetes APIs",
                "procedure": [
                  "SSH to each master node",
                  "Check file permissions: ls -la /etc/kubernetes/manifests/kube-apiserver.yaml",
                  "Verify permissions are 600 (rw-------) or more restrictive",
                  "Check ownership is root:root",
                  "Repeat for all master nodes"
                ],
                "acceptance_criteria": "All master node API server files have correct permissions and ownership",
                "artifacts_to_attach": ["file_permission_screenshots", "master_node_inventory"],
                "timebox_minutes": 30
              }
            }
          }
        ]
      }
    ]
  }
]
```

---

## ✅ PHASE 2 QUALITY CHECKLIST

### **Before Completing Phase 2**
- [ ] All Phase 1 expert analysis is preserved and referenced
- [ ] Check type matches Phase 1 API feasibility assessment
- [ ] All database references are validated against actual databases
- [ ] Programmatic methods use real APIs from Phase 1
- [ ] Manual methods cannot be automated (as per Phase 1)
- [ ] Hybrid methods have both programmatic and manual components
- [ ] Cross-reference alignment is maintained
- [ ] No contradictions between Phase 1 and Phase 2

### **Database Validation**
- [ ] Service names exist in matrix database or marked `not_available_in_database`
- [ ] Resource types exist in rules database or marked `not_available_in_database`
- [ ] Assertion IDs exist in assertion database or marked `not_available_in_database`
- [ ] Rule IDs exist in rules database or marked `not_available_in_database`
- [ ] Database validation feedback provided for all fields
- [ ] Missing values clearly explained with reasons
- [ ] No fake or generated values (only database values or `not_available_in_database`)

### **Field Path & Condition Validation**
- [ ] Field paths are specific to Kubernetes resource structure (e.g., `spec.containers[0].args[]`, not generic `data`)
- [ ] Field paths match the actual configuration being validated
- [ ] Endpoints correspond to the correct Kubernetes API resource
- [ ] Conditions use appropriate operators for the field type
- [ ] Values are specific and meaningful (e.g., `"DenyServiceExternalIPs"`, not generic `"true"`)
- [ ] Descriptions explain what the condition validates and why it's important
- [ ] No generic or placeholder field paths (avoid `"data"`, `"metadata"` unless specifically needed)

### **Cross-Reference Validation**
- [ ] API details implement expert recommendations from Phase 1
- [ ] Conditions map validates dangerous patterns from Phase 1
- [ ] Check methods align with validation strategy from Phase 1
- [ ] Manual procedures follow audit approach from Phase 1

---

## 🚫 PHASE 2 ANTI-PATTERNS

### **What NOT to Do in Phase 2**
- ❌ Don't change the technical approach from Phase 1
- ❌ Don't generate fake database values
- ❌ Don't ignore Phase 1 recommendations
- ❌ Don't create non-existent APIs or commands
- ❌ Don't skip database validation
- ❌ Don't break cross-reference alignment

### **What TO Do in Phase 2**
- ✅ Implement Phase 1 recommendations exactly
- ✅ Validate all values against actual databases
- ✅ Maintain cross-reference alignment
- ✅ Create executable compliance checks
- ✅ Use real APIs and commands from Phase 1

---

## 📊 EXAMPLE PHASE 2 OUTPUT

### **Programmatic Check Example**
```json
{
  "control_id": "5.1.1",
  "control_title": "Ensure that the cluster-admin role is only used where required",
  "check_type": "programmatic",
  "compliance_checks": [
    {
      "check_name": "Cluster Admin Role Validation",
      "check_description": "Programmatic validation of cluster-admin role bindings",
      "check_methods": [
        {
          "programmatic_check": {
            "automation_level": "PROGRAMMATIC",
            "method": "kubectl get clusterrolebindings --field-selector roleRef.name=cluster-admin",
            "description": "Check all subjects bound to cluster-admin role",
            "expected_result": "Minimal, necessary cluster-admin bindings only",
            "api_details": {
              "provider": "k8s",
              "service_name": "rbac",
              "resource_type": "k8s.rbac.role",
              "resource_field_path": "subjects[]",
              "endpoint": "/apis/rbac.authorization.k8s.io/v1/clusterrolebindings",
              "assertion_id": "rbac_entitlements.role_definition.least_privilege_roles",
              "rule_id": "k8s.rbac.role.least_privilege_roles",
              "conditions_map": [
                {
                  "field": "subjects[].name",
                  "operator": "not_contains",
                  "value": "system:anonymous",
                  "description": "Validates that no anonymous users have cluster-admin access, preventing unauthorized privilege escalation"
                },
                {
                  "field": "subjects.length",
                  "operator": "less_than_or_equal",
                  "value": "5",
                  "description": "Ensures cluster-admin role is not over-assigned by limiting total bindings to maximum of 5 users/groups"
                },
                {
                  "field": "subjects[].kind",
                  "operator": "not_contains",
                  "value": "ServiceAccount",
                  "description": "Prevents service accounts from having cluster-admin role to follow principle of least privilege"
                }
              ]
            }
          }
        }
      ]
    }
  ]
}
```

### **Admission Controller Example**
```json
{
  "control_id": "1.2.1",
  "control_title": "Ensure that the DenyServiceExternalIPs is set",
  "check_type": "programmatic",
  "compliance_checks": [
    {
      "check_name": "Admission Controller Validation",
      "check_description": "Programmatic validation of DenyServiceExternalIPs admission controller",
      "check_methods": [
        {
          "programmatic_check": {
            "automation_level": "PROGRAMMATIC",
            "method": "kubectl get pods -n kube-system -l component=kube-apiserver -o jsonpath='{.items[0].spec.containers[0].args}'",
            "description": "Check if DenyServiceExternalIPs admission controller is enabled",
            "expected_result": "DenyServiceExternalIPs found in admission controller args",
            "api_details": {
              "provider": "k8s",
              "service_name": "admission-controller",
              "resource_type": "k8s.admission.controller",
              "resource_field_path": "spec.containers[0].args[]",
              "endpoint": "/api/v1/pods",
              "assertion_id": "k8s.admission.controller.deny_service_external_ips",
              "rule_id": "k8s.admission.controller.deny_service_external_ips",
              "conditions_map": [
                {
                  "field": "spec.containers[0].args[]",
                  "operator": "contains",
                  "value": "DenyServiceExternalIPs",
                  "description": "Validates that DenyServiceExternalIPs admission controller is enabled to prevent services from using external IPs, reducing attack surface"
                },
                {
                  "field": "spec.containers[0].args[]",
                  "operator": "contains",
                  "value": "--enable-admission-plugins",
                  "description": "Ensures admission plugins are enabled in the API server configuration"
                }
              ]
            }
          }
        }
      ]
    }
  ]
}
```

---

**Remember**: Phase 2 is about **implementation and database mapping**. Take Phase 1's expert analysis and turn it into executable compliance checks using real databases and APIs!
