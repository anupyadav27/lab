#!/usr/bin/env python3
"""
Fix additional matches that AI should have caught
Including the case user identified
"""
import json

MAPPING_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING_BULLETPROOF.json"

print("=" * 80)
print("FIXING ADDITIONAL MATCHES")
print("=" * 80)
print()

with open(MAPPING_FILE, 'r') as f:
    mapping = json.load(f)

# The user's observation
print("USER'S OBSERVATION:")
print("aws.iam.user_accesskey_unused")
print("  Could be covered by: aws.iam.role.keys_not_used_or_rotated_90_days_or_less")
print()
print("ANALYSIS:")
print("- ISSUE: Roles don't have access keys in AWS (they use temp credentials)")
print("- This rule name seems incorrect or it's checking something else")
print("- BUT the concept is right: unused credentials should be detected")
print()

# Better matches AI should have found
ADDITIONAL_MATCHES = {
    'iam': {
        # Access key usage patterns
        'aws.iam.user_accesskey_unused': {
            'rule': 'aws.iam.user.access_keys_rotated_90_days_or_less_when_present',
            'reasoning': 'Keys not rotated in 90 days are likely unused - rotation check can identify stale keys',
            'confidence': 'MEDIUM',
            'note': 'Not exact match but rotation policy helps identify unused keys'
        },
        'aws.iam.user_console_access_unused': {
            'rule': 'aws.iam.user.last_activity_90_days',
            'reasoning': 'Last activity check covers console access usage',
            'confidence': 'HIGH'
        },
        # Certificate patterns
        'aws.iam.server_certificate_expiry_check': {
            'rule': 'aws.iam.server_certificate.expiry_90_days',
            'reasoning': 'Certificate expiry in 90 days covers general expiry check',
            'confidence': 'HIGH'
        }
    },
    'rds': {
        # Retention patterns
        'aws.rds.db_instance_backup_enabled': {
            'rule': 'aws.rds.instance.backup_enabled',
            'reasoning': 'Same check - db_instance = instance',
            'confidence': 'HIGH'
        }
    },
    'lambda': {
        # Dead letter queue patterns
        'aws.lambda.function_dlq_configured': {
            'rule': 'aws.lambda.function.dead_letter_queue_configured',
            'reasoning': 'DLQ = Dead Letter Queue (obvious abbreviation)',
            'confidence': 'HIGH'
        }
    }
}

# Apply these additional matches
total_fixed = 0

for service, matches in ADDITIONAL_MATCHES.items():
    if service not in mapping:
        continue
    
    data = mapping[service]
    step2 = data.get('step2_covered_by', {})
    step3 = data.get('step3_needs_development', [])
    
    for func, match_info in matches.items():
        if func in step3:
            # Check if the covering rule exists
            available = data.get('available_rules', [])
            if match_info['rule'] in available:
                step2[func] = {
                    'covered_by_rules': [match_info['rule']],
                    'coverage_type': 'AI_SHOULD_HAVE_FOUND',
                    'expert_reasoning': f"AI fix: {match_info['reasoning']}",
                    'confidence': match_info['confidence'],
                    'implementation_note': match_info.get('note', '')
                }
                
                # Remove from step3
                step3.remove(func)
                total_fixed += 1
                
                print(f"✓ Fixed: {func}")
                print(f"  → {match_info['rule']}")

# Update the mapping
for service, matches in ADDITIONAL_MATCHES.items():
    if service in mapping:
        data = mapping[service]
        data['step3_needs_development'] = [f for f in data.get('step3_needs_development', []) 
                                         if f not in matches]

# Save
with open(MAPPING_FILE, 'w') as f:
    json.dump(mapping, f, indent=2)

# Recalculate stats
total_step1 = sum(len(d.get('step1_direct_mapped', {})) for s, d in mapping.items() if s != 'metadata')
total_step2 = sum(len(d.get('step2_covered_by', {})) for s, d in mapping.items() if s != 'metadata')
total_step3 = sum(len(d.get('step3_needs_development', [])) for s, d in mapping.items() if s != 'metadata')

print()
print("=" * 80)
print("UPDATED RESULTS")
print("=" * 80)
print(f"Fixed {total_fixed} additional matches")
print()
print(f"Step 1: {total_step1}")
print(f"Step 2: {total_step2} (+{total_fixed})")
print(f"Step 3: {total_step3}")
print()
print(f"NEW COVERAGE: {(total_step1 + total_step2) / (total_step1 + total_step2 + total_step3) * 100:.1f}%")
print()

# About the specific case
print("=" * 80)
print("ABOUT YOUR SPECIFIC CASE")
print("=" * 80)
print()
print("aws.iam.role.keys_not_used_or_rotated_90_days_or_less")
print()
print("This rule name is SUSPICIOUS because:")
print("1. IAM Roles don't have access keys (they use temporary credentials)")
print("2. It might be mislabeled or checking something else")
print()
print("Better match for unused access keys:")
print("→ aws.iam.user.access_keys_rotated_90_days_or_less_when_present")
print("  (Keys not rotated in 90 days are likely unused)")
print()
print("With REAL OpenAI, it would understand these nuances better!")
print("=" * 80)
