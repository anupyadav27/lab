"""
Apply Function Normalization to Consolidated CSV
Replaces duplicate function names with canonical versions
"""

import csv
import json
from pathlib import Path
from datetime import datetime

# Paths
INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08.csv")
MAPPING_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/function_normalization_mapping.json")
OUTPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_normalized_2025-11-08.csv")
BACKUP_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08_backup.csv")

# Load mapping
with open(MAPPING_FILE, 'r') as f:
    mapping_data = json.load(f)
    variant_to_canonical = mapping_data['variant_to_canonical']

print("=" * 80)
print("APPLYING FUNCTION NORMALIZATION TO CSV")
print("=" * 80)
print()
print(f"Input CSV: {INPUT_CSV}")
print(f"Mapping file: {MAPPING_FILE}")
print(f"Output CSV: {OUTPUT_CSV}")
print()
print(f"Total normalization rules: {len(variant_to_canonical)}")
print()

# Statistics
stats = {
    'rows_processed': 0,
    'rows_updated': 0,
    'functions_normalized': 0,
    'normalizations_by_column': {
        'aws_checks': 0,
        'azure_checks': 0,
        'gcp_checks': 0,
        'oracle_checks': 0,
        'ibm_checks': 0,
        'alicloud_checks': 0,
        'k8s_checks': 0
    }
}

def normalize_check_string(check_string, column_name):
    """Normalize a semicolon-separated check string"""
    if not check_string or check_string == 'NA':
        return check_string, 0
    
    checks = [c.strip() for c in check_string.split(';') if c.strip()]
    normalized_checks = []
    changes = 0
    
    for check in checks:
        if check in variant_to_canonical:
            normalized_checks.append(variant_to_canonical[check])
            changes += 1
        else:
            normalized_checks.append(check)
    
    if changes > 0:
        stats['normalizations_by_column'][column_name] += changes
    
    return ';'.join(normalized_checks) if normalized_checks else 'NA', changes

# Create backup
print("Creating backup...")
import shutil
shutil.copy2(INPUT_CSV, BACKUP_CSV)
print(f"Backup created: {BACKUP_CSV}")
print()

# Process CSV
print("Processing CSV rows...")
check_columns = ['aws_checks', 'azure_checks', 'gcp_checks', 'oracle_checks', 'ibm_checks', 'alicloud_checks', 'k8s_checks']

with open(INPUT_CSV, 'r', encoding='utf-8') as infile, \
     open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    
    for row in reader:
        stats['rows_processed'] += 1
        row_changed = False
        
        # Normalize each check column
        for col in check_columns:
            original_value = row.get(col, 'NA')
            normalized_value, changes = normalize_check_string(original_value, col)
            
            if changes > 0:
                row[col] = normalized_value
                row_changed = True
                stats['functions_normalized'] += changes
        
        if row_changed:
            stats['rows_updated'] += 1
        
        writer.writerow(row)
        
        if stats['rows_processed'] % 500 == 0:
            print(f"  Processed {stats['rows_processed']} rows...")

print(f"  Processed {stats['rows_processed']} rows (complete)")
print()

# Summary
print("=" * 80)
print("NORMALIZATION COMPLETE!")
print("=" * 80)
print()
print(f"Rows processed: {stats['rows_processed']}")
print(f"Rows updated: {stats['rows_updated']}")
print(f"Total functions normalized: {stats['functions_normalized']}")
print()
print("Normalizations by column:")
for col, count in stats['normalizations_by_column'].items():
    if count > 0:
        print(f"  {col:20}: {count:4} functions")
print()
print(f"Output file: {OUTPUT_CSV}")
print(f"Backup file: {BACKUP_CSV}")
print()

# Save statistics
stats_file = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/normalization_statistics.json")
with open(stats_file, 'w') as f:
    json.dump(stats, f, indent=2)

print(f"Statistics saved: {stats_file}")
print()

