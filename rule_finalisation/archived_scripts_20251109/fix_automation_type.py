"""
Fix Automation Type Consistency in CSV
- If functions exist -> automation_type = "automated"
- If no functions exist -> automation_type = "manual"
"""

import csv
from pathlib import Path

INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08.csv")
OUTPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08_fixed.csv")

check_columns = ['aws_checks', 'azure_checks', 'gcp_checks', 'oracle_checks', 'ibm_checks', 'alicloud_checks', 'k8s_checks']

print("=" * 80)
print("FIXING AUTOMATION TYPE CONSISTENCY")
print("=" * 80)
print()

stats = {
    'total_rows': 0,
    'automated_to_manual': 0,
    'manual_to_automated': 0,
    'unchanged': 0
}

changes = []

with open(INPUT_CSV, 'r', encoding='utf-8') as infile, \
     open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    
    for row in reader:
        stats['total_rows'] += 1
        original_automation_type = row.get('automation_type', '').strip().lower()
        
        # Check if any valid functions exist
        has_functions = False
        for col in check_columns:
            checks = row.get(col, '')
            if checks and checks != 'NA' and checks.strip():
                # Check for actual function names (not "No checks defined")
                if 'no checks defined' not in checks.lower():
                    has_functions = True
                    break
        
        # Determine correct automation type
        correct_automation_type = 'automated' if has_functions else 'manual'
        
        # Update if needed
        if original_automation_type != correct_automation_type:
            if original_automation_type == 'automated' and correct_automation_type == 'manual':
                stats['automated_to_manual'] += 1
                changes.append({
                    'id': row['unique_compliance_id'],
                    'change': 'automated -> manual',
                    'reason': 'No functions found'
                })
            elif original_automation_type == 'manual' and correct_automation_type == 'automated':
                stats['manual_to_automated'] += 1
                changes.append({
                    'id': row['unique_compliance_id'],
                    'change': 'manual -> automated',
                    'reason': 'Functions exist'
                })
            
            row['automation_type'] = correct_automation_type
        else:
            stats['unchanged'] += 1
        
        writer.writerow(row)

print(f"Total rows processed: {stats['total_rows']}")
print(f"Rows unchanged: {stats['unchanged']}")
print(f"Changed 'automated' -> 'manual': {stats['automated_to_manual']}")
print(f"Changed 'manual' -> 'automated': {stats['manual_to_automated']}")
print()

if changes:
    print("Changes made:")
    for change in changes:
        print(f"  • {change['id']}: {change['change']} ({change['reason']})")
    print()

print(f"Output file: {OUTPUT_CSV}")
print()

# Replace original with fixed
import shutil
shutil.move(OUTPUT_CSV, INPUT_CSV)
print(f"✅ Original CSV updated with fixes")
print()

