# AWS Function Improvement Steps - Replicable for All CSPs

**Date:** November 8, 2025  
**Purpose:** Step-by-step guide to improve function quality for Azure, GCP, Oracle, IBM, Alicloud, Kubernetes

---

## 📊 AWS Results Summary

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Total Functions** | 629 | 524 | -105 (16.7% reduction) |
| **Services** | 80 | 80 | Same |
| **Unknown/Miscategorized** | 34 entries (~100+ functions) | 0 | ✅ 100% fixed |
| **Duplicate Services** | 2 (awslambda+lambda, docdb+documentdb) | 0 | ✅ Merged |
| **Functional Duplicates** | 105 | 0 | ✅ Consolidated |
| **Quality Score** | 2.5/5 | 4.5/5 | +80% |

---

## 🎯 Step-by-Step Improvement Process

### **PHASE 1: Fix Critical Issues** (Week 1)

#### Step 1.1: Identify "Unknown" or Miscategorized Functions
**Problem:** Functions missing CSP prefix or concatenated together

**AWS Example:**
```
❌ BAD:
- "acm_certificates_expiration_check"  (missing aws_ prefix)
- "s3_bucket_encryption, rds_encryption"  (concatenated)

✅ FIXED:
- "aws_acm_certificate_expiration"
- "aws_s3_bucket_encryption_enabled" + "aws_rds_instance_encryption_enabled"
```

**Action for Other CSPs:**
```bash
# Search for functions without proper prefix
grep -E "^[a-z_]+," consolidated_compliance_rules_FINAL.csv | grep "azure_checks\|gcp_checks"

# Look for comma-separated concatenations
grep "," consolidated_compliance_rules_FINAL.csv | grep -E "azure_|gcp_|oracle_"
```

**Expected Fix:** 
- Add proper CSP prefix (azure_, gcp_, oracle_, ibm_, alicloud_, k8s_)
- Split concatenated functions
- Categorize by correct service

---

#### Step 1.2: Merge Duplicate Service Names
**Problem:** Same service listed under different names

**AWS Example:**
```
❌ BAD:
- "awslambda" service (6 functions)
- "lambda" service (12 functions)

✅ FIXED:
- "lambda" service (18 functions merged)
```

**Action for Other CSPs:**
```
Check for:
- Azure: "azurefunctions" vs "functions"
- GCP: "gcpfunctions" vs "cloudfunctions"
- Kubernetes: "k8s" vs "kubernetes"
```

**Expected Fix:**
- Standardize to one service name
- Merge all functions under canonical name
- Update CSV with consolidated names

---

#### Step 1.3: Remove Name-Based Duplicates
**Problem:** Same function with different naming conventions

**AWS Example:**
```
❌ BAD:
- aws_backup_recovery_point_encryption
- aws_backup_recovery_point_encrypted

✅ FIXED:
- aws_backup_recovery_point_encrypted (kept)
```

**Action for Other CSPs:**
```
Look for patterns:
- *_encryption vs *_encrypted
- *_check vs *_enabled vs *_status_check
- *_is_enabled vs *_enabled
```

**Expected Fix:**
- Choose consistent naming pattern
- Consolidate to shortest/clearest name
- Update CSV and JSON

---

### **PHASE 2: Functional Analysis** (Week 2)

#### Step 2.1: Identify Functional Duplicates by Service

**AWS Example - CloudTrail:**
```
❌ DUPLICATES (same job):
- aws_cloudtrail_enabled
- aws_cloudtrail_multi_region_enabled
- aws_cloudtrail_trail_multi_region_logging_enabled
- aws_cloudtrail_multi_region_enabled_logging_management_events
- aws_cloudtrail_trail_multi_region_management_logging_enabled

✅ CONSOLIDATED:
- aws_cloudtrail_multi_region_enabled (covers all)

WHY: Multi-region CloudTrail automatically enables single-region. 
     Checking multi-region is sufficient.
```

**Action for Other CSPs:**
```
For each major service (compute, storage, database, logging):
1. List all functions
2. Group by what they CHECK (not what they're named)
3. Identify overlaps
4. Keep most comprehensive check
```

