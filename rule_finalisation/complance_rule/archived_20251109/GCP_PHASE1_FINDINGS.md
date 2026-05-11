# GCP Phase 1: Initial Findings

**Date:** November 9, 2025  
**Status:** ✅ Phase 1 Complete  
**Next:** Phase 2 - Functional Analysis

---

## Executive Summary

GCP has **significant AWS terminology contamination** affecting 58 functions (15% of total). Major issues include CloudWatch→Logging, S3→Cloud Storage, EBS→Persistent Disk, and other AWS-specific terms that don't exist in GCP.

---

## Statistics

| Metric | Value |
|--------|-------|
| Total GCP Functions | 396 |
| Total Services | 56 |
| Contaminated Functions | 58 (15%) |
| Estimated Consolidations | ~93 |

---

## Top GCP Services (by function count)

1. **Compute** - 61 functions
2. **IAM** - 46 functions  
3. **GKE** (Kubernetes) - 45 functions
4. **SQL** (Cloud SQL) - 38 functions
5. **Logging** - 30 functions
6. **BigQuery** - 15 functions
7. **CloudSQL** - 14 functions
8. **Storage** - 14 functions
9. **Monitoring** - 12 functions
10. **KMS** - 9 functions

---

## Critical Issue 1: AWS CloudWatch → GCP Logging/Monitoring

**Impact:** 4 functions, 115 total occurrences

### Functions Found:
```
gcp_logging_cloudwatch_logging_enabled (69x)
gcp_logging_cloudwatch_logs_enabled (2x)
gcp_sql_instance_integration_cloudwatch_logs (39x)
gcp_elasticsearch_service_domains_cloudwatch_logging_enabled (5x)
```

### Required Changes:
- `gcp_logging_cloudwatch_logging_enabled` → `gcp_logging_enabled`
- `gcp_logging_cloudwatch_logs_enabled` → `gcp_logging_enabled` (duplicate)
- `gcp_sql_instance_integration_cloudwatch_logs` → `gcp_sql_instance_logging_enabled`
- `gcp_elasticsearch_service_domains_cloudwatch_logging_enabled` → `gcp_elasticsearch_service_domains_logging_enabled`

**Consolidations:** 4 → 3 functions (1 duplicate)

---

## Critical Issue 2: AWS S3 → GCP Cloud Storage

**Impact:** 3 unique functions, 125 total occurrences

### Functions Found:
```
gcp_logging_s3_dataevents_read_enabled (61x)
gcp_logging_s3_dataevents_write_enabled (62x)
gcp_storage_s3_bucket_encryption_enabled (2x)
```

### Required Changes:
- `gcp_logging_s3_dataevents_read_enabled` → `gcp_logging_storage_read_events_enabled`
- `gcp_logging_s3_dataevents_write_enabled` → `gcp_logging_storage_write_events_enabled`
- `gcp_storage_s3_bucket_encryption_enabled` → `gcp_storage_bucket_encryption_enabled`

**Consolidations:** 3 functions need renaming

---

## Critical Issue 3: AWS EBS → GCP Persistent Disk

**Impact:** 6 functions, 114 total occurrences

### Functions Found:
```
gcp_compute_ebs_default_encryption (24x)
gcp_compute_ebs_volume_encryption (24x)
gcp_compute_ebs_public_snapshot (61x)
gcp_compute_ebs_volume_encrypted (3x)
gcp_compute_ebs_volume_encryption_enabled (2x)
gcp_vm_ebs_volume_encrypted (3x - overlaps with compute)
```

### Required Changes:
- `gcp_compute_ebs_default_encryption` → `gcp_compute_disk_encryption_enabled`
- `gcp_compute_ebs_volume_encryption` → `gcp_compute_disk_encryption_enabled` (duplicate)
- `gcp_compute_ebs_public_snapshot` → `gcp_compute_disk_public_snapshot`
- `gcp_compute_ebs_volume_encrypted` → `gcp_compute_disk_encrypted`
- `gcp_compute_ebs_volume_encryption_enabled` → `gcp_compute_disk_encryption_enabled` (duplicate)
- `gcp_vm_ebs_volume_encrypted` → `gcp_compute_disk_encrypted` (duplicate)

**Consolidations:** 6 → 3 functions (3 duplicates)

---

## Critical Issue 4: AWS RDS → GCP Cloud SQL

**Impact:** 1 function, 2 occurrences

### Functions Found:
```
gcp_sql_rds_instance_encryption_enabled (2x)
```

### Required Changes:
- `gcp_sql_rds_instance_encryption_enabled` → `gcp_sql_instance_encryption_at_rest_enabled`

**Consolidations:** 1 function needs renaming

---

## Critical Issue 5: AWS SSM → GCP OS Config

**Impact:** 3 functions, 39 occurrences

### Functions Found:
```
gcp_compute_instance_managed_by_ssm (36x)
gcp_compute_ssm_association_compliance (1x)
gcp_security_command_center_vulnerability_assessment_enabled (2x - false positive)
```

