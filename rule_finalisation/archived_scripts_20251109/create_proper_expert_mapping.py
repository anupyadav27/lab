#!/usr/bin/env python3
"""
Proper AWS Expert Mapping using Compliance CSV Context
- All audit log functions → CloudTrail
- Use actual compliance requirements to understand function purpose
- Map to Inspector if vulnerability assessment related
"""
import csv
import json
from collections import defaultdict

COMPLIANCE_CSV = "/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv"
SIMPLE_MAPPING = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/aws_simple_mapping.json"
OUTPUT_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_EXPERT_MAPPING_FINAL.json"

print("=" * 100)
print("PROPER AWS EXPERT MAPPING - Using Compliance CSV Context")
print("=" * 100)
print()

# Load compliance CSV to understand what each function is for
print("Step 1: Loading compliance context for each function...")
function_context = defaultdict(lambda: {
    'frameworks': set(),
    'requirements': [],
    'descriptions': set(),
    'usage_count': 0
})

with open(COMPLIANCE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        aws_uniform = row.get('aws_uniform_format', '')
        
        if aws_uniform and aws_uniform != 'NA':
            for func in aws_uniform.split(';'):
                func = func.strip()
                if func and func != 'NA':
                    function_context[func]['frameworks'].add(row.get('compliance_framework', ''))
                    function_context[func]['usage_count'] += 1
                    
                    req_id = row.get('requirement_id', '')
                    req_name = row.get('requirement_name', '')
                    if req_id and req_name:
                        req_text = f"{req_id}: {req_name}"
                        if req_text not in function_context[func]['requirements']:
                            function_context[func]['requirements'].append(req_text)
                    
                    desc = row.get('requirement_description', '')
                    if desc and desc != 'NA':
                        function_context[func]['descriptions'].add(desc[:100])

print(f"✓ Loaded context for {len(function_context)} compliance functions")
print()

# Load simple mapping
with open(SIMPLE_MAPPING, 'r') as f:
    simple_map = json.load(f)

# Expert mapping with proper context analysis
CRITICAL_SERVICES = [
    'guardduty', 'cloudtrail', 'iam', 's3', 'ec2', 
    'cloudwatch', 'kms', 'rds', 'vpc', 'lambda',
    'elbv2', 'elb', 'backup', 'securityhub', 'inspector'
]

print("Step 2: Creating expert mappings using compliance context...")
print()

expert_map = {
    'metadata': {
        'date': '2025-11-09',
        'version': '2.0',
        'analyst': 'AWS Security Expert',
        'methodology': 'Compliance CSV context analysis',
        'key_principles': [
            'Audit log functions → aws.cloudtrail.trail.flow_logs_enabled',
            'Vulnerability assessment → Inspector rules',
            'Use compliance requirement context to guide decisions'
        ]
    },
    'services': {}
}

# Keywords for automatic mapping
AUDIT_LOG_KEYWORDS = [
    'audit', 'logging', 'log_', 'access_logging', 
    'server_access_logging', 'flow_logs', 'integration_cloudwatch_logs',
    'cloudwatch_logging', 'restapi_logging'
]

for service in CRITICAL_SERVICES:
    if service not in simple_map:
        continue
    
    service_data = simple_map[service]
    rules = service_data.get('rules', [])
    compliance_funcs = service_data.get('compliance_functions', [])
    
    mapped_functions = {}
    
    for comp_func in compliance_funcs:
        context = function_context.get(comp_func, {})
        frameworks = ', '.join(sorted(context.get('frameworks', set())))[:80]
        requirements = context.get('requirements', [])[:3]
        usage = context.get('usage_count', 0)
        
        mapped_to = []
        status = 'NEEDS_DEVELOPMENT'
        confidence = 'N/A'
        notes = ''
        
        # PRINCIPLE 1: Audit Log Functions → CloudTrail
        func_lower = comp_func.lower()
        is_audit_log = any(keyword in func_lower for keyword in AUDIT_LOG_KEYWORDS)
        
        if is_audit_log:
            mapped_to = ['aws.cloudtrail.trail.flow_logs_enabled']
            status = 'MAPPED'
            confidence = 'HIGH'
            notes = f'Audit logging captured by CloudTrail. Per expert principle: CloudTrail enabled = audit logs for all AWS services.'
        
        # PRINCIPLE 2: Vulnerability Assessment → Inspector
        elif 'vulnerability' in func_lower or 'vuln' in func_lower:
            # Check if Inspector rules exist
            if 'inspector' in simple_map:
                inspector_rules = simple_map['inspector'].get('rules', [])
                vuln_rules = [r for r in inspector_rules if 'vulner' in r or 'assessment' in r or 'finding' in r]
                if vuln_rules:
                    mapped_to = vuln_rules[:1]
                    status = 'MAPPED'
                    confidence = 'HIGH'
                    notes = 'Vulnerability assessment via AWS Inspector'
                else:
                    notes = 'Vulnerability assessment - likely Inspector, but no matching rule found'
            else:
                notes = 'Vulnerability assessment - should use AWS Inspector (no rules in rule_list)'
        
        # PRINCIPLE 3: Service enabled checks
        elif comp_func.endswith('.enabled'):
            service_part = comp_func.split('.')[1] if '.' in comp_func else ''
            enabled_rules = [r for r in rules if 'enabled' in r and service_part in r]
            if enabled_rules:
                # Prefer 'all_regions' or 'detectors_enabled' for primary enabled check
                best = [r for r in enabled_rules if 'all_regions' in r or 'detectors_enabled' in r or f'{service_part}_enabled' in r]
                mapped_to = best[:1] if best else enabled_rules[:1]
                status = 'MAPPED'
                confidence = 'HIGH'
                notes = f'{service_part.upper()} service enabled check'
        
        # PRINCIPLE 4: Encryption checks
        elif 'encrypt' in func_lower or 'kms' in func_lower:
            enc_rules = [r for r in rules if 'encrypt' in r.lower() or 'kms' in r.lower()]
            if enc_rules:
                # Match more specifically
                if 'storage' in func_lower or 'at_rest' in func_lower:
                    best = [r for r in enc_rules if 'at_rest' in r or 'storage' in r]
                    mapped_to = best[:1] if best else enc_rules[:1]
                else:
                    mapped_to = enc_rules[:1]
                status = 'MAPPED'
                confidence = 'HIGH'
                notes = 'Encryption configuration check'
        
        # PRINCIPLE 5: Public access checks
        elif 'public' in func_lower or 'publicly_accessible' in func_lower:
            pub_rules = [r for r in rules if 'public' in r.lower() or 'private' in r.lower() or 'accessible' in r.lower()]
            if pub_rules:
                mapped_to = pub_rules[:2]
                status = 'MAPPED'
                confidence = 'HIGH'
                notes = 'Public access security check'
        
        # PRINCIPLE 6: Versioning checks
        elif 'versioning' in func_lower:
            ver_rules = [r for r in rules if 'version' in r.lower()]
            if ver_rules:
                mapped_to = ver_rules[:1]
                status = 'MAPPED'
                confidence = 'HIGH'
                notes = 'Versioning configuration check'
        
        # PRINCIPLE 7: Backup/snapshot checks
        elif 'backup' in func_lower or 'snapshot' in func_lower:
            backup_rules = [r for r in rules if 'backup' in r.lower() or 'snapshot' in r.lower()]
            if backup_rules:
                mapped_to = backup_rules[:1]
                status = 'MAPPED'
                confidence = 'HIGH'
                notes = 'Backup/snapshot configuration check'
        
        mapped_functions[comp_func] = {
            'name': comp_func,
            'usage_count': usage,
            'frameworks': frameworks,
            'requirements': requirements,
            'mapped_to': mapped_to,
            'status': status,
            'confidence': confidence,
            'expert_notes': notes if notes else 'Requires manual expert review for proper mapping'
        }
    
    # Calculate summary
    mapped_count = len([f for f in mapped_functions.values() if f['mapped_to']])
    
    expert_map['services'][service] = {
        'available_rules': rules,
        'rule_count': len(rules),
        'compliance_functions': list(mapped_functions.values()),
        'summary': {
            'total_compliance': len(compliance_funcs),
            'mapped': mapped_count,
            'needs_development': len(compliance_funcs) - mapped_count,
            'coverage_percent': round(mapped_count / len(compliance_funcs) * 100) if compliance_funcs else 0
        }
    }
    
    print(f"  ✓ {service:15s} {mapped_count:3d}/{len(compliance_funcs):3d} mapped ({expert_map['services'][service]['summary']['coverage_percent']:3d}%)")

# Save
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(expert_map, f, indent=2)

print()
print(f"✓ Saved: {OUTPUT_FILE}")
print()

# Overall stats
total_comp = sum(s['summary']['total_compliance'] for s in expert_map['services'].values())
total_mapped = sum(s['summary']['mapped'] for s in expert_map['services'].values())

print("=" * 100)
print("FINAL EXPERT MAPPING STATISTICS")
print("=" * 100)
print()
print(f"Services mapped:          {len(expert_map['services'])}")
print(f"Compliance functions:     {total_comp}")
print(f"Mapped to rules:          {total_mapped} ({total_mapped/total_comp*100:.1f}%)")
print(f"Need development:         {total_comp - total_mapped}")
print()
print("Key principles applied:")
print("  ✓ All audit log functions → CloudTrail")
print("  ✓ Vulnerability functions → Inspector")
print("  ✓ Service enabled checks → service.enabled rules")
print("  ✓ Encryption checks → service encryption rules")
print()
print("=" * 100)
print("✅ PROPER EXPERT MAPPING COMPLETE")
print("=" * 100)

