#!/usr/bin/env python3
"""
Azure Phase 4: Apply All Consolidations to CSV
Systematically rename Azure functions based on consolidation mapping
"""
import csv
import json
from collections import defaultdict

INPUT_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
OUTPUT_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv.backup"
MAPPING_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/azure_consolidation_mapping_complete.json"
FINAL_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

print("=" * 80)
print("AZURE PHASE 4: APPLYING CONSOLIDATIONS TO CSV")
print("=" * 80)
print()

# Load consolidation mapping
print("Step 1: Loading consolidation mapping...")
with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
    mapping_data = json.load(f)
    consolidations = mapping_data['consolidations']

# Remove comment keys
consolidations = {k: v for k, v in consolidations.items() if not k.startswith('_comment')}
print(f"✓ Loaded {len(consolidations)} consolidation mappings")
print()

# Track statistics
replacements_made = defaultdict(int)
rows_updated = 0

# Read and process CSV
print("Step 2: Processing CSV...")
rows = []
with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        row_modified = False
        azure_checks = row.get('azure_checks', '')
        
        if azure_checks and azure_checks != 'NA':
            # Split functions
            funcs = [f.strip() for f in azure_checks.split(';') if f.strip()]
            new_funcs = []
            
            for func in funcs:
                if func in consolidations:
                    new_func = consolidations[func]
                    new_funcs.append(new_func)
                    replacements_made[f"{func} → {new_func}"] += 1
                    row_modified = True
                else:
                    new_funcs.append(func)
            
            # Remove duplicates and sort
            new_funcs = sorted(list(set(new_funcs)))
            row['azure_checks'] = '; '.join(new_funcs)
            row['total_checks'] = str(len(new_funcs))
            
            if row_modified:
                rows_updated += 1
        
        rows.append(row)

print(f"✓ Processed {len(rows)} rows")
print(f"✓ Updated {rows_updated} rows with Azure consolidations")
print()

# Write updated CSV
print("Step 3: Writing updated CSV...")
with open(FINAL_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Updated CSV saved: {FINAL_CSV}")
print()

# Generate report
print("=" * 80)
print("CONSOLIDATION REPORT")
print("=" * 80)
print()

print(f"Total consolidation mappings:  {len(consolidations)}")
print(f"Rows updated:                  {rows_updated}")
print(f"Total replacements made:       {sum(replacements_made.values())}")
print()

print("Top 20 replacements:")
for replacement, count in sorted(replacements_made.items(), key=lambda x: x[1], reverse=True)[:20]:
    print(f"  {count:3d}x  {replacement}")

print()

# Save detailed report
report = {
    'metadata': {
        'phase': 4,
        'date': '2025-11-08',
        'status': 'complete'
    },
    'statistics': {
        'consolidation_mappings': len(consolidations),
        'rows_updated': rows_updated,
        'total_replacements': sum(replacements_made.values())
    },
    'replacements': dict(replacements_made)
}

report_file = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/azure_phase4_consolidation_report.json"
with open(report_file, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print(f"✓ Detailed report saved: {report_file}")
print()
print("=" * 80)
print("✅ AZURE PHASE 4 COMPLETE!")
print("=" * 80)




