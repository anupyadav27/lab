"""
Analyze AWS Services for Duplicate Functions by Purpose/Job
Find functions within AWS that do the same thing but have different names
"""

import json
from pathlib import Path
from collections import defaultdict
import re

OUTPUT_DIR = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule")
AWS_FILE = OUTPUT_DIR / "aws_functions_by_service_2025-11-08.json"

def extract_function_keywords(function_name):
    """Extract key purpose words from function name"""
    # Remove aws_ prefix
    name = function_name.replace('aws_', '')
    
    # Remove service name (first part usually)
    parts = name.split('_')
    if len(parts) > 1:
        # Get all parts except first (service name)
        keywords = parts[1:]
    else:
        keywords = parts
    
    return set(keywords)

def get_function_purpose(function_name):
    """Get the main purpose/action of the function"""
    name = function_name.replace('aws_', '')
    parts = name.split('_')
    
    # Common action words that indicate purpose
    action_words = {'enabled', 'disabled', 'configured', 'encrypted', 'public', 'private',
                   'logging', 'monitoring', 'backup', 'protected', 'secure', 'restricted',
                   'attached', 'detached', 'allowed', 'denied', 'check', 'exists',
                   'created', 'deleted', 'updated', 'rotation', 'expired', 'valid'}
    
    # Extract actions
    actions = [p for p in parts if p in action_words]
    
    # Extract resource type (usually early in name)
    resource_words = {'bucket', 'instance', 'volume', 'snapshot', 'key', 'user', 'group',
                     'role', 'policy', 'vpc', 'subnet', 'security', 'network', 'database',
                     'cluster', 'table', 'queue', 'topic', 'stream'}
    
    resources = [p for p in parts if p in resource_words]
    
    return {
        'actions': actions,
        'resources': resources,
        'all_parts': parts
    }

print("=" * 80)
print("ANALYZING AWS FUNCTIONS FOR DUPLICATES BY PURPOSE")
print("=" * 80)
print()

# Load AWS functions
with open(AWS_FILE, 'r') as f:
    data = json.load(f)

print(f"Total AWS services: {data['metadata']['total_services']}")
print(f"Total AWS functions: {data['metadata']['total_functions']}")
print()

# Collect all functions with their details
all_functions = []
for service_name, service_data in data['services'].items():
    for func_name, func_data in service_data['functions'].items():
        purpose = get_function_purpose(func_name)
        all_functions.append({
            'service': service_name,
            'function': func_name,
            'purpose': purpose,
            'compliance_count': func_data['compliance_count'],
            'compliance_ids': set(func_data['compliance_ids'])
        })

# Find similar functions
print("=" * 80)
print("FINDING SIMILAR FUNCTIONS (Same Actions + Same Resources)")
print("=" * 80)
print()

similar_groups = defaultdict(list)

for i, func1 in enumerate(all_functions):
    for func2 in all_functions[i+1:]:
        # Check if they have similar purpose
        actions1 = set(func1['purpose']['actions'])
        actions2 = set(func2['purpose']['actions'])
        resources1 = set(func1['purpose']['resources'])
        resources2 = set(func2['purpose']['resources'])
        
        # If they share actions or resources
        shared_actions = actions1 & actions2
        shared_resources = resources1 & resources2
        
        if shared_actions and shared_resources:
            # They might be similar
            key = (tuple(sorted(shared_actions)), tuple(sorted(shared_resources)))
            similar_groups[key].append((func1, func2))

# Analyze and display results
duplicate_groups = []

for key, pairs in similar_groups.items():
    actions, resources = key
    
    # Get unique functions from pairs
    funcs_in_group = {}
    for func1, func2 in pairs:
        funcs_in_group[func1['function']] = func1
        funcs_in_group[func2['function']] = func2
    
    if len(funcs_in_group) >= 2:
        duplicate_groups.append({
            'actions': list(actions),
            'resources': list(resources),
            'functions': list(funcs_in_group.values())
        })

# Sort by number of functions in group
duplicate_groups.sort(key=lambda x: len(x['functions']), reverse=True)

