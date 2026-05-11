#!/usr/bin/env python3
"""
Map Critical AWS Services - Expert Manual Mapping
Analyzes top priority services and creates expert mappings
"""
import json

INPUT_FILE = "/Users/apple/Desktop/compliance_Database/rule_finalisation/service_mappings/aws_simple_mapping.json"

# Load current mapping
with open(INPUT_FILE, 'r') as f:
    aws_map = json.load(f)

# Define critical services list
CRITICAL_SERVICES = [
    'iam', 'ec2', 's3', 'cloudtrail', 'cloudwatch', 
    'guardduty', 'securityhub', 'kms', 'rds', 'vpc',
    'lambda', 'elbv2', 'elb', 'backup'
]

print("=" * 80)
print("CRITICAL AWS SERVICES FOR EXPERT MAPPING")
print("=" * 80)
print()

for service in CRITICAL_SERVICES:
    if service in aws_map:
        data = aws_map[service]
        rules_count = len(data.get('rules', []))
        comp_count = len(data.get('compliance_functions', []))
        print(f"{service:15s} {rules_count:3d} rules → {comp_count:3d} compliance")

print()
print("These are the services to map first.")
print("I'll create expert mappings for each by analyzing compliance requirements.")

