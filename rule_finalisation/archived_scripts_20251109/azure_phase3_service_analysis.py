#!/usr/bin/env python3
"""
Azure Phase 3: Service-Specific Deep Dive
Complete extraction, service grouping, and pattern identification
"""
import csv
import json
from collections import defaultdict

INPUT_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
OUTPUT_DIR = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule"

print("=" * 80)
print("AZURE PHASE 3: SERVICE-SPECIFIC DEEP DIVE")
print("=" * 80)
print()

# Extract ALL Azure functions
azure_functions = set()
function_usage = defaultdict(int)

print("Step 1: Extracting all Azure functions...")
with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        azure_checks = row.get('azure_checks', '')
        if azure_checks and azure_checks != 'NA':
            funcs = [f.strip() for f in azure_checks.split(';') if f.strip()]
            for func in funcs:
                azure_functions.add(func)
                function_usage[func] += 1

print(f"✓ Extracted {len(azure_functions)} unique Azure functions")
print()

# Group by service
print("Step 2: Grouping by service...")
by_service = defaultdict(list)
for func in sorted(azure_functions):
    if func.startswith('azure_'):
        parts = func[6:].split('_', 1)  # Split after azure_
        if parts:
            service = parts[0]
            by_service[service].append(func)

print(f"✓ Identified {len(by_service)} Azure services")
print()

# Detailed service analysis
print("=" * 80)
print("SERVICE-BY-SERVICE ANALYSIS")
print("=" * 80)
print()

# Sort services by function count
services_sorted = sorted(by_service.items(), key=lambda x: len(x[1]), reverse=True)

for service, funcs in services_sorted:
    print(f"\n{'='*80}")
    print(f"SERVICE: {service.upper()} ({len(funcs)} functions)")
    print(f"{'='*80}")
    
    # Group by functional patterns
    patterns = {
        'encryption': [],
        'public_access': [],
        'logging': [],
        'monitoring': [],
        'backup': [],
        'multi_region': [],
        'authentication': [],
        'policy': [],
        'network': [],
        'kms': [],
        'deletion_protection': [],
        'other': []
    }
    
    for func in sorted(funcs):
        categorized = False
        if 'encryption' in func or 'encrypted' in func or 'kms' in func:
            patterns['encryption'].append(func)
            categorized = True
        if 'public' in func and 'access' in func:
            patterns['public_access'].append(func)
            categorized = True
        if 'log' in func and 'logging' not in service:
            patterns['logging'].append(func)
            categorized = True
        if 'monitor' in func and service != 'monitor':
            patterns['monitoring'].append(func)
            categorized = True
        if 'backup' in func or 'snapshot' in func or 'retention' in func:
            patterns['backup'].append(func)
            categorized = True
        if 'multi' in func or 'region' in func:
            patterns['multi_region'].append(func)
            categorized = True
        if 'auth' in func or 'mfa' in func or 'password' in func:
            patterns['authentication'].append(func)
            categorized = True
        if 'policy' in func or 'role' in func or 'privilege' in func:
            patterns['policy'].append(func)
            categorized = True
        if 'network' in func or 'vpc' in func or 'subnet' in func or 'firewall' in func:
            patterns['network'].append(func)
            categorized = True
        if 'deletion_protection' in func:
            patterns['deletion_protection'].append(func)
            categorized = True
        if not categorized:
            patterns['other'].append(func)
    
    # Display patterns
    for pattern_name, pattern_funcs in patterns.items():
        if pattern_funcs:
            print(f"\n  {pattern_name.upper()}: {len(pattern_funcs)} functions")
            for func in sorted(pattern_funcs):
                usage = function_usage[func]
                print(f"    • {func} (used {usage}x)")

print()
print("=" * 80)
print("CONSOLIDATION ANALYSIS")
print("=" * 80)
print()

# Identify all consolidation opportunities
consolidation_recommendations = {}

# Pattern: AWS terminology
aws_terms = {
    'cloudwatch': 'monitor',
    'ebs': 'disk',
    's3': 'storage',
    'bucket': 'account'
}

for func in sorted(azure_functions):
    for aws_term, azure_term in aws_terms.items():
        if aws_term in func:
            # Suggest replacement
            new_name = func.replace(aws_term, azure_term)
            if func != new_name:
                consolidation_recommendations[func] = {
                    'to': new_name,
                    'reason': f'AWS terminology: {aws_term} → {azure_term}'
                }

# Pattern: active_directory → ad
for func in sorted(azure_functions):
    if 'active_directory' in func:
        new_name = func.replace('active_directory', 'ad')
        if func not in consolidation_recommendations:
            consolidation_recommendations[func] = {
                'to': new_name,
                'reason': 'Shorten verbose service name: active_directory → ad'
            }

# Pattern: Suffix variations (_is_enabled, _check, _status_check → _enabled)
suffix_replacements = [
    ('_is_enabled', '_enabled', 'Standardize suffix'),
    ('_status_check', '_enabled', 'Standardize suffix'),
    ('_compliance_check', '_enabled', 'Standardize suffix')
]

for func in sorted(azure_functions):
    for old_suffix, new_suffix, reason in suffix_replacements:
        if func.endswith(old_suffix):
            new_name = func[:-len(old_suffix)] + new_suffix
            if func not in consolidation_recommendations and new_name in azure_functions:
                # Only if target exists
                consolidation_recommendations[func] = {
                    'to': new_name,
                    'reason': reason
                }

print(f"Found {len(consolidation_recommendations)} consolidation opportunities")
print()

# Save comprehensive results
output = {
    'metadata': {
        'phase': 3,
        'date': '2025-11-08',
        'total_functions': len(azure_functions),
        'services': len(by_service),
        'consolidations_identified': len(consolidation_recommendations)
    },
    'services': {
        service: {
            'function_count': len(funcs),
            'functions': sorted(funcs)
        }
        for service, funcs in by_service.items()
    },
    'consolidation_recommendations': consolidation_recommendations,
    'service_rankings': [
        {'service': service, 'count': len(funcs)}
        for service, funcs in services_sorted
    ]
}

output_file = f"{OUTPUT_DIR}/azure_phase3_complete_analysis.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"✓ Complete analysis saved: {output_file}")
print()

# Summary
print("=" * 80)
print("PHASE 3 SUMMARY")
print("=" * 80)
print()
print(f"Total Azure functions:           {len(azure_functions)}")
print(f"Services identified:             {len(by_service)}")
print(f"Consolidation opportunities:     {len(consolidation_recommendations)}")
print()
print("Top 10 services:")
for i, (service, funcs) in enumerate(services_sorted[:10], 1):
    print(f"  {i:2d}. {service:<30s} {len(funcs):3d} functions")
print()
print("=" * 80)
print("✅ AZURE PHASE 3 COMPLETE!")
print("=" * 80)




