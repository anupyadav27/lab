"""
Tier 3 semantic mapping via LLM. Runs AFTER Tier 2.

Input:  aws_config_rules_still_unmapped.csv (563 YAML rules Tier 2 couldn't cover)
        aws_rules.csv                         (catalog of compliance-tagged rules)

For each unmapped YAML rule:
  1. Build a candidate pool of top-K aws_rules.csv entries (Jaccard, same service first).
  2. Ask the LLM to pick the best match from the pool (or null), with confidence + reason.
  3. Write the chosen mapping + the reasoning for human review.

Outputs:
  aws_config_to_compliance_mapping_tier3_semantic.csv   one row per YAML rule with AI choice
  aws_config_rules_final_unmapped.csv                    YAML rules LLM said "none" for
  aws_mapping_summary_tier3.json
  aws_mapping_tier3_checkpoint.json                      resumable state

CLI:
  --limit N        Process only first N (dry-run)
  --provider P     openai | deepseek  (default: openai)
  --model NAME     Model id. Defaults: gpt-4o-mini (openai), deepseek-chat (deepseek)
  --concurrency K  Parallel LLM calls (default: 8)
  --resume         Resume from checkpoint, skipping already-done rule_ids

Env vars used:
  OPENAI_API_KEY       for --provider openai
  DEEPSEEK_API_KEY     for --provider deepseek
"""

import argparse
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
TIER2_UNMAPPED = BASE / "aws_config_rules_still_unmapped.csv"

OUT_CSV = BASE / "aws_config_to_compliance_mapping_tier3_semantic.csv"
OUT_FINAL_UNMAPPED = BASE / "aws_config_rules_final_unmapped.csv"
OUT_SUMMARY = BASE / "aws_mapping_summary_tier3.json"
CHECKPOINT = BASE / "aws_mapping_tier3_checkpoint.json"

TOP_K = 15

