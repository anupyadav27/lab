# Page 05 — Supporting Views
## Multi-Cloud Matrix · CIEM Posture · Remediation Queue · Reports
**These live within the main flow — not isolated islands.**

---

## A — Multi-Cloud Matrix
**Route:** `/matrix`  |  **Entry from:** Dashboard heatmap "Full matrix →"

```
┌──────────────────────────────────────────────────────────────────────┐
│ ← Dashboard  /  Multi-Cloud Matrix           [📥 Export CSV]        │
├──────────────────────────────────────────────────────────────────────┤
│  View: [Config ●] [CIEM ○] [Combined ○]                             │
│                                                                       │
│                  AWS    Az    GCP   K8S   OCI   IBM   Ali            │
│  CIS_AWS         89%     —     —     —     —     —     —             │
│  CIS_AZURE        —     83%    —     —     —     —     —             │
│  CIS_GCP          —      —    81%    —     —     —     —             │
│  CIS_K8S          —      —     —    76%    —     —     —             │
│  NIST_800_53     78%    74%   70%   65%   55%   52%   48%            │
│  PCI_DSS         89%    84%   82%   71%   67%   61%   58%            │
│  HIPAA           92%    88%   84%    —     —     —     —             │
│  SOC2            88%    85%   80%   72%    —     —     —             │
│  [ … 11 more frameworks … ]                                          │
│                                                                       │
│  Click any cell → /framework/:id?provider=:provider                 │
│  ■ 90%+ green  ■ 75-89% blue  ■ 50-74% amber  ■ <50% red  — N/A   │
└──────────────────────────────────────────────────────────────────────┘
```
**Click any cell** → Framework View filtered to that provider.

---

## B — CIEM / IAM Posture
**Route:** `/ciem`  |  **Entry from:** Dashboard CIEM ring click

```
┌──────────────────────────────────────────────────────────────────────┐
│ ← Dashboard  /  CIEM Posture                                        │
├──────────────────────────────────────────────────────────────────────┤
│  ◉ 71% overall  │  AWS 76%  Azure 69%  GCP 67%  K8S 65%            │
├──────────────────────────────────────────────────────────────────────┤
│  TOP FAILING CIEM CHECKS                                            │
│  🔴  aws.iam.user.mfa_enabled          48 users failing             │  ← click → /check/aws/…
│  🔴  aws.iam.root.no_mfa_enabled        1 root account failing      │
│  🟠  aws.iam.user.accesskey_unused     36 users failing             │
│  🟠  azure.aad.user.access_in90_days   28 users failing             │
│  🟠  gcp.iam.policy.no_action_star     14 policies failing          │
│  [ see all 246 CIEM checks ]                                        │
├──────────────────────────────────────────────────────────────────────┤
│  CIEM vs CONFIG GAP (bar chart per provider)                        │
│  AWS    Config 81% ████████████  CIEM 76% ██████████  gap: 5%      │
│  Azure  Config 79%              CIEM 69%             gap: 10%      │
│  GCP    Config 77%              CIEM 67%             gap: 10%      │
│  K8S    Config 65%              CIEM 65%             gap: 0%       │
│                                                                       │
│  Each failing CIEM check row → /check/:provider/:check_id           │
└──────────────────────────────────────────────────────────────────────┘
```

---

## C — Remediation Queue
**Route:** `/remediation`  |  **Entry from:** Dashboard "View all X critical →" link

```
┌──────────────────────────────────────────────────────────────────────┐
│ ← Dashboard  /  Remediation Queue         312 items  [Assign All]   │
├──────────────────────────────────────────────────────────────────────┤
│  [🔴 CRITICAL 28] [🟠 HIGH 94] [🟡 MEDIUM 146] [🟢 LOW 44]         │
│  [Provider ▾] [Framework ▾] [Config/CIEM ▾]                         │
├──────────────────────────────────────────────────────────────────────┤
│  🔴 CRITICAL                                                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ ☐  PCI_DSS 3.3.1 · Sensitive auth data                       │  │
│  │    Providers: aws · azure  │  22 assets failing               │  │
│  │    ↳ Enable encryption at rest on all DB instances...         │  │  ← click → /check/aws/…
│  │    [View check] [🎫 Ticket]                                   │  │
│  │                                                                │  │
│  │ ☐  NIST IA-2 · MFA not enforced                               │  │
│  │    Providers: aws·az·gcp·k8s  │  48 assets failing            │  │
│  │    ↳ Enable MFA for all IAM users and roles...                │  │
│  │    [View check] [🎫 Ticket]                                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Bulk: ☑ 3 selected → [Create Jira] [Export] [Assign to: ___]      │
│                                                                       │
│  Each [View check] → /check/:provider/:check_id                     │
└──────────────────────────────────────────────────────────────────────┘
```

---

## D — Reports (kept separate, clean)
**Route:** `/reports`  |  **Entry from:** Sidebar nav only

```
┌──────────────────────────────────────────────────────────────────────┐
│  Reports                                        [+ New Report]      │
├──────────────────────────────────────────────────────────────────────┤
│  TEMPLATES                   │  PREVIEW                              │
│  ─────────────────────────── │  ┌────────────────────────────────┐  │
│  🎯 Executive Summary         │  │  [Live PDF preview pane]       │  │
│  📑 Framework Compliance      │  │                                │  │
│  ⚖️  Audit Evidence Pack      │  │  Scope: PCI_DSS · AWS+Azure    │  │
│  🔍 Gap Analysis              │  │  Score: 73% · 5 CRITICAL       │  │
│  🌐 Multi-Cloud Coverage      │  │                                │  │
│  ─────────────────────────── │  └────────────────────────────────┘  │
│  Saved reports                │  [📥 PDF] [📊 CSV] [🔗 Link]        │
│  📋 Q1 PCI Audit — Apr 1      │  Schedule: [Monthly ▾] + emails     │
│  📋 SOC2 Board — Mar 15       │                                      │
└──────────────────────────────────────────────────────────────────────┘
```
**Note:** Evidence bundled here too — "Audit Evidence Pack" template exports
per-control evidence from the same check + CIEM data used in the live views.
No separate audit evidence page needed.

---

## Full Navigation Map (revised)

```
/ ─── Dashboard (one page, all graphs)
│       │
│       ├── click framework card ──────────────► /framework/:id
│       │                                              │
│       │                                         sections accordion
│       │                                              │
│       │                                         click control row
│       │                                              │
│       │                                         right panel opens
│       │                                              │
│       │                                         click check_id
│       │                                              │
│       ├── click heatmap cell ──────────────────► /check/:prov/:id
│       │                                              │
│       ├── click CIEM ring ─────────────────────► /ciem             │
│       │                                              │              │
│       ├── click "view all critical" ────────────► /remediation      │
│       │                                              │ click row    │
│       │                                         → /check/:prov/:id  │
│       │                                              │              │
│       │                                         click asset ────────►/asset/:id
│       │
│       └── sidebar: Reports ─────────────────────► /reports
```
