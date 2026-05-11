"""
Extract AWS Functions and Group by Service
Groups all AWS functions with their associated unique compliance IDs
"""

import csv
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Input/Output paths
INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08.csv")
OUTPUT_DIR = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule")
OUTPUT_FILE = OUTPUT_DIR / f"aws_functions_by_service_{datetime.now().strftime('%Y-%m-%d')}.json"

def extract_service_from_function(function_name):
    """Extract service name from AWS function name"""
    # Format: aws_service_function
    parts = function_name.split('_')
    if len(parts) >= 2 and parts[0] == 'aws':
        return parts[1]
    return 'unknown'

def main():
    print("=" * 80)
    print("AWS FUNCTIONS EXTRACTION AND GROUPING")
    print("=" * 80)
    print()
    
    # Data structure: {service: {function_name: [unique_ids]}}
    aws_functions = defaultdict(lambda: defaultdict(set))
    
    # Read consolidated CSV
    print(f"Reading: {INPUT_CSV}")
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            unique_id = row['unique_compliance_id']
            aws_checks = row.get('aws_checks', '')
            
            # Skip if no AWS checks
            if not aws_checks or aws_checks == 'NA':
                continue
            
            # Parse AWS checks (semicolon-separated)
            checks = [c.strip() for c in aws_checks.split(';') if c.strip()]
            
            for check in checks:
                # Extract service from function name
                service = extract_service_from_function(check)
                
                # Add to data structure
                aws_functions[service][check].add(unique_id)
    
    # Convert sets to sorted lists for JSON serialization
    aws_functions_json = {}
    for service in sorted(aws_functions.keys()):
        aws_functions_json[service] = {}
        for function in sorted(aws_functions[service].keys()):
            aws_functions_json[service][function] = sorted(list(aws_functions[service][function]))
    
    # Calculate statistics
    total_services = len(aws_functions_json)
    total_functions = sum(len(funcs) for funcs in aws_functions_json.values())
    total_mappings = sum(len(ids) for service_funcs in aws_functions_json.values() 
                        for ids in service_funcs.values())
    
    print()
    print("Statistics:")
    print(f"  Total AWS Services: {total_services}")
    print(f"  Total AWS Functions: {total_functions}")
    print(f"  Total Compliance Mappings: {total_mappings}")
    print()
    
    # Show top services by function count
    print("Top 10 Services by Function Count:")
    service_counts = [(service, len(funcs)) for service, funcs in aws_functions_json.items()]
    service_counts.sort(key=lambda x: x[1], reverse=True)
    for i, (service, count) in enumerate(service_counts[:10], 1):
        print(f"  {i:2}. {service:20} : {count:3} functions")
    print()
    
    # Write JSON output
    print(f"Writing: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(aws_functions_json, f, indent=2)
    
    print()
    print("=" * 80)
    print("EXTRACTION COMPLETE!")
    print("=" * 80)
    print()
    print(f"Output file: {OUTPUT_FILE}")
    print()

if __name__ == "__main__":
    main()

