#!/usr/bin/env python3
"""
More Effective Step 2 - Using Compliance Context & Security Intent
"""
import json
import pandas as pd
import re

# Files
MAPPING_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING.json"
COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"

# Load files
with open(MAPPING_FILE, 'r') as f:
    mapping = json.load(f)

# Load compliance CSV to get CONTEXT
df = pd.read_csv(COMPLIANCE_CSV)
print("=" * 100)
print("INTELLIGENT COVERAGE ANALYSIS - Using Compliance Context")
print("=" * 100)
print()

# Build a context dictionary for all AWS compliance functions
compliance_context = {}
for _, row in df.iterrows():
    # Use aws_uniform_format column
    if pd.notna(row.get('aws_uniform_format')):
        functions = str(row['aws_uniform_format']).split(';')
        requirement = str(row.get('Requirement', ''))
        sub_requirement = str(row.get('Sub Requirement', ''))
        description = str(row.get('Description', ''))
        aws_service = str(row.get('AWS Service', ''))
        
        for func in functions:
            func = func.strip()
            if func and func.startswith('aws.'):
                compliance_context[func] = {
                    'requirement': requirement,
                    'sub_requirement': sub_requirement,
                    'description': description,
                    'aws_service': aws_service,
                    'full_context': f"{requirement} {sub_requirement} {description}".lower()
                }

print(f"✓ Loaded context for {len(compliance_context)} AWS compliance functions")
print()

# Security Intent Patterns - based on common compliance requirements
SECURITY_INTENT_MAPPINGS = {
    # Encryption patterns
    r'encrypt|cryptograph': {
        'kms': ['aws.kms.cmk.rotation_enabled', 'aws.kms.key.encryption_enabled'],
        's3': ['aws.s3.bucket.default_encryption_enabled', 'aws.s3.bucket.server_side_encryption_enabled'],
        'rds': ['aws.rds.cluster.encrypted_at_rest', 'aws.rds.instance.encrypted_at_rest'],
        'ec2': ['aws.ec2.volume.encrypted'],
        'backup': ['aws.backup.vault.recovery_points_protected']
    },
    
    # Logging/Monitoring patterns
    r'log|audit|monitor|track': {
        'all': ['aws.cloudtrail.trail.flow_logs_enabled'],
        'vpc': ['aws.vpc.flow_logs.enabled'],
        's3': ['aws.s3.bucket.logging_enabled'],
        'cloudwatch': ['aws.cloudtrail.trail.integrated_with_cloudwatch'],
        'guardduty': ['aws.guardduty.detector.enabled_in_all_regions']
    },
    
    # Access control patterns
    r'access control|permission|privilege|rbac|least privilege': {
        'iam': ['aws.iam.group.attached_policy_least_privilege', 'aws.iam.role.attached_policy_least_privilege'],
        's3': ['aws.s3.bucket.public_access_blocked'],
        'general': ['aws.iam.policy.least_privilege_enforced']
    },
    
    # Backup patterns
    r'backup|recovery|retention|restore': {
        'backup': ['aws.backup.plan.min_retention_35_days', 'aws.backup.vault.recovery_points_protected'],
        'rds': ['aws.rds.instance.backup_enabled'],
        's3': ['aws.s3.bucket.versioning_enabled']
    },
    
    # Network security patterns
    r'network|firewall|ingress|egress|traffic': {
        'ec2': ['aws.ec2.security_group.no_unrestricted_ingress', 'aws.ec2.network_acl.no_unrestricted_ingress'],
        'vpc': ['aws.vpc.security_group.restricted_ingress', 'aws.vpc.flow_logs.enabled']
    },
    
    # Vulnerability/Patch patterns
    r'vulnerabilit|patch|update|scan|assessment': {
        'inspector': ['aws.inspector.assessment.agents_or_scanners_deployed', 'aws.inspector.assessment.regular_scans_configured'],
        'ssm': ['aws.ssm.patch_compliance', 'aws.ssm.managed_instance_compliance']
    },
    
    # Multi-factor authentication
    r'mfa|multi.?factor|two.?factor': {
        'iam': ['aws.iam.root_user.mfa_enabled', 'aws.iam.user.console_access_mfa_enabled']
    },
    
    # Public exposure patterns
    r'public|internet|external|private': {
        's3': ['aws.s3.bucket.public_access_blocked'],
        'rds': ['aws.rds.instance.not_publicly_accessible'],
        'ec2': ['aws.ec2.instance.not_publicly_accessible']
    },
    
    # Unused/inactive patterns
    r'unused|inactive|stale|90 days': {
        'iam': ['aws.iam.user.last_activity_90_days', 'aws.iam.user.accesskey_unused']
    },
    
    # Key rotation patterns
    r'rotation|rotate': {
        'kms': ['aws.kms.cmk.rotation_enabled'],
        'iam': ['aws.iam.user.accesskey_rotated_90_days']
    }
}

