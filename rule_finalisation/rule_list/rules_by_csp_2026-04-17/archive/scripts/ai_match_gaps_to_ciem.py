"""
AI semantic matching: 340 uncovered catalog rows → CIEM rules.

For each catalog row not covered by any config/CIEM rule, ask DeepSeek
whether any CIEM rule detects when that compliance requirement is violated.

Pre-filtering: top-20 CIEM candidates per catalog row via:
  - compliance-ID overlap (relaxed: Jaccard >= 0.05 OR shared >= 1)
  - token Jaccard on rule_id (>= 0.15)
  - service keyword match on title/description
  If <5 candidates remain, include top-20 by combined score from ALL CIEM rules.

Outputs:
  aws_gaps_ciem_ai_mapping.csv        one row per catalog gap rule
  aws_gaps_ciem_ai_checkpoint.json    resumable
  aws_gaps_ciem_ai_summary.json
"""
import argparse
import csv
import json
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from openai import OpenAI

csv.field_size_limit(sys.maxsize)

BASE         = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
MATRIX_CSV   = BASE / "aws_catalog_coverage_matrix.csv"
CIEM_JSON    = BASE / "aws_ciem_rules_consolidated.json"
OUT_CSV      = BASE / "aws_gaps_ciem_ai_mapping.csv"
CHECKPOINT   = BASE / "aws_gaps_ciem_ai_checkpoint.json"
OUT_SUMMARY  = BASE / "aws_gaps_ciem_ai_summary.json"

MODEL        = "deepseek-chat"
CONCURRENCY  = 10
CANDIDATES   = 20     # max CIEM candidates per catalog row
RETRY_LIMIT  = 3

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


def norm_tokens(rid: str) -> frozenset:
    parts = rid.lower().replace("-", "_").split(".")
    svc = parts[1] if len(parts) >= 2 and parts[0] == "aws" else (parts[0] if parts else "")
    tail = parts[2:] if len(parts) >= 2 and parts[0] == "aws" else parts[1:]
    toks = set()
    for p in tail:
        for t in p.split("_"):
            if not t or t in NOISE:
                continue
            t = SYN.get(t, t)
            if len(t) >= 4 and t.endswith("s") and not t.endswith("ss"):
                t = t[:-1]
            toks.add(t)
    return frozenset(toks)


