#!/usr/bin/env python3
"""
Apply section hierarchy to ALL CIS benchmark JSON files across ALL cloud providers.

Uses extracted section mappings from HTML files to add proper section titles.
Adds metadata with timestamp tracking.
"""

import json
from pathlib import Path
import shutil
from datetime import datetime

UPDATE_TIMESTAMP = "2026-02-14"

def load_section_mapping(mapping_file):
    """Load section mapping from JSON file."""
    try:
        with open(mapping_file, 'r') as f:
            data = json.load(f)
            return data.get('sections', {})
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def convert_to_hierarchy(sections):
    """Convert flat section mapping to hierarchical structure."""
    hierarchy = {}

    for section_num, title in sections.items():
        parts = section_num.split('.')

        if len(parts) == 1:
            # Top-level section
            hierarchy[section_num] = {"title": title, "parent": None}
        elif len(parts) == 2:
            # Subsection
            parent_num = parts[0]
            hierarchy[section_num] = {"title": title, "parent": parent_num}

    return hierarchy


def get_subsection_title(control_id, control_title, sections):
    """Get subsection title for a control."""

    if not sections:
        return f"{control_id}: {control_title}"

    parts = control_id.split('.')

    # Check if this is a predefined subsection (e.g., 2.1.x, 3.1.x)
    if len(parts) >= 3:
        subsection_key = f"{parts[0]}.{parts[1]}"
        if subsection_key in sections and sections[subsection_key].get('parent'):
            return f"{subsection_key}: {sections[subsection_key]['title']}"

    # For all other controls, use control ID + title
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
        # Fallback to existing or generic
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


def process_json_file(json_file, section_mapping_file):
    """Process a single CIS JSON file."""

    print(f"\n{'='*80}")
    print(f"Processing: {json_file.name}")
    print(f"{'='*80}\n")

    # Load section mapping
    sections_flat = load_section_mapping(section_mapping_file)
    sections = convert_to_hierarchy(sections_flat)

    if not sections:
        print(f"⚠️  No section mapping found, using fallback")
    else:
        print(f"✅ Loaded {len(sections)} section mappings")

    # Backup
    backup_file = json_file.with_name(json_file.stem + f'_before_sections_{UPDATE_TIMESTAMP}.json')
    if not backup_file.exists():
        shutil.copy(json_file, backup_file)
        print(f"✅ Backup created: {backup_file.name}")

    # Load JSON
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
    if stats['by_section']:
        print(f"📋 CONTROLS BY SECTION:\n")
        for section in sorted(stats['by_section'].keys()):
            count = stats['by_section'][section]
            print(f"  {section:<50} {count:>3} controls")

    return stats


