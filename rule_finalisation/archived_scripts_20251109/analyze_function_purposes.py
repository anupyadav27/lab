"""
Analyze All Services for Duplicate Functions by Purpose/Job
Find functions that do the same thing but have different names
"""

import json
from pathlib import Path
from collections import defaultdict
import re

OUTPUT_DIR = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule")

CSP_FILES = {
    'AWS': 'aws_functions_by_service_2025-11-08.json',
    'Azure': 'azure_functions_by_service_2025-11-08.json',
    'GCP': 'gcp_functions_by_service_2025-11-08.json',
    'Oracle': 'oracle_functions_by_service_2025-11-08.json',
    'IBM': 'ibm_functions_by_service_2025-11-08.json',
    'Alicloud': 'alicloud_functions_by_service_2025-11-08.json',
    'Kubernetes': 'kubernetes_functions_by_service_2025-11-08.json'
}

def extract_function_purpose(function_name):
    """Extract the purpose/job from function name"""
    # Remove CSP prefix
    name = function_name
    for prefix in ['aws_', 'azure_', 'gcp_', 'oracle_', 'ibm_', 'alicloud_', 'k8s_', 'oci_', 'azurerm_']:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    
    # Remove service name (first part)
    parts = name.split('_')
    if len(parts) > 1:
        # Skip first part (usually service name)
        purpose_parts = parts[1:]
        purpose = '_'.join(purpose_parts)
    else:
        purpose = name
    
    return purpose.lower().strip()

print("=" * 80)
print("ANALYZING FUNCTIONS BY PURPOSE (JOB) - FINDING DUPLICATES")
print("=" * 80)
print()

# Structure: {purpose: [(csp, service, function_name, compliance_count)]}
functions_by_purpose = defaultdict(list)

# Load all functions from all CSPs
for csp_name, filename in CSP_FILES.items():
    filepath = OUTPUT_DIR / filename
    
    print(f"Loading {csp_name}...")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    for service_name, service_data in data['services'].items():
        for func_name, func_data in service_data['functions'].items():
            purpose = extract_function_purpose(func_name)
            
            functions_by_purpose[purpose].append({
                'csp': csp_name,
                'service': service_name,
                'function': func_name,
                'compliance_count': func_data['compliance_count'],
                'compliance_ids': func_data['compliance_ids']
            })

print()
print("=" * 80)
print("FINDING FUNCTIONS WITH SAME PURPOSE")
print("=" * 80)
print()

# Find purposes with multiple functions
duplicates_by_purpose = {}
for purpose, functions in functions_by_purpose.items():
    if len(functions) > 1:
        # Group by CSP to see if same CSP has duplicates
        by_csp = defaultdict(list)
        for func in functions:
            by_csp[func['csp']].append(func)
        
        # Check if any CSP has multiple functions for same purpose
        has_csp_duplicates = any(len(funcs) > 1 for funcs in by_csp.values())
        
        duplicates_by_purpose[purpose] = {
            'functions': functions,
            'by_csp': dict(by_csp),
            'has_csp_duplicates': has_csp_duplicates,
            'total_count': len(functions)
        }

# Sort by count (most duplicates first)
sorted_duplicates = sorted(duplicates_by_purpose.items(), 
                          key=lambda x: x[1]['total_count'], 
                          reverse=True)

print(f"Found {len(sorted_duplicates)} purposes with multiple function implementations")
print()

# Show top duplicates
print("=" * 80)
print("TOP 30 FUNCTIONS WITH SAME PURPOSE (Most Duplicates)")
print("=" * 80)
print()

for i, (purpose, data) in enumerate(sorted_duplicates[:30], 1):
    print(f"{i}. Purpose: '{purpose}'")
    print(f"   Total implementations: {data['total_count']}")
    
    if data['has_csp_duplicates']:
        print(f"   ⚠️  WARNING: Same CSP has multiple implementations!")
    
    print()
    
    # Group by CSP
    for csp in sorted(data['by_csp'].keys()):
        funcs = data['by_csp'][csp]
        if len(funcs) > 1:
            print(f"   {csp} ({len(funcs)} functions) ⚠️  DUPLICATES IN SAME CSP:")
        else:
            print(f"   {csp} (1 function):")
        
        for func in funcs:
            print(f"     • [{func['service']}] {func['function']}")
            print(f"       Compliance mappings: {func['compliance_count']}")
    
    print()

# Analyze same-CSP duplicates
print("=" * 80)
print("SAME-CSP DUPLICATES (Most Critical)")
print("=" * 80)
print()

same_csp_duplicates = [(purpose, data) for purpose, data in sorted_duplicates 
                       if data['has_csp_duplicates']]

print(f"Found {len(same_csp_duplicates)} purposes with duplicates in SAME CSP")
print()

for i, (purpose, data) in enumerate(same_csp_duplicates[:20], 1):
    print(f"{i}. Purpose: '{purpose}'")
    
    for csp, funcs in data['by_csp'].items():
        if len(funcs) > 1:
            print(f"\n   ❌ {csp} has {len(funcs)} functions doing the same thing:")
            for func in funcs:
                print(f"      • {func['function']}")
                print(f"        Service: {func['service']}, Mappings: {func['compliance_count']}")
                
                # Check if they map to same compliance IDs
                if len(funcs) > 1:
                    ids_set = set(func['compliance_ids'])
                    other_ids = set()
                    for other_func in funcs:
                        if other_func != func:
                            other_ids.update(other_func['compliance_ids'])
                    
                    shared = ids_set & other_ids
                    if shared:
                        print(f"        ⚠️  Shares {len(shared)} compliance IDs with other functions")
    
    print()

# Summary statistics
print("=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)
print()

print(f"Total unique purposes: {len(functions_by_purpose)}")
print(f"Purposes with multiple implementations: {len(sorted_duplicates)}")
print(f"Purposes with same-CSP duplicates: {len(same_csp_duplicates)}")
print()

print("By Cloud Provider - Same-CSP Duplicates:")
csp_dup_count = defaultdict(int)
for purpose, data in same_csp_duplicates:
    for csp, funcs in data['by_csp'].items():
        if len(funcs) > 1:
            csp_dup_count[csp] += 1

for csp in sorted(csp_dup_count.keys()):
    print(f"  {csp:12} : {csp_dup_count[csp]:3} duplicate purposes")

print()

# Save report
report = {
    'total_purposes': len(functions_by_purpose),
    'duplicate_purposes': len(sorted_duplicates),
    'same_csp_duplicates': len(same_csp_duplicates),
    'details': {purpose: {
        'total_count': data['total_count'],
        'has_csp_duplicates': data['has_csp_duplicates'],
        'functions': data['functions']
    } for purpose, data in sorted_duplicates[:50]}  # Top 50
}

report_file = OUTPUT_DIR / "duplicate_functions_by_purpose_2025-11-08.json"
with open(report_file, 'w') as f:
    json.dump(report, f, indent=2)

print(f"Detailed report saved: {report_file}")
print()

