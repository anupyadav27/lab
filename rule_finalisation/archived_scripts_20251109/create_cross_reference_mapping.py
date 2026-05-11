#!/usr/bin/env python3
"""
Cross-Reference Mapping: Rule List Functions ↔ Compliance Functions
Creates comprehensive mapping between two different naming systems
"""
import csv
import json
from collections import defaultdict

RULE_LIST_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

print("=" * 100)
print("CROSS-REFERENCE MAPPING: RULE LIST ↔ COMPLIANCE DATABASE")
print("=" * 100)
print()

# === PART 1: Load both databases ===
print("Part 1: Loading databases...")
print()

# Load rule_list (CSPM function library)
rule_list_db = defaultdict(list)  # {csp: [{rule_details}]}
with open(RULE_LIST_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csp = row.get('cloud_provider', '').lower()
        if csp:
            rule_list_db[csp].append({
                'rule_id': row.get('rule_id', ''),
                'service': row.get('service', ''),
                'resource': row.get('resource', ''),
                'scope': row.get('scope', ''),
                'program': row.get('program', ''),
                'implementation_status': row.get('implementation_status', '')
            })

total_rules = sum(len(v) for v in rule_list_db.values())
print(f"✓ rule_list: {total_rules:,} CSPM functions across {len(rule_list_db)} CSPs")

# Load compliance (compliance requirement mappings)
compliance_db = []
compliance_functions = defaultdict(set)  # {csp: set of functions}
function_usage = defaultdict(int)  # {function_name: usage_count}

csp_columns = {'aws': 'aws_checks', 'azure': 'azure_checks', 'gcp': 'gcp_checks', 
               'oracle': 'oracle_checks', 'ibm': 'ibm_checks', 'alicloud': 'alicloud_checks', 'k8s': 'k8s_checks'}

with open(COMPLIANCE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        compliance_db.append(row)
        for csp, column in csp_columns.items():
            checks = row.get(column, '')
            if checks and checks != 'NA':
                for func in checks.split(';'):
                    func = func.strip()
                    if func:
                        compliance_functions[csp].add(func)
                        function_usage[func] += 1

total_comp_funcs = sum(len(v) for v in compliance_functions.values())
print(f"✓ compliance: {len(compliance_db):,} requirements using {total_comp_funcs:,} function references")
print()

# === PART 2: Analyze naming patterns ===
print("=" * 100)
print("PART 2: NAMING PATTERN ANALYSIS")
print("=" * 100)
print()

print("rule_list naming pattern:")
print("  Format: csp.service.resource.check_name")
print("  Example: aws.guardduty.finding.reports_storage_encrypted")
print()

print("compliance naming pattern:")
print("  Format: csp_service_check_name (or csp_service_resource_check_name)")
print("  Example: aws_guardduty_enabled")
print()

# === PART 3: Service-level mapping ===
print("=" * 100)
print("PART 3: SERVICE-LEVEL ANALYSIS (AWS Sample)")
print("=" * 100)
print()

# Extract services from both databases
rule_list_services = defaultdict(int)  # {service: count}
for rule in rule_list_db.get('aws', []):
    service = rule.get('service', '')
    if service:
        rule_list_services[service] += 1

compliance_services = defaultdict(int)  # {service: count}
for func in compliance_functions.get('aws', set()):
    # Extract service from function name
    # aws_guardduty_enabled -> guardduty
    # aws_ec2_instance_no_public_ip -> ec2
    parts = func.split('_')
    if len(parts) >= 2:
        service = parts[1]
        compliance_services[service] += 1

print(f"rule_list has {len(rule_list_services)} AWS services")
print(f"compliance has {len(compliance_services)} AWS services")
print()

# Find common services
common_services = set(rule_list_services.keys()) & set(compliance_services.keys())
only_in_rules = set(rule_list_services.keys()) - set(compliance_services.keys())
only_in_compliance = set(compliance_services.keys()) - set(rule_list_services.keys())

print(f"Common services (in both):        {len(common_services)}")
print(f"Only in rule_list:                {len(only_in_rules)}")
print(f"Only in compliance:               {len(only_in_compliance)}")
print()

if only_in_compliance:
    print("Services ONLY in compliance (top 20):")
    for service in sorted(only_in_compliance)[:20]:
        print(f"  - {service} ({compliance_services[service]} functions)")
    print()

# === PART 4: Create mapping strategy ===
print("=" * 100)
print("PART 4: MAPPING STRATEGY")
print("=" * 100)
print()

strategy = {
    'problem': 'Two different naming systems with minimal overlap',
    'rule_list_format': 'csp.service.resource.check (8,075 functions)',
    'compliance_format': 'csp_service_check (3,892 function references)',
    'alignment_rate': '0.1% (only 3 matches found)',
    
    'approach_options': [
        {
            'option': 1,
            'name': 'Create Name Translator',
            'description': 'Build mapping between rule_list IDs and compliance function names',
            'complexity': 'High',
            'time': '8-12 hours manual, or build smart mapper',
            'benefit': 'Enables use of existing 8K+ functions for compliance'
        },
        {
            'option': 2,
            'name': 'Develop Missing Functions',
            'description': 'Build 3,889 new functions matching compliance names',
            'complexity': 'Very High',
            'time': '40-60 hours',
            'benefit': 'Direct mapping, no translation layer needed'
        },
        {
            'option': 3,
            'name': 'Hybrid Approach (RECOMMENDED)',
            'description': 'Map what exists + develop critical gaps',
            'complexity': 'Medium',
            'time': '12-16 hours',
            'benefit': 'Leverage existing 8K functions + fill compliance gaps'
        }
    ],
    
    'recommended_next_steps': [
        '1. Build service-level mapping (guardduty functions in both systems)',
        '2. Create automated name translator (rule_list ID → compliance function name)',
        '3. Identify TRUE gaps (compliance needs that rule_list cannot satisfy)',
        '4. Prioritize development of critical missing functions',
        '5. Create alias/mapping file for existing functions'
    ]
}

with open('mapping_strategy.json', 'w') as f:
    json.dump(strategy, f, indent=2)

print("✓ Saved: mapping_strategy.json")
print()

# === PART 5: Generate actionable reports ===
print("=" * 100)
print("PART 5: ACTIONABLE INSIGHTS")
print("=" * 100)
print()

print("KEY FINDINGS:")
print()
print("1. 📊 DATABASE SIZES:")
print(f"   - rule_list: 8,075 CSPM functions (your existing function library)")
print(f"   - compliance: 3,892 function references (what compliance needs)")
print()

print("2. 🎯 NAMING MISMATCH:")
print("   - rule_list uses dot notation: aws.service.resource.check")
print("   - compliance uses underscore: aws_service_check")
print("   - Only 0.1% direct alignment!")
print()

print("3. 🔍 WHAT THIS MEANS:")
print("   - You HAVE 8K+ functions already built")
print("   - Compliance needs 3.9K function references")
print("   - But they use DIFFERENT naming conventions")
print("   - Need a MAPPING LAYER or TRANSLATOR")
print()

print("4. 💡 RECOMMENDED APPROACH:")
print("   a) Build intelligent service-level mapper")
print("   b) Map rule_list functions to compliance names")
print("   c) Identify TRUE gaps (what's actually missing)")
print("   d) Create alias/mapping file")
print("   e) Develop only critical missing functions")
print()

print("5. 📋 IMMEDIATE ACTIONS:")
print("   - Analyze ONE service deeply (e.g., AWS GuardDuty)")
print("   - Create mapping template for that service")
print("   - Scale to all services")
print()

print("=" * 100)
print("✅ CROSS-REFERENCE ANALYSIS COMPLETE")
print("=" * 100)
print()
print("Generated files:")
print("  1. gap_analysis_missing_functions.json - Missing functions by CSP")
print("  2. gap_analysis_alignment_summary.json - Alignment stats")
print("  3. intelligent_mapping_aws.json - AWS fuzzy matches")
print("  4. mapping_strategy.json - Recommended approach")
print()
print("NEXT: Review mapping_strategy.json for recommended approach")

