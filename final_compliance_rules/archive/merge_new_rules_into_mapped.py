"""
Merges suggested new rule IDs from new_rules_by_csp/*.csv into
final_compliance_rules_mapped.csv so each row carries the COMPLETE list
of rules the engine must check (existing mapped + suggested new).

Behaviour per {csp}_mapped_rule_ids column:
  - keep existing mapped rule_ids (from real catalog)
  - append suggested_rule_ids (to be built)
  - dedup
  - recompute has_any_mapped_rule / automated_without_rule flags
"""
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path("/Users/apple/Desktop/compliance_Database/final_compliance_rules")
MAPPED = BASE / "final_compliance_rules_mapped.csv"
NEW_DIR = BASE / "new_rules_by_csp"
BACKUP = BASE / "final_compliance_rules_mapped_BACKUP.csv"

CSPS = ["aws", "azure", "gcp", "oracle", "ibm", "alicloud", "k8s"]

# Build lookup: (csp, compliance_id) → [suggested_rule_ids]
suggestions: dict[tuple[str, str], list[str]] = defaultdict(list)
for csp in CSPS:
    fp = NEW_DIR / f"{csp}_new_rules_needed.csv"
    if not fp.exists():
        continue
    with open(fp) as f:
        for row in csv.DictReader(f):
            key = (csp, row["unique_compliance_id"])
            rid = row["suggested_rule_id"].strip()
            if rid and rid not in suggestions[key]:
                suggestions[key].append(rid)

print(f"Suggestion groups loaded: {len(suggestions)}")

# Backup first
import shutil
shutil.copy(MAPPED, BACKUP)
print(f"Backup: {BACKUP}")

# Load + merge
with open(MAPPED) as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

merged_count = 0
for row in rows:
    comp_id = row["unique_compliance_id"]
    any_mapped = False
    for csp in CSPS:
        col = f"{csp}_mapped_rule_ids"
        existing = [r.strip() for r in (row.get(col, "") or "").split(";") if r.strip()]
        new = suggestions.get((csp, comp_id), [])
        merged = list(dict.fromkeys(existing + new))  # dedup preserving order
        if merged:
            any_mapped = True
        row[col] = ";".join(merged)
        if new and not existing:
            merged_count += 1

    row["has_any_mapped_rule"] = "yes" if any_mapped else "no"
    is_auto = (row.get("automation_type") or "").strip().lower() == "automated"
    row["automated_without_rule"] = "yes" if (is_auto and not any_mapped) else "no"

with open(MAPPED, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Stats
total_auto = sum(1 for r in rows if (r.get("automation_type") or "").lower() == "automated")
auto_covered = sum(1 for r in rows if (r.get("automation_type") or "").lower() == "automated"
                    and r["has_any_mapped_rule"] == "yes")
auto_gap = total_auto - auto_covered

print(f"\n═══════ MERGED FINAL COMPLIANCE FILE ═══════")
print(f"Merged: {merged_count} (csp, compliance_id) pairs got new suggested rules")
print(f"\nAutomated compliance requirements: {total_auto}")
print(f"  With at least one rule (real+suggested): {auto_covered}  ({auto_covered/total_auto*100:.1f}%)")
print(f"  STILL with no rule:                       {auto_gap}")

# Per-CSP
print(f"\nPer-CSP (automated only):")
print(f"  {'CSP':<10} {'with rule':>12} {'without':>10} {'cov%':>6}")
for csp in CSPS:
    with_rule = 0
    without = 0
    for r in rows:
        if (r.get("automation_type") or "").lower() != "automated":
            continue
        if not (r.get(f"{csp}_checks") or "").strip():
            continue
        if (r.get(f"{csp}_mapped_rule_ids") or "").strip():
            with_rule += 1
        else:
            without += 1
    total = with_rule + without
    pct = with_rule / total * 100 if total else 0
    print(f"  {csp:<10} {with_rule:>12} {without:>10} {pct:>5.1f}%")

# Regenerate compliance_needs_new_rule.csv
OUT_GAPS = BASE / "compliance_needs_new_rule.csv"
gap_fields = ["unique_compliance_id","framework","framework_version","control_id",
               "section","title","automation_type","aws_checks","azure_checks",
               "gcp_checks","oracle_checks","ibm_checks","alicloud_checks","k8s_checks"]
gap_rows = [r for r in rows if r["automated_without_rule"] == "yes"]
with open(OUT_GAPS, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=gap_fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(gap_rows)
print(f"\nUpdated {OUT_GAPS}  ({len(gap_rows)} rows)")
