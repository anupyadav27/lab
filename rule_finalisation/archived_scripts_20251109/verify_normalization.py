"""
Verify No Duplicates in Normalized AWS Functions by Service
"""

import json
from pathlib import Path
from collections import Counter

INPUT_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functions_by_service_2025-11-08.json")

with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

print("=" * 80)
print("DUPLICATE VERIFICATION - NORMALIZED AWS FUNCTIONS")
print("=" * 80)
print()

# Check for duplicates within each service
duplicates_found = False
total_services = len(data)
total_functions = 0
services_checked = 0

print("Checking each service for duplicate function names...")
print()

for service in sorted(data.keys()):
    functions = list(data[service].keys())
    total_functions += len(functions)
    services_checked += 1
    
    # Check for duplicates using Counter
    function_counts = Counter(functions)
    duplicates = {func: count for func, count in function_counts.items() if count > 1}
    
    if duplicates:
        duplicates_found = True
        print(f"❌ Service: {service}")
        print(f"   Found {len(duplicates)} duplicate function names:")
        for func, count in duplicates.items():
            print(f"   - {func} appears {count} times")
        print()

if not duplicates_found:
    print("✅ NO DUPLICATES FOUND!")
    print()
    print("All functions are unique within their service categories.")
    print()

# Additional checks
print("=" * 80)
print("COMPREHENSIVE VALIDATION")
print("=" * 80)
print()

# Check 1: Verify all function names are unique across the entire dataset
all_functions = []
for service, funcs in data.items():
    for func in funcs.keys():
        all_functions.append((service, func))

print(f"1. Total Services: {total_services}")
print(f"2. Total Functions: {len(all_functions)}")
print()

# Check for any function appearing in multiple services
function_to_services = {}
for service, func in all_functions:
    if func not in function_to_services:
        function_to_services[func] = []
    function_to_services[func].append(service)

cross_service_duplicates = {func: services for func, services in function_to_services.items() if len(services) > 1}

if cross_service_duplicates:
    print("⚠️  Functions appearing in multiple services:")
    print(f"   Found {len(cross_service_duplicates)} functions in multiple services")
    print()
    for func, services in sorted(cross_service_duplicates.items()):
        print(f"   {func}")
        print(f"      Services: {', '.join(services)}")
        print()
else:
    print("✅ All functions are unique across services (no cross-service duplicates)")
    print()

# Check 2: Verify aws_ prefix consistency
print("=" * 80)
print("PREFIX CONSISTENCY CHECK")
print("=" * 80)
print()

prefix_stats = {
    'with_aws_prefix': 0,
    'without_aws_prefix': 0,
    'other_prefix': 0
}

functions_without_aws_prefix = []

for service, funcs in data.items():
    for func in funcs.keys():
        if func.startswith('aws_'):
            prefix_stats['with_aws_prefix'] += 1
        elif func.startswith(('No checks', 'check_')):
            prefix_stats['other_prefix'] += 1
        else:
            prefix_stats['without_aws_prefix'] += 1
            functions_without_aws_prefix.append((service, func))

print(f"Functions with 'aws_' prefix: {prefix_stats['with_aws_prefix']} ({prefix_stats['with_aws_prefix']/len(all_functions)*100:.1f}%)")
print(f"Functions without 'aws_' prefix: {prefix_stats['without_aws_prefix']} ({prefix_stats['without_aws_prefix']/len(all_functions)*100:.1f}%)")
print(f"Functions with other prefix: {prefix_stats['other_prefix']} ({prefix_stats['other_prefix']/len(all_functions)*100:.1f}%)")
print()

if functions_without_aws_prefix:
    print(f"Functions without 'aws_' prefix (showing first 20):")
    for service, func in functions_without_aws_prefix[:20]:
        print(f"   [{service:15}] {func}")
    if len(functions_without_aws_prefix) > 20:
        print(f"   ... and {len(functions_without_aws_prefix) - 20} more")
    print()

# Check 3: Verify service extraction consistency
print("=" * 80)
print("SERVICE EXTRACTION VALIDATION")
print("=" * 80)
print()

mismatched_services = []

for service, funcs in data.items():
    if service == 'unknown':
        continue  # Skip unknown service
    
    for func in funcs.keys():
        if not func.startswith('aws_'):
            continue
            
        # Extract service from function name
        parts = func.split('_')
        if len(parts) >= 2:
            extracted_service = parts[1]
            if extracted_service != service:
                mismatched_services.append((service, func, extracted_service))

if mismatched_services:
    print(f"⚠️  Found {len(mismatched_services)} functions with service mismatch:")
    for service, func, extracted in mismatched_services[:20]:
        print(f"   Function: {func}")
        print(f"   In service: {service}, Extracted: {extracted}")
        print()
else:
    print("✅ All functions are correctly categorized in their services")
    print()

# Final Summary
print("=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)
print()

issues = []
if duplicates_found:
    issues.append("❌ Duplicate functions found within services")
else:
    print("✅ No duplicate functions within services")

if cross_service_duplicates:
    issues.append(f"⚠️  {len(cross_service_duplicates)} functions appear in multiple services")
else:
    print("✅ No cross-service duplicates")

if prefix_stats['without_aws_prefix'] > 50:  # Threshold for concern
    issues.append(f"⚠️  {prefix_stats['without_aws_prefix']} functions without aws_ prefix")
else:
    print(f"✅ Prefix consistency acceptable ({prefix_stats['without_aws_prefix']} without aws_ prefix)")

if mismatched_services:
    issues.append(f"⚠️  {len(mismatched_services)} functions in wrong service category")
else:
    print("✅ All functions correctly categorized")

print()

if issues:
    print("ISSUES FOUND:")
    for issue in issues:
        print(f"  {issue}")
else:
    print("🎉 ALL VALIDATION CHECKS PASSED!")
    print()
    print("The normalized AWS functions data is clean and consistent.")

print()
print("=" * 80)
print()

