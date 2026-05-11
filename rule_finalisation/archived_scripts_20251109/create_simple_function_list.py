"""
Create Simple AWS Function List Categorized by Service
Just function names grouped by service - nothing else
"""

import csv
import json
from pathlib import Path
from collections import defaultdict

INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08.csv")
OUTPUT_JSON = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functions_by_service_simple.json")

def extract_service_from_function(function_name):
    """Extract service name from AWS function name"""
    # Remove aws_ prefix
    if function_name.startswith('aws_'):
        name = function_name[4:]  # Remove 'aws_'
        parts = name.split('_')
        if parts:
            return parts[0]  # First part is usually the service
    return 'unknown'

print("=" * 80)
print("CREATING SIMPLE AWS FUNCTION LIST BY SERVICE")
print("=" * 80)
print()

# Collect all unique AWS functions
aws_functions = set()

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        aws_checks = row.get('aws_checks', '')
        
        if aws_checks and aws_checks != 'NA':
            # Parse functions (semicolon-separated)
            functions = [f.strip() for f in aws_checks.split(';') if f.strip()]
            
            for func in functions:
                # Skip invalid entries
                if 'no checks defined' not in func.lower():
                    aws_functions.add(func)

print(f"Total unique AWS functions found: {len(aws_functions)}")
print()

# Group by service
functions_by_service = defaultdict(list)

for func in sorted(aws_functions):
    service = extract_service_from_function(func)
    functions_by_service[service].append(func)

# Sort functions within each service
for service in functions_by_service:
    functions_by_service[service] = sorted(functions_by_service[service])

# Convert to regular dict and sort by service name
output = {service: functions_by_service[service] 
          for service in sorted(functions_by_service.keys())}

# Save to JSON
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"Services found: {len(output)}")
print()

# Show summary
print("Service Summary:")
print(f"{'Service':<25} {'Function Count':<15}")
print("-" * 80)

for service in sorted(output.keys()):
    print(f"{service:<25} {len(output[service]):<15}")

print()
print(f"✅ Simple function list saved: {OUTPUT_JSON}")
print()