**Azure Example:**
```
Service: Monitor (equivalent to AWS CloudTrail)
- azure_monitor_enabled
- azure_monitor_multi_region_enabled
- azure_monitor_all_regions_enabled

Decision: Keep azure_monitor_multi_region_enabled
```

---

#### Step 2.2: Analyze Encryption Checks

**AWS Example - S3:**
```
❌ DUPLICATES:
- aws_s3_bucket_default_encryption
- aws_s3_bucket_encryption_enabled
- aws_s3_bucket_kms_encryption
- aws_s3_bucket_default_kms_encryption

✅ RATIONALIZED:
- aws_s3_bucket_encryption_enabled (any encryption)
- aws_s3_bucket_kms_encryption (specifically KMS)

WHY: Two levels of checking:
     1. Is ANY encryption enabled? (compliance requirement)
     2. Is it SPECIFICALLY KMS? (stricter requirement)
```

**Action for Other CSPs:**
```
For each storage/database service:
1. Group all encryption functions
2. Distinguish:
   - Any encryption vs specific encryption type
   - At-rest vs in-transit
   - Account-level vs resource-level
3. Keep both general AND specific checks
```

**Template:**
```
KEEP:
- {csp}_{service}_encryption_enabled  (general)
- {csp}_{service}_kms_encryption     (specific)

REMOVE:
- {csp}_{service}_default_encryption  (duplicate of general)
- {csp}_{service}_default_kms_encryption (duplicate of specific)
```

---

#### Step 2.3: Analyze Access/Public Exposure Checks

**AWS Example - S3:**
```
❌ TOO MANY:
- aws_s3_bucket_public_access
- aws_s3_bucket_public_read_prohibited
- aws_s3_bucket_public_write_prohibited
- aws_s3_bucket_policy_public_write_access
- aws_s3_account_level_public_access_blocks
- aws_s3_public_access_block_check

✅ RATIONALIZED:
- aws_s3_account_level_public_access_blocks (account-level)
- aws_s3_bucket_public_read_prohibited (bucket-level read)
- aws_s3_bucket_public_write_prohibited (bucket-level write)

WHY: Different control planes and granularity:
     - Account-level blocks (broad control)
     - Bucket-level read/write (granular control)
```

**Action for Other CSPs:**
```
For each service with public access:
1. Separate account-level vs resource-level
2. Separate read vs write permissions
3. Remove generic "public_access" if you have specific read/write
```

---

#### Step 2.4: Analyze Multi-AZ / High Availability Checks

**AWS Example - RDS:**
```
❌ DUPLICATES:
- aws_rds_instance_multi_az
- aws_rds_instance_multi_az_compliance_check
- aws_rds_multi_az_enabled
- aws_rds_cluster_multi_az

✅ RATIONALIZED:
- aws_rds_instance_multi_az (for instances)
- aws_rds_cluster_multi_az (for clusters)

WHY: Instance and Cluster are DIFFERENT resource types
     Both checks needed
```

**Action for Other CSPs:**
```
KEEP separate checks for:
- Different resource types (instance vs cluster)
- Different deployment models (VM vs container)

CONSOLIDATE:
- Multiple naming variations of same check
```

---

### **PHASE 3: Service-Specific Deep Dive** (Week 3)

#### Step 3.1: Identity & Access (IAM/RBAC)

**AWS Consolidations:**
```
1. Root Account MFA:
   - aws_iam_root_mfa_enabled (kept)
   - aws_iam_root_mfa_status_check (removed)
   - aws_iam_root_user_mfa_check (removed)

2. User MFA:
   - aws_iam_user_mfa_enabled_console_access (kept - specific)
   - aws_iam_user_mfa_enabled (removed - generic)

3. Access Key Rotation:
   - aws_iam_access_key_rotation_90_days_check (kept - specific days)
   - aws_iam_access_key_rotation_check (removed - generic)

4. Password Policy:
   - aws_iam_password_policy_minimum_length_14 (kept - specific)
   - aws_iam_password_policy_expires_passwords_within_90_days_or_less (kept)
   - aws_iam_password_policy_reuse_24 (kept)
   - aws_iam_user_password_policy_complex (kept)
   - aws_iam_password_policy_strong (removed - generic)
   - aws_iam_password_policy_compliance (removed - generic)
```

