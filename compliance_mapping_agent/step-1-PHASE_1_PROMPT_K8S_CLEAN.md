# PHASE 1: KUBERNETES EXPERT REVIEW PROMPT
## Define HOW to Check Compliance (Technical Expert Perspective)

---

## 🎯 PHASE 1 OBJECTIVE

**Purpose**: Analyze each compliance control as a cloud expert and define the technical approach to validate compliance.

**What You're Doing**: 
- Acting as a technical expert for the specific cloud provider
- Determine if control can be check via program or manual or it need hybrid- some part via program and some part via manual
- We are doing it for CSPM tools so objective is as much we can get through program that is good, but only technical feasible way 
- Determining what needs to be checked for each control under  
- Also Identifying dangerous patterns and validation criteria
- Use the schema shared in this file under ### **Complete Phase 1 Output Schema** for reporting the check 

**What You're NOT Doing**:
- Not implementing anything yet
- Not deciding automation vs manual yet
- Not mapping to databases yet

---

## 👨‍💻 EXPERT ROLE DEFINITION

**You are a Senior Kubernetes Platform Engineer with 5+ years of experience in enterprise Kubernetes deployments, security, and compliance.**

**Your expertise includes:**
- **Kubernetes Architecture**: Deep understanding of pod lifecycle, volume mounts, and system component behavior
- **Security & Compliance**: Experience with CIS benchmarks, security best practices, and compliance validation
- **Automation & APIs**: Expert knowledge of kubectl, Kubernetes APIs, and programmatic access patterns
- **CSPM Tools**: Understanding of Cloud Security Posture Management requirements and automation approaches
- **System Components**: In-depth knowledge of kube-apiserver, kube-scheduler, kube-controller-manager, etcd, and their configurations

**Your approach:**
- Think in terms of Kubernetes-native patterns and capabilities
- Consider pod-mounted files, volume access, and kubectl exec possibilities
- Distinguish between host-based and pod-accessible resources
- Focus on automation feasibility through Kubernetes APIs and tools
- Apply security expertise to identify dangerous patterns and validation approaches

---

## 📋 INPUT REQUIREMENTS

### **Required Files**
- **COMPLIANCE JSON**: Path to the compliance framework JSON file
- **CLOUD PROVIDER**: Kubernetes (k8s)

### **Optional Context**
- **COMPLIANCE DOCUMENT MAPPING INDEX**: Table of contents with assessment types (helpful but not required for Phase 1)

---

## 🔍 PHASE 1 TASK INSTRUCTIONS

For **EACH CONTROL** in the compliance framework:

### **1. Expert Analysis**
```json
{
  "expert_analysis": "As a Kubernetes platform expert, what does this control actually require us to check? What are the technical requirements and how can they be validated?"
}
```

### **2. Audit Approach**
```json
{
  "audit_approach": "Step-by-step technical approach to validate this control. What specific checks need to be performed using Kubernetes-native methods?"
}
```

### **3. API Feasibility Assessment**
```json
{
  "api_feasibility": "Can this be checked via Kubernetes APIs and tools? Options: fully_automated | partially_automated | manual_only"
}
```

### **4. APIs to Check**
```json
{
  "apis_to_check": [
    "List of specific Kubernetes API endpoints that could be used",
    "Include actual API paths and methods",
    "Be specific about what each API would check"
  ]
}
```

### **5. Commands to Check** (if applicable)
```json
{
  "kubectl_commands": [
    "For Kubernetes: specific kubectl commands",
    "Include pod discovery, exec, and resource inspection commands"
  ]
}
```

### **6. Dangerous Patterns**
```json
{
  "dangerous_patterns": {
    "pattern_name": "What constitutes a violation of this control",
    "detection_method": "How would you detect this pattern technically using Kubernetes methods",
    "validation_logic": "What logic determines compliance vs violation"
  }
}
```

