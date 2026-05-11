# AWS Functions by Service - Complete Summary (Normalized)

**Generated:** 2025-11-08  
**Source:** consolidated_compliance_rules_2025-11-08.csv (Normalized)

---

## Overview

This document summarizes all AWS security check functions extracted from the consolidated compliance rules database, organized by AWS service.

**All function names have been normalized to eliminate duplicates and ensure consistency.**

### Statistics

- **Total AWS Services:** 81
- **Total AWS Functions:** 636 (down from 747 - eliminated 111 duplicates)
- **Total Compliance Mappings:** 4,586

### Normalization Impact

- ✅ **Eliminated 111 duplicate function names** (14.9% reduction)
- ✅ **Fixed 7 functions** with repeated service names (e.g., `aws_s3_s3_bucket_*` → `aws_s3_bucket_*`)
- ✅ **Normalized 108 functions** with inconsistent `aws_` prefixes
- ✅ **Moved 108 functions** from 'unknown' to proper services (76.1% reduction in 'unknown' category)
- ✅ **Updated 397 CSV rows** with normalized function names
- ✅ **Standardized 2,039 function references** across all compliance controls

---

## Data Structure

The JSON file `aws_functions_by_service_2025-11-08.json` contains AWS functions grouped by service:

```json
{
  "service_name": {
    "function_name": [
      "unique_compliance_id_1",
      "unique_compliance_id_2",
      ...
    ]
  }
}
```

### Example: IAM Service

```json
{
  "iam": {
    "aws_iam_access_analyzer_active_status_all_regions": [
      "cis_aws_aws_1.20_0145"
    ],
    "aws_iam_access_key_rotation_90_days_check": [
      "cis_aws_aws_2.13_0013"
    ],
    "aws_iam_console_mfa_enabled": [
      "cisa_ce_v1_multi_cloud_Booting_Up-2_0010",
      "cisa_ce_v1_multi_cloud_Your_Surroundings-1_0013"
    ]
  }
}
```

---

## Top 20 Services by Function Count

| Rank | Service | Functions | Compliance Mappings |
|------|---------|-----------|---------------------|
| 1 | ec2 | 94 | 451 |
| 2 | iam | 73 | 290 |
| 3 | cloudtrail | 42 | 246 |
| 4 | unknown | 34 | 390 |
| 5 | rds | 32 | 192 |
| 6 | cloudwatch | 26 | 158 |
| 7 | s3 | 25 | 162 |
| 8 | vpc | 16 | 62 |
| 9 | backup | 13 | 19 |
| 10 | kms | 12 | 24 |
| 11 | lambda | 12 | 13 |
| 12 | neptune | 12 | 14 |
| 13 | dynamodb | 11 | 36 |
| 14 | glue | 11 | 24 |
| 15 | redshift | 11 | 93 |
| 16 | eks | 10 | 15 |
| 17 | codebuild | 8 | 11 |
| 18 | efs | 8 | 34 |
| 19 | elbv2 | 8 | 51 |
| 20 | guardduty | 7 | 110 |

**Note:** The 'unknown' category has been reduced from 142 to 34 functions (76% reduction) after normalization.

---

## Most Referenced Functions (Top 20)

Functions that appear in the most compliance controls:

| Rank | Service | Function | Mappings |
|------|---------|----------|----------|
| 1 | guardduty | aws_guardduty_is_enabled | 120 |
| 2 | iam | aws_iam_password_policy_minimum_length_14 | 88 |
| 3 | cloudtrail | aws_cloudtrail_cloudwatch_logging_enabled | 88 |
| 4 | cloudtrail | aws_cloudtrail_multi_region_enabled | 86 |
| 5 | cloudtrail | aws_cloudtrail_s3_dataevents_write_enabled | 80 |
| 6 | cloudtrail | aws_cloudtrail_s3_dataevents_read_enabled | 79 |
| 7 | ec2 | aws_ec2_ebs_public_snapshot | 75 |
| 8 | ec2 | aws_ec2_instance_public_ip | 75 |
| 9 | emr | aws_emr_cluster_master_nodes_no_public_ip | 69 |
| 10 | iam | aws_iam_aws_attached_policy_no_administrative_privileges | 66 |
| 11 | iam | aws_iam_customer_attached_policy_no_administrative_privileges | 66 |
| 12 | iam | aws_iam_inline_policy_no_administrative_privileges | 66 |
| 13 | apigateway | aws_apigateway_restapi_logging_enabled | 64 |
| 14 | elb | aws_elb_ssl_listeners | 62 |
| 15 | s3 | aws_s3_bucket_secure_transport_policy | 60 |
| 16 | iam | aws_iam_no_root_access_key | 58 |
| 17 | securityhub | aws_securityhub_enabled | 57 |
| 18 | ssm | aws_ssm_managed_compliant_patching | 57 |
| 19 | rds | aws_rds_instance_integration_cloudwatch_logs | 56 |
| 20 | opensearch | aws_opensearch_service_domains_node_to_node_encryption_enabled | 55 |

**Note:** All function names are now normalized with consistent `aws_` prefixes.

---

## Service Details

