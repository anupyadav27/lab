# Azure Functions Improvement Specification

**CSP:** Azure  
**Priority:** #1 (Largest after AWS)  
**Estimated Functions:** ~450  
**Target Functions:** ~380 (-15%)  
**Timeline:** 2-3 weeks

---

## 📋 Phase-by-Phase Plan

### **PHASE 1: Fix Critical Issues** (Week 1, Days 1-3)

#### Step 1.1: Fix Missing Prefix
**Action:** Search for functions without `azure_` prefix  
**AWS Example:** Fixed 530 functions missing `aws_` prefix  
**Expected:** 0-10 functions to fix

```bash
# Find functions without azure_ prefix
grep "^[a-z_]*," CSV | grep azure_checks column
```

**Fix Pattern:**
```
servicename_function → azure_servicename_function
```

---

#### Step 1.2: Split Concatenated Functions  
**Action:** Find comma-separated functions in single field  
**AWS Example:** Split "s3_encryption, rds_encryption" → separate functions  
**Expected:** 0-5 instances

**Fix Pattern:**
```
"func1, func2, func3" → "func1; func2; func3"
```

---

#### Step 1.3: Merge Duplicate Service Names
**Action:** Identify service name variations  
**AWS Example:** `awslambda` + `lambda` → `lambda`  
**Expected Azure Cases:**
- `azurefunctions` vs `functions`
- `azuresql` vs `sql`
- `azureactivedirectory` vs `activedirectory` vs `ad`

**Decision Rules:**
- Use shorter, official Azure service name
- Merge all functions under canonical name
- Update CSV

---

#### Step 1.4: Remove Name-Based Duplicates
**Action:** Find same function with different suffixes  
**AWS Example:** `_encryption` vs `_encrypted` → keep `_encrypted`

**Azure Patterns to Check:**
```
*_check vs *_enabled
*_status_check vs *_enabled  
*_is_enabled vs *_enabled
*_compliance_check vs *_enabled
```

**Consolidation Rule:** Keep `_enabled` (shortest, clearest)

---

### **PHASE 2: Functional Analysis** (Week 1, Days 4-7)

#### Step 2.1: Storage Account Functions
**AWS Template Applied:** S3 encryption, public access, versioning

**Azure Services:** `storage`, `blob`, `files`, `queue`, `table`

**Expected Duplicates:**
```
1. Encryption:
   - azure_storage_account_encryption_enabled (any encryption) ← KEEP
   - azure_storage_account_default_encryption ← REMOVE
   - azure_storage_account_kms_encryption (specific CMK) ← KEEP
   
2. Public Access:
   - azure_storage_account_public_access_blocked (account-level) ← KEEP
   - azure_blob_container_public_access (container-level) ← KEEP
   - azure_storage_public_access_check ← REMOVE (duplicate)

3. Versioning:
   - azure_blob_versioning_enabled ← KEEP
   - azure_storage_blob_versioning ← REMOVE (redundant naming)
```

---

#### Step 2.2: SQL Database Functions
**AWS Template Applied:** RDS encryption, backup, multi-AZ

**Azure Services:** `sql`, `sqldatabase`, `sqlserver`

**Expected Duplicates:**
```
1. Encryption:
   - azure_sql_database_transparent_data_encryption_enabled ← KEEP
   - azure_sql_tde_enabled ← REMOVE (abbreviation)
   - azure_sql_encryption_enabled ← REMOVE (generic)

2. High Availability:
   - azure_sql_database_zone_redundant ← KEEP (Azure's multi-AZ)
   - azure_sql_ha_enabled ← REMOVE (generic)

3. Backup:
   - azure_sql_database_long_term_retention_enabled ← KEEP
   - azure_sql_backup_retention_check ← REMOVE (duplicate)
```

---

#### Step 2.3: Virtual Machine Functions
**AWS Template Applied:** EC2 encryption, IMDSv2, security groups

**Azure Services:** `compute`, `vm`, `virtualmachine`

**Expected Duplicates:**
```
1. Disk Encryption:
   - azure_vm_disk_encryption_enabled (OS disk) ← KEEP
   - azure_vm_data_disk_encryption_enabled (data disks) ← KEEP
   - azure_compute_disk_encrypted ← REMOVE (less specific)

2. NSG (Network Security Groups):
   - azure_nsg_rdp_restricted ← KEEP
   - azure_nsg_ssh_restricted ← KEEP
   - azure_network_security_group_rdp_ssh_restricted ← REMOVE (combined)
   
   Note: Like AWS, keep port-specific checks separate!
```

---

#### Step 2.4: Monitor & Logging Functions
**AWS Template Applied:** CloudTrail multi-region, CloudWatch integration

**Azure Services:** `monitor`, `log`, `activitylog`, `loganalytics`

**Expected Duplicates:**
```
1. Activity Log:
   - azure_monitor_activity_log_enabled ← KEEP
   - azure_activity_log_enabled ← REMOVE (missing service prefix)
   - azure_monitor_activity_log_check ← REMOVE (_check suffix)

2. Log Analytics:
   - azure_log_analytics_workspace_retention_configured ← KEEP
   - azure_monitor_log_retention ← REMOVE (less specific)

3. Diagnostic Settings:
   - azure_monitor_diagnostic_setting_enabled ← KEEP
   - azure_diagnostic_settings_configured ← REMOVE (less specific)
```

---

### **PHASE 3: Service-Specific Deep Dive** (Week 2)