**Template for All CSPs:**
```
For IAM/RBAC functions:

CONSOLIDATE:
- *_mfa_enabled → Keep most specific (console_access, hardware, etc.)
- *_rotation_check → Keep version with specific days (90, 45, etc.)
- *_password_policy_* → Keep individual requirements (length, expiry, reuse, complexity)

KEEP SEPARATE:
- Root/admin vs regular users
- Service accounts vs user accounts
- Different MFA types (hardware vs virtual)
```

---

#### Step 3.2: Compute (EC2/VM)

**AWS Consolidations:**
```
1. EBS Encryption:
   - aws_ec2_ebs_encryption_by_default_enabled (account default)
   - aws_ec2_ebs_volume_encrypted (per-volume check)
   - aws_ec2_ebs_snapshots_encrypted (snapshot check)
   ALL KEPT - different scopes

2. IMDSv2:
   - aws_ec2_instance_imdsv2_enabled (running instances)
   - aws_ec2_launch_template_imdsv2_required (launch templates)
   BOTH KEPT - different resource types

3. Security Groups - Port Checks:
   - aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22 (SSH)
   - aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_3389 (RDP)
   - aws_ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_3306 (MySQL)
   ALL KEPT - different ports = different compliance requirements!
```

**Template for All CSPs:**
```
For Compute:

KEEP SEPARATE:
- Account-level settings vs resource-level
- Running instances vs templates/images
- Different ports (each port is a distinct check)
- Instance vs volume vs snapshot encryption

CONSOLIDATE:
- Different names for same encryption check
- Generic "encryption" if you have specific types
```

---

#### Step 3.3: Storage (S3/Blob/Object Storage)

**AWS Consolidations:**
```
1. Encryption:
   - aws_s3_bucket_encryption_enabled (any encryption) ✅ KEPT
   - aws_s3_bucket_kms_encryption (KMS specific) ✅ KEPT
   - aws_s3_bucket_default_encryption ❌ REMOVED (duplicate)

2. Versioning:
   - aws_s3_bucket_versioning_enabled ✅ KEPT
   - aws_s3_bucket_object_versioning ❌ REMOVED (misleading name)

3. Replication:
   - aws_s3_bucket_replication_enabled ✅ KEPT (covers CRR & SRR)
   - aws_s3_bucket_cross_region_replication ❌ REMOVED (specific case)

4. Logging:
   - aws_s3_bucket_server_access_logging_enabled ✅ KEPT
   - aws_s3_bucket_logging_enabled ❌ REMOVED (duplicate)
```

**Template for All CSPs:**
```
For Storage:

KEEP:
- General + Specific encryption (any + KMS/CMK)
- Account-level + bucket-level public access
- Versioning (one check)
- Replication (generic covering all types)
- Lifecycle (one check)

CONSOLIDATE:
- "default_encryption" → "encryption_enabled"
- "cross_region_replication" → "replication_enabled"
```

---

#### Step 3.4: Database (RDS/SQL)

**AWS Consolidations:**
```
1. Encryption:
   - aws_rds_instance_storage_encrypted ✅ KEPT
   - aws_rds_cluster_storage_encrypted ✅ KEPT
   - aws_rds_instance_encryption_at_rest_enabled ❌ REMOVED
   - aws_rds_storage_encrypted ❌ REMOVED

2. Backup:
   - aws_rds_instance_backup_enabled ✅ KEPT
   - aws_rds_backup_retention_period ✅ KEPT (checks >= 7 days)
   - aws_rds_backup_enabled ❌ REMOVED

3. Multi-AZ:
   - aws_rds_instance_multi_az ✅ KEPT
   - aws_rds_cluster_multi_az ✅ KEPT
   - aws_rds_multi_az_enabled ❌ REMOVED
```

