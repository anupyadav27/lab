#!/usr/bin/env python3
"""
AWS Expert Analysis - Find which unmapped functions can be COVERED BY existing rules
Step 2: Indirect coverage analysis
"""
import json

INPUT_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING.json"
OUTPUT_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_ONE_TO_ONE_MAPPING.json"

# Load current mapping
with open(INPUT_FILE, 'r') as f:
    mapping = json.load(f)

print("=" * 100)
print("AWS EXPERT ANALYSIS - Step 2: Coverage Analysis")
print("=" * 100)
print()

# Rename "mapped" to "step1_direct_mapped"
for service, data in mapping.items():
    if service == 'metadata':
        continue
    if 'mapped' in data:
        data['step1_direct_mapped'] = data.pop('mapped')

print("✓ Renamed 'mapped' to 'step1_direct_mapped'")
print()

# Now analyze unmapped with AWS expertise
print("Analyzing unmapped functions for indirect coverage...")
print()

# AWS Expert knowledge for coverage analysis
COVERAGE_PATTERNS = {
    # GuardDuty
    'aws.guardduty.no_high_severity_findings': {
        'can_be_covered_by': [],
        'reasoning': 'Requires GetFindings API call - cannot be covered by config checks',
        'coverage_type': 'CANNOT_COVER'
    },
    'aws.guardduty.centrally_managed': {
        'can_be_covered_by': [],
        'reasoning': 'Requires Organizations API - cannot be covered by GuardDuty config checks',
        'coverage_type': 'CANNOT_COVER'
    },
    'aws.guardduty.vulnerability_assessment_enabled': {
        'can_be_covered_by': ['aws.inspector.assessment.agents_or_scanners_deployed'],
        'reasoning': 'Vulnerability assessment is Inspector function, not GuardDuty',
        'coverage_type': 'DIFFERENT_SERVICE'
    },
    
    # CloudTrail metric filters - check if CloudTrail flow_logs + alerts cover them
    'aws.cloudtrail.vpc_changes_monitoring_enabled': {
        'can_be_covered_by': ['aws.cloudtrail.trail.flow_logs_enabled', 'aws.cloudtrail.trail.alerts_for_anomalies_configured'],
        'reasoning': 'VPC changes logged by CloudTrail + alerts_for_anomalies can detect VPC changes',
        'coverage_type': 'COMPOSITE'
    },
    'aws.cloudtrail.unauthorized_api_calls_monitoring_configured': {
        'can_be_covered_by': ['aws.cloudtrail.trail.alerts_for_anomalies_configured'],
        'reasoning': 'alerts_for_anomalies includes unauthorized API call detection',
        'coverage_type': 'COVERED'
    },
    
    # IAM - many cannot be covered but some can
    'aws.iam.user_credentials_unused_90_days': {
        'can_be_covered_by': ['aws.iam.user.last_activity_90_days'],
        'reasoning': 'Credential report last activity check can cover this',
        'coverage_type': 'SIMILAR_CHECK'
    },
    
    # S3
    'aws.s3.bucket_lifecycle_configuration_enabled': {
        'can_be_covered_by': [],
        'reasoning': 'Specific S3 lifecycle policy check - no equivalent in rule_list',
        'coverage_type': 'CANNOT_COVER'
    },
    'aws.s3.bucket_mfa_delete_enabled': {
        'can_be_covered_by': [],
        'reasoning': 'S3 versioning MFA delete - specific attribute check needed',
        'coverage_type': 'CANNOT_COVER'
    },
    
    # EC2 - many specific configs
    'aws.ec2.instance_managed_by_ssm': {
        'can_be_covered_by': [],
        'reasoning': 'Requires checking SSM managed instances - different service check',
        'coverage_type': 'DIFFERENT_SERVICE'
    },
    'aws.ec2.networkacl_allow_ingress_any_port': {
        'can_be_covered_by': ['aws.ec2.network_acl.no_unrestricted_ingress'],
        'reasoning': 'Network ACL unrestricted ingress check can cover this',
        'coverage_type': 'SIMILAR_CHECK'
    },
    
    # RDS
    'aws.rds.instance_enhanced_monitoring_enabled': {
        'can_be_covered_by': [],
        'reasoning': 'Enhanced monitoring is specific RDS feature - requires MonitoringInterval check',
        'coverage_type': 'CANNOT_COVER'
    },
    'aws.rds.snapshots_public_access': {
        'can_be_covered_by': ['aws.rds.snapshot.not_public'],
        'reasoning': 'If snapshot.not_public rule exists, it covers this',
        'coverage_type': 'LIKELY_EXISTS'
    },
    
    # VPC
    'aws.vpc.default_security_group_restricts_traffic': {
        'can_be_covered_by': ['aws.ec2.security_group.default_restricts_all_traffic'],
        'reasoning': 'Default SG restriction - if EC2 has this rule, it covers VPC requirement',
        'coverage_type': 'SIMILAR_CHECK'
    }
}

