#!/usr/bin/env python3
"""
Add subsection to EVERY control based on their control ID and title.

Structure:
- section: Main category (e.g., "1: Identity and Access Management")
- subsection: Control-level detail (e.g., "1.2: Ensure security contact information is registered")
- full_path: Complete path

Examples:
  Control 1.2:
    section: "1: Identity and Access Management"
    subsection: "1.2: Ensure security contact information is registered"
    full_path: "1: Identity and Access Management > 1.2: Ensure security contact information is registered"

  Control 2.1.1:
    section: "2: Storage"
    subsection: "2.1: Simple Storage Service (S3)"
    full_path: "2: Storage > 2.1: Simple Storage Service (S3)"
"""

import json
from pathlib import Path
import shutil

# Main section titles
MAIN_SECTIONS = {
    "v4.0.1": {
        "1": "Identity and Access Management",
        "2": "Storage",
        "3": "Logging",
        "4": "Monitoring",
        "5": "Networking"
    },
    "v5.0.0": {
        "1": "Identity and Access Management",
        "2": "Storage",
        "3": "Logging",
        "4": "Monitoring",
        "5": "Networking"
    }
}

# Service-specific subsections (these override control titles)
SERVICE_SUBSECTIONS = {
    "v4.0.1": {
        "2.1": "Simple Storage Service (S3)",
        "2.2": "Relational Database Service (RDS)",
        "2.3": "Elastic File System (EFS)",
        "5.1": "Elastic Compute Cloud (EC2)"
    },
    "v5.0.0": {
        "2.1": "Simple Storage Service (S3)",
        "2.2": "Relational Database Service (RDS)",
        "2.3": "Elastic File System (EFS)",
        "5.1": "Elastic Compute Cloud (EC2)"
    }
}

def get_subsection_title(control_id, control_title, version):
    """Get subsection title for a control."""

    parts = control_id.split('.')

    # Check if this is a predefined service subsection (2.1.x, 2.2.x, 5.1.x)
    if len(parts) >= 3:
        subsection_key = f"{parts[0]}.{parts[1]}"
        if subsection_key in SERVICE_SUBSECTIONS.get(version, {}):
            # Use service name (e.g., "2.1: Simple Storage Service (S3)")
            return f"{subsection_key}: {SERVICE_SUBSECTIONS[version][subsection_key]}"

    # For all other controls, use the control title
    # Format: "1.2: Ensure security contact information is registered"
    return f"{control_id}: {control_title}"

def add_control_subsections(json_file, version):
    """Add subsection to every control."""

    print(f"\n{'='*80}")
    print(f"Processing: {json_file.name}")
    print(f"Version: {version}")
    print(f"{'='*80}\n")

    if version not in MAIN_SECTIONS:
        print(f"⚠️  No section mapping for {version}, skipping...")
        return

    # Backup
    backup_file = json_file.with_name(json_file.stem + '_before_subsections.json')
    shutil.copy(json_file, backup_file)
    print(f"✅ Backup created: {backup_file.name}")

    # Load
    with open(json_file, 'r') as f:
        data = json.load(f)

    print(f"📊 Loaded: {len(data)} controls\n")

    # Update each control
    stats = {'updated': 0, 'by_section': {}}

    for control in data:
        control_id = control.get('id', '')
        control_title = control.get('title', '')

        if not control_id:
            continue

        # Get main section
        main_section_num = control_id.split('.')[0]
        main_section_title = MAIN_SECTIONS[version].get(main_section_num, 'Unknown')

        # Get subsection
        subsection_title = get_subsection_title(control_id, control_title, version)

        # Build section_hierarchy
        control['section_hierarchy'] = {
            "section": f"{main_section_num}: {main_section_title}",
            "subsection": subsection_title,
            "full_path": f"{main_section_num}: {main_section_title} > {subsection_title}"
        }

        stats['updated'] += 1

        # Track by section
        if main_section_num not in stats['by_section']:
            stats['by_section'][main_section_num] = {
                'title': main_section_title,
                'count': 0
            }
        stats['by_section'][main_section_num]['count'] += 1

    # Save
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated: {stats['updated']} controls\n")

    # Display stats
    print(f"📋 CONTROLS BY SECTION:\n")
    for section_num in sorted(stats['by_section'].keys(), key=lambda x: int(x)):
        section = stats['by_section'][section_num]
        print(f"  {section_num}: {section['title']:<40} {section['count']:>3} controls")

def main():
    """Process all CIS AWS Foundations Benchmark JSON files."""

    output_dir = Path('/Users/apple/Desktop/compliance_Database/compliance_document/cis/Cloud_Providers/AWS/output')

    files_to_process = [
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v4.0.1.json', 'v4.0.1'),
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v5.0.0.json', 'v5.0.0'),
    ]

    print("="*80)
    print("CIS AWS FOUNDATIONS BENCHMARK - ADD SUBSECTIONS TO ALL CONTROLS")
    print("="*80)
    print()
    print("Every control will have:")
    print("  • section: Main category")
    print("  • subsection: Control-specific or service-specific")
    print("  • full_path: Complete breadcrumb")
    print()

    for filename, version in files_to_process:
        json_file = output_dir / filename
        if json_file.exists():
            add_control_subsections(json_file, version)
        else:
            print(f"⚠️  File not found: {filename}")

    print("\n" + "="*80)
    print("✅ SUBSECTIONS ADDED TO ALL CONTROLS")
    print("="*80)
    print()

    print("Examples:")
    print()
    print("Control 1.2:")
    print("  {")
    print('    "section": "1: Identity and Access Management",')
    print('    "subsection": "1.2: Ensure security contact information is registered",')
    print('    "full_path": "1: Identity and Access Management > 1.2: Ensure security contact information is registered"')
    print("  }")
    print()
    print("Control 2.1.1:")
    print("  {")
    print('    "section": "2: Storage",')
    print('    "subsection": "2.1: Simple Storage Service (S3)",')
    print('    "full_path": "2: Storage > 2.1: Simple Storage Service (S3)"')
    print("  }")

if __name__ == "__main__":
    main()
