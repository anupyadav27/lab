#!/usr/bin/env python3
"""
Analyze remaining Azure functions after Phase 4
Extract all unique Azure functions and categorize them
"""
import csv
from collections import defaultdict

INPUT_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

print("=" * 80)
print("ANALYZING REMAINING AZURE FUNCTIONS AFTER PHASE 4")
print("=" * 80)
print()

# Collect all Azure functions
azure_functions = defaultdict(int)

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        azure_checks = row.get('azure_checks', '')
        if azure_checks and azure_checks != 'NA':
            funcs = [f.strip() for f in azure_checks.split(';') if f.strip()]
            for func in funcs:
                azure_functions[func] += 1

# Sort by frequency
sorted_funcs = sorted(azure_functions.items(), key=lambda x: (-x[1], x[0]))

print(f"Total unique Azure functions: {len(sorted_funcs)}")
print()

# Categorize by prefix
categories = defaultdict(list)
for func, count in sorted_funcs:
    prefix = func.split('_')[1] if len(func.split('_')) > 1 else 'unknown'
    categories[prefix].append((func, count))

print("=" * 80)
print("FUNCTIONS BY SERVICE PREFIX")
print("=" * 80)
print()

for prefix in sorted(categories.keys()):
    funcs = categories[prefix]
    print(f"\n{prefix.upper()} ({len(funcs)} functions):")
    print("-" * 80)
    for func, count in funcs[:10]:  # Show top 10
        print(f"  {count:3d}x  {func}")
    if len(funcs) > 10:
        print(f"  ... and {len(funcs) - 10} more")

print()
print("=" * 80)
print("FUNCTIONS THAT NEED CONSOLIDATION")
print("=" * 80)
print()

# Identify functions that still need cleanup
needs_cleanup = []

for func, count in sorted_funcs:
    # Check for problematic patterns
    issues = []
    
    if 'active_directory' in func:
        issues.append("Should use 'ad' instead of 'active_directory'")
    if '_ebs_' in func and 'azure' in func:
        issues.append("Should use 'disk' instead of 'ebs'")
    if '_bucket_' in func and 'azure' in func:
        issues.append("Should use 'account' instead of 'bucket'")
    if 'cloudwatch' in func and 'azure' in func:
        issues.append("Should use 'monitor' instead of 'cloudwatch'")
    if '_s3_' in func and 'azure' in func:
        issues.append("Should use 'storage' instead of 's3'")
    if '_instance_' in func and 'azure_sql' in func:
        issues.append("Should use 'database' instead of 'instance'")
    if 'azure_compute_instance_managed_by_ssm' in func:
        issues.append("Should use 'automation' instead of 'ssm'")
    
    if issues:
        needs_cleanup.append((func, count, issues))

print(f"Found {len(needs_cleanup)} functions that need cleanup:")
print()

for func, count, issues in needs_cleanup:
    print(f"{count:3d}x  {func}")
    for issue in issues:
        print(f"       → {issue}")
    print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total Azure functions:           {len(sorted_funcs)}")
print(f"Functions needing consolidation: {len(needs_cleanup)}")
print(f"Percentage needing cleanup:      {len(needs_cleanup)*100//len(sorted_funcs)}%")
print()

