#!/usr/bin/env python3
"""
Update CIS benchmark JSON files with proper section titles extracted from HTML.
"""

import json
from pathlib import Path
import shutil

UPDATE_TIMESTAMP = "2026-02-14"

# Proper section mappings extracted from HTML files
SECTION_MAPPINGS = {
    "Foundations_v6.0.0": {
        "2": {"title": "Identity and Access Management", "parent": None},
        "3": {"title": "Storage", "parent": None},
        "3.1": {"title": "Simple Storage Service (S3)", "parent": "3"},
        "3.2": {"title": "Relational Database Service (RDS)", "parent": "3"},
        "3.3": {"title": "Elastic File System (EFS)", "parent": "3"},
        "4": {"title": "Logging", "parent": None},
        "5": {"title": "Monitoring", "parent": None},
        "6": {"title": "Networking", "parent": None},
        "6.1": {"title": "Elastic Compute Cloud (EC2)", "parent": "6"}
    },
    "Compute_v1.1.0": {
        "2": {"title": "Amazon Elastic Cloud Compute (EC2)", "parent": None},
        "2.1": {"title": "Amazon Machine Images (AMI)", "parent": "2"},
        "2.2": {"title": "Elastic Block Storage (EBS)", "parent": "2"},
        "3": {"title": "Amazon Elastic Container Service (ECS)", "parent": None},
        "5": {"title": "Amazon Lightsail", "parent": None},
        "6": {"title": "AWS App Runner", "parent": None},
        "8": {"title": "AWS Batch", "parent": None},
        "10": {"title": "Elastic Beanstalk", "parent": None},
        "11": {"title": "AWS Fargate", "parent": None},
        "12": {"title": "AWS Lambda", "parent": None},
        "16": {"title": "AWS SimSpace Weaver", "parent": None}
    },
    "Database_v1.0.0": {
        "2": {"title": "Amazon Aurora", "parent": None},
        "3": {"title": "Amazon RDS", "parent": None},
        "4": {"title": "Amazon DynamoDB", "parent": None},
        "5": {"title": "Amazon ElastiCache", "parent": None},
        "6": {"title": "Amazon MemoryDB for Redis", "parent": None},
        "7": {"title": "Amazon DocumentDB", "parent": None},
        "8": {"title": "Amazon Keyspaces", "parent": None},
        "9": {"title": "Amazon Neptune", "parent": None},
        "10": {"title": "Amazon Timestream", "parent": None},
        "11": {"title": "Amazon Ledger Database Services (QLDB)", "parent": None}
    },
    "Storage_v1.0.0": {
        "1": {"title": "Introduction", "parent": None},
        "2": {"title": "Elastic Block Store (EBS)", "parent": None},
        "3": {"title": "Elastic File System (EFS)", "parent": None},
        "4": {"title": "FSx", "parent": None},
        "5": {"title": "Simple Storage Service (S3)", "parent": None},
        "6": {"title": "Elastic Disaster Recovery (EDR)", "parent": None}
    },
    "End_User_v1.1.0": {
        "2": {"title": "Amazon WorkSpaces", "parent": None},
        "3": {"title": "Amazon WorkSpaces Web", "parent": None},
        "4": {"title": "Amazon WorkDocs", "parent": None},
        "5": {"title": "Amazon AppStream 2.0", "parent": None}
    },
    "End_User_v1.2.0": {
        "2": {"title": "Amazon WorkSpaces", "parent": None},
        "3": {"title": "Amazon WorkSpaces Web", "parent": None},
        "4": {"title": "Amazon WorkDocs", "parent": None},
        "5": {"title": "Amazon AppStream 2.0", "parent": None}
    }
}


