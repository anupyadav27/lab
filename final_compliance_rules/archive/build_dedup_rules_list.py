"""
Creates the deduplicated 'unique new rules to build' list.

Input:  new_rules_to_build.csv  (5,705 per-compliance entries)
Output: new_rules_deduplicated.csv  (unique suggested_rule_ids with list of compliance_ids)
"""
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path("/Users/apple/Desktop/compliance_Database/final_compliance_rules")
SRC = BASE / "new_rules_to_build.csv"
OUT = BASE / "new_rules_deduplicated.csv"

# Group by suggested_rule_id
groups = defaultdict(lambda: {
    "suggested_rule_id": "",
    "csp": "",
    "missing_check_name": "",
    "compliance_ids": set(),
    "frameworks": set(),
    "titles": set(),
    "priority": 5,
})

with open(SRC) as f:
    for row in csv.DictReader(f):
        rid = row["suggested_rule_id"]
        g = groups[rid]
        g["suggested_rule_id"] = rid
        g["csp"] = row["csp"]
        g["missing_check_name"] = row["missing_check_name"]
        g["compliance_ids"].add(row["unique_compliance_id"])
        g["frameworks"].add(row["framework"])
        g["titles"].add(row["title"][:80])
        try:
            p = int(row["priority"])
            if p < g["priority"]:
                g["priority"] = p
        except ValueError:
            pass

rows_out = []
for rid, g in groups.items():
    rows_out.append({
        "suggested_rule_id": rid,
        "csp": g["csp"],
        "missing_check_name": g["missing_check_name"],
        "compliance_count": len(g["compliance_ids"]),
        "framework_count": len(g["frameworks"]),
        "frameworks": ";".join(sorted(g["frameworks"])),
        "priority": g["priority"],
        "sample_title": sorted(g["titles"])[0] if g["titles"] else "",
        "compliance_ids": ";".join(sorted(g["compliance_ids"])[:5]) + (f";...(+{len(g['compliance_ids'])-5} more)" if len(g['compliance_ids']) > 5 else ""),
    })

# Sort: priority, compliance_count DESC, csp
rows_out.sort(key=lambda r: (r["priority"], -r["compliance_count"], r["csp"]))

fields = ["suggested_rule_id", "csp", "missing_check_name", "compliance_count",
          "framework_count", "frameworks", "priority", "sample_title", "compliance_ids"]
with open(OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows_out)

print(f"Unique rules to build: {len(rows_out)}")
print(f"Saved: {OUT}")

# CSP + priority summary
from collections import Counter
csp_counts = Counter((r["csp"], r["priority"]) for r in rows_out)
print(f"\nBreakdown by CSP × Priority (P1=CIS, P2=NIST/FedRAMP/PCI/HIPAA/SOC2/ISO):")
print(f"{'CSP':<10} {'P1':>5} {'P2':>5} {'P3':>5} {'P4':>5} {'P5':>5}")
for csp in ["aws","azure","gcp","oracle","ibm","alicloud","k8s"]:
    line = f"{csp:<10}"
    for p in [1,2,3,4,5]:
        line += f" {csp_counts.get((csp,p),0):>5}"
    print(line)

# Top 10 highest-impact rules (most compliance_ids reference them)
print(f"\nTop 10 highest-impact new rules (most frameworks reference them):")
for r in rows_out[:10]:
    print(f"  [{r['csp']}/P{r['priority']}] {r['suggested_rule_id']}")
    print(f"     → {r['compliance_count']} compliance refs across {r['framework_count']} frameworks")
