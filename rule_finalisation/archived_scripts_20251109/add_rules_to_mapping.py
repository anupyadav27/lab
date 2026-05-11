#!/usr/bin/env python3
"""
Add available_rules section to each service in one-to-one mapping
"""
import json

SIMPLE_MAPPING = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/aws_simple_mapping.json"
ONE_TO_ONE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING.json"
OUTPUT = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING.json"

# Load both files
with open(SIMPLE_MAPPING, 'r') as f:
    simple_map = json.load(f)

with open(ONE_TO_ONE, 'r') as f:
    one_to_one = json.load(f)

print("Adding available_rules to each service...")

# Add available_rules to each service
for service, data in one_to_one.items():
    if service == 'metadata':
        continue
    
    if service in simple_map:
        rules = simple_map[service].get('rules', [])
        # Add available_rules as first item in service
        updated_service = {
            'available_rules': rules,
            'mapped': data.get('mapped', {}),
            'not_mapped': data.get('not_mapped', [])
        }
        one_to_one[service] = updated_service
        print(f"  ✓ {service}: {len(rules)} rules available")

# Save
with open(OUTPUT, 'w') as f:
    json.dump(one_to_one, f, indent=2)

print()
print(f"✓ Updated: {OUTPUT}")
print()
print("Each service now has:")
print("  - available_rules: [all rule_ids for this service]")
print("  - mapped: {compliance_function: rule_id}")
print("  - not_mapped: [functions needing development]")

