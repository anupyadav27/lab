#!/usr/bin/env python3
"""
Standardize rule_list to uniform dot notation format
Adds uniform_rule_format column
"""
import csv
import re

INPUT_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv"
OUTPUT_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv"

def standardize_to_dot_format(rule_id):
    """
    Convert any format to standard dot notation
    
    Examples:
    az::machine_learning_endpoint::check -> az.machine_learning_endpoint.check
    oci.oci_data_science::check -> oci.data_science.check
    aws.api_gateway.stage.check -> aws.api_gateway.stage.check (already correct)
    k8s.k8s.admission.control.check.audited -> k8s.admission.control.check.audited
    """
    # Replace :: with .
    standardized = rule_id.replace('::', '.')
    
    # Remove duplicate service names (e.g., oci.oci_data -> oci.data)
    parts = standardized.split('.')
    cleaned_parts = []
    
    for i, part in enumerate(parts):
        # If this is the second part and it starts with the CSP name, clean it
        if i == 1 and len(cleaned_parts) > 0:
            csp = cleaned_parts[0]
            if part.startswith(f"{csp}_"):
                part = part[len(csp)+1:]  # Remove "csp_" prefix
        cleaned_parts.append(part)
    
    # Join with single dot
    standardized = '.'.join(cleaned_parts)
    
    # Remove any double dots that might have been created
    while '..' in standardized:
        standardized = standardized.replace('..', '.')
    
    return standardized

print("=" * 100)
print("STANDARDIZING RULE_LIST TO UNIFORM DOT FORMAT")
print("=" * 100)
print()

# Read input
rows = []
conversions = {}
format_stats = {'double_colon': 0, 'already_dot': 0, 'other': 0}

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames) + ['uniform_rule_format']
    
    for row in reader:
        rule_id = row.get('rule_id', '')
        
        # Track original format
        if '::' in rule_id:
            format_stats['double_colon'] += 1
        elif rule_id.count('.') >= 2:
            format_stats['already_dot'] += 1
        else:
            format_stats['other'] += 1
        
        # Standardize
        uniform_format = standardize_to_dot_format(rule_id)
        row['uniform_rule_format'] = uniform_format
        
        # Track conversions for reporting
        if rule_id != uniform_format:
            if len(conversions) < 10:  # Sample first 10
                conversions[rule_id] = uniform_format
        
        rows.append(row)

print(f"✓ Processed {len(rows):,} rules")
print()

# Show format statistics
print("Format Statistics:")
for fmt, count in sorted(format_stats.items(), key=lambda x: -x[1]):
    print(f"  {fmt:20s} {count:5,} rules")
print()

# Show sample conversions
if conversions:
    print("Sample Conversions (first 10):")
    for orig, new in list(conversions.items())[:10]:
        print(f"  {orig}")
        print(f"    → {new}")
        print()

# Write output
with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Saved: {OUTPUT_CSV}")
print(f"✓ Added column: uniform_rule_format")
print()
print("=" * 100)
print("✅ RULE_LIST STANDARDIZATION COMPLETE")
print("=" * 100)

