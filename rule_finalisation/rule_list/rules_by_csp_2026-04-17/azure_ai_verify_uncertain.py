"""
AI verification of 139 UNCERTAIN Azure gap rules using DeepSeek.
Passes compliance IDs AND top 10 candidate config rules to the AI to resolve ambiguity.

For each uncertain rule:
  1. Look up compliance IDs from azure_rules.csv
  2. Get top 10 candidate config rules from the YAML (scoped by service)
  3. Ask DeepSeek: which config rule (if any) covers this catalog rule?
  4. Parse: covered/not_covered + confidence + reasoning

Checkpoint at every rule so re-runs skip completed work.
"""
import csv, json, os, re, sys, time, yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai package not installed", file=sys.stderr)
    sys.exit(1)

BASE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/rule_list/rules_by_csp_2026-04-17")
YAML_PATH = Path("/Users/apple/Desktop/threat-engine/catalog/rule/azure_rule_check/1_azure_full_scope_assertions.yaml")
CATALOG = BASE / "azure_rules.csv"
GAP_FILE = Path("/Users/apple/Desktop/compliance_Database/rule_finalisation/cspm_gap_rules_all_csp.csv")
MATRIX_FILE = BASE / "azure_catalog_coverage_matrix_final.csv"
REVIEW_FILE = BASE / "azure_cat4_complete_review.json"
CHECKPOINT = BASE / "azure_ai_uncertain_ckpt.json"

API_KEY = os.getenv("DEEPSEEK_API_KEY") or "sk-3d7acb8511ad4da18e8b0c89733f472b"
MODEL = "deepseek-chat"
CONCURRENCY = 10
RETRY_LIMIT = 3
TOP_CANDIDATES = 10


# ── Load YAML config rules ─────────────────────────────────────────────────
with open(YAML_PATH) as f:
    config_yaml = yaml.safe_load(f)

config_all = []
for svc, svc_data in config_yaml.items():
    if not isinstance(svc_data, dict):
        continue
    for res_type, items in svc_data.items():
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict) and item.get("rule_id"):
                config_all.append({
                    "rule_id": item["rule_id"],
                    "svc": svc,
                    "res_type": res_type,
                    "description": (item.get("description", "") or "")[:200],
                })

config_by_service = defaultdict(list)
for c in config_all:
    config_by_service[c["svc"]].append(c)


# ── Service mapping (catalog → YAML) ───────────────────────────────────────
SVC_MAP = {
    "defender": ["defender_for_cloud", "security_center"],
    "security": ["security_center", "defender_for_cloud"],
    "securitycenter": ["security_center", "defender_for_cloud"],
    "monitor": ["monitor"], "log": ["monitor"],
    "function": ["app_service"], "functionapp": ["app_service"],
    "functions": ["app_service"], "appservice": ["app_service"],
    "app": ["app_service"], "application": ["app_service", "network"],
    "webapp": ["app_service", "web"], "site": ["app_service"],
    "ad": ["active_directory", "azure_active_directory"],
    "aad": ["active_directory", "azure_active_directory"],
    "entra": ["active_directory", "azure_active_directory", "entra_id_governance"],
    "entrad": ["active_directory", "azure_active_directory"],
    "password": ["active_directory"], "user": ["active_directory"],
    "iam": ["rbac", "authorization"],
    "rbac": ["rbac", "authorization"],
    "cosmosdb": ["cosmos_db"], "cosmos": ["cosmos_db"],
    "databricks": ["azure_databricks"],
    "postgresql": ["postgresql"], "mysql": ["mysql"], "mariadb": ["mariadb"],
    "sqlserver": ["sql_server", "sql"],
    "sql": ["sql", "sql_server", "sql_managed_instance"],
    "storage": ["storage"], "blob": ["storage"], "files": ["storage"],
    "synapse": ["synapse"], "vm": ["compute"],
    "compute": ["compute"], "virtualmachines": ["compute"],
    "disk": ["compute"],
    "managed": ["compute", "managed_identity"],
    "container": ["container_registry", "container_apps"],
    "batch": ["batch"], "cache": ["cache"], "cdn": ["cdn"],
    "dataprotection": ["backup"], "backup": ["backup"],
    "load": ["network"], "loadbalancer": ["network"],
    "networksecuritygroup": ["network"], "vpn": ["network"],
    "network": ["network"],
    "policy": ["policy"], "search": ["search"],
    "resource": ["resource_groups"], "subscription": ["subscription"],
    "automation": ["automation"],
    "certificates": ["key_vault"], "key": ["key_vault"],
    "patch": ["guest_configuration", "compute"],
    "redis": ["cache"],
}


