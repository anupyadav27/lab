"""
Merges gcp_deep_review.csv matches into gcp_check_to_rule.csv.
Applies HIGH + MEDIUM confidence matches automatically (low are kept as gaps).
"""
import csv
from pathlib import Path

BASE = Path("/Users/apple/Desktop/compliance_Database/final_compliance_rules")
MAPPING = BASE / "rule_mapping/gcp_check_to_rule.csv"
DEEP = BASE / "rule_mapping/gcp_deep_review.csv"

# Load deep review results
apply_map = {}
for row in csv.DictReader(open(DEEP)):
    if row["category"] == "wrong_csp" or "wrong_csp" in row["category"]:
        continue
    rids = row["matched_rule_ids"].strip()
    conf = row["confidence"].strip().lower()
    if rids and conf in ("high", "medium"):
        apply_map[row["check_name"]] = (rids, conf, row["reasoning"])

print(f"Deep-review matches to apply: {len(apply_map)}")

# Update mapping file
rows = list(csv.DictReader(open(MAPPING)))
updated = 0
for r in rows:
    if r["check_name"] in apply_map:
        rids, conf, reasoning = apply_map[r["check_name"]]
        r["matched_rule_ids"] = rids
        r["method"] = f"deep_review_{conf}"
        r["confidence"] = conf
        r["reasoning"] = reasoning
        updated += 1

with open(MAPPING, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["check_name", "matched_rule_ids",
                                             "method", "confidence", "reasoning"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {updated} rows in {MAPPING}")
