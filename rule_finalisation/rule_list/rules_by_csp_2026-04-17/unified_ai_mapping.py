"""
Unified AI mapping: for every YAML config assertion, decide the best CATALOG match
and the best CIEM match in a single LLM call, using deterministic Jaccard prefilters.

Why one pass per rule (not two): sharing the model context cuts cost ~2x and lets
the LLM compare the two source pools holistically (e.g. it may prefer a CIEM detection
rule when no posture catalog rule exists).

Inputs:
  1_aws_full_scope_assertions.yaml
  aws_rules.csv                           (catalog; left-of-colon alt indexed)
  aws_ciem_rules_consolidated.json        (CIEM detections, 493 rules)

Outputs (next to inputs):
  aws_unified_ai_mapping.csv              one row per YAML rule with catalog + CIEM picks
  aws_unified_ai_unmatched.csv            YAML rules with no match in either source
  aws_unified_ai_summary.json             counts
  aws_unified_ai_checkpoint.json          resumable state

CLI:
  --limit N        Process only first N
  --model NAME     Default: deepseek-chat
  --concurrency K  Default: 10
  --resume         Skip rule_ids already in checkpoint
  --skip-exact     If set, don't call LLM for rules that already have an exact catalog hit
                   (faster; default True). Use --no-skip-exact to force AI on everything.

Env: DEEPSEEK_API_KEY  (OpenAI-compat endpoint https://api.deepseek.com)
"""
import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

import yaml
from openai import OpenAI

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
YAML_PATH = BASE / "1_aws_full_scope_assertions.yaml"
CATALOG_CSV = BASE / "aws_rules.csv"
CIEM_JSON = BASE / "aws_ciem_rules_consolidated.json"

OUT_CSV = BASE / "aws_unified_ai_mapping.csv"
OUT_UNMATCHED = BASE / "aws_unified_ai_unmatched.csv"
OUT_SUMMARY = BASE / "aws_unified_ai_summary.json"
CHECKPOINT = BASE / "aws_unified_ai_checkpoint.json"

TOP_K_CATALOG = 12
TOP_K_CIEM = 10

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


def load_yaml_rules():
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


def load_catalog():
    """Return (entries, by_service, by_key) — entries include colon-left alternates."""
    entries: list[dict] = []
    by_svc: dict[str, list[dict]] = defaultdict(list)
    by_key: dict[str, list[dict]] = defaultdict(list)
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
                e = {
                    "match_key": key,
                    "orig_rule_id": rid,
                    "svc": svc,
                    "toks": toks,
                    "uniform_rule_format": row.get("uniform_rule_format", ""),
                    "service": row.get("service", ""),
                    "category": row.get("category", ""),
                    "compliance_ids": row.get("aws_mapped_compliance_ids", ""),
                    "compliance_fns": row.get("aws_mapped_compliance_functions", ""),
                }
                entries.append(e)
                by_svc[svc].append(e)
                by_key[key].append(e)
    return entries, by_svc, by_key


def load_ciem():
    recs = json.loads(CIEM_JSON.read_text())
    entries = []
    by_svc: dict[str, list[dict]] = defaultdict(list)
    by_key: dict[str, list[dict]] = {}
    for r in recs:
        rid = (r.get("rule_id") or "").strip()
        if not rid:
            continue
        svc, toks = norm(rid)
        e = {
            "rule_id": rid,
            "svc": svc,
            "toks": toks,
            "title": r.get("title", ""),
            "description": r.get("description", ""),
            "service": r.get("service", ""),
            "source_category": r.get("source_category", ""),
            "threat_category": r.get("threat_category", ""),
            "domain": r.get("domain", ""),
            "compliance_ids": r.get("aws_mapped_compliance_ids", ""),
            "compliance_frameworks_nested": r.get("compliance_frameworks_nested", {}),
        }
        entries.append(e)
        by_svc[svc].append(e)
        by_key[rid] = e
    return entries, by_svc, by_key


def build_pool(svc, by_svc):
    pool = list(by_svc.get(svc, []))
    for alias in SVC_ALIASES.get(svc, []):
        root = alias.split(".")[0]
        pool.extend(by_svc.get(root, []))
    seen = set()
    dedup = []
    for e in pool:
        k = (e.get("orig_rule_id") or e.get("rule_id") or "") + "|" + (e.get("match_key", ""))
        if k not in seen:
            seen.add(k)
            dedup.append(e)
    return dedup


def top_candidates(y_toks, pool, k):
    scored = [(jac(y_toks, e["toks"]), e) for e in pool]
    scored.sort(key=lambda x: -x[0])
    return scored[:k]