### IAM (Identity and Access Management)
- **Functions:** 73
- **Compliance Mappings:** 290
- **Key Functions:**
  - `aws_iam_access_analyzer_active_status_all_regions`
  - `aws_iam_access_key_rotation_90_days_check`
  - `aws_iam_console_mfa_enabled`
  - `aws_iam_password_policy_minimum_length_14`

### EC2 (Elastic Compute Cloud)
- **Functions:** 94
- **Compliance Mappings:** 451
- **Key Functions:**
  - `aws_ec2_ebs_default_encryption_enabled`
  - `aws_ec2_instance_imdsv2_enabled`
  - `aws_ec2_security_group_ingress_open`
  - `aws_ec2_ebs_snapshot_encrypted`

### S3 (Simple Storage Service)
- **Functions:** 26
- **Compliance Mappings:** 162
- **Key Functions:**
  - `aws_s3_bucket_public_access`
  - `aws_s3_bucket_default_encryption`
  - `aws_s3_bucket_server_access_logging_enabled`
  - `aws_s3_bucket_secure_transport_policy`

### CloudTrail
- **Functions:** 42
- **Compliance Mappings:** 246
- **Key Functions:**
  - `aws_cloudtrail_multi_region_enabled`
  - `aws_cloudtrail_log_file_validation_enabled`
  - `aws_cloudtrail_cloudwatch_logging_enabled`
  - `aws_cloudtrail_encryption_enabled`

### RDS (Relational Database Service)
- **Functions:** 32
- **Compliance Mappings:** 192
- **Key Functions:**
  - `aws_rds_instance_encryption_enabled`
  - `aws_rds_instance_backup_enabled`
  - `aws_rds_instance_multi_az_enabled`
  - `aws_rds_instance_storage_encrypted`

---

## Usage Examples

### 1. Find all compliance controls for a specific function

```python
import json

with open('aws_functions_by_service_2025-11-08.json', 'r') as f:
    data = json.load(f)

# Get compliance IDs for S3 bucket encryption
function = 'aws_s3_bucket_default_encryption'
compliance_ids = data['s3'][function]
print(f"Function: {function}")
print(f"Compliance Controls: {len(compliance_ids)}")
for cid in compliance_ids:
    print(f"  - {cid}")
```

### 2. Get all functions for a service

```python
import json

with open('aws_functions_by_service_2025-11-08.json', 'r') as f:
    data = json.load(f)

# Get all IAM functions
service = 'iam'
functions = list(data[service].keys())
print(f"Service: {service.upper()}")
print(f"Total Functions: {len(functions)}")
for func in sorted(functions):
    print(f"  - {func}")
```

### 3. Find services with specific function patterns

```python
import json

with open('aws_functions_by_service_2025-11-08.json', 'r') as f:
    data = json.load(f)

# Find all encryption-related functions
keyword = 'encryption'
for service, functions in data.items():
    matching = [f for f in functions.keys() if keyword in f.lower()]
    if matching:
        print(f"{service.upper()} - {len(matching)} encryption functions")
        for func in matching:
            print(f"  - {func}")
```

---

## Notes

### Function Normalization

All AWS function names have been normalized to ensure consistency and eliminate duplicates:

1. **Standard Prefix:** All functions now use the `aws_` prefix consistently
   - Before: `guardduty_is_enabled` and `aws_guardduty_is_enabled`
   - After: `aws_guardduty_is_enabled` (consolidated)

2. **Removed Repeated Service Names:** Fixed functions with duplicate service identifiers
   - Before: `aws_s3_s3_bucket_encryption_enabled`
   - After: `aws_s3_bucket_encryption_enabled`

3. **Service Categorization:** Functions properly categorized by AWS service
   - Before: 142 functions in 'unknown' category
   - After: 34 functions in 'unknown' category (76% improvement)

### "Unknown" Service Category

The "unknown" category (34 functions remaining) contains functions that don't follow the standard AWS naming convention `aws_{service}_{function}`. These may be:
- Legacy function names
- Custom check names  
- Functions with non-standard naming patterns

These functions are still valid and mapped to compliance controls, but their service cannot be automatically extracted from the function name.

### Function Mapping Reference

A complete mapping of all normalized functions is available in:
- `function_normalization_mapping.json` - Shows which function variants were consolidated

This mapping can be used to:
- Update existing scripts or references
- Understand which function names are aliases
- Maintain backward compatibility if needed

---

## Files Generated

1. **aws_functions_by_service_2025-11-08.json**
   - Complete mapping of all AWS functions to compliance IDs
   - Grouped by AWS service
   - JSON format for easy programmatic access

2. **AWS_FUNCTIONS_SUMMARY.md** (this file)
   - Human-readable summary
   - Statistics and analysis
   - Usage examples

---

## Cross-Reference

To look up details for any unique compliance ID, refer to:
- `consolidated_compliance_rules_2025-11-08.csv`

Each unique compliance ID in this JSON maps back to a specific row in the consolidated CSV containing:
- Full compliance framework details
- Requirement descriptions
- All cloud provider checks (not just AWS)
- References and source information

---

**End of Summary**

