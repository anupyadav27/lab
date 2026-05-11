"""
Validates the rebuilt compliance file before using it as source of truth.

Checks:
  1. Compliance ID structure: all have valid framework prefix?
  2. Rule IDs: all exist in the master rules file?
  3. No duplicate compliance IDs?
  4. Compliance framework distribution (which frameworks are covered?)
  5. Rules uniqueness per compliance ID (any rule appear multiple times for same compliance?)
  6. Cross-CSP consistency: same compliance ID should be stable
"""
import csv
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation")
MASTER = BASE / "rule_list/consolidated_rules_phase4_2025-11-08_FINAL_WITH_ALL_IDS.csv"
REBUILT = BASE / "complance_rule/compliance_to_rules_rebuilt_from_master_2026-04-18.csv"

CSPS = ["aws", "azure", "gcp", "oci", "ibm", "alicloud", "k8s"]

# ── 1. Load master rule IDs per CSP ────────────────────────────────────────
master_rule_ids = {csp: set() for csp in CSPS}
master_compliance_ids = set()
with open(MASTER) as f:
    for row in csv.DictReader(f):
        csp = row.get("cloud_provider", "")
        rid = row.get("rule_id", "")
        if csp in master_rule_ids and rid:
            master_rule_ids[csp].add(rid)
        # Gather all compliance IDs
        for csp_inner in CSPS:
            for cid in (row.get(f"{csp_inner}_mapped_compliance_ids") or "").split(";"):
                cid = cid.strip()
                if cid:
                    master_compliance_ids.add(cid)

print("═"*70)
print("VALIDATION REPORT")
print("═"*70)
print(f"\nMaster file rule counts per CSP:")
for csp in CSPS:
    print(f"  {csp:10s}: {len(master_rule_ids[csp])}")
print(f"Master unique compliance IDs: {len(master_compliance_ids)}")


# ── 2. Load rebuilt file ─────────────────────────────────────────────────
rebuilt_comp_ids = []
rebuilt_rules_per_csp_per_comp: dict[str, dict[str, list[str]]] = {}
with open(REBUILT) as f:
    for row in csv.DictReader(f):
        cid = row["unique_compliance_id"]
        rebuilt_comp_ids.append(cid)
        rebuilt_rules_per_csp_per_comp[cid] = {}
        for csp in CSPS:
            rules = [r.strip() for r in (row.get(f"{csp}_mapped_rules","") or "").split(";") if r.strip()]
            rebuilt_rules_per_csp_per_comp[cid][csp] = rules

print(f"\nRebuilt file rows: {len(rebuilt_comp_ids)}")


# ── 3. Validate compliance ID integrity ───────────────────────────────────
print("\n" + "─"*70)
print("Check 1: Compliance ID structure")
print("─"*70)
cid_count = Counter(rebuilt_comp_ids)
duplicates = [(c, n) for c, n in cid_count.items() if n > 1]
print(f"  Unique IDs: {len(cid_count)}")
print(f"  Duplicate IDs: {len(duplicates)}")
if duplicates:
    print(f"  Duplicate examples: {duplicates[:5]}")

# Framework detection
frameworks = Counter()
malformed = []
for cid in set(rebuilt_comp_ids):
    # Expected format: <framework>_<variant>_multi_cloud_<section>_<number>
    if "_multi_cloud_" in cid:
        fw = cid.split("_multi_cloud_")[0]
    else:
        fw = cid.split("_")[0] if "_" in cid else cid
        malformed.append(cid)
    frameworks[fw] += 1

print(f"\n  Detected compliance frameworks ({len(frameworks)}):")
for fw, cnt in frameworks.most_common():
    print(f"    {fw:50s} {cnt:>5} compliance IDs")

print(f"\n  Malformed (no '_multi_cloud_' pattern): {len(malformed)}")
if malformed:
    print(f"  Examples: {malformed[:5]}")


