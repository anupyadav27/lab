#!/usr/bin/env python3
"""
Context-Based AWS Expert Mapping
Uses compliance requirement descriptions to understand what each function should check
Then applies AWS expertise to map appropriately
"""
import csv
import json
from collections import defaultdict

COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
SIMPLE_MAPPING = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/aws_simple_mapping.json"
OUTPUT_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_CONTEXT_BASED_MAPPING.json"

print("=" * 100)
print("AWS EXPERT MAPPING - Using Compliance Requirement Context")
print("=" * 100)
print()

# Step 1: Build full context for each compliance function
print("Loading full context from compliance CSV...")
function_full_context = defaultdict(lambda: {
    'usage_count': 0,
    'frameworks': set(),
    'requirements': [],
    'descriptions': []
})

with open(COMPLIANCE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        aws_uniform = row.get('aws_uniform_format', '')
        
        if aws_uniform and aws_uniform != 'NA':
            for func in aws_uniform.split(';'):
                func = func.strip()
                if func and func != 'NA':
                    function_full_context[func]['usage_count'] += 1
                    function_full_context[func]['frameworks'].add(row.get('compliance_framework', ''))
                    
                    # Get requirement details
                    req_id = row.get('requirement_id', '')
                    req_name = row.get('requirement_name', '')
                    req_desc = row.get('requirement_description', '')
                    
                    if req_id and len(function_full_context[func]['requirements']) < 3:
                        function_full_context[func]['requirements'].append({
                            'id': req_id,
                            'name': req_name,
                            'description': req_desc[:250] if req_desc and req_desc != 'NA' else 'No description'
                        })

print(f"✓ Loaded full context for {len(function_full_context)} functions")
print()

# Load simple mapping
with open(SIMPLE_MAPPING, 'r') as f:
    simple_map = json.load(f)

# Focus on critical services
CRITICAL_SERVICES = [
    'guardduty', 'cloudtrail', 'iam', 's3', 'ec2', 
    'cloudwatch', 'kms', 'rds', 'vpc', 'lambda',
    'elbv2', 'elb', 'backup', 'securityhub', 'inspector',
    'config', 'sns', 'sqs', 'dynamodb', 'apigateway'
]

print("Creating context-based expert mappings...")
print()

context_map = {
    'metadata': {
        'date': '2025-11-09',
        'version': '3.0 - Context-Based',
        'methodology': 'Using compliance requirement descriptions + AWS expertise'
    },
    'services': {}
}

total_functions = 0
total_mapped = 0

for service in CRITICAL_SERVICES:
    if service not in simple_map:
        continue
    
    service_data = simple_map[service]
    rules = service_data.get('rules', [])
    compliance_funcs = service_data.get('compliance_functions', [])
    
    if not compliance_funcs:
        continue
    
    service_mappings = []
    
    for comp_func in compliance_funcs:
        context = function_full_context.get(comp_func, {})
        
        # Build rich context view
        frameworks = ', '.join(sorted(context.get('frameworks', set())))
        requirements = context.get('requirements', [])
        usage = context.get('usage_count', 0)
        
        # Extract key information for mapping decision
        requirement_context = ''
        if requirements:
            # Use first requirement for context
            req = requirements[0]
            requirement_context = f"{req['id']}: {req['name']}"
            description_context = req['description']
        else:
            requirement_context = 'No requirement details'
            description_context = ''
        
        # Now make expert mapping decision with full context
        mapping_entry = {
            'compliance_function': comp_func,
            'usage_count': usage,
            'frameworks': frameworks,
            'requirement_context': requirement_context,
            'requirement_description': description_context,
            'available_rules': rules,
            'mapped_to': [],
            'status': 'NEEDS_REVIEW',
            'confidence': 'N/A',
            'expert_reasoning': ''
        }
        
        service_mappings.append(mapping_entry)
        total_functions += 1
    
    context_map['services'][service] = {
        'service_name': service,
        'rule_count': len(rules),
        'compliance_count': len(compliance_funcs),
        'mappings': service_mappings
    }
    
    print(f"  ✓ {service:15s} {len(compliance_funcs)} functions with full context")

# Save
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(context_map, f, indent=2)

print()
print(f"✓ Saved: {OUTPUT_FILE}")
print()
print("=" * 100)
print("CONTEXT-BASED MAPPING READY FOR EXPERT REVIEW")
print("=" * 100)
print()
print(f"Total services: {len(context_map['services'])}")
print(f"Total functions: {total_functions}")
print()
print("Each function now includes:")
print("  - Compliance requirement context (ID, name, description)")
print("  - Usage count across frameworks")
print("  - Available rules for mapping")
print("  - Ready for expert mapping decision")
print()
print("NOW you can review each function with full context and make proper mapping decisions!")

