import json
import csv

# Read AWS compliance data
with open('service_function_list_by_service_updated_with_compliance.json', 'r') as f:
    aws_data = json.load(f)

# Prepare CSV data
csv_data = []
for service_name, service_data in aws_data['services'].items():
    # Process programmable functions
    for function in service_data.get('programmable', []):
        csv_data.append({
            'program_name': function,
            'provider': 'AWS',
            'service': service_name,
            'short_description': f"AWS {service_name} programmable compliance check"
        })
    
    # Process manual functions
    for function in service_data.get('manual', []):
        csv_data.append({
            'program_name': function,
            'provider': 'AWS',
            'service': service_name,
            'short_description': f"AWS {service_name} manual compliance check"
        })

# Write to CSV
with open('aws_compliance_programs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['program_name', 'provider', 'service', 'short_description'])
    writer.writeheader()
    writer.writerows(csv_data)

print(f"Created aws_compliance_programs.csv with {len(csv_data)} records")
