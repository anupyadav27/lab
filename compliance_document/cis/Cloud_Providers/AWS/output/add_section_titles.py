#!/usr/bin/env python3
"""
Add section titles to CIS AWS Foundations Benchmark JSON files.

Adds proper section hierarchy:
- section_number: "1", "2", "2.1", etc.
- section_title: "Identity and Access Management", "Simple Storage Service (S3)", etc.
- section_category: Main category (level 1)
- section_subcategory: Subcategory (level 2)
"""

import json
from pathlib import Path
import shutil

# Section mappings for CIS AWS Foundations Benchmark
SECTION_MAPPINGS = {
    "v4.0.1": {
        "1": "Identity and Access Management",
        "2": "Storage",
        "2.1": "Simple Storage Service (S3)",
        "2.2": "Relational Database Service (RDS)",
        "2.3": "Elastic File System (EFS)",
        "3": "Logging",
        "4": "Monitoring",
        "5": "Networking",
        "5.1": "Elastic Compute Cloud (EC2)"
    },
    "v5.0.0": {
        # Same structure as v4.0.1
        "1": "Identity and Access Management",
        "2": "Storage",
        "2.1": "Simple Storage Service (S3)",
        "2.2": "Relational Database Service (RDS)",
        "2.3": "Elastic File System (EFS)",
        "3": "Logging",
        "4": "Monitoring",
        "5": "Networking",
        "5.1": "Elastic Compute Cloud (EC2)"
    },
    "v6.0.0": {
        # Same structure as v4.0.1
        "1": "Identity and Access Management",
        "2": "Storage",
        "2.1": "Simple Storage Service (S3)",
        "2.2": "Relational Database Service (RDS)",
        "2.3": "Elastic File System (EFS)",
        "3": "Logging",
        "4": "Monitoring",
        "5": "Networking",
        "5.1": "Elastic Compute Cloud (EC2)"
    }
}

def get_section_info(control_id, section_mapping):
    """Get section information for a control ID."""

    # Extract section numbers from control ID
    # Examples: 1.2 → section=1, 2.1.1 → section=2.1, 5.1.2 → section=5.1

    parts = control_id.split('.')

    # Try to match longest section first (e.g., 2.1 before 2)
    if len(parts) >= 3:  # e.g., 2.1.1, 5.1.2
        subsection = f"{parts[0]}.{parts[1]}"
        if subsection in section_mapping:
            # This is a level 2 subsection
            section_category = section_mapping[parts[0]]
            section_subcategory = section_mapping[subsection]
            return {
                'section_number': subsection,
                'section_title': section_subcategory,
                'section_category': section_category,
                'section_subcategory': section_subcategory
            }

    # Try single-level section (e.g., 1.2, 3.1, 4.5)
    if len(parts) >= 2:
        section = parts[0]
        if section in section_mapping:
            # This is a level 1 section
            section_category = section_mapping[section]
            return {
                'section_number': section,
                'section_title': section_category,
                'section_category': section_category,
                'section_subcategory': None
            }

    # Fallback
    return {
        'section_number': parts[0] if parts else '',
        'section_title': 'Unknown',
        'section_category': 'Unknown',
        'section_subcategory': None
    }

def add_section_titles(json_file, version):
    """Add section titles to CIS benchmark JSON."""

    print(f"\n{'='*80}")
    print(f"Processing: {json_file.name}")
    print(f"Version: {version}")
    print(f"{'='*80}\n")

    # Get section mapping for this version
    if version not in SECTION_MAPPINGS:
        print(f"⚠️  No section mapping for {version}, skipping...")
        return

    section_mapping = SECTION_MAPPINGS[version]

    # Backup original file
    backup_file = json_file.with_suffix('.json.backup')
    if not backup_file.exists():
        shutil.copy(json_file, backup_file)
        print(f"✅ Backup created: {backup_file.name}")

    # Load JSON
    with open(json_file, 'r') as f:
        data = json.load(f)

    print(f"📊 Loaded: {len(data)} controls")

    # Track changes
    stats = {
        'updated': 0,
        'sections': {}
    }

    # Add section info to each control
    for item in data:
        control_id = item.get('id', '')
        if not control_id:
            continue

        # Get section info
        section_info = get_section_info(control_id, section_mapping)

        # Add new fields
        item['section_number'] = section_info['section_number']
        item['section_title'] = section_info['section_title']
        item['section_category'] = section_info['section_category']
        if section_info['section_subcategory']:
            item['section_subcategory'] = section_info['section_subcategory']

        # Track stats
        stats['updated'] += 1
        section_num = section_info['section_number']
        if section_num not in stats['sections']:
            stats['sections'][section_num] = {
                'title': section_info['section_title'],
                'count': 0
            }
        stats['sections'][section_num]['count'] += 1

    # Save updated JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated: {stats['updated']} controls")
    print()

    # Show section distribution
    print(f"📋 SECTION DISTRIBUTION:")
    for section_num in sorted(stats['sections'].keys(), key=lambda x: [int(p) for p in x.split('.')]):
        section_data = stats['sections'][section_num]
        print(f"  {section_num:<6} {section_data['title']:<50} ({section_data['count']:>3} controls)")
    print()

def main():
    """Process all CIS AWS Foundations Benchmark JSON files."""

    output_dir = Path('/Users/apple/Desktop/compliance_Database/compliance_document/cis/Cloud_Providers/AWS/output')

    # Files to process
    files_to_process = [
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v4.0.1.json', 'v4.0.1'),
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v5.0.0.json', 'v5.0.0'),
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v6.0.0.json', 'v6.0.0'),
    ]

    print("="*80)
    print("CIS AWS FOUNDATIONS BENCHMARK - ADD SECTION TITLES")
    print("="*80)

    for filename, version in files_to_process:
        json_file = output_dir / filename
        if json_file.exists():
            add_section_titles(json_file, version)
        else:
            print(f"⚠️  File not found: {filename}")

    print("="*80)
    print("✅ PROCESSING COMPLETE")
    print("="*80)
    print()

    print("New fields added to each control:")
    print("  • section_number: Section/subsection number (e.g., '1', '2.1')")
    print("  • section_title: Full section title")
    print("  • section_category: Main category (level 1)")
    print("  • section_subcategory: Subcategory (level 2, if applicable)")
    print()

    print("Example:")
    print("  Control 2.1.1:")
    print("    section_number: '2.1'")
    print("    section_title: 'Simple Storage Service (S3)'")
    print("    section_category: 'Storage'")
    print("    section_subcategory: 'Simple Storage Service (S3)'")

if __name__ == "__main__":
    main()