NOISE = {"azure", "configured", "configuration", "resource", "enabled", "check",
         "policy", "az", "the", "for", "with", "and", "or", "is", "to", "of",
         "in", "on", "a", "an", "should", "be", "use", "using", "from", "that",
         "not", "are", "all", "have", "must", "only", "no", "new", "your", "by"}

def tokens(s):
    return set(t.lower() for t in re.split(r"[._\-\s/]+", s) if len(t) > 1) - NOISE


def get_top_candidates(catalog_id, yaml_svcs, n=TOP_CANDIDATES):
    cat_tok = tokens(catalog_id)
    candidates = []
    # Service-scoped candidates first
    for svc in yaml_svcs:
        for c in config_by_service.get(svc, []):
            cfg_tok = tokens(c["rule_id"])
            shared = len(cat_tok & cfg_tok)
            if shared > 0:
                candidates.append((shared, c))
    candidates.sort(key=lambda x: -x[0])
    # If fewer than n, also search all services
    if len(candidates) < n:
        seen = {c[1]["rule_id"] for c in candidates}
        extra = []
        for c in config_all:
            if c["rule_id"] in seen:
                continue
            cfg_tok = tokens(c["rule_id"])
            shared = len(cat_tok & cfg_tok)
            if shared >= 2:
                extra.append((shared, c))
        extra.sort(key=lambda x: -x[0])
        candidates += extra
    return [c[1] for c in candidates[:n]]


# ── Load catalog for compliance data ───────────────────────────────────────
catalog_map = {}
with open(CATALOG) as f:
    for row in csv.DictReader(f):
        rid = row["rule_id"]
        catalog_map[rid] = {
            "service": row.get("service", ""),
            "category": row.get("category", ""),
            "compliance_ids": row.get("azure_mapped_compliance_ids", ""),
            "compliance_functions": row.get("azure_mapped_compliance_functions", ""),
        }

# ── Load uncertain rules ───────────────────────────────────────────────────
with open(REVIEW_FILE) as f:
    review = json.load(f)
uncertain = review["uncertain"]
print(f"Loaded {len(uncertain)} uncertain rules")


# ── Load/init checkpoint ───────────────────────────────────────────────────
if CHECKPOINT.exists():
    with open(CHECKPOINT) as f:
        ckpt = json.load(f)
    print(f"Loaded checkpoint with {len(ckpt)} completed rules")
else:
    ckpt = {}


# ── AI prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a cloud security expert helping map compliance requirements to detection rules for a CSPM platform.
Config rules check static Azure resource configurations (e.g., whether encryption is enabled, TLS version is set).
A config rule "covers" a catalog rule if it detects violations of the SAME specific security control.

Consider these factors:
1. The catalog rule's compliance requirements must be addressed by the config rule.
2. The SERVICE must match semantically (e.g., function_apps ≈ functionapp, app_service.sites ≈ application webapp).
3. The SECURITY CONTROL must be the same specific check — similar keywords don't mean same intent.
   Examples of mismatch: "managed_updates" ≠ "managed_identity", "password_policy" ≠ "MFA_policy", "access_keys" ≠ "SSL_only".