### Required Changes:
- `gcp_compute_instance_managed_by_ssm` → `gcp_compute_instance_managed_by_os_config`
- `gcp_compute_ssm_association_compliance` → `gcp_compute_os_config_compliance`

**Note:** `gcp_security_command_center_vulnerability_assessment_enabled` contains "ssm" as part of "assessment" - NOT an issue.

**Consolidations:** 2 functions need renaming (1 false positive)

---

## Issue 6: GCP Bucket Terminology

**Impact:** 20 functions

### Analysis:
GCP **does use "bucket"** for Cloud Storage buckets (same as AWS S3). This is correct GCP terminology.

**However**, need to check for consistency:
- `gcp_storage_bucket_*` vs `gcp_gcs_bucket_*` 
- Are these the same or different services?

**GCS** = Google Cloud Storage = `gcp_storage_*` should be standard

### Potential Consolidations:
```
gcp_gcs_bucket_* → gcp_storage_bucket_* (use storage as standard prefix)
```

**Functions affected:** 7 functions with `gcp_gcs_bucket_*` prefix

---

## Issue 7: GCP VPC Terminology

**Impact:** 13 functions

### Analysis:
GCP **does use "VPC"** (Virtual Private Cloud). This is correct terminology and doesn't need to change.

**No consolidations needed** ✅

---

## Issue 8: IAM Policy Naming

**Impact:** 46 functions with AWS-style policy naming

### Functions Found:
```
gcp_iam_aws_attached_policy_no_administrative_privileges (46x)
gcp_iam_customer_attached_policy_no_administrative_privileges (46x)
gcp_iam_inline_policy_no_administrative_privileges (46x)
```

### Analysis:
These function names reference AWS-style policy types:
- **aws_attached_policy** - AWS concept (managed policies)
- **customer_attached_policy** - AWS concept (customer-managed policies)  
- **inline_policy** - AWS concept

GCP uses **IAM policies** and **IAM roles** differently - no concept of "attached" vs "inline".

### Required Changes:
All three → `gcp_iam_policy_no_administrative_privileges`

**Consolidations:** 3 → 1 function

---

## Issue 9: Encryption Naming Inconsistency

**Patterns found:** 4 different naming patterns

| Pattern | Count | Example |
|---------|-------|---------|
| `_encrypted` | 7 | `gcp_bigquery_cluster_encrypted` |
| `_encryption_enabled` | 13 | `gcp_gcs_bucket_encryption_enabled` |
| `_encryption_at_rest` | 2 | `gcp_sql_instance_encryption_at_rest` |
| `_encryption` (other) | 12 | `gcp_kms_cmk_rotation_enabled` |

### Recommendation:
Standardize on `_encryption_enabled` for most cases, `_encryption_at_rest_enabled` for specific at-rest encryption.

**Estimated consolidations:** 15-20 functions

---

## Issue 10: Logging Naming Inconsistency

**Patterns found:** 2 different naming patterns

| Pattern | Count |
|---------|-------|
| `_logging_enabled` | 16 |
| `_logs_enabled` | 5 |

### Recommendation:
Standardize on `_logging_enabled`

**Consolidations:** ~5 functions need renaming

---

## Summary of Required Consolidations

| Issue Category | Functions Affected | Estimated Consolidations |
|----------------|-------------------|-------------------------|
| CloudWatch → Logging | 4 | 4 → 3 (1 dupe) |
| S3 → Cloud Storage | 3 | 3 renames |
| EBS → Persistent Disk | 6 | 6 → 3 (3 dupes) |
| RDS → Cloud SQL | 1 | 1 rename |
| SSM → OS Config | 2 | 2 renames |
| GCS → Storage consistency | 7 | 7 renames |
| IAM policy types | 3 | 3 → 1 (2 dupes) |
| Encryption naming | 20 | 15-20 consolidations |
| Logging naming | 5 | 5 renames |
| **TOTAL** | **51+** | **~50-55 consolidations** |

**Note:** Initial estimate was 93, but after detailed analysis, real issues are ~50-55 targeted fixes.

---

## GCP-Specific Terminology (Correct)

These GCP terms are **correct** and should be kept:
- ✅ **bucket** - GCP Cloud Storage uses buckets
- ✅ **vpc** - GCP uses VPC (Virtual Private Cloud)
- ✅ **gke** - Google Kubernetes Engine
- ✅ **cloudsql** - GCP Cloud SQL (database service)
- ✅ **bigquery** - GCP BigQuery (data warehouse)
- ✅ **kms** - GCP Cloud KMS (Key Management Service)

---

## Next Steps: Phase 2

**Phase 2 Objectives:**
1. Service-by-service functional analysis
2. Create complete consolidation mapping
3. Identify all duplicates within services
4. Document GCP-specific patterns
5. Prepare for Phase 3 (detailed service deep dive)

**Estimated Time:** 2-3 hours

---

*GCP Phase 1 Complete - Ready for Phase 2* ✅

