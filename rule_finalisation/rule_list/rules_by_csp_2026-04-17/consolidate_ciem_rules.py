"""
Consolidate all AWS CIEM rules from /Users/apple/Desktop/threat-engine/catalog/rule/aws_rule_ciem
into one JSON file for use as an additional match source alongside aws_rules.csv.

Each consolidated record preserves the original rule's identifying + compliance fields
and flattens compliance_frameworks into a semicolon-joined aws_mapped_compliance_ids
string (to match the aws_rules.csv column convention), while also keeping the nested
per-framework list for detailed lookup.

Output:
  aws_ciem_rules_consolidated.json           list of dict records
  aws_ciem_rules_consolidated_summary.json   counts by service / check_type / framework
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

SRC = Path("/Users/apple/Desktop/threat-engine/catalog/rule/aws_rule_ciem")
BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
OUT = BASE / "aws_ciem_rules_consolidated.json"
OUT_SUMMARY = BASE / "aws_ciem_rules_consolidated_summary.json"


def flatten_compliance(ciem_rule_id: str, frameworks: dict) -> tuple[list[str], list[str]]:
    """
    Convert compliance_frameworks nested dict -> flat list of unified compliance IDs.
    Format: <framework>_<req_id>    e.g. nist_800_53_r5_AC-2, pci_dss_v4_8.2
    """
    if not isinstance(frameworks, dict):
        return [], []
    flat = []
    fws = []
    for framework, ids in frameworks.items():
        if not ids:
            continue
        fws.append(framework)
        if isinstance(ids, list):
            for i in ids:
                flat.append(f"{framework}_{i}")
        elif isinstance(ids, str):
            flat.append(f"{framework}_{ids}")
    return flat, fws


def main() -> None:
    yaml_files = sorted(p for p in SRC.rglob("*.yaml") if p.is_file())
    print(f"Found {len(yaml_files)} CIEM yaml files under {SRC}")

    records: list[dict] = []
    seen_ids: set[str] = set()
    skipped_no_id = 0
    skipped_dup = 0
    for p in yaml_files:
        try:
            data = yaml.safe_load(p.read_text())
        except Exception as e:
            print(f"  skip (yaml error): {p.relative_to(SRC)}: {e}", file=sys.stderr)
            continue
        if not isinstance(data, dict):
            continue
        rid = (data.get("rule_id") or "").strip()
        if not rid:
            skipped_no_id += 1
            continue
        if rid in seen_ids:
            skipped_dup += 1
            continue
        seen_ids.add(rid)

        compliance_ids, frameworks = flatten_compliance(rid, data.get("compliance_frameworks", {}))
        records.append({
            "rule_id": rid,
            "service": data.get("service", ""),
            "provider": data.get("provider", ""),
            "check_type": data.get("check_type", ""),
            "severity": data.get("severity", ""),
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "rationale": data.get("rationale", "")[:800],
            "domain": data.get("domain", ""),
            "threat_category": data.get("threat_category", ""),
            "action_category": data.get("action_category", ""),
            "posture_category": data.get("posture_category", ""),
            "mitre_tactics": data.get("mitre_tactics", []) or [],
            "mitre_techniques": data.get("mitre_techniques", []) or [],
            "threat_tags": data.get("threat_tags", []) or [],
            "risk_score": data.get("risk_score", ""),
            "resource": data.get("resource", ""),
            "compliance_frameworks_nested": data.get("compliance_frameworks", {}) or {},
            "aws_mapped_compliance_ids": ";".join(compliance_ids),
            "compliance_framework_list": frameworks,
            "source_category": p.relative_to(SRC).parts[0] if p.parent != SRC else "",
            "source_file": str(p.relative_to(SRC)),
        })

    print(f"Consolidated {len(records)} rules (skipped: no_id={skipped_no_id}, dup_rule_id={skipped_dup})")

    OUT.write_text(json.dumps(records, indent=2, default=str))

    svc_counts = Counter(r["service"] for r in records)
    cat_counts = Counter(r["source_category"] for r in records)
    ct_counts = Counter(r["check_type"] for r in records)
    sev_counts = Counter(r["severity"] for r in records)
    fw_counts: dict[str, int] = defaultdict(int)
    for r in records:
        for fw in r["compliance_framework_list"]:
            fw_counts[fw] += 1
    with_compliance = sum(1 for r in records if r["aws_mapped_compliance_ids"])

    summary = {
        "source": str(SRC),
        "output": str(OUT),
        "total_rules": len(records),
        "skipped": {"no_rule_id": skipped_no_id, "duplicate_rule_id": skipped_dup},
        "rules_with_compliance_framework_mapping": with_compliance,
        "by_source_category_top15": dict(cat_counts.most_common(15)),
        "by_service_top20": dict(svc_counts.most_common(20)),
        "by_check_type": dict(ct_counts.most_common()),
        "by_severity": dict(sev_counts.most_common()),
        "by_framework": dict(sorted(fw_counts.items(), key=lambda x: -x[1])),
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
