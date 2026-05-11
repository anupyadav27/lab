"""
Create Final Consolidated AWS Functions List
Based on functional overlap analysis - keep only distinct functions by JOB
"""

import csv
import json
from pathlib import Path

INPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_2025-11-08_fixed.csv")
ANALYSIS_JSON = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functional_overlap_analysis.json")
OUTPUT_CSV = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/consolidated_compliance_rules_FINAL.csv")
FINAL_FUNCTIONS_JSON = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/aws_functions_final_deduplicated.json")
CONSOLIDATION_REPORT = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule/AWS_FUNCTIONS_CONSOLIDATION_REPORT.md")

print("=" * 80)
print("CREATING FINAL CONSOLIDATED AWS FUNCTIONS LIST")
print("=" * 80)
print()

# Load functional analysis
with open(ANALYSIS_JSON, 'r') as f:
    analysis = json.load(f)

# Build consolidation map based on expert analysis
# Keep the RECOMMENDED function, remove others
consolidation_map = {}

# Extract functions to remove from each group
for group_name, group_data in analysis.items():
    functions = group_data.get('functions_found', [])
    recommendation = group_data.get('recommendation', '')
    
    if len(functions) > 1:
        # Parse recommendation to find which functions to keep
        keep_functions = []
        
        # Extract function names from recommendation
        if 'Keep:' in recommendation:
            keep_part = recommendation.split('Keep:')[1].split(',')
            for part in keep_part:
                # Extract function names from text
                words = part.strip().split()
                for word in words:
                    if word.startswith('aws_'):
                        keep_functions.append(word.rstrip('.,();'))
        
        # If we identified functions to keep, map others to them
        if keep_functions:
            # Use first keep function as primary
            primary = keep_functions[0]
            
            for func in functions:
                if func not in keep_functions:
                    consolidation_map[func] = primary
                    print(f"   {func}")
                    print(f"   → {primary}")
                    print()

print(f"Total function consolidations identified: {len(consolidation_map)}")
print()

# Read and update CSV
print("Processing CSV...")
updated_rows = []
stats = {
    'total_rows': 0,
    'rows_updated': 0,
    'functions_consolidated': 0
}

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        stats['total_rows'] += 1
        row_changed = False
        
        for col in ['aws_checks', 'azure_checks', 'gcp_checks', 'oracle_checks',
                    'ibm_checks', 'alicloud_checks', 'k8s_checks']:
            if row.get(col) and row[col] != 'NA':
                checks = row[col].split(';')
                new_checks = []
                
                for check in checks:
                    check = check.strip()
                    if check in consolidation_map:
                        new_checks.append(consolidation_map[check])
                        stats['functions_consolidated'] += 1
                        row_changed = True
                    else:
                        new_checks.append(check)
                
                # Remove duplicates and sort
                unique_checks = sorted(list(set(new_checks)))
                row[col] = '; '.join(unique_checks)
        
        if row_changed:
            stats['rows_updated'] += 1
        
        updated_rows.append(row)

# Write updated CSV
with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"✅ Final CSV: {OUTPUT_CSV.name}")
print(f"   Rows processed: {stats['total_rows']}")
print(f"   Rows updated: {stats['rows_updated']}")
print(f"   Functions consolidated: {stats['functions_consolidated']}")
print()

# Generate final deduplicated functions list by service
from collections import defaultdict

aws_functions_by_service = defaultdict(set)

with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        aws_checks = row.get('aws_checks', '')
        if aws_checks and aws_checks != 'NA':
            functions = [f.strip() for f in aws_checks.split(';') if f.strip()]
            for func in functions:
                # Extract service
                if func.startswith('aws_'):
                    parts = func[4:].split('_')
                    if parts:
                        service = parts[0]
                        aws_functions_by_service[service].add(func)

# Convert to sorted dict
final_functions = {
    service: sorted(list(funcs))
    for service, funcs in sorted(aws_functions_by_service.items())
}

with open(FINAL_FUNCTIONS_JSON, 'w', encoding='utf-8') as f:
    json.dump(final_functions, f, indent=2)

