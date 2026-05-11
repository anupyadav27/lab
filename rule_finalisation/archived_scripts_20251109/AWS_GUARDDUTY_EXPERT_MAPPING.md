# AWS GuardDuty - Expert Mapping (Based on Compliance CSV Analysis)

**Service:** GuardDuty  
**Available Rules:** 15  
**Compliance Needs:** 6  
**Mapped:** 1 (17%)  
**Needs Development:** 5 (83%)

---

## Compliance Function Mappings

### 1. ✅ aws.guardduty.enabled
**Compliance Frameworks:** CCCS CA-2 (Control Assessments), CA-7 (Continuous Monitoring), RA-1, RA-5 (Vulnerability)  
**Purpose:** Verify GuardDuty is enabled for security monitoring

**Mapping:**
```
→ aws.guardduty.detector.enabled_in_all_regions
```

**Type:** Direct mapping  
**Confidence:** HIGH  
**Reason:** The rule checks if GuardDuty detector is enabled across all regions, which satisfies the compliance requirement

---

### 2. ❌ aws.guardduty.no_high_severity_findings
**Compliance Framework:** CCCS IR-4 (Incident Handling)  
**Purpose:** Verify no high-severity security findings exist

**Mapping:**
```
→ NEEDS DEVELOPMENT
```

**Type:** Posture check (not configuration)  
**Reason:** This requires querying GuardDuty findings API and checking severity levels - it's a runtime posture check, not a configuration validation

**Implementation needed:** Query GuardDuty findings, filter by severity, count high/critical findings

---

### 3. ❌ aws.guardduty.centrally_managed
**Purpose:** Verify GuardDuty is centrally managed (likely via AWS Organizations)

**Mapping:**
```
→ NEEDS DEVELOPMENT
```

**Reason:** No existing rule checks for central management or AWS Organizations delegated administrator for GuardDuty

**Implementation needed:** Check if GuardDuty is managed through Organizations delegated admin

---

### 4. ❌ aws.guardduty.eks_audit_log_enabled  
**Compliance Framework:** ISO27001 A.8.15 (Logging)  
**Purpose:** Verify EKS audit logs are enabled/monitored

**Mapping:**
```
→ NEEDS DEVELOPMENT (or should be EKS service function)
```

**Reason:** This is about EKS Control Plane audit logging, not GuardDuty detector. May be misclassified as GuardDuty function.

**Recommendation:** Should this be `aws.eks.audit_log_enabled` instead? Or does it check if GuardDuty monitors EKS?

---

### 5. ❓ aws.guardduty.security_center_enabled
**Compliance Framework:** CCCS SI-16 (Memory Protection)  
**Purpose:** Unclear - possibly GuardDuty runtime protection or cross-reference

**Mapping:**
```
→ NEEDS CLARIFICATION
```

**Reason:** "Security Center" is Azure terminology. This might be:
- A cross-cloud copy error
- Referring to AWS Security Hub integration
- Referring to GuardDuty runtime protection features

**Recommendation:** Review compliance requirement to clarify what this actually checks

---

### 6. ❓ aws.guardduty.vulnerability_assessment_enabled
**Purpose:** Vulnerability assessment through GuardDuty

**Mapping:**
```
→ NEEDS CLARIFICATION
```

**Reason:** GuardDuty does threat detection, not vulnerability scanning. This might be:
- Amazon Inspector (the actual vulnerability scanner)
- GuardDuty Malware Protection
- GuardDuty Runtime Monitoring

**Recommendation:** Clarify if this should be `aws.inspector.enabled` instead

---

## Summary

| Compliance Function | Status | Mapped Rule | Action |
|---------------------|--------|-------------|--------|
| guardduty.enabled | ✅ Map | detector.enabled_in_all_regions | Use existing |
| no_high_severity_findings | ❌ Dev | - | Develop findings check |
| centrally_managed | ❌ Dev | - | Develop Org check |
| eks_audit_log_enabled | ❌ Review | - | Clarify service ownership |
| security_center_enabled | ❓ Clarify | - | Review requirement |
| vulnerability_assessment_enabled | ❓ Clarify | - | Review requirement |

**Actionable:** 1 mapped, 2 need development, 3 need clarification

---

**Next:** Should I proceed to map another service (IAM, S3, CloudTrail)?

