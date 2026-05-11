"""
Create Finalized AWS Functions JSON with Enhanced Metadata
"""

import json
from pathlib import Path
from datetime import datetime

INPUT_JSON = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functions_by_service_2025-11-08.json")
OUTPUT_JSON = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functions_by_service_final.json")

# Load the normalized data
with open(INPUT_JSON, 'r') as f:
    data = json.load(f)

# Create enhanced structure with metadata
finalized_data = {
    "metadata": {
        "version": "1.0",
        "generated_date": datetime.now().strftime("%Y-%m-%d"),
        "description": "AWS compliance check functions organized by service category",
        "total_services": len(data),
        "total_functions": sum(len(funcs) for funcs in data.values()),
        "total_compliance_mappings": sum(len(ids) for service_funcs in data.values() for ids in service_funcs.values()),
        "normalization_applied": True,
        "notes": "All function names have been normalized to eliminate duplicates"
    },
    "services": {}
}

# Process each service
print("=" * 80)
print("CREATING FINALIZED AWS FUNCTIONS JSON")
print("=" * 80)
print()

for service in sorted(data.keys()):
    functions = data[service]
    
    # Create service entry with metadata
    service_data = {
        "service_name": service,
        "function_count": len(functions),
        "total_compliance_mappings": sum(len(ids) for ids in functions.values()),
        "functions": {}
    }
    
    # Add each function with details
    for func_name in sorted(functions.keys()):
        compliance_ids = functions[func_name]
        service_data["functions"][func_name] = {
            "function_name": func_name,
            "compliance_count": len(compliance_ids),
            "compliance_ids": sorted(compliance_ids)
        }
    
    finalized_data["services"][service] = service_data

# Write finalized JSON
print(f"Writing finalized JSON: {OUTPUT_JSON}")
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(finalized_data, f, indent=2)

print()
print("=" * 80)
print("FINALIZED JSON CREATED")
print("=" * 80)
print()
print(f"Metadata:")
print(f"  Version: {finalized_data['metadata']['version']}")
print(f"  Generated: {finalized_data['metadata']['generated_date']}")
print(f"  Total Services: {finalized_data['metadata']['total_services']}")
print(f"  Total Functions: {finalized_data['metadata']['total_functions']}")
print(f"  Total Compliance Mappings: {finalized_data['metadata']['total_compliance_mappings']}")
print()
print(f"Output file: {OUTPUT_JSON}")
print()

# Show sample structure
print("Sample structure:")
print("-" * 80)
sample_service = list(finalized_data['services'].keys())[0]
sample_service_data = finalized_data['services'][sample_service]
print(json.dumps({
    "metadata": finalized_data['metadata'],
    "services": {
        sample_service: {
            **{k: v for k, v in sample_service_data.items() if k != 'functions'},
            "functions": {
                list(sample_service_data['functions'].keys())[0]: list(sample_service_data['functions'].values())[0]
            }
        }
    }
}, indent=2))
print()

