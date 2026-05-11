# Cloud Provider Correction Methodology

**Purpose:** Systematic approach to clean and consolidate cloud provider functions in the compliance CSV

**Status:** AWS ✅ | Azure ✅ | GCP ⏳ | OCI ⏳ | IBM ⏳ | Alicloud ⏳ | K8s ⏳

---

## Overview

This methodology was developed and proven through AWS and Azure corrections. It systematically removes cross-cloud terminology contamination, standardizes naming, and consolidates functional duplicates.

---

## The 5-Phase Approach

### Phase 1: Initial Analysis & Pattern Discovery
**Duration:** 1-2 hours  
**Goal:** Identify what's wrong with the current functions

#### Steps:

1. **Extract all unique functions for the cloud provider**
   ```bash
   # Create analysis script
   python3 analyze_[provider]_functions.py
   ```

2. **Analyze function prefixes and patterns**
   - Group by service prefix
   - Count occurrences
   - Identify obvious issues

3. **Look for cross-cloud contamination**
   - AWS terminology in other clouds (cloudwatch, ebs, s3, bucket, ssm, rds)
   - Inconsistent service names
   - Verbose vs abbreviated names

4. **Document initial findings**
   - Create `[PROVIDER]_PHASE1_FINDINGS.md`
   - List top issues by category
   - Estimate number of functions affected

#### Output:
- List of 5-10 major patterns/issues
- Estimated consolidation count (rough)
- Understanding of provider-specific terminology

---

### Phase 2: Functional Analysis & Categorization
**Duration:** 2-3 hours  
**Goal:** Deep dive into what each function does and identify true duplicates

#### Steps:

1. **Categorize by duplicate pattern type**
   - Cross-cloud terminology (AWS terms in other clouds)
   - Service name variations (verbose vs short)
   - Suffix variations (_enabled, _check, _status_check, _is_enabled)
   - Encryption variations (_encrypted, _encryption_enabled, _default_encryption)
   - Logging variations (_logging_enabled, _logs_enabled, _server_access_logging)
   - Resource terminology (instance vs database, bucket vs account)

2. **Group by service**
   - IAM/Identity
   - Compute/VMs
   - Storage
   - Database
   - Networking
   - Monitoring/Logging
   - Security

3. **Identify functional duplicates**
   - Functions that check the same thing
   - Multiple functions that should be parameters
   - Redundant checks

4. **Document service-specific patterns**
   - Create `[PROVIDER]_PHASE2_COMPLETE.md`
   - List consolidations by category
   - Estimate total reduction

#### Output:
- 8-10 duplicate pattern categories
- List of 20-30 high-priority consolidations
- Service-specific insights

---

### Phase 3: Service-Specific Deep Dive
**Duration:** 3-4 hours  
**Goal:** Analyze each major service individually for consistency

#### Steps:

1. **Top 10 services by function count**
   - Extract all functions for each service
   - Analyze naming patterns within service
   - Identify service-specific issues

2. **For each major service, document:**
   - **Current naming patterns** (what exists now)
   - **Issues found** (inconsistencies, AWS terms, etc.)
   - **Correct terminology** (what it should be)
   - **Consolidations needed** (specific mappings)

3. **Cross-service consistency check**
   - Are similar checks named similarly across services?
   - Are encryption checks consistent?
   - Are logging checks consistent?

4. **Create expanded consolidation mapping**
   - Document all consolidations (50-100+)
   - Create JSON mapping file

#### Output:
- `[PROVIDER]_PHASE3_COMPLETE.md`
- Detailed service analysis (top 10 services)
- Complete consolidation mapping (100+ entries typically)

---

### Phase 4: Apply Core Consolidations
**Duration:** 1 hour  
**Goal:** Apply the main consolidation mapping to CSV

#### Steps:

1. **Create consolidation mapping JSON**
   ```json
   {
     "metadata": {
       "csp": "ProviderName",
       "phase": "3_to_4",
       "date": "YYYY-MM-DD",
       "total_consolidations": 45,
       "status": "ready_for_application"
     },
     "consolidations": {
       "old_function_name_1": "new_function_name_1",
       "old_function_name_2": "new_function_name_2",
       ...
     }
   }
   ```

2. **Create application script**
   ```python
   # [provider]_phase4_apply_consolidations.py
   # - Read CSV
   # - For each row, check [provider]_checks column
   # - Apply mapping
   # - Remove duplicates
   # - Update total_checks count
   # - Write back to CSV
   ```

3. **Run the script**
   ```bash
   python3 [provider]_phase4_apply_consolidations.py
   ```

4. **Generate report**
   - How many rows updated
   - How many replacements made
   - Top 20 most common replacements

#### Output:
- Updated CSV
- `[provider]_phase4_consolidation_report.json`
- Backup of CSV (optional)

---

