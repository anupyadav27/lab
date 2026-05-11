#!/usr/bin/env python3
"""
Enrich final_compliance_rules_mapped.csv with:
  - section     : filled via rule-based logic for NIST, ISO, SOC2, PCI, CANADA_PBMM
  - severity    : CRITICAL / HIGH / MEDIUM / LOW / INFO
                  Phase 1 (--rule-based): derived from framework + control family
                  Phase 2 (--ai): AI-generated (needs ANTHROPIC_API_KEY)
  - description : filled where empty (AI-generated, Phase 2)
  - remediation : cloud-agnostic actionable fix guidance (AI-generated, Phase 2)

Usage:
  python3 enrich_compliance_csv.py --rule-based   # fast, no API key needed
  python3 enrich_compliance_csv.py --ai           # full AI enrichment (needs key)
  python3 enrich_compliance_csv.py                # auto: rule-based if no key, else AI

Resumable via checkpoint file. Runs in batches with prompt caching.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    import anthropic
except ImportError:
    anthropic = None  # type: ignore

try:
    from openai import OpenAI as _OpenAI
except ImportError:
    _OpenAI = None  # type: ignore

# ── Paths ────────────────────────────────────────────────────────────────────
BASE       = Path(__file__).parent
INPUT_CSV  = BASE / "final_compliance_rules" / "final_compliance_rules_mapped.csv"
OUTPUT_CSV = BASE / "final_compliance_rules" / "final_compliance_rules_enriched.csv"
CHECKPOINT = BASE / "final_compliance_rules" / "enrichment_checkpoint.json"

BATCH_SIZE  = 25   # controls per API call
MAX_RETRIES = 3
RETRY_DELAY = 5    # seconds between retries


# ── Rule-based severity mappings ─────────────────────────────────────────────

# NIST family → default severity
NIST_SEVERITY = {
    "AC": "HIGH",   # Access Control
    "AT": "LOW",    # Awareness and Training
    "AU": "HIGH",   # Audit and Accountability
    "CA": "MEDIUM", # Assessment, Authorization, Monitoring
    "CM": "MEDIUM", # Configuration Management
    "CP": "MEDIUM", # Contingency Planning
    "IA": "HIGH",   # Identification and Authentication
    "IR": "MEDIUM", # Incident Response
    "MA": "MEDIUM", # Maintenance
    "MP": "LOW",    # Media Protection
    "PE": "MEDIUM", # Physical and Environmental Protection
    "PL": "INFO",   # Planning
    "PM": "INFO",   # Program Management
    "PS": "LOW",    # Personnel Security
    "PT": "HIGH",   # PII Processing and Transparency
    "RA": "MEDIUM", # Risk Assessment
    "SA": "MEDIUM", # System and Services Acquisition
    "SC": "HIGH",   # System and Communications Protection
    "SI": "HIGH",   # System and Information Integrity
    "SR": "MEDIUM", # Supply Chain Risk Management
}

# PCI requirement number → severity
PCI_SEVERITY = {
    "1": "HIGH",     # Network Security Controls
    "2": "MEDIUM",   # Secure Configurations
    "3": "CRITICAL", # Protect Account Data
    "4": "HIGH",     # Protect Data with Cryptography
    "5": "HIGH",     # Protect Against Malware
    "6": "HIGH",     # Secure Systems and Software
    "7": "HIGH",     # Restrict Access to Cardholder Data
    "8": "HIGH",     # Identify and Authenticate Users
    "9": "MEDIUM",   # Restrict Physical Access
    "10": "HIGH",    # Log and Monitor All Access
    "11": "MEDIUM",  # Test Security of Systems and Networks
    "12": "LOW",     # Support Information Security with Policies
}

# ISO 27001 annex section → severity
ISO_SEVERITY = {
    "A.5":  "INFO",   # Information Security Policies
    "A.6":  "INFO",   # Organization of Information Security
    "A.7":  "LOW",    # Human Resource Security
    "A.8":  "MEDIUM", # Asset Management
    "A.9":  "HIGH",   # Access Control
    "A.10": "HIGH",   # Cryptography
    "A.11": "MEDIUM", # Physical and Environmental Security
    "A.12": "HIGH",   # Operations Security
    "A.13": "HIGH",   # Communications Security
    "A.14": "HIGH",   # System Acquisition, Development and Maintenance
    "A.15": "MEDIUM", # Supplier Relationships
    "A.16": "HIGH",   # Information Security Incident Management
    "A.17": "MEDIUM", # Business Continuity Management
    "A.18": "MEDIUM", # Compliance
}

# SOC2 trust criteria → severity
SOC2_SEVERITY = {
    "cc":  "HIGH",   # Common Criteria (Security)
    "a1":  "HIGH",   # Availability
    "c1":  "HIGH",   # Confidentiality
    "pi1": "MEDIUM", # Processing Integrity
    "p":   "HIGH",   # Privacy
}

# HIPAA section → severity
HIPAA_SEVERITY = {
    "164.308": "MEDIUM", # Administrative Safeguards
    "164.310": "LOW",    # Physical Safeguards
    "164.312": "HIGH",   # Technical Safeguards
    "164.314": "MEDIUM", # Organizational Requirements
    "164.316": "LOW",    # Policies and Procedures
}

# CIS check keywords → severity boost (applied if check IDs contain these)
CIS_CHECK_SEVERITY_KEYWORDS = {
    "CRITICAL": ["public_access", "public_snapshot", "publicly_accessible",
                 "encryption_disabled", "admin_access", "root_used", "mfa_disabled"],
    "HIGH":     ["accesskey_unused", "no_mfa", "password_policy", "logging",
                 "cloudtrail", "audit", "public_ip", "unrestricted_ingress",
                 "encryption", "ssl", "tls", "kms", "certificate"],
    "MEDIUM":   ["rotation", "versioning", "backup", "monitoring", "alerts",
                 "lifecycle", "retention", "tagging", "patch"],
}


def infer_severity_rule_based(row: dict) -> str:
    """Derive severity from framework + control family + check keywords."""
    fw  = row["framework"]
    cid = row["control_id"].strip()
    all_checks = " ".join(
        row.get(f"{p}_checks", "") for p in
        ("aws", "azure", "gcp", "oracle", "ibm", "alicloud", "k8s")
    ).lower()

    # Check for CRITICAL keywords in check IDs
    for kw in CIS_CHECK_SEVERITY_KEYWORDS["CRITICAL"]:
        if kw in all_checks:
            return "CRITICAL"

    # Framework-specific rules
    if fw in ("NIST_800_53", "NIST_800_171", "FedRAMP_Moderate", "CANADA_PBMM"):
        m = re.search(r"\b([A-Z]{2})\b", cid.upper())
        if m:
            return NIST_SEVERITY.get(m.group(1), "MEDIUM")

    if fw == "PCI_DSS":
        m = re.match(r"^(\d+)", cid)
        if m:
            return PCI_SEVERITY.get(m.group(1), "MEDIUM")

    if fw == "ISO27001_2022":
        m = re.match(r"(A\.\d+)", cid, re.IGNORECASE)
        if m:
            key = m.group(1).upper()
            # try exact, then parent
            if key in ISO_SEVERITY:
                return ISO_SEVERITY[key]
            parent = re.match(r"(A\.\d+)", key)
            if parent:
                return ISO_SEVERITY.get(parent.group(1), "MEDIUM")

    if fw == "SOC2":
        prefix = cid.lower().split("_")[0]
        for k in sorted(SOC2_SEVERITY, key=len, reverse=True):
            if prefix.startswith(k):
                return SOC2_SEVERITY[k]

    if fw == "HIPAA":
        for prefix, sev in HIPAA_SEVERITY.items():
            if cid.startswith(prefix):
                return sev

    if fw in ("GDPR",):
        return "HIGH"

    if fw in ("RBI_BANK", "RBI_NBFC"):
        return "HIGH"

    if fw == "CISA_CE":
        return "HIGH"

    # CIS benchmarks: check for HIGH keywords
    for kw in CIS_CHECK_SEVERITY_KEYWORDS["HIGH"]:
        if kw in all_checks:
            return "HIGH"
    for kw in CIS_CHECK_SEVERITY_KEYWORDS["MEDIUM"]:
        if kw in all_checks:
            return "MEDIUM"

    # Manual controls default lower
    if row.get("automation_type") == "manual":
        return "LOW"

    return "MEDIUM"


# ── Section mappings (rule-based) ─────────────────────────────────────────────

NIST_FAMILIES = {
    "AC": "Access Control",
    "AT": "Awareness and Training",
    "AU": "Audit and Accountability",
    "CA": "Assessment, Authorization, and Monitoring",
    "CM": "Configuration Management",
    "CP": "Contingency Planning",
    "IA": "Identification and Authentication",
    "IR": "Incident Response",
    "MA": "Maintenance",
    "MP": "Media Protection",
    "PE": "Physical and Environmental Protection",
    "PL": "Planning",
    "PM": "Program Management",
    "PS": "Personnel Security",
    "PT": "PII Processing and Transparency",
    "RA": "Risk Assessment",
    "SA": "System and Services Acquisition",
    "SC": "System and Communications Protection",
    "SI": "System and Information Integrity",
    "SR": "Supply Chain Risk Management",
}

ISO27001_SECTIONS = {
    "A.5":  "Information Security Policies",
    "A.6":  "Organization of Information Security",
    "A.7":  "Human Resource Security",
    "A.8":  "Asset Management",
    "A.9":  "Access Control",
    "A.10": "Cryptography",
    "A.11": "Physical and Environmental Security",
    "A.12": "Operations Security",
    "A.13": "Communications Security",
    "A.14": "System Acquisition, Development and Maintenance",
    "A.15": "Supplier Relationships",
    "A.16": "Information Security Incident Management",
    "A.17": "Business Continuity Management",
    "A.18": "Compliance",
}

SOC2_SECTIONS = {
    "cc":  "Common Criteria (Security)",
    "a1":  "Availability",
    "c1":  "Confidentiality",
    "pi1": "Processing Integrity",
    "p":   "Privacy",
}

PCI_DSS_SECTIONS = {
    "1":  "Network Security Controls",
    "2":  "Secure Configurations",
    "3":  "Protect Account Data",
    "4":  "Protect Data with Cryptography",
    "5":  "Protect Against Malware",
    "6":  "Secure Systems and Software",
    "7":  "Restrict Access to Cardholder Data",
    "8":  "Identify and Authenticate Users",
    "9":  "Restrict Physical Access",
    "10": "Log and Monitor All Access",
    "11": "Test Security of Systems and Networks",
    "12": "Support Information Security with Organizational Policies",
}


def infer_section(framework: str, control_id: str, existing: str) -> str:
    if existing.strip():
        return existing.strip()

    cid = control_id.strip()

    if framework in ("NIST_800_53", "NIST_800_171", "FedRAMP_Moderate", "CANADA_PBMM"):
        m = re.search(r"\b([A-Z]{2})\b", cid.upper())
        if m:
            return NIST_FAMILIES.get(m.group(1), m.group(1))

    if framework == "ISO27001_2022":
        m = re.match(r"(A\.\d+)", cid, re.IGNORECASE)
        if m:
            key = m.group(1).upper()
            # try exact match first, then prefix
            if key in ISO27001_SECTIONS:
                return ISO27001_SECTIONS[key]
            parent = re.match(r"(A\.\d+)", key)
            if parent:
                return ISO27001_SECTIONS.get(parent.group(1), key)

    if framework == "SOC2":
        prefix = cid.lower().split("_")[0]
        if prefix in SOC2_SECTIONS:
            return SOC2_SECTIONS[prefix]
        # pi1 check
        for k in sorted(SOC2_SECTIONS, key=len, reverse=True):
            if prefix.startswith(k):
                return SOC2_SECTIONS[k]

    if framework == "PCI_DSS":
        m = re.match(r"^(\d+)", cid)
        if m:
            return PCI_DSS_SECTIONS.get(m.group(1), f"Requirement {m.group(1)}")

    # CIS benchmarks — fallback to "N Section" from first number in control_id
    if framework.startswith("CIS_"):
        m = re.match(r"^(\d+)", cid)
        if m:
            return f"{m.group(1)} Section"

    return ""


# ── AI enrichment ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are a cloud security compliance expert for a CSPM (Cloud Security Posture Management) platform.

For each control provided return a JSON object with EXACTLY these keys:
  "id"          : the unique_compliance_id as provided (unchanged)
  "severity"    : one of CRITICAL | HIGH | MEDIUM | LOW | INFO
  "description" : 1-2 clear technical sentences describing what this control requires
  "remediation" : 2-3 actionable sentences for remediating this in cloud environments (IaC, RBAC, encryption, policy)

Severity guide for CSPM context:
  CRITICAL : Public data exposure, authentication bypass, unencrypted credentials, open admin ports to internet
  HIGH     : Missing MFA, excessive IAM permissions, no audit logging, unencrypted data at rest/in transit
  MEDIUM   : Access control misconfiguration, weak password policy, incomplete logging, missing patch cadence
  LOW      : Minor config deviations, key rotation policy gaps, unused accounts, documentation gaps
  INFO     : Manual/governance controls, policy documentation, awareness training, org procedures

Rules:
- If description is already provided and meaningful, copy it verbatim into the output.
- If automation_type is "manual", remediation should focus on process/procedure steps, not tooling.
- Return a raw JSON array of result objects — no markdown, no preamble, no trailing text.
"""