def get_subsection_title(control_id, control_title, sections):
    """Get subsection title for a control."""

    if not sections:
        return f"{control_id}: {control_title}"

    parts = control_id.split('.')

    # Check if this is a predefined service subsection (2.1.x, 2.2.x, 3.1.x, 6.1.x)
    if len(parts) >= 3:
        subsection_key = f"{parts[0]}.{parts[1]}"
        if subsection_key in sections and sections[subsection_key].get('parent'):
            # Use service name (e.g., "2.1: Amazon Machine Images (AMI)")
            return f"{subsection_key}: {sections[subsection_key]['title']}"

    # For all other controls, use the control title
    return f"{control_id}: {control_title}"


def update_control_section(control, sections):
    """Update section_hierarchy with proper section titles."""

    control_id = control.get('id', '')
    control_title = control.get('title', '')

    if not control_id or not sections:
        return False

    # Get main section number
    parts = control_id.split('.')
    main_section_num = parts[0]

    # Get main section title
    if main_section_num in sections:
        main_section_title = sections[main_section_num]['title']
    else:
        return False

    # Get subsection
    subsection_title = get_subsection_title(control_id, control_title, sections)

    # Update section_hierarchy
    control['section_hierarchy'] = {
        "section": f"{main_section_num}: {main_section_title}",
        "subsection": subsection_title,
        "full_path": f"{main_section_num}: {main_section_title} > {subsection_title}"
    }

    # Update metadata
    if 'metadata' not in control:
        control['metadata'] = {}

    control['metadata']['section_titles_updated'] = UPDATE_TIMESTAMP
    control['metadata']['structure_version'] = "1.1"

    return True


def process_file(json_file, sections_key):
    """Process a single JSON file with proper section titles."""

    print(f"\n{'='*80}")
    print(f"Updating: {json_file.name}")
    print(f"Section mapping: {sections_key}")
    print(f"{'='*80}\n")

    sections = SECTION_MAPPINGS.get(sections_key, {})

    if not sections:
        print(f"⚠️  No section mapping for {sections_key}, skipping...")
        return

    # Load
    with open(json_file, 'r') as f:
        data = json.load(f)

    print(f"📊 Loaded: {len(data)} controls")

    # Update each control
    updated_count = 0
    for control in data:
        if update_control_section(control, sections):
            updated_count += 1

    # Save
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated: {updated_count} controls with proper section titles\n")


def main():
    """Update all AWS CIS files with proper section titles."""

    output_dir = Path('/Users/apple/Desktop/compliance_Database/compliance_document/cis/Cloud_Providers/AWS/output')

    files_to_update = [
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v6.0.0.json', 'Foundations_v6.0.0'),
        ('CIS_AWS_Compute_Services_Benchmark_v1.1.0.json', 'Compute_v1.1.0'),
        ('CIS_AWS_Database_Services_Benchmark_v1.0.0.json', 'Database_v1.0.0'),
        ('CIS_AWS_Storage_Services_Benchmark_v1.0.0.json', 'Storage_v1.0.0'),
        ('CIS_AWS_End_User_Compute_Services_Benchmark_v1.1.0.json', 'End_User_v1.1.0'),
        ('CIS_AWS_End_User_Compute_Services_Benchmark_v1.2.0.json', 'End_User_v1.2.0'),
    ]

    print("="*80)
    print("UPDATE CIS BENCHMARKS WITH PROPER SECTION TITLES")
    print("="*80)
    print(f"\nTimestamp: {UPDATE_TIMESTAMP}")
    print(f"Files to update: {len(files_to_update)}\n")

    for filename, sections_key in files_to_update:
        json_file = output_dir / filename
        if json_file.exists():
            process_file(json_file, sections_key)
        else:
            print(f"⚠️  File not found: {filename}")

    print("="*80)
    print("✅ SECTION TITLES UPDATE COMPLETE")
    print("="*80)
    print("\nAll controls now have:")
    print("  • Proper section titles from HTML extraction")
    print("  • Updated metadata timestamp")
    print("  • Structure version 1.1")


if __name__ == "__main__":
    main()
