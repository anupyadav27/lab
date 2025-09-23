# PHASE 1: PROVIDER EXPERT REVIEW PROMPT
## Define HOW to Check Compliance (Technical Expert Perspective)

---

## 🎯 PHASE 1 OBJECTIVE

**Purpose**: Analyze each compliance control as a cloud expert and define the technical approach to validate compliance.

**What You're Doing**: 
- Acting as a technical expert for the specific cloud provider
- Determine if conrol can be check via program or manual or it need hybrid- some part via program and some part via manual
- We are doing it for CSPM tools so objective is as much we can get through program that is good, but only technical feasible way 
- Determining what needs to be checked for each control under  
- Also Identifying dangerous patterns and validation criteria
- Use the schmea shared in this file under ### **Complete Phase 1 Output Schema** for reporting the check 

**What You're NOT Doing**:
- Not implementing anything yet
- Not deciding automation vs manual yet
- Not mapping to databases yet

---

## 📋 INPUT REQUIREMENTS

### **Required Files**
- **COMPLIANCE JSON**: Path to the compliance framework JSON file
- **CLOUD PROVIDER**: Specify which provider 

### **Optional Context**
- **COMPLIANCE DOCUMENT MAPPING INDEX**: Table of contents with assessment types (helpful but not required for Phase 1)

---

## 🔍 PHASE 1 TASK INSTRUCTIONS

For **EACH CONTROL** in the compliance framework:

### **1. Expert Analysis**
```json
{
  "expert_analysis": "As a [CLOUD_PROVIDER] expert, what does this control actually require us to check? What are the technical requirements?"
}
```

### **2. Audit Approach**
```json
{
  "audit_approach": "Step-by-step technical approach to validate this control. What specific checks need to be performed?"
}
```

### **3. API Feasibility Assessment**
```json
{
  "api_feasibility": "Can this be checked via APIs? Options: fully_automated | partially_automated | manual_only"
}
```



### **5. APIs to Check**
```json
{
  "apis_to_check": [
    "List of specific API endpoints that could be used",
    "Include actual API paths and methods",
    "Be specific about what each API would check"
  ]
}
```

### **6. Commands to Check** (if applicable)
```json
{
  "kubectl_commands": [
    "For Kubernetes: specific kubectl commands",
    "For other clouds: equivalent CLI commands"
  ]
}
```

### **7. Dangerous Patterns**
```json
{
  "dangerous_patterns": {
    "pattern_name": "What constitutes a violation of this control",
    "detection_method": "How would you detect this pattern technically",
    "validation_logic": "What logic determines compliance vs violation"
  }
}
```

### **8. Validation Strategy**
```json
{
  "validation_strategy": "Overall technical strategy for compliance validation. How do all the pieces fit together?"
}
```

---

## 📝 OUTPUT FORMAT

### **Complete Phase 1 Output Schema**
```json
[
  {
    "control_id": "1.1.1",
    "control_title": "Ensure that the API server pod specification file permissions are set to 600 or more restrictive",
    "provider_expert_recommendation": {
      "expert_analysis": "This control requires checking file system permissions on master nodes where the API server pod specification files are located. The files must have restrictive permissions (600 or more restrictive) to prevent unauthorized access.",
      "audit_approach": [
        "1. Identify all master nodes in the cluster",
        "2. Check file permissions on /etc/kubernetes/manifests/kube-apiserver.yaml",
        "3. Verify permissions are 600 or more restrictive (no group/other read/write)",
        "4. Check ownership is root:root",
        "5. Repeat for all master nodes"
      ],
      "apis_to_check": [
        "No Kubernetes API can check file system permissions on host nodes",
        "Would require SSH access to master nodes"
      ],
      "kubectl_commands": [
        "kubectl get nodes --selector=node-role.kubernetes.io/master",
        "kubectl get nodes --selector=node-role.kubernetes.io/control-plane"
      ],
      "dangerous_patterns": {
        "pattern_name": "Overly permissive file permissions",
        "detection_method": "Check file permissions using 'ls -la' command on master nodes",
        "validation_logic": "File permissions should be 600 (rw-------) or more restrictive, ownership should be root:root"
      },
      "validation_strategy": "Manual file system inspection on all master nodes to verify API server configuration files have proper permissions and ownership"
    }
  }
]
```

---

## ✅ PHASE 1 QUALITY CHECKLIST

### **Before Completing Phase 1**
- [ ] Expert analysis clearly explains what needs to be checked
- [ ] Audit approach provides specific, actionable steps
- [ ] API feasibility assessment is accurate for the cloud provider
- [ ] Recommended method aligns with API feasibility
- [ ] APIs to check are real, existing endpoints
- [ ] Commands are real, executable commands
- [ ] Dangerous patterns clearly define violations
- [ ] Validation strategy ties everything together

### **Success Criteria**
- [ ] Each control has comprehensive expert analysis
- [ ] Technical approach is provider-specific and accurate
- [ ] All recommendations are technically feasible
- [ ] No generic or vague statements
- [ ] All APIs and commands are real and specific

---

## 🚫 PHASE 1 ANTI-PATTERNS

### **What NOT to Do in Phase 1**
- ❌ Don't decide automation vs manual yet (that's Phase 2)
- ❌ Don't map to databases yet (that's Phase 2)
- ❌ Don't create implementation details yet (that's Phase 2)
- ❌ Don't use generic statements - be provider-specific
- ❌ Don't list non-existent APIs or commands
- ❌ Don't skip the technical analysis

### **What TO Do in Phase 1**
- ✅ Focus on technical expertise and analysis
- ✅ Be specific about what needs to be checked
- ✅ Provide real APIs and commands
- ✅ Define clear dangerous patterns
- ✅ Think like a cloud provider expert

---

## 📊 EXAMPLE PHASE 1 OUTPUT

### **RBAC Control Example**
```json
{
  "control_id": "5.1.1",
  "control_title": "Ensure that the cluster-admin role is only used where required",
  "provider_expert_recommendation": {
    "expert_analysis": "This control requires checking which subjects (users, groups, service accounts) are bound to the cluster-admin ClusterRole. The cluster-admin role provides unlimited access to the entire cluster, so it should be used sparingly and only for legitimate administrative purposes.",
    "audit_approach": [
      "1. List all ClusterRoleBindings that reference cluster-admin role",
      "2. Identify all subjects bound to these ClusterRoleBindings",
      "3. Verify each subject has legitimate need for cluster-admin access",
      "4. Check for excessive or unnecessary bindings"
    ],
    "apis_to_check": [
      "/apis/rbac.authorization.k8s.io/v1/clusterrolebindings",
      "/apis/rbac.authorization.k8s.io/v1/clusterroles"
    ],
    "kubectl_commands": [
      "kubectl get clusterrolebindings --field-selector roleRef.name=cluster-admin",
      "kubectl describe clusterrolebindings cluster-admin"
    ],
    "dangerous_patterns": {
      "pattern_name": "Excessive cluster-admin bindings",
      "detection_method": "Check ClusterRoleBindings for cluster-admin role and analyze bound subjects",
      "validation_logic": "Should have minimal subjects bound to cluster-admin, typically only system components and essential administrators"
    },
    "validation_strategy": "Programmatically query ClusterRoleBindings to identify all subjects with cluster-admin access and validate necessity of each binding"
  }
}
```

---

**Remember**: Phase 1 is about **technical expertise and analysis**. Focus on understanding what each control requires and how to check it technically. Don't worry about implementation details yet - that's Phase 2!