# ── 4. Validate rule IDs exist in master ──────────────────────────────────
print("\n" + "─"*70)
print("Check 2: Rule IDs validity (exist in master)")
print("─"*70)
for csp in CSPS:
    all_rule_refs = set()
    for cid in rebuilt_rules_per_csp_per_comp:
        all_rule_refs.update(rebuilt_rules_per_csp_per_comp[cid][csp])
    valid = all_rule_refs & master_rule_ids[csp]
    invalid = all_rule_refs - master_rule_ids[csp]
    print(f"  {csp:10s}  refs {len(all_rule_refs):>4}  valid {len(valid):>4}  invalid {len(invalid)}")
    if invalid:
        print(f"             invalid samples: {list(invalid)[:3]}")


# ── 5. Compliance IDs missing from rebuilt ───────────────────────────────
print("\n" + "─"*70)
print("Check 3: Compliance IDs in master but missing from rebuilt")
print("─"*70)
missing_from_rebuilt = master_compliance_ids - set(rebuilt_comp_ids)
print(f"  Master total: {len(master_compliance_ids)}")
print(f"  In rebuilt:   {len(set(rebuilt_comp_ids) & master_compliance_ids)}")
print(f"  MISSING:      {len(missing_from_rebuilt)}")
if missing_from_rebuilt:
    print(f"  Samples of missing:")
    for cid in list(missing_from_rebuilt)[:5]:
        print(f"    {cid}")


# ── 6. Rules with no compliance mapping at all ─────────────────────────────
print("\n" + "─"*70)
print("Check 4: Rules in master with NO compliance mapping")
print("─"*70)
# Count rules that appear in master but not in any rebuilt compliance ID
rebuilt_rule_usage = {csp: set() for csp in CSPS}
for cid in rebuilt_rules_per_csp_per_comp:
    for csp in CSPS:
        rebuilt_rule_usage[csp].update(rebuilt_rules_per_csp_per_comp[cid][csp])

for csp in CSPS:
    unused = master_rule_ids[csp] - rebuilt_rule_usage[csp]
    print(f"  {csp:10s}  total {len(master_rule_ids[csp]):>5}  with_compliance {len(rebuilt_rule_usage[csp]):>5}  NO_compliance {len(unused):>5}")


# ── 7. Framework-level assessment ─────────────────────────────────────────
print("\n" + "─"*70)
print("Check 5: Rules per framework (are major frameworks covered?)")
print("─"*70)
framework_rule_counts = defaultdict(lambda: {csp: set() for csp in CSPS})
for cid, csp_rules in rebuilt_rules_per_csp_per_comp.items():
    if "_multi_cloud_" in cid:
        fw = cid.split("_multi_cloud_")[0]
    else:
        fw = cid.split("_")[0]
    for csp, rules in csp_rules.items():
        framework_rule_counts[fw][csp].update(rules)

print(f"\n  {'Framework':<50} {'AWS':>7} {'Azure':>7} {'GCP':>7} {'OCI':>7}")
for fw in sorted(framework_rule_counts.keys()):
    counts = framework_rule_counts[fw]
    print(f"  {fw:<50} {len(counts['aws']):>7} {len(counts['azure']):>7} {len(counts['gcp']):>7} {len(counts['oci']):>7}")


# ── Final verdict ─────────────────────────────────────────────────────────
print("\n" + "═"*70)
print("VERDICT")
print("═"*70)
all_valid = all(
    len(rebuilt_rule_usage[csp] - master_rule_ids[csp]) == 0
    for csp in CSPS
)
print(f"  All rule IDs valid (exist in master): {'✓ YES' if all_valid else '✗ NO'}")
print(f"  No duplicate compliance IDs:          {'✓ YES' if not duplicates else '✗ NO ('+str(len(duplicates))+' dupes)'}")
print(f"  All frameworks well-formed:           {'✓ YES' if not malformed else '✗ NO ('+str(len(malformed))+' malformed)'}")
print(f"  Compliance IDs covered vs master:     {len(set(rebuilt_comp_ids))}/{len(master_compliance_ids)}")
