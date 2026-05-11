#!/usr/bin/env python3
"""
Re-analyze alignment after standardization
Now both databases use uniform dot notation
"""
import csv
import json
from collections import defaultdict

RULE_LIST_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

print("=" * 100)
print("ALIGNMENT ANALYSIS AFTER STANDARDIZATION")
print("=" * 100)
print()

# Load rule_list uniform formats
rule_list_functions = defaultdict(set)  # {csp: set of uniform_rule_formats}

with open(RULE_LIST_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csp = row.get('cloud_provider', '').lower()
        uniform = row.get('uniform_rule_format', '')
        if uniform:
            rule_list_functions[csp].add(uniform)

total_rules = sum(len(v) for v in rule_list_functions.values())
print(f"✓ rule_list: {total_rules:,} uniform functions")

# Load compliance uniform formats
compliance_functions = defaultdict(set)  # {csp: set of uniform_rule_formats}
function_usage = defaultdict(int)

csp_columns = {
    'aws': 'aws_uniform_format',
    'azure': 'azure_uniform_format',
    'gcp': 'gcp_uniform_format',
    'oracle': 'oracle_uniform_format',
    'ibm': 'ibm_uniform_format',
    'alicloud': 'alicloud_uniform_format',
    'k8s': 'k8s_uniform_format'
}

with open(COMPLIANCE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for csp, column in csp_columns.items():
            checks = row.get(column, '')
            if checks and checks != 'NA':
                for func in checks.split(';'):
                    func = func.strip()
                    if func and func != 'NA':
                        compliance_functions[csp].add(func)
                        function_usage[func] += 1

total_comp = sum(len(v) for v in compliance_functions.values())
print(f"✓ compliance: {total_comp:,} uniform function references")
print()

# Analyze alignment for each CSP
print("=" * 100)
print("ALIGNMENT BY CSP (WITH UNIFORM DOT FORMAT)")
print("=" * 100)
print()

overall_stats = {
    'existing': 0,
    'required': 0,
    'aligned': 0,
    'missing': 0,
    'orphaned': 0
}

alignment_details = {}

# Handle OCI/Oracle naming mismatch
# rule_list uses "oci", compliance uses "oracle"
if 'oci' in rule_list_functions and 'oracle' in compliance_functions:
    print("⚠️  CSP NAME MISMATCH DETECTED: rule_list='oci' vs compliance='oracle'")
    print("   Treating as same CSP for alignment analysis...")
    print()
    rule_list_functions['oracle'] = rule_list_functions.pop('oci')

for csp in sorted(set(list(rule_list_functions.keys()) + list(compliance_functions.keys()))):
    existing = rule_list_functions.get(csp, set())
    required = compliance_functions.get(csp, set())
    
    aligned = required & existing
    missing = required - existing
    orphaned = existing - required
    
    coverage = len(aligned) / len(required) * 100 if required else 0
    
    alignment_details[csp] = {
        'existing': len(existing),
        'required': len(required),
        'aligned': len(aligned),
        'missing': len(missing),
        'orphaned': len(orphaned),
        'coverage_pct': round(coverage, 1)
    }
    
    print(f"{csp.upper()}")
    print("-" * 100)
    print(f"  Existing functions in rule_list:  {len(existing):,}")
    print(f"  Required by compliance:            {len(required):,}")
    print(f"  ✅ Aligned (matched):              {len(aligned):,} ({coverage:.1f}% coverage)")
    print(f"  ❌ Missing (TRUE gaps):            {len(missing):,}")
    print(f"  ⚪ Orphaned (unused in compliance): {len(orphaned):,}")
    print()
    
    # Show top missing (true gaps)
    if missing and len(missing) <= 20:
        print(f"  Missing functions (ALL {len(missing)}):")
        missing_sorted = sorted([(f, function_usage.get(f, 0)) for f in missing], key=lambda x: -x[1])
        for func, usage in missing_sorted:
            print(f"    - {func} (used {usage}x)")
        print()
    elif missing:
        print(f"  Top 10 Missing functions:")
        missing_sorted = sorted([(f, function_usage.get(f, 0)) for f in missing], key=lambda x: -x[1])
        for func, usage in missing_sorted[:10]:
            print(f"    - {func} (used {usage}x)")
        print(f"    ... and {len(missing) - 10} more")
        print()
    
    overall_stats['existing'] += len(existing)
    overall_stats['required'] += len(required)
    overall_stats['aligned'] += len(aligned)
    overall_stats['missing'] += len(missing)
    overall_stats['orphaned'] += len(orphaned)

# Overall summary
print("=" * 100)
print("OVERALL SUMMARY (AFTER STANDARDIZATION)")
print("=" * 100)
print()

overall_coverage = overall_stats['aligned'] / overall_stats['required'] * 100 if overall_stats['required'] else 0

print(f"Total rule_list functions:      {overall_stats['existing']:,}")
print(f"Total compliance requirements:  {overall_stats['required']:,}")
print(f"✅ Aligned (matched):           {overall_stats['aligned']:,} ({overall_coverage:.1f}% coverage)")
print(f"❌ Missing (TRUE gaps):         {overall_stats['missing']:,}")
print(f"⚪ Orphaned (unused):           {overall_stats['orphaned']:,}")
print()

print("=" * 100)
print("IMPROVEMENT FROM BEFORE:")
print("=" * 100)
print(f"Before standardization:  0.1% coverage (3 matches)")
print(f"After standardization:   {overall_coverage:.1f}% coverage ({overall_stats['aligned']:,} matches)")
print(f"Improvement:             {overall_coverage - 0.1:.1f}% ({'∞' if overall_coverage > 0.1 else '0'}x better)")
print()

# Save detailed report
report = {
    'summary': overall_stats,
    'coverage_percentage': round(overall_coverage, 1),
    'by_csp': alignment_details,
    'improvement': {
        'before_coverage': 0.1,
        'after_coverage': round(overall_coverage, 1),
        'improvement_pct': round(overall_coverage - 0.1, 1)
    }
}

with open('alignment_report_after_standardization.json', 'w') as f:
    json.dump(report, f, indent=2)

print("✓ Saved: alignment_report_after_standardization.json")
print()
print("=" * 100)
print("✅ ALIGNMENT ANALYSIS COMPLETE")
print("=" * 100)