def jac(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def parse_comp(raw: str) -> frozenset:
    if not raw:
        return frozenset()
    return frozenset(x.strip() for x in raw.split(";") if x.strip())


def service_tokens(text: str) -> set:
    return set(text.lower().replace("-", "_").replace(".", "_").split("_"))


def top_ciem_candidates(cat_row: dict, ciem_recs: list[dict]) -> list[dict]:
    cat_comp = parse_comp(cat_row.get("catalog_compliance_ids", ""))
    cat_tok  = norm_tokens(cat_row["catalog_rule_id"])
    cat_svc  = (cat_row.get("service", "") or "").lower()

    scored = []
    for c in ciem_recs:
        c_comp  = c["_comp"]
        c_tok   = c["_tok"]
        c_title = c.get("title", "").lower()
        c_desc  = c.get("description", "").lower()

        comp_j   = jac(cat_comp, c_comp)
        tok_j    = jac(cat_tok, c_tok)
        shared   = len(cat_comp & c_comp)
        svc_hit  = cat_svc and (cat_svc in c_title or cat_svc in c_desc or cat_svc in c.get("service","").lower())

        # inclusion signal
        if comp_j >= 0.05 or shared >= 1 or tok_j >= 0.15 or svc_hit:
            score = 0.5 * comp_j + 0.3 * tok_j + (0.2 if svc_hit else 0.0)
            scored.append((score, comp_j, tok_j, shared, c))

    scored.sort(key=lambda x: -x[0])
    if len(scored) < 5:
        # fallback: include all CIEM rules, sorted by combined score
        fallback = []
        for c in ciem_recs:
            comp_j = jac(cat_comp, c["_comp"])
            tok_j  = jac(cat_tok, c["_tok"])
            score  = 0.5 * comp_j + 0.3 * tok_j
            fallback.append((score, comp_j, tok_j, len(cat_comp & c["_comp"]), c))
        fallback.sort(key=lambda x: -x[0])
        scored = fallback

    return [x[4] for x in scored[:CANDIDATES]]


SYSTEM_PROMPT = """\
You are a cloud security expert helping map compliance requirements to detection rules for a CSPM platform.
Config rules check static asset configuration. CIEM rules detect security events via CloudTrail/logs.
A CIEM rule "covers" a catalog compliance check if it detects the same security concern:
  e.g., catalog="MFA must be enabled" is covered by ciem="login without MFA detected"
  e.g., catalog="S3 bucket must block public access" is covered by ciem="S3 public access block disabled event"
Only return a match if you are confident the CIEM rule directly addresses the same security control."""


def build_user_prompt(cat_row: dict, candidates: list[dict]) -> str:
    rid   = cat_row["catalog_rule_id"]
    svc   = cat_row.get("service", "")
    cat   = cat_row.get("category", "")
    comp  = cat_row.get("catalog_compliance_ids", "")[:300]

    lines = [
        "CATALOG RULE (no config scanner covers it yet):",
        f"  rule_id:     {rid}",
        f"  service:     {svc}",
        f"  category:    {cat}",
        f"  compliance:  {comp}",
        "",
        f"TOP {len(candidates)} CIEM CANDIDATES:",
    ]
    for i, c in enumerate(candidates, 1):
        lines.append(
            f"  {i:2d}. {c['rule_id']}"
            f"\n      title: {c.get('title','')[:100]}"
            f"\n      threat: {c.get('threat_category','')}"
            f"\n      compliance: {c.get('aws_mapped_compliance_ids','')[:120]}"
        )

    lines += [
        "",
        "Does any CIEM candidate detect when this catalog compliance requirement is violated?",
        'Return ONLY valid JSON (no markdown, no extra text):',
        '{"ciem_rule_id": "<rule_id or empty string>", "confidence": "high|medium|low|none", "reasoning": "<one sentence>"}',
    ]
    return "\n".join(lines)


def call_ai(client: OpenAI, cat_row: dict, candidates: list[dict]) -> dict:
    prompt = build_user_prompt(cat_row, candidates)
    for attempt in range(RETRY_LIMIT):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.1,
                max_tokens=200,
            )
            raw = resp.choices[0].message.content.strip()
            # strip markdown code fences if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            parsed = json.loads(raw)
            return {
                "ciem_rule_id":  (parsed.get("ciem_rule_id") or "").strip(),
                "confidence":    (parsed.get("confidence") or "none").lower().strip(),
                "reasoning":     (parsed.get("reasoning") or "").strip()[:300],
                "error":         "",
            }
        except Exception as e:
            if attempt < RETRY_LIMIT - 1:
                time.sleep(2 ** attempt)
            else:
                return {"ciem_rule_id": "", "confidence": "none", "reasoning": "", "error": str(e)[:200]}
    return {"ciem_rule_id": "", "confidence": "none", "reasoning": "", "error": "max retries"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    api_key = (os.getenv("DEEPSEEK_API_KEY") or "").strip()
    if not api_key and not args.dry_run:
        print("ERROR: DEEPSEEK_API_KEY not set", file=sys.stderr)
        sys.exit(2)

    client = OpenAI(api_key=api_key or "dry", base_url="https://api.deepseek.com") if not args.dry_run else None

    # Load CIEM
    print("[1/5] Load CIEM rules")
    ciem_recs = json.loads(CIEM_JSON.read_text())
    for r in ciem_recs:
        r["_comp"] = parse_comp(r.get("aws_mapped_compliance_ids", ""))
        r["_tok"]  = norm_tokens(r.get("rule_id", ""))
    ciem_by_id = {r["rule_id"]: r for r in ciem_recs}
    print(f"      {len(ciem_recs)} CIEM rules")

    # Load gap rows
    print("[2/5] Load gap rows from coverage matrix")
    gap_rows = []
    with MATRIX_CSV.open() as f:
        for row in csv.DictReader(f):
            if row.get("coverage_status") == "not_covered":
                gap_rows.append(row)
    print(f"      {len(gap_rows)} gap rows")

    if args.limit:
        gap_rows = gap_rows[:args.limit]
        print(f"      (limited to {args.limit})")

    # Resume from checkpoint
    checkpoint: dict = {}
    if CHECKPOINT.exists():
        checkpoint = json.loads(CHECKPOINT.read_text())
        print(f"      Resuming — {len(checkpoint)} already done")

    todo = [r for r in gap_rows if r["catalog_rule_id"] not in checkpoint]
    print(f"      Remaining: {len(todo)}")

    if args.dry_run:
        print("[DRY RUN] Showing first 3 prompts only")
        for row in todo[:3]:
            cands = top_ciem_candidates(row, ciem_recs)
            print(f"\n=== {row['catalog_rule_id']} ({len(cands)} candidates) ===")
            print(build_user_prompt(row, cands)[:800])
        return

    # AI matching
    print(f"[3/5] AI matching ({len(todo)} calls, concurrency={CONCURRENCY})")
    done = 0
    errors = 0

    def process(row):
        cands = top_ciem_candidates(row, ciem_recs)
        result = call_ai(client, row, cands)
        result["candidate_count"] = len(cands)
        return row["catalog_rule_id"], result

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futures = {ex.submit(process, row): row for row in todo}
        for fut in as_completed(futures):
            rid, result = fut.result()
            checkpoint[rid] = result
            done += 1
            if result.get("error"):
                errors += 1
            if done % 25 == 0 or done == len(todo):
                CHECKPOINT.write_text(json.dumps(checkpoint, indent=2))
                print(f"      [{done}/{len(todo)}]  errors={errors}", flush=True)

    CHECKPOINT.write_text(json.dumps(checkpoint, indent=2))

    # Write CSV
    print("[4/5] Write output CSV")
    out_cols = [
        "catalog_rule_id", "service", "category", "provider_service",
        "catalog_compliance_ids", "has_compliance_ids",
        "ciem_rule_id", "confidence", "reasoning",
        "ciem_title", "ciem_threat_category", "ciem_service", "ciem_compliance_ids",
        "candidate_count", "error",
    ]
    out_rows = []
    for row in gap_rows:
        rid = row["catalog_rule_id"]
        res = checkpoint.get(rid, {})
        ciem_id = res.get("ciem_rule_id", "")
        ciem_rec = ciem_by_id.get(ciem_id, {})
        out_rows.append({
            "catalog_rule_id":       rid,
            "service":               row.get("service", ""),
            "category":              row.get("category", ""),
            "provider_service":      row.get("provider_service", ""),
            "catalog_compliance_ids":row.get("catalog_compliance_ids", ""),
            "has_compliance_ids":    row.get("has_compliance_ids", ""),
            "ciem_rule_id":          ciem_id,
            "confidence":            res.get("confidence", ""),
            "reasoning":             res.get("reasoning", ""),
            "ciem_title":            ciem_rec.get("title", "")[:120],
            "ciem_threat_category":  ciem_rec.get("threat_category", ""),
            "ciem_service":          ciem_rec.get("service", ""),
            "ciem_compliance_ids":   ciem_rec.get("aws_mapped_compliance_ids", "")[:200],
            "candidate_count":       res.get("candidate_count", 0),
            "error":                 res.get("error", ""),
        })

    # Sort: high confidence first
    ORDER = {"high": 0, "medium": 1, "low": 2, "none": 3, "": 4}
    out_rows.sort(key=lambda x: (ORDER.get(x["confidence"], 9), x["service"]))

    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_cols)
        w.writeheader()
        w.writerows(out_rows)

    print("[5/5] Summary")
    from collections import Counter
    conf_counts = Counter(r["confidence"] for r in out_rows)
    newly_covered = sum(1 for r in out_rows if r["confidence"] in {"high", "medium"})
    summary = {
        "gap_rows_processed": len(out_rows),
        "newly_covered_by_ciem_ai": newly_covered,
        "still_not_covered": len(out_rows) - newly_covered,
        "final_total_coverage_estimate": {
            "previously_covered": 1704,
            "newly_covered": newly_covered,
            "total": 1704 + newly_covered,
            "total_catalog": 2044,
        },
        "by_confidence": dict(conf_counts),
        "errors": errors,
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
