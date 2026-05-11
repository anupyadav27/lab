"""
Finalize the Tier 3 review after noticing that ~21% of catalog rows have composite
rule_ids of the form "<left_concept>:<right_uniform>".  The LEFT side carries the
original scanner/assertion concept and is what YAML config rule_ids actually target;
the RIGHT side is the uniform catalog rule it is already linked to.  Matching only
on the full composite string misses most of these.

Pipeline:
  1. Re-index catalog using BOTH the full rule_id and its left-of-colon alternate.
  2. Re-score every reviewed YAML rule's best Jaccard against the expanded pool
     (same service + service aliases).
  3. Re-apply the deterministic verdict using the NEW jaccard.
  4. Emit a final CSV ready for human review or acceptance.

Inputs (read):
  aws_rules.csv
  aws_tier3_review_labeled.csv

Outputs (write):
  aws_tier3_review_final.csv     one row per reviewed rule with refreshed verdict
  aws_tier3_review_final_summary.json
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
RULES_CSV = BASE / "aws_rules.csv"
IN_REVIEW = BASE / "aws_tier3_review_labeled.csv"
OUT_CSV = BASE / "aws_tier3_review_final.csv"
OUT_SUMMARY = BASE / "aws_tier3_review_final_summary.json"

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


def verdict_for(new_conf: str, jaccard: float, pool_size: int, has_match: bool) -> tuple[str, str]:
    if pool_size == 0:
        return "CATALOG_GAP", "service absent in catalog"
    if jaccard >= 0.8 and has_match:
        return "ACCEPT", f"near-identical match (j={jaccard})"
    if jaccard >= 0.5 and new_conf in ("high", "medium") and has_match:
        return "ACCEPT", f"strong signals (j={jaccard}, ai={new_conf})"
    if jaccard >= 0.5 and has_match:
        return "KEEP_FOR_REVIEW", f"j={jaccard} but AI only {new_conf}"
    if jaccard >= 0.3 and new_conf == "high" and has_match:
        return "ACCEPT", f"AI high despite moderate j={jaccard}"
    if jaccard >= 0.3 and new_conf in ("medium", "low") and has_match:
        return "KEEP_FOR_REVIEW", f"moderate j={jaccard} + AI {new_conf}"
    if jaccard >= 0.3:
        return "GAP_LIKELY", f"j={jaccard}, AI none"
    if jaccard >= 0.15 and new_conf == "high" and has_match:
        return "KEEP_FOR_REVIEW", f"AI overrides weak j={jaccard}"
    if jaccard >= 0.15:
        return "GAP_LIKELY", f"weak overlap j={jaccard}"
    return "GAP_CONFIRMED", f"no overlap (j={jaccard})"


def main():
    print("[1/4] Build expanded catalog index (rule_id + left-of-colon alternate)")
    cat_by_svc: dict[str, list[dict]] = defaultdict(list)
    with RULES_CSV.open() as f:
        for row in csv.DictReader(f):
            rid = (row.get("rule_id") or "").strip()
            if not rid:
                continue
            keys = [rid]
            if ":" in rid:
                keys.append(rid.split(":", 1)[0])
            for key in keys:
                svc, toks = norm(key)
                cat_by_svc[svc].append({
                    "orig_rid": rid,
                    "key": key,
                    "uniform_rule_format": row.get("uniform_rule_format", ""),
                    "service": row.get("service", ""),
                    "category": row.get("category", ""),
                    "provider_service": row.get("provider_service", ""),
                    "compliance_ids": row.get("aws_mapped_compliance_ids", ""),
                    "compliance_fns": row.get("aws_mapped_compliance_functions", ""),
                    "_toks": toks,
                })

    print("[2/4] Re-score each reviewed rule")
    with IN_REVIEW.open() as f:
        rows = list(csv.DictReader(f))

    out_rows = []
    verdict_counts = Counter()
    moves = Counter()  # old -> new transitions
    for r in rows:
        yrid = r["yaml_rule_id"]
        svc, toks = norm(yrid)
        pool = list(cat_by_svc.get(svc, []))
        for alias in SVC_ALIASES.get(svc, []):
            root = alias.split(".")[0]
            pool.extend(cat_by_svc.get(root, []))
        # Dedupe by (orig_rid, key) pair
        seen = set()
        dedup = []
        for e in pool:
            k = (e["orig_rid"], e["key"])
            if k not in seen:
                seen.add(k)
                dedup.append(e)
        pool = dedup
        pool_size = len(pool)

        scored = [(jac(toks, e["_toks"]), e) for e in pool]
        scored.sort(key=lambda x: -x[0])
        top5 = scored[:5]
        best_j, best_e = (scored[0] if scored else (0.0, None))

        old_decision = r["manual_review_decision"]
        new_conf = (r["new_ai_confidence"] or "none").lower()
        has_match = best_e is not None and best_j > 0
        new_decision, note = verdict_for(new_conf, best_j, pool_size, has_match)
        verdict_counts[new_decision] += 1
        if old_decision != new_decision:
            moves[f"{old_decision} -> {new_decision}"] += 1

        out_rows.append({
            "yaml_rule_id": yrid,
            "yaml_service": r.get("yaml_service", ""),
            "yaml_resource_kind": r.get("yaml_resource_kind", ""),
            "scope": r.get("scope", ""),
            "domain": r.get("domain", ""),
            "severity": r.get("severity", ""),
            "pool_size": pool_size,
            "best_jaccard_v2": round(best_j, 3),
            "best_match_key": best_e["key"] if best_e else "",
            "best_match_orig_rid": best_e["orig_rid"] if best_e else "",
            "best_match_has_compliance_ids": "yes" if (best_e and best_e["compliance_ids"].strip()) else "no",
            "best_match_compliance_ids": best_e["compliance_ids"] if best_e else "",
            "best_match_compliance_fns": best_e["compliance_fns"] if best_e else "",
            "ai_match_rule_id": r.get("new_ai_match", ""),
            "ai_confidence": r.get("new_ai_confidence", ""),
            "ai_reasoning": r.get("new_ai_reasoning", ""),
            "old_verdict": old_decision,
            "final_verdict": new_decision,
            "final_verdict_note": note,
            "top5_candidates": "; ".join(f"{e['key']}({s:.2f})" for s, e in top5),
        })

    print("[3/4] Writing aws_tier3_review_final.csv")
    cols = list(out_rows[0].keys())
    # Order: ACCEPT first (fast win), then KEEP_FOR_REVIEW, then gaps
    order = {"ACCEPT": 0, "KEEP_FOR_REVIEW": 1, "GAP_LIKELY": 2, "GAP_CONFIRMED": 3, "CATALOG_GAP": 4}
    out_rows.sort(key=lambda x: (order.get(x["final_verdict"], 9), -float(x["best_jaccard_v2"] or 0)))
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out_rows)

    print("[4/4] Summary")
    # How many "moved up" (became ACCEPT from GAP_LIKELY etc.)
    upward = {"GAP_CONFIRMED -> ACCEPT", "GAP_CONFIRMED -> KEEP_FOR_REVIEW",
              "GAP_LIKELY -> ACCEPT", "GAP_LIKELY -> KEEP_FOR_REVIEW",
              "KEEP_FOR_REVIEW -> ACCEPT"}
    upgraded = sum(v for k, v in moves.items() if k in upward)
    summary = {
        "total_rows": len(out_rows),
        "final_verdicts": dict(verdict_counts),
        "verdict_changes": dict(moves.most_common()),
        "rows_upgraded_by_colon_split": upgraded,
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
