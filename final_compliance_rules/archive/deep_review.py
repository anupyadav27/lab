"""
Generic deep review for any CSP to find missed check→rule matches.

Usage: python deep_review.py <csp>    (csp = aws|azure|gcp|oracle|ibm|alicloud|k8s)

Two-pass approach:
  1. Classify rejected checks — filter out wrong-CSP data-quality cases
  2. AI review with widened candidate pool + catalog titles/descriptions
"""
import csv
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("pip install openai", file=sys.stderr); sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python deep_review.py <csp>")
    sys.exit(1)
CSP = sys.argv[1].lower()
VALID = {"aws", "azure", "gcp", "oracle", "ibm", "alicloud", "k8s"}
if CSP not in VALID:
    print(f"Invalid CSP. Choose from: {VALID}"); sys.exit(1)

BASE = Path("/Users/apple/Desktop/compliance_Database/final_compliance_rules")
CSP_TO_CATALOG = {"aws": "aws", "azure": "azure", "gcp": "gcp",
                   "oracle": "oci", "ibm": "ibm", "alicloud": "alicloud", "k8s": "k8s"}
CATALOG_PREFIX = CSP_TO_CATALOG[CSP]

CHECK_CSV = BASE / f"rule_catalogs/{CATALOG_PREFIX}_rule_check.csv"
CIEM_CSV = BASE / f"rule_catalogs/{CATALOG_PREFIX}_rule_ciem.csv"
MAPPING_CSV = BASE / f"rule_mapping/{CSP}_check_to_rule.csv"
OUT_CSV = BASE / f"rule_mapping/{CSP}_deep_review.csv"

API_KEY = os.getenv("DEEPSEEK_API_KEY") or "sk-3d7acb8511ad4da18e8b0c89733f472b"
MODEL = "deepseek-chat"
CONCURRENCY = 10
TOP_N = 10

# Per-CSP: tokens from OTHER CSPs that indicate wrong-CSP contamination
WRONG_CSP_MARKERS = {
    "gcp": {"alb","elb","ebs","elastic_ip","dynamodb","cloudfront","guardduty",
             "cloudwatch","cloudtrail","awslambda","emr","rds","aurora",
             "aws_","azure_","adfs","entra_","active_directory_"},
    "ibm": {"alb","elb","ebs","dynamodb","cloudfront","guardduty","cloudwatch",
             "cloudtrail","awslambda","emr","rds","aurora","aws_","azure_",
             "adfs","entra_","gcp_","s3_bucket","ec2_","elasticache",
             "eks","elb_v2","cloudhsm","kinesis","stepfunctions"},
    "alicloud": {"alb","elb","ebs","dynamodb","cloudfront","guardduty","cloudwatch",
                  "cloudtrail","awslambda","emr","rds","aurora","aws_","azure_",
                  "adfs","entra_","gcp_","s3_bucket","ec2_","elasticache",
                  "elasticsearch","kinesis"},
    "oracle": {"alb","elb","ebs","dynamodb","cloudfront","guardduty","cloudwatch",
                "cloudtrail","awslambda","emr","rds","aurora","aws_","azure_",
                "adfs","entra_","gcp_","s3_bucket","ec2_","elasticache",
                "elasticsearch","kinesis","lambda","redshift","fargate","glue_"},
    "aws": {"azure_","gcp_","oci_","ibm_","alicloud_","k8s_","entra_","active_directory_"},
    "azure": {"aws_","gcp_","oci_","ibm_","alicloud_","k8s_","lambda_","s3_","dynamodb","cloudfront","guardduty","cloudwatch","cloudtrail","awslambda","emr","rds","aurora","ec2_"},
    "k8s": {"aws_","azure_","gcp_","oci_","ibm_","alicloud_"},
}
MARKERS = WRONG_CSP_MARKERS.get(CSP, set())


def is_wrong_csp(name: str) -> list[str]:
    low = name.lower()
    return sorted({m for m in MARKERS if m in low})


# ── Load catalog ───────────────────────────────────────────────────────────
catalog = []
for fp in [CHECK_CSV, CIEM_CSV]:
    if not fp.exists():
        continue
    with open(fp) as f:
        for row in csv.DictReader(f):
            catalog.append(row)
print(f"{CSP.upper()} catalog rules: {len(catalog)}")


NOISE = {"the","a","an","for","with","and","or","is","to","of","in","on","by",
         "that","not","are","all","have","must","only","no","new","your","be",
         "use","using","from","check","configured","enabled","resource"}


def tokens(s: str) -> set[str]:
    return {t.lower() for t in re.split(r"[._\-\s/]+", s) if len(t) > 1} - NOISE


def jaccard(a, b):
    return (len(a & b) / len(a | b)) if (a and b) else 0.0


def top_candidates(check_name, n=TOP_N):
    ct = tokens(check_name)
    if not ct: return []
    scored = [(jaccard(ct, tokens(r["rule_id"])), r) for r in catalog]
    scored = [s for s in scored if s[0] > 0]
    scored.sort(key=lambda x: -x[0])
    return scored[:n]


# ── Load rejected checks ──────────────────────────────────────────────────
rejected = []
with open(MAPPING_CSV) as f:
    for row in csv.DictReader(f):
        if row["method"] in ("ai_rejected","weak_match","no_candidates"):
            rejected.append(row["check_name"])
print(f"Rejected checks: {len(rejected)}")