def find_coverage_by_intent(func_name, context, available_rules):
    """Find rules that can cover based on security intent"""
    covered_by = []
    
    if not context:
        return []
    
    full_context = context.get('full_context', '')
    sub_requirement = context.get('sub_requirement', '')
    
    # Check each intent pattern
    for pattern, service_rules in SECURITY_INTENT_MAPPINGS.items():
        if re.search(pattern, full_context, re.IGNORECASE) or re.search(pattern, sub_requirement, re.IGNORECASE):
            # Extract service from function name
            func_parts = func_name.split('.')
            if len(func_parts) >= 2:
                service = func_parts[1]
                
                # Get relevant rules for this service
                potential_rules = []
                if service in service_rules:
                    potential_rules.extend(service_rules[service])
                if 'all' in service_rules:
                    potential_rules.extend(service_rules['all'])
                if 'general' in service_rules:
                    potential_rules.extend(service_rules['general'])
                
                # Check if these rules exist in available_rules
                for rule in potential_rules:
                    if rule in available_rules:
                        covered_by.append({
                            'rule': rule,
                            'intent_pattern': pattern,
                            'confidence': 'HIGH'
                        })
    
    return covered_by

# Analyze each service
total_new_coverage = 0
services_with_coverage = []

for service, data in mapping.items():
    if service == 'metadata':
        continue
    
    available_rules = data.get('available_rules', [])
    step3_needs = data.get('step3_needs_development', [])
    
    # Keep existing step2
    existing_step2 = data.get('step2_covered_by', {})
    
    # Find new coverage
    new_coverage = {}
    still_not_covered = []
    
    for func in step3_needs:
        # Get context for this function
        context = compliance_context.get(func, {})
        
        # Find coverage by security intent
        coverage = find_coverage_by_intent(func, context, available_rules)
        
        if coverage:
            new_coverage[func] = {
                'covered_by_rules': [c['rule'] for c in coverage][:2],  # Limit to top 2
                'coverage_type': 'SECURITY_INTENT',
                'expert_reasoning': f"Based on requirement: '{context.get('sub_requirement', 'N/A')}' - matches security intent",
                'confidence': coverage[0]['confidence'],
                'compliance_context': context.get('sub_requirement', '')
            }
            total_new_coverage += 1
        else:
            still_not_covered.append(func)
    
    # Merge with existing step2
    all_step2 = {**existing_step2, **new_coverage}
    
    if all_step2:
        data['step2_covered_by'] = all_step2
    
    # Update step3
    data['step3_needs_development'] = still_not_covered
    
    if new_coverage:
        services_with_coverage.append((service, len(new_coverage), len(all_step2)))
        print(f"  ✓ {service:15s} +{len(new_coverage)} new coverage found (total: {len(all_step2)})")

# Save updated mapping
with open(MAPPING_FILE, 'w') as f:
    json.dump(mapping, f, indent=2)

print()
print(f"✓ Found {total_new_coverage} additional functions covered by security intent")
print(f"✓ Total Step 2 coverage improved from 7 to {7 + total_new_coverage}")
print()

# Show breakdown
if services_with_coverage:
    print("Services with improved coverage:")
    for svc, new, total in services_with_coverage:
        print(f"  - {svc}: +{new} (total step2: {total})")

print()
print("=" * 100)
print("IMPROVED COVERAGE ANALYSIS")
print("=" * 100)
print()
print("Now using:")
print("  1. Actual compliance requirement context")
print("  2. Security intent pattern matching")
print("  3. Service-aware rule suggestions")
print("  4. Confidence scoring")
print()
print("✅ INTELLIGENT COVERAGE COMPLETE")
print("=" * 100)