#!/usr/bin/env python3
"""
Cleanup and Fix Consolidated Compliance CSV:
1. Create backup
2. Remove columns 30-51 (mapping status columns)
3. Fix CIS Oracle - remove AWS functions, add correct Oracle functions
4. Fix CIS Azure - add correct Azure functions
"""
import csv
import shutil
from datetime import datetime
from pathlib import Path

print("=" * 80)
print("CLEANING UP AND FIXING CONSOLIDATED COMPLIANCE CSV")
print("=" * 80)

# File paths
CONSOLIDATED_CSV = '/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv'
ORACLE_CIS_CSV = '/Users/apple/Desktop/compliance_Database/compliance_agent/cis_compliance_agent/oracle_agent/output_final_20251101_144020/aws_automated_20251101_152816.csv'
AZURE_CIS_CSV = '/Users/apple/Desktop/compliance_Database/compliance_agent/cis_compliance_agent/azure_agent/output_final_20251101_214108/aws_automated_20251102_002703.csv'

# Step 1: Create backup
print("\n📋 Step 1: Creating backup...")
backup_file = CONSOLIDATED_CSV.replace('.csv', f'_BACKUP_CLEANUP_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
shutil.copy2(CONSOLIDATED_CSV, backup_file)
print(f"✅ Backup created: {backup_file}")

# Step 2: Load Oracle CIS mappings
print("\n📋 Step 2: Loading Oracle CIS functions...")
oracle_mappings = {}
if Path(ORACLE_CIS_CSV).exists():
    with open(ORACLE_CIS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            req_id = row.get('id', '').strip()
            program_name = row.get('program_name', '').strip()
            if req_id and program_name:
                oracle_mappings[req_id] = program_name
    print(f"✅ Loaded {len(oracle_mappings)} Oracle CIS functions")
else:
    print(f"❌ Oracle CIS file not found: {ORACLE_CIS_CSV}")

# Step 3: Load Azure CIS mappings
print("\n📋 Step 3: Loading Azure CIS functions...")
azure_mappings = {}
if Path(AZURE_CIS_CSV).exists():
    with open(AZURE_CIS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            req_id = row.get('id', '').strip()
            program_name = row.get('program_name', '').strip()
            if req_id and program_name:
                azure_mappings[req_id] = program_name
    print(f"✅ Loaded {len(azure_mappings)} Azure CIS functions")
else:
    print(f"❌ Azure CIS file not found: {AZURE_CIS_CSV}")

# Step 4: Load consolidated CSV
print("\n📋 Step 4: Loading consolidated CSV...")
with open(CONSOLIDATED_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

print(f"✅ Loaded {len(rows)} rows")
print(f"   Original columns: {len(fieldnames)}")

# Step 5: Remove columns 30-51 (mapping status columns)
print("\n📋 Step 5: Removing mapping status columns (30-51)...")
# Keep only columns 1-29
columns_to_keep = fieldnames[:29]
print(f"   Keeping first 29 columns")
print(f"   Removing: {', '.join(fieldnames[29:35])}...")

# Step 6: Fix CIS Oracle and Azure data
print("\n📋 Step 6: Fixing CIS Oracle and Azure data...")

oracle_fixed = 0
azure_fixed = 0
oracle_cleared = 0
azure_cleared = 0

for row in rows:
    comp_id = row.get('unique_compliance_id', '')
    
    # Fix CIS Oracle
    if 'cis_oracle_oracle' in comp_id.lower():
        # Extract requirement ID
        import re
        match = re.search(r'_(\d+(?:\.\d+)+)_', comp_id)
        if match:
            req_id = match.group(1)
            
            # Check if it has wrong AWS data
            current_oracle = row.get('oracle_uniform_format', '').strip()
            if current_oracle and current_oracle.startswith('aws_'):
                oracle_cleared += 1
            
            # Update with correct Oracle function (convert aws_ prefix to oracle_)
            if req_id in oracle_mappings:
                aws_function = oracle_mappings[req_id]
                # Convert aws_ prefix to oracle_
                if aws_function.startswith('aws_'):
                    oracle_function = 'oracle_' + aws_function[4:]
                else:
                    oracle_function = aws_function
                row['oracle_uniform_format'] = oracle_function
                oracle_fixed += 1
    
    # Fix CIS Azure
    if 'cis_azure' in comp_id.lower():
        # Extract requirement ID
        import re
        match = re.search(r'_(\d+(?:\.\d+)+)_', comp_id)
        if match:
            req_id = match.group(1)
            
            # Check if it has wrong AWS data
            current_azure = row.get('azure_uniform_format', '').strip()
            if current_azure and current_azure.startswith('aws_'):
                azure_cleared += 1
            
            # Update with correct Azure function
            if req_id in azure_mappings:
                row['azure_uniform_format'] = azure_mappings[req_id]
                azure_fixed += 1

print(f"✅ CIS Oracle: Cleared {oracle_cleared} AWS entries, Fixed {oracle_fixed} with Oracle functions")
print(f"✅ CIS Azure:  Cleared {azure_cleared} AWS entries, Fixed {azure_fixed} with Azure functions")

# Step 7: Save cleaned CSV with only kept columns
print("\n📋 Step 7: Saving cleaned CSV...")
with open(CONSOLIDATED_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns_to_keep, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Saved: {CONSOLIDATED_CSV}")
print(f"   Final columns: {len(columns_to_keep)}")

# Step 8: Verification
print("\n📋 Step 8: Verification...")
with open(CONSOLIDATED_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    final_rows = list(reader)
    final_cols = len(reader.fieldnames)

print(f"✅ Verification:")
print(f"   Total rows: {len(final_rows)}")
print(f"   Total columns: {final_cols} (was {len(fieldnames)})")
print(f"   Removed: {len(fieldnames) - final_cols} columns")

# Sample check
print(f"\n📋 Sample CIS Oracle after fix:")
with open(CONSOLIDATED_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'cis_oracle_oracle_1.1' in row.get('unique_compliance_id', ''):
            print(f"   ID: {row.get('unique_compliance_id', '')[:60]}")
            print(f"   Oracle: {row.get('oracle_uniform_format', '')[:80]}...")
            break

print("\n" + "=" * 80)
print("✅ CLEANUP AND FIX COMPLETE!")
print("=" * 80)
print(f"\n📂 Files:")
print(f"   Backup:  {backup_file}")
print(f"   Updated: {CONSOLIDATED_CSV}")
print("\n" + "=" * 80)