# -------- prompt --------
SYSTEM_PROMPT = """You are an AWS compliance and security expert.

You receive ONE YAML config (posture) assertion and two candidate lists:
  A) CATALOG candidates (configuration / posture rules from aws_rules.csv)
  B) CIEM candidates   (detection / log-correlation rules that may cover the same control from a threat-monitoring angle)

A config assertion can legitimately map to BOTH a catalog posture rule AND one or more CIEM detection rules that cover the same control. Pick the single best match for each source independently.

Return ONLY this JSON object (both keys required, null when no real match):

{
  "catalog_match": {
    "match_key":    "<candidate match_key or null>",
    "confidence":   "high" | "medium" | "low" | "none",
    "reasoning":    "<one short sentence>"
  },
  "ciem_match": {
    "rule_id":      "<candidate rule_id or null>",
    "confidence":   "high" | "medium" | "low" | "none",
    "reasoning":    "<one short sentence>"
  }
}

Confidence guidelines:
- high:   candidate covers the same technical control on the same resource (synonyms OK).
- medium: same intent at slightly different granularity.
- low:    partial overlap worth human review.
- none:   no candidate actually covers the control.

Reasoning MUST be non-empty whenever you return a non-null match. Prefer low over none when there is genuine partial overlap. Spurious matches are still worse than "none"."""


def build_user_prompt(yaml_rule: dict, cat_cands, ciem_cands) -> str:
    cat_lines = [
        f"  - match_key: {e['match_key']} | service: {e['service']} | category: {e['category']} | jaccard: {s:.2f}"
        for s, e in cat_cands
    ] or ["  (no catalog candidates)"]
    ciem_lines = [
        f"  - rule_id: {e['rule_id']} | title: {e['title'][:70]} | threat: {e['threat_category']} | jaccard: {s:.2f}"
        for s, e in ciem_cands
    ] or ["  (no CIEM candidates)"]
    return (
        f"YAML config assertion:\n"
        f"  rule_id:       {yaml_rule['rule_id']}\n"
        f"  assertion_id:  {yaml_rule['assertion_id']}\n"
        f"  scope:         {yaml_rule['scope']}\n"
        f"  domain:        {yaml_rule['domain']}\n"
        f"  severity:      {yaml_rule.get('severity','')}\n"
        f"\nA) CATALOG candidates:\n" + "\n".join(cat_lines) +
        f"\n\nB) CIEM candidates:\n" + "\n".join(ciem_lines)
    )


def classify(client: OpenAI, model: str, yaml_rule: dict, cat_cands, ciem_cands) -> dict:
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(yaml_rule, cat_cands, ciem_cands)},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        raw = resp.choices[0].message.content or "{}"
        p = json.loads(raw)
        cat = p.get("catalog_match") or {}
        cie = p.get("ciem_match") or {}
        return {
            "catalog_match_key": cat.get("match_key") or "",
            "catalog_confidence": (cat.get("confidence") or "none").lower(),
            "catalog_reasoning": (cat.get("reasoning") or "")[:400],
            "ciem_rule_id": cie.get("rule_id") or "",
            "ciem_confidence": (cie.get("confidence") or "none").lower(),
            "ciem_reasoning": (cie.get("reasoning") or "")[:400],
            "error": "",
        }
    except Exception as e:
        return {
            "catalog_match_key": "", "catalog_confidence": "none", "catalog_reasoning": "",
            "ciem_rule_id": "", "ciem_confidence": "none", "ciem_reasoning": "",
            "error": str(e)[:300],
        }


def load_ckpt():
    if CHECKPOINT.exists():
        try:
            return json.loads(CHECKPOINT.read_text()).get("results", {})
        except Exception:
            return {}
    return {}


