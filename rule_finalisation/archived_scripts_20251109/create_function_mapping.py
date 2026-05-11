"""
Create Function Normalization Mapping
Maps duplicate function names to a single canonical name
"""

import json
from pathlib import Path
from collections import defaultdict

INPUT_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functions_by_service_2025-11-08.json")
OUTPUT_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/function_normalization_mapping.json")

with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

# Build normalization mapping
function_mapping = {}
statistics = {
    'total_functions': 0,
    'duplicates_found': 0,
    'mappings_created': 0
}

# Collect all functions
all_functions = {}
for service, functions in data.items():
    for func, ids in functions.items():
        all_functions[func] = {
            'service': service,
            'compliance_ids': ids,
            'count': len(ids)
        }
        statistics['total_functions'] += 1

# 1. Fix repeated service names (e.g., aws_s3_s3_bucket -> aws_s3_bucket)
print("=" * 80)
print("CREATING FUNCTION NORMALIZATION MAPPING")
print("=" * 80)
print()
print("Step 1: Fixing repeated service names...")

repeated_fixes = {}
for func in all_functions.keys():
    parts = func.split('_')
    if len(parts) >= 4 and parts[0] == 'aws' and parts[1] == parts[2]:
        # aws_service_service_* -> aws_service_*
        canonical = '_'.join([parts[0], parts[1]] + parts[3:])
        repeated_fixes[func] = canonical
        print(f"  {func} -> {canonical}")

statistics['duplicates_found'] += len(repeated_fixes)
statistics['mappings_created'] += len(repeated_fixes)

# 2. Normalize aws_ prefix variations (prefer aws_ prefix)
print()
print("Step 2: Normalizing aws_ prefix variations...")

# Group by normalized name
normalized_groups = defaultdict(list)
for func, info in all_functions.items():
    # Skip if already in repeated_fixes
    if func in repeated_fixes:
        continue
    
    normalized = func.replace('aws_', '', 1) if func.startswith('aws_') else func
    normalized_groups[normalized].append((func, info['count']))

# For each group with multiple variations, choose canonical
prefix_fixes = {}
for normalized, variations in normalized_groups.items():
    if len(variations) > 1:
        # Sort by: 1) prefer aws_ prefix, 2) most mappings
        variations_sorted = sorted(variations, key=lambda x: (not x[0].startswith('aws_'), -x[1]))
        canonical = variations_sorted[0][0]
        
        for func, count in variations:
            if func != canonical:
                prefix_fixes[func] = canonical
                print(f"  {func} -> {canonical}")
        
        statistics['duplicates_found'] += len(variations) - 1
        statistics['mappings_created'] += len(variations) - 1

# 3. Combine all mappings
function_mapping = {**repeated_fixes, **prefix_fixes}

# 4. Create reverse mapping (canonical -> all variants)
canonical_to_variants = defaultdict(list)
for variant, canonical in function_mapping.items():
    canonical_to_variants[canonical].append(variant)

print()
print("=" * 80)
print("NORMALIZATION MAPPING CREATED")
print("=" * 80)
print()
print(f"Total functions analyzed: {statistics['total_functions']}")
print(f"Duplicate variations found: {statistics['duplicates_found']}")
print(f"Normalization mappings created: {statistics['mappings_created']}")
print()

# Save mapping
output_data = {
    'description': 'Function normalization mapping for AWS compliance checks',
    'statistics': statistics,
    'variant_to_canonical': function_mapping,
    'canonical_to_variants': {k: v for k, v in canonical_to_variants.items()}
}

with open(OUTPUT_FILE, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"Mapping saved to: {OUTPUT_FILE}")
print()

# Show most impactful normalizations
print("=" * 80)
print("TOP 20 NORMALIZATIONS (by total compliance mappings affected)")
print("=" * 80)
print()

# Calculate impact
impact_list = []
for canonical, variants in canonical_to_variants.items():
    total_mappings = 0
    for func in [canonical] + variants:
        if func in all_functions:
            total_mappings += all_functions[func]['count']
    impact_list.append((canonical, variants, total_mappings))

impact_list.sort(key=lambda x: x[2], reverse=True)

for i, (canonical, variants, total_mappings) in enumerate(impact_list[:20], 1):
    print(f"{i}. {canonical}")
    print(f"   Total compliance mappings: {total_mappings}")
    print(f"   Variants ({len(variants)}):")
    for variant in variants:
        count = all_functions.get(variant, {}).get('count', 0)
        print(f"     - {variant} ({count} mappings)")
    print()

print("=" * 80)
print()

