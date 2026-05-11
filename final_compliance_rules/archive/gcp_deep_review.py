"""
Deep review of GCP rejected check names to find matches missed by the strict pipeline.

Two-pass approach:
  1. Classify rejected checks:
     - WRONG_CSP:  check name contains AWS/Azure-specific terms (alb, ebs, dynamodb,
                    cloudwatch, cloudfront, aws_, azure_, etc.) → data quality issue
     - RETRY:      legitimate GCP check — retry matching with wider candidate pool
  2. For RETRY, expand search: show top 10 candidates (across ALL services in catalog)
     and let AI re-evaluate with service+description context.
"""
import csv
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    import sys
    print("pip install openai", file=sys.stderr); sys.exit(1)

BASE = Path("/Users/apple/Desktop/compliance_Database/final_compliance_rules")
GCP_CHECK_CSV = BASE / "rule_catalogs/gcp_rule_check.csv"
GCP_CIEM_CSV = BASE / "rule_catalogs/gcp_rule_ciem.csv"
MAPPING_CSV = BASE / "rule_mapping/gcp_check_to_rule.csv"
OUT_CSV = BASE / "rule_mapping/gcp_deep_review.csv"

API_KEY = os.getenv("DEEPSEEK_API_KEY") or "sk-3d7acb8511ad4da18e8b0c89733f472b"
MODEL = "deepseek-chat"
CONCURRENCY = 10
TOP_N = 10  # widened candidate pool

# Tokens indicating wrong-CSP contamination
WRONG_CSP_MARKERS = {
    "alb", "elb", "ebs", "elastic_ip", "dynamodb", "cloudfront", "guardduty",
    "cloudwatch", "cloudtrail", "awslambda", "emr", "eks", "rds", "s3_", "sns_",
    "sqs_", "ec2_", "iam_user_mfa", "redshift", "neptune", "codepipeline",
    "kinesis", "elasticbeanstalk", "glue_", "appflow", "workmail", "chime",
    "aurora", "aws_", "azure_", "adfs", "entra_", "active_directory_",
}


def is_wrong_csp(name: str) -> list[str]:
    """Return list of wrong-CSP markers found in the check name."""
    low = name.lower()
    return sorted({m for m in WRONG_CSP_MARKERS if m in low})


# ── Load GCP catalog (check + ciem) ───────────────────────────────────────
catalog = []
for fp in [GCP_CHECK_CSV, GCP_CIEM_CSV]:
    with open(fp) as f:
        for row in csv.DictReader(f):
            catalog.append(row)
print(f"GCP catalog rules: {len(catalog)}")


NOISE = {"the", "a", "an", "for", "with", "and", "or", "is", "to", "of", "in",
         "on", "by", "that", "not", "are", "all", "have", "must", "only", "no",
         "new", "your", "be", "use", "using", "from", "check", "configured",
         "enabled", "resource"}


def tokens(s: str) -> set[str]:
    return {t.lower() for t in re.split(r"[._\-\s/]+", s) if len(t) > 1} - NOISE


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def top_candidates(check_name: str, n: int = TOP_N):
    ct = tokens(check_name)
    if not ct:
        return []
    scored = []
    for r in catalog:
        score = jaccard(ct, tokens(r["rule_id"]))
        if score > 0:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    return scored[:n]


# ── Load rejected GCP checks ──────────────────────────────────────────────
rejected = []
with open(MAPPING_CSV) as f:
    for row in csv.DictReader(f):
        if row["method"] in ("ai_rejected", "weak_match", "no_candidates"):
            rejected.append(row["check_name"])

print(f"GCP rejected checks: {len(rejected)}")


# ── Classify ──────────────────────────────────────────────────────────────
wrong_csp_items = []
retry_items = []
for c in rejected:
    markers = is_wrong_csp(c)
    if markers:
        wrong_csp_items.append((c, markers))
    else:
        retry_items.append(c)

print(f"  Wrong-CSP (data quality): {len(wrong_csp_items)}")
print(f"  Legitimate GCP retry:     {len(retry_items)}")


# ── AI review on retry items ──────────────────────────────────────────────
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

