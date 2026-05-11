#!/Users/apple/Desktop/compliance_Database/ai_env/bin/python
"""
multi_csp_pipeline.py
=====================
Catalog coverage mapping pipeline for non-AWS CSPs.

Mirrors the AWS pipeline (consolidate_ciem_rules.py + build_catalog_coverage_matrix.py
+ ai_match_gaps_to_ciem.py) in a single unified script parameterised by --csp.

Supported CSPs: azure, gcp, k8s, oci, ibm, alicloud

Steps
-----
  1. Load config rules from assertions YAML (azure/gcp/k8s/oci) or *.checks.yaml (ibm/alicloud)
  2. Consolidate CIEM rules from the ciem_dir (skipped for alicloud — no ciem dir)
  3. Build Jaccard coverage matrix (no AI required)
  4. AI pass for remaining gaps  (only when --ai flag is set)
  5. Finalise coverage status
  6. Write {csp}_catalog_coverage_matrix_final.csv + print JSON summary
     Append true gaps to cspm_gap_rules_all_csp.csv

CLI
---
  python multi_csp_pipeline.py --csp azure
  python multi_csp_pipeline.py --csp k8s --ai
  python multi_csp_pipeline.py --csp ibm --ai --limit 50 --dry-run

Env vars
--------
  DEEPSEEK_API_KEY   required only when --ai is set (and not --dry-run)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

import yaml

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore[assignment,misc]

csv.field_size_limit(sys.maxsize)

# ── Path roots ───────────────────────────────────────────────────────────────

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
RULE_ROOT = Path("/Users/apple/Desktop/threat-engine/catalog/rule")
GAP_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/cspm_gap_rules_all_csp.csv")

# ── CSP configuration ────────────────────────────────────────────────────────

CSPS: dict[str, dict] = {
    "azure": {
        "catalog_csv":     BASE / "azure_rules.csv",
        "compliance_col":  "azure_mapped_compliance_ids",
        "assertions_yaml": RULE_ROOT / "azure_rule_check" / "1_azure_full_scope_assertions.yaml",
        "ciem_dir":        RULE_ROOT / "azure_rule_ciem",
        "config_format":   "assertions",
    },
    "gcp": {
        "catalog_csv":     BASE / "gcp_rules.csv",
        "compliance_col":  "gcp_mapped_compliance_ids",
        "assertions_yaml": RULE_ROOT / "gcp_rule_check" / "1_gcp_full_scope_assertions.yaml",
        "ciem_dir":        RULE_ROOT / "gcp_rule_ciem",
        "config_format":   "assertions",
    },
    "k8s": {
        "catalog_csv":     BASE / "k8s_rules.csv",
        "compliance_col":  "k8s_mapped_compliance_ids",
        "assertions_yaml": RULE_ROOT / "k8s_rule_check" / "1_k8s_full_scope_assertions.yaml",
        "ciem_dir":        RULE_ROOT / "k8s_rule_ciem",
        "config_format":   "assertions",
    },
    "oci": {
        "catalog_csv":     BASE / "oci_rules.csv",
        "compliance_col":  "oci_mapped_compliance_ids",
        "assertions_yaml": RULE_ROOT / "oci_rule_check" / "1_oci_full_scope_assertions.yaml",
        "ciem_dir":        RULE_ROOT / "oci_rule_ciem",
        "config_format":   "assertions",
    },
    "ibm": {
        "catalog_csv":     BASE / "ibm_rules.csv",
        "compliance_col":  "ibm_mapped_compliance_ids",
        "checks_dir":      RULE_ROOT / "ibm_rule_check",
        "ciem_dir":        RULE_ROOT / "ibm_rule_ciem",
        "config_format":   "checks",
    },
    "alicloud": {
        "catalog_csv":     BASE / "alicloud_rules.csv",
        "compliance_col":  "alicloud_mapped_compliance_ids",  # fallback detection below
        "checks_dir":      RULE_ROOT / "alicloud_rule_check",
        "ciem_dir":        None,  # no alicloud CIEM rules
        "config_format":   "checks",
    },
}

# ── Token normalisation (identical to AWS scripts) ────────────────────────────

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


def norm(rid: str) -> tuple[str, frozenset]:
    """Return (service_token, frozenset_of_content_tokens).

    Splits on '.' then '_', discards noise, applies synonyms, light-stems.
    Service token is parts[0] for non-AWS prefixes (azure/gcp/k8s/oci/ibm/alicloud).
    """
    parts = rid.lower().replace("-", "_").split(".")
    if not parts:
        return "", frozenset()
    # For AWS-style IDs the provider is parts[0]=='aws'; for all others it's also parts[0]
    svc = parts[1] if len(parts) >= 2 else parts[0]
    tail = parts[2:] if len(parts) >= 2 else []
    toks: set[str] = set()
    for p in tail:
        for t in p.split("_"):
            if not t or t in NOISE:
                continue
            t = SYN.get(t, t)
            if len(t) >= 4 and t.endswith("s") and not t.endswith("ss"):
                t = t[:-1]
            toks.add(t)
    return svc, frozenset(toks)


def jac(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def parse_comp(raw: str) -> frozenset:
    if not raw:
        return frozenset()
    return frozenset(x.strip() for x in raw.split(";") if x.strip())


# ── Step 1: Load config rules ─────────────────────────────────────────────────

def load_config_rules_assertions(yaml_path: Path, csp: str) -> list[dict]:
    """Parse assertions YAML: service -> resource_kind -> [items with rule_id]."""
    if not yaml_path.exists():
        print(f"  WARNING: assertions YAML not found: {yaml_path}", file=sys.stderr)
        return []
    raw = yaml.safe_load(yaml_path.read_text()) or {}
    out: list[dict] = []
    for service, rmap in raw.items():
        if not isinstance(rmap, dict):
            continue
        for resource_kind, lst in rmap.items():
            if not isinstance(lst, list):
                continue
            for item in lst:
                if not isinstance(item, dict):
                    continue
                rid = (item.get("rule_id") or "").strip()
                if not rid:
                    continue
                out.append({
                    "rule_id":       rid,
                    "service":       service,
                    "resource_kind": resource_kind,
                    "domain":        item.get("domain", ""),
                    "severity":      item.get("severity", ""),
                    "assertion_id":  item.get("assertion_id", ""),
                })
    return out


def load_config_rules_checks(checks_dir: Path, csp: str) -> list[dict]:
    """Parse *.checks.yaml files: top-level 'checks' list, each item with rule_id."""
    if not checks_dir or not checks_dir.exists():
        print(f"  WARNING: checks_dir not found: {checks_dir}", file=sys.stderr)
        return []
    yaml_files = sorted(p for p in checks_dir.rglob("*.checks.yaml") if p.is_file())
    out: list[dict] = []
    seen: set[str] = set()
    for p in yaml_files:
        try:
            data = yaml.safe_load(p.read_text()) or {}
        except Exception as e:
            print(f"  skip (yaml error): {p}: {e}", file=sys.stderr)
            continue
        if not isinstance(data, dict):
            continue
        checks = data.get("checks") or []
        if not isinstance(checks, list):
            continue
        file_service = data.get("service", p.parent.name)
        for item in checks:
            if not isinstance(item, dict):
                continue
            rid = (item.get("rule_id") or "").strip()
            if not rid or rid in seen:
                continue
            seen.add(rid)
            out.append({
                "rule_id":       rid,
                "service":       file_service,
                "resource_kind": "",
                "domain":        item.get("domain", ""),
                "severity":      item.get("severity", ""),
                "assertion_id":  "",
            })
    return out


def load_config_rules(cfg: dict, csp: str) -> list[dict]:
    fmt = cfg["config_format"]
    if fmt == "assertions":
        rules = load_config_rules_assertions(cfg["assertions_yaml"], csp)
    elif fmt == "checks":
        rules = load_config_rules_checks(cfg.get("checks_dir"), csp)
    else:
        raise ValueError(f"Unknown config_format: {fmt!r}")
    print(f"      Loaded {len(rules)} config rules ({fmt} format)")
    return rules


# ── Step 2: Consolidate CIEM rules ────────────────────────────────────────────

def flatten_compliance(frameworks: object) -> tuple[list[str], list[str]]:
    """Convert compliance_frameworks nested dict -> flat list of IDs + framework names."""
    if not isinstance(frameworks, dict):
        return [], []
    flat: list[str] = []
    fws: list[str] = []
    for framework, ids in frameworks.items():
        if not ids:
            continue
        fws.append(str(framework))
        if isinstance(ids, list):
            for i in ids:
                flat.append(f"{framework}_{i}")
        elif isinstance(ids, (str, int, float)):
            flat.append(f"{framework}_{ids}")
    return flat, fws


def consolidate_ciem_rules(ciem_dir: Path | None, csp: str) -> list[dict]:
    """Load all CIEM YAML files from ciem_dir, return consolidated records."""
    if ciem_dir is None or not ciem_dir.exists():
        print(f"      No CIEM dir for {csp} — skipping CIEM consolidation")
        return []
    yaml_files = sorted(p for p in ciem_dir.rglob("*.yaml") if p.is_file()
                        and not p.name.startswith("generate_"))
    print(f"      Found {len(yaml_files)} CIEM yaml files under {ciem_dir.name}")
    records: list[dict] = []
    seen_ids: set[str] = set()
    skipped_no_id = skipped_dup = 0
    for p in yaml_files:
        try:
            data = yaml.safe_load(p.read_text())
        except Exception as e:
            print(f"  skip (yaml error): {p.relative_to(ciem_dir)}: {e}", file=sys.stderr)
            continue
        if not isinstance(data, dict):
            continue
        rid = (data.get("rule_id") or "").strip()
        if not rid:
            skipped_no_id += 1
            continue
        if rid in seen_ids:
            skipped_dup += 1
            continue
        seen_ids.add(rid)

        compliance_ids, frameworks = flatten_compliance(data.get("compliance_frameworks", {}))
        # Build a CSP-keyed compliance IDs string (e.g. "azure_mapped_compliance_ids")
        csp_comp_key = f"{csp}_mapped_compliance_ids"
        records.append({
            "rule_id":                   rid,
            "service":                   data.get("service", ""),
            "provider":                  data.get("provider", csp),
            "check_type":                data.get("check_type", ""),
            "severity":                  data.get("severity", ""),
            "title":                     data.get("title", ""),
            "description":               data.get("description", ""),
            "rationale":                 (data.get("rationale", "") or "")[:800],
            "domain":                    data.get("domain", ""),
            "threat_category":           data.get("threat_category", ""),
            "action_category":           data.get("action_category", ""),
            "posture_category":          data.get("posture_category", ""),
            "mitre_tactics":             data.get("mitre_tactics", []) or [],
            "mitre_techniques":          data.get("mitre_techniques", []) or [],
            "threat_tags":               data.get("threat_tags", []) or [],
            "risk_score":                data.get("risk_score", ""),
            "resource":                  data.get("resource", ""),
            "compliance_frameworks_nested": data.get("compliance_frameworks", {}) or {},
            csp_comp_key:                ";".join(compliance_ids),
            "compliance_ids":            ";".join(compliance_ids),   # generic alias
            "compliance_framework_list": frameworks,
            "source_category": (p.relative_to(ciem_dir).parts[0]
                                if p.parent != ciem_dir else ""),
            "source_file":     str(p.relative_to(ciem_dir)),
        })
    print(f"      Consolidated {len(records)} CIEM rules "
          f"(skipped: no_id={skipped_no_id}, dup={skipped_dup})")
    return records


# ── Step 3: Build Jaccard coverage matrix ────────────────────────────────────

# Thresholds (same as AWS)
CONFIG_JAC_MIN   = 0.50   # token Jaccard for config rule match
CIEM_COMP_JAC    = 0.20   # compliance-ID Jaccard for CIEM match
CIEM_COMP_SHARED = 2      # minimum shared compliance IDs
CIEM_TOK_JAC     = 0.50   # token Jaccard fallback for CIEM match


def _detect_compliance_col(catalog_csv: Path, preferred: str) -> str:
    """Return the actual compliance-IDs column name from the CSV header."""
    with catalog_csv.open() as f:
        header = next(csv.reader(f))
    if preferred in header:
        return preferred
    # Fallback: look for any column containing 'compliance_ids'
    candidates = [h for h in header if "compliance_ids" in h.lower()]
    if candidates:
        col = candidates[0]
        print(f"      compliance_col fallback: using '{col}' instead of '{preferred}'")
        return col
    # Last resort: look for 'mapped_compliance_ids'
    candidates2 = [h for h in header if "mapped" in h.lower() and "compliance" in h.lower()]
    if candidates2:
        col = candidates2[0]
        print(f"      compliance_col fallback: using '{col}' instead of '{preferred}'")
        return col
    print(f"      WARNING: no compliance-IDs column found; tried '{preferred}', header={header[:10]}",
          file=sys.stderr)
    return preferred  # will just return empty strings


def load_catalog(catalog_csv: Path, compliance_col: str) -> list[dict]:
    """Load catalog CSV, deduplicate by rule_id, attach pre-computed token sets."""
    actual_col = _detect_compliance_col(catalog_csv, compliance_col)
    rows: list[dict] = []
    seen: set[str] = set()
    with catalog_csv.open() as f:
        for row in csv.DictReader(f):
            rid = (row.get("rule_id") or "").strip()
            if not rid or rid in seen:
                continue
            seen.add(rid)
            comp_raw = (row.get(actual_col) or "").strip()
            row["_comp_ids"] = parse_comp(comp_raw)
            row["_tokens"]   = norm(rid)[1]
            row["_comp_raw"] = comp_raw
            rows.append(row)
    print(f"      {len(rows)} unique catalog rules  (compliance col: '{actual_col}')")
    return rows


def build_coverage_matrix(
    catalog_rows: list[dict],
    config_rules: list[dict],
    ciem_recs: list[dict],
) -> list[dict]:
    """For each catalog row decide coverage status via Jaccard similarity."""

    # Pre-index config rules
    config_indexed: list[tuple[frozenset, dict]] = [
        (norm(r["rule_id"])[1], r) for r in config_rules
    ]

    # Pre-index CIEM rules
    for c in ciem_recs:
        c["_comp_ids"] = parse_comp(c.get("compliance_ids", ""))
        c["_tokens"]   = norm(c.get("rule_id", ""))[1]

    out_rows: list[dict] = []

    for cat in catalog_rows:
        rid       = cat["rule_id"]
        cat_tok   = cat["_tokens"]
        cat_comp  = cat["_comp_ids"]

        # ── Config coverage (token Jaccard >= 0.50) ──────────────────────────
        config_hits: list[tuple[float, dict]] = []
        for cfg_toks, cfg_rule in config_indexed:
            j = jac(cat_tok, cfg_toks)
            if j >= CONFIG_JAC_MIN:
                config_hits.append((j, cfg_rule))
        config_hits.sort(key=lambda x: -x[0])
        config_covered    = bool(config_hits)
        config_rule_ids   = ";".join(h[1]["rule_id"] for h in config_hits[:10])
        config_best_j     = round(config_hits[0][0], 3) if config_hits else 0.0

        # ── CIEM coverage ─────────────────────────────────────────────────────
        ciem_hits: list[tuple[float, float, dict]] = []
        for c in ciem_recs:
            comp_j = jac(cat_comp, c["_comp_ids"])
            tok_j  = jac(cat_tok,  c["_tokens"])
            shared = len(cat_comp & c["_comp_ids"])
            covered_by_comp = comp_j >= CIEM_COMP_JAC and shared >= CIEM_COMP_SHARED
            covered_by_tok  = tok_j  >= CIEM_TOK_JAC
            if covered_by_comp or covered_by_tok:
                ciem_hits.append((comp_j, tok_j, c))
        ciem_hits.sort(key=lambda x: -(x[0] + x[1]))
        ciem_covered    = bool(ciem_hits)
        ciem_rule_ids   = ";".join(h[2]["rule_id"] for h in ciem_hits[:10])
        ciem_best_comp  = round(ciem_hits[0][0], 3) if ciem_hits else 0.0
        ciem_best_tok   = round(ciem_hits[0][1], 3) if ciem_hits else 0.0

        # ── Coverage status ──────────────────────────────────────────────────
        if config_covered and ciem_covered:
            status = "config+ciem"
        elif config_covered:
            status = "config_only"
        elif ciem_covered:
            status = "ciem_only"
        else:
            status = "not_covered"

        out_rows.append({
            "catalog_rule_id":    rid,
            "service":            cat.get("service", ""),
            "category":           cat.get("category", ""),
            "compliance_ids":     cat["_comp_raw"],
            "has_compliance_ids": "yes" if cat_comp else "no",
            # Config
            "config_covered":     "yes" if config_covered else "no",
            "config_rule_ids":    config_rule_ids,
            "config_best_jaccard":config_best_j,
            # CIEM
            "ciem_covered":       "yes" if ciem_covered else "no",
            "ciem_rule_ids":      ciem_rule_ids,
            "ciem_best_comp_j":   ciem_best_comp,
            "ciem_best_tok_j":    ciem_best_tok,
            # Overall (AI columns will be filled later)
            "coverage_status":    status,
            "covered":            "no" if status == "not_covered" else "yes",
            # AI columns (populated in step 4 if --ai)
            "ai_match_rule_id":   "",
            "ai_confidence":      "",
            "ai_reasoning":       "",
        })

    return out_rows


# ── Step 4: AI pass ───────────────────────────────────────────────────────────

MODEL       = "deepseek-chat"
CONCURRENCY = 10
CANDIDATES  = 20
RETRY_LIMIT = 3

SYSTEM_PROMPT = """\
You are a cloud security expert helping map compliance requirements to detection rules for a CSPM platform.
Config rules check static asset configuration. CIEM rules detect security events via cloud audit logs.
A CIEM rule "covers" a catalog compliance check if it detects the same security concern.
Only return a match if you are confident the CIEM rule directly addresses the same security control."""


def _top_ciem_candidates(cat_comp: frozenset, cat_tok: frozenset,
                          cat_svc: str, ciem_recs: list[dict]) -> list[dict]:
    scored: list[tuple[float, dict]] = []
    for c in ciem_recs:
        c_comp = c["_comp_ids"]
        c_tok  = c["_tokens"]
        c_title = c.get("title", "").lower()
        c_desc  = c.get("description", "").lower()

        comp_j  = jac(cat_comp, c_comp)
        tok_j   = jac(cat_tok,  c_tok)
        shared  = len(cat_comp & c_comp)
        svc_hit = bool(cat_svc and (
            cat_svc in c_title or cat_svc in c_desc
            or cat_svc in (c.get("service") or "").lower()
        ))

        if comp_j >= 0.05 or shared >= 1 or tok_j >= 0.15 or svc_hit:
            score = 0.5 * comp_j + 0.3 * tok_j + (0.2 if svc_hit else 0.0)
            scored.append((score, c))

    scored.sort(key=lambda x: -x[0])
    if len(scored) < 5:
        fallback = [(0.5 * jac(cat_comp, c["_comp_ids"]) + 0.3 * jac(cat_tok, c["_tokens"]), c)
                    for c in ciem_recs]
        fallback.sort(key=lambda x: -x[0])
        scored = fallback

    return [x[1] for x in scored[:CANDIDATES]]


def _build_ai_prompt(cat_row: dict, candidates: list[dict]) -> str:
    rid  = cat_row["catalog_rule_id"]
    svc  = cat_row.get("service", "")
    cat  = cat_row.get("category", "")
    comp = cat_row.get("compliance_ids", "")[:300]

    lines = [
        "CATALOG RULE (not yet covered by any config/CIEM rule):",
        f"  rule_id:    {rid}",
        f"  service:    {svc}",
        f"  category:   {cat}",
        f"  compliance: {comp}",
        "",
        f"TOP {len(candidates)} CIEM CANDIDATES:",
    ]
    for i, c in enumerate(candidates, 1):
        lines.append(
            f"  {i:2d}. {c['rule_id']}"
            f"\n      title: {c.get('title','')[:100]}"
            f"\n      threat: {c.get('threat_category','')}"
            f"\n      compliance: {c.get('compliance_ids','')[:120]}"
        )
    lines += [
        "",
        "Does any CIEM candidate detect when this catalog compliance requirement is violated?",
        "Return ONLY valid JSON (no markdown, no extra text):",
        '{"ciem_rule_id": "<rule_id or empty string>", "confidence": "high|medium|low|none", "reasoning": "<one sentence>"}',
    ]
    return "\n".join(lines)


def _call_ai(client: "OpenAI", cat_row: dict, candidates: list[dict]) -> dict:
    prompt = _build_ai_prompt(cat_row, candidates)
    for attempt in range(RETRY_LIMIT):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.1,
                max_tokens=200,
            )
            raw = (resp.choices[0].message.content or "").strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            parsed = json.loads(raw)
            return {
                "ciem_rule_id": (parsed.get("ciem_rule_id") or "").strip(),
                "confidence":   (parsed.get("confidence") or "none").lower().strip(),
                "reasoning":    (parsed.get("reasoning") or "").strip()[:300],
                "error":        "",
            }
        except Exception as e:
            if attempt < RETRY_LIMIT - 1:
                time.sleep(2 ** attempt)
            else:
                return {"ciem_rule_id": "", "confidence": "none",
                        "reasoning": "", "error": str(e)[:200]}
    return {"ciem_rule_id": "", "confidence": "none", "reasoning": "", "error": "max retries"}


def run_ai_pass(
    out_rows: list[dict],
    ciem_recs: list[dict],
    csp: str,
    limit: int,
    dry_run: bool,
) -> list[dict]:
    """Fill ai_* columns for rows still not_covered.  Returns updated out_rows."""
    if OpenAI is None:
        print("ERROR: openai package not installed — cannot run AI pass", file=sys.stderr)
        return out_rows

    api_key = (os.getenv("DEEPSEEK_API_KEY") or "").strip()
    if not api_key and not dry_run:
        print("ERROR: DEEPSEEK_API_KEY not set", file=sys.stderr)
        sys.exit(2)

    client = None if dry_run else OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # Checkpoint
    ckpt_path = BASE / f"{csp}_ai_gap_checkpoint.json"
    checkpoint: dict = {}
    if ckpt_path.exists():
        try:
            checkpoint = json.loads(ckpt_path.read_text())
            print(f"      Resuming from checkpoint: {len(checkpoint)} already done")
        except Exception:
            pass

    # Build index for fast lookup by catalog_rule_id
    row_index: dict[str, dict] = {r["catalog_rule_id"]: r for r in out_rows}

    gap_rows = [r for r in out_rows if r["coverage_status"] == "not_covered"]
    if limit:
        gap_rows = gap_rows[:limit]
    todo = [r for r in gap_rows if r["catalog_rule_id"] not in checkpoint]

    print(f"      Gap rows: {len(gap_rows)}  |  Remaining after checkpoint: {len(todo)}")

    if dry_run:
        print("[DRY RUN] Showing first 3 AI prompts:")
        for row in todo[:3]:
            cat_comp = parse_comp(row.get("compliance_ids", ""))
            cat_tok  = norm(row["catalog_rule_id"])[1]
            cat_svc  = (row.get("service") or "").lower()
            cands    = _top_ciem_candidates(cat_comp, cat_tok, cat_svc, ciem_recs)
            print(f"\n=== {row['catalog_rule_id']} ({len(cands)} candidates) ===")
            print(_build_ai_prompt(row, cands)[:800])
        return out_rows

    lock = Lock()
    done = 0
    errors = 0

    def process(row: dict):
        cat_comp = parse_comp(row.get("compliance_ids", ""))
        cat_tok  = norm(row["catalog_rule_id"])[1]
        cat_svc  = (row.get("service") or "").lower()
        cands    = _top_ciem_candidates(cat_comp, cat_tok, cat_svc, ciem_recs)
        result   = _call_ai(client, row, cands)
        return row["catalog_rule_id"], result

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futures = {ex.submit(process, row): row for row in todo}
        for fut in as_completed(futures):
            rid, result = fut.result()
            with lock:
                checkpoint[rid] = result
                done += 1
                if result.get("error"):
                    errors += 1
                if done % 25 == 0 or done == len(todo):
                    ckpt_path.write_text(json.dumps(checkpoint, indent=2))
                    print(f"      [{done}/{len(todo)}]  errors={errors}", flush=True)

    ckpt_path.write_text(json.dumps(checkpoint, indent=2))

    # Apply results back to out_rows
    for row in out_rows:
        rid = row["catalog_rule_id"]
        if rid not in checkpoint:
            continue
        res    = checkpoint[rid]
        ciem_id = (res.get("ciem_rule_id") or "").strip()
        conf   = (res.get("confidence") or "none").lower()
        if ciem_id and conf in {"high", "medium"}:
            row["ai_match_rule_id"] = ciem_id
            row["ai_confidence"]    = conf
            row["ai_reasoning"]     = res.get("reasoning", "")

    return out_rows


# ── Step 5: Finalise coverage status ─────────────────────────────────────────

def finalise_status(out_rows: list[dict]) -> list[dict]:
    """Reclassify rows where AI found a match; apply final coverage labels."""
    for row in out_rows:
        if row["coverage_status"] != "not_covered":
            continue
        ai_conf = row.get("ai_confidence", "")
        ai_rid  = row.get("ai_match_rule_id", "")
        if ai_rid and ai_conf in {"high", "medium"}:
            # Was config_only/ciem_only or not_covered; now also has CIEM via AI
            if row["config_covered"] == "yes":
                row["coverage_status"] = "config+ciem"
            elif row["ciem_covered"] == "yes":
                row["coverage_status"] = "ciem_only"
            else:
                row["coverage_status"] = "ciem_only"
            row["covered"] = "yes"
        elif not ai_rid and row.get("ai_confidence") in {"", None}:
            # No AI pass ran — check if this might be a naming variant
            # (non-standard-prefix rule_id that didn't match via Jaccard)
            if row["catalog_rule_id"] and "." not in row["catalog_rule_id"]:
                row["coverage_status"] = "naming_variant_covered"
                row["covered"]         = "yes"
            else:
                row["coverage_status"] = "ai_confirmed_gap"
        else:
            row["coverage_status"] = "ai_confirmed_gap"

    return out_rows


# ── Step 6: Write outputs ─────────────────────────────────────────────────────

OUTPUT_COLS = [
    "catalog_rule_id",
    "service",
    "category",
    "compliance_ids",
    "has_compliance_ids",
    "config_covered",
    "config_rule_ids",
    "config_best_jaccard",
    "ciem_covered",
    "ciem_rule_ids",
    "coverage_status",
    "covered",
    "ai_match_rule_id",
    "ai_confidence",
    "ai_reasoning",
]

STATUS_ORDER = {
    "not_covered":           0,
    "ai_confirmed_gap":      1,
    "naming_variant_covered":2,
    "ciem_only":             3,
    "config_only":           4,
    "config+ciem":           5,
}


def write_outputs(out_rows: list[dict], csp: str) -> None:
    out_rows.sort(key=lambda x: (
        STATUS_ORDER.get(x["coverage_status"], 9),
        x.get("service", ""),
        x["catalog_rule_id"],
    ))

    out_csv = BASE / f"{csp}_catalog_coverage_matrix_final.csv"
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=OUTPUT_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(out_rows)
    print(f"      Wrote {len(out_rows)} rows → {out_csv.name}")


def append_gaps_to_gap_file(out_rows: list[dict], csp: str) -> None:
    """Append true gaps (ai_confirmed_gap + has_compliance_ids=yes) to GAP_FILE."""
    true_gaps = [
        r for r in out_rows
        if r.get("coverage_status") == "ai_confirmed_gap"
        and r.get("has_compliance_ids") == "yes"
    ]
    if not true_gaps:
        print("      No true gaps to append to gap file.")
        return

    # Read existing gap rule_ids to avoid duplicates
    existing_ids: set[str] = set()
    if GAP_FILE.exists():
        with GAP_FILE.open() as f:
            for row in csv.DictReader(f):
                existing_ids.add(row.get("catalog_rule_id", ""))

    new_gaps = [r for r in true_gaps if r["catalog_rule_id"] not in existing_ids]
    if not new_gaps:
        print(f"      {len(true_gaps)} true gaps already in gap file — nothing appended.")
        return

    gap_cols = [
        "csp", "catalog_rule_id", "service", "category", "compliance_ids",
        "compliance_frameworks", "gap_reason", "suggested_rule_type", "priority", "notes",
    ]
    write_header = not GAP_FILE.exists()
    GAP_FILE.parent.mkdir(parents=True, exist_ok=True)
    with GAP_FILE.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=gap_cols, extrasaction="ignore")
        if write_header:
            w.writeheader()
        for r in new_gaps:
            # Derive framework list from compliance_ids
            fw_names = sorted({
                "_".join(cid.split("_")[:3]) for cid in
                parse_comp(r.get("compliance_ids", ""))
            })
            w.writerow({
                "csp":                  csp,
                "catalog_rule_id":      r["catalog_rule_id"],
                "service":              r.get("service", ""),
                "category":             r.get("category", ""),
                "compliance_ids":       r.get("compliance_ids", ""),
                "compliance_frameworks":";".join(fw_names),
                "gap_reason":           (
                    r.get("ai_reasoning") or
                    f"No config or CIEM rule found for {csp} {r.get('service','')} service"
                ),
                "suggested_rule_type":  "config",
                "priority":             "medium",
                "notes":                "",
            })
    print(f"      Appended {len(new_gaps)} true gaps to {GAP_FILE.name}")


def print_summary(out_rows: list[dict], config_rules: list[dict], ciem_recs: list[dict],
                  csp: str) -> None:
    total = len(out_rows)
    covered_total = sum(1 for r in out_rows if r["covered"] == "yes")
    status_counts = Counter(r["coverage_status"] for r in out_rows)
    summary = {
        "csp":                csp,
        "total_catalog_rules":total,
        "covered_total":      covered_total,
        "not_covered":        total - covered_total,
        "coverage_pct":       round(100.0 * covered_total / total, 2) if total else 0.0,
        "config_rules_loaded":len(config_rules),
        "ciem_rules_loaded":  len(ciem_recs),
        "by_status":          dict(status_counts),
        "thresholds": {
            "config_token_jaccard_min":   CONFIG_JAC_MIN,
            "ciem_comp_jaccard_min":      CIEM_COMP_JAC,
            "ciem_comp_shared_min":       CIEM_COMP_SHARED,
            "ciem_token_jaccard_min":     CIEM_TOK_JAC,
        },
    }
    print(json.dumps(summary, indent=2))


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Multi-CSP catalog coverage mapping pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--csp", required=True, choices=list(CSPS),
                    help="Cloud service provider to process")
    ap.add_argument("--ai",      action="store_true",
                    help="Run DeepSeek AI pass for uncovered gaps")
    ap.add_argument("--limit",   type=int, default=0, metavar="N",
                    help="Limit AI pass to first N gap rows")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show prompts without calling AI API")
    args = ap.parse_args()

    csp = args.csp
    cfg = CSPS[csp]

    print(f"\n{'='*60}")
    print(f"  Multi-CSP pipeline  →  {csp.upper()}")
    print(f"{'='*60}\n")

    # ── 1. Load config rules ──────────────────────────────────────────────────
    print("[1/6] Load config rules")
    config_rules = load_config_rules(cfg, csp)

    # ── 2. Consolidate CIEM rules ─────────────────────────────────────────────
    print("[2/6] Consolidate CIEM rules")
    ciem_recs = consolidate_ciem_rules(cfg.get("ciem_dir"), csp)

    # ── 3. Load catalog & build Jaccard coverage matrix ───────────────────────
    print("[3/6] Load catalog and build coverage matrix")
    catalog_rows = load_catalog(cfg["catalog_csv"], cfg["compliance_col"])
    out_rows     = build_coverage_matrix(catalog_rows, config_rules, ciem_recs)

    # ── 4. AI pass (optional) ──────────────────────────────────────────────────
    if args.ai:
        print(f"[4/6] AI pass (--ai flag set, model={MODEL}, concurrency={CONCURRENCY})")
        if not ciem_recs:
            print("      No CIEM rules available — AI pass skipped for this CSP.")
        else:
            out_rows = run_ai_pass(out_rows, ciem_recs, csp, args.limit, args.dry_run)
    else:
        print("[4/6] AI pass skipped (use --ai to enable)")

    # ── 5. Finalise coverage status ────────────────────────────────────────────
    print("[5/6] Finalise coverage status")
    out_rows = finalise_status(out_rows)

    # ── 6. Write outputs ───────────────────────────────────────────────────────
    print("[6/6] Write outputs")
    write_outputs(out_rows, csp)
    append_gaps_to_gap_file(out_rows, csp)

    print("\n── Summary ──────────────────────────────────────────────")
    print_summary(out_rows, config_rules, ciem_recs, csp)


if __name__ == "__main__":
    main()
