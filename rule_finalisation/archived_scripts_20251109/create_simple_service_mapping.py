#!/usr/bin/env python3
"""
Create Simple Service Mappings - Just rule_ids and compliance functions
Clean format for easy mapping work
"""
import csv
import json
from collections import defaultdict

RULE_LIST_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
OUTPUT_DIR = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings"

CSP_CONFIGS = {
    'aws': {'name': 'AWS', 'compliance_column': 'aws_uniform_format'},
    'azure': {'name': 'Azure', 'compliance_column': 'azure_uniform_format', 'rule_list_name': 'az'},
    'gcp': {'name': 'GCP', 'compliance_column': 'gcp_uniform_format'},
    'oracle': {'name': 'Oracle', 'compliance_column': 'oracle_uniform_format', 'rule_list_name': 'oci'},
    'ibm': {'name': 'IBM', 'compliance_column': 'ibm_uniform_format'},
    'alicloud': {'name': 'Alicloud', 'compliance_column': 'alicloud_uniform_format'},
    'k8s': {'name': 'Kubernetes', 'compliance_column': 'k8s_uniform_format'}
}

print("=" * 80)
print("CREATING SIMPLE SERVICE MAPPINGS (Clean Format)")
print("=" * 80)
print()

# Load rule_list
rule_list_by_csp = defaultdict(lambda: defaultdict(list))

with open(RULE_LIST_CSV, 'r') as f:
    for row in csv.DictReader(f):
        csp = row.get('cloud_provider', '').lower()
        service = row.get('service', '')
        uniform = row.get('uniform_rule_format', '')
        
        if csp and service and uniform:
            rule_list_by_csp[csp][service].append(uniform)

# Load compliance
compliance_by_csp = defaultdict(lambda: defaultdict(set))

with open(COMPLIANCE_CSV, 'r') as f:
    for row in csv.DictReader(f):
        for csp_key, config in CSP_CONFIGS.items():
            column = config['compliance_column']
            checks = row.get(column, '')
            
            if checks and checks != 'NA':
                for func in checks.split(';'):
                    func = func.strip()
                    if func and func != 'NA':
                        parts = func.split('.')
                        if len(parts) >= 2:
                            service = parts[1]
                            compliance_by_csp[csp_key][service].add(func)

# Create simple mappings for each CSP
print("Creating mappings...")
for csp_key, config in CSP_CONFIGS.items():
    csp_name = config['name']
    rule_list_csp = config.get('rule_list_name', csp_key)
    
    rule_services = rule_list_by_csp.get(rule_list_csp, {})
    comp_services = compliance_by_csp.get(csp_key, {})
    
    all_services = sorted(set(rule_services.keys()) | set(comp_services.keys()))
    
    # Build simple mapping
    simple_mapping = {}
    
    for service in all_services:
        simple_mapping[service] = {
            'rules': sorted(rule_services.get(service, [])),
            'compliance_functions': sorted(comp_services.get(service, set()))
        }
    
    # Save
    output_file = f"{OUTPUT_DIR}/{csp_key}_simple_mapping.json"
    with open(output_file, 'w') as f:
        json.dump(simple_mapping, f, indent=2)
    
    rl_count = sum(len(v['rules']) for v in simple_mapping.values())
    comp_count = sum(len(v['compliance_functions']) for v in simple_mapping.values())
    
    print(f"  ✓ {csp_name}: {len(all_services)} services, {rl_count} rules, {comp_count} compliance")

print()
print("=" * 80)
print("✅ SIMPLE MAPPINGS CREATED")
print("=" * 80)
print()
print(f"Location: {OUTPUT_DIR}/")
print("Files: *_simple_mapping.json")

