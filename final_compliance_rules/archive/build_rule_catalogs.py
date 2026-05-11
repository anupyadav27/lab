"""
Builds authoritative rule catalogs by parsing threat-engine YAML files.

Produces per CSP:
  rule_catalogs/{csp}_rule_check.csv — config assertion rules
  rule_catalogs/{csp}_rule_ciem.csv  — CIEM log-correlation rules

Source:
  /Users/apple/Desktop/threat-engine/catalog/rule/{csp}_rule_check/**/*.yaml
  /Users/apple/Desktop/threat-engine/catalog/rule/{csp}_rule_ciem/**/*.yaml

Each rule row captures:
  rule_id, provider, service, category, severity, title, description,
  check_type, source_file
"""
import csv
import yaml
from pathlib import Path

CATALOG = Path("/Users/apple/Desktop/threat-engine/catalog/rule")
OUT_DIR = Path("/Users/apple/Desktop/compliance_Database/final_compliance_rules/rule_catalogs")
OUT_DIR.mkdir(exist_ok=True)

CSPS = ["aws", "azure", "gcp", "oci", "ibm", "alicloud", "k8s"]

CHECK_FIELDS = [
    "rule_id", "provider", "service", "category", "severity",
    "title", "description", "check_type", "source_file",
]

CIEM_FIELDS = [
    "rule_id", "provider", "service", "category", "severity",
    "title", "description", "check_type", "threat_category",
    "mitre_tactics", "mitre_techniques", "risk_score",
    "domain", "action_category", "posture_category",
    "source_file",
]


def _parse_check_yaml(path: Path) -> list[dict]:
    """Parse a `*.checks.yaml` file (config rules) into flat rule rows."""
    try:
        data = yaml.safe_load(path.read_text())
    except Exception as e:
        print(f"  ⚠ yaml error: {path.name}: {e}")
        return []
    if not isinstance(data, dict):
        return []

    provider = (data.get("provider") or "").strip()
    service = (data.get("service") or "").strip()
    checks = data.get("checks") or []
    if not isinstance(checks, list):
        return []

    rows = []
    for c in checks:
        if not isinstance(c, dict):
            continue
        rid = (c.get("rule_id") or "").strip()
        if not rid:
            continue
        # Derive category: first dot-segment after provider prefix
        parts = rid.split(".")
        category = parts[2] if len(parts) >= 3 else ""
        rows.append({
            "rule_id": rid,
            "provider": provider,
            "service": service,
            "category": category,
            "severity": (c.get("severity") or "").strip(),
            "title": (c.get("title") or "").strip()[:300],
            "description": (c.get("description") or "").strip()[:500],
            "check_type": "config",
            "source_file": str(path.relative_to(CATALOG)),
        })
    return rows


def _parse_ciem_yaml(path: Path) -> list[dict]:
    """Parse a CIEM YAML file (single-rule format) into a rule row."""
    try:
        data = yaml.safe_load(path.read_text())
    except Exception as e:
        print(f"  ⚠ yaml error: {path.name}: {e}")
        return []
    if not isinstance(data, dict):
        return []

    rid = (data.get("rule_id") or "").strip()
    if not rid:
        return []

    return [{
        "rule_id": rid,
        "provider": (data.get("provider") or "").strip(),
        "service": (data.get("service") or "").strip(),
        "category": path.parent.name,
        "severity": str(data.get("severity") or "").strip(),
        "title": (data.get("title") or "").strip()[:300],
        "description": (data.get("description") or "").strip()[:500],
        "check_type": (data.get("check_type") or "ciem").strip(),
        "threat_category": (data.get("threat_category") or "").strip(),
        "mitre_tactics": ";".join(data.get("mitre_tactics") or []),
        "mitre_techniques": ";".join(data.get("mitre_techniques") or []),
        "risk_score": str(data.get("risk_score") or "").strip(),
        "domain": (data.get("domain") or "").strip(),
        "action_category": (data.get("action_category") or "").strip(),
        "posture_category": (data.get("posture_category") or "").strip(),
        "source_file": str(path.relative_to(CATALOG)),
    }]


summary = {}
for csp in CSPS:
    print(f"\n━━━━━━━━━━━━━━━━━━ {csp.upper()} ━━━━━━━━━━━━━━━━━━")

    # ── Config checks ──────────────────────────────────────────────────
    check_dir = CATALOG / f"{csp}_rule_check"
    check_rows = []
    seen_ids = set()
    if check_dir.exists():
        for yaml_file in sorted(check_dir.rglob("*.yaml")):
            # Skip full_scope aggregated files (contain duplicates of per-service rules)
            if "full_scope" in yaml_file.name.lower():
                continue
            # Skip discovery-only files (no 'checks:' key)
            if yaml_file.name.endswith(".discovery.yaml"):
                continue
            rows = _parse_check_yaml(yaml_file)
            for r in rows:
                if r["rule_id"] in seen_ids:
                    continue
                seen_ids.add(r["rule_id"])
                check_rows.append(r)

    out_check = OUT_DIR / f"{csp}_rule_check.csv"
    with open(out_check, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CHECK_FIELDS)
        writer.writeheader()
        writer.writerows(check_rows)
    print(f"  rule_check:  {len(check_rows):>5} unique rules → {out_check.name}")

    # ── CIEM rules ──────────────────────────────────────────────────────
    ciem_dir = CATALOG / f"{csp}_rule_ciem"
    ciem_rows = []
    seen_ids_ciem = set()
    if ciem_dir.exists():
        for yaml_file in sorted(ciem_dir.rglob("*.yaml")):
            rows = _parse_ciem_yaml(yaml_file)
            for r in rows:
                if r["rule_id"] in seen_ids_ciem:
                    continue
                seen_ids_ciem.add(r["rule_id"])
                ciem_rows.append(r)

    out_ciem = OUT_DIR / f"{csp}_rule_ciem.csv"
    with open(out_ciem, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CIEM_FIELDS)
        writer.writeheader()
        writer.writerows(ciem_rows)
    print(f"  rule_ciem:   {len(ciem_rows):>5} unique rules → {out_ciem.name}")

    summary[csp] = {"check": len(check_rows), "ciem": len(ciem_rows)}


print("\n━━━━━━━━━━━━━━━━━━ SUMMARY ━━━━━━━━━━━━━━━━━━")
print(f"{'CSP':<10} {'rule_check':>12} {'rule_ciem':>11} {'total':>8}")
total_check = total_ciem = 0
for csp, s in summary.items():
    print(f"{csp:<10} {s['check']:>12} {s['ciem']:>11} {s['check']+s['ciem']:>8}")
    total_check += s['check']
    total_ciem += s['ciem']
print(f"{'TOTAL':<10} {total_check:>12} {total_ciem:>11} {total_check+total_ciem:>8}")