print(f"Found {len(duplicate_groups)} groups of similar functions")
print()

# Display top groups
print("TOP 30 GROUPS OF SIMILAR FUNCTIONS:")
print("=" * 80)
print()

for i, group in enumerate(duplicate_groups[:30], 1):
    print(f"{i}. Similar Functions ({len(group['functions'])} functions)")
    print(f"   Common Actions: {', '.join(group['actions']) if group['actions'] else 'None'}")
    print(f"   Common Resources: {', '.join(group['resources']) if group['resources'] else 'None'}")
    print()
    
    for func in group['functions']:
        print(f"   • [{func['service']}] {func['function']}")
        print(f"     Compliance mappings: {func['compliance_count']}")
    
    # Check if any share compliance IDs
    if len(group['functions']) > 1:
        shared_ids = group['functions'][0]['compliance_ids'].copy()
        for func in group['functions'][1:]:
            shared_ids &= func['compliance_ids']
        
        if shared_ids:
            print(f"\n   ⚠️  {len(shared_ids)} shared compliance IDs across these functions!")
            print(f"   This suggests they might be doing the same job!")
    
    print()

# Find exact duplicate purposes (same service, similar names)
print("=" * 80)
print("FUNCTIONS IN SAME SERVICE WITH SIMILAR NAMES")
print("=" * 80)
print()

by_service = defaultdict(list)
for func in all_functions:
    by_service[func['service']].append(func)

same_service_similars = []
for service, funcs in by_service.items():
    if len(funcs) < 2:
        continue
    
    for i, func1 in enumerate(funcs):
        for func2 in funcs[i+1:]:
            # Calculate name similarity
            name1_parts = set(func1['function'].split('_'))
            name2_parts = set(func2['function'].split('_'))
            
            shared = name1_parts & name2_parts
            
            # If they share 60%+ of words
            similarity = len(shared) / max(len(name1_parts), len(name2_parts))
            
            if similarity >= 0.6:
                same_service_similars.append({
                    'service': service,
                    'func1': func1,
                    'func2': func2,
                    'similarity': similarity,
                    'shared_words': len(shared)
                })

same_service_similars.sort(key=lambda x: x['similarity'], reverse=True)

print(f"Found {len(same_service_similars)} pairs of similar functions in same service")
print()

for i, pair in enumerate(same_service_similars[:20], 1):
    print(f"{i}. Service: {pair['service']}")
    print(f"   Similarity: {pair['similarity']*100:.1f}% ({pair['shared_words']} shared words)")
    print(f"   Function 1: {pair['func1']['function']}")
    print(f"     Mappings: {pair['func1']['compliance_count']}")
    print(f"   Function 2: {pair['func2']['function']}")
    print(f"     Mappings: {pair['func2']['compliance_count']}")
    
    # Check for shared compliance IDs
    shared_ids = pair['func1']['compliance_ids'] & pair['func2']['compliance_ids']
    if shared_ids:
        print(f"   ⚠️  Share {len(shared_ids)} compliance IDs - likely duplicates!")
    
    print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()
print(f"Total function groups with similar purpose: {len(duplicate_groups)}")
print(f"Pairs of similar functions in same service: {len(same_service_similars)}")
print()

# Save report
report = {
    'summary': {
        'total_services': data['metadata']['total_services'],
        'total_functions': data['metadata']['total_functions'],
        'similar_groups': len(duplicate_groups),
        'same_service_pairs': len(same_service_similars)
    },
    'duplicate_groups': duplicate_groups[:50],  # Top 50
    'same_service_similars': same_service_similars[:30]  # Top 30
}

report_file = OUTPUT_DIR / "aws_duplicate_functions_analysis_2025-11-08.json"
with open(report_file, 'w', encoding='utf-8') as f:
    # Convert sets to lists for JSON serialization
    def convert_sets(obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, dict):
            return {k: convert_sets(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_sets(item) for item in obj]
        return obj
    
    json.dump(convert_sets(report), f, indent=2)

print(f"Detailed report saved: {report_file}")
print()

