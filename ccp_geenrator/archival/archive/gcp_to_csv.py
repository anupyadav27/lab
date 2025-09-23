import json
import csv

# Read GCP compliance data
with open('gcp_security_functions_filtered.json', 'r') as f:
    gcp_data = json.load(f)

# Prepare CSV data
csv_data = []
for sdk_package, services in gcp_data['sdk_packages'].items():
    for service_name, functions in services.items():
        for function in functions:
            csv_data.append({
                'program_name': function,
                'provider': 'GCP',
                'service': service_name,
                'short_description': f"GCP {service_name} security compliance check"
            })

# Write to CSV
with open('gcp_compliance_programs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['program_name', 'provider', 'service', 'short_description'])
    writer.writeheader()
    writer.writerows(csv_data)

print(f"Created gcp_compliance_programs.csv with {len(csv_data)} records")