4. Partial coverage only if the config rule addresses a MAJOR sub-requirement."""


def build_prompt(rule_id, compliance, candidates):
    cat_info = catalog_map.get(rule_id, {})
    svc = cat_info.get("service", "")
    cat = cat_info.get("category", "")

    lines = [
        "CATALOG RULE TO VERIFY:",
        f"  rule_id:      {rule_id}",
        f"  service:      {svc}",
        f"  category:     {cat}",
        f"  compliance:   {compliance[:300]}",
        "",
        f"TOP {len(candidates)} CONFIG RULE CANDIDATES:",
    ]
    for i, c in enumerate(candidates, 1):
        lines.append(f"  {i:2d}. {c['rule_id']}")
        if c.get("description"):
            lines.append(f"       desc: {c['description'][:150]}")
    lines += [
        "",
        "Does any config rule ABOVE cover the catalog rule's specific security requirement?",
        "Strict test: same Azure service AND same exact security control (not just related topics).",
        "Return ONLY valid JSON (no markdown):",
        '{"config_rule_id": "<exact rule_id or empty>", "confidence": "high|medium|low|none", "match_type": "full|partial|none", "reasoning": "<one sentence>"}',
    ]
    return "\n".join(lines)


client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")


def verify_one(entry):
    rule_id, _score, _prev_config = entry
    if rule_id in ckpt:
        return rule_id, ckpt[rule_id]

    cat_info = catalog_map.get(rule_id, {})
    compliance = cat_info.get("compliance_ids", "") or cat_info.get("compliance_functions", "")

    # Get top 10 candidates (service-scoped + fallback)
    parts = rule_id.split(":")[0].strip().split(".")
    svc_key = parts[1] if len(parts) > 1 else ""
    yaml_svcs = SVC_MAP.get(svc_key, [])
    candidates = get_top_candidates(rule_id, yaml_svcs)

    if not candidates:
        result = {"config_rule_id": "", "confidence": "none", "match_type": "none",
                  "reasoning": "No candidate config rules in catalog for this service.",
                  "error": ""}
        return rule_id, result

    prompt = build_prompt(rule_id, compliance, candidates)

    for attempt in range(RETRY_LIMIT):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=250,
            )
            raw = (resp.choices[0].message.content or "").strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()
            parsed = json.loads(raw)
            return rule_id, {
                "config_rule_id": (parsed.get("config_rule_id") or "").strip(),
                "confidence": (parsed.get("confidence") or "none").lower().strip(),
                "match_type": (parsed.get("match_type") or "none").lower().strip(),
                "reasoning": (parsed.get("reasoning") or "").strip()[:300],
                "error": "",
            }
        except Exception as e:
            if attempt < RETRY_LIMIT - 1:
                time.sleep(2 ** attempt)
            else:
                return rule_id, {"config_rule_id": "", "confidence": "none",
                                 "match_type": "none", "reasoning": "", "error": str(e)[:200]}
    return rule_id, {"config_rule_id": "", "confidence": "none",
                     "match_type": "none", "reasoning": "", "error": "max retries"}


# ── Run verification with concurrency ─────────────────────────────────────
pending = [e for e in uncertain if e[0] not in ckpt]
print(f"Pending: {len(pending)} (skipping {len(uncertain)-len(pending)} already done)")

completed = 0
with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
    futures = [ex.submit(verify_one, e) for e in pending]
    for fut in as_completed(futures):
        rule_id, result = fut.result()
        ckpt[rule_id] = result
        completed += 1
        if completed % 10 == 0:
            with open(CHECKPOINT, "w") as f:
                json.dump(ckpt, f, indent=2)
            print(f"  progress: {completed}/{len(pending)}")

# Final save
with open(CHECKPOINT, "w") as f:
    json.dump(ckpt, f, indent=2)
print(f"\nCompleted {completed} AI verifications")


# ── Summary of results ─────────────────────────────────────────────────────
from collections import Counter
mt_counts = Counter(r.get("match_type", "none") for r in ckpt.values())
conf_counts = Counter(r.get("confidence", "none") for r in ckpt.values())
print(f"\nResults by match_type: {dict(mt_counts)}")
print(f"Results by confidence: {dict(conf_counts)}")


# Breakdown
confirmed_covered = [(rid, r) for rid, r in ckpt.items()
                     if r.get("match_type") == "full" and r.get("confidence") in ("high", "medium")]
partial = [(rid, r) for rid, r in ckpt.items()
           if r.get("match_type") == "partial"]
still_gap = [(rid, r) for rid, r in ckpt.items()
             if r.get("match_type") == "none" or r.get("confidence") == "low"]

print(f"\nAI-CONFIRMED COVERAGE:     {len(confirmed_covered)}")
print(f"AI-CONFIRMED PARTIAL:      {len(partial)}")
print(f"AI-CONFIRMED STILL A GAP:  {len(still_gap)}")
