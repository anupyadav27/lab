"""
Corrects false positives from the complete CAT-4 analysis.
Moves incorrectly classified COVERED rules back to UNCERTAIN or TRUE_GAP.
Updates coverage matrix and gap file accordingly.
"""
import csv, json
from pathlib import Path

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
GAP_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/cspm_gap_rules_all_csp.csv")
MATRIX_FILE = BASE / "azure_catalog_coverage_matrix_final.csv"
REVIEW_FILE = BASE / "azure_cat4_complete_review.json"

with open(REVIEW_FILE) as f:
    data = json.load(f)

# ── Classification of false positives ─────────────────────────────────────
# Format: (exact rule_id as it appears in the JSON, "uncertain" or "true_gap")
FALSE_POSITIVES = [
    # Wrong service (no YAML mapping → fallback found wrong service)
    ("azure.intune.diagnostic.settings.log.analytics.check", "true_gap"),
    ("azure.netappfiles.encryption.key.source.cmk.check", "true_gap"),
    ("azure.elastic.san.volume.group.encryption.at.rest.with.cmk", "true_gap"),
    # Malformed rule IDs with extra `:az.` annotation text → mismatched on extra tokens
    ("azure.entra.policy.require_mfa_for_management_api:az.active_directory_tenant.identity_access_security_password_policy_require_upper_lower_number_special", "uncertain"),
    ("azure.entra.policy.user_consent_for_verified_apps storage_blob_public_access_level_is_disabled storage_ensure_azure_services_are_trusted_to_access_is_enabled:az.active_directory_user.identity_access_security_user_inactive_90_days_disabled", "uncertain"),
    ("azure.app.service.managed_updates_enabled:az.azure_paas_app.paas_security_app_logging_enabled", "uncertain"),
    # Wrong concept (only semantic noise words matched)
    ("azure.cache.redis.ssl.only.access", "uncertain"),
    ("azure.storage.account.smb.channel.encryption.in.transit.aes256gcm", "uncertain"),
]

fp_map = {rule_id: dest for rule_id, dest in FALSE_POSITIVES}
fp_ids = set(fp_map.keys())

print(f"False positives to correct: {len(fp_ids)}")

# ── Separate correct covered from false positives ─────────────────────────
kept_covered = []
new_uncertain_entries = []
new_true_gap_entries = []

for entry in data["covered"]:
    rule_id, score, config_id = entry
    if rule_id in fp_ids:
        dest = fp_map[rule_id]
        if dest == "uncertain":
            new_uncertain_entries.append(entry)
            print(f"  COVERED → UNCERTAIN: {rule_id}")
        else:
            new_true_gap_entries.append(rule_id)
            print(f"  COVERED → TRUE_GAP:  {rule_id}")
    else:
        kept_covered.append(entry)

data["covered"] = kept_covered
data["uncertain"] = data["uncertain"] + new_uncertain_entries
data["true_gap"] = data["true_gap"] + new_true_gap_entries

print(f"\nCorrected totals:")
print(f"  COVERED:   {len(data['covered'])}")
print(f"  UNCERTAIN: {len(data['uncertain'])}")
print(f"  TRUE GAP:  {len(data['true_gap'])}")
print(f"  TOTAL:     {sum(len(v) for v in data.values())}")

with open(REVIEW_FILE, "w") as f:
    json.dump(data, f, indent=2)
print(f"\nSaved corrected review to {REVIEW_FILE}")


# ── Fix coverage matrix: revert false positives ───────────────────────────
print("\n=== Reverting false positives in coverage matrix ===")

# Get the base rule IDs (strip the :az. annotation)
def base_id(rule_id):
    return rule_id.split(":")[0].strip().split(" ")[0].strip()

fp_base_ids = {base_id(rid) for rid in fp_ids}

rows = []
reverted_count = 0
with open(MATRIX_FILE) as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        rid = row["catalog_rule_id"]
        if rid in fp_base_ids or rid in fp_ids:
            # Revert to ai_confirmed_gap
            row["config_covered"] = "no"
            row["coverage_status"] = "ai_confirmed_gap"
            row["covered"] = "no"
            # Remove the falsely added config rule ID
            reverted_count += 1
        rows.append(row)

print(f"  Reverted {reverted_count} rows in coverage matrix")

with open(MATRIX_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
print(f"  Saved corrected matrix")


# ── Fix gap file: add false positives back ─────────────────────────────────
print("\n=== Re-adding false positives to gap file ===")

# Load original gap file to get the full rows for these rules
# (they were removed, so we need to reconstruct from the matrix)
gap_rows = []
with open(GAP_FILE) as f:
    reader = csv.DictReader(f)
    gap_fieldnames = reader.fieldnames
    for row in reader:
        gap_rows.append(row)

# Get the rules currently in gap file
existing_gap_ids = {r["catalog_rule_id"] for r in gap_rows if r["csp"] == "azure"}

# Add back false positives that aren't already in gap file
added_back = 0
for rule_id in fp_ids:
    bid = base_id(rule_id)
    if bid not in existing_gap_ids and rule_id not in existing_gap_ids:
        # Reconstruct from matrix
        for row in rows:
            if row["catalog_rule_id"] == bid:
                gap_row = {
                    "csp": "azure",
                    "catalog_rule_id": bid,
                    "service": row.get("service", ""),
                    "category": row.get("category", ""),
                    "compliance_ids": row.get("compliance_ids", ""),
                    "compliance_frameworks": "",
                    "gap_reason": "no_config_or_ciem_match_after_ai",
                    "suggested_rule_type": "config",
                    "priority": "medium",
                    "notes": "AI checked, no CIEM match. Best AI confidence: none.",
                }
                gap_rows.append(gap_row)
                added_back += 1
                break

print(f"  Added back {added_back} false positives to gap file")
print(f"  Total Azure gaps now: {sum(1 for r in gap_rows if r['csp'] == 'azure')}")

with open(GAP_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=gap_fieldnames)
    writer.writeheader()
    writer.writerows(gap_rows)
print(f"  Saved corrected gap file")


# ── Final summary ─────────────────────────────────────────────────────────
total_covered = sum(1 for r in rows if r["covered"] == "yes")
total_gaps = sum(1 for r in gap_rows if r["csp"] == "azure")
total_rules = 1734

print(f"\n=== FINAL AZURE COVERAGE SUMMARY ===")
print(f"  Total catalog rules: {total_rules}")
print(f"  Covered (matrix):    {total_covered}")
print(f"  Coverage rate:       {total_covered/total_rules*100:.1f}%")
print(f"  Gap file entries:    {total_gaps}")
print(f"    COVERED (config_naming_variant): {len(data['covered'])}")
print(f"    UNCERTAIN (need AI/manual):      {len(data['uncertain'])}")
print(f"    TRUE CONFIRMED GAPs:             {len(data['true_gap'])}")

# Coverage status breakdown
from collections import Counter
status_counts = Counter(r["coverage_status"] for r in rows)
print(f"\nCoverage status breakdown:")
for status, cnt in sorted(status_counts.items(), key=lambda x: -x[1]):
    print(f"  {status}: {cnt}")
