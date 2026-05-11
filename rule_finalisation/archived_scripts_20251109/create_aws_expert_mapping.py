#!/usr/bin/env python3
"""
AWS Expert Mapping - Intelligently map rule_list rules to compliance functions
Acts as AWS security expert to identify best mappings
"""
import json
from difflib import SequenceMatcher

INPUT_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/aws_simple_mapping.json"
OUTPUT_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/aws_simple_mapping.json"

def calculate_relevance(rule_id, compliance_func):
    """
    Calculate relevance score between a rule and compliance function
    Returns score 0-1 and reason
    """
    # Extract keywords from both
    rule_parts = set(rule_id.lower().split('.'))
    comp_parts = set(compliance_func.lower().split('.'))
    
    # Common keywords
    common = rule_parts & comp_parts
    
    # Similarity score
    similarity = SequenceMatcher(None, rule_id.lower(), compliance_func.lower()).ratio()
    
    # Check for semantic matches
    semantic_matches = []
    
    # Enabled/disabled checks
    if 'enabled' in compliance_func:
        if 'enabled' in rule_id or 'detectors_enabled' in rule_id or 'status' in rule_id:
            semantic_matches.append('enabled_check')
    
    # Public access checks
    if 'public' in compliance_func or 'no_public' in compliance_func:
        if 'public' in rule_id or 'private' in rule_id or 'accessible' in rule_id:
            semantic_matches.append('access_control')
    
    # Encryption checks
    if 'encrypt' in compliance_func:
        if 'encrypt' in rule_id or 'kms' in rule_id or 'cmk' in rule_id:
            semantic_matches.append('encryption')
    
    # Logging/monitoring
    if 'log' in compliance_func or 'monitoring' in compliance_func:
        if 'log' in rule_id or 'monitor' in rule_id or 'audit' in rule_id:
            semantic_matches.append('logging')
    
    # Multi-region/availability
    if 'multi' in compliance_func or 'all_regions' in compliance_func:
        if 'multi' in rule_id or 'all_regions' in rule_id or 'region' in rule_id:
            semantic_matches.append('multi_region')
    
    # MFA checks
    if 'mfa' in compliance_func:
        if 'mfa' in rule_id or 'multi_factor' in rule_id or 'authentication' in rule_id:
            semantic_matches.append('mfa')
    
    # Backup checks
    if 'backup' in compliance_func:
        if 'backup' in rule_id or 'snapshot' in rule_id or 'retention' in rule_id:
            semantic_matches.append('backup')
    
    # Calculate final score
    keyword_score = len(common) / max(len(rule_parts), len(comp_parts)) if rule_parts or comp_parts else 0
    semantic_score = len(semantic_matches) * 0.2
    
    final_score = (similarity * 0.3) + (keyword_score * 0.4) + min(semantic_score, 0.3)
    
    reason = []
    if common:
        reason.append(f"common_keywords: {', '.join(sorted(common)[:3])}")
    if semantic_matches:
        reason.append(f"semantic: {', '.join(semantic_matches)}")
    
    return final_score, ' | '.join(reason) if reason else 'low_similarity'

def map_compliance_to_rules(service, rules, compliance_functions):
    """
    For each compliance function, find best matching rules
    Returns updated compliance functions with mappings
    """
    mapped_compliance = []
    
    for comp_func in compliance_functions:
        # Find all rules with relevance > threshold
        matches = []
        
        for rule in rules:
            score, reason = calculate_relevance(rule, comp_func)
            
            if score >= 0.4:  # Threshold for relevance
                matches.append({
                    'rule_id': rule,
                    'score': round(score, 2),
                    'reason': reason
                })
        
        # Sort by score
        matches.sort(key=lambda x: -x['score'])
        
        # Create mapping entry
        mapped_compliance.append({
            'name': comp_func,
            'mapping': [m['rule_id'] for m in matches[:5]],  # Top 5 matches
            'mapping_confidence': matches[0]['score'] if matches else 0,
            'mapping_details': matches[:3] if matches else []  # Top 3 with details
        })
    
    return mapped_compliance

print("=" * 100)
print("AWS EXPERT MAPPING - Intelligent Rule-to-Compliance Matching")
print("=" * 100)
print()

# Load current mapping
with open(INPUT_FILE, 'r') as f:
    aws_mapping = json.load(f)

print(f"Loaded {len(aws_mapping)} AWS services")
print()

# Process each service
print("Creating intelligent mappings...")
services_processed = 0
total_mappings = 0

for service, data in aws_mapping.items():
    rules = data.get('rules', [])
    compliance_funcs = data.get('compliance_functions', [])
    
    if compliance_funcs:
        # Map compliance functions to rules
        mapped_compliance = map_compliance_to_rules(service, rules, compliance_funcs)
        
        # Update the structure
        aws_mapping[service]['compliance_functions'] = mapped_compliance
        
        services_processed += 1
        mappings_found = sum(1 for c in mapped_compliance if c['mapping'])
        total_mappings += mappings_found
        
        if services_processed <= 5:  # Show first 5 services
            print(f"  ✓ {service}: {len(compliance_funcs)} compliance funcs, {mappings_found} mapped")

if services_processed > 5:
    print(f"  ... and {services_processed - 5} more services processed")

print()
print(f"✓ Total services processed: {services_processed}")
print(f"✓ Total mappings created: {total_mappings}")
print()

# Save updated mapping
with open(OUTPUT_FILE, 'w') as f:
    json.dump(aws_mapping, f, indent=2)

print(f"✓ Saved: {OUTPUT_FILE}")
print()

# Show sample mapping
print("=" * 100)
print("SAMPLE MAPPING: GuardDuty")
print("=" * 100)
print()

if 'guardduty' in aws_mapping:
    gd = aws_mapping['guardduty']
    print(f"Available rules: {len(gd['rules'])}")
    print(f"Compliance functions: {len(gd['compliance_functions'])}")
    print()
    
    for comp in gd['compliance_functions'][:3]:
        print(f"Compliance: {comp['name']}")
        if comp['mapping']:
            print(f"  Confidence: {comp['mapping_confidence']}")
            print(f"  Mapped to:")
            for detail in comp.get('mapping_details', []):
                print(f"    - {detail['rule_id']} (score: {detail['score']}) - {detail['reason']}")
        else:
            print(f"  ❌ No good mapping found - needs development")
        print()

print("=" * 100)
print("✅ AWS EXPERT MAPPING COMPLETE")
print("=" * 100)
print()
print("Review the updated aws_simple_mapping.json to see all mappings!")

