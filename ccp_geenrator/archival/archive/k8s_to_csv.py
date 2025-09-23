import json
import csv

# Read Kubernetes compliance data
with open('kubernetes_security_functions_optimized_v2.json', 'r') as f:
    k8s_data = json.load(f)

# Prepare CSV data
csv_data = []
for category, functions in k8s_data.items():
    for function_name, function_data in functions.items():
        if isinstance(function_data, dict) and 'description' in function_data:
            description = function_data['description']
        else:
            description = f"Kubernetes {category} compliance check"
        
        csv_data.append({
            'program_name': function_name,
            'provider': 'Kubernetes',
            'service': category,
            'short_description': description
        })

# Write to CSV
with open('k8s_compliance_programs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['program_name', 'provider', 'service', 'short_description'])
    writer.writeheader()
    writer.writerows(csv_data)

print(f"Created k8s_compliance_programs.csv with {len(csv_data)} records")
