#!/usr/bin/env python3
"""
Apply section hierarchy to ALL CIS benchmark JSON files across ALL cloud providers.

Adds:
- section_hierarchy object with section, subsection, full_path
- metadata with timestamp
"""

import json
from pathlib import Path
import shutil
from datetime import datetime

# Timestamp for tracking updates
UPDATE_TIMESTAMP = "2026-02-14"

# AWS CIS Foundations Benchmark Section Mappings
AWS_FOUNDATIONS_SECTIONS = {
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
    },
    "v6.0.0": {
        # v6.0.0 appears to have different section structure based on the JSON
        # Will need to analyze the HTML to extract proper sections
        # For now using generic mapping based on visible control IDs
    }
}

# AWS Compute Services Benchmark
AWS_COMPUTE_SECTIONS = {
    "v1.1.0": {
        # Will extract from HTML - controls appear to be under section 2
    }
}

# AWS Database Services Benchmark
AWS_DATABASE_SECTIONS = {
    "v1.0.0": {
        # Will extract from HTML - controls appear to be under section 2
    }
}

# AWS Storage Services Benchmark
AWS_STORAGE_SECTIONS = {
    "v1.0.0": {
        # Will extract from HTML - controls appear to be under section 1
    }
}

# AWS End User Compute Services Benchmark
AWS_END_USER_SECTIONS = {
    "v1.1.0": {},
    "v1.2.0": {}
}


def get_section_mapping(benchmark_type, version):
    """Get section mapping for a specific benchmark and version."""

    if "Foundations" in benchmark_type:
        return AWS_FOUNDATIONS_SECTIONS.get(version, {})
    elif "Compute" in benchmark_type and "End_User" not in benchmark_type:
        return AWS_COMPUTE_SECTIONS.get(version, {})
    elif "Database" in benchmark_type:
        return AWS_DATABASE_SECTIONS.get(version, {})
    elif "Storage" in benchmark_type:
        return AWS_STORAGE_SECTIONS.get(version, {})
    elif "End_User" in benchmark_type:
        return AWS_END_USER_SECTIONS.get(version, {})

    return {}


def get_subsection_title(control_id, control_title, sections):
    """Get subsection title for a control."""

    if not sections:
        # Fallback: use control ID + title
        return f"{control_id}: {control_title}"

    parts = control_id.split('.')

    # Check if this is a predefined service subsection (2.1.x, 2.2.x, 5.1.x)
    if len(parts) >= 3:
        subsection_key = f"{parts[0]}.{parts[1]}"
        if subsection_key in sections and sections[subsection_key].get('parent'):
            # Use service name (e.g., "2.1: Simple Storage Service (S3)")
            return f"{subsection_key}: {sections[subsection_key]['title']}"

    # For all other controls, use the control title
    # Format: "1.2: Ensure security contact information is registered"
    return f"{control_id}: {control_title}"


def add_section_hierarchy(control, sections):
    """Add section_hierarchy object to a control."""

    control_id = control.get('id', '')
    control_title = control.get('title', '')

    if not control_id:
        return False

    # Get main section number
    parts = control_id.split('.')
    main_section_num = parts[0]

    # Get main section title
    if sections and main_section_num in sections:
        main_section_title = sections[main_section_num]['title']
    else:
        # Fallback to existing section_title if available
        main_section_title = control.get('section_title', f'Section {main_section_num}')

    # Get subsection
    subsection_title = get_subsection_title(control_id, control_title, sections)

    # Build section_hierarchy
    control['section_hierarchy'] = {
        "section": f"{main_section_num}: {main_section_title}",
        "subsection": subsection_title,
        "full_path": f"{main_section_num}: {main_section_title} > {subsection_title}"
    }

    # Add metadata
    if 'metadata' not in control:
        control['metadata'] = {}

    control['metadata']['section_hierarchy_added'] = UPDATE_TIMESTAMP
    control['metadata']['structure_version'] = "1.0"

    return True


