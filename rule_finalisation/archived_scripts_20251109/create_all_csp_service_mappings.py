#!/usr/bin/env python3
"""
Create Service-by-Service Mappings for ALL CSPs
Common format for easy comparison across cloud providers
"""
import csv
import json
from collections import defaultdict

RULE_LIST_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
OUTPUT_DIR = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings"

# CSP configurations
CSP_CONFIGS = {
    'aws': {'name': 'AWS', 'compliance_column': 'aws_uniform_format'},
    'azure': {'name': 'Azure', 'compliance_column': 'azure_uniform_format', 'rule_list_name': 'az'},
    'gcp': {'name': 'GCP', 'compliance_column': 'gcp_uniform_format'},
    'oracle': {'name': 'Oracle', 'compliance_column': 'oracle_uniform_format', 'rule_list_name': 'oci'},
    'ibm': {'name': 'IBM', 'compliance_column': 'ibm_uniform_format'},
    'alicloud': {'name': 'Alicloud', 'compliance_column': 'alicloud_uniform_format'},
    'k8s': {'name': 'Kubernetes', 'compliance_column': 'k8s_uniform_format'}
}

print("=" * 100)
print("CREATING SERVICE MAPPINGS FOR ALL CSPs")
print("=" * 100)
print()

import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === LOAD RULE_LIST ===
print("Loading rule_list database...")
rule_list_by_csp = defaultdict(lambda: defaultdict(list))

with open(RULE_LIST_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csp = row.get('cloud_provider', '').lower()
        service = row.get('service', '')
        uniform = row.get('uniform_rule_format', '')
        
        if csp and service and uniform:
            rule_list_by_csp[csp][service].append({
                'rule_id': uniform,
                'original_rule_id': row.get('rule_id', ''),
                'scope': row.get('scope', ''),
                'resource': row.get('resource', ''),
                'program': row.get('program', ''),
                'implementation_status': row.get('implementation_status', ''),
                'mapping_status': row.get('mapping_status', '')
            })

print(f"✓ Loaded rule_list for {len(rule_list_by_csp)} CSPs")
print()

# === LOAD COMPLIANCE ===
print("Loading compliance database...")
compliance_by_csp = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

with open(COMPLIANCE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for csp_key, config in CSP_CONFIGS.items():
            column = config['compliance_column']
            checks = row.get(column, '')
            
            if checks and checks != 'NA':
                for func in checks.split(';'):
                    func = func.strip()
                    if func and func != 'NA':
                        # Extract service from function
                        parts = func.split('.')
                        if len(parts) >= 2:
                            service = parts[1]
                            compliance_by_csp[csp_key][service][func] += 1

print(f"✓ Loaded compliance for {len(compliance_by_csp)} CSPs")
print()

# === CREATE SERVICE MAPPINGS FOR EACH CSP ===
print("Creating service mappings...")
print()

summary_stats = []

for csp_key, config in CSP_CONFIGS.items():
    csp_name = config['name']
    rule_list_csp = config.get('rule_list_name', csp_key)
    
    print(f"Processing {csp_name}...")
    
    # Get data for this CSP
    rule_list_services = rule_list_by_csp.get(rule_list_csp, {})
    compliance_services = compliance_by_csp.get(csp_key, {})
    
    # Get all services
    all_services = sorted(set(rule_list_services.keys()) | set(compliance_services.keys()))
    
    # Build mapping
    mapping = {
        'metadata': {
            'cloud_provider': csp_name,
            'csp_key': csp_key,
            'date': '2025-11-09',
            'total_services': len(all_services),
            'services_in_rule_list': len(rule_list_services),
            'services_in_compliance': len(compliance_services),
            'common_services': len(set(rule_list_services.keys()) & set(compliance_services.keys()))
        },
        'services': {}
    }
    
    for service in all_services:
        rule_list_funcs = rule_list_services.get(service, [])
        compliance_funcs = compliance_services.get(service, {})
        
        # Build compliance function list with priority
        compliance_func_list = [
            {
                'function': func,
                'usage_count': count,
                'priority': 'critical' if count >= 50 else 'high' if count >= 20 else 'medium' if count >= 5 else 'low'
            }
            for func, count in sorted(compliance_funcs.items(), key=lambda x: -x[1])
        ]
        
        mapping['services'][service] = {
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
                'rule_list_count': len(rule_list_funcs),
                'compliance_count': len(compliance_func_list),
                'status': 'both' if rule_list_funcs and compliance_func_list else 
                         'rule_list_only' if rule_list_funcs else 
                         'compliance_only' if compliance_func_list else 
                         'none'
            }
        }
    
    # Save to file
    output_file = f"{OUTPUT_DIR}/{csp_key}_service_mapping.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)
    
    # Summary stats
    both_count = len([s for s, d in mapping['services'].items() if d['alignment']['status'] == 'both'])
    rule_only = len([s for s, d in mapping['services'].items() if d['alignment']['status'] == 'rule_list_only'])
    comp_only = len([s for s, d in mapping['services'].items() if d['alignment']['status'] == 'compliance_only'])
    
    total_rl = sum(d['rule_list']['count'] for d in mapping['services'].values())
    total_comp = sum(d['compliance']['count'] for d in mapping['services'].values())
    
    summary_stats.append({
        'csp': csp_name,
        'file': f"{csp_key}_service_mapping.json",
        'services': len(all_services),
        'both': both_count,
        'rule_only': rule_only,
        'comp_only': comp_only,
        'rule_list_funcs': total_rl,
        'compliance_funcs': total_comp
    })
    
    print(f"  ✓ {csp_name}: {len(all_services)} services, {both_count} in both")

print()
print("=" * 100)
print("ALL CSP SERVICE MAPPINGS SUMMARY")
print("=" * 100)
print()

print(f"{'CSP':<12} {'Services':<10} {'In Both':<10} {'rule_list':<12} {'compliance':<12} {'File'}")
print("-" * 100)
for stat in summary_stats:
    print(f"{stat['csp']:<12} {stat['services']:<10} {stat['both']:<10} {stat['rule_list_funcs']:<12} {stat['compliance_funcs']:<12} {stat['file']}")

print()
print("=" * 100)
print("✅ ALL CSP SERVICE MAPPINGS CREATED")
print("=" * 100)
print()
print(f"Location: {OUTPUT_DIR}/")
print("Files created:")
for stat in summary_stats:
    print(f"  - {stat['file']}")

