"""
Applies a deterministic verdict to every row in aws_tier3_review.csv based on:
  - verdict_bucket (Jaccard-derived)
  - new_ai_confidence (DeepSeek re-evaluation)

Verdicts:
  ACCEPT            strong evidence the AI match is valid; safe to take
  KEEP_FOR_REVIEW   plausible match; human should eyeball
  GAP_LIKELY        AI + Jaccard both weak; probably not in catalog
  GAP_CONFIRMED     real gap per both signals
  CATALOG_GAP       the service itself is missing from the catalog

Reads:  aws_tier3_review.csv
Writes: aws_tier3_review_labeled.csv  (same rows + manual_review_decision filled)
        aws_tier3_verdict_summary.json
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
IN_CSV = BASE / "aws_tier3_review.csv"
OUT_CSV = BASE / "aws_tier3_review_labeled.csv"
OUT_SUMMARY = BASE / "aws_tier3_verdict_summary.json"


def verdict(row: dict) -> tuple[str, str]:
    bucket = row["verdict_bucket"]
    new_conf = (row["new_ai_confidence"] or "none").lower()
    new_match = (row["new_ai_match"] or "").strip()
    j = float(row.get("best_jaccard") or 0.0)

    if bucket == "catalog-empty":
        return "CATALOG_GAP", "no catalog rules exist for this service — add catalog entry"

    if bucket == "ai-likely-missed":
        if new_conf in ("high", "medium") and new_match:
            return "ACCEPT", f"Jaccard {j} + AI {new_conf} — strong recovery"
        if new_conf == "low" and new_match:
            return "KEEP_FOR_REVIEW", f"Jaccard {j} but AI only low — eyeball"
        return "KEEP_FOR_REVIEW", f"Jaccard {j} but AI says none — check catalog wording drift"

    if bucket == "borderline-look":
        if new_conf == "high" and new_match:
            return "ACCEPT", f"AI high despite moderate Jaccard {j}"
        if new_conf in ("medium", "low") and new_match:
            return "KEEP_FOR_REVIEW", f"AI {new_conf} at Jaccard {j}"
        return "GAP_LIKELY", f"Jaccard {j}, AI none"

    if bucket == "weak-shared-theme":
        if new_conf == "high" and new_match:
            return "KEEP_FOR_REVIEW", f"AI overrides weak Jaccard {j} — verify match"
        if new_conf in ("medium", "low") and new_match:
            return "GAP_LIKELY", f"weak overlap {j} + AI {new_conf}"
        return "GAP_LIKELY", f"weak Jaccard {j}, AI none"

    if bucket == "real-gap":
        if new_conf == "high" and new_match:
            return "KEEP_FOR_REVIEW", f"AI disagrees with ~0 Jaccard — double-check"
        return "GAP_CONFIRMED", "no token overlap, AI none"

    return "KEEP_FOR_REVIEW", "unrecognised bucket"


def main():
    with IN_CSV.open() as f:
        rows = list(csv.DictReader(f))

    out_rows = []
    decisions = Counter()
    by_service = defaultdict(Counter)
    for row in rows:
        d, note = verdict(row)
        row["manual_review_decision"] = d
        row["manual_review_notes"] = note
        decisions[d] += 1
        by_service[row["yaml_service"]][d] += 1
        out_rows.append(row)

    fieldnames = list(rows[0].keys())
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    summary = {
        "total_rows": len(rows),
        "verdicts": dict(decisions),
        "per_service_top20": {
            svc: dict(cnt) for svc, cnt in sorted(by_service.items(), key=lambda x: -sum(x[1].values()))[:20]
        },
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
