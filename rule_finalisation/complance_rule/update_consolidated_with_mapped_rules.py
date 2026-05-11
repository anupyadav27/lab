"""
Updates consolidated_compliance_rules_FINAL_CLEAN_2026-04-17.csv by replacing
AWS and Azure catalog rule entries in `aws_mapped_rules` / `azure_mapped_rules`
with the actual mapped config/CIEM detection rule IDs from the coverage matrices.

Rules:
  - If catalog rule is COVERED → emit `catalog_rule_id:mapped_rule_id`
  - If catalog rule is a GAP (true_gap / ai_confirmed_gap) → keep as `catalog_rule_id` only
  - Multiple mapped rules joined by comma within the pair
  - Entries separated by `; ` (matching the original format)

Writes a new file alongside the original with `_UPDATED_<date>` suffix.
"""
import csv
from datetime import date
from pathlib import Path

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation")
CONSOLIDATED = BASE / "complance_rule/consolidated_compliance_rules_FINAL_CLEAN_2026-04-17.csv"
AWS_MATRIX = BASE / "rule_list/rules_by_csp_2026-04-17/aws_catalog_coverage_matrix_final.csv"
AZURE_MATRIX = BASE / "rule_list/rules_by_csp_2026-04-17/azure_catalog_coverage_matrix_final.csv"

TODAY = date.today().isoformat()
OUT = BASE / f"complance_rule/consolidated_compliance_rules_FINAL_CLEAN_2026-04-17_UPDATED_{TODAY}.csv"

# ── Build AWS map: catalog_rule_id → list of mapped rule IDs ──────────────
aws_map = {}           # catalog_id → [mapped_rule_ids]
aws_gap = set()        # true_gap / unmapped
aws_status_map = {}    # catalog_id → coverage_status

# AWS "covered" statuses (anything except true_gap / catalog_invalid)
AWS_COVERED_STATUSES = {
    "config+ciem", "ciem_multi", "ciem_ai_match", "ciem_direct_only",
    "config_only", "config_resolved", "naming_variant_covered",
    "compliance_met_elsewhere", "catalog_data_quality",
}
AWS_GAP_STATUSES = {"true_gap", "catalog_invalid"}

with open(AWS_MATRIX) as f:
    for row in csv.DictReader(f):
        rid = row["catalog_rule_id"]
        status = row["coverage_status"]
        aws_status_map[rid] = status

        mapped = []
        # Combine all matched rule IDs
        for col in ["config_rule_ids", "ciem_via_yaml_rule_ids",
                    "ciem_direct_rule_ids", "ciem_ai_gap_rule_id"]:
            val = (row.get(col) or "").strip()
            if val:
                for m in val.replace(",", ";").split(";"):
                    m = m.strip()
                    if m and m not in mapped:
                        mapped.append(m)

        if status in AWS_GAP_STATUSES or not mapped:
            aws_gap.add(rid)
        else:
            aws_map[rid] = mapped

print(f"AWS matrix: {len(aws_status_map)} rules | covered={len(aws_map)} | gap={len(aws_gap)}")


# ── Build Azure map ────────────────────────────────────────────────────────
azure_map = {}
azure_gap = set()
azure_status_map = {}

AZURE_COVERED_STATUSES = {
    "config_only", "ciem_only", "config_naming_variant",
    "partial_config_match",
}
AZURE_GAP_STATUSES = {"ai_confirmed_gap", "not_covered"}

with open(AZURE_MATRIX) as f:
    for row in csv.DictReader(f):
        rid = row["catalog_rule_id"]
        status = row["coverage_status"]
        azure_status_map[rid] = status

        mapped = []
        for col in ["config_rule_ids", "ciem_rule_ids", "ai_match_rule_id"]:
            val = (row.get(col) or "").strip()
            if val:
                for m in val.replace(",", ";").split(";"):
                    m = m.strip()
                    if m and m not in mapped:
                        mapped.append(m)

        if status in AZURE_GAP_STATUSES or not mapped:
            azure_gap.add(rid)
        else:
            azure_map[rid] = mapped

print(f"Azure matrix: {len(azure_status_map)} rules | covered={len(azure_map)} | gap={len(azure_gap)}")