# YAML service token -> catalog service prefix(es). Keys are already normalized
# (hyphens -> underscores, lowercase). When a key is present the candidate pool
# is widened to any catalog rule_id that starts with `aws.<alias>.` in addition
# to same-service matches.
SERVICE_ALIASES = {
    "acm_pca": ["acm.private_ca"],
    "apigateway": ["api_gateway", "api_gatewayv2", "apigateway", "apigatewayv2"],
    "api_gateway": ["apigateway", "api_gatewayv2", "apigatewayv2"],
    "apigatewayv2": ["api_gatewayv2", "api_gateway"],
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

NOISE_TOKENS = {"aws", "configured", "configuration", "resource"}
SYNONYMS = {
    "logging": "log", "logs": "log",
    "encrypted": "encryption", "encrypting": "encryption",
    "policies": "policy", "keys": "key", "accounts": "account",
    "users": "user", "roles": "role", "groups": "group",
    "permissions": "permission", "instances": "instance",
    "buckets": "bucket", "clusters": "cluster", "volumes": "volume",
    "snapshots": "snapshot",
    "rotation": "rotate", "rotated": "rotate", "rotating": "rotate",
    "restricted": "restrict", "restricting": "restrict",
    "enforced": "enforce", "enforcing": "enforce",
    "required": "require", "requires": "require",
    "disabled": "disable",
}

csv.field_size_limit(sys.maxsize)


def normalize(rule_id: str) -> tuple[str, frozenset[str]]:
    parts = rule_id.lower().replace("-", "_").split(".")
    if len(parts) < 2:
        return "", frozenset()
    service = parts[1] if parts[0] == "aws" else parts[0]
    tail = parts[2:] if parts[0] == "aws" else parts[1:]
    toks = set()
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
    return len(a & b) / len(a | b)


def load_yaml_rules(path: Path) -> dict[str, dict]:
    with path.open() as f:
        data = yaml.safe_load(f) or {}
    out: dict[str, dict] = {}
    for service, rmap in data.items():
        if not isinstance(rmap, dict):
            continue
        for rk, lst in rmap.items():
            if not isinstance(lst, list):
                continue
            for a in lst:
                if isinstance(a, dict) and "rule_id" in a:
                    out[a["rule_id"]] = {
                        "yaml_service": service,
                        "yaml_resource_kind": rk,
                        "assertion_id": a.get("assertion_id", ""),
                        "rule_id": a["rule_id"],
                        "scope": a.get("scope", ""),
                        "domain": a.get("domain", ""),
                        "severity": a.get("severity", ""),
                    }
    return out


def load_unmapped_ids(path: Path) -> list[str]:
    with path.open() as f:
        return [row["rule_id"] for row in csv.DictReader(f)]


def load_catalog(path: Path) -> tuple[list[dict], dict[str, list[dict]]]:
    rows: list[dict] = []
    by_service: dict[str, list[dict]] = defaultdict(list)
    with path.open() as f:
        for row in csv.DictReader(f):
            rid = (row.get("rule_id") or "").strip()
            if not rid:
                continue
            svc, toks = normalize(rid)
            row["_svc"] = svc
            row["_toks"] = toks
            rows.append(row)
            by_service[svc].append(row)
    return rows, by_service


def pick_candidates(yaml_rule: dict, by_service, all_rows, k: int = TOP_K) -> list[tuple[float, dict]]:
    svc, toks = normalize(yaml_rule["rule_id"])
    pool = list(by_service.get(svc, []))

    # Widen via service aliases (e.g. acm_pca -> acm.private_ca)
    for alias in SERVICE_ALIASES.get(svc, []):
        alias_root = alias.split(".")[0]
        for row in by_service.get(alias_root, []):
            rid = (row.get("rule_id") or "").lower()
            if rid.startswith(f"aws.{alias}.") or rid.startswith(f"aws.{alias_root}."):
                pool.append(row)

    # Dedupe pool
    seen = set()
    unique_pool = []
    for r in pool:
        rid = r.get("rule_id", "")
        if rid and rid not in seen:
            seen.add(rid)
            unique_pool.append(r)
    pool = unique_pool

    scored = [(jaccard(toks, r["_toks"]), r) for r in pool]
    scored.sort(key=lambda x: -x[0])
    top = scored[:k]
    # Final fallback: nothing useful in same/alias service -> widen to all
    if not top or top[0][0] == 0.0:
        scored_all = [(jaccard(toks, r["_toks"]), r) for r in all_rows]
        scored_all.sort(key=lambda x: -x[0])
        top = scored_all[:k]
    return top


SYSTEM_PROMPT = """You are an AWS compliance expert helping match scanner assertions to a catalog of compliance-tagged rules.

You will receive one YAML config rule and a short list of candidate catalog rules (same AWS service). Pick the single best semantic match from the candidates, or return null only if NONE of the candidates actually covers the same control.

Output ONLY a JSON object with this exact shape (always include reasoning):
{
  "match_rule_id": "<chosen candidate rule_id or null>",
  "confidence": "high" | "medium" | "low" | "none",
  "reasoning": "<one short sentence explaining the choice>"
}

Confidence guide:
- high:   candidate asserts the same technical control on the same resource (synonyms OK, e.g. "logging_enabled" == "logs_enabled").
- medium: covers the same intent with slightly different resource granularity or wording.
- low:    related but partial overlap — still record it for human review.
- none:   genuinely unrelated; the catalog does not cover this control.

Reasoning MUST be non-empty whenever there are candidates. A low-confidence match is useful for reviewers; prefer it to "none" when there is at least a partial overlap."""


def build_user_prompt(yaml_rule: dict, candidates: list[tuple[float, dict]]) -> str:
    cand_lines = []
    for score, row in candidates:
        cand_lines.append(
            f"- rule_id: {row.get('rule_id','')} "
            f"| service: {row.get('service','')} "
            f"| category: {row.get('category','')} "
            f"| jaccard: {score:.2f}"
        )
    cands = "\n".join(cand_lines) if cand_lines else "(no candidates)"
    return (
        f"YAML config rule to classify:\n"
        f"  rule_id:       {yaml_rule['rule_id']}\n"
        f"  assertion_id:  {yaml_rule['assertion_id']}\n"
        f"  domain:        {yaml_rule['domain']}\n"
        f"  scope:         {yaml_rule['scope']}\n"
        f"  severity:      {yaml_rule.get('severity','')}\n"
        f"\nCandidate compliance-catalog rules (same service first):\n"
        f"{cands}\n"
    )


def classify(client: OpenAI, model: str, yaml_rule: dict, candidates) -> dict:
    prompt = build_user_prompt(yaml_rule, candidates)
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        raw = resp.choices[0].message.content or "{}"
        parsed = json.loads(raw)
        return {
            "match_rule_id": parsed.get("match_rule_id") or "",
            "confidence": (parsed.get("confidence") or "none").lower(),
            "reasoning": parsed.get("reasoning", "")[:500],
            "error": "",
        }
    except Exception as e:
        return {"match_rule_id": "", "confidence": "none", "reasoning": "", "error": str(e)[:300]}


def load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text())
    return {}


