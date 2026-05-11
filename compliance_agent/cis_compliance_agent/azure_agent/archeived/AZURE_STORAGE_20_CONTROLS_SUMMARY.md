# CIS Microsoft Azure Storage Services Benchmark - 20 Controls Analysis

**Source:** CIS MICROSOFT AZURE STORAGE SERVICES BENCHMARK V1.0.0  
**Generated:** 2025-10-26  
**Agent:** Enterprise CSPM Compliance Audit Agent

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Controls Analyzed** | 20 |
| **Manual Approach** | 5 (25%) |
| **Automated Approach** | 15 (75%) |
| **Success Rate** | 100% |

**Key Finding:** Unlike AKS controls (100% Manual), Azure Storage controls are **75% Automated** because they use Azure Resource Manager APIs that directly expose storage account configurations.

---

## Control Mapping Table

| Control ID | Title | Approach | Program Name |
|------------|-------|----------|--------------|
| **2.1.1.1** | Allowed Protocols for SAS | Manual | - |
| **2.1.1.2** | SAS Token Expiry (1 hour) | Manual | - |
| **2.1.1.3** | Stored Access Policies | Manual | - |
| **2.1.2.1.1** | Critical Data Encryption (Blob) | Manual | - |
| **2.1.2.2.1** | Critical Data Encryption (File) | Manual | - |
| **2.2.1.1** | Public Network Access Disabled | **Automated** | `azure_storage_account_public_network_access_disabled` |
| **2.2.1.2** | Network Access Rules (Deny by Default) | **Automated** | `azure_storage_account_network_access_rules_deny_by_default` |
| **2.2.2.1** | Private Endpoints Used | **Automated** | `azure_storage_private_endpoint_enabled` |
| **4.1** | Lustre File System Key Encryption | **Automated** | `azure_lustre_file_system_key_encryption_audit` |
| **5.1.1** | Backup Vault Soft Delete | **Automated** | `azure_dataprotection_backup_vault_soft_delete_enabled` |
| **5.1.2** | Backup Vault Immutability | **Automated** | `azure_backup_digital_vault_immutability_enabled` |
| **5.1.3** | Backup Vault CMK Encryption | **Automated** | `azure_backup_vaults_encryption_cmk_enabled` |
| **5.1.4** | Infrastructure Encryption (Backup) | **Automated** | `azure_dataprotection_backup_vault_infrastructure_encryption_enabled` |
| **5.1.5** | Cross Region Restore | **Automated** | `azure_backup_vault_cross_region_restore_enabled` |
| **5.1.6** | Cross Subscription Restore Disabled | **Automated** | `azure_dataprotection_backup_vault_cross_subscription_restore_disabled` |
| **5.2.1** | Recovery Services Soft Delete | **Automated** | `azure_backup_recovery_services_vault_soft_delete_enabled` |
| **5.2.2** | Recovery Services Immutability | **Automated** | `azure_recovery_services_vault_immutability_enabled` |
| **5.2.3** | Recovery Services CMK Encryption | **Automated** | `azure_recovery_services_vault_encryption_customer_managed_keys_enabled` |
| **5.2.4** | Infrastructure Encryption (Recovery) | **Automated** | `azure_recovery_services_vault_infrastructure_encryption_enabled` |
| **5.2.5** | Recovery Services Public Network Disabled | **Automated** | `azure_backup_recovery_services_vault_public_network_access_disabled` |

---

## Key Findings

### 1. **Why 75% Automated?**

**Automated Controls** check configurations exposed via Azure Resource Manager APIs:
- ✅ Storage Account properties (`networkAcls`, `publicNetworkAccess`)
- ✅ Backup Vault settings (`softDelete`, `immutability`, `encryption`)
- ✅ Recovery Services configuration
- ✅ Private Endpoint status
- ✅ Network access rules

**Manual Controls** require human judgment:
- ❌ SAS token expiry policies (not queryable via API)
- ❌ SAS token review/validation
- ❌ Data encryption verification (content-level)
- ❌ Access policy assessment

### 2. **Comparison: AKS vs Storage**

| Aspect | AKS Controls | Storage Controls |
|--------|--------------|------------------|
| **Manual** | 100% (10/10) | 25% (5/20) |
| **Automated** | 0% (0/10) | 75% (15/20) |
| **Reason** | Node-level file access required | ARM API exposes configurations |
| **Access Method** | SSH to worker nodes | REST API queries |

### 3. **Program Name Patterns**

**Service Patterns:**
```
azure_storage_<resource>_<security_intent>
azure_backup_<resource>_<security_intent>
azure_recovery_services_<resource>_<security_intent>
azure_dataprotection_<resource>_<security_intent>
```

**Examples:**
- `azure_storage_account_public_network_access_disabled`
- `azure_backup_vault_cross_region_restore_enabled`
- `azure_recovery_services_vault_immutability_enabled`

---

## Detailed Examples

### Example 1: Automated Control

**Control 2.2.1.1:** Ensure public network access is Disabled

**Approach:** Automated  
**Program Name:** `azure_storage_account_public_network_access_disabled`

