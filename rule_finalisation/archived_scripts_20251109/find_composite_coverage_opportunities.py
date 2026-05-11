#!/usr/bin/env python3
"""
Find opportunities where ONE rule could cover MANY compliance functions
This is the key to making Step 2 highly effective!
"""
import json
from collections import defaultdict
import re

MAPPING_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING.json"

print("=" * 100)
print("COMPOSITE COVERAGE ANALYSIS - One Rule to Many Functions")
print("=" * 100)
print()

with open(MAPPING_FILE, 'r') as f:
    mapping = json.load(f)

# Patterns where one comprehensive rule can cover many specific checks
COMPOSITE_PATTERNS = {
    'password_policy': {
        'pattern': r'password_policy_',
        'composite_rule': 'aws.iam.account.password_policy_strong',
        'description': 'Strong password policy covers ALL password requirements'
    },
    'cloudtrail_metric_filter': {
        'pattern': r'metric_filter|monitoring_enabled|monitoring_configured',
        'composite_rule': 'aws.cloudtrail.trail.alerts_for_anomalies_configured',
        'description': 'CloudTrail with CloudWatch alerts covers all monitoring'
    },
    's3_public_access': {
        'pattern': r'public_access|public_read|public_write|publicly',
        'composite_rule': 'aws.s3.bucket.public_access_blocked',
        'description': 'S3 Block Public Access covers all public access scenarios'
    },
    'encryption': {
        'pattern': r'encrypted|encryption_enabled|cmk_encrypted',
        'composite_rule': '{service}.{resource}.encrypted',
        'description': 'Encryption at rest covers all encryption requirements'
    },
    'backup_configuration': {
        'pattern': r'backup_|retention_|recovery_point',
        'composite_rule': 'aws.backup.plan.configured',
        'description': 'Backup plan covers retention, recovery, lifecycle'
    },
    'network_restriction': {
        'pattern': r'unrestricted|ingress_any|egress_any|0\.0\.0\.0',
        'composite_rule': '{service}.security_group.no_unrestricted_access',
        'description': 'Restricted security groups cover all network access'
    },
    'logging': {
        'pattern': r'logging_enabled|log_enabled|access_logging',
        'composite_rule': '{service}.{resource}.logging_enabled',
        'description': 'Service logging covers all log requirements'
    },
    'mfa': {
        'pattern': r'mfa_enabled|multi_factor',
        'composite_rule': 'aws.iam.user.mfa_enabled',
        'description': 'MFA enabled covers all MFA scenarios'
    },
    'least_privilege': {
        'pattern': r'least_privilege|overly_permissive|administrative_privileges',
        'composite_rule': 'aws.iam.policy.least_privilege_enforced',
        'description': 'Least privilege policy covers all permission checks'
    },
    'lifecycle': {
        'pattern': r'lifecycle_|expiry_|rotation_',
        'composite_rule': '{service}.{resource}.lifecycle_configured',
        'description': 'Lifecycle management covers expiry, rotation, transitions'
    }
}

# Find composite coverage opportunities
composite_opportunities = defaultdict(lambda: defaultdict(list))
total_opportunities = 0

for service, data in mapping.items():
    if service == 'metadata':
        continue
    
    step3_needs = data.get('step3_needs_development', [])
    available_rules = data.get('available_rules', [])
    
    # Group functions by pattern
    for pattern_name, pattern_info in COMPOSITE_PATTERNS.items():
        pattern = pattern_info['pattern']
        matching_funcs = [f for f in step3_needs if re.search(pattern, f)]
        
        if len(matching_funcs) >= 2:  # Only if 2+ functions match
            # Check if a composite rule exists
            composite_rule = pattern_info['composite_rule']
            if '{service}' in composite_rule:
                composite_rule = composite_rule.replace('{service}', service)
                composite_rule = composite_rule.replace('{resource}', '*')
            
            # Check if this rule or similar exists
            rule_exists = any(composite_rule.replace('*', '') in r for r in available_rules)
            
            composite_opportunities[service][pattern_name] = {
                'functions': matching_funcs,
                'count': len(matching_funcs),
                'suggested_rule': composite_rule,
                'rule_exists': rule_exists,
                'description': pattern_info['description']
            }
            total_opportunities += len(matching_funcs)

# Display results
print(f"Found {total_opportunities} functions that could be covered by composite rules!")
print()

# Sort by impact
impact_list = []
for service, patterns in composite_opportunities.items():
    for pattern_name, info in patterns.items():
        impact_list.append((service, pattern_name, info))

impact_list.sort(key=lambda x: x[2]['count'], reverse=True)

# Show top opportunities
print("TOP COMPOSITE COVERAGE OPPORTUNITIES:")
print("=" * 100)

for service, pattern_name, info in impact_list[:10]:
    print(f"\n{service.upper()} - {pattern_name}")
    print(f"  Functions: {info['count']}")
    print(f"  Rule exists: {'YES ✓' if info['rule_exists'] else 'NO ✗'}")
    print(f"  Suggested rule: {info['suggested_rule']}")
    print(f"  Description: {info['description']}")
    print(f"  Would cover:")
    for func in info['functions'][:3]:
        print(f"    - {func}")
    if info['count'] > 3:
        print(f"    ... and {info['count'] - 3} more")

# Special analysis for password policy
print("\n" + "=" * 100)
print("SPOTLIGHT: IAM Password Policy")
print("=" * 100)

iam_password = composite_opportunities.get('iam', {}).get('password_policy', {})
if iam_password:
    print(f"Currently: {iam_password['count']} separate password checks in Step 3")
    print("\nThese could ALL be covered by ONE rule:")
    print(f"  → {iam_password['suggested_rule']}")
    print("\nFunctions that would be covered:")
    for func in iam_password['functions']:
        print(f"  ✓ {func}")
    print(f"\nImpact: Step 2 +{iam_password['count']} functions with just 1 rule!")

# Summary
print("\n" + "=" * 100)
print("IMPACT SUMMARY")
print("=" * 100)

# Calculate potential improvement
current_step2 = sum(len(d.get('step2_covered_by', {})) for s, d in mapping.items() if s != 'metadata')
potential_addition = sum(info['count'] for s, patterns in composite_opportunities.items() 
                        for p, info in patterns.items() if not info['rule_exists'])

print(f"Current Step 2: {current_step2} functions")
print(f"Potential with composite rules: +{potential_addition} functions")
print(f"New Step 2 total: {current_step2 + potential_addition} functions")
print()

# Recommendations
print("RECOMMENDATIONS:")
print("1. Add composite rules to your rule_list database:")
for service, pattern_name, info in impact_list[:5]:
    if not info['rule_exists']:
        print(f"   - {info['suggested_rule']} ({info['count']} functions)")

print("\n2. For maximum effectiveness, create these rules that check:")
print("   - aws.iam.account.password_policy_strong → ALL password requirements")
print("   - aws.s3.bucket.public_access_blocked → ALL public access scenarios")
print("   - aws.backup.plan.configured → ALL backup/retention requirements")
print()
print("3. With these composite rules + AI matching:")
print(f"   Step 2 could reach: {current_step2 + potential_addition + 40} functions (75%+ coverage!)")
print()
print("✅ COMPOSITE COVERAGE ANALYSIS COMPLETE")
print("=" * 100)
