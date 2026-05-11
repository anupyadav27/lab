#!/usr/bin/env python3
"""
Add "Needs Development" placeholder rules for CIS Azure/OCI controls
where compliance CSV says automated but agent didn't produce functions.
"""

import csv
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path('/Users/apple/Desktop/compliance_Database')
RULES_CSV = BASE_DIR / 'rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv'
COMPLIANCE_CSV = BASE_DIR / 'rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv'


def main():
    # Load reports
    azure_report = json.loads((BASE_DIR / 'rule_finalisation/complance_rule/CIS_AZURE_COMPLETE_MAPPING_REPORT.json').read_text())
    oci_report = json.loads((BASE_DIR / 'rule_finalisation/complance_rule/CIS_OCI_COMPLETE_MAPPING_REPORT.json').read_text())
    
    azure_needs = azure_report.get('needs_development', [])
    oci_needs = oci_report.get('needs_development', [])
    
    print(f'Azure needs development: {len(azure_needs)}')
    print(f'OCI needs development: {len(oci_needs)}')
    
    if not azure_needs and not oci_needs:
        print('No needs development entries found.')
        return
    
    # Load compliance data
    comp_df = pd.read_csv(COMPLIANCE_CSV, dtype=str).fillna('')
    
    # Load rules
    with RULES_CSV.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    # Backup
    backup_path = BASE_DIR / f"rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08_BACKUP_NEEDS_DEV_{datetime.now():%Y%m%d_%H%M%S}.csv"
    backup_path.write_bytes(RULES_CSV.read_bytes())
    
    existing_uniforms = {row.get('uniform_rule_format', '').strip() for row in rows}
    added = 0
    skipped = 0
    
    # Process Azure
    for item in azure_needs:
        comp_id = item['compliance_id']
        comp_row = comp_df[comp_df['unique_compliance_id']==comp_id]
        if comp_row.empty:
            skipped += 1
            continue
        
        # Generate function name from requirement
        req_id = item.get('requirement_id', '').replace('.', '_')
        service = item.get('service', 'unknown').lower().replace(' ', '_')
        uniform = f'azure.{service}.cis_{req_id}_needs_development'
        
        if uniform in existing_uniforms:
            skipped += 1
            continue
        
        # Create placeholder rule
        new_row = {col: '' for col in fieldnames}
        new_row['cloud_provider'] = 'azure'
        new_row['rule_id'] = f'azure::{service}::cis_{req_id}_needs_development'
        new_row['uniform_rule_format'] = uniform
        new_row['service'] = service
        new_row['category'] = 'cis_control'
        new_row['provider_service'] = service
        new_row['azure_mapped_compliance_ids'] = comp_id
        new_row['azure_mapped_compliance_functions'] = uniform
        new_row['azure_mapping_sources'] = f'{uniform}:Needs Development'
        
        rows.append(new_row)
        existing_uniforms.add(uniform)
        added += 1
    
    # Process OCI
    for item in oci_needs:
        comp_id = item['compliance_id']
        comp_row = comp_df[comp_df['unique_compliance_id']==comp_id]
        if comp_row.empty:
            skipped += 1
            continue
        
        req_id = item.get('requirement_id', '').replace('.', '_')
        service = item.get('service', 'unknown').lower().replace(' ', '_')
        uniform = f'oci.{service}.cis_{req_id}_needs_development'
        
        if uniform in existing_uniforms:
            skipped += 1
            continue
        
        new_row = {col: '' for col in fieldnames}
        new_row['cloud_provider'] = 'oci'
        new_row['rule_id'] = f'oci::{service}::cis_{req_id}_needs_development'
        new_row['uniform_rule_format'] = uniform
        new_row['service'] = service
        new_row['category'] = 'cis_control'
        new_row['provider_service'] = service
        new_row['oci_mapped_compliance_ids'] = comp_id
        new_row['oci_mapped_compliance_functions'] = uniform
        new_row['oci_mapping_sources'] = f'{uniform}:Needs Development'
        
        rows.append(new_row)
        existing_uniforms.add(uniform)
        added += 1
    
    # Save
    with RULES_CSV.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'backup': str(backup_path),
        'added': added,
        'skipped': skipped
    }
    
    report_path = BASE_DIR / 'rule_finalisation/complance_rule/NEEDS_DEV_PLACEHOLDERS_REPORT.json'
    report_path.write_text(json.dumps(report, indent=2))
    
    print(f'\nAdded {added} "Needs Development" placeholder rules')
    print(f'Skipped (already exist): {skipped}')
    print(f'Backup: {backup_path.name}')


if __name__ == '__main__':
    main()

