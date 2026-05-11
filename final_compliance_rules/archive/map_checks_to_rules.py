"""
Maps compliance_agent check names (e.g. `aws_iam_user_no_inline_policies`) to
catalog rule_ids (e.g. `aws.iam.user.policies.no_inline_policies`) per CSP.

Strategy:
  1. Token-similarity first: compute Jaccard score between check-name tokens and
     each catalog rule_id tokens (across both rule_check and rule_ciem)
  2. Auto-accept when best score ≥ 0.60 AND service aligned
  3. Low-confidence (0.25 ≤ score < 0.60) → AI verify with DeepSeek
  4. Below 0.25 → mark as unmapped (needs new rule)

Output: rule_mapping/{csp}_check_to_rule.csv — one row per compliance check name
  check_name, matched_rule_ids (semicolon-list), mapping_method, confidence
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
    print("Install openai first: pip install openai", file=sys.stderr)
    sys.exit(1)

BASE = Path("/Users/apple/Desktop/compliance_Database/final_compliance_rules")
RULE_CATALOGS = BASE / "rule_catalogs"
COMP = BASE / "final_compliance_rules.csv"
OUT_DIR = BASE / "rule_mapping"
OUT_DIR.mkdir(exist_ok=True)

CSPS = ["aws", "azure", "gcp", "oracle", "ibm", "alicloud", "k8s"]
# Map compliance CSV column csp → catalog file prefix (oracle → oci)
CSP_TO_CATALOG = {"aws": "aws", "azure": "azure", "gcp": "gcp",
                   "oracle": "oci", "ibm": "ibm", "alicloud": "alicloud", "k8s": "k8s"}

API_KEY = os.getenv("DEEPSEEK_API_KEY") or "sk-3d7acb8511ad4da18e8b0c89733f472b"
MODEL = "deepseek-chat"
CONCURRENCY = 10
AUTO_ACCEPT = 0.60
AI_MIN = 0.25

NOISE = {"the", "a", "an", "for", "with", "and", "or", "is", "to", "of", "in",
         "on", "by", "that", "not", "are", "all", "have", "must", "only", "no",
         "new", "your", "be", "use", "using", "from", "check", "configured",
         "enabled", "resource", "configuration", "az"}


def tokens(s: str) -> set[str]:
    return {t.lower() for t in re.split(r"[._\-\s/]+", s) if len(t) > 1} - NOISE


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load_catalog(csp_catalog: str) -> list[dict]:
    """Load both rule_check and rule_ciem catalogs for a CSP."""
    rows = []
    for kind in ["rule_check", "rule_ciem"]:
        fp = RULE_CATALOGS / f"{csp_catalog}_{kind}.csv"
        if not fp.exists():
            continue
        with open(fp) as f:
            for row in csv.DictReader(f):
                rid = row["rule_id"]
                row["_kind"] = kind
                row["_tokens"] = tokens(rid)
                rows.append(row)
    return rows


def find_candidates(check_name: str, catalog: list[dict], top_k: int = 5):
    """Return top candidates by Jaccard score."""
    check_tok = tokens(check_name)
    if not check_tok:
        return []
    scored = []
    for r in catalog:
        score = jaccard(check_tok, r["_tokens"])
        if score > 0:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    return scored[:top_k]


def extract_service(check_name: str) -> str:
    """Pull out the service name from `aws_iam_user_...` → `iam`."""
    parts = check_name.split("_")
    return parts[1] if len(parts) >= 2 else ""


# ── AI verification ───────────────────────────────────────────────────────
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com") if API_KEY else None

SYSTEM_PROMPT = """You are a cloud security expert mapping compliance check names to catalog rule IDs.
Return the rule_id(s) that implement the same security check as the given check name.
Consider: service match, action match, target resource match.
A match is VALID only if the rule detects the same security violation."""


def ai_verify(check_name: str, candidates: list) -> dict:
    if not client or not candidates:
        return {"rule_id": "", "confidence": "none", "reasoning": ""}

    prompt_lines = [
        f"CHECK NAME: {check_name}",
        "",
        "TOP CANDIDATE CATALOG RULES:",
    ]
    for i, (score, r) in enumerate(candidates[:5], 1):
        title = r.get("title", "")[:100]
        prompt_lines.append(f"  {i}. [score={score:.2f}] {r['rule_id']}")
        if title:
            prompt_lines.append(f"       title: {title}")

    prompt_lines += [
        "",
        "Which candidate rule(s) implement the same check?",
        "Return JSON only (no markdown):",
        '{"rule_ids": ["<rule_id>", ...], "confidence": "high|medium|low|none", "reasoning": "<one sentence>"}',
    ]

    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": "\n".join(prompt_lines)}],
                temperature=0.1,
                max_tokens=200,
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
            return {
                "rule_id": ";".join(r for r in rids if r),
                "confidence": (parsed.get("confidence") or "none").lower(),
                "reasoning": (parsed.get("reasoning") or "")[:200],
            }
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return {"rule_id": "", "confidence": "none", "reasoning": f"error: {e}"[:200]}


# ── Main pipeline ─────────────────────────────────────────────────────────
def process_csp(csp: str):
    csp_catalog_name = CSP_TO_CATALOG[csp]
    catalog = load_catalog(csp_catalog_name)
    print(f"\n━━━ {csp.upper()} ━━━")
    print(f"  catalog rules: {len(catalog)}")

    # Gather unique check names
    unique_checks = set()
    with open(COMP) as f:
        for row in csv.DictReader(f):
            col = f"{csp}_checks"
            for c in (row.get(col, "") or "").split(";"):
                c = c.strip()
                if c:
                    unique_checks.add(c)
    unique_checks = sorted(unique_checks)
    print(f"  unique check names: {len(unique_checks)}")

    if not catalog or not unique_checks:
        return

    # Token-match each check name
    mappings = {}  # check_name → {matched_rule_ids, method, confidence, reasoning}
    ai_queue = []

    for check in unique_checks:
        candidates = find_candidates(check, catalog, top_k=5)
        if not candidates:
            mappings[check] = {"matched_rule_ids": "", "method": "no_candidates",
                                "confidence": "none", "reasoning": "no token overlap"}
            continue

        best_score, best_rule = candidates[0]
        if best_score >= AUTO_ACCEPT:
            mappings[check] = {"matched_rule_ids": best_rule["rule_id"],
                                "method": "token_match_high",
                                "confidence": f"{best_score:.2f}",
                                "reasoning": f"Jaccard={best_score:.2f}"}
        elif best_score >= AI_MIN:
            ai_queue.append((check, candidates))
        else:
            mappings[check] = {"matched_rule_ids": "", "method": "weak_match",
                                "confidence": f"{best_score:.2f}",
                                "reasoning": "weak token overlap — likely no matching rule"}

    print(f"  auto-accepted: {sum(1 for m in mappings.values() if m['method']=='token_match_high')}")
    print(f"  AI queue:      {len(ai_queue)}")
    print(f"  no candidates: {sum(1 for m in mappings.values() if m['method']=='no_candidates')}")

    # Run AI in parallel
    if ai_queue and client:
        def ai_one(item):
            check, cands = item
            r = ai_verify(check, cands)
            return check, r

        completed = 0
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
            futures = [ex.submit(ai_one, item) for item in ai_queue]
            for fut in as_completed(futures):
                check, result = fut.result()
                mappings[check] = {
                    "matched_rule_ids": result["rule_id"],
                    "method": "ai_verified" if result["rule_id"] else "ai_rejected",
                    "confidence": result["confidence"],
                    "reasoning": result["reasoning"],
                }
                completed += 1
                if completed % 50 == 0:
                    print(f"    AI progress: {completed}/{len(ai_queue)}")

    # Write output
    out_path = OUT_DIR / f"{csp}_check_to_rule.csv"
    fieldnames = ["check_name", "matched_rule_ids", "method", "confidence", "reasoning"]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for check in unique_checks:
            m = mappings[check]
            writer.writerow({
                "check_name": check,
                "matched_rule_ids": m["matched_rule_ids"],
                "method": m["method"],
                "confidence": m["confidence"],
                "reasoning": m["reasoning"],
            })
    print(f"  saved: {out_path}")

    # Stats
    from collections import Counter
    method_counts = Counter(m["method"] for m in mappings.values())
    mapped = sum(1 for m in mappings.values() if m["matched_rule_ids"])
    print(f"  mapped: {mapped}/{len(unique_checks)} ({mapped/len(unique_checks)*100:.1f}%)")
    print(f"  methods: {dict(method_counts)}")


# ── Run for all CSPs ─────────────────────────────────────────────────────
if __name__ == "__main__":
    csps_to_process = sys.argv[1:] if len(sys.argv) > 1 else CSPS
    for csp in csps_to_process:
        process_csp(csp)