def save_checkpoint(state: dict) -> None:
    CHECKPOINT.write_text(json.dumps(state, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--provider", choices=["openai", "deepseek"], default="openai")
    ap.add_argument("--model", default=None)
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    if args.provider == "deepseek":
        api_key = (os.getenv("DEEPSEEK_API_KEY") or "").strip()
        env_name = "DEEPSEEK_API_KEY"
        base_url = "https://api.deepseek.com"
        default_model = "deepseek-chat"
    else:
        api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
        env_name = "OPENAI_API_KEY"
        base_url = None
        default_model = "gpt-4o-mini"
    if not api_key:
        print(f"ERROR: {env_name} not set", file=sys.stderr)
        sys.exit(2)
    model = args.model or default_model
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    print(f"[1/5] Load YAML rules")
    yaml_idx = load_yaml_rules(YAML_PATH)

    unmapped_ids = load_unmapped_ids(TIER2_UNMAPPED)
    if args.limit:
        unmapped_ids = unmapped_ids[: args.limit]
    print(f"      -> processing {len(unmapped_ids)} still-unmapped YAML rules")

    print(f"[2/5] Load catalog")
    catalog_rows, by_service = load_catalog(RULES_CSV)
    print(f"      -> {len(catalog_rows)} catalog rows")

    state = load_checkpoint() if args.resume else {}
    processed = state.get("results", {})
    remaining = [rid for rid in unmapped_ids if rid not in processed]
    print(f"[3/5] {len(processed)} already processed (resume), {len(remaining)} remaining")

    lock = Lock()

    def worker(rule_id: str) -> tuple[str, dict]:
        yaml_rule = yaml_idx.get(rule_id)
        if not yaml_rule:
            return rule_id, {"match_rule_id": "", "confidence": "none",
                             "reasoning": "yaml rule not found", "error": "missing",
                             "candidates": []}
        cands = pick_candidates(yaml_rule, by_service, catalog_rows)
        result = classify(client, model, yaml_rule, cands)
        result["candidates"] = [
            {"rule_id": r.get("rule_id",""), "jaccard": round(s, 3)} for s, r in cands
        ]
        return rule_id, result

    print(f"[4/5] Calling {model} ({args.concurrency} parallel) ...")
    done = 0
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = {ex.submit(worker, rid): rid for rid in remaining}
        for fut in as_completed(futures):
            rid, res = fut.result()
            with lock:
                processed[rid] = res
                done += 1
                if done % 25 == 0:
                    save_checkpoint({"results": processed})
                    print(f"      ... {done}/{len(remaining)}")
    save_checkpoint({"results": processed})

    print(f"[5/5] Writing outputs")
    # Build index of catalog rows by rule_id for lookup
    cat_by_id: dict[str, dict] = {}
    for row in catalog_rows:
        cat_by_id[(row.get("rule_id") or "").strip()] = row

    out_cols = [
        "yaml_rule_id", "yaml_service", "yaml_resource_kind", "domain", "severity",
        "scope", "assertion_id",
        "ai_match_rule_id", "ai_confidence", "ai_reasoning",
        "csv_service", "csv_category", "csv_provider_service",
        "aws_mapped_compliance_functions", "aws_mapped_compliance_ids",
        "top_candidate_pool",
        "review_decision",
    ]
    mapped_rows = []
    final_unmapped_rows = []
    conf_counts: dict[str, int] = defaultdict(int)
    error_count = 0
    for rid in unmapped_ids:
        res = processed.get(rid)
        if not res:
            continue
        yaml_rule = yaml_idx.get(rid, {})
        if res.get("error"):
            error_count += 1
        conf = res.get("confidence", "none")
        conf_counts[conf] += 1
        match_id = (res.get("match_rule_id") or "").strip()
        cat_row = cat_by_id.get(match_id, {}) if match_id else {}
        pool_str = "; ".join(f"{c['rule_id']}({c['jaccard']})" for c in res.get("candidates", [])[:5])

        row = {
            "yaml_rule_id": rid,
            "yaml_service": yaml_rule.get("yaml_service", ""),
            "yaml_resource_kind": yaml_rule.get("yaml_resource_kind", ""),
            "domain": yaml_rule.get("domain", ""),
            "severity": yaml_rule.get("severity", ""),
            "scope": yaml_rule.get("scope", ""),
            "assertion_id": yaml_rule.get("assertion_id", ""),
            "ai_match_rule_id": match_id,
            "ai_confidence": conf,
            "ai_reasoning": res.get("reasoning", ""),
            "csv_service": cat_row.get("service", ""),
            "csv_category": cat_row.get("category", ""),
            "csv_provider_service": cat_row.get("provider_service", ""),
            "aws_mapped_compliance_functions": cat_row.get("aws_mapped_compliance_functions", ""),
            "aws_mapped_compliance_ids": cat_row.get("aws_mapped_compliance_ids", ""),
            "top_candidate_pool": pool_str,
            "review_decision": "",
        }
        if match_id and conf in ("high", "medium", "low"):
            mapped_rows.append(row)
        else:
            final_unmapped_rows.append(row)

    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_cols)
        w.writeheader()
        w.writerows(mapped_rows)

    final_unmapped_cols = [
        "yaml_rule_id", "yaml_service", "yaml_resource_kind", "domain", "severity",
        "scope", "assertion_id", "ai_confidence", "ai_reasoning", "top_candidate_pool",
    ]
    with OUT_FINAL_UNMAPPED.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=final_unmapped_cols)
        w.writeheader()
        for r in final_unmapped_rows:
            w.writerow({k: r.get(k, "") for k in final_unmapped_cols})

    summary = {
        "inputs": {
            "tier2_still_unmapped": str(TIER2_UNMAPPED),
            "yaml": str(YAML_PATH),
            "aws_rules_csv": str(RULES_CSV),
        },
        "outputs": {
            "mapped_csv": str(OUT_CSV),
            "final_unmapped_csv": str(OUT_FINAL_UNMAPPED),
            "checkpoint": str(CHECKPOINT),
        },
        "provider": args.provider,
        "model": model,
        "processed": len(processed),
        "confidence_breakdown": dict(conf_counts),
        "mapped_rows": len(mapped_rows),
        "final_unmapped_rows": len(final_unmapped_rows),
        "api_errors": error_count,
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
