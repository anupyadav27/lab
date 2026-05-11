#!/usr/bin/env python3
"""
Finalize CIS section structure with simpler naming:
- Use "section" and "subsection" instead of "level_1" and "level_2"
- Format as "2: Storage" and "2.1: Simple Storage Service (S3)"
"""

import json
from pathlib import Path
import shutil

SECTION_HIERARCHY = {
    "v4.0.1": {
        "1": {"title": "Identity and Access Management", "parent": None},
        "2": {"title": "Storage", "parent": None},
        "2.1": {"title": "Simple Storage Service (S3)", "parent": "2"},
        "2.2": {"title": "Relational Database Service (RDS)", "parent": "2"},
        "2.3": {"title": "Elastic File System (EFS)", "parent": "2"},
        "3": {"title": "Logging", "parent": None},
        "4": {"title": "Monitoring", "parent": None},
        "5": {"title": "Networking", "parent": None},
        "5.1": {"title": "Elastic Compute Cloud (EC2)", "parent": "5"}
    },
    "v5.0.0": {
        "1": {"title": "Identity and Access Management", "parent": None},
        "2": {"title": "Storage", "parent": None},
        "2.1": {"title": "Simple Storage Service (S3)", "parent": "2"},
        "2.2": {"title": "Relational Database Service (RDS)", "parent": "2"},
        "2.3": {"title": "Elastic File System (EFS)", "parent": "2"},
        "3": {"title": "Logging", "parent": None},
        "4": {"title": "Monitoring", "parent": None},
        "5": {"title": "Networking", "parent": None},
        "5.1": {"title": "Elastic Compute Cloud (EC2)", "parent": "5"}
    }
}

def build_final_section(control_id, version):
    """Build final simplified section structure."""

    if version not in SECTION_HIERARCHY:
        return None

    sections = SECTION_HIERARCHY[version]
    parts = control_id.split('.')

    # Determine section number
    if len(parts) >= 3:  # e.g., 2.1.1, 5.1.2
        section_num = f"{parts[0]}.{parts[1]}"
    elif len(parts) >= 2:  # e.g., 1.2, 3.5
        section_num = parts[0]
    else:
        return None

    if section_num not in sections:
        return None

    section_info = sections[section_num]
    parent_num = section_info.get('parent')

    # Build simplified structure
    if parent_num:
        # Has parent (subsection)
        parent_info = sections.get(parent_num, {})

        return {
            "section": f"{parent_num}: {parent_info.get('title', 'Unknown')}",
            "subsection": f"{section_num}: {section_info['title']}",
            "path": [
                parent_info.get('title', 'Unknown'),
                section_info['title']
            ]
        }
    else:
        # No parent (main section only)
        return {
            "section": f"{section_num}: {section_info['title']}",
            "path": [section_info['title']]
        }

def finalize_structure(json_file, version):
    """Finalize section structure with simplified naming."""

    print(f"\n{'='*80}")
    print(f"Processing: {json_file.name}")
    print(f"Version: {version}")
    print(f"{'='*80}\n")

    if version not in SECTION_HIERARCHY:
        print(f"⚠️  No section hierarchy for {version}, skipping...")
        return

    # Backup
    backup_file = json_file.with_name(json_file.stem + '_before_final.json')
    shutil.copy(json_file, backup_file)
    print(f"✅ Backup created: {backup_file.name}")

    # Load
    with open(json_file, 'r') as f:
        data = json.load(f)

    print(f"📊 Loaded: {len(data)} controls\n")

    # Update each control
    stats = {'updated': 0}

    for control in data:
        control_id = control.get('id', '')
        if not control_id:
            continue

        # Build final section structure
        section_obj = build_final_section(control_id, version)
        if not section_obj:
            continue

        # Replace section_hierarchy with simplified version
        control['section_hierarchy'] = section_obj
        stats['updated'] += 1

    # Save
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Finalized: {stats['updated']} controls\n")

def main():
    """Process all CIS AWS Foundations Benchmark JSON files."""

    output_dir = Path('/Users/apple/Desktop/compliance_Database/compliance_document/cis/Cloud_Providers/AWS/output')

    files_to_process = [
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v4.0.1.json', 'v4.0.1'),
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v5.0.0.json', 'v5.0.0'),
    ]

    print("="*80)
    print("CIS AWS FOUNDATIONS BENCHMARK - FINAL STRUCTURE")
    print("="*80)
    print()
    print("Simplifying section structure:")
    print('  • "section" and "subsection" (not level_1, level_2)')
    print('  • Format: "2: Storage", "2.1: Simple Storage Service (S3)"')
    print()

    for filename, version in files_to_process:
        json_file = output_dir / filename
        if json_file.exists():
            finalize_structure(json_file, version)
        else:
            print(f"⚠️  File not found: {filename}")

    print("="*80)
    print("✅ FINAL STRUCTURE COMPLETE")
    print("="*80)
    print()

    print("Final section_hierarchy structure:")
    print()
    print("Main section only:")
    print("  {")
    print('    "section": "1: Identity and Access Management",')
    print('    "path": ["Identity and Access Management"]')
    print("  }")
    print()
    print("Section with subsection:")
    print("  {")
    print('    "section": "2: Storage",')
    print('    "subsection": "2.1: Simple Storage Service (S3)",')
    print('    "path": ["Storage", "Simple Storage Service (S3)"]')
    print("  }")

if __name__ == "__main__":
    main()