def process_json_file(json_file, benchmark_type, version):
    """Process a single CIS benchmark JSON file."""

    print(f"\n{'='*80}")
    print(f"Processing: {json_file.name}")
    print(f"Benchmark: {benchmark_type}")
    print(f"Version: {version}")
    print(f"{'='*80}\n")

    # Get section mapping
    sections = get_section_mapping(benchmark_type, version)

    if not sections:
        print(f"⚠️  No section mapping available for {benchmark_type} {version}")
        print(f"   Will use fallback mapping (control ID + title)")

    # Backup
    backup_file = json_file.with_name(json_file.stem + f'_before_sections_{UPDATE_TIMESTAMP}.json')
    if not backup_file.exists():
        shutil.copy(json_file, backup_file)
        print(f"✅ Backup created: {backup_file.name}")
    else:
        print(f"ℹ️  Backup already exists: {backup_file.name}")

    # Load
    with open(json_file, 'r') as f:
        data = json.load(f)

    print(f"📊 Loaded: {len(data)} controls\n")

    # Update each control
    stats = {'updated': 0, 'by_section': {}}

    for control in data:
        if add_section_hierarchy(control, sections):
            stats['updated'] += 1

            # Track by section
            section_hierarchy = control.get('section_hierarchy', {})
            section = section_hierarchy.get('section', 'Unknown')

            if section not in stats['by_section']:
                stats['by_section'][section] = 0
            stats['by_section'][section] += 1

    # Save
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated: {stats['updated']} controls\n")

    # Display stats
    print(f"📋 CONTROLS BY SECTION:\n")
    for section in sorted(stats['by_section'].keys()):
        count = stats['by_section'][section]
        print(f"  {section:<50} {count:>3} controls")

    return stats


def main():
    """Process all CIS AWS benchmark JSON files."""

    output_dir = Path('/Users/apple/Desktop/compliance_Database/compliance_document/cis/Cloud_Providers/AWS/output')

    # AWS CIS files to process
    files_to_process = [
        # Foundations Benchmarks
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v4.0.1.json', 'Foundations', 'v4.0.1'),
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v5.0.0.json', 'Foundations', 'v5.0.0'),
        ('CIS_Amazon_Web_Services_Foundations_Benchmark_v6.0.0.json', 'Foundations', 'v6.0.0'),

        # Service-specific Benchmarks
        ('CIS_AWS_Compute_Services_Benchmark_v1.1.0.json', 'Compute', 'v1.1.0'),
        ('CIS_AWS_Database_Services_Benchmark_v1.0.0.json', 'Database', 'v1.0.0'),
        ('CIS_AWS_Storage_Services_Benchmark_v1.0.0.json', 'Storage', 'v1.0.0'),
        ('CIS_AWS_End_User_Compute_Services_Benchmark_v1.1.0.json', 'End_User', 'v1.1.0'),
        ('CIS_AWS_End_User_Compute_Services_Benchmark_v1.2.0.json', 'End_User', 'v1.2.0'),
    ]

    print("="*80)
    print("CIS BENCHMARKS - APPLY SECTION HIERARCHY TO ALL FILES")
    print("="*80)
    print(f"\nTimestamp: {UPDATE_TIMESTAMP}")
    print(f"Total files to process: {len(files_to_process)}\n")

    total_stats = {
        'files_processed': 0,
        'files_skipped': 0,
        'total_controls': 0
    }

    for filename, benchmark_type, version in files_to_process:
        json_file = output_dir / filename

        if json_file.exists():
            stats = process_json_file(json_file, benchmark_type, version)
            total_stats['files_processed'] += 1
            total_stats['total_controls'] += stats['updated']
        else:
            print(f"\n⚠️  File not found: {filename}")
            total_stats['files_skipped'] += 1

    print("\n" + "="*80)
    print("✅ SECTION HIERARCHY APPLICATION COMPLETE")
    print("="*80)
    print(f"\nFiles processed: {total_stats['files_processed']}")
    print(f"Files skipped: {total_stats['files_skipped']}")
    print(f"Total controls updated: {total_stats['total_controls']}")
    print(f"\nAll controls now have:")
    print("  • section: Main category (e.g., '1: Identity and Access Management')")
    print("  • subsection: Control-specific or service-specific")
    print("  • full_path: Complete breadcrumb")
    print("  • metadata: timestamp and structure version")


if __name__ == "__main__":
    main()
