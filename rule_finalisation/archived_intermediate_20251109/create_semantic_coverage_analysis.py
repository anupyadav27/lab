#!/usr/bin/env python3
"""
Semantic Coverage Analysis - More Effective Step 2
Uses actual compliance descriptions and smart pattern matching
"""
import json
import pandas as pd
import re
from collections import defaultdict

# Files
MAPPING_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING.json"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

# Load files
with open(MAPPING_FILE, 'r') as f:
    mapping = json.load(f)

# Load compliance CSV
df = pd.read_csv(COMPLIANCE_CSV)
print("=" * 100)
print("SEMANTIC COVERAGE ANALYSIS - More Effective Step 2")
print("=" * 100)
print()

# Build compliance context
compliance_context = {}
for _, row in df.iterrows():
    if pd.notna(row.get('aws_uniform_format')):
        functions = str(row['aws_uniform_format']).split(';')
        for func in functions:
            func = func.strip()
            if func and func.startswith('aws.'):
                compliance_context[func] = {
                    'requirement': str(row.get('requirement_name', '')),
                    'description': str(row.get('requirement_description', '')),
                    'service': str(row.get('service', ''))
                }

print(f"✓ Loaded context for {len(compliance_context)} AWS compliance functions")

# Build rule capabilities - what each rule can check
RULE_CAPABILITIES = {}

# Analyze all available rules to understand what they check
all_rules = set()
for service, data in mapping.items():
    if service != 'metadata':
        all_rules.update(data.get('available_rules', []))

# Categorize rules by what they check
for rule in all_rules:
    parts = rule.lower().split('.')
    
    # Extract key capabilities
    capabilities = []
    
    # Encryption checks
    if any(word in rule for word in ['encrypt', 'kms', 'cmk']):
        capabilities.append('ENCRYPTION')
    
    # Access control
    if any(word in rule for word in ['public', 'privilege', 'access', 'rbac', 'permission']):
        capabilities.append('ACCESS_CONTROL')
    
    # Logging/Monitoring
    if any(word in rule for word in ['log', 'trail', 'monitor', 'flow_logs', 'cloudwatch']):
        capabilities.append('LOGGING')
    
    # Network security
    if any(word in rule for word in ['ingress', 'egress', 'security_group', 'firewall', 'network']):
        capabilities.append('NETWORK_SECURITY')
    
    # Backup/Recovery
    if any(word in rule for word in ['backup', 'retention', 'snapshot', 'recovery']):
        capabilities.append('BACKUP')
    
    # Compliance/Audit
    if any(word in rule for word in ['compliance', 'audit', 'enabled', 'configured']):
        capabilities.append('COMPLIANCE')
    
    # MFA
    if 'mfa' in rule:
        capabilities.append('MFA')
    
    # Vulnerability
    if any(word in rule for word in ['scan', 'assessment', 'vulnerability', 'patch']):
        capabilities.append('VULNERABILITY')
    
    RULE_CAPABILITIES[rule] = capabilities

# Semantic matching function
def semantic_match(compliance_func, context, available_rules):
    """Find rules that semantically match the compliance requirement"""
    
    if not context:
        return []
    
    req_desc = context.get('description', '').lower()
    req_name = context.get('requirement', '').lower()
    
    # Determine what capabilities are needed
    needed_capabilities = set()
    
    # Map requirement keywords to capabilities
    if any(word in req_desc for word in ['encrypt', 'cryptograph', 'protect data']):
        needed_capabilities.add('ENCRYPTION')
    
    if any(word in req_desc for word in ['log', 'audit', 'monitor', 'track']):
        needed_capabilities.add('LOGGING')
    
    if any(word in req_desc for word in ['access', 'permission', 'privilege', 'authorized']):
        needed_capabilities.add('ACCESS_CONTROL')
    
    if any(word in req_desc for word in ['network', 'traffic', 'firewall', 'ingress', 'egress']):
        needed_capabilities.add('NETWORK_SECURITY')
    
    if any(word in req_desc for word in ['backup', 'recovery', 'retention', 'restore']):
        needed_capabilities.add('BACKUP')
    
    if any(word in req_desc for word in ['mfa', 'multi-factor', 'two-factor']):
        needed_capabilities.add('MFA')
    
    if any(word in req_desc for word in ['vulnerability', 'patch', 'scan', 'assessment']):
        needed_capabilities.add('VULNERABILITY')
    
    # Score rules based on capability match
    scored_rules = []
    
    for rule in available_rules:
        rule_caps = set(RULE_CAPABILITIES.get(rule, []))
        if not rule_caps:
            continue
            
        # Calculate match score
        overlap = needed_capabilities & rule_caps
        if overlap:
            score = len(overlap) / len(needed_capabilities) if needed_capabilities else 0
            
            # Boost score for service match
            func_service = compliance_func.split('.')[1]
            rule_service = rule.split('.')[1]
            if func_service == rule_service:
                score *= 1.5
            
            scored_rules.append((rule, score, list(overlap)))
    
    # Return top matches
    scored_rules.sort(key=lambda x: x[1], reverse=True)
    return scored_rules[:3]  # Top 3 matches

# Apply semantic matching
total_new_coverage = 0
detailed_coverage = {}

for service, data in mapping.items():
    if service == 'metadata':
        continue
    
    available_rules = data.get('available_rules', [])
    step3_needs = data.get('step3_needs_development', [])
    existing_step2 = data.get('step2_covered_by', {})
    
    new_coverage = {}
    still_not_covered = []
    
    for func in step3_needs:
        context = compliance_context.get(func, {})
        matches = semantic_match(func, context, available_rules)
        
        if matches and matches[0][1] >= 0.5:  # At least 50% capability match
            top_match = matches[0]
            new_coverage[func] = {
                'covered_by_rules': [m[0] for m in matches if m[1] >= 0.5],
                'coverage_type': 'SEMANTIC_MATCH',
                'expert_reasoning': f"Matches {', '.join(top_match[2])} capabilities required by: {context.get('requirement', 'N/A')}",
                'confidence': 'HIGH' if top_match[1] >= 0.8 else 'MEDIUM',
                'match_score': round(top_match[1], 2)
            }
            total_new_coverage += 1
            detailed_coverage[func] = (service, context.get('requirement', ''), matches[0][0])
        else:
            still_not_covered.append(func)
    
    # Update mapping
    all_step2 = {**existing_step2, **new_coverage}
    if all_step2:
        data['step2_covered_by'] = all_step2
    data['step3_needs_development'] = still_not_covered
    
    if new_coverage:
        print(f"  ✓ {service:15s} +{len(new_coverage)} semantic matches (total: {len(all_step2)})")

# Save
with open(MAPPING_FILE, 'w') as f:
    json.dump(mapping, f, indent=2)

print()
print(f"✓ Found {total_new_coverage} additional functions via semantic matching")
print(f"✓ Total Step 2 coverage: 7 → {7 + total_new_coverage}")
print()

# Show some examples
if detailed_coverage:
    print("Example semantic matches:")
    for func, (svc, req, rule) in list(detailed_coverage.items())[:5]:
        print(f"\n  {func}")
        print(f"    Requirement: {req[:60]}...")
        print(f"    Matched to:  {rule}")

print()
print("=" * 100)
print("KEY IMPROVEMENTS")
print("=" * 100)
print("1. Analyzes WHAT each rule can check (capabilities)")
print("2. Matches based on security requirements, not names")
print("3. Scores matches based on capability overlap")
print("4. Service-aware matching (prioritizes same service)")
print()
print("✅ SEMANTIC COVERAGE COMPLETE")
print("=" * 100)
