#!/usr/bin/env python3
"""
Process Incomplete Compliance Rows
Filters and processes only rows missing final_approach or program_name
"""

import argparse
import csv
import os
import shutil
from datetime import datetime


def filter_incomplete_rows(input_csv: str, output_csv: str) -> int:
    """
    Filter rows that need processing (missing final_approach or program_name).
    Returns count of filtered rows.
    """
    incomplete_rows = []
    
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            # Check if row needs processing
            if not row.get('final_approach') or not row.get('program_name'):
                incomplete_rows.append(row)
    
    # Write incomplete rows to new CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(incomplete_rows)
    
    print(f"✓ Filtered {len(incomplete_rows)} incomplete rows to: {output_csv}")
    return len(incomplete_rows)


def merge_results_back(original_csv: str, step4_output_csv: str, backup: bool = True) -> None:
    """
    Merge processed results back into original CSV.
    Updates rows that were processed while preserving already-complete rows.
    """
    # Backup original
    if backup:
        backup_path = original_csv.replace('.csv', f'_BACKUP_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        shutil.copy2(original_csv, backup_path)
        print(f"✓ Backed up original to: {backup_path}")
    
    # Read original CSV
    original_rows = {}
    with open(original_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            key = row.get('id') or row.get('unique_id')
            original_rows[key] = row
    
    # Read processed results
    processed_rows = {}
    with open(step4_output_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get('id') or row.get('unique_id')
            if key:
                processed_rows[key] = row
    
    # Merge: update original rows with processed data
    updated_count = 0
    for key, processed_row in processed_rows.items():
        if key in original_rows:
            # Update only the decision fields
            decision_fields = [
                'final_approach', 'final_confidence', 'program_name',
                'justification', 'automation_summary', 'manual_summary',
                'three_ai_consensus', 'decision_timestamp'
            ]
            for field in decision_fields:
                if field in processed_row and processed_row[field]:
                    original_rows[key][field] = processed_row[field]
            updated_count += 1
    
    # Write merged results back
    with open(original_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in original_rows.values():
            writer.writerow(row)
    
    print(f"✓ Merged {updated_count} processed rows back into: {original_csv}")


def main():
    parser = argparse.ArgumentParser(description="Process incomplete compliance rows")
    parser.add_argument("--action", choices=['filter', 'merge'], required=True,
                       help="Action to perform")
    parser.add_argument("--input-csv", required=True, help="Input CSV file")
    parser.add_argument("--output-csv", help="Output CSV file (for filter action)")
    parser.add_argument("--step4-csv", help="Step 4 output CSV (for merge action)")
    parser.add_argument("--no-backup", action='store_true', help="Skip backup when merging")
    
    args = parser.parse_args()
    
    if args.action == 'filter':
        if not args.output_csv:
            parser.error("--output-csv required for filter action")
        count = filter_incomplete_rows(args.input_csv, args.output_csv)
        print(f"\n✓ Ready to process {count} incomplete rows")
    
    elif args.action == 'merge':
        if not args.step4_csv:
            parser.error("--step4-csv required for merge action")
        merge_results_back(args.input_csv, args.step4_csv, backup=not args.no_backup)
        print("\n✓ Merge complete")


if __name__ == "__main__":
    main()


