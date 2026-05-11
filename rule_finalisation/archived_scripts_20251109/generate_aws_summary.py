"""
Generate AWS Functions Summary
"""

import json
from pathlib import Path

INPUT_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functions_by_service_2025-11-08.json")

with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

print("=" * 80)
print("AWS FUNCTIONS BY SERVICE - DETAILED SUMMARY")
print("=" * 80)
print()

# Overall stats
total_services = len(data)
total_functions = sum(len(funcs) for funcs in data.values())
total_mappings = sum(len(ids) for service_funcs in data.values() for ids in service_funcs.values())

print(f"Total AWS Services: {total_services}")
print(f"Total AWS Functions: {total_functions}")
print(f"Total Compliance Mappings: {total_mappings}")
print()

# Services sorted by function count
print("=" * 80)
print("ALL AWS SERVICES (sorted by function count)")
print("=" * 80)
print()

service_stats = []
for service, funcs in data.items():
    func_count = len(funcs)
    mapping_count = sum(len(ids) for ids in funcs.values())
    service_stats.append((service, func_count, mapping_count))

service_stats.sort(key=lambda x: x[1], reverse=True)

for i, (service, func_count, mapping_count) in enumerate(service_stats, 1):
    print(f"{i:3}. {service:25} : {func_count:3} functions, {mapping_count:4} compliance mappings")

print()
print("=" * 80)
print("MOST REFERENCED FUNCTIONS (Top 20)")
print("=" * 80)
print()

# Find most referenced functions
all_functions = []
for service, funcs in data.items():
    for func, ids in funcs.items():
        all_functions.append((func, len(ids), service))

all_functions.sort(key=lambda x: x[1], reverse=True)

for i, (func, count, service) in enumerate(all_functions[:20], 1):
    print(f"{i:3}. [{service:15}] {func:60} : {count:3} mappings")

print()