**Template for All CSPs:**
```
For Databases:

KEEP SEPARATE:
- Instance vs Cluster (different resources)
- Encryption enabled vs retention period
- Backup enabled vs backup retention >= N days

CONSOLIDATE:
- Generic names → Specific to resource type
- "enabled" + "compliance_check" → Keep "enabled"
```

---

#### Step 3.5: Logging & Monitoring

**AWS Consolidations:**
```
1. CloudTrail Enabled:
   - aws_cloudtrail_multi_region_enabled ✅ KEPT
   - aws_cloudtrail_enabled ❌ REMOVED
   - aws_cloudtrail_trail_multi_region_logging_enabled ❌ REMOVED

2. CloudWatch Integration:
   - aws_cloudtrail_cloudwatch_logging_enabled ✅ KEPT
   - aws_cloudtrail_cloudwatch_logs_enabled ❌ REMOVED

3. KMS Encryption:
   - aws_cloudtrail_kms_encryption_enabled ✅ KEPT
   - aws_cloudtrail_trail_encryption_at_rest_kms_enabled ❌ REMOVED
   - aws_cloudtrail_trail_sse_kms_encryption_at_rest_enabled ❌ REMOVED

4. Log Validation:
   - aws_cloudtrail_log_file_validation_enabled ✅ KEPT
   - aws_cloudtrail_trail_log_file_validation_check ❌ REMOVED
   - aws_cloudtrail_trail_log_file_validation_status_check ❌ REMOVED
```

**Template for All CSPs:**
```
For Logging:

KEEP:
- Multi-region/global logging (most comprehensive)
- CloudWatch/monitoring integration (one check)
- KMS encryption (one check)
- Log validation (one check)

CONSOLIDATE:
- *_enabled, *_check, *_status_check → Keep *_enabled
- Multi-region covers single-region
- trail_* prefix redundant if service is clear
```

---

#### Step 3.6: Networking (VPC/Security Groups)

**AWS Consolidations:**
```
1. Flow Logs:
   - aws_vpc_flow_logs_enabled ✅ KEPT
   - aws_ec2_vpc_flow_logging_reject_enabled ✅ KEPT (more strict)
   BOTH KEPT - different levels

2. Default Security Group:
   - aws_ec2_securitygroup_default_restrict_traffic ✅ KEPT
   - aws_ec2_default_security_group_restriction_check ❌ REMOVED
   - aws_ec2_securitygroup_default_restricted ❌ REMOVED

3. SSH/RDP Access:
   - aws_ec2_securitygroup_ssh_restricted ✅ KEPT
   - aws_ec2_securitygroup_rdp_restricted ✅ KEPT
   - aws_ec2_security_group_ingress_ssh_rdp_restricted ❌ REMOVED
```

**Template for All CSPs:**
```
For Networking:

KEEP SEPARATE:
- SSH vs RDP (different protocols)
- All port-specific checks (each is distinct)
- Flow logs general vs reject-only

CONSOLIDATE:
- Multiple names for default SG restriction
- Generic ingress checks if you have protocol-specific
```

---

### **PHASE 4: Naming Standardization** (Week 4)

#### Step 4.1: Establish Naming Conventions

**AWS Pattern:**
```
{csp}_{service}_{resource}_{attribute}_{state}

Examples:
✅ GOOD:
- aws_s3_bucket_encryption_enabled
- aws_ec2_instance_imdsv2_enabled
- aws_rds_cluster_multi_az_enabled

❌ BAD:
- aws_s3_bucket_encryption_check
- aws_ec2_imdsv2_required_check
- aws_rds_is_multi_az_enabled
```

**Suffix Priority:**
```
1. _enabled (preferred for boolean checks)
2. _encrypted (for encryption state)
3. _configured (for complex setup)
4. Avoid: _check, _status_check, _compliance_check
```

---

#### Step 4.2: Service Name Consistency