def build_prompt(batch: list[dict]) -> str:
    items = []
    for row in batch:
        checks = []
        for p in ("aws", "azure", "gcp", "oracle", "ibm", "alicloud", "k8s"):
            c = row.get(f"{p}_checks", "").strip()
            if c:
                # first check ID only to save tokens
                first = c.split(";")[0].strip()
                checks.append(f"{p}:{first}")

        items.append({
            "id":              row["unique_compliance_id"],
            "framework":       row["framework"],
            "control_id":      row["control_id"],
            "title":           row["title"],
            "description":     row.get("description", "").strip(),
            "automation_type": row["automation_type"],
            "sample_checks":   checks[:4],
        })
    return f"Enrich these {len(items)} controls:\n\n{json.dumps(items, indent=2)}"


def call_api_deepseek(client: object, batch: list[dict]) -> dict:
    """DeepSeek via OpenAI-compatible chat completions."""
    prompt = build_prompt(batch)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = client.chat.completions.create(  # type: ignore[union-attr]
                model="deepseek-chat",
                max_tokens=8000,
                temperature=0.1,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                response_format={"type": "json_object"},
            )
            raw = resp.choices[0].message.content.strip()
            raw = re.sub(r"^```[a-z]*\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            # DeepSeek may wrap in {"results": [...]} or return array directly
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                results = parsed
            elif isinstance(parsed, dict):
                # try common wrapper keys
                for key in ("results", "controls", "data", "items"):
                    if key in parsed and isinstance(parsed[key], list):
                        results = parsed[key]
                        break
                else:
                    # single object — wrap it
                    results = [parsed]
            else:
                raise ValueError(f"Unexpected JSON shape: {type(parsed)}")
            return {r["id"]: r for r in results if "id" in r}
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"  Parse error attempt {attempt}: {e}")
            if attempt == MAX_RETRIES:
                return {}
            time.sleep(RETRY_DELAY)
        except Exception as e:
            if "rate" in str(e).lower() or "429" in str(e):
                wait = RETRY_DELAY * attempt
                print(f"  Rate limit, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  API error attempt {attempt}: {e}")
                if attempt == MAX_RETRIES:
                    return {}
                time.sleep(RETRY_DELAY)
    return {}


