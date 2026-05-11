#!/usr/bin/env python3
"""
Create Service-by-Service Mapping for AWS
Groups rule_list and compliance functions by AWS service for easy comparison
"""
import csv
import json
from collections import defaultdict

RULE_LIST_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
OUTPUT_JSON = "/Users/apple/Desktop/compliance_Database/rule_finalisation/aws_service_mapping.json"

print("=" * 100)
print("CREATING AWS SERVICE-BY-SERVICE MAPPING")
print("=" * 100)
print()

# === STEP 1: Extract rule_list functions by service ===
print("Step 1: Loading rule_list functions...")

rule_list_by_service = defaultdict(list)

with open(RULE_LIST_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('cloud_provider') == 'aws':
            uniform = row.get('uniform_rule_format', '')
            service = row.get('service', '')
            
            if uniform and service:
                rule_list_by_service[service].append({
                    'rule_id': uniform,
                    'original_rule_id': row.get('rule_id', ''),
                    'scope': row.get('scope', ''),
                    'resource': row.get('resource', ''),
                    'program': row.get('program', ''),
                    'implementation_status': row.get('implementation_status', ''),
                    'mapping_status': row.get('mapping_status', '')
                })

print(f"✓ Found {len(rule_list_by_service)} AWS services in rule_list")
print(f"✓ Total functions: {sum(len(v) for v in rule_list_by_service.values())}")
print()

# === STEP 2: Extract compliance functions by service ===
print("Step 2: Loading compliance functions...")

compliance_by_service = defaultdict(lambda: defaultdict(int))  # {service: {function: usage_count}}
compliance_details = defaultdict(list)  # {service: [compliance_requirements]}

with open(COMPLIANCE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        aws_uniform = row.get('aws_uniform_format', '')
        
        if aws_uniform and aws_uniform != 'NA':
            # Split multiple functions
            for func in aws_uniform.split(';'):
                func = func.strip()
                if func and func != 'NA':
                    # Extract service from function
                    # aws.guardduty.enabled -> guardduty
                    # aws.ec2.instance.no_public_ip -> ec2
                    parts = func.split('.')
                    if len(parts) >= 2:
                        service = parts[1]
                        compliance_by_service[service][func] += 1
                        
                        # Store which compliance requirement uses this
                        compliance_details[service].append({
                            'compliance_id': row.get('unique_compliance_id', ''),
                            'framework': row.get('compliance_framework', ''),
                            'requirement_id': row.get('requirement_id', ''),
                            'function': func
                        })

print(f"✓ Found {len(compliance_by_service)} AWS services in compliance")
print(f"✓ Total unique functions: {sum(len(v) for v in compliance_by_service.values())}")
print()

# === STEP 3: Create service mapping ===
print("Step 3: Creating service-by-service mapping...")

all_services = sorted(set(rule_list_by_service.keys()) | set(compliance_by_service.keys()))

aws_mapping = {
    'metadata': {
        'cloud_provider': 'AWS',
        'date': '2025-11-09',
        'total_services': len(all_services),
        'services_in_rule_list': len(rule_list_by_service),
        'services_in_compliance': len(compliance_by_service),
        'common_services': len(set(rule_list_by_service.keys()) & set(compliance_by_service.keys()))
    },
    'services': {}
}

for service in all_services:
    rule_list_funcs = rule_list_by_service.get(service, [])
    compliance_funcs = compliance_by_service.get(service, {})
    
    # Get unique compliance functions for this service
    compliance_func_list = [
        {
            'function': func,
            'usage_count': count,
            'priority': 'critical' if count >= 50 else 'high' if count >= 20 else 'medium' if count >= 5 else 'low'
        }
        for func, count in sorted(compliance_funcs.items(), key=lambda x: -x[1])
    ]
    
    aws_mapping['services'][service] = {
        'service_name': service,
        'rule_list': {
            'count': len(rule_list_funcs),
            'functions': sorted(rule_list_funcs, key=lambda x: x['rule_id'])
        },
        'compliance': {
            'count': len(compliance_func_list),
            'total_usage': sum(f['usage_count'] for f in compliance_func_list),
            'functions': compliance_func_list
        },
        'alignment': {
            'has_rule_list': len(rule_list_funcs) > 0,
            'has_compliance': len(compliance_func_list) > 0,
            'status': 'both' if rule_list_funcs and compliance_func_list else 
                     'rule_list_only' if rule_list_funcs else 
                     'compliance_only' if compliance_func_list else 
                     'none'
        }
    }

# Save mapping
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(aws_mapping, f, indent=2)

print(f"✓ Saved: {OUTPUT_JSON}")
print()

# === STEP 4: Generate summary statistics ===
print("=" * 100)
print("AWS SERVICE MAPPING SUMMARY")
print("=" * 100)
print()

print(f"Total AWS Services:           {len(all_services)}")
print(f"Services in rule_list:        {len(rule_list_by_service)}")
print(f"Services in compliance:       {len(compliance_by_service)}")
print(f"Services in BOTH:             {aws_mapping['metadata']['common_services']}")
print()

# Services with both
both = [(s, len(rule_list_by_service[s]), len(compliance_by_service[s])) 
        for s in all_services 
        if s in rule_list_by_service and s in compliance_by_service]

rule_only = [(s, len(rule_list_by_service[s])) 
             for s in all_services 
             if s in rule_list_by_service and s not in compliance_by_service]

comp_only = [(s, len(compliance_by_service[s])) 
             for s in all_services 
             if s not in rule_list_by_service and s in compliance_by_service]

print(f"SERVICES IN BOTH (top 20):")
print("-" * 100)
print(f"{'Service':<25} {'rule_list':<12} {'compliance':<12} {'Status'}")
print("-" * 100)
for service, rl_count, comp_count in sorted(both, key=lambda x: -(x[1] + x[2]))[:20]:
    status = "✅ Can map" if rl_count >= comp_count else "🔧 Partial"
    print(f"{service:<25} {rl_count:<12} {comp_count:<12} {status}")

if len(both) > 20:
    print(f"... and {len(both) - 20} more services")
print()

if comp_only:
    print(f"SERVICES ONLY IN COMPLIANCE (need development):")
    print("-" * 100)
    for service, count in sorted(comp_only, key=lambda x: -x[1])[:15]:
        print(f"  {service:<25} {count} functions needed")
    if len(comp_only) > 15:
        print(f"  ... and {len(comp_only) - 15} more")
    print()

if rule_only:
    print(f"SERVICES ONLY IN rule_list (unused in compliance): {len(rule_only)} services")
    print()

print("=" * 100)
print("✅ AWS SERVICE MAPPING COMPLETE")
print("=" * 100)
print()
print(f"Review: {OUTPUT_JSON}")
print("  - Organized by service")
print("  - Shows rule_list vs compliance side-by-side")
print("  - Easy to identify mapping opportunities")

