"""
Analyze AWS Functions for Duplicates and Similar Functions
"""

import json
from pathlib import Path
from collections import defaultdict
import re

INPUT_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functions_by_service_2025-11-08.json")

with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

print("=" * 80)
print("AWS FUNCTIONS DUPLICATE ANALYSIS")
print("=" * 80)
print()

# Collect all functions
all_functions = {}
for service, functions in data.items():
    for func, ids in functions.items():
        all_functions[func] = {
            'service': service,
            'compliance_ids': ids,
            'count': len(ids)
        }

print(f"Total unique function names: {len(all_functions)}")
print()

# 1. Find functions with repeated service names (e.g., aws_s3_s3_bucket_encryption)
print("=" * 80)
print("1. FUNCTIONS WITH REPEATED SERVICE NAMES")
print("=" * 80)
print()

repeated_service = []
for func, info in all_functions.items():
    # Check for patterns like aws_service_service_*
    parts = func.split('_')
    if len(parts) >= 4 and parts[0] == 'aws':
        if parts[1] == parts[2]:  # Repeated service name
            repeated_service.append((func, info['service'], len(info['compliance_ids'])))

if repeated_service:
    repeated_service.sort(key=lambda x: x[2], reverse=True)
    for func, service, count in repeated_service:
        # Suggest cleaned name
        parts = func.split('_')
        cleaned = '_'.join([parts[0], parts[1]] + parts[3:])  # Remove duplicate
        print(f"❌ {func}")
        print(f"   Service: {service}, Mappings: {count}")
        print(f"   Suggested: {cleaned}")
        print()

print(f"Total with repeated service names: {len(repeated_service)}")
print()

# 2. Find functions with/without aws_ prefix that might be duplicates
print("=" * 80)
print("2. FUNCTIONS WITH/WITHOUT 'aws_' PREFIX (Potential Duplicates)")
print("=" * 80)
print()

# Group by normalized name (without aws_ prefix)
normalized_groups = defaultdict(list)
for func, info in all_functions.items():
    # Normalize by removing aws_ prefix
    normalized = func.replace('aws_', '', 1) if func.startswith('aws_') else func
    normalized_groups[normalized].append((func, info['service'], len(info['compliance_ids'])))

# Find groups with multiple variations
duplicates = []
for normalized, variations in normalized_groups.items():
    if len(variations) > 1:
        duplicates.append((normalized, variations))

if duplicates:
    duplicates.sort(key=lambda x: sum(v[2] for v in x[1]), reverse=True)
    for i, (normalized, variations) in enumerate(duplicates[:20], 1):  # Top 20
        total_mappings = sum(v[2] for v in variations)
        print(f"{i}. Normalized: {normalized}")
        print(f"   Total mappings: {total_mappings}")
        for func, service, count in sorted(variations, key=lambda x: x[2], reverse=True):
            print(f"   - {func:60} [{service:15}] {count:3} mappings")
        print()

print(f"Total duplicate groups found: {len(duplicates)}")
print()

# 3. Find functions in "unknown" service that should be in proper services
print("=" * 80)
print("3. FUNCTIONS IN 'unknown' SERVICE (Should be Categorized)")
print("=" * 80)
print()

unknown_functions = []
if 'unknown' in data:
    for func, ids in data['unknown'].items():
        unknown_functions.append((func, len(ids)))
    
    unknown_functions.sort(key=lambda x: x[1], reverse=True)
    
    # Analyze patterns
    prefixed_with_service = []
    for func, count in unknown_functions:
        # Check if it starts with a known service name
        for service in data.keys():
            if service != 'unknown' and func.startswith(service + '_'):
                prefixed_with_service.append((func, service, count))
                break
    
    print(f"Total functions in 'unknown': {len(unknown_functions)}")
    print(f"Functions that start with known service names: {len(prefixed_with_service)}")
    print()
    
    if prefixed_with_service:
        print("Top 20 examples that could be recategorized:")
        prefixed_with_service.sort(key=lambda x: x[2], reverse=True)
        for i, (func, suggested_service, count) in enumerate(prefixed_with_service[:20], 1):
            print(f"{i:2}. {func:65} -> {suggested_service:15} ({count:3} mappings)")
        print()

# 4. Find exact semantic duplicates (different names, same purpose)
print("=" * 80)
print("4. POTENTIAL SEMANTIC DUPLICATES (Similar Names)")
print("=" * 80)
print()

# Extract key terms from function names
def extract_key_terms(func_name):
    # Remove aws_ prefix and service name
    terms = func_name.replace('aws_', '').split('_')
    # Remove common words
    stopwords = {'is', 'in', 'to', 'for', 'all', 'enabled', 'check', 'status', 'policy'}
    key_terms = [t for t in terms if t not in stopwords and len(t) > 2]
    return set(key_terms)

# Group by similar key terms
semantic_groups = defaultdict(list)
for func, info in all_functions.items():
    key_terms = extract_key_terms(func)
    if len(key_terms) >= 2:  # Only if at least 2 key terms
        key = tuple(sorted(key_terms))
        semantic_groups[key].append((func, info['service'], len(info['compliance_ids'])))

# Find groups with multiple functions
semantic_duplicates = []
for key_terms, functions in semantic_groups.items():
    if len(functions) > 1:
        total_mappings = sum(f[2] for f in functions)
        semantic_duplicates.append((key_terms, functions, total_mappings))

semantic_duplicates.sort(key=lambda x: x[2], reverse=True)

print("Top 15 groups with similar key terms:")
for i, (key_terms, functions, total_mappings) in enumerate(semantic_duplicates[:15], 1):
    print(f"{i}. Key terms: {', '.join(key_terms)}")
    print(f"   Total mappings: {total_mappings}")
    for func, service, count in sorted(functions, key=lambda x: x[2], reverse=True):
        print(f"   - {func:60} [{service:15}] {count:3} mappings")
    print()

print(f"Total semantic duplicate groups: {len(semantic_duplicates)}")
print()

# 5. Summary
print("=" * 80)
print("SUMMARY OF FINDINGS")
print("=" * 80)
print()
print(f"1. Functions with repeated service names: {len(repeated_service)}")
print(f"2. Functions with aws_ prefix variations: {len(duplicates)}")
print(f"3. Functions in 'unknown' category: {len(unknown_functions)}")
print(f"4. Semantic duplicate groups: {len(semantic_duplicates)}")
print()
print("Recommendation: Create a function mapping/normalization table to consolidate")
print("these duplicates in the CSV file.")
print()