# ── Classify ──────────────────────────────────────────────────────────────
wrong_csp_items = []
retry_items = []
for c in rejected:
    m = is_wrong_csp(c)
    if m:
        wrong_csp_items.append((c, m))
    else:
        retry_items.append(c)
print(f"  Wrong-CSP: {len(wrong_csp_items)}")
print(f"  Retry:     {len(retry_items)}")


# ── AI review ─────────────────────────────────────────────────────────────
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

SYSTEM_PROMPT = f"""You are a cloud security expert mapping compliance check names to {CSP.upper()} catalog rule IDs.
The check name describes a security control. Find the catalog rule_id that enforces the SAME control.
Be LENIENT — if a candidate is clearly about the same thing (even with different wording), accept it.

Decision: HIGH = exact same control; MEDIUM = same concept/different phrasing; LOW = related but not same; NONE = no match."""


def build_prompt(name, cands):
    lines = [f"COMPLIANCE CHECK NAME: {name}", "",
              f"TOP {len(cands)} {CSP.upper()} CATALOG CANDIDATES:"]
    for i, (score, r) in enumerate(cands, 1):
        title = r.get("title", "")[:120]
        desc = r.get("description", "")[:150]
        lines.append(f"  {i}. [score={score:.2f}] {r['rule_id']}")
        if title: lines.append(f"       title: {title}")
        if desc:  lines.append(f"       desc:  {desc}")
    lines += ["", "Which candidate enforces the SAME control? Be lenient.",
               'Return JSON only: {"rule_ids": ["<rule_id>", ...], "confidence": "high|medium|low|none", "reasoning": "<one sentence>"}']
    return "\n".join(lines)


def ai_one(name):
    cands = top_candidates(name, TOP_N)
    if not cands:
        return name, {"rule_id":"", "confidence":"none", "reasoning":"no candidates"}
    prompt = build_prompt(name, cands)
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role":"system","content":SYSTEM_PROMPT},
                          {"role":"user","content":prompt}],
                temperature=0.1, max_tokens=250,
            )
            raw = (resp.choices[0].message.content or "").strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"): raw = raw[4:]
                raw = raw.strip()
            parsed = json.loads(raw)
            rids = parsed.get("rule_ids", [])
            if isinstance(rids, str): rids = [rids]
            return name, {"rule_id": ";".join(r for r in rids if r),
                           "confidence": (parsed.get("confidence") or "none").lower(),
                           "reasoning": (parsed.get("reasoning") or "")[:250]}
        except Exception as e:
            if attempt < 2: time.sleep(2 ** attempt)
            else:
                return name, {"rule_id":"", "confidence":"none", "reasoning": f"err: {e}"[:200]}


results = {}
print(f"\nRunning AI deep review on {len(retry_items)} items…")
with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
    futures = [ex.submit(ai_one, c) for c in retry_items]
    done = 0
    for fut in as_completed(futures):
        name, r = fut.result()
        results[name] = r
        done += 1
        if done % 50 == 0:
            print(f"  progress: {done}/{len(retry_items)}")


# ── Save ─────────────────────────────────────────────────────────────────
with open(OUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["check_name","category",
                                             "matched_rule_ids","confidence","reasoning"])
    writer.writeheader()
    for name, markers in wrong_csp_items:
        writer.writerow({"check_name":name, "category": f"wrong_csp[{','.join(markers)}]",
                          "matched_rule_ids":"", "confidence":"",
                          "reasoning":"check contains non-"+CSP+" service markers"})
    for name in retry_items:
        r = results.get(name, {})
        writer.writerow({"check_name":name, "category":"deep_review",
                          "matched_rule_ids": r.get("rule_id",""),
                          "confidence": r.get("confidence","none"),
                          "reasoning": r.get("reasoning","")})


# ── Apply HIGH+MEDIUM to main mapping file ───────────────────────────────
apply_map = {}
for name in retry_items:
    r = results.get(name, {})
    if r.get("rule_id") and r.get("confidence","").lower() in ("high","medium"):
        apply_map[name] = (r["rule_id"], r["confidence"], r["reasoning"])

rows = list(csv.DictReader(open(MAPPING_CSV)))
updated = 0
for row in rows:
    if row["check_name"] in apply_map:
        rids, conf, reason = apply_map[row["check_name"]]
        row["matched_rule_ids"] = rids
        row["method"] = f"deep_review_{conf}"
        row["confidence"] = conf
        row["reasoning"] = reason
        updated += 1

with open(MAPPING_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["check_name","matched_rule_ids",
                                             "method","confidence","reasoning"])
    writer.writeheader()
    writer.writerows(rows)


# ── Summary ─────────────────────────────────────────────────────────────
from collections import Counter
new_matched = [n for n in retry_items if results.get(n,{}).get("rule_id")]
by_conf = Counter(results[n]["confidence"] for n in new_matched)

print(f"\n═══════ {CSP.upper()} DEEP REVIEW RESULTS ═══════")
print(f"  Wrong-CSP dropped:   {len(wrong_csp_items)}")
print(f"  Retried:             {len(retry_items)}")
print(f"  Newly matched:       {len(new_matched)} (by conf: {dict(by_conf)})")
print(f"  Applied (H+M):       {updated}")
print(f"  Still unmatched:     {len(retry_items) - len(new_matched)}")
print(f"\nOutput: {OUT_CSV}")
print(f"Updated: {MAPPING_CSV}")
