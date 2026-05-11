#!/usr/bin/env python3
"""
Restructure CIS section information into a hierarchical object structure.

Instead of flat fields:
  section_number, section_title, section_level, parent_section_number, etc.

Use nested hierarchy:
  section: {
    level_1: { number, title },
    level_2: { number, title },
    path: [...],
    full_path: "..."
  }
"""

import json
from pathlib import Path
import shutil

# Section hierarchy mapping
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

def build_section_object(control_id, version):
    """Build hierarchical section object for a control."""

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

    # Build hierarchical structure
    section_obj = {}

    if parent_num:
        # This is a level 2 section (has parent)
        parent_info = sections.get(parent_num, {})

        section_obj = {
            "level_1": {
                "number": parent_num,
                "title": parent_info.get('title', 'Unknown')
            },
            "level_2": {
                "number": section_num,
                "title": section_info['title']
            },
            "path": [
                parent_info.get('title', 'Unknown'),
                section_info['title']
            ],
            "full_path": f"{parent_num}. {parent_info.get('title', 'Unknown')} > {section_num} {section_info['title']}"
        }
    else:
        # This is a level 1 section (no parent)
        section_obj = {
            "level_1": {
                "number": section_num,
                "title": section_info['title']
            },
            "path": [section_info['title']],
            "full_path": f"{section_num}. {section_info['title']}"
        }

    return section_obj

def restructure_to_hierarchical(json_file, version):
    """Restructure CIS JSON to use hierarchical section objects."""

    print(f"\n{'='*80}")
    print(f"Processing: {json_file.name}")
    print(f"Version: {version}")
    print(f"{'='*80}\n")

    if version not in SECTION_HIERARCHY:
        print(f"⚠️  No section hierarchy for {version}, skipping...")
        return

    # Backup
    backup_file = json_file.with_name(json_file.stem + '_before_hierarchical.json')
    shutil.copy(json_file, backup_file)
    print(f"✅ Backup created: {backup_file.name}")

    # Load
    with open(json_file, 'r') as f:
        data = json.load(f)

    print(f"📊 Loaded: {len(data)} controls\n")

    # Restructure each control
    stats = {'updated': 0, 'sections': {}}

    for control in data:
        control_id = control.get('id', '')
        if not control_id:
            continue

        # Build hierarchical section object
        section_obj = build_section_object(control_id, version)
        if not section_obj:
            continue

        # Remove old flat fields
        old_fields = [
            'section_number', 'section_title', 'section_level',
            'section_path', 'parent_section_number', 'parent_section_title',
            'section_category', 'section_subcategory'
        ]
        for field in old_fields:
            control.pop(field, None)

        # Add new hierarchical section object
        # Keep the old "section" field but add structured "section_hierarchy"
        control['section_hierarchy'] = section_obj

        stats['updated'] += 1

        # Track sections
        if 'level_1' in section_obj:
            level1_num = section_obj['level_1']['number']
            if level1_num not in stats['sections']:
                stats['sections'][level1_num] = {
                    'title': section_obj['level_1']['title'],
                    'count': 0,
                    'subsections': {}
                }
            stats['sections'][level1_num]['count'] += 1

            if 'level_2' in section_obj:
                level2_num = section_obj['level_2']['number']
                if level2_num not in stats['sections'][level1_num]['subsections']:
                    stats['sections'][level1_num]['subsections'][level2_num] = {
                        'title': section_obj['level_2']['title'],
                        'count': 0
                    }
                stats['sections'][level1_num]['subsections'][level2_num]['count'] += 1

    # Save
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Restructured: {stats['updated']} controls\n")

    # Display hierarchy
    print(f"📋 HIERARCHICAL SECTION STRUCTURE:\n")

    for section_num in sorted(stats['sections'].keys(), key=lambda x: int(x.split('.')[0])):
        section = stats['sections'][section_num]
        print(f"{section_num}. {section['title']} ({section['count']} controls)")

        if section['subsections']:
            for subsec_num in sorted(section['subsections'].keys(),
                                    key=lambda x: [int(p) for p in x.split('.')]):
                subsec = section['subsections'][subsec_num]
                print(f"  └─ {subsec_num} {subsec['title']} ({subsec['count']} controls)")
        print()

def main():
    """Process all CIS AWS Foundations Benchmark JSON files."""

    output_dir = Path('/Users/apple/Desktop/compliance_Database/compliance_document/cis/Cloud_Providers/AWS/output')

    files_to_process = [
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v4.0.1.json', 'v4.0.1'),
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v5.0.0.json', 'v5.0.0'),
    ]

    print("="*80)
    print("CIS AWS FOUNDATIONS BENCHMARK - HIERARCHICAL RESTRUCTURE")
    print("="*80)
    print()
    print("Converting flat section fields to nested hierarchical objects")
    print()

    for filename, version in files_to_process:
        json_file = output_dir / filename
        if json_file.exists():
            restructure_to_hierarchical(json_file, version)
        else:
            print(f"⚠️  File not found: {filename}")

    print("="*80)
    print("✅ HIERARCHICAL RESTRUCTURE COMPLETE")
    print("="*80)
    print()

    print("New structure - section_hierarchy object:")
    print()
    print("Level 1 (parent only):")
    print("  {")
    print('    "level_1": { "number": "1", "title": "Identity and Access Management" },')
    print('    "path": ["Identity and Access Management"],')
    print('    "full_path": "1. Identity and Access Management"')
    print("  }")
    print()
    print("Level 2 (with parent):")
    print("  {")
    print('    "level_1": { "number": "2", "title": "Storage" },')
    print('    "level_2": { "number": "2.1", "title": "Simple Storage Service (S3)" },')
    print('    "path": ["Storage", "Simple Storage Service (S3)"],')
    print('    "full_path": "2. Storage > 2.1 Simple Storage Service (S3)"')
    print("  }")

if __name__ == "__main__":
    main()
