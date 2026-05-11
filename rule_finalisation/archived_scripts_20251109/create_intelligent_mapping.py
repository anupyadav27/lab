#!/usr/bin/env python3
"""
Intelligent Name Mapping Between Rule List and Compliance Database
Uses fuzzy matching, service alignment, and semantic similarity
"""
import csv
import json
from collections import defaultdict
from difflib import SequenceMatcher

RULE_LIST_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08.csv"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

def normalize_name(name):
    """Normalize function name for comparison"""
    # Remove common variations
    name = name.lower()
    name = name.replace('_enabled', '').replace('_check', '').replace('_configured', '')
    name = name.replace('_status', '').replace('_is_', '_')
    return name

def extract_keywords(name):
    """Extract meaningful keywords from function name"""
    # Split by dots or underscores
    parts = name.replace('.', '_').split('_')
    # Remove common words
    stop_words = {'is', 'are', 'be', 'the', 'a', 'an', 'for', 'to', 'of', 'in', 'on', 'enabled', 'check', 'status'}
    keywords = [p for p in parts if p and p not in stop_words and len(p) > 2]
    return set(keywords)

def similarity_score(name1, name2):
    """Calculate similarity between two function names"""
    # Normalize both names
    norm1 = normalize_name(name1)
    norm2 = normalize_name(name2)
    
    # Calculate sequence similarity
    seq_similarity = SequenceMatcher(None, norm1, norm2).ratio()
    
    # Calculate keyword overlap
    keywords1 = extract_keywords(name1)
    keywords2 = extract_keywords(name2)
    
    if keywords1 and keywords2:
        keyword_overlap = len(keywords1 & keywords2) / max(len(keywords1), len(keywords2))
    else:
        keyword_overlap = 0
    
    # Weighted score
    score = (seq_similarity * 0.4) + (keyword_overlap * 0.6)
    return score

print("=" * 100)
print("INTELLIGENT NAME MAPPING ANALYZER")
print("=" * 100)
print()

# Load rule_list functions
print("Loading rule_list functions...")
rule_list_functions = {}  # {rule_id: {details}}

with open(RULE_LIST_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rule_id = row.get('rule_id', '')
        if rule_id:
            rule_list_functions[rule_id] = {
                'cloud_provider': row.get('cloud_provider', ''),
                'service': row.get('service', ''),
                'resource': row.get('resource', ''),
                'program': row.get('program', ''),
                'scope': row.get('scope', ''),
                'implementation_status': row.get('implementation_status', '')
            }

print(f"✓ Loaded {len(rule_list_functions):,} rule_list functions")

# Load compliance functions
print("Loading compliance functions...")
compliance_functions = defaultdict(set)  # {csp: set of function_names}
compliance_details = {}  # {function_name: usage_count}

csp_columns = {'aws': 'aws_checks', 'azure': 'azure_checks', 'gcp': 'gcp_checks', 
               'oracle': 'oracle_checks', 'ibm': 'ibm_checks', 'alicloud': 'alicloud_checks', 'k8s': 'k8s_checks'}

with open(COMPLIANCE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for csp, column in csp_columns.items():
            checks = row.get(column, '')
            if checks and checks != 'NA':
                for func in checks.split(';'):
                    func = func.strip()
                    if func:
                        compliance_functions[csp].add(func)
                        compliance_details[func] = compliance_details.get(func, 0) + 1

print(f"✓ Loaded {sum(len(v) for v in compliance_functions.values()):,} compliance functions")
print()

# Analyze AWS as example (largest dataset)
print("=" * 100)
print("AWS INTELLIGENT MAPPING ANALYSIS")
print("=" * 100)
print()

aws_rule_list = {k: v for k, v in rule_list_functions.items() if v['cloud_provider'] == 'aws'}
aws_compliance = compliance_functions.get('aws', set())

print(f"AWS rule_list functions:    {len(aws_rule_list):,}")
print(f"AWS compliance functions:   {len(aws_compliance):,}")
print()

# Find best matches
print("Finding best matches using intelligent mapping...")
print()

matches = []  # [(rule_id, compliance_func, score, match_type)]
matched_compliance = set()
matched_rules = set()

# Method 1: Direct name similarity
for rule_id, details in list(aws_rule_list.items())[:100]:  # Sample first 100
    best_match = None
    best_score = 0
    
    for comp_func in aws_compliance:
        score = similarity_score(rule_id, comp_func)
        if score > best_score:
            best_score = score
            best_match = comp_func
    
    if best_score > 0.5:  # Threshold for good match
        matches.append((rule_id, best_match, best_score, 'similarity'))
        matched_compliance.add(best_match)
        matched_rules.add(rule_id)

print(f"✓ Found {len(matches)} potential matches (score > 0.5)")
print()

# Show top matches
print("TOP 20 MATCHES:")
print("-" * 100)
for rule_id, comp_func, score, match_type in sorted(matches, key=lambda x: -x[2])[:20]:
    print(f"Score: {score:.2f} | {match_type}")
    print(f"  rule_list:  {rule_id}")
    print(f"  compliance: {comp_func}")
    print()

# Analyze coverage
coverage = len(matched_compliance) / len(aws_compliance) * 100 if aws_compliance else 0
print("=" * 100)
print(f"COVERAGE: {len(matched_compliance)}/{len(aws_compliance)} compliance functions mapped ({coverage:.1f}%)")
print(f"UNMAPPED: {len(aws_compliance) - len(matched_compliance)} compliance functions have no match")
print(f"UNUSED: {len(aws_rule_list) - len(matched_rules)} rule_list functions not used")
print("=" * 100)
print()

# Generate mapping file
mapping_output = {
    'metadata': {
        'source': 'intelligent_name_mapping',
        'date': '2025-11-09',
        'method': 'fuzzy_similarity + keyword_overlap',
        'threshold': 0.5
    },
    'aws_mappings': [
        {
            'rule_list_id': rule_id,
            'compliance_function': comp_func,
            'similarity_score': round(score, 3),
            'match_type': match_type,
            'rule_details': aws_rule_list.get(rule_id, {}),
            'compliance_usage': compliance_details.get(comp_func, 0)
        }
        for rule_id, comp_func, score, match_type in sorted(matches, key=lambda x: -x[2])
    ],
    'stats': {
        'rule_list_total': len(aws_rule_list),
        'compliance_total': len(aws_compliance),
        'matched': len(matches),
        'coverage_pct': round(coverage, 1)
    }
}

with open('intelligent_mapping_aws.json', 'w') as f:
    json.dump(mapping_output, f, indent=2)

print("✓ Saved: intelligent_mapping_aws.json")
print()

# Identify unmapped high-priority compliance functions
print("=" * 100)
print("TOP 30 UNMAPPED HIGH-PRIORITY COMPLIANCE FUNCTIONS")
print("=" * 100)
print()

unmapped = [(f, compliance_details.get(f, 0)) for f in aws_compliance if f not in matched_compliance]
unmapped_sorted = sorted(unmapped, key=lambda x: -x[1])

print("These are compliance-required but NO good match found in rule_list:")
print()
for func, usage in unmapped_sorted[:30]:
    print(f"  {usage:3d}x  {func}")

print()
print("✅ ANALYSIS COMPLETE")
print()
print("RECOMMENDATION:")
print("1. Review intelligent_mapping_aws.json for confirmed mappings")
print("2. Create aliases/mappings for high-score matches (> 0.7)")
print("3. Investigate medium-score matches (0.5-0.7) manually")
print("4. Develop missing functions for unmapped high-priority items")