**Automation Details:**
- **APIs:**
  - `GET /subscriptions/{id}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{account}`
  - `GET /subscriptions/{id}/providers/Microsoft.Storage/elasticSans/{san}`
  - `GET /subscriptions/{id}/providers/Microsoft.RecoveryServices/vaults/{vault}`

- **Properties to Validate:**
  - Storage Account: `networkAcls.defaultAction == "Deny"`
  - Elastic SAN: `publicNetworkAccess == "Disabled"`
  - Recovery Vault: `publicNetworkAccess == "Disabled"`

- **CLI Example:**
  ```bash
  az storage account show --name {account} --resource-group {rg} \
    --query "networkAcls.defaultAction"
  ```

- **Pass/Fail:**
  - **Pass:** `defaultAction = "Deny"`
  - **Fail:** `defaultAction = "Allow"` or not set

---

### Example 2: Manual Control

**Control 2.1.1.2:** Ensure SAS tokens expire within an hour

**Approach:** Manual

**Manual Steps:**
1. Navigate to Azure Portal → Storage Accounts
2. Select the storage account
3. Click "Shared access signature" in left menu
4. Review expiry time for each SAS token
5. Verify expiration ≤ 1 hour
6. Document any non-compliant tokens

**Why Manual:**
- SAS token policies are not queryable via ARM APIs
- Requires human review of token configurations
- Expiry validation needs policy interpretation

---

## Architecture Insights

### Why Storage is More Automatable

```
┌────────────────────────────────────────────────┐
│     Azure Resource Manager (ARM)               │
│  ✅ Storage Account Configurations              │
│  ✅ Network Rules, Encryption, Access           │
│  ✅ Backup Vault Settings                       │
│  ✅ All exposed via REST APIs                   │
└────────────────────────────────────────────────┘
                     │
            ┌────────┴────────┐
            │                 │
    ┌───────▼──────┐   ┌─────▼────────┐
    │  Storage     │   │   Backup     │
    │  Accounts    │   │   Vaults     │
    │  (API-based) │   │  (API-based) │
    └──────────────┘   └──────────────┘
```

**vs AKS Worker Nodes:**

```
┌────────────────────────────────────────────────┐
│     Azure Resource Manager (ARM)               │
│  ✅ AKS Cluster Configuration                   │
│  ❌ Worker Node File System (Not Exposed)       │
└────────────────────────────────────────────────┘
                     │
            ┌────────┴────────┐
            │                 │
    ┌───────▼──────┐   ┌─────▼────────┐
    │  Control     │   │   Worker     │
    │  Plane       │   │   Nodes      │
    │  (Managed)   │   │  (Need SSH)  │
    └──────────────┘   └──────────────┘
```

---

## Implementation Guide

### For Automated Controls:

**Use Azure CLI/PowerShell/SDK:**

```bash
# Example: Check public network access
az storage account list --query "[].{name:name, rg:resourceGroup}" -o table | \
while read name rg; do
  access=$(az storage account show --name $name --resource-group $rg \
    --query "networkAcls.defaultAction" -o tsv)
  if [ "$access" != "Deny" ]; then
    echo "FAIL: $name - Public access allowed"
  fi
done
```

**Or Use Azure Resource Graph:**

```kusto
Resources
| where type == "microsoft.storage/storageaccounts"
| extend publicAccess = properties.networkAcls.defaultAction
| where publicAccess != "Deny"
| project name, resourceGroup, publicAccess
```

### For Manual Controls:

1. **SAS Token Review:** Implement organizational policy
2. **Regular Audits:** Schedule quarterly reviews
3. **Documentation:** Maintain audit trail
4. **Automation Workarounds:**
   - Use Azure Policy to enforce SAS expiry
   - Implement custom monitoring scripts
   - Log Analytics queries for SAS usage

---

## Comparison Summary

| Category | AKS | Storage |
|----------|-----|---------|
| **Automated** | 0% | 75% |
| **Manual** | 100% | 25% |
| **Primary Reason** | Node file system access | ARM API exposure |
| **Check Method** | SSH + file inspection | REST API queries |
| **Typical Tools** | kubectl exec, SSH | az CLI, PowerShell, SDKs |
| **CSPM Friendly** | ❌ Requires agents | ✅ Native API support |

---

## Files Generated

1. **`storage_controls_20.csv`** - Input CSV with 20 Storage controls
2. **`output_storage/*.json`** - 20 JSON files with detailed audit approaches
3. **`AZURE_STORAGE_20_CONTROLS_SUMMARY.md`** - This document

---

## Next Steps

1. ✅ Implement automated checks using Azure Resource Graph or CLI
2. ✅ Create Azure Policy definitions for enforceable controls
3. ✅ Set up continuous compliance monitoring
4. ✅ Integrate program names into CSPM tool
5. ✅ Schedule manual reviews for the 5 manual controls

---

**Conclusion:** Azure Storage controls are significantly more automatable (75%) than AKS controls (0%) because Azure Resource Manager APIs directly expose storage configurations, making them ideal candidates for programmatic CSPM auditing.

