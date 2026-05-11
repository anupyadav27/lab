# CSPM Compliance Engine — Story Flow & Data Binding
## Navigation is the product. Every click answers the next question.

---

## The Story

```
User logs in
     │
     ▼
DASHBOARD ── "How compliant am I across everything?"
     │              One page. All graphs. Framework scores, CIEM split,
     │              top failures, trend. No separate KPI pages.
     │
     │  [click framework card]
     ▼
FRAMEWORK VIEW ── "What's failing in PCI DSS? Show me by section."
     │              Score ring + CIEM split in header.
     │              Sections accordion: each section shows controls,
     │              pass/fail counts, CIEM findings inline.
     │
     │  [click section header]
     ▼
SECTION EXPANDED ── (inline, same page) ── "Show me the controls in Req 3."
     │              Controls table: ID, title, severity, status per provider.
     │              Each control row has CIEM badge if CIEM checks exist.
     │
     │  [click control row]
     ▼
CONTROL DETAIL PANEL ── (right slide-in) ── "What checks cover 3.3.1? What's failing?"
     │              Description, severity, automation type.
     │              Config checks list: check_id → provider → PASS/FAIL → N assets
     │              CIEM checks list: check_id → provider → PASS/FAIL
     │              AI remediation inline.
     │              Evidence bundle download.
     │
     │  [click check_id link]
     ▼
CHECK DETAIL PAGE ── "Which assets are failing this check? Show me everything."
     │              Check description + linked compliance controls.
     │              Failing assets table: asset_id, type, region, account.
     │              Evidence: scan_id, timestamp, SHA256.
     │
     │  [click asset row]
     ▼
ASSET DETAIL PAGE ── "What else is wrong with this asset?"
                     Asset metadata. All failing checks on this asset.
                     Remediation steps. Fix history.
```

---

## Navigation Map

```
/ ─────────────────────────────── Dashboard (single page)
│
├── /framework/:id ─────────────── Framework View (sections accordion)
│       │
│       └── ?section=:name ──────── Section expanded (same page, scroll-to)
│               │
│               └── ?control=:id ── Control detail panel (right slide-in)
│
├── /check/:provider/:check_id ──── Check Detail (assets + evidence)
│       │
│       └── /asset/:asset_id ────── Asset Detail
│
└── /reports ────────────────────── Report Builder (separate, clean)
```

---

## Data Binding at Every Level

```
CSV LAYER (static compliance rules)
  └── unique_compliance_id
        ├── framework, section, control_id, title, description
        ├── severity, automation_type
        ├── aws_checks      → "check_a;check_b;check_c"
        ├── aws_ciem_checks → "ciem_check_a;ciem_check_b"
        ├── azure_checks, gcp_checks, k8s_checks, oci_checks …
        └── remediation (AI-generated)

RUNTIME LAYER (scan results — live from CSPM engine)
  └── check_id + provider
        ├── status: PASS | FAIL | ERROR
        ├── resources_total, resources_passing, resources_failing
        ├── failing_assets: [ asset_id, asset_type, region, account, tags ]
        ├── scan_id, scan_timestamp
        └── evidence_hash: SHA256

BINDING: control.aws_checks.split(";") → [check_id] → runtime[check_id]
         control.aws_ciem_checks.split(";") → [ciem_check_id] → runtime[ciem_check_id]
```

---

## Control Status Rollup Logic

```
control.status[provider] =
  if no checks for provider            → "N/A"
  if automation_type == "manual"       → "MANUAL"
  if any check FAIL                    → "FAIL"
  if all checks PASS                   → "PASS"

control.status[overall] = worst-case across all providers
  FAIL > MANUAL > PASS > N/A

framework.score = count(controls where status != FAIL and status != N/A)
                  / count(controls where status != N/A)
```
