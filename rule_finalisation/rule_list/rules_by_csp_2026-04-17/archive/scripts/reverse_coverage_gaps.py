"""
Reverse direction of aws_unified_ai_mapping.csv:
  For every catalog row (aws_rules.csv) and every CIEM rule, identify which ones
  have NO YAML config rule backing them — i.e. compliance/detection rules that your
  scanner currently cannot cover.

Inputs:
  aws_rules.csv
  aws_ciem_rules_consolidated.json
  aws_unified_ai_mapping.csv       (source of truth for YAML <-> match relationships)

Outputs:
  aws_catalog_rules_without_yaml.csv    catalog rows no YAML rule maps to
  aws_ciem_rules_without_yaml.csv       CIEM rules no YAML rule maps to
  aws_reverse_coverage_summary.json
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
CATALOG_CSV = BASE / "aws_rules.csv"
CIEM_JSON = BASE / "aws_ciem_rules_consolidated.json"
MAPPING_CSV = BASE / "aws_unified_ai_mapping.csv"

OUT_CATALOG_GAP = BASE / "aws_catalog_rules_without_yaml.csv"
OUT_CIEM_GAP = BASE / "aws_ciem_rules_without_yaml.csv"
OUT_SUMMARY = BASE / "aws_reverse_coverage_summary.json"

# Only these confidence levels count as "real coverage".
# The 'low' AI confidence is noisy; we don't treat it as coverage for gap analysis.
COVERING_CONFIDENCES = {"high", "medium"}


def main():
    print("[1/5] Load mapping CSV")
    covered_catalog_ids: set[str] = set()
    covered_ciem_ids: set[str] = set()
    by_cat_conf: dict[str, Counter] = defaultdict(Counter)
    by_ciem_conf: dict[str, Counter] = defaultdict(Counter)
    with MAPPING_CSV.open() as f:
        for row in csv.DictReader(f):
            c_orig = (row.get("catalog_orig_rule_id") or "").strip()
            c_conf = (row.get("catalog_confidence") or "").strip()
            if c_orig:
                by_cat_conf[c_orig][c_conf] += 1
                if c_conf in COVERING_CONFIDENCES:
                    covered_catalog_ids.add(c_orig)
            i_rid = (row.get("ciem_rule_id") or "").strip()
            i_conf = (row.get("ciem_confidence") or "").strip()
            if i_rid:
                by_ciem_conf[i_rid][i_conf] += 1
                if i_conf in COVERING_CONFIDENCES:
                    covered_ciem_ids.add(i_rid)
    print(f"      YAML-covered catalog rule_ids: {len(covered_catalog_ids)}")
    print(f"      YAML-covered CIEM rule_ids:    {len(covered_ciem_ids)}")

    print("[2/5] Load aws_rules.csv + diff")
    with CATALOG_CSV.open() as f:
        cat_rows = list(csv.DictReader(f))
    cat_rows_unique = []
    seen_ids = set()
    for row in cat_rows:
        rid = (row.get("rule_id") or "").strip()
        if not rid or rid in seen_ids:
            continue
        seen_ids.add(rid)
        cat_rows_unique.append(row)
    cat_gap = [r for r in cat_rows_unique if r["rule_id"].strip() not in covered_catalog_ids]
    print(f"      catalog rows total: {len(cat_rows_unique)}  gap (no YAML): {len(cat_gap)}")

    # Enrich gap rows with convenience columns
    for r in cat_gap:
        rid = r["rule_id"].strip()
        r["__service_guess"] = rid.split(".")[1] if rid.count(".") >= 2 else ""
        r["__is_composite"] = "yes" if ":" in rid else "no"
        r["__has_compliance_ids"] = "yes" if (r.get("aws_mapped_compliance_ids") or "").strip() else "no"

    print("[3/5] Load CIEM + diff")
    ciem_recs = json.loads(CIEM_JSON.read_text())
    ciem_gap = [r for r in ciem_recs if r["rule_id"] not in covered_ciem_ids]
    print(f"      CIEM rules total: {len(ciem_recs)}  gap (no YAML): {len(ciem_gap)}")

    print("[4/5] Write outputs")

    # Catalog gap — original columns + 3 helpers
    cat_cols = list(cat_rows_unique[0].keys()) + ["__service_guess", "__is_composite", "__has_compliance_ids"]
    with OUT_CATALOG_GAP.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cat_cols)
        w.writeheader()
        w.writerows(cat_gap)

    # CIEM gap — selected flat columns
    ciem_cols = [
        "rule_id", "source_category", "service", "severity", "check_type",
        "title", "description", "threat_category",
        "aws_mapped_compliance_ids", "compliance_frameworks_list",
        "source_file",
    ]
    with OUT_CIEM_GAP.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ciem_cols)
        w.writeheader()
        for r in ciem_gap:
            w.writerow({
                "rule_id": r.get("rule_id", ""),
                "source_category": r.get("source_category", ""),
                "service": r.get("service", ""),
                "severity": r.get("severity", ""),
                "check_type": r.get("check_type", ""),
                "title": r.get("title", "")[:140],
                "description": r.get("description", "")[:200],
                "threat_category": r.get("threat_category", ""),
                "aws_mapped_compliance_ids": (r.get("aws_mapped_compliance_ids", "") or "")[:400],
                "compliance_frameworks_list": ";".join(r.get("compliance_framework_list", []) or []),
                "source_file": r.get("source_file", ""),
            })

    print("[5/5] Summary")
    # Breakdown: how many uncovered catalog rows have compliance IDs (meaningful loss)
    cat_gap_with_compliance = sum(1 for r in cat_gap if r["__has_compliance_ids"] == "yes")
    cat_gap_by_svc = Counter(r["__service_guess"] for r in cat_gap)
    ciem_gap_by_cat = Counter(r.get("source_category", "") for r in ciem_gap)

    summary = {
        "coverage_threshold": sorted(list(COVERING_CONFIDENCES)),
        "catalog": {
            "total_rows": len(cat_rows_unique),
            "covered_by_yaml": len(covered_catalog_ids),
            "not_covered_by_yaml": len(cat_gap),
            "not_covered_but_has_compliance_ids": cat_gap_with_compliance,
            "not_covered_no_compliance_ids": len(cat_gap) - cat_gap_with_compliance,
            "coverage_pct": round(100.0 * len(covered_catalog_ids) / len(cat_rows_unique), 2),
            "top_uncovered_services_top20": dict(cat_gap_by_svc.most_common(20)),
        },
        "ciem": {
            "total_rules": len(ciem_recs),
            "covered_by_yaml": len(covered_ciem_ids),
            "not_covered_by_yaml": len(ciem_gap),
            "coverage_pct": round(100.0 * len(covered_ciem_ids) / len(ciem_recs), 2),
            "top_uncovered_categories": dict(ciem_gap_by_cat.most_common()),
        },
        "outputs": {
            "catalog_gap_csv": str(OUT_CATALOG_GAP),
            "ciem_gap_csv": str(OUT_CIEM_GAP),
        },
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
