"""
Tier 1 deterministic mapping between:
  - Config rules:      1_aws_full_scope_assertions.yaml  (what the scanner can assert)
  - Compliance rules:  aws_rules.csv                     (rule catalog already tagged with
                                                         aws_mapped_compliance_ids / functions)

Join key: YAML `rule_id`  <->  aws_rules.csv `rule_id` (and `uniform_rule_format` as fallback).

Outputs (written alongside the two inputs):
  - aws_config_to_compliance_mapping.csv      mapped config rules + compliance attrs
  - aws_config_rules_unmapped.csv             YAML rules with no row in aws_rules.csv
  - aws_compliance_rules_without_config.csv   aws_rules.csv rows with no YAML assertion
  - aws_mapping_summary.json                  counts / coverage

Nothing is written back to aws_rules.csv here. The user asked for separate mapping files.
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
YAML_PATH = BASE / "1_aws_full_scope_assertions.yaml"
RULES_CSV = BASE / "aws_rules.csv"

OUT_MAPPED = BASE / "aws_config_to_compliance_mapping.csv"
OUT_CONFIG_UNMAPPED = BASE / "aws_config_rules_unmapped.csv"
OUT_COMPLIANCE_WITHOUT_CONFIG = BASE / "aws_compliance_rules_without_config.csv"
OUT_SUMMARY = BASE / "aws_mapping_summary.json"

csv.field_size_limit(sys.maxsize)


def load_yaml_rules(path: Path) -> list[dict]:
    with path.open() as f:
        data = yaml.safe_load(f) or {}
    rules: list[dict] = []
    for service, resource_map in data.items():
        if not isinstance(resource_map, dict):
            continue
        for resource_kind, assertions in resource_map.items():
            if not isinstance(assertions, list):
                continue
            for a in assertions:
                if not isinstance(a, dict) or "rule_id" not in a:
                    continue
                rules.append({
                    "yaml_service": service,
                    "yaml_resource_kind": resource_kind,
                    "assertion_id": a.get("assertion_id", ""),
                    "rule_id": a["rule_id"],
                    "scope": a.get("scope", ""),
                    "domain": a.get("domain", ""),
                    "severity": a.get("severity", ""),
                    "implementable": a.get("implementable", ""),
                    "python_client": a.get("python_client", ""),
                    "check_client": a.get("check_client", ""),
                })
    return rules


def load_rules_csv(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def main() -> None:
    print(f"[1/4] YAML ............. {YAML_PATH.name}")
    yaml_rules = load_yaml_rules(YAML_PATH)
    print(f"      -> {len(yaml_rules)} assertions")

    print(f"[2/4] Rules CSV ........ {RULES_CSV.name}")
    csv_rows = load_rules_csv(RULES_CSV)
    print(f"      -> {len(csv_rows)} rows")

    # Index aws_rules.csv by rule_id AND uniform_rule_format (they are usually identical,
    # but either field can be authoritative). We keep a list because duplicates are possible.
    csv_index: dict[str, list[dict]] = defaultdict(list)
    for row in csv_rows:
        for key in (row.get("rule_id", "").strip(), row.get("uniform_rule_format", "").strip()):
            if key:
                csv_index[key].append(row)

    print("[3/4] Joining ...")
    mapped: list[dict] = []
    config_unmapped: list[dict] = []
    matched_csv_rule_ids: set[str] = set()

    compliance_hit_with_ids = 0  # config rules matched to a CSV row that has compliance IDs
    compliance_hit_empty = 0     # config rules matched to a CSV row with NO compliance IDs

    for r in yaml_rules:
        hits = csv_index.get(r["rule_id"], [])
        if not hits:
            config_unmapped.append(r)
            continue

        # Aggregate across all matching CSV rows (usually 1)
        all_fns: set[str] = set()
        all_ids: set[str] = set()
        services: set[str] = set()
        categories: set[str] = set()
        provider_services: set[str] = set()
        for row in hits:
            matched_csv_rule_ids.add(row.get("rule_id", "").strip())
            for v in (row.get("aws_mapped_compliance_functions", "") or "").split(";"):
                v = v.strip()
                if v: all_fns.add(v)
            for v in (row.get("aws_mapped_compliance_ids", "") or "").split(";"):
                v = v.strip()
                if v: all_ids.add(v)
            if row.get("service"): services.add(row["service"])
            if row.get("category"): categories.add(row["category"])
            if row.get("provider_service"): provider_services.add(row["provider_service"])

        has_compliance = bool(all_ids)
        if has_compliance:
            compliance_hit_with_ids += 1
        else:
            compliance_hit_empty += 1

        mapped.append({
            **r,
            "match_count": len(hits),
            "csv_service": "; ".join(sorted(services)),
            "csv_category": "; ".join(sorted(categories)),
            "csv_provider_service": "; ".join(sorted(provider_services)),
            "has_compliance_mapping": "yes" if has_compliance else "no",
            "aws_mapped_compliance_functions": "; ".join(sorted(all_fns)),
            "aws_mapped_compliance_ids": "; ".join(sorted(all_ids)),
            "aws_mapped_compliance_id_count": len(all_ids),
            "mapping_tier": "exact",
        })

    # CSV rules the YAML never covers
    all_csv_rule_ids = {row.get("rule_id", "").strip() for row in csv_rows if row.get("rule_id", "").strip()}
    compliance_without_config = [row for row in csv_rows
                                 if row.get("rule_id", "").strip()
                                 and row.get("rule_id", "").strip() not in matched_csv_rule_ids]

    print(f"      -> mapped={len(mapped)}  config_unmapped={len(config_unmapped)}  "
          f"csv_rows_without_config_rule={len(compliance_without_config)}")

    print(f"[4/4] Writing outputs to {BASE}")

    mapped_cols = [
        "rule_id", "yaml_service", "yaml_resource_kind", "csv_service", "csv_category",
        "csv_provider_service", "domain", "severity", "scope", "assertion_id",
        "python_client", "check_client", "implementable", "mapping_tier",
        "match_count", "has_compliance_mapping",
        "aws_mapped_compliance_id_count", "aws_mapped_compliance_functions",
        "aws_mapped_compliance_ids",
    ]
    with OUT_MAPPED.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=mapped_cols)
        w.writeheader()
        for r in mapped:
            w.writerow({k: r.get(k, "") for k in mapped_cols})

    unmapped_cols = [
        "rule_id", "yaml_service", "yaml_resource_kind", "domain", "severity", "scope",
        "assertion_id", "python_client", "check_client", "implementable",
    ]
    with OUT_CONFIG_UNMAPPED.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=unmapped_cols)
        w.writeheader()
        for r in config_unmapped:
            w.writerow({k: r.get(k, "") for k in unmapped_cols})

    # Preserve original aws_rules.csv columns for the "compliance-without-config" file
    orig_cols = list(csv_rows[0].keys()) if csv_rows else []
    with OUT_COMPLIANCE_WITHOUT_CONFIG.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=orig_cols)
        w.writeheader()
        for row in compliance_without_config:
            w.writerow(row)

    total_yaml = len(yaml_rules)
    summary = {
        "inputs": {
            "yaml": str(YAML_PATH),
            "aws_rules_csv": str(RULES_CSV),
        },
        "outputs": {
            "mapped": str(OUT_MAPPED),
            "config_rules_unmapped": str(OUT_CONFIG_UNMAPPED),
            "compliance_rules_without_config": str(OUT_COMPLIANCE_WITHOUT_CONFIG),
        },
        "yaml_rules": {
            "total": total_yaml,
            "matched_to_csv": len(mapped),
            "matched_with_compliance_ids": compliance_hit_with_ids,
            "matched_but_csv_has_no_compliance_ids": compliance_hit_empty,
            "unmatched": len(config_unmapped),
            "coverage_pct_vs_csv": round(100.0 * len(mapped) / total_yaml, 2) if total_yaml else 0.0,
        },
        "csv_rules": {
            "total": len(csv_rows),
            "with_compliance_ids": sum(1 for r in csv_rows if (r.get("aws_mapped_compliance_ids") or "").strip()),
            "covered_by_yaml": len(matched_csv_rule_ids),
            "not_covered_by_yaml": len(compliance_without_config),
        },
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
