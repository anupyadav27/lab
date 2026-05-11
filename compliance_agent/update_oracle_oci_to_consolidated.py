#!/usr/bin/env python3
"""
Update consolidated_compliance_rules_FINAL.csv with Oracle OCI functions
Process one framework at a time
"""
import csv
import shutil
from datetime import datetime
from pathlib import Path

print("=" * 80)
print("UPDATING CONSOLIDATED CSV WITH ORACLE OCI FUNCTIONS")
print("=" * 80)

# Consolidated CSV path
CONSOLIDATED_CSV = '/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv'

# Framework mappings
FRAMEWORKS = {
    'FedRamp': {
        'csv': 'FedRamp/FedRAMP_controls_with_checks.csv',
        'id_field': 'Control_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'FedRAMP'
    },
    'canada_pbmm': {
        'csv': 'canada_pbmm/CANADA_PBMM_controls_with_checks.csv',
        'id_field': 'Control_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'CANADA_PBMM'
    },
    'cisa_ce': {
        'csv': 'cisa_ce/CISA_CE_controls_with_checks.csv',
        'id_field': 'Practice_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'CISA_CE'
    },
    'gdpr': {
        'csv': 'gdpr/GDPR_controls_with_checks.csv',
        'id_field': 'Article_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'GDPR'
    },
    'hipaa': {
        'csv': 'hipaa/HIPAA_controls_with_checks.csv',
        'id_field': 'Requirement_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'HIPAA'
    },
    'iso27001-2022': {
        'csv': 'iso27001-2022/ISO27001_2022_controls_with_checks.csv',
        'id_field': 'Control_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'ISO27001'  # Fixed to match consolidated CSV
    },
    'nist_800_171': {
        'csv': 'nist_800_171/NIST_800-171_R2_controls_with_checks.csv',
        'id_field': 'Requirement_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'NIST_800-171'
    },
    'nist_sp_800_53': {
        'csv': 'nist_complaince_agent/NIST_controls_with_checks.csv',
        'id_field': 'Control_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'NIST_800-53'  # Fixed to match consolidated CSV
    },
    'pci_dss': {
        'csv': 'pci_compliance_agent/PCI_controls_with_checks.csv',
        'id_field': 'id',  # PCI uses 'id' field, not 'Requirement_ID'
        'oracle_field': 'oracle_checks',  # lowercase for PCI
        'framework_name': 'PCI-DSS'  # Fixed to match consolidated CSV (with hyphen)
    },
    'rbi_bank': {
        'csv': 'rbi_bank/RBI_BANK_controls_with_checks.csv',
        'id_field': 'Control_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'RBI_BANK'
    },
    'rbi_nbfc': {
        'csv': 'rbi_nbfc/RBI_NBFC_controls_with_checks.csv',
        'id_field': 'Control_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'RBI_NBFC'
    },
    'soc2': {
        'csv': 'soc2/SOC2_controls_with_checks.csv',
        'id_field': 'Criteria_ID',
        'oracle_field': 'Oracle_Checks',
        'framework_name': 'SOC2'
    },
    'cis_oracle': {
        'csv': 'cis_compliance_agent/oracle_agent/output_final_20251101_144020/aws_automated_20251101_152816.csv',
        'id_field': 'id',
        'oracle_field': 'program_name',  # AWS function names for Oracle checks
        'framework_name': 'CIS'
    }
}

def normalize_requirement_id(req_id):
    """Normalize requirement ID for matching"""
    # Handle FedRAMP sub-controls: AC-2 (1) -> ac_2_1
    import re
    req_id = req_id.strip()
    # Convert "AC-2 (1)" to "AC-2-1" format first
    req_id = re.sub(r'\s*\((\d+)\)', r'_\1', req_id)
    # Then normalize
    return req_id.replace('-', '_').replace('.', '_').lower()

