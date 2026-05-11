#!/usr/bin/env python3
"""
Find semantic matches that AI would catch
Including inverse logic, synonyms, and technical equivalents
"""
import json
import re

MAPPING_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING.json"

print("=" * 100)
print("SEMANTIC MATCHING OPPORTUNITIES - What AI Would Find")
print("=" * 100)
print()

with open(MAPPING_FILE, 'r') as f:
    mapping = json.load(f)

# Semantic patterns AI would recognize
SEMANTIC_PATTERNS = {
    'internet_access': {
        'equivalent_terms': ['0.0.0.0', 'internet', 'public', 'any', 'unrestricted', 'open'],
        'inverse_pairs': [
            ('no_0_0_0_0', 'allow_ingress_from_internet'),
            ('no_unrestricted', 'unrestricted'),
            ('restricted', 'allow_any'),
            ('not_publicly_accessible', 'public_access')
        ]
    },
    'port_patterns': {
        'equivalent_terms': ['any_port', 'all_ports', '0-65535', 'unrestricted_port', '*'],
        'common_ports': {
            '22': ['ssh', 'secure_shell'],
            '3389': ['rdp', 'remote_desktop'],
            '80': ['http', 'web'],
            '443': ['https', 'ssl', 'tls']
        }
    },
    'security_patterns': {
        'equivalent_terms': ['security_group', 'sg', 'firewall', 'nacl', 'network_acl'],
        'actions': ['allow', 'deny', 'permit', 'block', 'restrict']
    },
    'encryption_patterns': {
        'equivalent_terms': ['encrypted', 'encryption_enabled', 'cmk_encrypted', 'kms_encrypted'],
        'related': ['tls', 'ssl', 'https', 'secure_transport']
    }
}

# Find semantic matches
semantic_opportunities = []
inverse_matches = []

for service, data in mapping.items():
    if service == 'metadata':
        continue
    
    available_rules = data.get('available_rules', [])
    step3_needs = data.get('step3_needs_development', [])
    
    # Check each unmapped function
    for func in step3_needs:
        func_lower = func.lower()
        
        # Check available rules for semantic matches
        for rule in available_rules:
            rule_lower = rule.lower()
            
            # Check for 0.0.0.0/internet pattern
            if ('0_0_0_0' in rule_lower or 'unrestricted' in rule_lower) and \
               ('internet' in func_lower or 'any_port' in func_lower or 'ingress' in func_lower):
                
                # Check if it's inverse logic
                if ('no_' in rule_lower and 'allow' in func_lower) or \
                   ('restrict' in rule_lower and 'unrestricted' in func_lower):
                    inverse_matches.append({
                        'compliance_func': func,
                        'available_rule': rule,
                        'match_type': 'INVERSE_LOGIC',
                        'explanation': 'Rule checks the opposite - if rule passes, compliance fails'
                    })
                else:
                    semantic_opportunities.append({
                        'compliance_func': func,
                        'available_rule': rule,
                        'match_type': 'SEMANTIC_EQUIVALENT',
                        'explanation': '0.0.0.0 = internet access, same security check'
                    })
            
            # Check for port equivalents
            elif 'any_port' in func_lower and ('0_0_0_0' in rule_lower or 'unrestricted' in rule_lower):
                semantic_opportunities.append({
                    'compliance_func': func,
                    'available_rule': rule,
                    'match_type': 'SEMANTIC_EQUIVALENT',
                    'explanation': 'Unrestricted access implies any port'
                })
            
            # Check for encryption patterns
            elif 'encrypt' in func_lower and 'encrypt' in rule_lower:
                if service in rule_lower:  # Same service
                    semantic_opportunities.append({
                        'compliance_func': func,
                        'available_rule': rule,
                        'match_type': 'ENCRYPTION_CHECK',
                        'explanation': 'Same encryption requirement, different naming'
                    })
            
            # Check for public/private patterns
            elif ('public' in func_lower and 'public' in rule_lower) or \
                 ('private' in func_lower and 'private' in rule_lower):
                semantic_opportunities.append({
                    'compliance_func': func,
                    'available_rule': rule,
                    'match_type': 'ACCESS_CONTROL',
                    'explanation': 'Same public/private access check'
                })

# Display findings
print(f"Found {len(semantic_opportunities)} semantic matches AI would recognize!")
print(f"Found {len(inverse_matches)} inverse logic matches!")
print()

# Show the EC2 example the user mentioned
print("YOUR EXAMPLE:")
print("-" * 80)
ec2_matches = [m for m in semantic_opportunities + inverse_matches 
               if 'ec2.securitygroup_allow_ingress_from_internet' in m['compliance_func']]
for match in ec2_matches:
    print(f"Compliance: {match['compliance_func']}")
    print(f"Available:  {match['available_rule']}")
    print(f"Type:       {match['match_type']}")
    print(f"AI would recognize: {match['explanation']}")
    print()

# Show more examples
if semantic_opportunities:
    print("\nMORE SEMANTIC MATCHES AI WOULD FIND:")
    print("=" * 80)
    
    # Group by match type
    by_type = {}
    for match in semantic_opportunities[:10]:
        match_type = match['match_type']
        if match_type not in by_type:
            by_type[match_type] = []
        by_type[match_type].append(match)
    
    for match_type, matches in by_type.items():
        print(f"\n{match_type}:")
        for match in matches[:3]:
            print(f"  {match['compliance_func'][:50]:50s} → {match['available_rule'][:40]}")

# Show inverse matches
if inverse_matches:
    print("\n\nINVERSE LOGIC MATCHES (Need Special Handling):")
    print("=" * 80)
    for match in inverse_matches[:5]:
        print(f"\n{match['compliance_func']}")
        print(f"  ↔ {match['available_rule']}")
        print(f"  ⚠️  {match['explanation']}")

# Summary
print("\n" + "=" * 100)
print("AI SEMANTIC MATCHING CAPABILITIES")
print("=" * 100)
print()
print("AI would recognize these patterns:")
print("1. Technical equivalents: 0.0.0.0 = internet access")
print("2. Inverse logic: no_unrestricted vs allow_unrestricted")
print("3. Implied relationships: unrestricted = any port")
print("4. Abbreviations: sg = security_group")
print("5. Similar concepts: public_access_blocked ≈ not_publicly_accessible")
print()
print(f"Total opportunities found: {len(semantic_opportunities) + len(inverse_matches)}")
print()
print("With AI, your Step 2 would catch ALL of these automatically!")
print("=" * 100)