def save_ckpt(results: dict):
    CHECKPOINT.write_text(json.dumps({"results": results}, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--model", default="deepseek-chat")
    ap.add_argument("--concurrency", type=int, default=10)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--skip-exact", dest="skip_exact", action="store_true", default=True)
    ap.add_argument("--no-skip-exact", dest="skip_exact", action="store_false")
    args = ap.parse_args()

    api_key = (os.getenv("DEEPSEEK_API_KEY") or "").strip()
    if not api_key:
        print("ERROR: DEEPSEEK_API_KEY not set", file=sys.stderr)
        sys.exit(2)
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    print("[1/6] Loading inputs")
    yaml_rules = load_yaml_rules()
    if args.limit:
        yaml_rules = yaml_rules[: args.limit]
    cat_entries, cat_by_svc, cat_by_key = load_catalog()
    ciem_entries, ciem_by_svc, ciem_by_key = load_ciem()
    # CIEM uses functional categories (paas, netsec, datasec, ...) not AWS service names,
    # so same-service filtering misses most relevant detections. Jaccard the whole pool.
    print(f"      yaml={len(yaml_rules)} catalog={len(cat_entries)} ciem={len(ciem_entries)}")

    # Pre-compute top-K candidates + exact hits; collect rules that need the LLM
    print("[2/6] Prefilter candidates per YAML rule")
    prep = {}
    ai_needed_ids = []
    exact_hit_count = 0
    for r in yaml_rules:
        rid = r["rule_id"]
        svc, toks = norm(rid)
        cat_pool = build_pool(svc, cat_by_svc)
        # CIEM: scan ALL rules (small pool, functional categories as service)
        ciem_pool = ciem_entries

        cat_exact = cat_by_key.get(rid, [])
        ciem_exact = [ciem_by_key[rid]] if rid in ciem_by_key else []

        cat_top = top_candidates(toks, cat_pool, TOP_K_CATALOG)
        ciem_top = top_candidates(toks, ciem_pool, TOP_K_CIEM)

        prep[rid] = {
            "yaml_rule": r,
            "cat_exact": cat_exact,
            "ciem_exact": ciem_exact,
            "cat_top": cat_top,
            "ciem_top": ciem_top,
        }
        has_exact = bool(cat_exact) or bool(ciem_exact)
        if has_exact:
            exact_hit_count += 1
        if args.skip_exact and cat_exact and ciem_exact:
            # both sides exact — still skip LLM
            continue
        ai_needed_ids.append(rid)
    print(f"      exact-hit rules: {exact_hit_count} | AI-needed: {len(ai_needed_ids)}")

    prev = load_ckpt() if args.resume else {}
    todo = [rid for rid in ai_needed_ids if rid not in prev]
    print(f"[3/6] Resume: {len(prev)} already done, {len(todo)} remaining")

    lock = Lock()
    results = dict(prev)

    def worker(rid):
        p = prep[rid]
        return rid, classify(client, args.model, p["yaml_rule"], p["cat_top"], p["ciem_top"])

    print(f"[4/6] Calling {args.model} (concurrency={args.concurrency}) ...")
    done = 0
    if todo:
        with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futs = {ex.submit(worker, rid): rid for rid in todo}
            for f in as_completed(futs):
                rid, res = f.result()
                with lock:
                    results[rid] = res
                    done += 1
                    if done % 50 == 0:
                        save_ckpt(results)
                        print(f"      ... {done}/{len(todo)}")
        save_ckpt(results)

    print("[5/6] Assemble final rows")
    out_rows: list[dict] = []
    unmatched: list[dict] = []

    for rid, p in prep.items():
        r = p["yaml_rule"]
        # Catalog resolution
        cat_match_key = ""
        cat_match_orig = ""
        cat_tier = ""
        cat_conf = ""
        cat_reason = ""
        cat_ids = ""
        cat_fns = ""
        cat_service = ""
        cat_category = ""
        if p["cat_exact"]:
            e = p["cat_exact"][0]
            cat_match_key = e["match_key"]
            cat_match_orig = e["orig_rule_id"]
            cat_tier = "exact"
            cat_conf = "high"
            cat_reason = "rule_id exact match"
            cat_ids = e["compliance_ids"]
            cat_fns = e["compliance_fns"]
            cat_service = e["service"]
            cat_category = e["category"]
        else:
            ai = results.get(rid, {})
            chosen_key = (ai.get("catalog_match_key") or "").strip()
            if chosen_key:
                # Find the entry
                candidates_pool = p["cat_top"]
                chosen_entry = None
                for _, e in candidates_pool:
                    if e["match_key"] == chosen_key:
                        chosen_entry = e
                        break
                if chosen_entry:
                    # Determine tier from jaccard of chosen
                    jc = 0.0
                    for s, e in candidates_pool:
                        if e["match_key"] == chosen_key:
                            jc = s
                            break
                    cat_match_key = chosen_entry["match_key"]
                    cat_match_orig = chosen_entry["orig_rule_id"]
                    cat_tier = "fuzzy_strong_ai" if jc >= 0.5 else "ai_semantic"
                    cat_conf = ai.get("catalog_confidence", "")
                    cat_reason = ai.get("catalog_reasoning", "")
                    cat_ids = chosen_entry["compliance_ids"]
                    cat_fns = chosen_entry["compliance_fns"]
                    cat_service = chosen_entry["service"]
                    cat_category = chosen_entry["category"]
            else:
                cat_tier = "no_catalog_match"
                cat_conf = ai.get("catalog_confidence", "none") if ai else "none"
                cat_reason = ai.get("catalog_reasoning", "") if ai else ""

        # CIEM resolution
        ciem_rid = ""
        ciem_tier = ""
        ciem_conf = ""
        ciem_reason = ""
        ciem_ids = ""
        ciem_title = ""
        ciem_threat = ""
        ciem_frameworks = ""
        if p["ciem_exact"]:
            e = p["ciem_exact"][0]
            ciem_rid = e["rule_id"]
            ciem_tier = "exact"
            ciem_conf = "high"
            ciem_reason = "rule_id exact match"
            ciem_ids = e["compliance_ids"]
            ciem_title = e["title"]
            ciem_threat = e["threat_category"]
            ciem_frameworks = ";".join(e["compliance_frameworks_nested"].keys()) if isinstance(e.get("compliance_frameworks_nested"), dict) else ""
        else:
            ai = results.get(rid, {})
            chosen_rid = (ai.get("ciem_rule_id") or "").strip()
            if chosen_rid and chosen_rid in ciem_by_key:
                e = ciem_by_key[chosen_rid]
                jc = 0.0
                for s, ee in p["ciem_top"]:
                    if ee["rule_id"] == chosen_rid:
                        jc = s
                        break
                ciem_rid = chosen_rid
                ciem_tier = "fuzzy_strong_ai" if jc >= 0.5 else "ai_semantic"
                ciem_conf = ai.get("ciem_confidence", "")
                ciem_reason = ai.get("ciem_reasoning", "")
                ciem_ids = e["compliance_ids"]
                ciem_title = e["title"]
                ciem_threat = e["threat_category"]
                ciem_frameworks = ";".join(e["compliance_frameworks_nested"].keys()) if isinstance(e.get("compliance_frameworks_nested"), dict) else ""
            else:
                ciem_tier = "no_ciem_match"
                ciem_conf = ai.get("ciem_confidence", "none") if ai else "none"
                ciem_reason = ai.get("ciem_reasoning", "") if ai else ""

        coverage = "both" if cat_match_key and ciem_rid else ("catalog_only" if cat_match_key else ("ciem_only" if ciem_rid else "none"))
        if coverage == "none":
            unmatched.append(r)

        out_rows.append({
            "yaml_rule_id": rid,
            "yaml_service": r["yaml_service"],
            "yaml_resource_kind": r["yaml_resource_kind"],
            "domain": r["domain"],
            "severity": r["severity"],
            "scope": r["scope"],
            "assertion_id": r["assertion_id"],

            "catalog_tier": cat_tier,
            "catalog_confidence": cat_conf,
            "catalog_match_key": cat_match_key,
            "catalog_orig_rule_id": cat_match_orig,
            "catalog_service": cat_service,
            "catalog_category": cat_category,
            "catalog_reasoning": cat_reason,
            "catalog_compliance_ids": cat_ids,
            "catalog_compliance_fns": cat_fns,

            "ciem_tier": ciem_tier,
            "ciem_confidence": ciem_conf,
            "ciem_rule_id": ciem_rid,
            "ciem_title": ciem_title,
            "ciem_threat_category": ciem_threat,
            "ciem_frameworks": ciem_frameworks,
            "ciem_reasoning": ciem_reason,
            "ciem_compliance_ids": ciem_ids,

            "coverage": coverage,
        })

    print("[6/6] Writing outputs")
    cols = list(out_rows[0].keys())
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out_rows)
    un_cols = ["rule_id", "yaml_service", "yaml_resource_kind", "domain", "severity", "scope", "assertion_id"]
    with OUT_UNMATCHED.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=un_cols)
        w.writeheader()
        w.writerows(unmatched)

    cov_counts = Counter(r["coverage"] for r in out_rows)
    cat_tier_counts = Counter(r["catalog_tier"] for r in out_rows)
    ciem_tier_counts = Counter(r["ciem_tier"] for r in out_rows)
    cat_conf_counts = Counter(r["catalog_confidence"] for r in out_rows)
    ciem_conf_counts = Counter(r["ciem_confidence"] for r in out_rows)

    summary = {
        "model": args.model,
        "yaml_rules": len(yaml_rules),
        "ai_calls_made": len(results),
        "coverage": dict(cov_counts),
        "catalog_tier_counts": dict(cat_tier_counts),
        "ciem_tier_counts": dict(ciem_tier_counts),
        "catalog_confidence": dict(cat_conf_counts),
        "ciem_confidence": dict(ciem_conf_counts),
        "unmatched_rows": len(unmatched),
        "outputs": {"mapping": str(OUT_CSV), "unmatched": str(OUT_UNMATCHED), "checkpoint": str(CHECKPOINT)},
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
