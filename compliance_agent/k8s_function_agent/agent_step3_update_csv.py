#!/usr/bin/env python3
"""
K8s Function Generator - Step 3: Update CSV
Consolidates Step 2 results and updates the compliance CSV with K8s_Checks column.
"""

import argparse
import csv
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_step2_results(step2_dir: str) -> Dict[str, Dict]:
    """Load all Step 2 review results into a dictionary."""
    step2_path = Path(step2_dir)
    json_files = list(step2_path.glob("*.json"))
    
    results = {}
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            control_id = data.get('control_id', '')
            if control_id:
                results[control_id] = data
    
    logging.info(f"Loaded {len(results)} Step 2 results")
    return results


def update_csv_with_k8s_functions(input_csv: str, step2_results: Dict, output_csv: str, framework_name: str):
    """Update CSV file with K8s_Checks column."""
    
    logging.info(f"Reading CSV: {input_csv}")
    
    # Read original CSV
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    
    # Check if K8s_Checks already exists
    if 'K8s_Checks' in fieldnames or 'k8s_checks' in fieldnames:
        logging.warning("K8s_Checks column already exists in CSV")
        # Remove it to replace
        fieldnames = [f for f in fieldnames if f not in ['K8s_Checks', 'k8s_checks']]
    
    # Insert K8s_Checks before Total_Checks or at the end
    if 'Total_Checks' in fieldnames:
        insert_idx = fieldnames.index('Total_Checks')
        new_fieldnames = fieldnames[:insert_idx] + ['K8s_Checks'] + fieldnames[insert_idx:]
    elif 'total_checks' in fieldnames:
        insert_idx = fieldnames.index('total_checks')
        new_fieldnames = fieldnames[:insert_idx] + ['K8s_Checks'] + fieldnames[insert_idx:]
    else:
        new_fieldnames = fieldnames + ['K8s_Checks']
    
    # Update rows with K8s functions
    updated_rows = []
    k8s_added_count = 0
    k8s_not_applicable_count = 0
    
    for row in rows:
        # Get control ID (try different field names)
        control_id = (row.get('id') or row.get('Control_ID') or row.get('Requirement_ID') or 
                     row.get('Article_ID') or '').strip()
        
        if not control_id:
            logging.warning(f"Row has no control ID, skipping: {row}")
            row['K8s_Checks'] = ''
            updated_rows.append(row)
            continue
        
        # Get Step 2 result
        step2_data = step2_results.get(control_id, {})
        
        if not step2_data:
            # No Step 2 data (likely manual control)
            row['K8s_Checks'] = ''
            k8s_not_applicable_count += 1
        elif step2_data.get('k8s_applicable') and step2_data.get('validated_functions'):
            # Has K8s functions
            functions = step2_data['validated_functions']
            row['K8s_Checks'] = '; '.join(functions)
            k8s_added_count += 1
            
            # Update Total_Checks if exists
            if 'Total_Checks' in row:
                current_total = int(row.get('Total_Checks', 0) or 0)
                row['Total_Checks'] = str(current_total + len(functions))
            elif 'total_checks' in row:
                current_total = int(row.get('total_checks', 0) or 0)
                row['total_checks'] = str(current_total + len(functions))
        else:
            # Not applicable to K8s
            row['K8s_Checks'] = ''
            k8s_not_applicable_count += 1
        
        updated_rows.append(row)
    
    # Write updated CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)
    
    logging.info(f"\n{'='*80}")
    logging.info(f"CSV UPDATED - {framework_name}")
    logging.info(f"  Total controls: {len(rows)}")
    logging.info(f"  K8s functions added: {k8s_added_count}")
    logging.info(f"  Not applicable: {k8s_not_applicable_count}")
    logging.info(f"  Output CSV: {output_csv}")
    logging.info(f"{'='*80}\n")
    
    return k8s_added_count


def generate_summary_report(step2_dir: str, output_file: str, framework_name: str):
    """Generate a summary report of K8s functions."""
    step2_results = load_step2_results(step2_dir)
    
    report_lines = [
        f"# K8s Function Generation Summary - {framework_name}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Statistics",
        f"- Total controls processed: {len(step2_results)}",
    ]
    
    # Count by status
    status_counts = {
        'APPROVE': 0,
        'APPROVE_WITH_CHANGES': 0,
        'REJECT': 0,
        'NOT_APPLICABLE': 0,
        'ERROR': 0
    }
    
    k8s_functions_list = []
    
    for control_id, data in step2_results.items():
        status = data.get('review_status', 'UNKNOWN')
        status_counts[status] = status_counts.get(status, 0) + 1
        
        if data.get('k8s_applicable') and data.get('validated_functions'):
            k8s_functions_list.extend(data['validated_functions'])
    
    report_lines.extend([
        f"- Approved: {status_counts['APPROVE']}",
        f"- Approved with changes: {status_counts['APPROVE_WITH_CHANGES']}",
        f"- Rejected: {status_counts['REJECT']}",
        f"- Not applicable: {status_counts['NOT_APPLICABLE']}",
        f"- Errors: {status_counts['ERROR']}",
        f"- Total K8s functions generated: {len(k8s_functions_list)}",
        f"- Unique K8s functions: {len(set(k8s_functions_list))}",
        "",
        "## K8s Functions by Category",
        ""
    ])
    
    # Group by resource type
    by_resource = {}
    for func in set(k8s_functions_list):
        if func.startswith('k8s_'):
            parts = func.split('_')
            if len(parts) >= 2:
                resource = parts[1]
                by_resource.setdefault(resource, []).append(func)
    
    for resource in sorted(by_resource.keys()):
        report_lines.append(f"### {resource.upper()}")
        for func in sorted(by_resource[resource]):
            report_lines.append(f"- {func}")
        report_lines.append("")
    
    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    logging.info(f"Summary report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Update CSV with K8s functions - Step 3')
    parser.add_argument('--input-csv', required=True, help='Original compliance CSV file')
    parser.add_argument('--step2-dir', required=True, help='Directory with Step 2 review results')
    parser.add_argument('--output-csv', required=True, help='Output CSV file path')
    parser.add_argument('--framework', required=True, help='Framework name')
    parser.add_argument('--summary-report', help='Path for summary report (optional)')
    
    args = parser.parse_args()
    
    # Load Step 2 results
    step2_results = load_step2_results(args.step2_dir)
    
    # Update CSV
    update_csv_with_k8s_functions(
        args.input_csv,
        step2_results,
        args.output_csv,
        args.framework
    )
    
    # Generate summary report if requested
    if args.summary_report:
        generate_summary_report(args.step2_dir, args.summary_report, args.framework)
    
    return 0


if __name__ == "__main__":
    exit(main())

