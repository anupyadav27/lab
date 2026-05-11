"""
Re-evaluates the Tier 3 medium/low/none rules after expanding the service-alias map,
and produces a single review CSV with a verdict bucket per rule:

Verdict buckets (independent of the LLM call):
  - ai-likely-missed      best Jaccard >= 0.5   (likely a valid match the first pass missed)
  - borderline-look       0.3  <= best < 0.5    (human should confirm)
  - weak-shared-theme     0.15 <= best < 0.3    (loosely related)
  - real-gap              best < 0.15           (catalog likely does not cover this)
  - catalog-empty         service absent in catalog (genuine gap)

For every rule we ALSO run DeepSeek again with the widened candidate pool, so the
review file shows both the token-based verdict AND the LLM's second-pass choice.

Output: aws_tier3_review.csv  (one row per rule)
        aws_tier3_review_summary.json
"""
import csv
import json
import os
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

import yaml
from openai import OpenAI

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
YAML_PATH = BASE / "1_aws_full_scope_assertions.yaml"
RULES_CSV = BASE / "aws_rules.csv"
CHECKPOINT_IN = BASE / "aws_mapping_tier3_checkpoint.json"

OUT_CSV = BASE / "aws_tier3_review.csv"
OUT_SUMMARY = BASE / "aws_tier3_review_summary.json"
CHECKPOINT_OUT = BASE / "aws_tier3_review_checkpoint.json"

TOP_K = 20

SERVICE_ALIASES = {
    "acm_pca": ["acm.private_ca"],
    "apigateway": ["api_gateway", "api_gatewayv2", "apigatewayv2"],
    "api_gateway": ["apigateway", "api_gatewayv2", "apigatewayv2"],
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
    "timestream": ["timestream_write", "timestream_query"],
    "elasticbeanstalk": ["elastic_beanstalk"],
}

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

csv.field_size_limit(sys.maxsize)


def norm(rid):
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


def load_yaml_idx():
    with YAML_PATH.open() as f:
        d = yaml.safe_load(f) or {}
    out = {}
    for s, rm in d.items():
        if not isinstance(rm, dict):
            continue
        for rk, lst in rm.items():
            if not isinstance(lst, list):
                continue
            for a in lst:
                if isinstance(a, dict) and "rule_id" in a:
                    out[a["rule_id"]] = {
                        "yaml_service": s,
                        "yaml_resource_kind": rk,
                        "assertion_id": a.get("assertion_id", ""),
                        "scope": a.get("scope", ""),
                        "domain": a.get("domain", ""),
                        "severity": a.get("severity", ""),
                    }
    return out


def load_catalog():
    rows = []
    by_svc = defaultdict(list)
    by_id = {}
    with RULES_CSV.open() as f:
        for row in csv.DictReader(f):
            rid = (row.get("rule_id") or "").strip()
            if not rid:
                continue
            svc, toks = norm(rid)
            row["_svc"] = svc
            row["_toks"] = toks
            rows.append(row)
            by_svc[svc].append(row)
            by_id[rid] = row
    return rows, by_svc, by_id


def build_pool(svc, by_svc):
    pool = list(by_svc.get(svc, []))
    for alias in SERVICE_ALIASES.get(svc, []):
        root = alias.split(".")[0]
        pool.extend(by_svc.get(root, []))
    seen = set()
    dedup = []
    for r in pool:
        rid = r.get("rule_id", "")
        if rid and rid not in seen:
            seen.add(rid)
            dedup.append(r)
    return dedup


def verdict_for(best_jaccard, pool_size):
    if pool_size == 0:
        return "catalog-empty"
    if best_jaccard >= 0.5:
        return "ai-likely-missed"
    if best_jaccard >= 0.3:
        return "borderline-look"
    if best_jaccard >= 0.15:
        return "weak-shared-theme"
    return "real-gap"


SYSTEM_PROMPT = """You are an AWS compliance expert matching scanner assertions to a compliance-catalog of rule_ids.

You will receive one YAML config rule and a list of candidate catalog rules (drawn from the same AWS service, including common alias services such as api_gatewayv2 for apigatewayv2, documentdb for docdb, etc).

Pick the single best semantic match from the candidates, or return null only if NONE of the candidates actually covers the same control.

Output ONLY a JSON object:
{
  "match_rule_id": "<candidate rule_id or null>",
  "confidence": "high" | "medium" | "low" | "none",
  "reasoning": "<one short sentence>"
}

Confidence guide:
- high:   candidate asserts the same control on the same resource (minor wording drift OK).
- medium: same intent, slightly different resource or granularity.
- low:    partial overlap worth keeping for review.
- none:   genuinely unrelated.

Reasoning MUST be non-empty whenever you return a match_rule_id. Prefer low over none when there is partial overlap."""


def user_prompt(rid, yinfo, cands):
    lines = [
        f"- rule_id: {row.get('rule_id','')} | category: {row.get('category','')} | jaccard: {s:.2f}"
        for s, row in cands
    ]
    return (
        f"YAML config rule:\n"
        f"  rule_id:       {rid}\n"
        f"  assertion_id:  {yinfo.get('assertion_id','')}\n"
        f"  scope:         {yinfo.get('scope','')}\n"
        f"  domain:        {yinfo.get('domain','')}\n"
        f"\nCandidate catalog rules:\n" + "\n".join(lines)
    )