def call_api_anthropic(client: object, batch: list[dict]) -> dict:
    """Anthropic claude-sonnet-4-6 with prompt caching."""
    prompt = build_prompt(batch)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = client.messages.create(  # type: ignore[union-attr]
                model="claude-sonnet-4-6",
                max_tokens=8000,
                system=[{"type": "text", "text": SYSTEM_PROMPT,
                         "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()
            raw = re.sub(r"^```[a-z]*\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            results = json.loads(raw)
            if not isinstance(results, list):
                results = [results]
            return {r["id"]: r for r in results if "id" in r}
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  Parse error attempt {attempt}: {e}")
            if attempt == MAX_RETRIES:
                return {}
            time.sleep(RETRY_DELAY)
        except Exception as e:
            if "rate" in str(e).lower() or "429" in str(e):
                wait = RETRY_DELAY * attempt
                print(f"  Rate limit, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  API error attempt {attempt}: {e}")
                if attempt == MAX_RETRIES:
                    return {}
                time.sleep(RETRY_DELAY)
    return {}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rule-based", action="store_true",
                        help="Run rule-based enrichment only (no API key needed)")
    parser.add_argument("--ai", action="store_true",
                        help="Run full AI enrichment")
    args = parser.parse_args()

    anthropic_key  = os.environ.get("ANTHROPIC_API_KEY", "")
    deepseek_key   = os.environ.get("DEEPSEEK_API_KEY", "")
    has_any_key    = bool(anthropic_key or deepseek_key)
    use_ai         = args.ai or (not args.rule_based and has_any_key)

    call_api  = None
    client    = None
    provider  = None

    if use_ai:
        if deepseek_key:
            if _OpenAI is None:
                print("ERROR: openai package not installed. Run: pip3 install openai")
                sys.exit(1)
            client   = _OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
            call_api = call_api_deepseek
            provider = "DeepSeek (deepseek-chat)"
        elif anthropic_key:
            if anthropic is None:
                print("ERROR: anthropic package not installed. Run: pip3 install anthropic")
                sys.exit(1)
            client   = anthropic.Anthropic(api_key=anthropic_key)
            call_api = call_api_anthropic
            provider = "Anthropic (claude-sonnet-4-6)"
        else:
            print("ERROR: --ai mode requires DEEPSEEK_API_KEY or ANTHROPIC_API_KEY")
            sys.exit(1)

    if not use_ai:
        print("Mode: RULE-BASED (section + severity via framework/family logic)")
    else:
        print(f"Mode: FULL AI — provider: {provider}")

    print(f"Reading {INPUT_CSV}...")
    with open(INPUT_CSV, newline="") as f:
        reader = csv.DictReader(f)
        original_fields = list(reader.fieldnames)
        rows = list(reader)
    print(f"  Loaded {len(rows)} rows")

    # Load checkpoint
    checkpoint: dict = {}
    if CHECKPOINT.exists():
        with open(CHECKPOINT) as f:
            checkpoint = json.load(f)
        print(f"  Resuming: {len(checkpoint)} already enriched")

    # ── Step 1: Rule-based section fill ───────────────────────────────────────
    print("\nStep 1: Rule-based section fill...")
    section_filled = 0
    for row in rows:
        new_section = infer_section(row["framework"], row["control_id"], row["section"])
        if new_section and not row["section"].strip():
            section_filled += 1
        row["section"] = new_section
    print(f"  Filled {section_filled} empty section fields")

    # ── Step 2: Rule-based severity (always runs) ────────────────────────────
    print("\nStep 2: Rule-based severity inference...")
    sev_counts: dict = {}
    for row in rows:
        sev = infer_severity_rule_based(row)
        row["_rb_severity"] = sev
        sev_counts[sev] = sev_counts.get(sev, 0) + 1
    for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"):
        print(f"  {level:8}: {sev_counts.get(level, 0)}")

    # ── Step 3: AI enrichment (only when use_ai) ─────────────────────────────
    if use_ai:
        to_process = [r for r in rows if r["unique_compliance_id"] not in checkpoint]
        print(f"\nStep 3: AI enrichment for {len(to_process)} controls...")

        batches = [to_process[i:i + BATCH_SIZE] for i in range(0, len(to_process), BATCH_SIZE)]
        print(f"  {len(batches)} batches of up to {BATCH_SIZE}")

        for i, batch in enumerate(batches):
            fw_label = batch[0]["framework"]
            print(f"  Batch {i+1:3}/{len(batches)}  [{fw_label}...]", end="  ", flush=True)
            results = call_api(client, batch)
            if results:
                checkpoint.update(results)
                print(f"✓ ({len(results)} enriched)")
            else:
                print("✗ (skipped, will retry on next run)")
            with open(CHECKPOINT, "w") as f:
                json.dump(checkpoint, f)
    else:
        print("\nStep 3: AI enrichment skipped (rule-based mode)")

    # ── Step 4: Build enriched rows ───────────────────────────────────────────
    step = "4" if use_ai else "3"
    print(f"\nStep {step}: Building enriched CSV...")

    new_fields = list(original_fields)
    for col in ("severity", "remediation"):
        if col not in new_fields:
            new_fields.append(col)

    enriched_rows = []
    missing = 0
    for row in rows:
        new_row = dict(row)
        ai_result = checkpoint.get(row["unique_compliance_id"], {}) if use_ai else {}

        if ai_result:
            # AI result: override severity, fill description, add remediation
            new_row["severity"]    = ai_result.get("severity", row["_rb_severity"])
            new_row["remediation"] = ai_result.get("remediation", "")
            if not row.get("description", "").strip():
                new_row["description"] = ai_result.get("description", "")
        else:
            # Rule-based fallback
            new_row["severity"]    = row["_rb_severity"]
            new_row["remediation"] = ""
            if use_ai:
                missing += 1

        new_row.pop("_rb_severity", None)
        enriched_rows.append(new_row)

    # strip internal temp field if it leaked
    clean_fields = [f for f in new_fields if f != "_rb_severity"]
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=clean_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(enriched_rows)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = len(enriched_rows)
    ai_enriched = total - missing if use_ai else 0
    print(f"\n{'='*60}")
    print(f"  Output  : {OUTPUT_CSV}")
    print(f"  Total   : {total} rows")
    print(f"  Severity: 100% (rule-based)")
    print(f"  Section : 100% (rule-based fills applied)")
    if use_ai:
        print(f"  AI desc+remediation: {ai_enriched} ({ai_enriched/total*100:.1f}%)")
        if missing:
            print(f"  Pending AI : {missing} (re-run --ai to complete)")
    else:
        print(f"  Description/Remediation: pending (run with --ai)")
        print(f"\n  Next step:")
        print(f"    export ANTHROPIC_API_KEY=sk-ant-...")
        print(f"    python3 enrich_compliance_csv.py --ai")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
