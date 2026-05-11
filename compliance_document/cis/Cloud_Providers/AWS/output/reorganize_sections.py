#!/usr/bin/env python3
"""
Reorganize CIS section hierarchy to show proper parent-child relationships.

The issue: Section 2 (Storage) should be the parent of 2.1, 2.2, 2.3
Currently showing as separate sections instead of nested hierarchy.

New structure will make it clear:
  Section 1: Identity and Access Management (parent only)
  Section 2: Storage (parent category)
    ├─ Section 2.1: Simple Storage Service (S3) (child)
    ├─ Section 2.2: Relational Database Service (RDS) (child)
    └─ Section 2.3: Elastic File System (EFS) (child)
"""

import json
from pathlib import Path
import shutil

# Proper section hierarchy for CIS AWS Foundations Benchmark
SECTION_HIERARCHY = {
    "v4.0.1": {
        # Level 1 - Main categories (parents)
        "1": {
            "title": "Identity and Access Management",
            "parent": None,
            "level": 1
        },
        "2": {
            "title": "Storage",
            "parent": None,
            "level": 1
        },
        "3": {
            "title": "Logging",
            "parent": None,
            "level": 1
        },
        "4": {
            "title": "Monitoring",
            "parent": None,
            "level": 1
        },
        "5": {
            "title": "Networking",
            "parent": None,
            "level": 1
        },

        # Level 2 - Subsections (children)
        "2.1": {
            "title": "Simple Storage Service (S3)",
            "parent": "2",
            "parent_title": "Storage",
            "level": 2
        },
        "2.2": {
            "title": "Relational Database Service (RDS)",
            "parent": "2",
            "parent_title": "Storage",
            "level": 2
        },
        "2.3": {
            "title": "Elastic File System (EFS)",
            "parent": "2",
            "parent_title": "Storage",
            "level": 2
        },
        "5.1": {
            "title": "Elastic Compute Cloud (EC2)",
            "parent": "5",
            "parent_title": "Networking",
            "level": 2
        }
    }
}

# Copy same structure for v5.0.0
SECTION_HIERARCHY["v5.0.0"] = SECTION_HIERARCHY["v4.0.1"].copy()

def get_section_hierarchy(control_id, version):
    """Get complete section hierarchy for a control."""

    if version not in SECTION_HIERARCHY:
        return None

    sections = SECTION_HIERARCHY[version]
    parts = control_id.split('.')

    # Try to match longest section first (e.g., 2.1 before 2)
    if len(parts) >= 3:  # e.g., 2.1.1, 5.1.2
        section_key = f"{parts[0]}.{parts[1]}"
        if section_key in sections:
            section_info = sections[section_key]
            return {
                'section_number': section_key,
                'section_title': section_info['title'],
                'section_level': section_info['level'],
                'parent_section_number': section_info.get('parent'),
                'parent_section_title': section_info.get('parent_title'),
                'section_path': f"{section_info.get('parent_title', '')} > {section_info['title']}" if section_info.get('parent') else section_info['title']
            }

    # Try single-level section (e.g., 1.2, 3.1, 4.5)
    if len(parts) >= 2:
        section_key = parts[0]
        if section_key in sections:
            section_info = sections[section_key]
            return {
                'section_number': section_key,
                'section_title': section_info['title'],
                'section_level': section_info['level'],
                'parent_section_number': None,
                'parent_section_title': None,
                'section_path': section_info['title']
            }

    return None

