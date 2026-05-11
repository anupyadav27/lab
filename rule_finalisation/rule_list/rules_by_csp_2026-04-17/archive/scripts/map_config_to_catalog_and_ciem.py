"""
Unified mapper: YAML config rules -> UNION of (aws_rules.csv catalog + CIEM catalog).

For every YAML config assertion we look up matches in BOTH sources in a single pass
and emit one row per (config_rule, match_source) candidate. Tiers applied:
  - exact:  rule_id equal to full id OR to left-of-colon alternate (catalog only)
  - fuzzy:  token Jaccard within same service (+ alias service pool) with threshold 0.5
            for the strong bucket, 0.3 for review
AI tier is a separate script (run on leftovers from this file).

Outputs:
  aws_config_unified_mapping.csv         one row per (config_rule_id, match)
  aws_config_unified_unmatched.csv       config rules with NO exact/fuzzy match in either source
  aws_config_unified_summary.json
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
YAML_PATH = BASE / "1_aws_full_scope_assertions.yaml"
CATALOG_CSV = BASE / "aws_rules.csv"
CIEM_JSON = BASE / "aws_ciem_rules_consolidated.json"

OUT_MAP = BASE / "aws_config_unified_mapping.csv"
OUT_UNMATCHED = BASE / "aws_config_unified_unmatched.csv"
OUT_SUMMARY = BASE / "aws_config_unified_summary.json"

FUZZY_STRONG = 0.5   # strong fuzzy
FUZZY_MIN = 0.3      # review fuzzy
MAX_PER_SOURCE = 5   # top-N fuzzy matches to record per (yaml_rule, source)

NOISE = {"aws", "configured", "configuration", "resource"}
SYN = {
    "logging": "log", "logs": "log",
    "encrypted": "encryption", "encrypting": "encryption",
    "policies": "policy", "keys": "key", "accounts": "account",
    "users": "user", "roles": "role", "groups": "group",
    "permissions": "permission", "instances": "instance", "buckets": "bucket",
    "clusters": "cluster", "volumes": "volume", "snapshots": "snapshot",
    "rotation": "rotate", "rotated": "rotate", "rotating": "rotate",
    "restricted": "restrict", "restricting": "restrict",
    "enforced": "enforce", "enforcing": "enforce",
    "required": "require", "requires": "require",
    "disabled": "disable",
}
SVC_ALIASES = {
    "acm_pca": ["acm.private_ca"],
    "apigateway": ["api_gateway", "api_gatewayv2", "apigatewayv2"],
    "apigatewayv2": ["api_gatewayv2", "api_gateway", "apigateway"],
    "api_gatewayv2": ["apigatewayv2", "apigateway"],
    "elb": ["elasticloadbalancing", "elbv2"],
    "elbv2": ["elasticloadbalancing", "elb"],
    "rds": ["rds", "aurora"],
    "cloudwatch": ["cloudwatch", "logs"],
    "logs": ["cloudwatch", "logs"],
    "docdb": ["documentdb", "docdb"],
    "documentdb": ["docdb"],
    "storagegateway": ["storage_gateway"],
    "directconnect": ["direct_connect"],
    "stepfunctions": ["step_functions", "sfn"],
    "step_functions": ["stepfunctions", "sfn"],
    "identitystore": ["identity_store"],
    "securityhub": ["security_hub"],
    "security_hub": ["securityhub"],
    "kinesisfirehose": ["kinesis_firehose", "firehose"],
    "inspector2": ["inspector"],
    "elasticbeanstalk": ["elastic_beanstalk"],
}

csv.field_size_limit(sys.maxsize)


def norm(rid: str):
    parts = rid.lower().replace("-", "_").split(".")
    if len(parts) < 2:
        return "", frozenset()
    svc = parts[1] if parts[0] == "aws" else parts[0]
    tail = parts[2:] if parts[0] == "aws" else parts[1:]
    toks = set()
    for p in tail:
        for t in p.split("_"):
            if not t or t in NOISE:
                continue
            t = SYN.get(t, t)
            if len(t) >= 4 and t.endswith("s") and not t.endswith("ss"):
                t = t[:-1]
            toks.add(t)
    return svc, frozenset(toks)


def jac(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load_yaml_rules() -> list[dict]:
    data = yaml.safe_load(YAML_PATH.read_text()) or {}
    out = []
    for s, rmap in data.items():
        if not isinstance(rmap, dict):
            continue
        for rk, lst in rmap.items():
            if not isinstance(lst, list):
                continue
            for a in lst:
                if isinstance(a, dict) and "rule_id" in a:
                    out.append({
                        "rule_id": a["rule_id"],
                        "yaml_service": s,
                        "yaml_resource_kind": rk,
                        "assertion_id": a.get("assertion_id", ""),
                        "scope": a.get("scope", ""),
                        "domain": a.get("domain", ""),
                        "severity": a.get("severity", ""),
                    })
    return out


def load_catalog_entries() -> list[dict]:
    """Each catalog row -> one or two entries (full rule_id + left-of-colon)."""
    entries: list[dict] = []
    with CATALOG_CSV.open() as f:
        for row in csv.DictReader(f):
            rid = (row.get("rule_id") or "").strip()
            if not rid:
                continue
            keys = [rid]
            if ":" in rid:
                keys.append(rid.split(":", 1)[0])
            for key in keys:
                svc, toks = norm(key)
                entries.append({
                    "source": "catalog",
                    "match_key": key,
                    "orig_rule_id": rid,
                    "svc": svc,
                    "toks": toks,
                    "uniform_rule_format": row.get("uniform_rule_format", ""),
                    "service": row.get("service", ""),
                    "category": row.get("category", ""),
                    "provider_service": row.get("provider_service", ""),
                    "compliance_ids": row.get("aws_mapped_compliance_ids", ""),
                    "compliance_fns": row.get("aws_mapped_compliance_functions", ""),
                    "title": "",
                    "description": "",
                })
    return entries


def load_ciem_entries() -> list[dict]:
    recs = json.loads(CIEM_JSON.read_text())
    out = []
    for r in recs:
        rid = (r.get("rule_id") or "").strip()
        if not rid:
            continue
        svc, toks = norm(rid)
        out.append({
            "source": "ciem",
            "match_key": rid,
            "orig_rule_id": rid,
            "svc": svc,
            "toks": toks,
            "uniform_rule_format": "",
            "service": r.get("service", ""),
            "category": r.get("source_category", ""),
            "provider_service": "",
            "compliance_ids": r.get("aws_mapped_compliance_ids", ""),  # semi-joined by consolidator
            "compliance_fns": "",
            "title": r.get("title", ""),
            "description": r.get("description", ""),
        })
    return out


def build_pool(svc: str, by_svc: dict[str, list[dict]]) -> list[dict]:
    pool = list(by_svc.get(svc, []))
    for alias in SVC_ALIASES.get(svc, []):
        root = alias.split(".")[0]
        pool.extend(by_svc.get(root, []))
    seen = set()
    dedup = []
    for e in pool:
        k = (e["source"], e["orig_rule_id"], e["match_key"])
        if k not in seen:
            seen.add(k)
            dedup.append(e)
    return dedup


def main():
    print("[1/5] Load inputs")
    yaml_rules = load_yaml_rules()
    catalog_entries = load_catalog_entries()
    ciem_entries = load_ciem_entries()
    all_entries = catalog_entries + ciem_entries
    by_svc: dict[str, list[dict]] = defaultdict(list)
    for e in all_entries:
        by_svc[e["svc"]].append(e)

    # exact lookup tables
    exact_by_key: dict[str, list[dict]] = defaultdict(list)
    for e in all_entries:
        exact_by_key[e["match_key"]].append(e)

    print(f"      YAML rules: {len(yaml_rules)}")
    print(f"      Catalog entries (with colon alt): {len(catalog_entries)}")
    print(f"      CIEM rules: {len(ciem_entries)}")

    print("[2/5] Match each YAML rule against unified pool")
    out_rows: list[dict] = []
    unmatched: list[dict] = []
    per_src_exact = Counter()
    per_src_strong = Counter()
    per_src_review = Counter()
    yaml_with_any_match = 0

    for r in yaml_rules:
        rid = r["rule_id"]
        svc, toks = norm(rid)

        exact_hits = exact_by_key.get(rid, [])

        pool = build_pool(svc, by_svc)
        scored = [(jac(toks, e["toks"]), e) for e in pool if e["match_key"] != rid]
        scored.sort(key=lambda x: -x[0])

        # collect top-N per source above FUZZY_MIN
        fuzzy_per_src: dict[str, list[tuple[float, dict]]] = {"catalog": [], "ciem": []}
        for s, e in scored:
            if s < FUZZY_MIN:
                continue
            bucket = fuzzy_per_src[e["source"]]
            if len(bucket) < MAX_PER_SOURCE:
                bucket.append((s, e))

        rows_for_rule = []
        for e in exact_hits:
            per_src_exact[e["source"]] += 1
            rows_for_rule.append({
                "yaml_rule_id": rid,
                "match_source": e["source"],
                "match_tier": "exact",
                "jaccard": 1.0,
                "match_key": e["match_key"],
                "match_orig_rule_id": e["orig_rule_id"],
                "match_title": e["title"],
                "match_description": e["description"][:300],
                "match_service": e["service"],
                "match_category": e["category"],
                "compliance_ids": e["compliance_ids"],
                "compliance_fns": e["compliance_fns"],
            })

        for src, bucket in fuzzy_per_src.items():
            for s, e in bucket:
                tier = "fuzzy_strong" if s >= FUZZY_STRONG else "fuzzy_review"
                if tier == "fuzzy_strong":
                    per_src_strong[src] += 1
                else:
                    per_src_review[src] += 1
                rows_for_rule.append({
                    "yaml_rule_id": rid,
                    "match_source": src,
                    "match_tier": tier,
                    "jaccard": round(s, 3),
                    "match_key": e["match_key"],
                    "match_orig_rule_id": e["orig_rule_id"],
                    "match_title": e["title"],
                    "match_description": e["description"][:300],
                    "match_service": e["service"],
                    "match_category": e["category"],
                    "compliance_ids": e["compliance_ids"],
                    "compliance_fns": e["compliance_fns"],
                })

        if rows_for_rule:
            yaml_with_any_match += 1
            # prepend YAML meta to each row for convenience
            for x in rows_for_rule:
                x.update({
                    "yaml_service": r["yaml_service"],
                    "yaml_resource_kind": r["yaml_resource_kind"],
                    "domain": r["domain"],
                    "severity": r["severity"],
                    "scope": r["scope"],
                    "assertion_id": r["assertion_id"],
                })
            out_rows.extend(rows_for_rule)
        else:
            unmatched.append(r)

    print(f"      -> YAML with >=1 match: {yaml_with_any_match}/{len(yaml_rules)}")
    print(f"      -> exact:  catalog={per_src_exact['catalog']}  ciem={per_src_exact['ciem']}")
    print(f"      -> strong: catalog={per_src_strong['catalog']}  ciem={per_src_strong['ciem']}")
    print(f"      -> review: catalog={per_src_review['catalog']}  ciem={per_src_review['ciem']}")

    print(f"[3/5] Write mapping CSV ({len(out_rows)} rows)")
    cols = [
        "yaml_rule_id", "yaml_service", "yaml_resource_kind", "domain", "severity",
        "scope", "assertion_id",
        "match_source", "match_tier", "jaccard",
        "match_key", "match_orig_rule_id", "match_service", "match_category",
        "match_title", "match_description",
        "compliance_ids", "compliance_fns",
    ]
    with OUT_MAP.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out_rows)

    print(f"[4/5] Write unmatched CSV ({len(unmatched)} rows)")
    un_cols = ["rule_id", "yaml_service", "yaml_resource_kind", "domain", "severity", "scope", "assertion_id"]
    with OUT_UNMATCHED.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=un_cols)
        w.writeheader()
        w.writerows(unmatched)

    print("[5/5] Summary")
    # Breakdown: rules with catalog hits, rules with ciem hits, rules with both
    yaml_cat = set()
    yaml_ciem = set()
    for row in out_rows:
        if row["match_source"] == "catalog":
            yaml_cat.add(row["yaml_rule_id"])
        else:
            yaml_ciem.add(row["yaml_rule_id"])
    summary = {
        "inputs": {
            "yaml_rules": len(yaml_rules),
            "catalog_entries_incl_colon_alt": len(catalog_entries),
            "ciem_rules": len(ciem_entries),
        },
        "coverage": {
            "yaml_with_any_match": yaml_with_any_match,
            "yaml_with_catalog_match": len(yaml_cat),
            "yaml_with_ciem_match": len(yaml_ciem),
            "yaml_with_both": len(yaml_cat & yaml_ciem),
            "yaml_unmatched": len(unmatched),
        },
        "match_rows_by_tier_and_source": {
            "exact_catalog": per_src_exact["catalog"],
            "exact_ciem": per_src_exact["ciem"],
            "fuzzy_strong_catalog": per_src_strong["catalog"],
            "fuzzy_strong_ciem": per_src_strong["ciem"],
            "fuzzy_review_catalog": per_src_review["catalog"],
            "fuzzy_review_ciem": per_src_review["ciem"],
        },
        "outputs": {"mapping": str(OUT_MAP), "unmatched": str(OUT_UNMATCHED)},
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
