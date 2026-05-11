"""
Consolidates all compliance framework files from /compliance_agent/ into a single
authoritative compliance rules registry.

Output: final_compliance_rules.csv with one row per compliance requirement across
all 13 frameworks. Includes per-CSP check names (from the compliance_agent AI
generation), ready to be AI-mapped to catalog rule_ids later.

Schema (unified across 13 frameworks):
  unique_compliance_id    — normalized, e.g. cis_aws_1.19, nist_800_53_rev5_AC-2
  framework               — CIS_AWS | CIS_AZURE | NIST_800_53 | ...
  framework_version       — benchmark version if known
  control_id              — raw ID from source file
  section                 — section/family (if provided)
  title                   — control title
  description             — description (CIS only; blank for others)
  automation_type         — Automated | Manual
  {csp}_checks            — semicolon-joined check function names per CSP
  source_file             — path to the origin file
"""
import csv
import re
from pathlib import Path

AGENT_BASE = Path("/Users/apple/Desktop/compliance_Database/compliance_agent")
OUT_DIR = Path("/Users/apple/Desktop/compliance_Database/final_compliance_rules")
OUT = OUT_DIR / "final_compliance_rules.csv"


def _clean_id(s: str) -> str:
    """Normalize a control_id to a safe, lowercase identifier (keeps digits/dots)."""
    if not s:
        return ""
    s = s.strip()
    # Replace spaces, hyphens, parens with underscores
    s = re.sub(r"[\s\-()]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def _parse_checks(val: str) -> str:
    """Normalize check list: semicolon-separated, no blanks, unique, stable order."""
    if not val:
        return ""
    parts = [p.strip() for p in val.replace(",", ";").split(";")]
    seen = []
    for p in parts:
        if p and p not in seen:
            seen.append(p)
    return ";".join(seen)


FIELDNAMES = [
    "unique_compliance_id", "framework", "framework_version",
    "control_id", "section", "title", "description", "automation_type",
    "aws_checks", "azure_checks", "gcp_checks", "oracle_checks",
    "ibm_checks", "alicloud_checks", "k8s_checks",
    "source_file",
]


def _empty_row() -> dict:
    return {k: "" for k in FIELDNAMES}


# ── Per-framework loaders ─────────────────────────────────────────────────
def load_cis_aws() -> list[dict]:
    """CIS AWS: each row is one control with a single program_name (AWS check)."""
    out = []
    fp = AGENT_BASE / "cis_compliance_agent/aws_agent/aws_controls_FINAL_20251031_165652.csv"
    with open(fp) as f:
        for row in csv.DictReader(f):
            cid = (row.get("id") or "").strip()
            src = (row.get("source") or "").strip()
            if not cid:
                continue
            # Extract benchmark version from source (e.g., "CIS_AWS_End_User_..._v1.1.0")
            version_match = re.search(r"v(\d+[._]\d+[._]?\d*)", src)
            version = version_match.group(1).replace("_", ".") if version_match else ""

            rec = _empty_row()
            rec["unique_compliance_id"] = f"cis_aws_{_clean_id(cid)}"
            rec["framework"] = "CIS_AWS"
            rec["framework_version"] = version
            rec["control_id"] = cid
            rec["section"] = (row.get("section") or "").strip()
            rec["title"] = (row.get("title") or "").strip()
            rec["description"] = (row.get("description") or "").strip()[:500]
            rec["automation_type"] = (row.get("final_approach") or "").strip()
            rec["aws_checks"] = _parse_checks(row.get("program_name") or "")
            rec["source_file"] = str(fp.relative_to(AGENT_BASE))
            out.append(rec)
    return out


def load_cis_azure() -> list[dict]:
    return _load_cis_single("azure_agent/azure_controls_FINAL_20251031_201346.csv",
                             "CIS_AZURE", "cis_azure", "azure_checks")


def _load_cis_single(rel_path: str, framework: str, prefix: str, csp_col: str) -> list[dict]:
    """Generic loader for CIS agent files with single program_name per row."""
    out = []
    fp = AGENT_BASE / "cis_compliance_agent" / rel_path
    with open(fp) as f:
        for row in csv.DictReader(f):
            cid = (row.get("id") or "").strip()
            src = (row.get("source") or "").strip()
            if not cid:
                continue
            version_match = re.search(r"v(\d+[._]\d+[._]?\d*)", src)
            version = version_match.group(1).replace("_", ".") if version_match else ""

            rec = _empty_row()
            rec["unique_compliance_id"] = f"{prefix}_{_clean_id(cid)}"
            rec["framework"] = framework
            rec["framework_version"] = version
            rec["control_id"] = cid
            rec["section"] = (row.get("section") or "").strip()
            rec["title"] = (row.get("title") or "").strip()
            rec["description"] = (row.get("description") or "").strip()[:500]
            rec["automation_type"] = (row.get("final_approach") or "").strip()
            rec[csp_col] = _parse_checks(row.get("program_name") or "")
            rec["source_file"] = str(fp.relative_to(AGENT_BASE))
            out.append(rec)
    return out


def _load_multi_csp(fp: Path, framework: str, id_col: str, prefix: str,
                     version: str = "", extra: dict | None = None) -> list[dict]:
    """Generic loader for frameworks with AWS_Checks/Azure_Checks/... columns."""
    out = []
    extra = extra or {}
    with open(fp) as f:
        for row in csv.DictReader(f):
            cid = (row.get(id_col) or "").strip()
            if not cid:
                continue
            rec = _empty_row()
            rec["unique_compliance_id"] = f"{prefix}_{_clean_id(cid)}"
            rec["framework"] = framework
            rec["framework_version"] = version
            rec["control_id"] = cid
            rec["section"] = (row.get("Section") or row.get("Family_Code") or
                              row.get("Category") or row.get("FedRAMP_Baseline") or "").strip()
            rec["title"] = (row.get("Title") or row.get("title") or "").strip()
            rec["automation_type"] = (row.get("Automation_Type") or
                                       row.get("automation_type") or "").strip()
            for csp_col, target in [
                ("AWS_Checks", "aws_checks"), ("aws_checks", "aws_checks"),
                ("Azure_Checks", "azure_checks"), ("azure_checks", "azure_checks"),
                ("GCP_Checks", "gcp_checks"), ("gcp_checks", "gcp_checks"),
                ("Oracle_Checks", "oracle_checks"), ("oracle_checks", "oracle_checks"),
                ("IBM_Checks", "ibm_checks"), ("ibm_checks", "ibm_checks"),
                ("Alicloud_Checks", "alicloud_checks"), ("alicloud_checks", "alicloud_checks"),
                ("K8s_Checks", "k8s_checks"), ("k8s_checks", "k8s_checks"),
            ]:
                if csp_col in row:
                    val = row.get(csp_col) or ""
                    if val:
                        existing = rec[target]
                        merged = _parse_checks(f"{existing};{val}") if existing else _parse_checks(val)
                        rec[target] = merged
            for k, v in extra.items():
                rec[k] = v
            rec["source_file"] = str(fp.relative_to(AGENT_BASE))
            out.append(rec)
    return out


LOADERS = [
    lambda: load_cis_aws(),
    lambda: load_cis_azure(),
    lambda: _load_cis_single("gcp_agent/gcp_controls_FINAL_20251031_201244.csv",
                              "CIS_GCP", "cis_gcp", "gcp_checks"),
    lambda: _load_cis_single("ibm_agent/ibm_controls_FINAL_20251031_215936.csv",
                              "CIS_IBM", "cis_ibm", "ibm_checks"),
    lambda: _load_cis_single("oracle_agent/oracle_controls_FINAL_20251031_220049.csv",
                              "CIS_OCI", "cis_oci", "oracle_checks"),
    lambda: _load_cis_single("alicloud_agent/alicloud_controls_FINAL_20251031_171157.csv",
                              "CIS_ALICLOUD", "cis_alicloud", "alicloud_checks"),
    lambda: _load_cis_single("k8s_agent/k8s_controls_FINAL_20251031_220854.csv",
                              "CIS_K8S", "cis_k8s", "k8s_checks"),
    lambda: _load_multi_csp(AGENT_BASE / "nist_complaince_agent/NIST_controls_with_checks.csv",
                             "NIST_800_53", "Control_ID", "nist_800_53_rev5", "rev5"),
    lambda: _load_multi_csp(AGENT_BASE / "nist_800_171/NIST_800-171_R2_controls_with_checks.csv",
                             "NIST_800_171", "Requirement_ID", "nist_800_171_r2", "R2"),
    lambda: _load_multi_csp(AGENT_BASE / "hipaa/HIPAA_controls_with_checks.csv",
                             "HIPAA", "Control_ID", "hipaa", ""),
    lambda: _load_multi_csp(AGENT_BASE / "pci_compliance_agent/PCI_controls_with_checks.csv",
                             "PCI_DSS", "id", "pci_dss_v4", "v4.0.1"),
    lambda: _load_multi_csp(AGENT_BASE / "soc2/SOC2_controls_with_checks.csv",
                             "SOC2", "Control_ID", "soc2", ""),
    lambda: _load_multi_csp(AGENT_BASE / "iso27001-2022/ISO27001_2022_controls_with_checks.csv",
                             "ISO27001_2022", "Control_ID", "iso27001_2022", "2022"),
    lambda: _load_multi_csp(AGENT_BASE / "FedRamp/FedRAMP_controls_with_checks.csv",
                             "FedRAMP_Moderate", "Control_ID", "fedramp_moderate", "Moderate"),
    lambda: _load_multi_csp(AGENT_BASE / "canada_pbmm/CANADA_PBMM_controls_with_checks.csv",
                             "CANADA_PBMM", "Control_ID", "canada_pbmm_moderate", "Moderate"),
    lambda: _load_multi_csp(AGENT_BASE / "cisa_ce/CISA_CE_controls_with_checks.csv",
                             "CISA_CE", "Control_ID", "cisa_ce_v1", "v1"),
    lambda: _load_multi_csp(AGENT_BASE / "rbi_bank/RBI_BANK_controls_with_checks.csv",
                             "RBI_BANK", "Control_ID", "rbi_bank", ""),
    lambda: _load_multi_csp(AGENT_BASE / "rbi_nbfc/RBI_NBFC_controls_with_checks.csv",
                             "RBI_NBFC", "Control_ID", "rbi_nbfc", ""),
    lambda: _load_multi_csp(AGENT_BASE / "gdpr/GDPR_controls_with_checks.csv",
                             "GDPR", "Article_ID", "gdpr", ""),
]


all_rows: list[dict] = []
for load in LOADERS:
    rows = load()
    if rows:
        fw = rows[0]["framework"]
        print(f"Loaded {len(rows):>4} rows from {fw}")
        all_rows.extend(rows)

print(f"\nTotal compliance requirements: {len(all_rows)}")


# ── Deduplicate by unique_compliance_id ────────────────────────────────────
seen_ids: dict[str, dict] = {}
dup_count = 0
for row in all_rows:
    cid = row["unique_compliance_id"]
    if cid in seen_ids:
        dup_count += 1
        # Merge check lists from the duplicate
        for k in ["aws_checks", "azure_checks", "gcp_checks", "oracle_checks",
                  "ibm_checks", "alicloud_checks", "k8s_checks"]:
            existing = seen_ids[cid][k]
            new = row[k]
            if new:
                seen_ids[cid][k] = _parse_checks(f"{existing};{new}" if existing else new)
    else:
        seen_ids[cid] = row

print(f"Duplicates merged: {dup_count}")
print(f"Unique compliance IDs: {len(seen_ids)}")


# ── Write output ───────────────────────────────────────────────────────────
with open(OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    for cid in sorted(seen_ids.keys()):
        writer.writerow(seen_ids[cid])

print(f"\n✓ Wrote: {OUT}")


# ── Summary stats ─────────────────────────────────────────────────────────
from collections import Counter
fw_counts = Counter(r["framework"] for r in seen_ids.values())
print(f"\nFramework breakdown:")
for fw, n in fw_counts.most_common():
    print(f"  {fw:25s} {n:>5}")

csps_with_checks = {
    "aws": sum(1 for r in seen_ids.values() if r["aws_checks"]),
    "azure": sum(1 for r in seen_ids.values() if r["azure_checks"]),
    "gcp": sum(1 for r in seen_ids.values() if r["gcp_checks"]),
    "oracle": sum(1 for r in seen_ids.values() if r["oracle_checks"]),
    "ibm": sum(1 for r in seen_ids.values() if r["ibm_checks"]),
    "alicloud": sum(1 for r in seen_ids.values() if r["alicloud_checks"]),
    "k8s": sum(1 for r in seen_ids.values() if r["k8s_checks"]),
}
print(f"\nCompliance IDs with at least one check per CSP:")
for csp, n in csps_with_checks.items():
    print(f"  {csp:10s} {n:>5} ({n/len(seen_ids)*100:.1f}%)")

manual_count = sum(1 for r in seen_ids.values()
                   if r["automation_type"].lower() == "manual")
auto_count = sum(1 for r in seen_ids.values()
                 if r["automation_type"].lower() == "automated")
print(f"\nAutomation type:")
print(f"  Automated: {auto_count}")
print(f"  Manual:    {manual_count}")
print(f"  Other/blank: {len(seen_ids) - manual_count - auto_count}")
