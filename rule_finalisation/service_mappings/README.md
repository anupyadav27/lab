# Service Mappings - Simple Clean Format

**Purpose:** Service-by-service comparison for mapping work  
**Date:** November 9, 2025  
**Format:** Simple JSON - just rule_ids and compliance functions

---

## Files (7 CSPs)

| CSP | File | Size | Services |
|-----|------|------|----------|
| AWS | `aws_simple_mapping.json` | 128 KB | 111 |
| Azure | `azure_simple_mapping.json` | 31 KB | 88 |
| GCP | `gcp_simple_mapping.json` | 22 KB | 54 |
| Oracle | `oracle_simple_mapping.json` | 46 KB | 123 |
| IBM | `ibm_simple_mapping.json` | 52 KB | 133 |
| Alicloud | `alicloud_simple_mapping.json` | 52 KB | 133 |
| K8s | `k8s_simple_mapping.json` | 68 KB | 65 |

---

## JSON Format (Clean & Simple)

Each file contains services as keys, with two arrays:

```json
{
  "service_name": {
    "rules": [
      "csp.service.resource.check1",
      "csp.service.resource.check2",
      ...
    ],
    "compliance_functions": [
      "csp.service.check1",
      "csp.service.check2",
      ...
    ]
  }
}
```

---

## Example: AWS GuardDuty

```json
{
  "guardduty": {
    "rules": [
      "aws.guardduty.custom_identifier.source_trusted",
      "aws.guardduty.custom_identifier.storage_encrypted",
      "aws.guardduty.detector.destinations_encrypted",
      "aws.guardduty.detector.detectors_enabled",
      "aws.guardduty.detector.enabled_in_all_regions",
      "aws.guardduty.detector.finding_export_encrypted_destination",
      "aws.guardduty.finding.access_rbac_least_privilege",
      "aws.guardduty.finding.alert_destinations_configured",
      "aws.guardduty.finding.archival_export_encrypted",
      "aws.guardduty.finding.export_destinations_private",
      "aws.guardduty.finding.reports_storage_encrypted",
      "aws.guardduty.finding.suppression_rules_documented_and_scoped",
      "aws.guardduty.ip_set.sources_trusted",
      "aws.guardduty.ip_set.storage_encrypted",
      "aws.guardduty.ip_set.used_by_detectors"
    ],
    "compliance_functions": [
      "aws.guardduty.centrally_managed",
      "aws.guardduty.eks_audit_log_enabled",
      "aws.guardduty.enabled",
      "aws.guardduty.no_high_severity_findings",
      "aws.guardduty.security_center_enabled",
      "aws.guardduty.vulnerability_assessment_enabled"
    ]
  }
}
```

---

## How to Use

### View a Specific Service

```bash
# GuardDuty
cat aws_simple_mapping.json | jq '.guardduty'

# IAM
cat aws_simple_mapping.json | jq '.iam'

# S3
cat aws_simple_mapping.json | jq '.s3'
```

### List All Services

```bash
cat aws_simple_mapping.json | jq 'keys'
```

### Find Services with Both Rules and Compliance

```bash
cat aws_simple_mapping.json | jq 'to_entries | map(select(.value.rules != [] and .value.compliance_functions != [])) | .[].key'
```

### Count Functions Per Service

```bash
cat aws_simple_mapping.json | jq 'to_entries | map({service: .key, rules: (.value.rules | length), compliance: (.value.compliance_functions | length)})'
```

---

## Mapping Workflow

For each service:

1. **Open the JSON** for your CSP
2. **Find a service** (e.g., guardduty)
3. **Review both lists:**
   - `rules[]` - What exists in rule_list
   - `compliance_functions[]` - What compliance needs
4. **Decide for each compliance function:**
   - ✅ Can map to existing rule(s)
   - 🔧 Need to combine multiple rules
   - ❌ Need new development
5. **Document your decision**
6. **Move to next service**

---

## Example Mapping Decision

**Service:** guardduty  
**Compliance needs:** `aws.guardduty.enabled`  
**Available rules:** 
- `aws.guardduty.detector.detectors_enabled`
- `aws.guardduty.detector.enabled_in_all_regions`

**Decision:**
- ✅ **Can map** - `aws.guardduty.enabled` can use `aws.guardduty.detector.enabled_in_all_regions`
- **Action:** Create alias or wrapper function

---

## Quick Stats

### AWS (Best Coverage)
- 111 services total
- 46 services have both rules AND compliance
- 32 services have only rules (unused)
- 33 services have only compliance (need development)

### Other CSPs
**Note:** Azure and Oracle show 0 rules due to CSP name mismatch in source data:
- rule_list uses: `az`, `oci`
- compliance uses: `azure`, `oracle`

This doesn't mean no rules exist - just different naming in source!

---

## Files

```
service_mappings/
├── README.md (this file)
├── aws_simple_mapping.json
├── azure_simple_mapping.json
├── gcp_simple_mapping.json
├── oracle_simple_mapping.json
├── ibm_simple_mapping.json
├── alicloud_simple_mapping.json
└── k8s_simple_mapping.json
```

---

**Simple, clean format - ready for your mapping work!** ✅
