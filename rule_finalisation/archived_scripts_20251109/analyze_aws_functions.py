#!/usr/bin/env python3
"""
Analyze AWS Functions - Find remaining issues and consolidation opportunities
"""
import csv
from collections import defaultdict

CSV_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
PROVIDER_COLUMN = "aws_checks"

print("=" * 80)
print("ANALYZING AWS FUNCTIONS")
print("=" * 80)
print()

# Extract all unique functions
functions = set()
function_counts = defaultdict(int)

with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        checks = row.get(PROVIDER_COLUMN, '')
        if checks and checks != 'NA':
            for func in checks.split(';'):
                func = func.strip()
                if func:
                    functions.add(func)
                    function_counts[func] += 1

print(f"Total unique AWS functions: {len(functions)}")
print()

# Group by prefix/service
services = defaultdict(list)
for func in sorted(functions):
    parts = func.split('_')
    if len(parts) >= 2:
        service = parts[1]  # e.g., "iam", "s3", "ec2"
        services[service].append((func, function_counts[func]))

# Display by service
print("=" * 80)
print("FUNCTIONS BY SERVICE PREFIX")
print("=" * 80)
print()

for service in sorted(services.keys()):
    funcs = services[service]
    service_display = service.upper()
    print(f"{service_display} ({len(funcs)} functions):")
    print("-" * 80)
    for func, count in sorted(funcs, key=lambda x: (-x[1], x[0]))[:10]:
        print(f"  {count:3d}x  {func}")
    if len(funcs) > 10:
        print(f"  ... and {len(funcs) - 10} more")
    print()

# Look for potential issues
print("=" * 80)
print("POTENTIAL ISSUES TO INVESTIGATE")
print("=" * 80)
print()

# Check for suffix variations (potential duplicates)
print("⚠️  Checking for suffix variations (potential duplicates):")
print()

base_names = defaultdict(list)
for func in functions:
    # Remove common suffixes to find base
    base = func
    for suffix in ['_enabled', '_is_enabled', '_check', '_status_check', '_configured', 
                   '_configuration', '_status', '_compliance', '_exists']:
        if base.endswith(suffix):
            base = base[:-len(suffix)]
            break
    if len(base_names[base]) < 5:  # Only show if multiple similar functions
        base_names[base].append(func)

duplicates_found = 0
for base, funcs in sorted(base_names.items()):
    if len(funcs) > 1:
        duplicates_found += 1
        if duplicates_found <= 10:  # Show first 10
            print(f"Similar functions for '{base}':")
            for func in sorted(funcs):
                print(f"  - {func} ({function_counts[func]}x)")
            print()

if duplicates_found > 10:
    print(f"... and {duplicates_found - 10} more potential duplicate groups")
    print()

# Check for inconsistent naming patterns
print("=" * 80)
print("CHECKING FOR NAMING INCONSISTENCIES")
print("=" * 80)
print()

# Functions with mixed terminology
issues = []

# Check for inconsistent encryption naming
encryption_funcs = [f for f in functions if 'encrypt' in f]
encryption_patterns = defaultdict(list)
for func in encryption_funcs:
    if '_encrypted' in func:
        encryption_patterns['_encrypted'].append(func)
    elif '_encryption_enabled' in func:
        encryption_patterns['_encryption_enabled'].append(func)
    elif '_encryption_at_rest' in func:
        encryption_patterns['_encryption_at_rest'].append(func)
    elif '_encryption' in func:
        encryption_patterns['_encryption'].append(func)

if len(encryption_patterns) > 1:
    print(f"⚠️  Inconsistent encryption naming ({len(encryption_funcs)} total):")
    for pattern, funcs in sorted(encryption_patterns.items()):
        print(f"  {pattern}: {len(funcs)} functions")
    print()

# Check for logging inconsistencies
logging_funcs = [f for f in functions if 'log' in f]
logging_patterns = defaultdict(list)
for func in logging_funcs:
    if '_logging_enabled' in func:
        logging_patterns['_logging_enabled'].append(func)
    elif '_logs_enabled' in func:
        logging_patterns['_logs_enabled'].append(func)
    elif '_log_enabled' in func:
        logging_patterns['_log_enabled'].append(func)

if len(logging_patterns) > 1:
    print(f"⚠️  Inconsistent logging naming ({len(logging_funcs)} total):")
    for pattern, funcs in sorted(logging_patterns.items()):
        print(f"  {pattern}: {len(funcs)} functions")
    print()

# Check for functions that might need consolidation
print("=" * 80)
print("FUNCTIONS THAT MIGHT NEED CONSOLIDATION")
print("=" * 80)
print()

# Look for very similar function names
similar_groups = []
checked = set()

for func1 in sorted(functions):
    if func1 in checked:
        continue
    
    group = [func1]
    checked.add(func1)
    
    # Find similar functions (differ by only a few words)
    parts1 = func1.split('_')
    
    for func2 in sorted(functions):
        if func2 == func1 or func2 in checked:
            continue
        
        parts2 = func2.split('_')
        
        # If they share most parts, they might be duplicates
        common = set(parts1) & set(parts2)
        if len(common) >= len(parts1) - 2 and len(parts1) >= 4:
            group.append(func2)
            checked.add(func2)
    
    if len(group) > 1:
        similar_groups.append(group)

consolidation_candidates = 0
for group in sorted(similar_groups, key=lambda x: -len(x))[:20]:
    if len(group) > 1:
        consolidation_candidates += len(group) - 1
        print(f"Potential consolidation group ({len(group)} functions):")
        for func in sorted(group):
            print(f"  - {func} ({function_counts[func]}x)")
        print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total AWS functions:               {len(functions)}")
print(f"Potential duplicate groups found:  {len([g for g in similar_groups if len(g) > 1])}")
print(f"Potential consolidation candidates: {consolidation_candidates}")
print(f"Encryption naming patterns:        {len(encryption_patterns)}")
print(f"Logging naming patterns:           {len(logging_patterns)}")
print()

