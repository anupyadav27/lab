#!/usr/bin/env python3
"""
STEP 6: Generate compliance function status CSV
- Combine Step 1, Step 2, Step 3 into one table
- Include service, status, mapped rule (if any), coverage source, compliance IDs
"""
import json
import pandas as pd
from collections import defaultdict

MAPPING_FILE = "service_mappings/AWS_ONE_TO_ONE_MAPPING_BULLETPROOF_COMPLETE_FINAL_WITH_COMPLIANCE.json"
COMPLIANCE_CSV = "complance_rule/consolidated_compliance_rules_FINAL.csv"
OUTPUT_CSV = "AWS_STEP6_FUNCTION_STATUS.csv"

# Load mapping
with open(MAPPING_FILE, 'r') as f:
    mapping = json.load(f)

# Build compliance context
comp_df = pd.read_csv(COMPLIANCE_CSV)
func_to_ids = defaultdict(set)
func_to_requirements = defaultdict(set)

for _, row in comp_df.iterrows():
    funcs = str(row.get('aws_uniform_format', '')).split(';') if pd.notna(row.get('aws_uniform_format')) else []
    unique_id = str(row.get('unique_compliance_id', '')) if pd.notna(row.get('unique_compliance_id')) else ''
    requirement_name = str(row.get('requirement_name', '')) if pd.notna(row.get('requirement_name')) else ''

    for func in funcs:
        func = func.strip()
        if not func:
            continue
        if unique_id:
            func_to_ids[func].add(unique_id)
        if requirement_name:
            func_to_requirements[func].add(requirement_name)

rows = []

for service, data in mapping.items():
    if service == 'metadata':
        continue

    # Step1
    for func, rule in data.get('step1_direct_mapped', {}).items():
        rows.append({
            'service': service,
            'compliance_function': func,
            'status': 'Mapped - Direct',
            'mapped_rule_id': rule,
            'coverage_source': 'STEP1_DIRECT',
            'confidence': 'HIGH',
            'compliance_ids': ';'.join(sorted(func_to_ids.get(func, []))),
            'requirements': ';'.join(sorted(func_to_requirements.get(func, [])))
        })

    # Step2
    for func, info in data.get('step2_covered_by', {}).items():
        mapped_rules = info.get('covered_by_rules', [])
        rows.append({
            'service': service,
            'compliance_function': func,
            'status': 'Mapped - AI',
            'mapped_rule_id': mapped_rules[0] if mapped_rules else '',
            'coverage_source': info.get('coverage_type', 'AI'),
            'confidence': info.get('confidence', 'MEDIUM'),
            'compliance_ids': ';'.join(sorted(func_to_ids.get(func, []))),
            'requirements': ';'.join(sorted(func_to_requirements.get(func, [])))
        })

    # Step3
    step3_funcs = data.get('step3_needs_development', [])
    enhanced = {item.get('function'): item for item in data.get('step3_needs_development_enhanced', []) if 'function' in item}

    for func in step3_funcs:
        entry = enhanced.get(func, {})
        orphaned = False
        if entry:
            for req in entry.get('compliance_requirements', []):
                if 'ORPHANED FUNCTION' in req.get('note', ''):
                    orphaned = True
                    break
        rows.append({
            'service': service,
            'compliance_function': func,
            'status': 'Needs Development - Orphaned' if orphaned else 'Needs Development',
            'mapped_rule_id': '',
            'coverage_source': '',
            'confidence': '',
            'compliance_ids': ';'.join(sorted(func_to_ids.get(func, []))),
            'requirements': ';'.join(sorted(func_to_requirements.get(func, [])))
        })

# Create DataFrame
status_df = pd.DataFrame(rows)
status_df.sort_values(by=['service', 'status', 'compliance_function'], inplace=True)
status_df.to_csv(OUTPUT_CSV, index=False)

print(f"Step 6 function status CSV created: {OUTPUT_CSV}")
print(f"Total rows: {len(status_df)}")
print(status_df['status'].value_counts())