print(f"✅ Final Functions JSON: {FINAL_FUNCTIONS_JSON.name}")
print(f"   Services: {len(final_functions)}")
print(f"   Total functions: {sum(len(funcs) for funcs in final_functions.values())}")
print()

# Generate consolidation report
report_lines = []
report_lines.append("# AWS Functions Consolidation Report")
report_lines.append("**Date:** November 8, 2025")
report_lines.append("**Analysis Type:** Functional Overlap - Keep Only Distinct Functions by Job")
report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("## Executive Summary")
report_lines.append("")
report_lines.append(f"- **Total compliance controls:** {stats['total_rows']}")
report_lines.append(f"- **Controls updated:** {stats['rows_updated']}")
report_lines.append(f"- **Function consolidations:** {len(consolidation_map)}")
report_lines.append(f"- **Final unique functions:** {sum(len(funcs) for funcs in final_functions.values())}")
report_lines.append(f"- **Services covered:** {len(final_functions)}")
report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("## Consolidation Decisions")
report_lines.append("")
report_lines.append("### Rationale")
report_lines.append("Functions were consolidated based on:")
report_lines.append("1. **Functional Equivalence** - Multiple functions checking the same AWS configuration")
report_lines.append("2. **AWS Expert Analysis** - Understanding of actual AWS service behavior")
report_lines.append("3. **Compliance Overlap** - Analysis of which compliance controls use which functions")
report_lines.append("")
report_lines.append("### Key Consolidations")
report_lines.append("")

# Group consolidations by service
consolidations_by_service = defaultdict(list)
for old_func, new_func in consolidation_map.items():
    service = old_func.split('_')[1] if len(old_func.split('_')) > 1 else 'unknown'
    consolidations_by_service[service].append((old_func, new_func))

for service in sorted(consolidations_by_service.keys()):
    report_lines.append(f"#### {service.upper()}")
    report_lines.append("")
    
    for old_func, new_func in sorted(consolidations_by_service[service]):
        report_lines.append(f"- ❌ `{old_func}`")
        report_lines.append(f"  - ✅ Consolidated to: `{new_func}`")
        report_lines.append("")

report_lines.append("---")
report_lines.append("")
report_lines.append("## Final Function Count by Service")
report_lines.append("")
report_lines.append("| Service | Function Count |")
report_lines.append("|---------|---------------|")

for service in sorted(final_functions.keys()):
    count = len(final_functions[service])
    report_lines.append(f"| {service} | {count} |")

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("## Analysis Details")
report_lines.append("")

for group_name, group_data in sorted(analysis.items()):
    functions = group_data.get('functions_found', [])
    if len(functions) > 1:
        report_lines.append(f"### {group_name.replace('_', ' ').title()}")
        report_lines.append("")
        report_lines.append(f"**Description:** {group_data['description']}")
        report_lines.append("")
        report_lines.append(f"**Functions Analyzed:** {len(functions)}")
        report_lines.append("")
        for func in functions:
            if func in consolidation_map:
                report_lines.append(f"- ❌ `{func}` → `{consolidation_map[func]}`")
            else:
                report_lines.append(f"- ✅ `{func}` (kept)")
        report_lines.append("")
        report_lines.append(f"**Rationale:** {group_data['rationale']}")
        report_lines.append("")

report_lines.append("---")
report_lines.append("")
report_lines.append("## Files Generated")
report_lines.append("")
report_lines.append(f"1. **{OUTPUT_CSV.name}** - Final consolidated compliance CSV")
report_lines.append(f"2. **{FINAL_FUNCTIONS_JSON.name}** - Deduplicated functions by service")
report_lines.append(f"3. **{CONSOLIDATION_REPORT.name}** - This report")
report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("*End of Report*")

with open(CONSOLIDATION_REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print(f"✅ Consolidation Report: {CONSOLIDATION_REPORT.name}")
print()
print("=" * 80)
print("FINAL CONSOLIDATION COMPLETE!")
print("=" * 80)
print()
print("Files created:")
print(f"  1. {OUTPUT_CSV.name}")
print(f"  2. {FINAL_FUNCTIONS_JSON.name}")
print(f"  3. {CONSOLIDATION_REPORT.name}")

