#!/usr/bin/env python3
"""
Azure Phase 1 - Complete Function Extraction and Consolidation Mapping
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv")
OUTPUT_DIR = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule")

print("=" * 80)
print("AZURE PHASE 1: COMPLETE FUNCTION EXTRACTION")
print("=" * 80)
print()

# Extract all Azure functions
azure_functions = set()
function_usage = defaultdict(int)

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        azure_checks = row.get('azure_checks', '')
        if azure_checks and azure_checks != 'NA':
            funcs = [f.strip() for f in azure_checks.split(';') if f.strip()]
            for func in funcs:
                azure_functions.add(func)
                function_usage[func] += 1

print(f"Total unique Azure functions: {len(azure_functions)}")
print()

# Categorize by service
by_service = defaultdict(list)
issues = {'missing_prefix': [], 'concatenated': [], 'short_names': []}

for func in sorted(azure_functions):
    if not func.startswith('azure_'):
        issues['missing_prefix'].append(func)
        continue
    
    if ',' in func:
        issues['concatenated'].append(func)
        continue
    
    parts = func[6:].split('_')
    if len(parts) < 2:
        issues['short_names'].append(func)
    
    if parts:
        service = parts[0]
        by_service[service].append(func)

print(f"Services: {len(by_service)}")
print(f"Missing prefix: {len(issues['missing_prefix'])}")
print(f"Concatenated: {len(issues['concatenated'])}")
print()

# Create consolidation mapping based on AWS lessons
consolidation_map = {
    # Service name shortenings
    "service_renames": {
        "active_directory": "ad",
        "activedirectory": "ad"
    },
    
    # Function consolidations
    "function_consolidations": {}
}

# Find duplicate patterns
for service, funcs in by_service.items():
    # Pattern 1: Policy attachment duplicates (like AWS IAM)
    aws_attached = [f for f in funcs if 'aws_attached_policy' in f]
    customer_attached = [f for f in funcs if 'customer_attached_policy' in f]
    inline = [f for f in funcs if 'inline_policy' in f]
    
    if aws_attached and customer_attached and inline:
        # Check if they're about same thing (no_administrative_privileges)
        if all('no_administrative_privileges' in f for f in aws_attached + customer_attached + inline):
            base_name = f"azure_{service}_policy_no_administrative_privileges"
            for func in aws_attached + customer_attached + inline:
                if func != base_name:
                    consolidation_map['function_consolidations'][func] = base_name
    
    # Pattern 2: Suffix variations (_check, _status_check, _is_enabled)
    base_names = defaultdict(list)
    for func in funcs:
        base = func
        for suffix in ['_check', '_status_check', '_is_enabled', '_enabled']:
            if base.endswith(suffix):
                base = base[:-(len(suffix))]
                break
        base_names[base].append(func)
    
    for base, variations in base_names.items():
        if len(variations) > 1:
            # Keep the one with _enabled, or shortest
            preferred = None
            if any(f.endswith('_enabled') for f in variations):
                preferred = [f for f in variations if f.endswith('_enabled')][0]
            else:
                preferred = min(variations, key=len)
            
            for func in variations:
                if func != preferred:
                    consolidation_map['function_consolidations'][func] = preferred

print("=" * 80)
print("CONSOLIDATION MAPPING CREATED")
print("=" * 80)
print()

print(f"Function consolidations identified: {len(consolidation_map['function_consolidations'])}")
print()

# Show examples
if consolidation_map['function_consolidations']:
    print("Sample consolidations:")
    for i, (old, new) in enumerate(list(consolidation_map['function_consolidations'].items())[:10], 1):
        print(f"  {i}. {old}")
        print(f"     → {new}")
    print()

# Save outputs
# 1. All Azure functions
with open(OUTPUT_DIR / 'azure_functions_raw.txt', 'w', encoding='utf-8') as f:
    for func in sorted(azure_functions):
        f.write(f"{func}\n")

# 2. Functions by service
functions_by_service = {svc: sorted(funcs) for svc, funcs in by_service.items()}
with open(OUTPUT_DIR / 'azure_functions_by_service_raw.json', 'w', encoding='utf-8') as f:
    json.dump(functions_by_service, f, indent=2)

# 3. Consolidation mapping
with open(OUTPUT_DIR / 'azure_consolidation_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(consolidation_map, f, indent=2)

# 4. Phase 1 complete analysis
analysis = {
    'total_functions': len(azure_functions),
    'services_count': len(by_service),
    'issues': issues,
    'functions_by_service': functions_by_service,
    'consolidations_count': len(consolidation_map['function_consolidations']),
    'estimated_after_consolidation': len(azure_functions) - len(consolidation_map['function_consolidations'])
}

with open(OUTPUT_DIR / 'azure_phase1_complete.json', 'w', encoding='utf-8') as f:
    json.dump(analysis, f, indent=2)

print("=" * 80)
print("FILES CREATED")
print("=" * 80)
print()
print("1. azure_functions_raw.txt - All functions")
print("2. azure_functions_by_service_raw.json - Grouped by service")
print("3. azure_consolidation_mapping.json - Consolidation plan")
print("4. azure_phase1_complete.json - Complete analysis")
print()

print("=" * 80)
print("PHASE 1 SUMMARY")
print("=" * 80)
print()
print(f"Before: {len(azure_functions)} functions")
print(f"Consolidations: {len(consolidation_map['function_consolidations'])}")
print(f"After: {analysis['estimated_after_consolidation']} functions")
print(f"Reduction: {len(consolidation_map['function_consolidations'])} (-{len(consolidation_map['function_consolidations'])/len(azure_functions)*100:.1f}%)")
print()
print("✅ AZURE PHASE 1 COMPLETE!")
print()
print("Next: Phase 2 - Functional analysis by service")

# Write the script to file so it can be run
print("\nTo run this script:")
print("  cd /Users/apple/Desktop/compliance_Database/rule_finalisation")
print("  python3 azure_extraction_complete.py")

