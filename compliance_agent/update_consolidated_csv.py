#!/usr/bin/env python3
"""
Update consolidated_compliance_rules_FINAL.csv with GCP and Azure functions
from NIST 800-171, GDPR, and HIPAA enhanced CSV files
"""
import csv
import shutil
from datetime import datetime

print("=" * 80)
print("UPDATING CONSOLIDATED COMPLIANCE CSV WITH GCP & AZURE FUNCTIONS")
print("=" * 80)

# File paths
CONSOLIDATED_CSV = '/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv'

ENHANCED_FILES = {
    'NIST_800-171': 'nist_800_171/NIST_800-171_R2_controls_with_checks_ENHANCED.csv',
    'GDPR': 'gdpr/GDPR_controls_with_checks_ENHANCED.csv',
    'HIPAA': 'hipaa/HIPAA_controls_with_checks_ENHANCED.csv'
}

# Step 1: Create backup
print("\n📋 Step 1: Creating backup...")
backup_file = CONSOLIDATED_CSV.replace('.csv', f'_BACKUP_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
shutil.copy2(CONSOLIDATED_CSV, backup_file)
print(f"✅ Backup created: {backup_file}")

# Step 2: Load enhanced function mappings
print("\n📋 Step 2: Loading enhanced function mappings...")

function_mappings = {}  # Key: (framework, requirement_id) -> Value: {gcp: [...], azure: [...]}

for framework, file_path in ENHANCED_FILES.items():
    print(f"  Loading {framework}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            req_id = row.get('Requirement_ID', row.get('Control_ID', row.get('Article_ID', '')))
            gcp_checks = row.get('GCP_Checks', '').strip()
            azure_checks = row.get('Azure_Checks', '').strip()
            
            # Parse functions
            gcp_funcs = [f.strip() for f in gcp_checks.split(';') if f.strip()]
            azure_funcs = [f.strip() for f in azure_checks.split(';') if f.strip()]
            
            function_mappings[(framework, req_id)] = {
                'gcp': gcp_funcs,
                'azure': azure_funcs
            }
    
    print(f"    ✅ Loaded {len([k for k in function_mappings.keys() if k[0] == framework])} requirements")

print(f"  Total mappings loaded: {len(function_mappings)}")

# Step 3: Load consolidated CSV
print("\n📋 Step 3: Loading consolidated compliance CSV...")
with open(CONSOLIDATED_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

print(f"✅ Loaded {len(rows)} compliance requirements")

# Step 4: Update rows with GCP and Azure functions
print("\n📋 Step 4: Updating compliance requirements...")

updates = {
    'NIST_800-171': 0,
    'GDPR': 0,
    'HIPAA': 0,
    'not_found': 0
}

for row in rows:
    framework = row.get('compliance_framework', '').strip()
    compliance_id = row.get('unique_compliance_id', '').strip()
    
    # Extract requirement ID from compliance_id
    # Format examples:
    # nist_800_171_r2_multi_cloud_3_11_2_... -> 3_11_2
    # gdpr_multi_cloud_article_25_... -> article_25
    # hipaa_multi_cloud_164_308_a_1_ii_a_... -> 164_308_a_1_ii_a
    
    req_id = None
    
    if framework == 'NIST_800-171':
        # Extract pattern like 3_11_2 from compliance_id
        parts = compliance_id.split('_')
        # Find the part that matches requirement pattern (e.g., 3_11_2)
        for i, part in enumerate(parts):
            if part.isdigit() and i + 2 < len(parts):
                # Check if next two parts are also numeric
                if parts[i+1].isdigit() and parts[i+2].isdigit():
                    req_id = f"{parts[i]}_{parts[i+1]}_{parts[i+2]}"
                    break
    
    elif framework == 'GDPR':
        # Extract article_XX from compliance_id (case-insensitive)
        compliance_id_lower = compliance_id.lower()
        if 'article_25' in compliance_id_lower or 'Article_25' in compliance_id:
            req_id = 'article_25'
        elif 'article_30' in compliance_id_lower or 'Article_30' in compliance_id:
            req_id = 'article_30'
        elif 'article_32' in compliance_id_lower or 'Article_32' in compliance_id:
            req_id = 'article_32'
    
    elif framework == 'HIPAA':
        # Extract pattern like 164_308_a_1_ii_a from compliance_id
        # hipaa_multi_cloud_164_308_a_1_ii_a_... -> 164_308_a_1_ii_a
        parts = compliance_id.split('_')
        # Find 164_ pattern
        for i, part in enumerate(parts):
            if part == '164':
                # Take next parts until we hit a description word
                req_parts = [part]
                j = i + 1
                while j < len(parts):
                    next_part = parts[j]
                    # Stop at number with 4 digits (like 0001, 0002)
                    if len(next_part) == 4 and next_part.isdigit():
                        break
                    # Add if it's a valid part (number, letter, or combination)
                    if next_part and (next_part.isdigit() or len(next_part) <= 3):
                        req_parts.append(next_part)
                    else:
                        break
                    j += 1
                req_id = '_'.join(req_parts)
                break
    
    # Look up mapping
    if req_id and framework in ['NIST_800-171', 'GDPR', 'HIPAA']:
        mapping_key = (framework, req_id)
        if mapping_key in function_mappings:
            mapping = function_mappings[mapping_key]
            
            # Update GCP column
            if mapping['gcp']:
                row['gcp_uniform_format'] = '; '.join(mapping['gcp'])
            
            # Update Azure column
            if mapping['azure']:
                row['azure_uniform_format'] = '; '.join(mapping['azure'])
            
            updates[framework] += 1

print(f"\n✅ Updates applied:")
print(f"  NIST 800-171: {updates['NIST_800-171']} requirements")
print(f"  GDPR:         {updates['GDPR']} requirements")
print(f"  HIPAA:        {updates['HIPAA']} requirements")
print(f"  Total:        {sum([v for k, v in updates.items() if k != 'not_found'])} requirements updated")

# Step 5: Save updated CSV
print("\n📋 Step 5: Saving updated consolidated CSV...")
with open(CONSOLIDATED_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Saved: {CONSOLIDATED_CSV}")

# Step 6: Verification
print("\n📋 Step 6: Verification...")
with open(CONSOLIDATED_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    
    gcp_count = sum(1 for r in rows if r.get('gcp_uniform_format', '').strip())
    azure_count = sum(1 for r in rows if r.get('azure_uniform_format', '').strip())

print(f"✅ Verification complete:")
print(f"  Total rows in CSV:    {len(rows)}")
print(f"  Rows with GCP funcs:  {gcp_count}")
print(f"  Rows with Azure funcs: {azure_count}")

print("\n" + "=" * 80)
print("✅ CONSOLIDATED CSV UPDATE COMPLETE!")
print("=" * 80)
print(f"\n📂 Files:")
print(f"  Original (backup): {backup_file}")
print(f"  Updated:           {CONSOLIDATED_CSV}")
print("\n" + "=" * 80)

