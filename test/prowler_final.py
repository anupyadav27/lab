import json
import csv

print("="*70)
print("PROWLER HUB - Creating Compliance CSVs")
print("="*70)

with open('prowler_frameworks_raw.json', 'r') as f:
    frameworks = json.load(f)

print(f"Loaded {len(frameworks)} frameworks\n")

all_records = []
for fw in frameworks:
    fw_id = fw.get('id', '')
    fw_name = fw.get('framework', '')
    fw_provider = fw.get('provider', 'Unknown')
    fw_description = fw.get('description', '')
    fw_version = str(fw.get('version', '')) if fw.get('version') else ''
    requirements = fw.get('requirements', [])
    print(f"{fw_name} ({fw_provider}): {len(requirements)} requirements")
    for req in requirements:
        attributes = req.get('attributes', [])
        service = attributes[0].get('service', '') if attributes else ''
        section = attributes[0].get('section', '') if attributes else ''
        checks = req.get('checks', [])
        all_records.append({
            'Technology': fw_provider.upper(),
            'Compliance Framework': fw_name,
            'Framework ID': fw_id,
            'Framework Version': fw_version,
            'Requirement ID': req.get('id', ''),
            'Requirement Name': req.get('name', ''),
            'Requirement Description': (req.get('description', '')[:200] + '...') if len(req.get('description', '')) > 200 else req.get('description', ''),
            'Section': section,
            'Service': service,
            'Total Checks': req.get('total_checks', len(checks)),
            'Check Names': ', '.join(checks) if checks else 'No checks defined',
            'Framework Description': (fw_description[:100] + '...') if len(fw_description) > 100 else fw_description
        })

print(f"\n{'='*70}")
print(f"Total Requirements: {len(all_records)}")

fieldnames = ['Technology', 'Compliance Framework', 'Framework ID', 'Framework Version', 'Requirement ID', 'Requirement Name', 'Requirement Description', 'Section', 'Service', 'Total Checks', 'Check Names', 'Framework Description']

with open('prowler_all_compliance.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_records)
print("✓ Saved prowler_all_compliance.csv")

tech_groups = {}
for r in all_records:
    tech = r['Technology']
    if tech not in tech_groups:
        tech_groups[tech] = []
    tech_groups[tech].append(r)

for tech, records in sorted(tech_groups.items()):
    filename = f'prowler_{tech.lower()}_compliance.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"✓ Saved {filename} ({len(records)} requirements)")

print("="*70)
print("✓ COMPLETE")
print("="*70)