#### 3.1: Azure Active Directory (IAM equivalent)
**AWS Template:** IAM MFA, password policy, access keys

**Expected Patterns:**
```
MFA:
- azure_ad_user_mfa_enabled ← KEEP
- azure_active_directory_mfa_check ← REMOVE

Password Policy:
- azure_ad_password_policy_length_minimum ← KEEP
- azure_ad_password_policy_expiry ← KEEP
- azure_ad_password_policy_complexity ← KEEP
- azure_ad_password_policy_strong ← REMOVE (combined check)

Access Keys:
- azure_ad_service_principal_credential_expiry ← KEEP
- azure_ad_credential_rotation_90_days ← KEEP (specific)
- azure_ad_credential_rotation ← REMOVE (generic)
```

---

#### 3.2: Key Vault (Secrets Manager equivalent)
```
- azure_keyvault_secret_expiration_enabled ← KEEP
- azure_keyvault_rbac_enabled ← KEEP
- azure_key_vault_secrets_expiry ← REMOVE (redundant)
```

---

#### 3.3: Network Security
```
NSG Rules:
- Keep all port-specific checks (like AWS)
- azure_nsg_port_22_restricted (SSH) ← KEEP
- azure_nsg_port_3389_restricted (RDP) ← KEEP
- azure_nsg_port_1433_restricted (SQL) ← KEEP
- Different ports = different compliance!

VNet:
- azure_vnet_ddos_protection_enabled ← KEEP
- azure_virtual_network_ddos_enabled ← REMOVE (less specific)
```

---

### **PHASE 4: Naming Standardization** (Week 3, Days 1-2)

#### Naming Convention
```
azure_{service}_{resource}_{attribute}_{state}

Examples:
✅ GOOD:
- azure_sql_database_encryption_enabled
- azure_storage_account_public_access_blocked
- azure_vm_disk_encryption_enabled

❌ BAD:
- azure_sql_tde_enabled (abbreviation)
- azure_storage_public_check (missing resource)
- azure_vm_encrypted (missing attribute)
```

#### Service Name Standards
Use official Azure service names:
- `storage` (not azurestorage)
- `sql` (not azuresql)
- `ad` or `activedirectory` (choose one)
- `keyvault` (one word)
- `compute` or `vm` (choose one)

---

### **PHASE 5: Validation & Delivery** (Week 3, Days 3-5)

#### Deliverables
1. `azure_functions_final_deduplicated.json`
2. `AZURE_CONSOLIDATION_REPORT.md`
3. Updated `consolidated_compliance_rules_FINAL.csv`
4. `azure_consolidation_mapping.json` (for audit trail)

#### Quality Checks
```bash
# 1. No duplicates
cat azure_functions_final_deduplicated.json | jq -r '.[] | .[]' | sort | uniq -d
# Should return: (empty)

# 2. All have azure_ prefix
cat azure_functions_final_deduplicated.json | jq -r '.[] | .[]' | grep -v "^azure_"
# Should return: (empty)

# 3. CSV-JSON consistency
# All Azure functions in CSV should exist in JSON
```

---

## 📊 Expected Results

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Functions | ~450 | ~380 | -15% |
| Services | ~40 | ~35 | Consolidated |
| Quality Score | 2.5/5 | 4.0/5 | +60% |

---

## 🔑 Key Azure-Specific Considerations

1. **Azure Active Directory ≠ AWS IAM**
   - Azure AD is identity service
   - RBAC is separate authorization layer
   - Keep both AD and RBAC checks

2. **Resource Groups**
   - Azure-specific concept
   - Keep resource group governance checks

3. **Azure Policy**
   - Built-in compliance framework
   - Different from AWS Config
   - Keep policy-specific checks

4. **Naming: Storage Account vs Blob**
   - Storage Account = parent
   - Blob/Files/Queue/Table = children
   - Keep hierarchy in naming

5. **Zone Redundancy = Multi-AZ**
   - Azure term for high availability
   - Equivalent to AWS Multi-AZ

---

## 💡 Decision Framework

When uncertain if functions are duplicates:

**KEEP BOTH if:**
- Different resource types (database vs server)
- Different levels (account vs resource)
- Different aspects (at-rest vs in-transit)
- Different ports (like AWS)

**CONSOLIDATE if:**
- Same check, different suffix (_check vs _enabled)
- Generic vs specific (keep specific)
- Abbreviation vs full name (keep full)
- Multi-region covers single-region

---

## 📅 Timeline

| Phase | Days | Deliverable |
|-------|------|-------------|
| Phase 1 | 3 | Critical issues fixed |
| Phase 2 | 4 | Functional analysis complete |
| Phase 3 | 5 | Service templates applied |
| Phase 4 | 2 | Naming standardized |
| Phase 5 | 3 | Final validation & delivery |
| **Total** | **17 days** | **~3 weeks** |

---

## ✅ Success Criteria

- [ ] No functions missing `azure_` prefix
- [ ] No concatenated functions
- [ ] No duplicate service names
- [ ] No name-based duplicates
- [ ] Functional duplicates consolidated
- [ ] Naming conventions followed
- [ ] CSV and JSON in sync
- [ ] Quality score >= 4.0/5
- [ ] Documentation complete

---

**STATUS:** Ready to execute  
**NEXT ACTION:** Begin Phase 1 - analyze current Azure functions

*This spec follows the proven AWS methodology and can be replicated for GCP, Oracle, IBM, Alicloud, and Kubernetes.*

