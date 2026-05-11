#!/usr/bin/env python3
"""
Add CIS rule entries to consolidated_rules_phase4_2025-11-08.csv
based on uniform formats from compliance CSV.
"""

import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path('/Users/apple/Desktop/compliance_Database')
COMPLIANCE_CSV = BASE_DIR / 'rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv'
RULES_CSV = BASE_DIR / 'rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv'


def load_existing_rules():
    """Load existing rule uniform formats."""
    existing = set()
    with RULES_CSV.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uniform = row.get('uniform_rule_format', '').strip()
            if uniform:
                existing.add(uniform)
    return existing


def extract_cis_functions():
    """Extract all CIS functions from compliance CSV."""
    cis_functions = defaultdict(list)
    
    with COMPLIANCE_CSV.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            unique_id = row['unique_compliance_id']
            
            # Azure CIS
            if unique_id.startswith('cis_azure'):
                funcs = row.get('azure_mapped_functions', '').strip()
                if funcs:
                    for func in funcs.split(';'):
                        func = func.strip()
                        if func:
                            cis_functions['azure'].append({
                                'uniform': func,
                                'compliance_id': unique_id,
                                'service': 'various'  # Will need to derive from function name
                            })
            
            # GCP CIS
            elif unique_id.startswith('cis_gcp'):
                funcs = row.get('gcp_mapped_functions', '').strip()
                if funcs:
                    for func in funcs.split(';'):
                        func = func.strip()
                        if func:
                            cis_functions['gcp'].append({
                                'uniform': func,
                                'compliance_id': unique_id,
                                'service': 'various'
                            })
            
            # OCI CIS (uses oracle_uniform_format)
            elif unique_id.startswith('cis_oracle'):
                funcs = row.get('oracle_uniform_format', '').strip()
                if funcs:
                    for func in funcs.split(';'):
                        func = func.strip()
                        if func and not func.startswith('aws_'):  # Skip AWS contamination
                            cis_functions['oci'].append({
                                'uniform': func,
                                'compliance_id': unique_id,
                                'service': 'various'
                            })
    
    return cis_functions


def derive_service_from_uniform(uniform, csp):
    """Derive service name from uniform format."""
    parts = uniform.split('.')
    if len(parts) >= 2:
        return parts[1]
    return 'unknown'


def add_cis_rules():
    """Add missing CIS rules to rule CSV."""
    
    # Backup
    backup_path = BASE_DIR / f"rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08_BACKUP_CIS_ADD_{datetime.now():%Y%m%d_%H%M%S}.csv"
    backup_path.write_bytes(RULES_CSV.read_bytes())
    
    existing_uniforms = load_existing_rules()
    cis_functions = extract_cis_functions()
    
    stats = defaultdict(lambda: {'added': 0, 'already_exists': 0})
    
    # Load existing rules
    with RULES_CSV.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    # Deduplicate functions per CSP
    for csp, functions_list in cis_functions.items():
        unique_funcs = {}
        for item in functions_list:
            uniform = item['uniform']
            if uniform not in unique_funcs:
                unique_funcs[uniform] = item
        
        # Add missing rules
        for uniform, item in unique_funcs.items():
            if uniform in existing_uniforms:
                stats[csp]['already_exists'] += 1
                continue
            
            service = derive_service_from_uniform(uniform, csp)
            
            # Create new rule row
            new_row = {col: '' for col in fieldnames}
            new_row['cloud_provider'] = csp if csp != 'oci' else 'oci'
            new_row['rule_id'] = uniform
            new_row['uniform_rule_format'] = uniform
            new_row['service'] = service
            new_row['category'] = 'cis_control'
            new_row['provider_service'] = service
            
            rows.append(new_row)
            existing_uniforms.add(uniform)
            stats[csp]['added'] += 1
    
    # Write back
    with RULES_CSV.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    return {
        'timestamp': datetime.now().isoformat(),
        'backup': str(backup_path),
        'stats': dict(stats)
    }


def main():
    print('Adding CIS rule entries to rule catalog...')
    report = add_cis_rules()
    
    import json
    report_path = BASE_DIR / 'rule_finalisation/complance_rule/CIS_RULES_ADD_REPORT.json'
    report_path.write_text(json.dumps(report, indent=2))
    
    print(f'\nCompleted. Report: {report_path.name}')
    for csp, data in report['stats'].items():
        print(f'{csp.upper()}: Added {data["added"]}, Already existed {data["already_exists"]}')


if __name__ == '__main__':
    main()

