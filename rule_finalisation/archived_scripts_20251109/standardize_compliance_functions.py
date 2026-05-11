#!/usr/bin/env python3
"""
Standardize compliance functions to uniform dot notation format
Adds uniform_rule_format columns for each CSP
"""
import csv

INPUT_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
OUTPUT_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

def convert_underscore_to_dot(function_name):
    """
    Convert underscore notation to dot notation
    
    Examples:
    aws_guardduty_enabled -> aws.guardduty.enabled
    aws_ec2_instance_no_public_ip -> aws.ec2.instance.no_public_ip
    azure_ad_user_mfa_enabled -> azure.ad.user.mfa_enabled
    gcp_compute_disk_encryption_enabled -> gcp.compute.disk.encryption_enabled
    """
    if not function_name or function_name == 'NA':
        return 'NA'
    
    parts = function_name.split('_')
    
    if len(parts) < 2:
        return function_name  # Can't convert
    
    # First part is CSP
    csp = parts[0]
    
    # Second part is usually service
    service = parts[1]
    
    # Rest is resource and check name
    # Strategy: Try to identify resource vs check components
    remaining = parts[2:]
    
    if len(remaining) == 0:
        # csp_service
        return f"{csp}.{service}"
    
    elif len(remaining) == 1:
        # csp_service_check
        return f"{csp}.{service}.{remaining[0]}"
    
    elif len(remaining) == 2:
        # csp_service_resource_check OR csp_service_check_qualifier
        # Heuristic: if second-to-last is a resource-like word, use it as resource
        resource_words = ['instance', 'bucket', 'disk', 'volume', 'database', 'cluster', 
                         'user', 'policy', 'role', 'group', 'key', 'certificate', 'function',
                         'service', 'app', 'vm', 'account', 'storage', 'network', 'firewall']
        
        if remaining[0] in resource_words:
            # csp.service.resource.check
            return f"{csp}.{service}.{remaining[0]}.{remaining[1]}"
        else:
            # csp.service.check_part1_part2
            return f"{csp}.{service}.{'_'.join(remaining)}"
    
    else:
        # csp_service_...multiple_parts
        # Try to identify resource
        resource_idx = None
        for i, part in enumerate(remaining):
            if part in ['instance', 'bucket', 'disk', 'volume', 'database', 'cluster', 
                       'user', 'policy', 'role', 'group', 'key', 'certificate', 'function',
                       'service', 'app', 'vm', 'account', 'storage', 'network', 'firewall']:
                resource_idx = i
                break
        
        if resource_idx is not None:
            # csp.service.resource.check_parts
            resource = remaining[resource_idx]
            check_parts = remaining[resource_idx+1:]
            return f"{csp}.{service}.{resource}.{'_'.join(check_parts)}"
        else:
            # No clear resource, just combine remaining as check
            return f"{csp}.{service}.{'_'.join(remaining)}"

print("=" * 100)
print("STANDARDIZING COMPLIANCE FUNCTIONS TO UNIFORM DOT FORMAT")
print("=" * 100)
print()

# CSP columns to process
csp_columns = {
    'aws_checks': 'aws_uniform_format',
    'azure_checks': 'azure_uniform_format',
    'gcp_checks': 'gcp_uniform_format',
    'oracle_checks': 'oracle_uniform_format',
    'ibm_checks': 'ibm_uniform_format',
    'alicloud_checks': 'alicloud_uniform_format',
    'k8s_checks': 'k8s_uniform_format'
}

rows = []
conversions_sample = []

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    
    # Add new uniform format columns
    for new_col in csp_columns.values():
        if new_col not in fieldnames:
            fieldnames.append(new_col)
    
    for row in reader:
        # Convert each CSP's functions to uniform dot format
        for orig_col, uniform_col in csp_columns.items():
            checks = row.get(orig_col, '')
            
            if checks and checks != 'NA':
                # Split multiple functions
                funcs = [f.strip() for f in checks.split(';') if f.strip()]
                uniform_funcs = []
                
                for func in funcs:
                    uniform = convert_underscore_to_dot(func)
                    uniform_funcs.append(uniform)
                    
                    # Sample first few conversions
                    if len(conversions_sample) < 15:
                        conversions_sample.append((func, uniform))
                
                row[uniform_col] = '; '.join(uniform_funcs)
            else:
                row[uniform_col] = 'NA'
        
        rows.append(row)

print(f"✓ Processed {len(rows):,} compliance requirements")
print()

# Show sample conversions
print("Sample Conversions (first 15):")
for orig, uniform in conversions_sample:
    print(f"  {orig}")
    print(f"    → {uniform}")
print()

# Write output
with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Saved: {OUTPUT_CSV}")
print(f"✓ Added {len(csp_columns)} new uniform format columns")
print()

# Show new column names
print("New columns added:")
for uniform_col in csp_columns.values():
    print(f"  - {uniform_col}")
print()

print("=" * 100)
print("✅ COMPLIANCE STANDARDIZATION COMPLETE")
print("=" * 100)