### Phase 5: Final Cleanup & Verification
**Duration:** 1 hour  
**Goal:** Catch any missed functions and verify completeness

#### Steps:

1. **Re-run analysis script**
   ```bash
   python3 analyze_[provider]_functions.py
   ```

2. **Check for remaining issues**
   - Any AWS terminology remaining?
   - Any inconsistent patterns?
   - Any missed consolidations?

3. **Create final cleanup mapping**
   - Document 10-20 additional fixes
   - Often catches edge cases from Phase 4

4. **Apply final fixes**
   ```python
   # [provider]_phase5_final_cleanup.py
   # Apply remaining consolidations
   ```

5. **Final verification**
   - Run analysis again
   - Should show 0 functions needing consolidation

6. **Generate completion documentation**
   - `[PROVIDER]_CORRECTIONS_COMPLETE.md`
   - Summary statistics
   - Before/after comparison

#### Output:
- Fully cleaned CSV
- `[provider]_phase5_final_cleanup_report.json`
- Completion documentation
- Verification showing 0 issues remaining

---

## Common Patterns to Look For

### 1. Cross-Cloud Terminology Contamination

**AWS terms that appear in other clouds:**
- `cloudwatch` → should be provider's monitoring service
- `s3` / `bucket` → should be provider's object storage term
- `ebs` / `volume` → should be provider's disk/block storage term
- `ec2` / `instance` → should be provider's compute term
- `vpc` → should be provider's network term
- `rds` / `instance` → should be provider's database term
- `ssm` → should be provider's automation/management term
- `iam` → might be provider-specific identity service
- `lambda` → should be provider's functions/serverless term
- `cloudtrail` → should be provider's audit log term

### 2. Service Name Issues

**Common problems:**
- Too verbose: `azure_active_directory_*` → `azure_ad_*`
- Inconsistent abbreviations
- Mixed naming conventions

### 3. Suffix Variations

**Multiple suffixes for same check:**
- `_enabled`, `_is_enabled`, `_check`, `_status_check`
- Pick ONE standard (usually `_enabled`)

### 4. Encryption Variations

**Common patterns:**
- `_encrypted`, `_encryption_enabled`, `_default_encryption`, `_encryption_at_rest_enabled`, `_storage_encrypted`
- Consolidate to: `_encryption_enabled` or `_encryption_at_rest_enabled`

### 5. Logging Variations

**Common patterns:**
- `_logging_enabled`, `_logs_enabled`, `_server_access_logging_enabled`, `_log_enabled`
- Consolidate to: `_logging_enabled`

### 6. Resource Terminology

**Use correct provider terminology:**
- AWS: instance, bucket, volume
- Azure: database, account, disk
- GCP: instance, bucket, disk
- Oracle: instance, bucket, block volume
- Each provider has their own terms!

---

## Scripts Template

### Analysis Script Template

```python
#!/usr/bin/env python3
"""
Analyze [PROVIDER] Functions - Find issues and consolidation opportunities
"""
import csv
from collections import defaultdict

CSV_FILE = "rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
PROVIDER_COLUMN = "[provider]_checks"  # e.g., "gcp_checks"

print("=" * 80)
print("ANALYZING [PROVIDER] FUNCTIONS")
print("=" * 80)

# Extract all unique functions
functions = set()
function_counts = defaultdict(int)

with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        checks = row.get(PROVIDER_COLUMN, '')
        if checks and checks != 'NA':
            for func in checks.split(';'):
                func = func.strip()
                if func:
                    functions.add(func)
                    function_counts[func] += 1

print(f"\nTotal unique [PROVIDER] functions: {len(functions)}")
print()

# Group by prefix
prefixes = defaultdict(list)
for func in sorted(functions):
    parts = func.split('_')
    if len(parts) >= 2:
        prefix = parts[0] + '_' + parts[1]  # e.g., "gcp_compute"
        prefixes[prefix].append((func, function_counts[func]))

# Display by service
print("=" * 80)
print("FUNCTIONS BY SERVICE PREFIX")
print("=" * 80)
print()

for prefix in sorted(prefixes.keys()):
    funcs = prefixes[prefix]
    print(f"{prefix.upper().replace('_', ' ')} ({len(funcs)} functions):")
    print("-" * 80)
    for func, count in sorted(funcs, key=lambda x: (-x[1], x[0]))[:10]:
        print(f"  {count:3d}x  {func}")
    if len(funcs) > 10:
        print(f"  ... and {len(funcs) - 10} more")
    print()

# Look for issues
print("=" * 80)
print("POTENTIAL ISSUES TO INVESTIGATE")
print("=" * 80)
print()

issues = []

# Check for AWS terminology
aws_terms = ['cloudwatch', 'ebs', 's3', 'bucket', 'ssm', 'rds', 'ec2', 'vpc', 'lambda', 'cloudtrail', 'iam_policy']
for term in aws_terms:
    funcs_with_term = [f for f in functions if term in f and not f.startswith('aws_')]
    if funcs_with_term:
        print(f"⚠️  Functions with '{term}' (AWS terminology):")
        for func in sorted(funcs_with_term)[:5]:
            print(f"    - {func}")
        if len(funcs_with_term) > 5:
            print(f"    ... and {len(funcs_with_term) - 5} more")
        print()

# Check for suffix variations
suffixes = ['_enabled', '_is_enabled', '_check', '_status_check']
print("⚠️  Check for suffix variations (may indicate duplicates)")
print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total [PROVIDER] functions: {len(functions)}")
print()
```