def extract_oracle_mappings():
    """Extract Oracle OCI mappings from all framework CSV files"""
    mappings = {}  # Key: (framework, normalized_req_id) -> Value: [oracle_functions]
    
    print("\n📋 Extracting Oracle OCI mappings from frameworks...")
    
    for fw_key, fw_info in FRAMEWORKS.items():
        csv_path = fw_info['csv']
        if not Path(csv_path).exists():
            print(f"  ⚠️  {fw_key}: File not found - {csv_path}")
            continue
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            
            for row in reader:
                req_id = row.get(fw_info['id_field'], '').strip()
                oracle_checks = row.get(fw_info['oracle_field'], '').strip()
                
                if oracle_checks:
                    # Parse Oracle functions
                    oracle_funcs = [f.strip() for f in oracle_checks.split(';') if f.strip()]
                    if oracle_funcs:
                        norm_req_id = normalize_requirement_id(req_id)
                        mappings[(fw_info['framework_name'], norm_req_id)] = oracle_funcs
                        count += 1
            
            print(f"  ✅ {fw_key}: {count} requirements with Oracle data")
    
    return mappings

def update_consolidated_csv(oracle_mappings):
    """Update consolidated CSV with Oracle OCI functions"""
    
    # Step 1: Create backup
    print("\n📋 Creating backup...")
    backup_file = CONSOLIDATED_CSV.replace('.csv', f'_BACKUP_ORACLE_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    shutil.copy2(CONSOLIDATED_CSV, backup_file)
    print(f"✅ Backup: {backup_file}")
    
    # Step 2: Load consolidated CSV
    print("\n📋 Loading consolidated CSV...")
    with open(CONSOLIDATED_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    print(f"✅ Loaded {len(rows)} requirements")
    
    # Check if oracle column exists
    oracle_col = 'oracle_uniform_format'
    if oracle_col not in fieldnames:
        print(f"⚠️  Adding new column: {oracle_col}")
        fieldnames = list(fieldnames) + [oracle_col]
    
    # Step 3: Update rows
    print("\n📋 Updating requirements with Oracle OCI functions...")
    
    updates_by_framework = {}
    
    for row in rows:
        framework = row.get('compliance_framework', '').strip()
        compliance_id = row.get('unique_compliance_id', '').strip()
        
        # Extract requirement ID from compliance_id
        req_id = extract_requirement_id_from_compliance_id(framework, compliance_id)
        
        if req_id:
            norm_req_id = normalize_requirement_id(req_id)
            mapping_key = (framework, norm_req_id)
            
            if mapping_key in oracle_mappings:
                oracle_funcs = oracle_mappings[mapping_key]
                row[oracle_col] = '; '.join(oracle_funcs)
                
                if framework not in updates_by_framework:
                    updates_by_framework[framework] = 0
                updates_by_framework[framework] += 1
    
    # Step 4: Save updated CSV
    print("\n📋 Saving updated consolidated CSV...")
    with open(CONSOLIDATED_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ Saved: {CONSOLIDATED_CSV}")
    
    return updates_by_framework, len(rows)

def extract_requirement_id_from_compliance_id(framework, compliance_id):
    """Extract requirement ID from compliance_id based on framework"""
    
    if not compliance_id:
        return None
    
    compliance_id_lower = compliance_id.lower()
    
    # NIST 800-171: Extract pattern like 3_11_2
    if framework == 'NIST_800-171':
        parts = compliance_id.split('_')
        for i, part in enumerate(parts):
            if part.isdigit() and i + 2 < len(parts):
                if parts[i+1].isdigit() and parts[i+2].isdigit():
                    return f"{parts[i]}_{parts[i+1]}_{parts[i+2]}"
    
    # GDPR: Extract article_XX
    elif framework == 'GDPR':
        if 'article' in compliance_id_lower:
            # Extract article number
            parts = compliance_id_lower.split('_')
            for i, part in enumerate(parts):
                if part == 'article' and i + 1 < len(parts):
                    return f"article_{parts[i+1]}"
    
    # HIPAA: Extract 164_308_...
    elif framework == 'HIPAA':
        parts = compliance_id.split('_')
        for i, part in enumerate(parts):
            if part == '164' or part == '164':
                req_parts = [part]
                j = i + 1
                while j < len(parts):
                    next_part = parts[j]
                    if len(next_part) == 4 and next_part.isdigit():
                        break
                    if next_part and (next_part.isdigit() or len(next_part) <= 3):
                        req_parts.append(next_part)
                    else:
                        break
                    j += 1
                return '_'.join(req_parts)
    
    # FedRAMP: Extract control ID (e.g., AC-1, AC-2, AC-2-1 for sub-controls)
    elif framework == 'FedRAMP':
        import re
        # Match pattern like AC-2 or AC-2_1 (sub-control)
        match = re.search(r'([A-Z]{2,3}-\d+(?:_\d+)?)', compliance_id)
        if match:
            # Return in format that matches source: AC-2_1 should match AC-2 (1)
            return match.group(1)
    
    # NIST SP 800-53: Extract control ID (e.g., AC-1-a, AC-2)
    elif framework == 'NIST_800-53':
        parts = compliance_id.split('_')
        for part in parts:
            # Match patterns like AC-1, AC-1-a, AC-2-1
            if '-' in part and len(part) <= 15:
                # Check if it starts with letters
                if part[0].isalpha():
                    return part
    
    # PCI DSS: Extract requirement number (e.g., 1.1.1, 2.2, 6.2.3.1)
    elif framework == 'PCI-DSS':
        import re
        # Look for pattern like 1.1.1 or 2.2 or 6.2.3.1 (multiple dots)
        match = re.search(r'_(\d+(?:\.\d+)+)_', compliance_id)
        if match:
            return match.group(1)
    
    # SOC2: Extract criteria ID (e.g., cc_1_3 -> CC1.3)
    elif framework == 'SOC2':
        import re
        # Look for pattern like cc_1_3 or CC1.3
        match = re.search(r'cc_(\d+)_(\d+)', compliance_id, re.IGNORECASE)
        if match:
            return f"CC{match.group(1)}.{match.group(2)}"
    
    # ISO 27001: Extract control ID (e.g., A.5.1, A.8.10)
    elif framework == 'ISO27001':
        import re
        # Look for pattern like A.10.1 or A.12.4
        match = re.search(r'(A\.\d+\.\d+)', compliance_id, re.IGNORECASE)
        if match:
            return match.group(1)
    
    # RBI: Extract control number (e.g., 1.1, 1.2)
    elif framework in ['RBI_BANK', 'RBI_NBFC']:
        import re
        # Look for pattern like 1.1 or 2.3
        match = re.search(r'_(\d+\.\d+)_', compliance_id)
        if match:
            return match.group(1)
    
    # CISA CE: Extract practice ID (e.g., Your_Staff-1)
    elif framework == 'CISA_CE':
        import re
        # Look for pattern like Your_Staff-1, Your_Devices-2
        match = re.search(r'([\w]+_[\w]+[-]\d+)', compliance_id)
        if match:
            return match.group(1)
    
    # CANADA PBMM: Extract control ID (e.g., CCCS_AC-1, CCCS_AC-2)
    elif framework == 'CANADA_PBMM':
        parts = compliance_id.split('_')
        # Look for pattern like CCCS_AC-1
        for i, part in enumerate(parts):
            if part == 'CCCS' and i + 1 < len(parts):
                return f"{part}_{parts[i+1]}"
    
    # CIS: Extract control ID (e.g., 1.1, 1.2, 2.1) - ONLY for CIS Oracle
    elif framework == 'CIS':
        import re
        # Only match if this is a CIS Oracle entry (cis_oracle_oracle_X.X)
        if 'cis_oracle_oracle' in compliance_id.lower():
            # Look for pattern like oracle_1.1
            match = re.search(r'_(\d+\.\d+(?:\.\d+)?)_', compliance_id)
            if match:
                return match.group(1)
        return None  # Don't match other CSP CIS entries
    
    return None

# Main execution
if __name__ == '__main__':
    # Extract Oracle mappings
    oracle_mappings = extract_oracle_mappings()
    
    print(f"\n✅ Total Oracle mappings extracted: {len(oracle_mappings)}")
    
    # Update consolidated CSV
    updates_by_framework, total_rows = update_consolidated_csv(oracle_mappings)
    
    # Print summary
    print("\n" + "=" * 80)
    print("ORACLE OCI UPDATE SUMMARY")
    print("=" * 80)
    
    print("\n📊 Updates by Framework:")
    print("-" * 80)
    total_updates = 0
    for fw in sorted(updates_by_framework.keys()):
        count = updates_by_framework[fw]
        total_updates += count
        print(f"  {fw:30s}: {count:4d} requirements updated")
    
    print("-" * 80)
    print(f"  {'TOTAL':30s}: {total_updates:4d} requirements updated")
    print(f"\n  Total requirements in CSV: {total_rows}")
    print(f"  Coverage: {round(total_updates/total_rows*100, 1)}%")
    
    print("\n" + "=" * 80)
    print("✅ ORACLE OCI UPDATE COMPLETE!")
    print("=" * 80)

