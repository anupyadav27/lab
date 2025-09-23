import json
import csv

# Read Azure compliance data
with open('azure_final_sdk_service_function_grouped_enhanced.json', 'r') as f:
    azure_data = json.load(f)

# Prepare CSV data
csv_data = []
for sdk_package, services in azure_data.items():
    for service_name, functions in services.items():
        for function in functions:
            csv_data.append({
                'program_name': function,
                'provider': 'Azure',
                'service': service_name,
                'short_description': f"Azure {service_name} compliance check"
            })

# Write to CSV
with open('azure_compliance_programs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['program_name', 'provider', 'service', 'short_description'])
    writer.writeheader()
    writer.writerows(csv_data)

print(f"Created azure_compliance_programs.csv with {len(csv_data)} records")
