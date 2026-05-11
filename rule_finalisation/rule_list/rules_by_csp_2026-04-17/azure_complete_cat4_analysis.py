"""
Complete analysis of all unanalyzed Azure gap rules.
Runs service-scoped keyword matching to identify:
  - COVERED: config rule exists but was missed by Jaccard (verbose naming)
  - UNCERTAIN: weak match, needs manual/AI review
  - TRUE_GAP: no matching config rule found

Then applies results to:
1. Update azure_catalog_coverage_matrix_final.csv
2. Remove covered rules from cspm_gap_rules_all_csp.csv
"""
import csv, json, re, sys, yaml
from collections import defaultdict
from pathlib import Path

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
YAML_PATH = Path("/Users/apple/Desktop/threat-engine/catalog/rule/azure_rule_check/1_azure_full_scope_assertions.yaml")
GAP_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/cspm_gap_rules_all_csp.csv")
MATRIX_FILE = BASE / "azure_catalog_coverage_matrix_final.csv"
EXISTING_REVIEW = BASE / "azure_cat4_final_review.json"
OUT_FULL = BASE / "azure_cat4_complete_review.json"

# ── Load YAML config rules ─────────────────────────────────────────────────
with open(YAML_PATH) as f:
    config_yaml = yaml.safe_load(f)

# Build flat list: (svc, rule_id)
config_all = []
for svc, svc_data in config_yaml.items():
    if not isinstance(svc_data, dict):
        continue
    for res_type, items in svc_data.items():
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict) and item.get("rule_id"):
                config_all.append((svc, item["rule_id"]))

# Build per-service index
config_by_service = defaultdict(list)
for svc, rid in config_all:
    config_by_service[svc].append(rid)

all_config_ids = [rid for _, rid in config_all]


# ── Normalize rule ID to tokens ────────────────────────────────────────────
NOISE = {"azure", "configured", "configuration", "resource", "enabled", "check",
         "policy", "az", "the", "for", "with", "and", "or", "is", "to", "of",
         "in", "on", "a", "an", "should", "be", "use", "using", "from", "that",
         "not", "are", "all", "have", "must", "only", "no", "new", "your", "by"}

def tokens(s):
    return set(t.lower() for t in re.split(r"[._\-\s/]+", s) if len(t) > 1) - NOISE


# ── Catalog rule → service mapping ─────────────────────────────────────────
# Maps catalog service prefix → YAML service(s) to search
SVC_MAP = {
    "defender": ["defender_for_cloud", "security_center"],
    "security": ["security_center", "defender_for_cloud"],
    "securitycenter": ["security_center", "defender_for_cloud"],
    "monitor": ["monitor"],
    "log": ["monitor"],
    "function": ["app_service"],
    "functionapp": ["app_service"],
    "functions": ["app_service"],
    "appservice": ["app_service"],
    "app": ["app_service"],
    "application": ["app_service"],
    "webapp": ["app_service", "web"],
    "site": ["app_service"],
    "ad": ["active_directory", "azure_active_directory"],
    "aad": ["active_directory", "azure_active_directory"],
    "entra": ["active_directory", "azure_active_directory", "entra_id_governance"],
    "entrad": ["active_directory", "azure_active_directory"],
    "password": ["active_directory"],
    "user": ["active_directory"],
    "iam": ["rbac", "authorization"],
    "rbac": ["rbac", "authorization"],
    "cosmosdb": ["cosmos_db"],
    "cosmos": ["cosmos_db"],
    "databricks": ["azure_databricks"],
    "postgresql": ["postgresql"],
    "mysql": ["mysql"],
    "mariadb": ["mariadb"],
    "sqlserver": ["sql_server"],
    "sql": ["sql", "sql_server", "sql_managed_instance"],
    "storage": ["storage"],
    "blob": ["storage"],
    "files": ["storage"],
    "synapse": ["synapse"],
    "vm": ["compute"],
    "compute": ["compute"],
    "virtualmachines": ["compute"],
    "disk": ["compute"],
    "managed": ["compute", "managed_identity"],
    "container": ["container_registry", "container_apps"],
    "batch": ["batch"],
    "cache": ["cache"],
    "cdn": ["cdn"],
    "dataprotection": ["backup"],
    "backup": ["backup"],
    "load": ["network"],
    "loadbalancer": ["network"],
    "networksecuritygroup": ["network"],
    "vpn": ["network"],
    "network": ["network"],
    "policy": ["policy"],
    "search": ["search"],
    "resource": ["resource_groups"],
    "subscription": ["subscription"],
    "automation": ["automation"],
    "certificates": ["key_vault"],
    "key": ["key_vault"],
    "patch": ["guest_configuration", "compute"],
    "redis": ["cache"],
    "iot": [],  # no IoT service in YAML
    "intune": [],  # no Intune in YAML
    "notification": [],
    "elastic": [],  # likely wrong CSP
    "netappfiles": [],
    "cdn": ["cdn"],
    "azure": [],  # too generic
    "enabled": [],  # too generic
}