SYSTEM_PROMPT = """You are a cloud security expert mapping compliance check names to GCP catalog rule IDs.
The check name describes a security control. You must find the catalog rule_id that enforces the SAME control.
Rules are from a real catalog — if a candidate is clearly about the same thing (even with different wording), accept it.
Be more LENIENT than strict here — partial-but-clear matches should be returned.

Decision: HIGH = exact same control; MEDIUM = same concept/different phrasing; LOW = related but not same; NONE = no match."""


def build_prompt(check_name: str, cands):
    lines = [
        f"COMPLIANCE CHECK NAME: {check_name}",
        "",
        f"TOP {len(cands)} GCP CATALOG CANDIDATES:",
    ]
    for i, (score, r) in enumerate(cands, 1):
        title = r.get("title", "")[:120] or ""
        desc = r.get("description", "")[:150] or ""
        lines.append(f"  {i}. [score={score:.2f}] {r['rule_id']}")
        if title:
            lines.append(f"       title: {title}")
        if desc:
            lines.append(f"       desc:  {desc}")
    lines += [
        "",
        "Which candidate enforces the SAME control as the check name?",
        "Be lenient — same concept with different wording counts.",
        'Return JSON only: {"rule_ids": ["<rule_id>", ...], "confidence": "high|medium|low|none", "reasoning": "<one sentence>"}',
    ]
    return "\n".join(lines)


def ai_one(check_name):
    cands = top_candidates(check_name, TOP_N)
    if not cands:
        return check_name, {"rule_id": "", "confidence": "none",
                             "reasoning": "no candidates"}
    prompt = build_prompt(check_name, cands)
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=250,
            )
            raw = (resp.choices[0].message.content or "").strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()
            parsed = json.loads(raw)
            rids = parsed.get("rule_ids", [])
            if isinstance(rids, str):
                rids = [rids]
            return check_name, {
                "rule_id": ";".join(r for r in rids if r),
                "confidence": (parsed.get("confidence") or "none").lower(),
                "reasoning": (parsed.get("reasoning") or "")[:250],
            }
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return check_name, {"rule_id": "", "confidence": "none",
                                     "reasoning": f"err: {e}"[:200]}


results = {}
print(f"\nRunning AI deep review on {len(retry_items)} legitimate GCP checks…")
with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
    futures = [ex.submit(ai_one, c) for c in retry_items]
    done = 0
    for fut in as_completed(futures):
        name, r = fut.result()
        results[name] = r
        done += 1
        if done % 30 == 0:
            print(f"  progress: {done}/{len(retry_items)}")


# ── Save results ─────────────────────────────────────────────────────────
with open(OUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["check_name", "category",
                                             "matched_rule_ids", "confidence",
                                             "reasoning"])
    writer.writeheader()
    for name, markers in wrong_csp_items:
        writer.writerow({
            "check_name": name,
            "category": f"wrong_csp[{','.join(markers)}]",
            "matched_rule_ids": "",
            "confidence": "",
            "reasoning": "check name contains non-GCP service markers",
        })
    for name in retry_items:
        r = results.get(name, {})
        writer.writerow({
            "check_name": name,
            "category": "deep_review",
            "matched_rule_ids": r.get("rule_id", ""),
            "confidence": r.get("confidence", "none"),
            "reasoning": r.get("reasoning", ""),
        })


# ── Summary ──────────────────────────────────────────────────────────────
from collections import Counter
newly_matched = [n for n in retry_items if results.get(n, {}).get("rule_id")]
by_conf = Counter(results[n]["confidence"] for n in newly_matched)
print(f"\n═══════ DEEP REVIEW RESULTS ═══════")
print(f"  Wrong-CSP (need to drop):   {len(wrong_csp_items)}")
print(f"  Retried:                    {len(retry_items)}")
print(f"  Newly matched:              {len(newly_matched)}")
print(f"  Still unmatched:            {len(retry_items) - len(newly_matched)}")
print(f"  Confidence breakdown of new matches: {dict(by_conf)}")
print(f"\nOutput: {OUT_CSV}")

# Show some new matches for spot-checking
print(f"\nSample NEW matches found:")
for n in newly_matched[:10]:
    r = results[n]
    print(f"  [{r['confidence']:>6}] {n}")
    print(f"           → {r['rule_id']}")
