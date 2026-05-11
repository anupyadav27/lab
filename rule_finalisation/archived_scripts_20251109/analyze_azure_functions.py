"""
Analyze Azure functions - Phase 1: Identify issues
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv")
OUTPUT_JSON = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/azure_analysis.json")

print("=" * 80)
print("AZURE FUNCTIONS ANALYSIS - Phase 1")
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

# Categorize issues
issues = {
    'missing_prefix': [],
    'concatenated': [],
    'duplicate_services': defaultdict(list),
    'naming_patterns': defaultdict(list)
}

by_service = defaultdict(list)

for func in sorted(azure_functions):
    # Check for missing prefix
    if not func.startswith('azure_'):
        issues['missing_prefix'].append(func)
        continue
    
    # Check for concatenated (comma-separated)
    if ',' in func:
        issues['concatenated'].append(func)
        continue
    
    # Extract service
    parts = func[6:].split('_')  # Remove 'azure_'
    if parts:
        service = parts[0]
        by_service[service].append(func)
        
        # Check naming patterns
        if func.endswith('_check'):
            issues['naming_patterns']['_check'].append(func)
        elif func.endswith('_status_check'):
            issues['naming_patterns']['_status_check'].append(func)
        elif func.endswith('_compliance_check'):
            issues['naming_patterns']['_compliance_check'].append(func)
        elif '_is_enabled' in func:
            issues['naming_patterns']['_is_enabled'].append(func)

# Check for potential service duplicates
service_names = list(by_service.keys())
for i, svc1 in enumerate(service_names):
    for svc2 in service_names[i+1:]:
        if svc1 in svc2 or svc2 in svc1:
            if svc1 != svc2:
                issues['duplicate_services'][svc1].append(svc2)

print("ISSUES FOUND:")
print(f"  ❌ Missing azure_ prefix: {len(issues['missing_prefix'])}")
print(f"  ❌ Concatenated functions: {len(issues['concatenated'])}")
print(f"  ⚠️  Functions with '_check' suffix: {len(issues['naming_patterns']['_check'])}")
print(f"  ⚠️  Functions with '_status_check' suffix: {len(issues['naming_patterns']['_status_check'])}")
print(f"  ⚠️  Functions with '_is_enabled': {len(issues['naming_patterns']['_is_enabled'])}")
print()

# Show services
print(f"Services found: {len(by_service)}")
print()
print("Top 15 services by function count:")
sorted_services = sorted(by_service.items(), key=lambda x: len(x[1]), reverse=True)
for i, (service, funcs) in enumerate(sorted_services[:15], 1):
    print(f"  {i:2d}. {service:25s} {len(funcs):3d} functions")

print()

# Look for potential duplicates by name similarity
print("Potential duplicate patterns:")
print()

# Storage functions
storage_funcs = [f for f in azure_functions if 'storage' in f.lower()]
if storage_funcs:
    print(f"Storage functions: {len(storage_funcs)}")
    # Group by encryption
    encryption = [f for f in storage_funcs if 'encryption' in f or 'encrypted' in f]
    if len(encryption) > 1:
        print(f"  - Encryption checks: {len(encryption)}")
        for f in sorted(encryption)[:5]:
            print(f"    • {f}")

print()

# Compute functions
compute_funcs = [f for f in azure_functions if 'compute' in f.lower() or 'vm' in f.lower()]
if compute_funcs:
    print(f"Compute/VM functions: {len(compute_funcs)}")
    encryption = [f for f in compute_funcs if 'encryption' in f or 'encrypted' in f]
    if len(encryption) > 1:
        print(f"  - Encryption checks: {len(encryption)}")
        for f in sorted(encryption)[:5]:
            print(f"    • {f}")

print()

# SQL functions
sql_funcs = [f for f in azure_functions if 'sql' in f.lower()]
if sql_funcs:
    print(f"SQL/Database functions: {len(sql_funcs)}")
    multi_az = [f for f in sql_funcs if 'multi' in f or 'az' in f or 'availability' in f]
    if multi_az:
        print(f"  - Multi-AZ/HA checks: {len(multi_az)}")
        for f in sorted(multi_az)[:5]:
            print(f"    • {f}")

print()

# Monitor/Logging functions
monitor_funcs = [f for f in azure_functions if 'monitor' in f.lower() or 'log' in f.lower()]
if monitor_funcs:
    print(f"Monitor/Logging functions: {len(monitor_funcs)}")
    enabled = [f for f in monitor_funcs if '_enabled' in f or '_check' in f]
    if len(enabled) > 5:
        print(f"  - Enabled/check variations: {len(enabled)}")

print()

# Save analysis
analysis_data = {
    'total_functions': len(azure_functions),
    'services': {svc: len(funcs) for svc, funcs in by_service.items()},
    'issues': {
        'missing_prefix': issues['missing_prefix'],
        'concatenated': issues['concatenated'],
        'naming_patterns': {k: v for k, v in issues['naming_patterns'].items()}
    },
    'functions_by_service': {svc: funcs for svc, funcs in by_service.items()}
}

with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(analysis_data, f, indent=2)

print(f"✅ Analysis saved: {OUTPUT_JSON.name}")
print()
print("=" * 80)
print("READY FOR PHASE 2: FUNCTIONAL CONSOLIDATION")
print("=" * 80)