# Apply coverage analysis to each service
coverage_found = 0

for service, data in mapping.items():
    if service == 'metadata':
        continue
    
    not_mapped = data.get('not_mapped', [])
    covered_by = {}
    still_not_covered = []
    
    for func in not_mapped:
        if func in COVERAGE_PATTERNS:
            pattern = COVERAGE_PATTERNS[func]
            if pattern['can_be_covered_by']:
                covered_by[func] = {
                    'covered_by_rules': pattern['can_be_covered_by'],
                    'coverage_type': pattern['coverage_type'],
                    'expert_reasoning': pattern['reasoning']
                }
                coverage_found += 1
            else:
                still_not_covered.append(func)
        else:
            # Apply generic logic for common patterns
            available_rules = data.get('available_rules', [])
            
            # Check if similar rule exists
            func_keywords = set(func.lower().split('.'))
            potential_covers = []
            
            for rule in available_rules:
                rule_keywords = set(rule.lower().split('.'))
                common = func_keywords & rule_keywords
                if len(common) >= 3:  # At least 3 common keywords
                    potential_covers.append(rule)
            
            if potential_covers:
                covered_by[func] = {
                    'covered_by_rules': potential_covers[:2],  # Top 2
                    'coverage_type': 'POTENTIAL',
                    'expert_reasoning': 'Similar rule exists - requires expert validation'
                }
                coverage_found += 1
            else:
                still_not_covered.append(func)
    
    # Update service with step2
    if covered_by:
        data['step2_covered_by'] = covered_by
    
    # Update not_mapped to only include what truly cannot be covered
    data['step3_needs_development'] = still_not_covered
    
    # Remove old not_mapped
    if 'not_mapped' in data:
        del data['not_mapped']
    
    if covered_by:
        print(f"  ✓ {service:15s} {len(covered_by)} functions can be covered")

# Update metadata
mapping['metadata']['step1'] = 'Direct 1:1 mappings'
mapping['metadata']['step2'] = 'Coverage via existing rules (composite/similar checks)'
mapping['metadata']['step3'] = 'Truly needs new development'

# Save
with open(OUTPUT_FILE, 'w') as f:
    json.dump(mapping, f, indent=2)

print()
print(f"✓ Saved: {OUTPUT_FILE}")
print()
print(f"✓ Found {coverage_found} additional functions that can be covered")
print()
print("=" * 100)
print("UPDATED STRUCTURE")
print("=" * 100)
print()
print("Each service now has:")
print("  - available_rules: [all rules for this service]")
print("  - step1_direct_mapped: {compliance: rule_id}")
print("  - step2_covered_by: {compliance: {covered_by_rules, coverage_type, reasoning}}")
print("  - step3_needs_development: [truly needs new development]")
print()
print("=" * 100)
print("✅ COVERAGE ANALYSIS COMPLETE")
print("=" * 100)