def get_yaml_services(rule_id):
    """Get YAML service sections to search for a given catalog rule ID."""
    parts = rule_id.split(".")
    svc_key = parts[1] if len(parts) > 1 else ""
    return SVC_MAP.get(svc_key, [])


def score_match(catalog_id, config_id):
    """Score semantic similarity between catalog and config rule IDs."""
    cat_tokens = tokens(catalog_id)
    cfg_tokens = tokens(config_id)
    if not cat_tokens:
        return 0
    shared = cat_tokens & cfg_tokens
    # Weight: score = number of shared tokens (penalize for very short catalog)
    score = len(shared)
    # Bonus if catalog tokens are mostly covered
    coverage = len(shared) / len(cat_tokens) if cat_tokens else 0
    if coverage >= 0.7:
        score += 1
    return score


def find_best_config_match(rule_id, yaml_services):
    """Find best matching config rule within given YAML services."""
    candidates = []
    for svc in yaml_services:
        for config_id in config_by_service.get(svc, []):
            s = score_match(rule_id, config_id)
            if s > 0:
                candidates.append((s, config_id))

    if not candidates:
        # Fallback: search all services
        for config_id in all_config_ids:
            s = score_match(rule_id, config_id)
            if s >= 3:
                candidates.append((s, config_id))

    if not candidates:
        return 0, ""
    best = max(candidates, key=lambda x: x[0])
    return best


# ── Load existing review results ───────────────────────────────────────────
with open(EXISTING_REVIEW) as f:
    existing = json.load(f)

analyzed_ids = set()
covered_map = {}   # rule_id → config_id
uncertain_map = {}
true_gaps = set()

for rule_id, score, config_id in existing["covered"]:
    analyzed_ids.add(rule_id)
    covered_map[rule_id] = config_id

for rule_id, score, config_id in existing["uncertain"]:
    analyzed_ids.add(rule_id)
    uncertain_map[rule_id] = config_id

for rule_id in existing["true_gap"]:
    analyzed_ids.add(rule_id)
    true_gaps.add(rule_id)


# ── Load gap file to get all unanalyzed Azure rules ──────────────────────
unanalyzed = []
with open(GAP_FILE) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["csp"] != "azure":
            continue
        rid = row["catalog_rule_id"]
        if rid not in analyzed_ids:
            unanalyzed.append(rid)

print(f"Unanalyzed Azure gap rules: {len(unanalyzed)}")

# ── Service distribution of unanalyzed ──────────────────────────────────
from collections import Counter
svc_dist = Counter(r.split(".")[1] if len(r.split(".")) > 1 else "?" for r in unanalyzed)
print("\nService distribution of unanalyzed:")
for svc, cnt in sorted(svc_dist.items(), key=lambda x: -x[1]):
    print(f"  {svc}: {cnt}")


# ── Run keyword analysis on unanalyzed ───────────────────────────────────
NEW_COVERED = []   # (rule_id, score, config_id)
NEW_UNCERTAIN = [] # (rule_id, score, config_id)
NEW_TRUE_GAP = []  # rule_id

# Defender rules are CAT-3 (needs Defender-specific enables, not regular config)
# But let's still check security_center/defender_for_cloud
DEFENDER_KEYWORDS = ["azure.defender", "azure.security", "azure.securitycenter"]

for rule_id in unanalyzed:
    yaml_svcs = get_yaml_services(rule_id)
    score, best_config = find_best_config_match(rule_id, yaml_svcs)

    if score >= 3:
        NEW_COVERED.append((rule_id, score, best_config))
    elif score == 2:
        NEW_UNCERTAIN.append((rule_id, score, best_config))
    else:
        NEW_TRUE_GAP.append(rule_id)

