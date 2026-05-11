#!/usr/bin/env python3
"""
Create Step 5: Rule-to-Compliance alignment
- Update final mapping JSON with step5 summary
- Update rule list CSV with mapped compliance functions and IDs
"""
import json
import pandas as pd
from collections import defaultdict

MAPPING_FILE = "service_mappings/AWS_ONE_TO_ONE_MAPPING_BULLETPROOF_COMPLETE_FINAL_WITH_COMPLIANCE.json"
COMPLIANCE_CSV = "complance_rule/consolidated_compliance_rules_FINAL.csv"
RULE_LIST_CSV = "rule_list/consolidated_rules_phase4_2025-11-08.csv"

# Load mapping JSON
with open(MAPPING_FILE, "r") as f:
    mapping = json.load(f)

# Build compliance context (function -> set of unique IDs and requirement strings)
df = pd.read_csv(COMPLIANCE_CSV)
func_to_ids = defaultdict(set)
func_to_req = defaultdict(set)

for _, row in df.iterrows():
    funcs = str(row.get("aws_uniform_format", "")).split(';') if pd.notna(row.get("aws_uniform_format")) else []
    unique_id = str(row.get("unique_compliance_id", "")) if pd.notna(row.get("unique_compliance_id")) else ""
    requirement_name = str(row.get("requirement_name", "")) if pd.notna(row.get("requirement_name")) else ""

    for func in funcs:
        func = func.strip()
        if not func:
            continue
        if unique_id:
            func_to_ids[func].add(unique_id)
        if requirement_name:
            func_to_req[func].add(requirement_name)

# Build rule alignment structure
rule_alignment = {}

for service, data in mapping.items():
    if service == "metadata":
        continue

    # Step 1 - direct
    for func, rule in data.get("step1_direct_mapped", {}).items():
        entry = rule_alignment.setdefault(rule, {
            "services": set(),
            "compliance_functions": set(),
            "compliance_ids": set(),
            "coverage_sources": set()
        })
        entry["services"].add(service)
        entry["compliance_functions"].add(func)
        entry["compliance_ids"].update(func_to_ids.get(func, []))
        entry["coverage_sources"].add("STEP1_DIRECT")

    # Step 2 - AI coverage
    for func, info in data.get("step2_covered_by", {}).items():
        rules = info.get("covered_by_rules", [])
        coverage_type = info.get("coverage_type", "AI")
        for rule in rules:
            entry = rule_alignment.setdefault(rule, {
                "services": set(),
                "compliance_functions": set(),
                "compliance_ids": set(),
                "coverage_sources": set()
            })
            entry["services"].add(service)
            entry["compliance_functions"].add(func)
            entry["compliance_ids"].update(func_to_ids.get(func, []))
            entry["coverage_sources"].add(coverage_type)

# Convert sets to sorted lists
formatted_alignment = {}
for rule, details in sorted(rule_alignment.items()):
    functions_sorted = sorted(details["compliance_functions"])
    ids_sorted = sorted(details["compliance_ids"])
    services_sorted = sorted(details["services"])
    coverage_sorted = sorted(details["coverage_sources"])

    formatted_alignment[rule] = {
        "services": services_sorted,
        "compliance_functions": functions_sorted,
        "compliance_ids": ids_sorted,
        "coverage_sources": coverage_sorted,
        "compliance_requirements": {
            func: sorted(func_to_req.get(func, [])) for func in functions_sorted
        }
    }

# Add Step 5 section to mapping JSON
mapping["step5_rule_alignment"] = formatted_alignment

with open(MAPPING_FILE, "w") as f:
    json.dump(mapping, f, indent=2)

# Update rule list CSV with new columns
rule_df = pd.read_csv(RULE_LIST_CSV)

mapped_functions = []
mapped_ids = []
coverage_sources = []
services = []

for rule_id in rule_df.get("rule_id", []):
    details = formatted_alignment.get(rule_id, None)
    if details:
        mapped_functions.append(';'.join(details["compliance_functions"]))
        mapped_ids.append(';'.join(details["compliance_ids"]))
        coverage_sources.append(';'.join(details["coverage_sources"]))
        services.append(';'.join(details["services"]))
    else:
        mapped_functions.append('')
        mapped_ids.append('')
        coverage_sources.append('')
        services.append('')

rule_df['mapped_compliance_functions'] = mapped_functions
rule_df['mapped_compliance_ids'] = mapped_ids
rule_df['mapping_sources'] = coverage_sources
rule_df['mapping_services'] = services

rule_df.to_csv(RULE_LIST_CSV, index=False)

print("Step 5 alignment complete:")
print(f"- Updated mapping JSON with {len(formatted_alignment)} rule entries")
print(f"- Updated CSV with new mapping columns")
