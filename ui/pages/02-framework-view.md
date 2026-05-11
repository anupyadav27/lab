# Page 02 — Framework View
**Route:** `/framework/:id`  e.g. `/framework/pci_dss`
**Entry from:** Dashboard framework card click
**Purpose:** "What's failing in this framework? Show me by section, with checks and CIEM inline."

---

## Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ ← Dashboard  /  PCI DSS v4.0.1                  [📥 Export] [Share] │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  FRAMEWORK HEADER (always visible, sticky)                           │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  PCI DSS v4.0.1 · 257 controls                                 │  │
│  │                                                                │  │
│  │  ◉ 73% overall    Config ████████████████░░░  76%             │  │
│  │  188 / 257         CIEM  ██████████████░░░░░  68%  ← gap      │  │
│  │                                                                │  │
│  │  Providers: [AWS 89%] [Azure 84%] [GCP 82%] [K8S 71%]        │  │
│  │             [OCI 67%] [IBM 61%]  [AliCloud 58%]               │  │
│  │                                                                │  │
│  │  [All providers ▾]  [All status ▾]  [All severity ▾]  [🔍]   │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  SECTIONS ACCORDION                                                  │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ ▶ Requirement 1 — Network Security Controls    32 ctrls  91%  │  │
│  ├────────────────────────────────────────────────────────────────┤  │
│  │ ▼ Requirement 3 — Protect Account Data         48 ctrls  60%  │  ← EXPANDED
│  │   CIEM: 8 checks  │  5 CRITICAL  │  12 HIGH                   │  │
│  │                                                                │  │
│  │   Sev    │ Ctrl   │ Title                  │AWS│Az │GCP│Status│  │
│  │   ───────┼────────┼────────────────────────┼───┼───┼───┼──────│  │
│  │   🔴CRIT │ 3.3.1  │ Sensitive auth data    │❌ │❌ │✅ │FAIL  │  │ ← click row
│  │   🔴CRIT │ 3.5.1  │ PAN masked on display  │❌ │❌ │❌ │FAIL  │  │
│  │   🟠HIGH │ 3.2.1  │ Cardholder data flow   │✅ │✅ │✅ │PASS  │  │
│  │   🟠HIGH │ 3.4.1  │ PAN render unreadable  │✅ │✅ │❌ │FAIL  │  │
│  │   🟡MED  │ 3.1.1  │ Data retention policy  │ — │ — │ — │MAN  │  │
│  │                                                                │  │
│  │   CIEM FINDINGS IN THIS SECTION:                              │  │
│  │   🔴 aws.iam.user.accesskey_unused_configured  14 assets fail │  │ ← click check
│  │   🟠 azure.aad.user.access_user_in90_days      8 assets fail  │  │
│  │                                                                │  │
│  ├────────────────────────────────────────────────────────────────┤  │
│  │ ▶ Requirement 6 — Secure Systems & Software    58 ctrls  71%  │  │
│  ├────────────────────────────────────────────────────────────────┤  │
│  │ ▶ Requirement 8 — Identify and Authenticate    42 ctrls  91%  │  │
│  ├────────────────────────────────────────────────────────────────┤  │
│  │   … 8 more sections …                                          │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Control Row Click → Right Panel Slides In

```
                                    ┌─────────────────────────────────┐
                                    │  PCI_DSS  3.3.1           [✕]  │
                                    │  Protect stored account data    │
                                    ├─────────────────────────────────┤
                                    │  🔴 CRITICAL · FAIL · automated │
                                    │  Section: Requirement 3         │
                                    │                                 │
                                    │  Description                    │
                                    │  Sensitive authentication data  │
                                    │  must not be stored after auth. │
                                    │                                 │
                                    │  CONFIG CHECKS                  │
                                    │  ┌───────────────────────────┐  │
                                    │  │[aws] aws.rds.instance.    │  │
                                    │  │      encryption_at_rest   │  │  ← click → /check/aws/…
                                    │  │      ❌ FAIL · 14 assets  │  │
                                    │  │                           │  │
                                    │  │[az]  azure.sql.tde_enab.. │  │
                                    │  │      ❌ FAIL ·  8 assets  │  │
                                    │  │                           │  │
                                    │  │[gcp] gcp.sql.instance.    │  │
                                    │  │      encryption_at_rest   │  │
                                    │  │      ✅ PASS · 22 assets  │  │
                                    │  └───────────────────────────┘  │
                                    │                                 │
                                    │  CIEM CHECKS                    │
                                    │  ┌───────────────────────────┐  │
                                    │  │[aws] aws.iam.user.access  │  │  ← click → /check/aws/…
                                    │  │      key_unused_config..  │  │
                                    │  │      ❌ FAIL · 14 users   │  │
                                    │  └───────────────────────────┘  │
                                    │                                 │
                                    │  REMEDIATION                    │
                                    │  Enable encryption at rest on   │
                                    │  all DB instances. Use KMS.     │
                                    │  [📋 Copy IaC] [🎫 Ticket]      │
                                    │                                 │
                                    │  [📄 Bundle Evidence]           │
                                    └─────────────────────────────────┘
```

## Data Binding

```
URL param: /framework/pci_dss
  → filter CSV rows where framework == "PCI_DSS"
  → group by section field
  → for each row, split *_checks and *_ciem_checks by ";"
  → join each check_id → runtime scan results
  → compute status per provider per control
  → compute section score = passing controls / total controls

Control panel open: ?control=pci_dss_req_3_3_1
  → load CSV row by unique_compliance_id
  → split aws_checks → ["aws.rds.instance.encryption_at_rest", ...]
  → load runtime[provider][check_id] → {status, failing_assets_count}
  → split aws_ciem_checks → load same way

Check ID link: click "aws.rds.instance.encryption_at_rest"
  → navigate to /check/aws/aws.rds.instance.encryption_at_rest
```
