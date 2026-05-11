# Prompt Template for Function Duplicate Corrections

## When You Find Duplicate Functions

Use this template to request corrections when you spot duplicate functions that do the same job.

---

## 📋 **Template 1: Simple Duplicate Consolidation**

```
In @aws_functions_final_deduplicated.json, these functions are duplicates - they check the same thing:

Lines X-Y:
- function_name_1
- function_name_2
- function_name_3

These all check [describe what they check, e.g., "EFS encryption at rest"].

Consolidate them to: function_name_1 (or specify which one to keep)

Apply this to both the JSON and the CSV file.
```

### Example:
```
In @aws_functions_final_deduplicated.json, these functions are duplicates:

Lines 306-308:
- aws_efs_encryption_at_rest_enabled
- aws_efs_file_system_encryption_at_rest_check
- aws_efs_file_system_encryption_at_rest_enabled

These all check EFS encryption at rest.

Consolidate them to: aws_efs_encryption_at_rest_enabled

Apply this to both the JSON and the CSV file.
```

---

## 📋 **Template 2: Multiple Service Duplicates**

```
Found duplicates across multiple services:

1. SERVICE_NAME (lines X-Y):
   - function_1 → keep: function_A
   - function_2 → keep: function_A
   Reason: [explain why they're the same]

2. SERVICE_NAME (lines X-Y):
   - function_3 → keep: function_B
   - function_4 → keep: function_B
   Reason: [explain why they're the same]

Consolidate these in both JSON and CSV files.
```

### Example:
```
Found duplicates across multiple services:

1. EFS (lines 306-308):
   - aws_efs_file_system_encryption_at_rest_check → keep: aws_efs_encryption_at_rest_enabled
   - aws_efs_file_system_encryption_at_rest_enabled → keep: aws_efs_encryption_at_rest_enabled
   Reason: All check EFS encryption at rest, same API call

2. EFS (lines 305, 309):
   - aws_efs_have_backup_enabled → keep: aws_efs_backup_enabled
   Reason: Both check if EFS has backup enabled

3. Lambda (lines XXX):
   - aws_lambda_function_not_publicly_accessible → keep: aws_lambda_function_restrict_public_access
   - aws_lambda_function_public_access_check → keep: aws_lambda_function_restrict_public_access
   Reason: All check Lambda resource policy for public access

Consolidate these in both JSON and CSV files.
```

---

## 📋 **Template 3: Ask for Clarification**

Use this when you're unsure if functions are duplicates:

```
Need clarification on these functions in @aws_functions_final_deduplicated.json:

Lines X-Y in SERVICE:
- function_1: [what it seems to check]
- function_2: [what it seems to check]

Are these checking the same thing or different aspects?

If same: which one should we keep?
If different: explain the distinction so I understand.
```

### Example:
```
Need clarification on these functions in @aws_functions_final_deduplicated.json:

Lines 330-335 in elasticache:
- aws_elasticache_redis_cluster_rest_encryption_enabled: checks encryption at rest?
- aws_elasticache_redis_cluster_in_transit_encryption_enabled: checks encryption in transit?

Are these checking the same thing or different aspects?
If different, I'll keep both. If same, which one to keep?
```

---

## 📋 **Template 4: Pattern-Based Duplicates**

Use this for finding duplicates by pattern:

```
Search for pattern duplicates:

Pattern: [describe pattern, e.g., "encryption_enabled vs encrypted"]

Find all functions matching:
- *_encryption_enabled
- *_encrypted

Review and consolidate to consistent naming.
```

### Example:
```
Search for pattern duplicates:

Pattern: Different suffixes for same check

1. Find all: *_encryption_enabled vs *_encrypted
2. Find all: *_check vs *_enabled  
3. Find all: *_status_check vs *_enabled

For each group, keep the most concise/clear naming and consolidate others.
```

---

## 🎯 **Best Practices for Reporting Duplicates**

1. **Be Specific**: Include line numbers from the file
2. **Explain the Job**: Describe what the functions actually check in AWS
3. **Suggest Keep**: Recommend which function to keep (shortest, clearest name)
4. **Provide Context**: Why are they duplicates? (same API, same config check, etc.)

---

## ⚙️ **What Happens When You Use These Templates**

The assistant will:
1. ✅ Create a consolidation mapping
2. ✅ Update the CSV file (replace old functions with new)
3. ✅ Update the JSON file (remove duplicates)
4. ✅ Provide statistics (how many consolidated)
5. ✅ Show before/after function counts

---

## 🚫 **What NOT to Flag as Duplicates**

❌ **Different Resource Types**
```
aws_rds_instance_encryption_enabled  ← RDS Instance
aws_rds_cluster_encryption_enabled   ← RDS Cluster
```
These are DIFFERENT - keep both!

❌ **Different Ports/Protocols**
```
aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22    ← SSH
aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_3389  ← RDP
```
These are DIFFERENT - keep both!

❌ **Different Levels (Account vs Resource)**
```
aws_s3_account_level_public_access_blocks  ← Account level
aws_s3_bucket_public_access                ← Bucket level
```
These are DIFFERENT - keep both!

❌ **Different Granularity**
```
aws_s3_bucket_encryption_enabled  ← Any encryption
aws_s3_bucket_kms_encryption      ← Specifically KMS
```
These are DIFFERENT - keep both!

---

## 💡 **Quick Reference**

| Situation | Template | Example Prompt |
|-----------|----------|----------------|
| Found obvious duplicates | Template 1 | "Lines 306-308 are duplicates, consolidate to X" |
| Multiple duplicates | Template 2 | "Found 3 groups of duplicates, consolidate each" |
| Unsure if duplicate | Template 3 | "Are these the same or different?" |
| Pattern-based search | Template 4 | "Find all *_enabled vs *_check patterns" |

---

## 📝 **Example Session**

**You say:**
```
@aws_functions_final_deduplicated.json lines 306-308:
- aws_efs_encryption_at_rest_enabled
- aws_efs_file_system_encryption_at_rest_check  
- aws_efs_file_system_encryption_at_rest_enabled

These check the same thing (EFS encryption). Keep: aws_efs_encryption_at_rest_enabled
```

**Assistant will:**
- ✅ Update CSV to replace functions
- ✅ Update JSON to remove duplicates
- ✅ Show: "Removed 2 duplicates, 524 functions remaining"

---

*Save this template for future use!*