# ── Parse existing mapped_rules format ────────────────────────────────────
def extract_catalog_id(entry: str, matrix_ids: set) -> str:
    """
    Extract the CURRENT catalog rule ID from an entry.
    Entries can be:
      - `catalog_id` (plain)
      - `OLD_id:NEW_id`         (AWS style — RIGHT is new catalog)
      - `catalog_id:az.func_id` (Azure style — LEFT is catalog, RIGHT is fn)
      - `catalog_id:az.func_id` stored as-is in matrix (malformed IDs)
    Preference: FULL entry > RIGHT > LEFT > original.
    """
    entry = entry.strip()
    # FULL entry (with colon) is the catalog_id
    if entry in matrix_ids:
        return entry
    if ":" in entry:
        parts = entry.split(":", 1)
        left, right = parts[0].strip(), parts[1].strip()
        # AWS: RIGHT is new catalog_id
        if right in matrix_ids:
            return right
        # Azure: LEFT is catalog_id (RIGHT is az.* function)
        if left in matrix_ids:
            return left
        return right
    return entry


def replace_mappings(mapped_rules_str: str, coverage_map: dict, gap_set: set,
                     matrix_ids: set, stats: dict) -> str:
    """Replace each catalog_rule_id entry with the new mapped detection rule IDs."""
    if not mapped_rules_str or not mapped_rules_str.strip():
        return mapped_rules_str

    new_entries = []
    for raw in mapped_rules_str.split(";"):
        entry = raw.strip()
        if not entry:
            continue
        cat_id = extract_catalog_id(entry, matrix_ids)

        if cat_id in coverage_map:
            # Format: catalog_rule_id:mapped_detection_rule(s)
            mapped_ids = coverage_map[cat_id]
            new_entries.append(f"{cat_id}:{','.join(mapped_ids)}")
            stats["replaced"] += 1
        elif cat_id in gap_set:
            # Keep catalog ID alone (it's a gap — no detection rule yet)
            new_entries.append(cat_id)
            stats["kept_as_gap"] += 1
        else:
            # Catalog ID not in our matrix — preserve original entry
            new_entries.append(entry)
            stats["not_in_matrix"] += 1

    return "; ".join(new_entries)


# ── Process consolidated CSV ─────────────────────────────────────────────
aws_stats = {"replaced": 0, "kept_as_gap": 0, "not_in_matrix": 0}
azure_stats = {"replaced": 0, "kept_as_gap": 0, "not_in_matrix": 0}

rows_updated_aws = 0
rows_updated_azure = 0
total_rows = 0

with open(CONSOLIDATED) as f_in, open(OUT, "w", newline="") as f_out:
    reader = csv.DictReader(f_in)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        total_rows += 1

        # AWS
        orig_aws = row.get("aws_mapped_rules", "") or ""
        if orig_aws.strip():
            new_aws = replace_mappings(orig_aws, aws_map, aws_gap,
                                        set(aws_status_map.keys()), aws_stats)
            if new_aws != orig_aws:
                row["aws_mapped_rules"] = new_aws
                rows_updated_aws += 1

        # Azure
        orig_azure = row.get("azure_mapped_rules", "") or ""
        if orig_azure.strip():
            new_azure = replace_mappings(orig_azure, azure_map, azure_gap,
                                          set(azure_status_map.keys()), azure_stats)
            if new_azure != orig_azure:
                row["azure_mapped_rules"] = new_azure
                rows_updated_azure += 1

        writer.writerow(row)

print(f"\n=== PROCESSING COMPLETE ===")
print(f"Total compliance rows:  {total_rows}")
print(f"Rows with AWS changes:   {rows_updated_aws}")
print(f"Rows with Azure changes: {rows_updated_azure}")
print()
print(f"AWS entry stats:")
print(f"  Replaced with mapped rule:  {aws_stats['replaced']}")
print(f"  Kept as gap (catalog only): {aws_stats['kept_as_gap']}")
print(f"  Not in matrix (unchanged):  {aws_stats['not_in_matrix']}")
print()
print(f"Azure entry stats:")
print(f"  Replaced with mapped rule:  {azure_stats['replaced']}")
print(f"  Kept as gap (catalog only): {azure_stats['kept_as_gap']}")
print(f"  Not in matrix (unchanged):  {azure_stats['not_in_matrix']}")
print(f"\nWrote: {OUT}")