def reorganize_sections(json_file, version):
    """Reorganize section hierarchy in CIS benchmark JSON."""

    print(f"\n{'='*80}")
    print(f"Processing: {json_file.name}")
    print(f"Version: {version}")
    print(f"{'='*80}\n")

    if version not in SECTION_HIERARCHY:
        print(f"⚠️  No section hierarchy for {version}, skipping...")
        return

    # Backup
    backup_file = json_file.with_name(json_file.stem + '_before_reorganize.json')
    shutil.copy(json_file, backup_file)
    print(f"✅ Backup created: {backup_file.name}")

    # Load
    with open(json_file, 'r') as f:
        data = json.load(f)

    print(f"📊 Loaded: {len(data)} controls\n")

    # Update each control with proper hierarchy
    stats = {
        'level1': 0,  # Parent sections
        'level2': 0,  # Child sections
        'sections': {}
    }

    for control in data:
        control_id = control.get('id', '')
        if not control_id:
            continue

        # Get hierarchy
        hierarchy = get_section_hierarchy(control_id, version)
        if not hierarchy:
            continue

        # Update control with new hierarchy fields
        control['section_number'] = hierarchy['section_number']
        control['section_title'] = hierarchy['section_title']
        control['section_level'] = hierarchy['section_level']
        control['section_path'] = hierarchy['section_path']

        # Add parent info for level 2 sections
        if hierarchy['parent_section_number']:
            control['parent_section_number'] = hierarchy['parent_section_number']
            control['parent_section_title'] = hierarchy['parent_section_title']
        else:
            # Remove parent fields for level 1 sections
            control.pop('parent_section_number', None)
            control.pop('parent_section_title', None)

        # Remove old fields
        control.pop('section_category', None)
        control.pop('section_subcategory', None)

        # Track stats
        if hierarchy['section_level'] == 1:
            stats['level1'] += 1
        else:
            stats['level2'] += 1

        section_num = hierarchy['section_number']
        if section_num not in stats['sections']:
            stats['sections'][section_num] = {
                'title': hierarchy['section_title'],
                'level': hierarchy['section_level'],
                'parent': hierarchy.get('parent_section_number'),
                'count': 0
            }
        stats['sections'][section_num]['count'] += 1

    # Save
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Reorganized: {len(data)} controls")
    print(f"  Level 1 (parent): {stats['level1']} controls")
    print(f"  Level 2 (child): {stats['level2']} controls\n")

    # Display hierarchy
    print(f"📋 SECTION HIERARCHY:\n")

    # Sort sections: level 1 first, then level 2 under their parents
    level1_sections = {k: v for k, v in stats['sections'].items() if v['level'] == 1}

    for section_num in sorted(level1_sections.keys(), key=lambda x: int(x)):
        section = stats['sections'][section_num]
        print(f"Section {section_num}: {section['title']} ({section['count']} controls)")

        # Show child sections
        children = {k: v for k, v in stats['sections'].items()
                   if v.get('parent') == section_num}

        if children:
            for child_num in sorted(children.keys(), key=lambda x: [int(p) for p in x.split('.')]):
                child = children[child_num]
                print(f"  ├─ Section {child_num}: {child['title']} ({child['count']} controls)")
        print()

def main():
    """Process all CIS AWS Foundations Benchmark JSON files."""

    output_dir = Path('/Users/apple/Desktop/compliance_Database/compliance_document/cis/Cloud_Providers/AWS/output')

    files_to_process = [
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v4.0.1.json', 'v4.0.1'),
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v5.0.0.json', 'v5.0.0'),
    ]

    print("="*80)
    print("CIS AWS FOUNDATIONS BENCHMARK - REORGANIZE SECTION HIERARCHY")
    print("="*80)
    print()
    print("Goal: Show proper parent-child relationship between sections")
    print()

    for filename, version in files_to_process:
        json_file = output_dir / filename
        if json_file.exists():
            reorganize_sections(json_file, version)
        else:
            print(f"⚠️  File not found: {filename}")

    print("="*80)
    print("✅ REORGANIZATION COMPLETE")
    print("="*80)
    print()

    print("New fields:")
    print("  • section_number: Section number (e.g., '1', '2.1')")
    print("  • section_title: Section title")
    print("  • section_level: 1 (parent) or 2 (child)")
    print("  • section_path: Full path (e.g., 'Storage > Simple Storage Service (S3)')")
    print("  • parent_section_number: Parent section (for level 2 only)")
    print("  • parent_section_title: Parent title (for level 2 only)")
    print()

    print("Example - Control 2.1.1:")
    print("  section_number: '2.1'")
    print("  section_title: 'Simple Storage Service (S3)'")
    print("  section_level: 2")
    print("  section_path: 'Storage > Simple Storage Service (S3)'")
    print("  parent_section_number: '2'")
    print("  parent_section_title: 'Storage'")

if __name__ == "__main__":
    main()