def main():
    """Apply section hierarchy to all CIS JSON files across all CSPs."""

    base_dir = Path('/Users/apple/Desktop/compliance_Database/compliance_document/cis/Cloud_Providers')
    mapping_dir = Path('/Users/apple/Desktop/cspm')

    # CSPs and their files
    csp_configs = [
        # Azure
        {
            'csp': 'Azure',
            'json_files': [
                'Azure/output/CIS_Microsoft_Azure_Foundations_Benchmark_v3_0_0.json',
                'Azure/output/CIS_Microsoft_Azure_Foundations_Benchmark_v4_0_0.json',
                'Azure/output/CIS_Microsoft_Azure_Foundations_Benchmark_v5_0_0.json',
                'Azure/output/CIS_Microsoft_Azure_Compute_Services_Benchmark_v1_0_0.json',
                'Azure/output/CIS_Microsoft_Azure_Compute_Services_Benchmark_v2_0_0.json',
                'Azure/output/CIS_Microsoft_Azure_Database_Services_Benchmark_v1_0_0.json',
                'Azure/output/CIS_Microsoft_Azure_Storage_Services_Benchmark_v1_0_0.json',
            ],
            'mapping_pattern': 'cis_sections_azure_*_v*.json'
        },
        # GCP
        {
            'csp': 'GCP',
            'json_files': [
                'GCP/output/CIS_Google_Cloud_Platform_Foundation_Benchmark_v3_0_0.json',
                'GCP/output/CIS_Google_Cloud_Platform_Foundation_Benchmark_v4_0_0.json',
            ],
            'mapping_pattern': 'cis_sections_gcp_*_v*.json'
        },
        # Oracle Cloud
        {
            'csp': 'Oracle',
            'json_files': [
                'Oracle_Cloud/output/CIS_Oracle_Cloud_Infrastructure_Foundations_Benchmark_v2_0_0.json',
                'Oracle_Cloud/output/CIS_Oracle_Cloud_Infrastructure_Foundations_Benchmark_v3_0_0.json',
            ],
            'mapping_pattern': 'cis_sections_oracle_*_v*.json'
        },
        # IBM Cloud
        {
            'csp': 'IBM',
            'json_files': [
                'IBM_Cloud/output/CIS_IBM_Cloud_Foundations_Benchmark_v1_0_0.json',
                'IBM_Cloud/output/CIS_IBM_Cloud_Foundations_Benchmark_v1_1_0.json',
            ],
            'mapping_pattern': 'cis_sections_ibm_*_v*.json'
        },
        # Alibaba Cloud
        {
            'csp': 'Alibaba',
            'json_files': [
                'Alibaba_Cloud/output/CIS_Alibaba_Cloud_Foundation_Benchmark_v1_0_0.json',
                'Alibaba_Cloud/output/CIS_CIS_Alibaba_Cloud_Foundation_Benchmark_v2_0_0.json',
            ],
            'mapping_pattern': 'cis_sections_alibaba_*_v*.json'
        },
    ]

    print("="*80)
    print("APPLY SECTION HIERARCHY TO ALL CSP CIS BENCHMARKS")
    print("="*80)
    print(f"\nTimestamp: {UPDATE_TIMESTAMP}\n")

    total_stats = {
        'files_processed': 0,
        'files_skipped': 0,
        'total_controls': 0,
        'by_csp': {}
    }

    for config in csp_configs:
        csp_name = config['csp']
        print(f"\n{'#'*80}")
        print(f"# {csp_name}")
        print(f"{'#'*80}")

        csp_stats = {'processed': 0, 'controls': 0}

        for json_file_path in config['json_files']:
            json_file = base_dir / json_file_path

            if not json_file.exists():
                print(f"\n⚠️  File not found: {json_file_path}")
                total_stats['files_skipped'] += 1
                continue

            # Find corresponding section mapping
            # Extract version from filename
            filename = json_file.stem
            version_parts = filename.split('_v')[-1].split('_')
            version = version_parts[0].replace('_', '.')

            # Try to find matching mapping file
            mapping_files = list(mapping_dir.glob(config['mapping_pattern']))
            mapping_file = None

            for mf in mapping_files:
                if version in mf.name:
                    mapping_file = mf
                    break

            if not mapping_file and mapping_files:
                # Use first available mapping as fallback
                mapping_file = mapping_files[0]

            if not mapping_file:
                mapping_file = Path('/dev/null')  # Fallback to generic

            stats = process_json_file(json_file, mapping_file)

            total_stats['files_processed'] += 1
            total_stats['total_controls'] += stats['updated']
            csp_stats['processed'] += 1
            csp_stats['controls'] += stats['updated']

        total_stats['by_csp'][csp_name] = csp_stats

    print("\n" + "="*80)
    print("✅ SECTION HIERARCHY APPLICATION COMPLETE")
    print("="*80)
    print(f"\nTotal files processed: {total_stats['files_processed']}")
    print(f"Total files skipped: {total_stats['files_skipped']}")
    print(f"Total controls updated: {total_stats['total_controls']}")

    print(f"\n📊 BY CLOUD PROVIDER:\n")
    for csp, stats in total_stats['by_csp'].items():
        print(f"  {csp:<15} {stats['processed']:>2} files, {stats['controls']:>4} controls")

    print(f"\n✅ All controls now have:")
    print("  • section: Main category")
    print("  • subsection: Control-specific or service-specific")
    print("  • full_path: Complete breadcrumb")
    print("  • metadata: timestamp and structure version")


if __name__ == "__main__":
    main()