### Consolidation Script Template

```python
#!/usr/bin/env python3
"""
[PROVIDER] Phase 4: Apply Consolidations
"""
import csv
import json
from collections import defaultdict

INPUT_CSV = "rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
OUTPUT_CSV = "rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
MAPPING_FILE = "rule_finalisation/complance_rule/[provider]_consolidation_mapping_complete.json"

print("=" * 80)
print("[PROVIDER] PHASE 4: APPLYING CONSOLIDATIONS")
print("=" * 80)
print()

# Load mapping
with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
    mapping_data = json.load(f)
    consolidations = mapping_data['consolidations']

# Remove comments
consolidations = {k: v for k, v in consolidations.items() if not k.startswith('_comment')}
print(f"Loaded {len(consolidations)} consolidation mappings")
print()

replacements_made = defaultdict(int)
rows_updated = 0

# Process CSV
rows = []
with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        row_modified = False
        checks = row.get('[provider]_checks', '')
        
        if checks and checks != 'NA':
            funcs = [f.strip() for f in checks.split(';') if f.strip()]
            new_funcs = []
            
            for func in funcs:
                if func in consolidations:
                    new_func = consolidations[func]
                    new_funcs.append(new_func)
                    replacements_made[f"{func} → {new_func}"] += 1
                    row_modified = True
                else:
                    new_funcs.append(func)
            
            new_funcs = sorted(list(set(new_funcs)))
            row['[provider]_checks'] = '; '.join(new_funcs)
            
            if row_modified:
                rows_updated += 1
        
        rows.append(row)

print(f"✓ Processed {len(rows)} rows")
print(f"✓ Updated {rows_updated} rows")
print(f"✓ Total replacements: {sum(replacements_made.values())}")
print()

# Write CSV
with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Updated CSV saved")
print()

# Generate report
report = {
    'metadata': {'phase': 4, 'date': 'YYYY-MM-DD', 'status': 'complete'},
    'statistics': {
        'consolidation_mappings': len(consolidations),
        'rows_updated': rows_updated,
        'total_replacements': sum(replacements_made.values())
    },
    'replacements': dict(replacements_made)
}

with open('rule_finalisation/complance_rule/[provider]_phase4_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print("✅ PHASE 4 COMPLETE!")
```

---

## Quality Checks

After each phase, verify:

1. **No unintended changes** to other cloud providers
2. **CSV structure intact** (same number of rows, columns)
3. **No broken function names** (no typos introduced)
4. **Counts accurate** (total_checks column updated correctly)
5. **Duplicates removed** (no duplicate functions in same cell)

---

## Success Criteria

A cloud provider correction is COMPLETE when:

✅ Analysis shows 0 functions needing consolidation  
✅ No AWS terminology in functions (unless it's AWS)  
✅ Consistent service naming throughout  
✅ Proper provider-specific terminology used  
✅ Functional duplicates consolidated  
✅ All documentation generated  
✅ Verification passed  

---

## Remaining Cloud Providers

### Priority Order (by usage/importance):

1. **GCP** - Google Cloud Platform (high priority)
2. **OCI** - Oracle Cloud Infrastructure (medium priority)
3. **IBM Cloud** - IBM Cloud (medium priority)
4. **Alicloud** - Alibaba Cloud (medium priority)
5. **K8s** - Kubernetes (special case - may have different patterns)

---

## Time Estimates

Based on AWS and Azure experience:

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1 | 1-2 hours | 1-2 hours |
| Phase 2 | 2-3 hours | 3-5 hours |
| Phase 3 | 3-4 hours | 6-9 hours |
| Phase 4 | 1 hour | 7-10 hours |
| Phase 5 | 1 hour | 8-11 hours |

**Per cloud provider:** 8-11 hours  
**Total for 5 providers:** 40-55 hours

Can be accelerated with:
- Parallel analysis
- Reusing script templates
- Pattern recognition from previous work

---

## Next Steps

For each cloud provider:

1. Create folder: `rule_finalisation/complance_rule/[provider]_corrections/`
2. Follow 5-phase methodology
3. Generate all documentation
4. Verify completion
5. Move to next provider

---

*Methodology proven and tested on AWS ✅ and Azure ✅*
*Ready to apply to GCP, OCI, IBM, Alicloud, K8s*


