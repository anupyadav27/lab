#!/usr/bin/env python3
"""
Add Needs Development compliance functions as rows to rule_list CSV using existing schema.
"""
import pandas as pd
from pathlib import Path

RULE_LIST_CSV = Path('rule_list/consolidated_rules_phase4_2025-11-08.csv')
STEP6_CSV = Path('AWS_STEP6_FUNCTION_STATUS.csv')

rule_df = pd.read_csv(RULE_LIST_CSV)
status_df = pd.read_csv(STEP6_CSV)
needs = status_df[status_df['status'] == 'Needs Development'].copy()

existing_rule_ids = set(rule_df['rule_id'].astype(str))

# Determine service from compliance function
service_col = []
for func in needs['compliance_function']:
    parts = func.split('.')
    service_col.append(parts[1] if len(parts) > 1 else '')
needs['service'] = service_col

# Columns present in rule_df
columns = list(rule_df.columns)

new_rows = []
for _, row in needs.iterrows():
    func = row['compliance_function']
    if func in existing_rule_ids:
        continue
    data = {col: '' for col in columns}
    data['cloud_provider'] = 'aws'
    data['rule_id'] = func
    data['service'] = row['service']
    data['uniform_rule_format'] = func
    data['mapped_compliance_functions'] = ''
    data['mapped_compliance_ids'] = row.get('compliance_ids', '')
    data['mapping_sources'] = 'Needs Development'
    data['mapping_services'] = row['service']
    new_rows.append(data)

if new_rows:
    rule_df = pd.concat([rule_df, pd.DataFrame(new_rows)], ignore_index=True)
    rule_df.to_csv(RULE_LIST_CSV, index=False)
    print(f"Added {len(new_rows)} needs-development rows to {RULE_LIST_CSV}")
else:
    print("No new rows added (all needs-development functions already present)")