**AWS Examples:**
```
✅ GOOD service names:
- ec2 (not compute)
- rds (not database)
- s3 (not storage)
- lambda (not function, not awslambda)

✅ For other CSPs:
- Azure: use official service names (storage, compute, sql)
- GCP: use official service names (gce, gcs, cloudsql)
- K8s: use resource types (pod, deployment, service)
```

---

### **PHASE 5: Validation & Quality Checks**

#### Step 5.1: No Duplicates Check
```bash
# Extract all functions and check for duplicates
cat aws_functions_final_deduplicated.json | \
  jq -r '.[] | .[]' | sort | uniq -d

# Should return: (empty)
```

#### Step 5.2: Proper Categorization
```bash
# All functions should have proper prefix
cat aws_functions_final_deduplicated.json | \
  jq -r '.[] | .[]' | grep -v "^aws_"

# Should return: (empty)
```

#### Step 5.3: CSV-JSON Consistency
```python
# Verify all functions in CSV exist in JSON
csv_functions = extract_from_csv("aws_checks")
json_functions = extract_from_json()

missing = csv_functions - json_functions
# Should return: (empty set)
```

---

## 🔄 Replication Steps for Other CSPs

### For Azure, GCP, Oracle, IBM, Alicloud, Kubernetes:

1. **Extract Current Functions**
   ```bash
   # Get all functions for target CSP
   grep "{csp}_checks" consolidated_compliance_rules_FINAL.csv | \
     cut -d',' -f11 | tr ';' '\n' | sort -u > {csp}_functions_current.txt
   ```

2. **Apply Phase 1 Fixes**
   - Search for missing prefixes
   - Identify concatenated functions
   - Merge duplicate service names

3. **Apply Phase 2 Analysis**
   - Group by service
   - Identify functional duplicates
   - Use AWS patterns as template

4. **Apply Phase 3 Service-Specific**
   - Follow AWS templates for each service type
   - Adapt to CSP-specific naming

5. **Apply Phase 4 Standardization**
   - Use consistent naming pattern
   - Standardize suffixes

6. **Validate with Phase 5**
   - Run all quality checks
   - Verify no regressions

---

## 📊 Expected Results Per CSP

| CSP | Est. Current | Est. After | Expected Reduction |
|-----|-------------|------------|-------------------|
| **AWS** | 629 | 524 | -16.7% ✅ DONE |
| **Azure** | ~450 | ~380 | -15% |
| **GCP** | ~420 | ~350 | -16% |
| **Oracle** | ~180 | ~150 | -17% |
| **IBM** | ~160 | ~135 | -16% |
| **Alicloud** | ~140 | ~120 | -14% |
| **Kubernetes** | ~80 | ~70 | -12% |

---

## 🎯 Success Criteria

For each CSP, confirm:

✅ No functions with missing CSP prefix  
✅ No concatenated functions  
✅ No duplicate service names  
✅ No name-based duplicates  
✅ No functional duplicates (same job)  
✅ Consistent naming pattern  
✅ Proper service categorization  
✅ CSV and JSON in sync  
✅ Quality score >= 4.0/5  

---

## 📝 Documentation to Create Per CSP

1. `{CSP}_FUNCTIONS_EXPERT_REVIEW.md` - Analysis and recommendations
2. `{CSP}_FUNCTIONS_CONSOLIDATION_REPORT.md` - All decisions documented
3. `{csp}_functions_final_deduplicated.json` - Clean function list
4. Update `consolidated_compliance_rules_FINAL.csv` - Apply all changes

---

## 💡 Key Learnings from AWS

1. **Don't consolidate by name alone** - Analyze what the function DOES
2. **Keep granularity when needed** - Different ports are different checks
3. **Respect resource types** - Instance vs Cluster are different
4. **Account vs Resource** - Different control planes, keep both
5. **General + Specific** - Keep both "any encryption" and "KMS encryption"
6. **Multi-region covers single-region** - One check is sufficient
7. **Port-specific checks matter** - Each port is a unique compliance requirement

---

*Apply this process to each CSP sequentially for best results.*  
*Estimated time per CSP: 2-3 weeks*  
*Total time for all 6 remaining CSPs: 12-18 weeks*

