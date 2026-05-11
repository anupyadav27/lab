#!/usr/bin/env python3
"""
CSPM Rule vs Compliance Mapping Gap Analysis
Analyzes alignment between existing functions and compliance mappings
"""
import csv
import json
from collections import defaultdict
import re

RULE_LIST_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

print("=" * 100)
print("CSPM RULE vs COMPLIANCE MAPPING GAP ANALYSIS")
print("=" * 100)
print()

# Step 1: Extract all existing CSPM functions from rule_list
print("Step 1: Loading existing CSPM functions...")
existing_functions = defaultdict(set)  # {csp: set of rule_ids}
function_details = {}  # {rule_id: details}

with open(RULE_LIST_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csp = row.get('cloud_provider', '').lower()
        rule_id = row.get('rule_id', '')
        
        if rule_id:
            existing_functions[csp].add(rule_id)
            function_details[rule_id] = {
                'scope': row.get('scope', ''),
                'program': row.get('program', ''),
                'service': row.get('service', ''),
                'resource': row.get('resource', ''),
                'implementation_status': row.get('implementation_status', ''),
                'mapping_status': row.get('mapping_status', ''),
                'mapped': row.get('mapped', '')
            }

print(f"✓ Loaded {sum(len(v) for v in existing_functions.values())} existing functions")
print()

# Step 2: Extract all required functions from compliance mappings
print("Step 2: Loading compliance-required functions...")
compliance_functions = defaultdict(set)  # {csp: set of function_names}
compliance_usage = defaultdict(int)  # {function_name: count}

csp_columns = {
    'aws': 'aws_checks',
    'azure': 'azure_checks',
    'gcp': 'gcp_checks',
    'oracle': 'oracle_checks',
    'ibm': 'ibm_checks',
    'alicloud': 'alicloud_checks',
    'k8s': 'k8s_checks'
}

with open(COMPLIANCE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for csp, column in csp_columns.items():
            checks = row.get(column, '')
            if checks and checks != 'NA':
                for func in checks.split(';'):
                    func = func.strip()
                    if func:
                        compliance_functions[csp].add(func)
                        compliance_usage[func] += 1

print(f"✓ Loaded {sum(len(v) for v in compliance_functions.values())} compliance-required functions")
print()

# Step 3: Analyze alignment for each CSP
print("=" * 100)
print("ALIGNMENT ANALYSIS BY CSP")
print("=" * 100)
print()

total_stats = {
    'existing': 0,
    'required': 0,
    'aligned': 0,
    'missing': 0,
    'orphaned': 0
}

for csp in sorted(set(list(existing_functions.keys()) + list(compliance_functions.keys()))):
    existing = existing_functions.get(csp, set())
    required = compliance_functions.get(csp, set())
    
    # Convert rule_ids to function names for comparison
    # rule_id format: aws.service.resource.check_name
    # function format: aws_service_resource_check_name or aws_service_check_name
    
    existing_names = set()
    for rule_id in existing:
        # Extract function name from rule_id
        # Example: aws.api_gateway.stage.api_access_logging_enabled -> aws_api_gateway_api_access_logging_enabled
        parts = rule_id.split('.')
        if len(parts) >= 4:
            # aws.service.resource.check
            func_name = f"{parts[0]}_{parts[1]}_{parts[3]}"
            existing_names.add(func_name)
        elif len(parts) >= 3:
            # aws.service.check
            func_name = f"{parts[0]}_{parts[1]}_{parts[2]}"
            existing_names.add(func_name)
    
    # Find alignment
    aligned = required & existing_names
    missing = required - existing_names  # Required but not in existing functions
    orphaned = existing_names - required  # Exist but not used in compliance
    
    print(f"{csp.upper()}")
    print("-" * 100)
    print(f"  Existing functions:           {len(existing):,}")
    print(f"  Compliance-required functions: {len(required):,}")
    print(f"  Aligned (exist + used):       {len(aligned):,} ({len(aligned)/len(required)*100 if required else 0:.1f}%)")
    print(f"  Missing (needed but missing): {len(missing):,}")
    print(f"  Orphaned (exist but unused):  {len(orphaned):,}")
    print()
    
    # Show top missing functions
    if missing:
        print(f"  Top 10 MISSING functions (needed but don't exist):")
        missing_with_count = [(f, compliance_usage.get(f, 0)) for f in missing]
        for func, count in sorted(missing_with_count, key=lambda x: -x[1])[:10]:
            print(f"    - {func} (used {count}x in compliance)")
        print()
    
    # Show top orphaned functions
    if orphaned and len(orphaned) > 10:
        print(f"  NOTE: {len(orphaned):,} orphaned functions exist but aren't mapped to compliance")
        print()
    
    total_stats['existing'] += len(existing)
    total_stats['required'] += len(required)
    total_stats['aligned'] += len(aligned)
    total_stats['missing'] += len(missing)
    total_stats['orphaned'] += len(orphaned)

# Step 4: Overall summary
print("=" * 100)
print("OVERALL SUMMARY")
print("=" * 100)
print()
print(f"Total existing CSPM functions:      {total_stats['existing']:,}")
print(f"Total compliance-required functions: {total_stats['required']:,}")
print(f"Total aligned (matched):            {total_stats['aligned']:,} ({total_stats['aligned']/total_stats['required']*100 if total_stats['required'] else 0:.1f}%)")
print(f"Total missing (gaps):               {total_stats['missing']:,}")
print(f"Total orphaned (unmapped):          {total_stats['orphaned']:,}")
print()

# Step 5: Identify potential aliases/duplicates
print("=" * 100)
print("POTENTIAL ALIASES & DUPLICATES")
print("=" * 100)
print()

# Look for similar function names that might be aliases
aliases_found = []
for csp in compliance_functions:
    required = compliance_functions[csp]
    for func in list(required)[:20]:  # Sample first 20
        # Look for similar names
        base = func.replace('_enabled', '').replace('_check', '').replace('_configured', '')
        similar = [f for f in required if base in f and f != func]
        if similar:
            aliases_found.append((func, similar))

if aliases_found:
    print("Potential aliases detected (same base check, different suffix):")
    for orig, similar in aliases_found[:10]:
        print(f"  - {orig}")
        for s in similar:
            print(f"      → {s} (potential alias)")
    print()
else:
    print("No obvious aliases detected in sample.")
    print()

# Generate detailed reports
print("=" * 100)
print("GENERATING DETAILED REPORTS...")
print("=" * 100)
print()

# Report 1: Missing functions by CSP
missing_report = {}
for csp in sorted(compliance_functions.keys()):
    required = compliance_functions.get(csp, set())
    existing_names = set()
    
    for rule_id in existing_functions.get(csp, set()):
        parts = rule_id.split('.')
        if len(parts) >= 4:
            func_name = f"{parts[0]}_{parts[1]}_{parts[3]}"
            existing_names.add(func_name)
        elif len(parts) >= 3:
            func_name = f"{parts[0]}_{parts[1]}_{parts[2]}"
            existing_names.add(func_name)
    
    missing = required - existing_names
    missing_report[csp] = sorted([(f, compliance_usage.get(f, 0)) for f in missing], key=lambda x: -x[1])

with open('gap_analysis_missing_functions.json', 'w') as f:
    json.dump(missing_report, f, indent=2)

print("✓ Saved: gap_analysis_missing_functions.json")

# Report 2: Alignment summary
alignment_summary = {
    'overall': total_stats,
    'by_csp': {}
}

for csp in sorted(set(list(existing_functions.keys()) + list(compliance_functions.keys()))):
    existing = existing_functions.get(csp, set())
    required = compliance_functions.get(csp, set())
    existing_names = set()
    
    for rule_id in existing:
        parts = rule_id.split('.')
        if len(parts) >= 4:
            func_name = f"{parts[0]}_{parts[1]}_{parts[3]}"
            existing_names.add(func_name)
        elif len(parts) >= 3:
            func_name = f"{parts[0]}_{parts[1]}_{parts[2]}"
            existing_names.add(func_name)
    
    aligned = required & existing_names
    missing = required - existing_names
    orphaned = existing_names - required
    
    alignment_summary['by_csp'][csp] = {
        'existing': len(existing),
        'required': len(required),
        'aligned': len(aligned),
        'missing': len(missing),
        'orphaned': len(orphaned),
        'coverage_pct': round(len(aligned)/len(required)*100 if required else 0, 1)
    }

with open('gap_analysis_alignment_summary.json', 'w') as f:
    json.dump(alignment_summary, f, indent=2)

print("✓ Saved: gap_analysis_alignment_summary.json")
print()

print("=" * 100)
print("✅ ANALYSIS COMPLETE")
print("=" * 100)

