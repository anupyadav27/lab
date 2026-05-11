"""
Create Service-Grouped List of High Overlap Functions
Focus on functions in same service with 80%+ compliance overlap
"""

import json
from pathlib import Path
from collections import defaultdict

INPUT_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_true_duplicates_analysis_2025-11-08.json")
OUTPUT_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_high_overlap_by_service_2025-11-08.json")

# Load the analysis
with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

print("=" * 80)
print("HIGH OVERLAP FUNCTIONS GROUPED BY SERVICE")
print("=" * 80)
print()

# Get high overlap pairs
high_overlap_pairs = data.get('high_overlap_same_service', [])

print(f"Total pairs with 80%+ overlap: {len(high_overlap_pairs)}")
print()

# Group by service
by_service = defaultdict(list)

for pair in high_overlap_pairs:
    service = pair['service']
    by_service[service].append(pair)

print(f"Services with high overlap pairs: {len(by_service)}")
print()

# Create clean, grouped output
service_groups = {}

for service in sorted(by_service.keys()):
    pairs = by_service[service]
    
    # Count unique functions involved
    functions_involved = set()
    for pair in pairs:
        functions_involved.add(pair['function_1']['name'])
        functions_involved.add(pair['function_2']['name'])
    
    service_groups[service] = {
        'service_name': service,
        'total_pairs': len(pairs),
        'unique_functions_involved': len(functions_involved),
        'pairs': []
    }
    
    # Sort pairs by overlap percentage
    pairs_sorted = sorted(pairs, key=lambda x: x['overlap_percentage'], reverse=True)
    
    for pair in pairs_sorted:
        service_groups[service]['pairs'].append({
            'overlap_percentage': pair['overlap_percentage'],
            'shared_compliance_count': pair['shared_compliance_count'],
            'function_1': {
                'name': pair['function_1']['name'],
                'total_mappings': pair['function_1']['total_mappings'],
                'unique_mappings': pair['function_1']['unique_mappings']
            },
            'function_2': {
                'name': pair['function_2']['name'],
                'total_mappings': pair['function_2']['total_mappings'],
                'unique_mappings': pair['function_2']['unique_mappings']
            },
            'analysis': pair['analysis']
        })

# Save to file
with open(OUTPUT_FILE, 'w') as f:
    json.dump(service_groups, f, indent=2)

print(f"Service-grouped output saved: {OUTPUT_FILE}")
print()

# Display summary by service
print("=" * 80)
print("SUMMARY BY SERVICE")
print("=" * 80)
print()

# Sort by number of pairs
service_summary = [(service, data['total_pairs'], data['unique_functions_involved']) 
                   for service, data in service_groups.items()]
service_summary.sort(key=lambda x: x[1], reverse=True)

print(f"{'Service':<25} {'Pairs':<10} {'Functions':<12}")
print("-" * 80)

for service, pair_count, func_count in service_summary:
    print(f"{service:<25} {pair_count:<10} {func_count:<12}")

print()

# Show detailed view for top services
print("=" * 80)
print("DETAILED VIEW - TOP 10 SERVICES")
print("=" * 80)
print()

for service, pair_count, func_count in service_summary[:10]:
    service_data = service_groups[service]
    
    print(f"\n{'=' * 80}")
    print(f"SERVICE: {service.upper()}")
    print(f"{'=' * 80}")
    print(f"Total Pairs: {pair_count}")
    print(f"Unique Functions: {func_count}")
    print()
    
    # Show top 10 pairs
    for i, pair in enumerate(service_data['pairs'][:10], 1):
        print(f"{i}. Overlap: {pair['overlap_percentage']}% ({pair['shared_compliance_count']} shared)")
        print(f"   Analysis: {pair['analysis']}")
        print()
        print(f"   Function 1: {pair['function_1']['name']}")
        print(f"     Total: {pair['function_1']['total_mappings']} | Unique: {pair['function_1']['unique_mappings']}")
        print()
        print(f"   Function 2: {pair['function_2']['name']}")
        print(f"     Total: {pair['function_2']['total_mappings']} | Unique: {pair['function_2']['unique_mappings']}")
        print()
    
    if len(service_data['pairs']) > 10:
        print(f"   ... and {len(service_data['pairs']) - 10} more pairs")
        print()

print()
print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print()
print(f"Service-grouped JSON: {OUTPUT_FILE}")
print()