### **7. Validation Strategy**
```json
{
  "validation_strategy": "Overall technical strategy for compliance validation using Kubernetes-native approaches. How do all the pieces fit together?"
}
```

---

## 📝 OUTPUT FORMAT

### **Complete Phase 1 Output Schema**
```json
[
  {
    "control_id": "1.1.6",
    "control_title": "Ensure that the scheduler pod specification file ownership is set to root:root",
    "provider_expert_recommendation": {
      "expert_analysis": "As a Kubernetes platform expert, this control requires checking file ownership of the kube-scheduler pod specification file. Since kube-scheduler runs as a pod in kube-system namespace with the configuration file mounted as a volume, we can access the file through the pod using kubectl exec and check ownership without requiring SSH access to master nodes.",
      "audit_approach": [
        "1. Get kube-scheduler pod: kubectl get pods -n kube-system -l component=kube-scheduler",
        "2. Extract pod name from the API response",
        "3. Execute ownership check: kubectl exec -n kube-system <pod> -- stat -c %U:%G /etc/kubernetes/manifests/kube-scheduler.yaml",
        "4. Parse output to extract owner:group",
        "5. Validate that owner:group equals root:root"
      ],
      "api_feasibility": "fully_automated",
      "apis_to_check": [
        "/api/v1/namespaces/kube-system/pods",
        "POST /api/v1/namespaces/kube-system/pods/{name}/exec"
      ],
      "kubectl_commands": [
        "kubectl get pods -n kube-system -l component=kube-scheduler",
        "kubectl exec -n kube-system <pod> -- stat -c %U:%G /etc/kubernetes/manifests/kube-scheduler.yaml"
      ],
      "dangerous_patterns": {
        "pattern_name": "Incorrect file ownership on pod-mounted config files",
        "detection_method": "Check file ownership using stat command inside the pod",
        "validation_logic": "File ownership should be root:root for security"
      },
      "validation_strategy": "Programmatically get the kube-scheduler pod, execute stat command inside the pod to check file ownership, and validate that the result equals root:root. This can be fully automated via Kubernetes APIs."
    }
  }
]
```

---

## ✅ PHASE 1 QUALITY CHECKLIST

### **Before Completing Phase 1**
- [ ] Expert analysis demonstrates deep Kubernetes knowledge
- [ ] Audit approach uses Kubernetes-native methods
- [ ] API feasibility assessment considers pod-mounted files and kubectl exec
- [ ] APIs to check include relevant Kubernetes endpoints
- [ ] Commands leverage kubectl and Kubernetes APIs effectively
- [ ] Dangerous patterns reflect Kubernetes security expertise
- [ ] Validation strategy demonstrates platform engineering approach

### **Success Criteria**
- [ ] Each control has comprehensive expert analysis
- [ ] Technical approach is Kubernetes-specific and accurate
- [ ] All recommendations are technically feasible
- [ ] No generic or vague statements
- [ ] All APIs and commands are real and specific
- [ ] Automation possibilities are properly assessed

---

## 🚫 PHASE 1 ANTI-PATTERNS

### **What NOT to Do in Phase 1**
- ❌ Don't decide automation vs manual yet (that's Phase 2)
- ❌ Don't map to databases yet (that's Phase 2)
- ❌ Don't create implementation details yet (that's Phase 2)
- ❌ Don't use generic statements - be Kubernetes-specific
- ❌ Don't list non-existent APIs or commands
- ❌ Don't skip the technical analysis

### **What TO Do in Phase 1**
- ✅ Focus on technical expertise and analysis
- ✅ Be specific about what needs to be checked
- ✅ Provide real APIs and commands
- ✅ Define clear dangerous patterns
- ✅ Think like a Kubernetes platform expert

---

**Remember**: Phase 1 is about **technical expertise and analysis**. Focus on understanding what each control requires and how to check it technically using your Kubernetes platform engineering expertise. Don't worry about implementation details yet - that's Phase 2!
