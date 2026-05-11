"""
Builds a comprehensive per-CSP gap file from final_compliance_rules_mapped.csv.

For each (compliance_id, csp) pair where the compliance has a check but no mapped rule,
emit a row with:
  - the original check_name(s) from compliance_agent
  - a SUGGESTED rule_id following catalog naming convention (e.g. aws.qldb.ledger.encryption_at_rest)
  - the framework for prioritization

This produces the definitive list of NEW detection rules to build.
"""
import csv
import re
from pathlib import Path

BASE = Path("/Users/apple/Desktop/compliance_Database/final_compliance_rules")
SRC = BASE / "final_compliance_rules_mapped.csv"
OUT_RULES = BASE / "new_rules_to_build.csv"
OUT_BY_CSP = BASE / "new_rules_by_csp"
OUT_BY_CSP.mkdir(exist_ok=True)

# Also load rejected mappings so we can mark which checks were tried but rejected
MAPPING_DIR = BASE / "rule_mapping"
CSPS = ["aws", "azure", "gcp", "oracle", "ibm", "alicloud", "k8s"]

# Priority score per framework (1=highest)
FRAMEWORK_PRIORITY = {
    "CIS_AWS": 1, "CIS_AZURE": 1, "CIS_GCP": 1, "CIS_OCI": 1,
    "CIS_IBM": 1, "CIS_ALICLOUD": 1, "CIS_K8S": 1,
    "NIST_800_53": 2, "FedRAMP_Moderate": 2, "PCI_DSS": 2,
    "HIPAA": 2, "SOC2": 2, "ISO27001_2022": 2,
    "NIST_800_171": 3, "CANADA_PBMM": 3, "CISA_CE": 3,
    "RBI_BANK": 4, "RBI_NBFC": 4, "GDPR": 4,
}


def suggest_rule_id(check_name: str, csp: str) -> str:
    """
    Convert a compliance_agent check name like `aws_iam_user_mfa_enabled`
    into a catalog-style rule_id like `aws.iam.user.mfa_enabled`.

    Heuristic: take the first 3 underscore-tokens as service hierarchy (csp.service.resource),
    and join the rest with underscores as the check name.
    """
    if not check_name:
        return ""
    parts = check_name.split("_")
    if len(parts) < 3:
        return check_name.replace("_", ".")

    # CSP normalization
    csp_prefix = parts[0]
    if csp == "oracle" and csp_prefix == "oracle":
        csp_prefix = "oci"
    if csp == "k8s" and csp_prefix == "k8s":
        pass

    # Take service + resource
    service = parts[1]
    resource = parts[2]
    rest = "_".join(parts[3:]) if len(parts) > 3 else resource

    # If resource is a common compound (e.g., 'ebs_volume' → keep)
    return f"{csp_prefix}.{service}.{resource}.{rest}"


# ── Load mapped compliance + mappings ─────────────────────────────────────
mapped_rows = list(csv.DictReader(open(SRC)))
print(f"Compliance rows: {len(mapped_rows)}")

# Load per-csp mapping status (for detecting 'rejected' vs 'not attempted')
check_mapping_status = {csp: {} for csp in CSPS}
for csp in CSPS:
    fp = MAPPING_DIR / f"{csp}_check_to_rule.csv"
    if fp.exists():
        with open(fp) as f:
            for row in csv.DictReader(f):
                check_mapping_status[csp][row["check_name"]] = {
                    "method": row.get("method", ""),
                    "matched": row.get("matched_rule_ids", ""),
                }


# ── Build per-CSP per-check gap entries ───────────────────────────────────
new_rules = []

for row in mapped_rows:
    if (row.get("automation_type") or "").strip().lower() != "automated":
        continue  # Only automated rules need detection rules

    comp_id = row["unique_compliance_id"]
    framework = row["framework"]
    title = row.get("title", "")
    control_id = row.get("control_id", "")
    priority = FRAMEWORK_PRIORITY.get(framework, 5)

    for csp in CSPS:
        checks_raw = (row.get(f"{csp}_checks") or "").strip()
        mapped = (row.get(f"{csp}_mapped_rule_ids") or "").strip()
        if not checks_raw:
            continue  # framework doesn't require a check for this CSP

        check_names = [c.strip() for c in checks_raw.split(";") if c.strip()]

        # For each check name, figure out if it was mapped or is a gap
        unmapped_checks = []
        for c in check_names:
            status = check_mapping_status[csp].get(c, {})
            if status.get("matched"):
                continue  # this check got mapped
            unmapped_checks.append(c)

        if not unmapped_checks:
            continue  # all checks for this CSP mapped OK

        # Emit one new-rule row per unmapped check
        for c in unmapped_checks:
            suggested = suggest_rule_id(c, csp)
            new_rules.append({
                "csp": csp,
                "unique_compliance_id": comp_id,
                "framework": framework,
                "control_id": control_id,
                "title": title[:200],
                "missing_check_name": c,
                "suggested_rule_id": suggested,
                "priority": priority,
                "rule_type": "config",  # default; CIEM needed for some
                "notes": "Generated from compliance_agent check name; refine during rule development",
            })


# ── Write master file ─────────────────────────────────────────────────────
fields = ["csp", "unique_compliance_id", "framework", "control_id", "title",
          "missing_check_name", "suggested_rule_id", "priority", "rule_type", "notes"]

# Sort: priority ASC, csp, framework, compliance_id
new_rules.sort(key=lambda r: (r["priority"], r["csp"], r["framework"], r["unique_compliance_id"]))

with open(OUT_RULES, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(new_rules)

# ── Per-CSP split files ───────────────────────────────────────────────────
from collections import defaultdict
by_csp = defaultdict(list)
for r in new_rules:
    by_csp[r["csp"]].append(r)

for csp, rows in by_csp.items():
    fp = OUT_BY_CSP / f"{csp}_new_rules_needed.csv"
    with open(fp, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

# ── Summary ───────────────────────────────────────────────────────────────
from collections import Counter
print(f"\n═══════ NEW RULES TO BUILD ═══════")
print(f"Total per-CSP rule gaps: {len(new_rules)}")
print(f"Master file: {OUT_RULES}")
print()

print(f"{'CSP':<10} {'count':>7}")
print("-" * 20)
for csp in CSPS:
    c = len(by_csp.get(csp, []))
    print(f"{csp:<10} {c:>7}")
print()

# Breakdown by framework
fw_counts = Counter(r["framework"] for r in new_rules)
print(f"Top 10 frameworks needing rules:")
for fw, n in fw_counts.most_common(10):
    print(f"  {fw:<25} {n:>5}")

# Unique suggested rule IDs (dedup across compliance rows)
unique_rules = {r["suggested_rule_id"] for r in new_rules}
print(f"\nUnique suggested rule IDs (dedup): {len(unique_rules)}")

# Sample output
print(f"\nSample rows (AWS QLDB):")
for r in new_rules:
    if "qldb" in r["suggested_rule_id"].lower():
        print(f"  [{r['csp']}] {r['unique_compliance_id']}")
        print(f"    check:     {r['missing_check_name']}")
        print(f"    suggested: {r['suggested_rule_id']}")
        print()
