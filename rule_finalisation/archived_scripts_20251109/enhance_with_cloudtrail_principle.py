#!/usr/bin/env python3
"""
Enhance Expert Mapping with CloudTrail Principle
ALL audit log compliance functions map to aws.cloudtrail.trail.flow_logs_enabled
"""
import json

INPUT_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_EXPERT_MAPPING_COMPLETE.json"
OUTPUT_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/AWS_EXPERT_MAPPING_COMPLETE.json"

# Load current mapping
with open(INPUT_FILE, 'r') as f:
    expert_map = json.load(f)

print("=" * 100)
print("APPLYING CLOUDTRAIL PRINCIPLE: Audit Logs = CloudTrail Enabled")
print("=" * 100)
print()

# Keywords that indicate audit logging
AUDIT_LOG_INDICATORS = [
    'audit', 'log', 'logging', 'integration_cloudwatch_logs',
    'cloudwatch_logging', 'flow_logs', 'access_logging',
    'server_access_logging', 'restapi_logging'
]

updates_made = 0

for service_name, service_data in expert_map['services'].items():
    compliance_mappings = service_data.get('compliance_mappings', {})
    
    for comp_func, mapping_data in compliance_mappings.items():
        # Check if this is an audit log function
        is_audit_log = any(indicator in comp_func.lower() for indicator in AUDIT_LOG_INDICATORS)
        
        # Special handling for different cases
        if is_audit_log:
            # If currently unmapped or low confidence
            if not mapping_data.get('mapped_rules') or mapping_data.get('confidence') in ['n/a', 'low']:
                # Map to CloudTrail flow_logs_enabled
                mapping_data['mapped_rules'] = ['aws.cloudtrail.trail.flow_logs_enabled']
                mapping_data['mapping_type'] = 'cloudtrail_principle'
                mapping_data['confidence'] = 'high'
                
                # Update notes
                service_upper = service_name.upper()
                original_notes = mapping_data.get('notes', '')
                mapping_data['notes'] = f"{service_upper} audit logs captured by CloudTrail when enabled. {original_notes}"
                
                updates_made += 1

print(f"✓ Applied CloudTrail principle to {updates_made} compliance functions")
print()

# Update summary metadata
expert_map['metadata']['cloudtrail_principle_applied'] = True
expert_map['metadata']['audit_functions_mapped_to_cloudtrail'] = updates_made

# Recalculate summaries
for service_name, service_data in expert_map['services'].items():
    compliance_mappings = service_data.get('compliance_mappings', {})
    mapped = len([f for f in compliance_mappings.values() if f.get('mapped_rules')])
    needs_dev = len([f for f in compliance_mappings.values() if not f.get('mapped_rules')])
    
    service_data['summary']['mapped'] = mapped
    service_data['summary']['needs_development'] = needs_dev

# Save
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(expert_map, f, indent=2)

print(f"✓ Saved: {OUTPUT_FILE}")
print()

# Show updated statistics
total_mapped = sum(s['summary']['mapped'] for s in expert_map['services'].values())
total_compliance = sum(s['summary']['total_compliance'] for s in expert_map['services'].values())

print("=" * 100)
print("UPDATED MAPPING STATISTICS")
print("=" * 100)
print()
print(f"Total compliance functions:  {total_compliance}")
print(f"Mapped to existing rules:    {total_mapped} ({total_mapped/total_compliance*100:.1f}%)")
print(f"Need development:            {total_compliance - total_mapped}")
print()

# Show services with best coverage
print("Services with best mapping coverage:")
for service_name, service_data in sorted(expert_map['services'].items(), 
                                          key=lambda x: x[1]['summary']['mapped']/max(x[1]['summary']['total_compliance'],1), 
                                          reverse=True)[:10]:
    summary = service_data['summary']
    coverage = summary['mapped'] / summary['total_compliance'] * 100 if summary['total_compliance'] > 0 else 0
    print(f"  {service_name:15s} {summary['mapped']:3d}/{summary['total_compliance']:3d} ({coverage:5.1f}%)")

print()
print("=" * 100)
print("✅ CLOUDTRAIL PRINCIPLE APPLIED")
print("=" * 100)

