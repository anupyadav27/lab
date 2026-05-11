"""
Tier 2 fuzzy mapping (human-review). Runs AFTER Tier 1 (map_aws_config_to_compliance.py).

Goal: for each YAML rule left unmapped by Tier 1, find the top-N closest aws_rules.csv
rule_ids in the SAME service, using normalized token-set similarity.

Normalization:
  - Split rule_id on "." and "_"
  - Drop noise tokens: aws, configured, configuration, resource (case-insensitive)
  - Apply a small synonym map (logging->log, logs->log, encrypted->encryption, ...)
  - Naive singularize (trailing "s" on tokens length >= 4)

Similarity:
  - Hard filter: same AWS service (token 1 after "aws.")
  - Jaccard similarity on the remaining token sets
  - Report candidates at >= FUZZY_MIN (0.5). Mark >= FUZZY_STRONG (0.8) as "strong".

Outputs (written next to the inputs):
  - aws_config_to_compliance_mapping_tier2_fuzzy.csv   top-N candidate rows for review
  - aws_config_rules_still_unmapped.csv                YAML rules with no candidate >= threshold
  - aws_mapping_summary_tier2.json                     counts and threshold breakdown

Nothing is written back to aws_rules.csv.
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
TIER1_UNMAPPED = BASE / "aws_config_rules_unmapped.csv"

OUT_FUZZY = BASE / "aws_config_to_compliance_mapping_tier2_fuzzy.csv"
OUT_STILL_UNMAPPED = BASE / "aws_config_rules_still_unmapped.csv"
OUT_SUMMARY = BASE / "aws_mapping_summary_tier2.json"

FUZZY_MIN = 0.50      # below this -> "still unmapped"
FUZZY_STRONG = 0.80   # at/above this -> strong match
TOP_N = 3             # candidates per YAML rule

NOISE_TOKENS = {"aws", "configured", "configuration", "resource"}
SYNONYMS = {
    "logging": "log", "logs": "log",
    "encrypted": "encryption", "encrypting": "encryption",
    "policies": "policy",
    "keys": "key",
    "accounts": "account",
    "users": "user",
    "roles": "role",
    "groups": "group",
    "permissions": "permission",
    "instances": "instance",
    "buckets": "bucket",
    "clusters": "cluster",
    "volumes": "volume",
    "snapshots": "snapshot",
    "rotation": "rotate", "rotated": "rotate", "rotating": "rotate",
    "restricted": "restrict", "restricting": "restrict",
    "enforced": "enforce", "enforcing": "enforce",
    "required": "require", "requires": "require",
    "disabled": "disable",
}

csv.field_size_limit(sys.maxsize)


def normalize_tokens(rule_id: str) -> tuple[str, frozenset[str]]:
    """Return (service, token_set_without_service)."""
    parts = rule_id.lower().replace("-", "_").split(".")
    if len(parts) < 2:
        return "", frozenset()
    # parts[0] is usually "aws"; service is parts[1]
    service = parts[1] if parts[0] == "aws" else parts[0]
    tail = parts[2:] if parts[0] == "aws" else parts[1:]
    toks: set[str] = set()
    for p in tail:
        for t in p.split("_"):
            if not t or t in NOISE_TOKENS:
                continue
            t = SYNONYMS.get(t, t)
            if len(t) >= 4 and t.endswith("s") and not t.endswith("ss"):
                t = t[:-1]
            toks.add(t)
    return service, frozenset(toks)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def load_yaml_rules(path: Path) -> list[dict]:
    with path.open() as f:
        data = yaml.safe_load(f) or {}
    out: list[dict] = []
    for service, rmap in data.items():
        if not isinstance(rmap, dict):
            continue
        for rk, lst in rmap.items():
            if not isinstance(lst, list):
                continue
            for a in lst:
                if isinstance(a, dict) and "rule_id" in a:
                    out.append({
                        "yaml_service": service,
                        "yaml_resource_kind": rk,
                        "assertion_id": a.get("assertion_id", ""),
                        "rule_id": a["rule_id"],
                        "scope": a.get("scope", ""),
                        "domain": a.get("domain", ""),
                        "severity": a.get("severity", ""),
                        "implementable": a.get("implementable", ""),
                        "python_client": a.get("python_client", ""),
                        "check_client": a.get("check_client", ""),
                    })
    return out


def main() -> None:
    print(f"[1/5] Load Tier 1 unmapped ids from {TIER1_UNMAPPED.name}")
    with TIER1_UNMAPPED.open() as f:
        unmapped_ids = {row["rule_id"] for row in csv.DictReader(f)}
    print(f"      -> {len(unmapped_ids)} rule_ids")

    print(f"[2/5] Load YAML to get full attrs for unmapped rules")
    yaml_rules = [r for r in load_yaml_rules(YAML_PATH) if r["rule_id"] in unmapped_ids]
    print(f"      -> {len(yaml_rules)} YAML rules to fuzzy-match")

    print(f"[3/5] Index aws_rules.csv by service")
    csv_by_service: dict[str, list[dict]] = defaultdict(list)
    all_csv_rows: list[dict] = []
    with RULES_CSV.open() as f:
        for row in csv.DictReader(f):
            rid = (row.get("rule_id") or "").strip()
            if not rid:
                continue
            svc, toks = normalize_tokens(rid)
            row["_svc"] = svc
            row["_toks"] = toks
            csv_by_service[svc].append(row)
            all_csv_rows.append(row)
    print(f"      -> {len(all_csv_rows)} CSV rows in {len(csv_by_service)} services")

    print(f"[4/5] Fuzzy matching (top {TOP_N}, min={FUZZY_MIN}, strong={FUZZY_STRONG}) ...")
    fuzzy_rows: list[dict] = []
    still_unmapped: list[dict] = []
    strong_n = 0
    weak_n = 0

    for r in yaml_rules:
        svc, toks = normalize_tokens(r["rule_id"])
        candidates = []
        for row in csv_by_service.get(svc, []):
            s = jaccard(toks, row["_toks"])
            if s >= FUZZY_MIN:
                candidates.append((s, row))
        candidates.sort(key=lambda x: -x[0])
        candidates = candidates[:TOP_N]

        if not candidates:
            still_unmapped.append(r)
            continue

        top_score = candidates[0][0]
        if top_score >= FUZZY_STRONG:
            strong_n += 1
        else:
            weak_n += 1

        for rank, (score, row) in enumerate(candidates, start=1):
            fuzzy_rows.append({
                "yaml_rule_id": r["rule_id"],
                "yaml_service": r["yaml_service"],
                "yaml_resource_kind": r["yaml_resource_kind"],
                "domain": r["domain"],
                "severity": r["severity"],
                "scope": r["scope"],
                "assertion_id": r["assertion_id"],
                "candidate_rank": rank,
                "similarity": round(score, 3),
                "candidate_strength": "strong" if score >= FUZZY_STRONG else "weak",
                "csv_rule_id": row.get("rule_id", ""),
                "csv_uniform_rule_format": row.get("uniform_rule_format", ""),
                "csv_service": row.get("service", ""),
                "csv_category": row.get("category", ""),
                "csv_provider_service": row.get("provider_service", ""),
                "aws_mapped_compliance_functions": row.get("aws_mapped_compliance_functions", ""),
                "aws_mapped_compliance_ids": row.get("aws_mapped_compliance_ids", ""),
                "review_decision": "",  # fill in manually: accept | reject | needs-edit
            })

    print(f"      -> strong matches: {strong_n}, weak matches: {weak_n}, still unmapped: {len(still_unmapped)}")

    print(f"[5/5] Writing outputs")
    fuzzy_cols = [
        "yaml_rule_id", "yaml_service", "yaml_resource_kind", "domain", "severity",
        "scope", "assertion_id", "candidate_rank", "similarity", "candidate_strength",
        "csv_rule_id", "csv_uniform_rule_format", "csv_service", "csv_category",
        "csv_provider_service", "aws_mapped_compliance_functions",
        "aws_mapped_compliance_ids", "review_decision",
    ]
    with OUT_FUZZY.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fuzzy_cols)
        w.writeheader()
        w.writerows(fuzzy_rows)

    unmapped_cols = [
        "rule_id", "yaml_service", "yaml_resource_kind", "domain", "severity", "scope",
        "assertion_id", "python_client", "check_client", "implementable",
    ]
    with OUT_STILL_UNMAPPED.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=unmapped_cols)
        w.writeheader()
        for r in still_unmapped:
            w.writerow({k: r.get(k, "") for k in unmapped_cols})

    summary = {
        "inputs": {
            "tier1_unmapped": str(TIER1_UNMAPPED),
            "yaml": str(YAML_PATH),
            "aws_rules_csv": str(RULES_CSV),
        },
        "outputs": {
            "fuzzy_candidates_csv": str(OUT_FUZZY),
            "still_unmapped_csv": str(OUT_STILL_UNMAPPED),
        },
        "thresholds": {"fuzzy_min": FUZZY_MIN, "fuzzy_strong": FUZZY_STRONG, "top_n": TOP_N},
        "counts": {
            "tier1_unmapped_input": len(yaml_rules),
            "yaml_with_at_least_one_candidate": strong_n + weak_n,
            "yaml_with_strong_candidate": strong_n,
            "yaml_with_only_weak_candidates": weak_n,
            "still_unmapped_for_tier3": len(still_unmapped),
            "total_candidate_rows_written": len(fuzzy_rows),
        },
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary["counts"], indent=2))


if __name__ == "__main__":
    main()
