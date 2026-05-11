# Quick Start Guide - K8s Function Generation

## Step-by-Step: Process Your First Framework

### 1. Test with GDPR (Smallest Framework - 3 controls)

```bash
cd /Users/apple/Desktop/compliance_Database/compliance_agent/k8s_function_agent

# Ensure API key is set
echo $OPENAI_API_KEY  # Should show your key

# Run GDPR
./run_framework.sh GDPR ../gdpr/GDPR_controls_with_checks.csv
```

**Expected Output:**
```
==========================================================================
K8s Function Generation Pipeline
Framework: GDPR
Input CSV: ../gdpr/GDPR_controls_with_checks.csv
==========================================================================

Step 1: Generating K8s functions...
[1/3] Processing: article_25
[2/3] Processing: article_30
[3/3] Processing: article_32

Step 2: Reviewing K8s functions...
[1/3] Reviewing: article_25.json
[2/3] Reviewing: article_30.json
[3/3] Reviewing: article_32.json

Step 3: Updating CSV...
✅ Complete!
```

### 2. Check the Results

```bash
# View summary
cat output_GDPR_*/step3_final/GDPR_K8S_SUMMARY.md

# Check CSV
head -20 output_GDPR_*/step3_final/GDPR_controls_with_k8s.csv

# View detailed JSON (optional)
ls output_GDPR_*/step2_review/
cat output_GDPR_*/step2_review/article_25.json | jq .
```

### 3. Process More Frameworks

Once GDPR works, continue with others:

```bash
# NIST 800-171 (~50 controls, ~25 min)
./run_framework.sh NIST_800_171 ../nist_800_171/NIST_800-171_R2_controls_with_checks.csv

# HIPAA (~30 controls, ~15 min)
./run_framework.sh HIPAA ../hipaa/HIPAA_controls_with_checks.csv

# SOC2 (~25 controls)
./run_framework.sh SOC2 ../soc2/SOC2_controls_with_checks.csv

# ISO27001
./run_framework.sh ISO27001 ../iso27001-2022/ISO27001_2022_controls_with_checks.csv

# PCI DSS
./run_framework.sh PCI_DSS ../pci_compliance_agent/PCI_controls_with_checks.csv

# FedRAMP
./run_framework.sh FedRAMP ../FedRamp/FedRAMP_controls_with_checks.csv

# NIST 800-53
./run_framework.sh NIST_800_53 ../nist_complaince_agent/NIST_controls_with_checks.csv

# CISA CE
./run_framework.sh CISA_CE ../cisa_ce/CISA_CE_controls_with_checks.csv

# RBI Bank
./run_framework.sh RBI_BANK ../rbi_bank/RBI_BANK_controls_with_checks.csv

# RBI NBFC
./run_framework.sh RBI_NBFC ../rbi_nbfc/RBI_NBFC_controls_with_checks.csv

# Canada PBMM
./run_framework.sh CANADA_PBMM ../canada_pbmm/CANADA_PBMM_controls_with_checks.csv
```

## Estimated Processing Times

| Framework | Controls | Time Estimate |
|-----------|----------|---------------|
| GDPR | 3 | ~2 min |
| RBI Bank/NBFC | ~10 | ~5 min |
| CISA CE | ~20 | ~10 min |
| SOC2 | ~25 | ~15 min |
| HIPAA | ~30 | ~15 min |
| ISO27001 | ~40 | ~20 min |
| NIST 800-171 | ~50 | ~25 min |
| PCI DSS | ~200 | ~90 min |
| FedRAMP | ~400 | ~180 min |
| NIST 800-53 | ~500 | ~240 min |

## What Gets Generated

For each control:

1. **Step 1 JSON** - Initial K8s function proposals
```json
{
  "control_id": "article_25",
  "k8s_applicable": true,
  "k8s_functions": [
    "k8s_rbac_least_privilege_enforcement",
    "k8s_audit_logging_enabled",
    "k8s_secret_encryption_at_rest_enabled"
  ],
  "reasoning": "Maps IAM/logging/encryption to K8s equivalents",
  "confidence": "HIGH"
}
```

2. **Step 2 JSON** - Reviewed and validated
```json
{
  "review_status": "APPROVE_WITH_CHANGES",
  "k8s_applicable": true,
  "validated_functions": [
    "k8s_rbac_least_privilege_enforcement",
    "k8s_audit_logging_enabled",
    "k8s_secret_encryption_at_rest_enabled",
    "k8s_pod_security_context_non_root"
  ],
  "changes_made": ["Added pod security check"],
  "review_notes": "Functions accurate, added pod security for completeness"
}
```

3. **Final CSV** - Updated with K8s_Checks column
```csv
Article_ID,Title,...,K8s_Checks,Total_Checks
article_25,Data protection by design,...,k8s_rbac_least_privilege_enforcement; k8s_audit_logging_enabled; k8s_secret_encryption_at_rest_enabled; k8s_pod_security_context_non_root,148
```

## Troubleshooting

### "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### "Connection error"
- Check internet connection
- Verify API key is valid
- Script will auto-retry up to 4 times

### "CSV file not found"
- Check the path relative to `compliance_agent/` directory
- Use tab completion to verify path

### Want to reprocess?
Each run creates a new timestamped directory, so you can safely rerun without overwriting previous results.

## Review Checklist

After processing each framework:

- [ ] Check Step 1 has JSON files for all controls
- [ ] Check Step 2 shows review statuses
- [ ] Verify CSV has K8s_Checks column
- [ ] Review summary report for reasonable mappings
- [ ] Spot-check a few function names for accuracy

## Next Framework Decision

**Start with GDPR** - smallest framework, perfect for validating the setup works.

**Then do one of each size**:
1. Small (GDPR) ✓
2. Medium (HIPAA or SOC2)
3. Large (NIST 800-171 or ISO27001)
4. Very Large (PCI DSS or FedRAMP)

This ensures the process works at all scales before committing to process everything.

