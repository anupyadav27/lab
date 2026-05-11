"""
Applies AI verification results from azure_ai_uncertain_ckpt.json to:
  1. Coverage matrix (mark as config_naming_variant / partial / keep as gap)
  2. Gap file (remove confirmed-covered rules)
  3. Review JSON (move from uncertain → covered/partial/true_gap based on AI verdict)
"""
import csv, json
from pathlib import Path

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
GAP_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/cspm_gap_rules_all_csp.csv")
MATRIX_FILE = BASE / "azure_catalog_coverage_matrix_final.csv"
REVIEW_FILE = BASE / "azure_cat4_complete_review.json"
CHECKPOINT = BASE / "azure_ai_uncertain_ckpt.json"

with open(CHECKPOINT) as f:
    ckpt = json.load(f)
with open(REVIEW_FILE) as f:
    review = json.load(f)

# ── Classify each AI result ───────────────────────────────────────────────
ai_covered = {}   # rule_id → config_rule_id
ai_partial = {}
ai_gap = set()

for rule_id, result in ckpt.items():
    mt = result.get("match_type", "none")
    conf = result.get("confidence", "none")
    cfg_id = (result.get("config_rule_id") or "").strip()

    if mt == "full" and conf in ("high", "medium") and cfg_id:
        ai_covered[rule_id] = cfg_id
    elif mt == "partial" and cfg_id:
        ai_partial[rule_id] = cfg_id
    else:
        ai_gap.add(rule_id)

print(f"AI RESULTS:")
print(f"  Covered (full): {len(ai_covered)}")
print(f"  Partial:        {len(ai_partial)}")
print(f"  Still gap:      {len(ai_gap)}")


# ── Update review JSON (move entries from uncertain) ──────────────────────
new_uncertain = []
new_covered_additions = []
new_partial_additions = []
new_true_gap_additions = []

for entry in review["uncertain"]:
    rule_id = entry[0]
    if rule_id in ai_covered:
        new_covered_additions.append([rule_id, "AI-verified", ai_covered[rule_id]])
    elif rule_id in ai_partial:
        new_partial_additions.append([rule_id, "AI-partial", ai_partial[rule_id]])
    elif rule_id in ai_gap:
        new_true_gap_additions.append(rule_id)
    else:
        new_uncertain.append(entry)

review["covered"] += new_covered_additions
review["uncertain"] = new_uncertain
review["true_gap"] += new_true_gap_additions
review.setdefault("partial", []).extend(new_partial_additions)

with open(REVIEW_FILE, "w") as f:
    json.dump(review, f, indent=2)

print(f"\nUpdated review JSON:")
print(f"  COVERED:  {len(review['covered'])}")
print(f"  PARTIAL:  {len(review.get('partial', []))}")
print(f"  UNCERTAIN: {len(review['uncertain'])}")
print(f"  TRUE GAP: {len(review['true_gap'])}")


# ── Helper to get base rule ID (strip malformed annotations) ──────────────
def base_id(rule_id):
    return rule_id.split(":")[0].strip().split(" ")[0].strip()

ai_covered_base = {base_id(rid): (rid, cfg) for rid, cfg in ai_covered.items()}
ai_partial_base = {base_id(rid): (rid, cfg) for rid, cfg in ai_partial.items()}


# ── Update coverage matrix ────────────────────────────────────────────────
print(f"\n=== Updating coverage matrix ===")
rows = []
covered_updated = 0
partial_updated = 0
gap_reasonings_added = 0
with open(MATRIX_FILE) as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        rid = row["catalog_rule_id"]
        bid = base_id(rid)

        # AI-confirmed covered
        if rid in ai_covered or bid in ai_covered_base:
            cfg_id = ai_covered.get(rid) or ai_covered_base.get(bid, ("", ""))[1]
            row["config_covered"] = "yes"
            row["coverage_status"] = "config_naming_variant"
            row["covered"] = "yes"
            existing_cfg = row.get("config_rule_ids", "").strip()
            if cfg_id and cfg_id not in existing_cfg:
                row["config_rule_ids"] = (existing_cfg + ";" + cfg_id).strip(";")
            row["ai_match_rule_id"] = cfg_id
            row["ai_confidence"] = ckpt.get(rid, ckpt.get(bid, {})).get("confidence", "")
            row["ai_reasoning"] = (ckpt.get(rid, ckpt.get(bid, {})).get("reasoning", ""))[:200]
            covered_updated += 1
        # AI-confirmed partial
        elif rid in ai_partial or bid in ai_partial_base:
            cfg_id = ai_partial.get(rid) or ai_partial_base.get(bid, ("", ""))[1]
            row["config_covered"] = "partial"
            row["coverage_status"] = "partial_config_match"
            row["covered"] = "partial"
            existing_cfg = row.get("config_rule_ids", "").strip()
            if cfg_id and cfg_id not in existing_cfg:
                row["config_rule_ids"] = (existing_cfg + ";" + cfg_id).strip(";")
            row["ai_match_rule_id"] = cfg_id
            row["ai_confidence"] = ckpt.get(rid, ckpt.get(bid, {})).get("confidence", "")
            row["ai_reasoning"] = (ckpt.get(rid, ckpt.get(bid, {})).get("reasoning", ""))[:200]
            partial_updated += 1
        # AI-confirmed gap → update reasoning only
        elif rid in ai_gap or bid in ai_gap:
            r = ckpt.get(rid, ckpt.get(bid, {}))
            if r:
                row["ai_confidence"] = r.get("confidence", "")
                row["ai_reasoning"] = (r.get("reasoning", ""))[:200]
                gap_reasonings_added += 1
        rows.append(row)

print(f"  Covered updates: {covered_updated}")
print(f"  Partial updates: {partial_updated}")
print(f"  Gap reasoning added: {gap_reasonings_added}")

with open(MATRIX_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


# ── Remove confirmed-covered rules from gap file ──────────────────────────
print(f"\n=== Updating gap file ===")
ai_covered_ids = set(ai_covered.keys()) | set(ai_covered_base.keys())

gap_rows = []
removed = 0
with open(GAP_FILE) as f:
    reader = csv.DictReader(f)
    gap_fieldnames = reader.fieldnames
    for row in reader:
        if row["csp"] == "azure" and (row["catalog_rule_id"] in ai_covered_ids
                                      or base_id(row["catalog_rule_id"]) in ai_covered_ids):
            removed += 1
            continue
        gap_rows.append(row)

print(f"  Removed {removed} covered rules from gap file")

with open(GAP_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=gap_fieldnames)
    writer.writeheader()
    writer.writerows(gap_rows)


# ── Final summary ─────────────────────────────────────────────────────────
from collections import Counter
status_counts = Counter(r["coverage_status"] for r in rows)
covered = sum(1 for r in rows if r["covered"] == "yes")
partial = sum(1 for r in rows if r["covered"] == "partial")
total = len(rows)
azure_gaps = sum(1 for r in gap_rows if r["csp"] == "azure")

print(f"\n=== FINAL AZURE COVERAGE STATE ===")
print(f"Total catalog rules:   {total}")
print(f"Covered (yes):         {covered}  ({covered/total*100:.1f}%)")
print(f"Covered (partial):     {partial}  ({partial/total*100:.1f}%)")
print(f"Not covered:           {total-covered-partial}  ({(total-covered-partial)/total*100:.1f}%)")
print(f"Gap file Azure rows:   {azure_gaps}")
print(f"\nCoverage status breakdown:")
for s, c in sorted(status_counts.items(), key=lambda x: -x[1]):
    print(f"  {s}: {c}")
