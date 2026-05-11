"""
Build a full catalog coverage matrix: for every aws_rules.csv row, show
which YAML config rules cover it and which CIEM rules cover it.

Sources:
  aws_rules.csv                  — 2,313 catalog rows (ground truth)
  aws_unified_ai_mapping.csv     — YAML → (catalog, CIEM) AI matches
  aws_ciem_rules_consolidated.json — 493 CIEM rules with compliance IDs

Config coverage:
  Inverted from aws_unified_ai_mapping: any YAML rule with catalog_confidence
  high or medium pointing at this catalog row counts as "config covered".

CIEM direct coverage (two signals combined):
  1. Compliance-ID Jaccard: shared compliance IDs / union.
     Threshold: Jaccard >= 0.20  AND  shared_ids >= 2  → covered
  2. Rule-token Jaccard: same norm() used everywhere.
     Threshold: token_jaccard >= 0.50                  → covered

CIEM via-YAML coverage:
  For every YAML rule that maps to this catalog row (high/medium),
  collect its mapped CIEM rule (if ciem_confidence >= medium).

Outputs:
  aws_catalog_coverage_matrix.csv    one row per catalog rule
  aws_catalog_coverage_summary.json
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
CATALOG_CSV   = BASE / "aws_rules.csv"
MAPPING_CSV   = BASE / "aws_unified_ai_mapping.csv"
CIEM_JSON     = BASE / "aws_ciem_rules_consolidated.json"
OUT_MATRIX    = BASE / "aws_catalog_coverage_matrix.csv"
OUT_SUMMARY   = BASE / "aws_catalog_coverage_summary.json"

CONFIG_CONF_OK  = {"high", "medium"}
CIEM_CONF_OK    = {"high", "medium"}

# Thresholds for DIRECT CIEM → catalog matching
COMP_JACC_MIN   = 0.20   # compliance-ID Jaccard
COMP_SHARED_MIN = 2      # minimum shared compliance IDs
TOKEN_JACC_MIN  = 0.50   # rule-token Jaccard fallback

NOISE = {"aws", "configured", "configuration", "resource"}
SYN = {
    "logging": "log", "logs": "log",
    "encrypted": "encryption", "encrypting": "encryption",
    "policies": "policy", "keys": "key", "accounts": "account",
    "users": "user", "roles": "role", "groups": "group",
    "permissions": "permission", "instances": "instance", "buckets": "bucket",
    "clusters": "cluster", "volumes": "volume", "snapshots": "snapshot",
    "rotation": "rotate", "rotated": "rotate", "rotating": "rotate",
    "restricted": "restrict", "restricting": "restrict",
    "enforced": "enforce", "enforcing": "enforce",
    "required": "require", "requires": "require",
    "disabled": "disable",
}


def norm_tokens(rid: str) -> frozenset:
    parts = rid.lower().replace("-", "_").split(".")
    svc = parts[1] if len(parts) >= 2 and parts[0] == "aws" else (parts[0] if parts else "")
    tail = parts[2:] if len(parts) >= 2 and parts[0] == "aws" else parts[1:]
    toks = set()
    for p in tail:
        for t in p.split("_"):
            if not t or t in NOISE:
                continue
            t = SYN.get(t, t)
            if len(t) >= 4 and t.endswith("s") and not t.endswith("ss"):
                t = t[:-1]
            toks.add(t)
    return frozenset(toks)


def jac(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def parse_compliance_ids(raw: str) -> frozenset:
    """Split semicolon-separated compliance IDs into a set."""
    if not raw:
        return frozenset()
    return frozenset(x.strip() for x in raw.split(";") if x.strip())


# ── 1. Load catalog ──────────────────────────────────────────────────────────
print("[1/5] Load catalog (aws_rules.csv)")
catalog_rows: list[dict] = []
seen_cat_ids: set[str] = set()
with CATALOG_CSV.open() as f:
    for row in csv.DictReader(f):
        rid = (row.get("rule_id") or "").strip()
        if not rid or rid in seen_cat_ids:
            continue
        seen_cat_ids.add(rid)
        row["_comp_ids"] = parse_compliance_ids(row.get("aws_mapped_compliance_ids", ""))
        row["_tokens"]   = norm_tokens(rid)
        catalog_rows.append(row)
print(f"      {len(catalog_rows)} unique catalog rules")

# ── 2. Invert AI mapping: catalog_rule_id → config info ─────────────────────
print("[2/5] Invert aws_unified_ai_mapping for config coverage")

# catalog_rule_id → list of (yaml_rule_id, confidence)
cat_to_config: dict[str, list[tuple[str, str]]] = defaultdict(list)
# catalog_rule_id → list of (ciem_rule_id, confidence)  [via YAML bridge]
cat_to_ciem_via_yaml: dict[str, list[tuple[str, str]]] = defaultdict(list)

with MAPPING_CSV.open() as f:
    for row in csv.DictReader(f):
        cat_id   = (row.get("catalog_orig_rule_id") or "").strip()
        cat_conf = (row.get("catalog_confidence") or "").strip()
        yaml_id  = (row.get("yaml_rule_id") or "").strip()
        ciem_id  = (row.get("ciem_rule_id") or "").strip()
        ciem_conf= (row.get("ciem_confidence") or "").strip()

        if cat_id and cat_conf in CONFIG_CONF_OK and yaml_id:
            cat_to_config[cat_id].append((yaml_id, cat_conf))

        # via-YAML CIEM: YAML must cover catalog (high/med) AND CIEM (high/med)
        if cat_id and cat_conf in CONFIG_CONF_OK and ciem_id and ciem_conf in CIEM_CONF_OK:
            cat_to_ciem_via_yaml[cat_id].append((ciem_id, ciem_conf))

print(f"      catalog rules with config coverage: {len(cat_to_config)}")
print(f"      catalog rules with via-YAML CIEM:   {len(cat_to_ciem_via_yaml)}")

# ── 3. Build CIEM direct match index ─────────────────────────────────────────
print("[3/5] Build direct CIEM→catalog match index")
ciem_recs: list[dict] = json.loads(CIEM_JSON.read_text())
for r in ciem_recs:
    r["_comp_ids"] = parse_compliance_ids(r.get("aws_mapped_compliance_ids", ""))
    r["_tokens"]   = norm_tokens(r.get("rule_id", ""))

# For each catalog row find matching CIEM rules
# Returns list of (ciem_rule_id, comp_jaccard, tok_jaccard, method)
def find_ciem_direct(cat_comp: frozenset, cat_tok: frozenset) -> list[tuple]:
    hits = []
    for c in ciem_recs:
        cid = c["rule_id"]
        ccomp = c["_comp_ids"]
        ctok  = c["_tokens"]

        comp_j = jac(cat_comp, ccomp)
        tok_j  = jac(cat_tok, ctok)
        shared = len(cat_comp & ccomp)

        methods = []
        if comp_j >= COMP_JACC_MIN and shared >= COMP_SHARED_MIN:
            methods.append("comp_overlap")
        if tok_j >= TOKEN_JACC_MIN:
            methods.append("token_match")
        if methods:
            hits.append((cid, round(comp_j, 3), round(tok_j, 3), "+".join(methods)))

    hits.sort(key=lambda x: -(x[1] + x[2]))
    return hits[:10]  # top 10 per catalog row

# ── 4. Build matrix ──────────────────────────────────────────────────────────
print("[4/5] Build coverage matrix")
out_rows = []
counters = {
    "covered_config_only": 0,
    "covered_ciem_direct_only": 0,
    "covered_via_yaml_ciem_only": 0,
    "covered_config_and_ciem": 0,
    "covered_config_only_no_ciem": 0,
    "not_covered": 0,
}

for cat in catalog_rows:
    rid = cat["rule_id"]

    # Config coverage
    cfg_pairs  = cat_to_config.get(rid, [])
    cfg_ids    = sorted({p[0] for p in cfg_pairs})
    cfg_best   = "high" if any(p[1] == "high" for p in cfg_pairs) else \
                 ("medium" if cfg_pairs else "none")
    config_covered = bool(cfg_pairs)

    # CIEM via-YAML coverage
    via_pairs  = cat_to_ciem_via_yaml.get(rid, [])
    via_ids    = sorted({p[0] for p in via_pairs})
    via_best   = "high" if any(p[1] == "high" for p in via_pairs) else \
                 ("medium" if via_pairs else "none")

    # CIEM direct coverage
    direct_hits = find_ciem_direct(cat["_comp_ids"], cat["_tokens"])
    direct_ids  = [h[0] for h in direct_hits]
    direct_best_comp = max((h[1] for h in direct_hits), default=0.0)
    direct_best_tok  = max((h[2] for h in direct_hits), default=0.0)
    ciem_direct_covered = bool(direct_hits)

    # Determine coverage status
    any_ciem = ciem_direct_covered or bool(via_pairs)
    if config_covered and any_ciem:
        status = "config+ciem"
        counters["covered_config_and_ciem"] += 1
    elif config_covered:
        status = "config_only"
        counters["covered_config_only_no_ciem"] += 1
    elif ciem_direct_covered:
        status = "ciem_direct_only"
        counters["covered_ciem_direct_only"] += 1
    elif bool(via_pairs):
        status = "ciem_via_yaml_only"
        counters["covered_via_yaml_ciem_only"] += 1
    else:
        status = "not_covered"
        counters["not_covered"] += 1

    out_rows.append({
        "catalog_rule_id":           rid,
        "service":                   cat.get("service", ""),
        "category":                  cat.get("category", ""),
        "provider_service":          cat.get("provider_service", ""),
        "catalog_compliance_ids":    cat.get("aws_mapped_compliance_ids", ""),
        "has_compliance_ids":        "yes" if cat["_comp_ids"] else "no",
        # Config
        "config_covered":            "yes" if config_covered else "no",
        "config_rule_count":         len(cfg_ids),
        "config_best_confidence":    cfg_best,
        "config_rule_ids":           ";".join(cfg_ids),
        # CIEM via YAML
        "ciem_via_yaml_covered":     "yes" if via_pairs else "no",
        "ciem_via_yaml_count":       len(via_ids),
        "ciem_via_yaml_best_conf":   via_best,
        "ciem_via_yaml_rule_ids":    ";".join(via_ids),
        # CIEM direct
        "ciem_direct_covered":       "yes" if ciem_direct_covered else "no",
        "ciem_direct_count":         len(direct_ids),
        "ciem_direct_best_comp_j":   direct_best_comp,
        "ciem_direct_best_tok_j":    direct_best_tok,
        "ciem_direct_rule_ids":      ";".join(direct_ids),
        # Overall
        "coverage_status":           status,
        "covered":                   "no" if status == "not_covered" else "yes",
    })

# Sort: not_covered first (actionable gaps at top), then by service
ORDER = {"not_covered": 0, "ciem_direct_only": 1, "ciem_via_yaml_only": 2,
         "config_only": 3, "config+ciem": 4}
out_rows.sort(key=lambda x: (ORDER.get(x["coverage_status"], 9), x["service"], x["catalog_rule_id"]))

print(f"[5/5] Write outputs ({len(out_rows)} rows)")
cols = list(out_rows[0].keys())
with OUT_MATRIX.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(out_rows)

total = len(out_rows)
covered_total = sum(1 for r in out_rows if r["covered"] == "yes")
summary = {
    "total_catalog_rules": total,
    "covered_total": covered_total,
    "not_covered": counters["not_covered"],
    "coverage_pct": round(100.0 * covered_total / total, 2),
    "by_status": {
        "config+ciem":          counters["covered_config_and_ciem"],
        "config_only":          counters["covered_config_only_no_ciem"],
        "ciem_direct_only":     counters["covered_ciem_direct_only"],
        "ciem_via_yaml_only":   counters["covered_via_yaml_ciem_only"],
        "not_covered":          counters["not_covered"],
    },
    "thresholds": {
        "config_confidence_ok":  sorted(CONFIG_CONF_OK),
        "ciem_confidence_ok_via_yaml": sorted(CIEM_CONF_OK),
        "ciem_direct_comp_jacc_min":  COMP_JACC_MIN,
        "ciem_direct_comp_shared_min": COMP_SHARED_MIN,
        "ciem_direct_token_jacc_min": TOKEN_JACC_MIN,
    },
}
OUT_SUMMARY.write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
