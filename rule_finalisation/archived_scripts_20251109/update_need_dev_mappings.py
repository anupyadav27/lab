#!/usr/bin/env python3
"""
For rows tagged 'Needs Development' in rule_list CSV, fill mapped_compliance_functions and mapped_compliance_ids using Step6 status.
"""
import pandas as pd
from pathlib import Path

RULE_LIST_CSV = Path('rule_list/consolidated_rules_phase4_2025-11-08.csv')
STEP6_CSV = Path('AWS_STEP6_FUNCTION_STATUS.csv')

rule_df = pd.read_csv(RULE_LIST_CSV)
step6_df = pd.read_csv(STEP6_CSV)

needs_map = step6_df[step6_df['status'] == 'Needs Development'].set_index('compliance_function')

updated = 0
for idx, row in rule_df.iterrows():
    if str(row.get('mapping_sources')) != 'Needs Development':
        continue
    rule_id = row.get('rule_id')
    if rule_id not in needs_map.index:
        continue
    info = needs_map.loc[rule_id]
    rule_df.at[idx, 'mapped_compliance_functions'] = rule_id
    rule_df.at[idx, 'mapped_compliance_ids'] = info.get('compliance_ids', '')
    updated += 1

rule_df.to_csv(RULE_LIST_CSV, index=False)
print(f'Updated {updated} Needs Development rows with compliance functions and IDs')
