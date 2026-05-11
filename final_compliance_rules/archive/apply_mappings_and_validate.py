"""
Applies check→rule mappings to final_compliance_rules.csv, producing:
  final_compliance_rules_mapped.csv — with new columns {csp}_mapped_rule_ids
  compliance_needs_new_rule.csv     — compliance IDs where automated but no rule mapped
  mapping_coverage_report.csv        — per-framework per-CSP coverage stats
"""
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path("/Users/apple/Desktop/compliance_Database/final_compliance_rules")
COMP = BASE / "final_compliance_rules.csv"
MAPPING_DIR = BASE / "rule_mapping"
OUT_MAPPED = BASE / "final_compliance_rules_mapped.csv"
OUT_GAPS = BASE / "compliance_needs_new_rule.csv"
OUT_REPORT = BASE / "mapping_coverage_report.csv"

CSPS = ["aws", "azure", "gcp", "oracle", "ibm", "alicloud", "k8s"]

# ── Load check → rule mappings per CSP ────────────────────────────────────
check_to_rule = {csp: {} for csp in CSPS}
for csp in CSPS:
    fp = MAPPING_DIR / f"{csp}_check_to_rule.csv"
    if not fp.exists():
        continue
    with open(fp) as f:
        for row in csv.DictReader(f):
            check = row["check_name"].strip()
            rules = row["matched_rule_ids"].strip()
            if check and rules:
                check_to_rule[csp][check] = rules


# ── Apply mappings to compliance file ─────────────────────────────────────
with open(COMP) as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    # Add mapped_rule_ids column per CSP
    for csp in CSPS:
        new_col = f"{csp}_mapped_rule_ids"
        if new_col not in fieldnames:
            fieldnames.append(new_col)
    fieldnames.append("has_any_mapped_rule")
    fieldnames.append("automated_without_rule")

    rows = []
    for row in reader:
        any_mapped = False
        for csp in CSPS:
            check_col = f"{csp}_checks"
            map_col = f"{csp}_mapped_rule_ids"
            checks = [c.strip() for c in (row.get(check_col, "") or "").split(";") if c.strip()]
            mapped_ids = []
            for c in checks:
                mapped = check_to_rule[csp].get(c, "").strip()
                if mapped:
                    for rid in mapped.split(";"):
                        rid = rid.strip()
                        if rid and rid not in mapped_ids:
                            mapped_ids.append(rid)
            row[map_col] = ";".join(mapped_ids)
            if mapped_ids:
                any_mapped = True

        is_automated = (row.get("automation_type") or "").strip().lower() == "automated"
        row["has_any_mapped_rule"] = "yes" if any_mapped else "no"
        row["automated_without_rule"] = "yes" if (is_automated and not any_mapped) else "no"
        rows.append(row)

with open(OUT_MAPPED, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Wrote: {OUT_MAPPED} ({len(rows)} rows)")


# ── Gap file: automated compliance without any rule ──────────────────────
gap_rows = [r for r in rows if r["automated_without_rule"] == "yes"]
gap_fieldnames = [
    "unique_compliance_id", "framework", "framework_version",
    "control_id", "section", "title", "automation_type",
    "aws_checks", "azure_checks", "gcp_checks", "oracle_checks",
    "ibm_checks", "alicloud_checks", "k8s_checks",
]
with open(OUT_GAPS, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=gap_fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(gap_rows)
print(f"✓ Wrote: {OUT_GAPS} ({len(gap_rows)} automated compliance IDs with NO mapped rule)")


# ── Coverage report by framework × CSP ────────────────────────────────────
fw_totals = defaultdict(lambda: {"automated": 0, "manual": 0, "auto_with_rule": 0})
fw_csp_covered = defaultdict(lambda: defaultdict(int))

for r in rows:
    fw = r["framework"]
    is_auto = (r["automation_type"] or "").strip().lower() == "automated"
    fw_totals[fw]["automated" if is_auto else "manual"] += 1
    if is_auto and r["has_any_mapped_rule"] == "yes":
        fw_totals[fw]["auto_with_rule"] += 1
    for csp in CSPS:
        if r.get(f"{csp}_mapped_rule_ids"):
            fw_csp_covered[fw][csp] += 1

report_fields = ["framework", "total_automated", "total_manual",
                  "automated_with_rule", "automated_coverage_%"] + CSPS
with open(OUT_REPORT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=report_fields)
    writer.writeheader()
    for fw in sorted(fw_totals.keys()):
        t = fw_totals[fw]
        auto = t["automated"]
        auto_with = t["auto_with_rule"]
        pct = auto_with / auto * 100 if auto else 0
        row_out = {
            "framework": fw,
            "total_automated": auto,
            "total_manual": t["manual"],
            "automated_with_rule": auto_with,
            "automated_coverage_%": f"{pct:.1f}",
        }
        for csp in CSPS:
            row_out[csp] = fw_csp_covered[fw][csp]
        writer.writerow(row_out)

print(f"✓ Wrote: {OUT_REPORT}")


# ── Print summary ─────────────────────────────────────────────────────────
total_automated = sum(1 for r in rows if (r["automation_type"] or "").lower() == "automated")
auto_with_rule = sum(1 for r in rows if r["automated_without_rule"] == "no"
                      and (r["automation_type"] or "").lower() == "automated")
auto_without_rule = len(gap_rows)

print(f"\n{'═'*60}")
print(f"FINAL COMPLIANCE VALIDATION REPORT")
print(f"{'═'*60}")
print(f"Total compliance requirements: {len(rows)}")
print(f"  Automated:                  {total_automated}")
print(f"  Manual:                     {len(rows) - total_automated}")
print(f"")
print(f"Automated coverage:")
print(f"  WITH at least one rule:     {auto_with_rule}")
print(f"  WITHOUT any rule (gap):     {auto_without_rule}  ← need new rules")
print(f"  Coverage rate:              {auto_with_rule/total_automated*100:.1f}%")

print(f"\nFramework-level coverage:")
print(f"  {'Framework':<25} {'auto':>5} {'with_rule':>10} {'cov%':>6}")
for fw in sorted(fw_totals.keys()):
    t = fw_totals[fw]
    auto = t["automated"]
    auto_with = t["auto_with_rule"]
    pct = auto_with / auto * 100 if auto else 0
    print(f"  {fw:<25} {auto:>5} {auto_with:>10} {pct:>5.1f}%")

# Per-CSP coverage
print(f"\nPer-CSP coverage (automated compliance with mapped rule):")
csp_totals = defaultdict(lambda: {"with_rule": 0, "without_rule": 0})
for r in rows:
    if (r["automation_type"] or "").lower() != "automated":
        continue
    for csp in CSPS:
        if r.get(f"{csp}_checks", "").strip():  # Only count if framework expects a check
            if r.get(f"{csp}_mapped_rule_ids"):
                csp_totals[csp]["with_rule"] += 1
            else:
                csp_totals[csp]["without_rule"] += 1
print(f"  {'CSP':<10} {'with_rule':>10} {'without_rule':>13} {'cov%':>6}")
for csp in CSPS:
    s = csp_totals[csp]
    tot = s["with_rule"] + s["without_rule"]
    pct = s["with_rule"] / tot * 100 if tot else 0
    print(f"  {csp:<10} {s['with_rule']:>10} {s['without_rule']:>13} {pct:>5.1f}%")