def classify(client, model, rid, yinfo, cands):
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt(rid, yinfo, cands)},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        raw = resp.choices[0].message.content or "{}"
        p = json.loads(raw)
        return {
            "match_rule_id": p.get("match_rule_id") or "",
            "confidence": (p.get("confidence") or "none").lower(),
            "reasoning": (p.get("reasoning") or "")[:500],
            "error": "",
        }
    except Exception as e:
        return {"match_rule_id": "", "confidence": "none", "reasoning": "", "error": str(e)[:300]}


def main():
    api_key = (os.getenv("DEEPSEEK_API_KEY") or "").strip()
    if not api_key:
        print("ERROR: DEEPSEEK_API_KEY not set", file=sys.stderr)
        sys.exit(2)
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    model = "deepseek-chat"

    print("[1/5] Loading inputs")
    yaml_idx = load_yaml_idx()
    catalog, by_svc, by_id = load_catalog()
    cp = json.loads(CHECKPOINT_IN.read_text())["results"]

    # Pick only rows whose original confidence was low/medium/none
    target_ids = [rid for rid, res in cp.items() if res.get("confidence") in ("low", "medium", "none")]
    print(f"      -> {len(target_ids)} rules to re-evaluate")

    # Resume handling
    prev = {}
    if CHECKPOINT_OUT.exists():
        prev = json.loads(CHECKPOINT_OUT.read_text()).get("results", {})
    remaining = [rid for rid in target_ids if rid not in prev]
    print(f"[2/5] {len(prev)} resumed, {len(remaining)} remaining")

    print("[3/5] Re-picking candidates with widened aliases + re-classifying")
    lock = Lock()

    def worker(rid):
        yinfo = yaml_idx.get(rid, {})
        svc, toks = norm(rid)
        pool = build_pool(svc, by_svc)
        pool_size = len(pool)
        scored = [(jac(toks, r["_toks"]), r) for r in pool]
        scored.sort(key=lambda x: -x[0])
        top = scored[:TOP_K]
        best_jaccard = top[0][0] if top else 0.0
        v = verdict_for(best_jaccard, pool_size)
        # Skip LLM for catalog-empty (save tokens)
        if pool_size == 0:
            res = {"match_rule_id": "", "confidence": "none",
                   "reasoning": "no catalog rule exists for this service", "error": ""}
        else:
            res = classify(client, model, rid, yinfo, top)
        return rid, {
            "yaml_service": yinfo.get("yaml_service", ""),
            "yaml_resource_kind": yinfo.get("yaml_resource_kind", ""),
            "assertion_id": yinfo.get("assertion_id", ""),
            "scope": yinfo.get("scope", ""),
            "domain": yinfo.get("domain", ""),
            "severity": yinfo.get("severity", ""),
            "best_jaccard": round(best_jaccard, 3),
            "pool_size": pool_size,
            "verdict_bucket": v,
            "prev_ai_match": cp[rid].get("match_rule_id") or "",
            "prev_ai_confidence": cp[rid].get("confidence") or "",
            "prev_ai_reasoning": cp[rid].get("reasoning") or "",
            "new_ai_match": res.get("match_rule_id", ""),
            "new_ai_confidence": res.get("confidence", ""),
            "new_ai_reasoning": res.get("reasoning", ""),
            "top5_candidates": "; ".join(f"{r.get('rule_id','')}({s:.2f})" for s, r in top[:5]),
            "error": res.get("error", ""),
        }

    done = 0
    results = dict(prev)
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(worker, rid): rid for rid in remaining}
        for f in as_completed(futs):
            rid, rec = f.result()
            with lock:
                results[rid] = rec
                done += 1
                if done % 25 == 0:
                    CHECKPOINT_OUT.write_text(json.dumps({"results": results}, indent=2))
                    print(f"      ... {done}/{len(remaining)}")
    CHECKPOINT_OUT.write_text(json.dumps({"results": results}, indent=2))

    print("[4/5] Writing review CSV")
    cols = [
        "yaml_rule_id", "yaml_service", "yaml_resource_kind",
        "scope", "domain", "severity", "assertion_id",
        "verdict_bucket", "best_jaccard", "pool_size",
        "prev_ai_match", "prev_ai_confidence", "prev_ai_reasoning",
        "new_ai_match", "new_ai_confidence", "new_ai_reasoning",
        "top5_candidates",
        "manual_review_decision", "manual_review_notes",
    ]
    rows_out = []
    for rid in target_ids:
        rec = results.get(rid, {})
        rows_out.append({
            "yaml_rule_id": rid,
            **{k: rec.get(k, "") for k in cols if k not in ("yaml_rule_id", "manual_review_decision", "manual_review_notes")},
            "manual_review_decision": "",
            "manual_review_notes": "",
        })
    # sort: ai-likely-missed first, borderline, weak, real-gap, catalog-empty
    order = {"ai-likely-missed": 0, "borderline-look": 1, "weak-shared-theme": 2, "real-gap": 3, "catalog-empty": 4}
    rows_out.sort(key=lambda r: (order.get(r.get("verdict_bucket", ""), 9), r["yaml_rule_id"]))
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows_out)

    print("[5/5] Summary")
    from collections import Counter
    bucket_counts = Counter(r["verdict_bucket"] for r in rows_out)
    new_conf_counts = Counter(r["new_ai_confidence"] for r in rows_out)
    # Count rows where AI changed its mind (none -> high/medium/low)
    flipped = sum(
        1 for r in rows_out
        if r["prev_ai_confidence"] == "none" and r["new_ai_confidence"] in ("high", "medium", "low")
    )
    summary = {
        "total_reviewed": len(rows_out),
        "verdict_buckets": dict(bucket_counts),
        "new_ai_confidence": dict(new_conf_counts),
        "flipped_none_to_match": flipped,
        "output_csv": str(OUT_CSV),
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
