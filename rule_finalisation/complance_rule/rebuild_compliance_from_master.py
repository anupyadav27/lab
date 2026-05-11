"""
Rebuilds the compliance → catalog-rules mapping by INVERTING the master rules file
(consolidated_rules_phase4_2025-11-08_FINAL_WITH_ALL_IDS.csv), which is the authoritative
source for the current catalog.

Each catalog rule row has `azure_mapped_compliance_ids` (semicolon list). We invert to
produce: one row per compliance_id → list of catalog rules that reference it.

Output columns (per compliance_id):
  unique_compliance_id, aws_mapped_rules, azure_mapped_rules, gcp_mapped_rules,
  oci_mapped_rules, ibm_mapped_rules, alicloud_mapped_rules, k8s_mapped_rules
"""
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path

SRC = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/consolidated_rules_phase4_2025-11-08_FINAL_WITH_ALL_IDS.csv")
OUT_DIR = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/complance_rule")
OUT = OUT_DIR / f"compliance_to_rules_rebuilt_from_master_{date.today().isoformat()}.csv"

CSPS = ["aws", "azure", "gcp", "oci", "ibm", "alicloud", "k8s"]

# compliance_id → csp → [catalog_rule_ids]
comp_to_rules: dict[str, dict[str, set]] = defaultdict(lambda: {c: set() for c in CSPS})

# Also track which compliance frameworks each compliance_id belongs to
comp_frameworks: dict[str, set] = defaultdict(set)

total_rules = 0
with open(SRC) as f:
    for row in csv.DictReader(f):
        csp = row.get("cloud_provider", "")
        rid = row.get("rule_id", "")
        if not csp or not rid:
            continue
        total_rules += 1

        # Each CSP has its own mapped_compliance_ids column — but the rule is only
        # associated with its own CSP (cloud_provider field determines which one)
        comp_ids_col = f"{csp}_mapped_compliance_ids"
        comp_ids_val = (row.get(comp_ids_col) or "").strip()
        if not comp_ids_val:
            continue

        for cid in comp_ids_val.split(";"):
            cid = cid.strip()
            if not cid:
                continue
            comp_to_rules[cid][csp].add(rid)
            # Extract framework from compliance_id (e.g. "canada_pbmm_moderate" from "canada_pbmm_moderate_multi_cloud_CCCS_AC-2_0002")
            parts = cid.split("_")
            if parts:
                # Heuristic: framework is the prefix before "_multi_cloud" or similar
                fw = cid.split("_multi_cloud_")[0] if "_multi_cloud_" in cid else parts[0]
                comp_frameworks[cid].add(fw)

print(f"Read {total_rules} catalog rule rows")
print(f"Found {len(comp_to_rules)} unique compliance IDs")

# ── Write output ───────────────────────────────────────────────────────────
fieldnames = ["unique_compliance_id", "compliance_framework"] + \
             [f"{csp}_mapped_rules" for csp in CSPS] + \
             [f"{csp}_rule_count" for csp in CSPS]

with open(OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for cid in sorted(comp_to_rules.keys()):
        row = {"unique_compliance_id": cid,
               "compliance_framework": ";".join(sorted(comp_frameworks.get(cid, set())))}
        for csp in CSPS:
            rules = sorted(comp_to_rules[cid][csp])
            row[f"{csp}_mapped_rules"] = ";".join(rules)
            row[f"{csp}_rule_count"] = len(rules)
        writer.writerow(row)

print(f"\nWrote: {OUT}")
print(f"  Rows: {len(comp_to_rules)}")

# ── Summary stats ─────────────────────────────────────────────────────────
from collections import Counter
rules_per_comp = Counter()
coverage_by_csp = {c: 0 for c in CSPS}
for cid, per_csp in comp_to_rules.items():
    total_rules_for_cid = sum(len(rules) for rules in per_csp.values())
    rules_per_comp[cid] = total_rules_for_cid
    for csp, rules in per_csp.items():
        if rules:
            coverage_by_csp[csp] += 1

print(f"\nCoverage by CSP (compliance IDs with at least one mapped rule):")
for csp, cnt in sorted(coverage_by_csp.items(), key=lambda x: -x[1]):
    pct = cnt / len(comp_to_rules) * 100
    print(f"  {csp:10s}: {cnt:5d} / {len(comp_to_rules)} ({pct:.1f}%)")

print(f"\nRules per compliance_id distribution:")
bucket = Counter()
for cid, n in rules_per_comp.items():
    if n == 0: b = "0"
    elif n <= 5: b = "1-5"
    elif n <= 20: b = "6-20"
    elif n <= 50: b = "21-50"
    else: b = "51+"
    bucket[b] += 1
for b in ["0", "1-5", "6-20", "21-50", "51+"]:
    print(f"  {b:>6} rules: {bucket[b]}")
