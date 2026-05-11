"""
AZURE FUNCTIONS IMPROVEMENT - PHASE 1
Fix Critical Issues: Missing prefix, concatenated, duplicate services, name duplicates
Following AWS improvement methodology
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv")
OUTPUT_DIR = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule")

print("=" * 80)
print("AZURE PHASE 1: CRITICAL ISSUES ANALYSIS")
print("=" * 80)
print()

# Extract all Azure functions
azure_functions = set()
function_usage = defaultdict(int)
function_contexts = defaultdict(list)

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        azure_checks = row.get('azure_checks', '')
        if azure_checks and azure_checks != 'NA':
            funcs = [f.strip() for f in azure_checks.split(';') if f.strip()]
            for func in funcs:
                azure_functions.add(func)
                function_usage[func] += 1
                # Store context for analysis
                function_contexts[func].append({
                    'framework': row.get('compliance_framework'),
                    'control': row.get('requirement_id')
                })

print(f"Total unique Azure functions: {len(azure_functions)}")
print()

# STEP 1.1: Identify issues
issues = {
    'missing_prefix': [],
    'concatenated': [],
    'duplicate_services': defaultdict(set),
    'name_duplicates': defaultdict(list)
}

by_service = defaultdict(list)

for func in sorted(azure_functions):
    # Check 1: Missing prefix
    if not func.startswith('azure_'):
        issues['missing_prefix'].append(func)
        continue
    
    # Check 2: Concatenated (comma-separated)
    if ',' in func:
        issues['concatenated'].append(func)
        continue
    
    # Extract service
    parts = func[6:].split('_')  # Remove 'azure_'
    if parts:
        service = parts[0]
        by_service[service].append(func)

# Check 3: Duplicate service names (like awslambda vs lambda)
service_names = list(by_service.keys())
for i, svc1 in enumerate(service_names):
    for svc2 in service_names[i+1:]:
        # Check if one is contained in the other
        if svc1 in svc2 or svc2 in svc1:
            if svc1 != svc2:
                issues['duplicate_services'][svc1].add(svc2)

# Check 4: Name-based duplicates (different suffixes for same thing)
# Group by base name (remove suffixes like _check, _enabled, _status_check)
base_names = defaultdict(list)
for func in azure_functions:
    if not func.startswith('azure_'):
        continue
    
    # Remove common suffixes to find base
    base = func
    for suffix in ['_check', '_status_check', '_compliance_check', '_enabled', '_is_enabled']:
        if base.endswith(suffix):
            base = base[:-(len(suffix))]
            break
    
    base_names[base].append(func)

# Find duplicates (base names with multiple variations)
for base, funcs in base_names.items():
    if len(funcs) > 1:
        issues['name_duplicates'][base] = funcs

print("=" * 80)
print("PHASE 1 RESULTS")
print("=" * 80)
print()

print(f"✓ Services identified: {len(by_service)}")
print()

# Show issues
print("CRITICAL ISSUES FOUND:")
print()

if issues['missing_prefix']:
    print(f"❌ Issue 1: Functions missing 'azure_' prefix")
    print(f"   Count: {len(issues['missing_prefix'])}")
    print(f"   Examples:")
    for func in issues['missing_prefix'][:5]:
        print(f"      • {func}")
    print()

if issues['concatenated']:
    print(f"❌ Issue 2: Concatenated functions (comma-separated)")
    print(f"   Count: {len(issues['concatenated'])}")
    print(f"   Examples:")
    for func in issues['concatenated'][:5]:
        print(f"      • {func}")
    print()

if issues['duplicate_services']:
    print(f"❌ Issue 3: Duplicate service names")
    print(f"   Count: {len(issues['duplicate_services'])}")
    for svc1, svc2_set in list(issues['duplicate_services'].items())[:5]:
        print(f"      • {svc1} overlaps with {', '.join(svc2_set)}")
    print()

if issues['name_duplicates']:
    print(f"❌ Issue 4: Name-based duplicates (suffix variations)")
    print(f"   Count: {len(issues['name_duplicates'])} groups")
    print(f"   Examples:")
    for base, funcs in list(issues['name_duplicates'].items())[:5]:
        if len(funcs) <= 3:  # Only show clear duplicates
            print(f"      • Base: {base}")
            for func in funcs:
                print(f"        - {func}")
    print()

# Show top services
print("=" * 80)
print("TOP 15 AZURE SERVICES BY FUNCTION COUNT")
print("=" * 80)
print()

sorted_services = sorted(by_service.items(), key=lambda x: len(x[1]), reverse=True)
for i, (service, funcs) in enumerate(sorted_services[:15], 1):
    print(f"{i:2d}. {service:<25s} {len(funcs):3d} functions")

print()

# Identify potential functional duplicates by pattern
print("=" * 80)
print("POTENTIAL FUNCTIONAL DUPLICATES (Need Phase 2 analysis)")
print("=" * 80)
print()

# Storage encryption
storage_enc = [f for f in azure_functions if 'storage' in f and ('encryption' in f or 'encrypted' in f)]
if len(storage_enc) > 2:
    print(f"Storage Encryption: {len(storage_enc)} functions")
    for f in sorted(storage_enc)[:5]:
        print(f"  • {f}")
    print()

# SQL/Database multi-AZ
sql_ha = [f for f in azure_functions if 'sql' in f and ('multi' in f or 'availability' in f or 'az' in f)]
if len(sql_ha) > 1:
    print(f"SQL High Availability: {len(sql_ha)} functions")
    for f in sorted(sql_ha)[:5]:
        print(f"  • {f}")
    print()

# Monitoring/logging enabled
monitor_enabled = [f for f in azure_functions if ('monitor' in f or 'log' in f) and '_enabled' in f]
if len(monitor_enabled) > 3:
    print(f"Monitor/Logging Enabled: {len(monitor_enabled)} functions")
    for f in sorted(monitor_enabled)[:5]:
        print(f"  • {f}")
    print()

# Save detailed analysis
analysis_data = {
    'total_functions': len(azure_functions),
    'services_count': len(by_service),
    'issues': {
        'missing_prefix': issues['missing_prefix'],
        'concatenated': issues['concatenated'],
        'duplicate_services': {k: list(v) for k, v in issues['duplicate_services'].items()},
        'name_duplicates': {k: v for k, v in issues['name_duplicates'].items() if len(v) <= 3}
    },
    'services': {svc: len(funcs) for svc, funcs in by_service.items()},
    'functions_by_service': {svc: funcs for svc, funcs in by_service.items()},
    'function_usage': {f: function_usage[f] for f in azure_functions}
}

output_file = OUTPUT_DIR / "azure_phase1_analysis.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_data, f, indent=2)

print()
print("=" * 80)
print(f"✅ Phase 1 analysis saved: {output_file.name}")
print("=" * 80)
print()
print("SUMMARY:")
print(f"  • Total Azure functions: {len(azure_functions)}")
print(f"  • Services: {len(by_service)}")
print(f"  • Critical issues to fix: {len(issues['missing_prefix']) + len(issues['concatenated']) + len(issues['duplicate_services']) + len([v for v in issues['name_duplicates'].values() if len(v) <= 3])}")
print()
print("NEXT: Phase 2 - Functional analysis by service")

