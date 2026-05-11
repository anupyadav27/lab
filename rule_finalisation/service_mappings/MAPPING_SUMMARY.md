# AWS One-to-One Mapping Summary

**File:** `AWS_ONE_TO_ONE_MAPPING.json`  
**Format:** Simple compliance_function → rule_id mapping  
**Services:** 11 critical services mapped

---

## Format

```json
{
  "service_name": {
    "mapped": {
      "compliance_function": "rule_id",
      "compliance_function": "rule_id"
    },
    "not_mapped": [
      "function_that_needs_development",
      "another_function_to_develop"
    ]
  }
}
```

---

## Mapping Summary

| Service | Mapped | Not Mapped | Coverage |
|---------|--------|------------|----------|
| **KMS** | 9 | 0 | 100% ✅ |
| **Backup** | 12 | 0 | 100% ✅ |
| **S3** | 10 | 6 | 62% ✅ |
| **RDS** | 15 | 12 | 56% ✅ |
| **EC2** | 14 | 67+ | 17% ⚠️ |
| **CloudTrail** | 5 | 23 | 18% ⚠️ |
| **GuardDuty** | 3 | 3 | 50% ✅ |
| **Lambda** | 4 | 12 | 25% ⚠️ |
| **CloudWatch** | 2 | 23+ | 8% ⚠️ |
| **VPC** | 1 | 15 | 6% ⚠️ |
| **ELBv2** | 2 | 7 | 22% ⚠️ |
| **ELB** | 2 | 4 | 33% ⚠️ |

**Total Estimated:** ~79 mapped, ~172+ need development

---

## Principles Applied

✅ **Audit Logs → CloudTrail**  
All `*_logging_enabled`, `*_audit_*`, `*_integration_cloudwatch_logs` → `aws.cloudtrail.trail.flow_logs_enabled`

✅ **Direct Name Matches**  
Where rule_list has same check with similar name

✅ **AWS Expertise**  
Using knowledge of AWS service capabilities

---

## Quick Examples

**Perfect Match (S3):**
```
aws.s3.bucket_encryption_enabled → aws.s3.bucket.encryption_at_rest_enabled
```

**Audit Log Principle (RDS):**
```
aws.rds.instance_integration_cloudwatch_logs → aws.cloudtrail.trail.flow_logs_enabled
```

**CloudTrail Audit (GuardDuty):**
```
aws.guardduty.eks_audit_log_enabled → aws.cloudtrail.trail.flow_logs_enabled
```

---

**File ready for your review!**  
`service_mappings/AWS_ONE_TO_ONE_MAPPING.json`