print(f"\nNew results for {len(unanalyzed)} unanalyzed rules:")
print(f"  COVERED: {len(NEW_COVERED)}")
print(f"  UNCERTAIN: {len(NEW_UNCERTAIN)}")
print(f"  TRUE GAP: {len(NEW_TRUE_GAP)}")


# ── Merge with existing results ─────────────────────────────────────────
all_covered = existing["covered"] + NEW_COVERED
all_uncertain = existing["uncertain"] + NEW_UNCERTAIN
all_true_gap = existing["true_gap"] + NEW_TRUE_GAP

print(f"\nCombined totals:")
print(f"  COVERED: {len(all_covered)}")
print(f"  UNCERTAIN: {len(all_uncertain)}")
print(f"  TRUE GAP: {len(all_true_gap)}")
print(f"  TOTAL: {len(all_covered) + len(all_uncertain) + len(all_true_gap)}")

# Save complete review
result = {
    "covered": all_covered,
    "uncertain": all_uncertain,
    "true_gap": all_true_gap
}
with open(OUT_FULL, "w") as f:
    json.dump(result, f, indent=2)
print(f"\nSaved complete review to {OUT_FULL}")


# ── Print detailed breakdown ─────────────────────────────────────────────
print("\n=== NEW COVERED (config rule exists but missed by Jaccard) ===")
for rule_id, score, config_id in NEW_COVERED:
    print(f"  [{score}] {rule_id}")
    print(f"       → {config_id}")

print("\n=== NEW UNCERTAIN ===")
for rule_id, score, config_id in NEW_UNCERTAIN:
    print(f"  [{score}] {rule_id}")
    print(f"       → {config_id}")

print("\n=== NEW TRUE GAPS ===")
for rule_id in NEW_TRUE_GAP:
    print(f"  {rule_id}")


# ── Apply results to coverage matrix ─────────────────────────────────────
print("\n=== Applying results to coverage matrix ===")

covered_rule_ids = set(r[0] for r in all_covered)
covered_config_map = {r[0]: r[2] for r in all_covered}

# Read matrix
rows = []
with open(MATRIX_FILE) as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        rows.append(row)

updated_count = 0
for row in rows:
    rid = row["catalog_rule_id"]
    if rid in covered_rule_ids:
        row["config_covered"] = "yes"
        row["coverage_status"] = "config_naming_variant"
        row["covered"] = "yes"
        # Add config rule ID if not already there
        existing_cfg = row.get("config_rule_ids", "").strip()
        new_cfg = covered_config_map[rid]
        if new_cfg and new_cfg not in existing_cfg:
            row["config_rule_ids"] = (existing_cfg + ";" + new_cfg).strip(";")
        updated_count += 1

print(f"  Updated {updated_count} rows in coverage matrix")

with open(MATRIX_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
print(f"  Saved updated matrix to {MATRIX_FILE}")


# ── Remove covered rules from gap file ───────────────────────────────────
print("\n=== Updating gap file ===")

gap_rows = []
removed = 0
with open(GAP_FILE) as f:
    reader = csv.DictReader(f)
    gap_fieldnames = reader.fieldnames
    for row in reader:
        if row["csp"] == "azure" and row["catalog_rule_id"] in covered_rule_ids:
            removed += 1
            continue  # Remove this row
        gap_rows.append(row)

print(f"  Removed {removed} covered rules from gap file")
print(f"  Remaining Azure gaps: {sum(1 for r in gap_rows if r['csp'] == 'azure')}")

with open(GAP_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=gap_fieldnames)
    writer.writeheader()
    writer.writerows(gap_rows)
print(f"  Saved updated gap file")


# ── Final summary ─────────────────────────────────────────────────────────
remaining_azure = sum(1 for r in gap_rows if r["csp"] == "azure")
print(f"\n=== FINAL AZURE GAP SUMMARY ===")
print(f"  Total catalog rules: 1734")
print(f"  Covered: {1734 - remaining_azure}")
print(f"  Gap file entries: {remaining_azure}")
print(f"    → Of which UNCERTAIN (need review): {len(all_uncertain)}")
print(f"    → True confirmed gaps: {len(all_true_gap)}")
