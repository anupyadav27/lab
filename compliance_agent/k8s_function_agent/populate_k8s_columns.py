#!/usr/bin/env python3
"""
Populate K8s-related columns in Consolidated CSV
Updates: total_checks, k8s_uniform_format for rows with new K8s functions
Leaves *_mapped_* columns untouched
"""

import csv
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def convert_to_uniform_format(k8s_function):
    """
    Convert K8s function name to uniform format.
    Pattern: k8s_<resource>_<check> → k8s.<resource>.<check>
    
    Examples:
    - k8s_rbac_least_privilege_enforcement → k8s.rbac.least_privilege_enforcement
    - k8s_networkpolicy_default_deny_ingress → k8s.networkpolicy.default_deny_ingress
    - k8s_secret_encryption_at_rest_enabled → k8s.secret.encryption_at_rest_enabled
    """
    if not k8s_function or not k8s_function.startswith('k8s_'):
        return k8s_function
    
    # Remove 'k8s_' prefix
    without_prefix = k8s_function[4:]
    
    # Split by underscore and take first part as resource
    parts = without_prefix.split('_', 1)
    if len(parts) == 2:
        resource, check = parts
        return f"k8s.{resource}.{check}"
    
    # Fallback if no underscore found
    return f"k8s.{without_prefix}"


def count_checks(check_string):
    """Count number of checks in a semicolon-separated string."""
    if not check_string or check_string.strip() == '':
        return 0
    return len([c for c in check_string.split(';') if c.strip()])


def populate_k8s_columns(input_csv, output_csv):
    """Populate K8s-related columns for rows with K8s functions."""
    
    logging.info("="*80)
    logging.info("POPULATING K8S COLUMNS IN CONSOLIDATED CSV")
    logging.info("="*80)
    
    # Read CSV
    logging.info(f"\nReading CSV: {input_csv}")
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    
    logging.info(f"Loaded {len(rows)} rows")
    
    # Process each row
    updated_total_checks = 0
    updated_uniform_format = 0
    skipped_no_k8s = 0
    skipped_already_has_uniform = 0
    
    for row in rows:
        k8s_checks = row.get('k8s_checks', '').strip()
        
        # Skip if no K8s checks
        if not k8s_checks:
            skipped_no_k8s += 1
            continue
        
        # Get current values
        current_uniform = row.get('k8s_uniform_format', '').strip()
        current_total = row.get('total_checks', '0').strip()
        
        # Update k8s_uniform_format if empty
        if not current_uniform:
            # Convert each K8s function to uniform format
            k8s_functions = [f.strip() for f in k8s_checks.split(';') if f.strip()]
            uniform_functions = [convert_to_uniform_format(f) for f in k8s_functions]
            row['k8s_uniform_format'] = '; '.join(uniform_functions)
            updated_uniform_format += 1
        else:
            skipped_already_has_uniform += 1
        
        # Update total_checks (add K8s count)
        # Count existing checks from all CSP columns
        aws_count = count_checks(row.get('aws_checks', ''))
        azure_count = count_checks(row.get('azure_checks', ''))
        gcp_count = count_checks(row.get('gcp_checks', ''))
        oracle_count = count_checks(row.get('oracle_checks', ''))
        ibm_count = count_checks(row.get('ibm_checks', ''))
        alicloud_count = count_checks(row.get('alicloud_checks', ''))
        k8s_count = count_checks(k8s_checks)
        
        new_total = aws_count + azure_count + gcp_count + oracle_count + ibm_count + alicloud_count + k8s_count
        
        # Update if different from current
        if current_total != str(new_total):
            row['total_checks'] = str(new_total)
            updated_total_checks += 1
    
    # Write updated CSV
    logging.info(f"\nWriting updated CSV to: {output_csv}")
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    # Summary
    logging.info("\n" + "="*80)
    logging.info("POPULATE K8S COLUMNS COMPLETE")
    logging.info("="*80)
    logging.info(f"  Total rows: {len(rows)}")
    logging.info(f"  Updated total_checks: {updated_total_checks}")
    logging.info(f"  Updated k8s_uniform_format: {updated_uniform_format}")
    logging.info(f"  Skipped (no K8s checks): {skipped_no_k8s}")
    logging.info(f"  Skipped (already has uniform): {skipped_already_has_uniform}")
    logging.info(f"  Output file: {output_csv}")
    logging.info("="*80)
    
    return updated_total_checks, updated_uniform_format


def main():
    input_csv = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
    output_csv = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL_K8S_COMPLETE.csv"
    
    populate_k8s_columns(input_csv, output_csv)
    
    print("\n✅ K8s columns populated!")
    print(f"\nUpdated file:")
    print(f"  {output_csv}")
    print(f"\nReview and replace if satisfied:")
    print(f"  cp {output_csv} {input_csv}.backup")
    print(f"  mv {output_csv} {input_csv}")


if __name__ == "__main__":
    main()

