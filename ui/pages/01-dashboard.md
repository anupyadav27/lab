# Page 01 — Dashboard
**Route:** `/`
**Purpose:** Single-page answer to "How compliant am I across everything?"
**Rule:** One page. All graphs. No drill-down here — just status + entry points.

---

## Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ TOPBAR  [☁ acme-corp ▾]  Scan: 4h ago [↺]  [🔔 28 failures]  [👤] │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ROW 1 — POSTURE RINGS (3 rings)                                     │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐          │
│  │  ◉  Overall    │  │  ◉  Config     │  │  ◉  CIEM/IAM   │          │
│  │     78%        │  │     81%        │  │     71%        │          │
│  │  3,210/4,117   │  │  2,841/3,502   │  │    369/615     │          │
│  │  ▲ +3% 7d      │  │  ▲ +1% 7d      │  │  ▼ -2% 7d      │          │
│  └────────────────┘  └────────────────┘  └────────────────┘          │
│                                                                       │
│  ROW 2 — FRAMEWORK SCORE CARDS (scrollable row, one card per fw)    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ PCI_DSS  │ │NIST_800_ │ │ CIS_AWS  │ │  SOC2    │ │  HIPAA   │  │
│  │  🔴 73%  │ │53 🔵 77% │ │  🟢 89%  │ │  🟢 88%  │ │  🟢 91%  │  │
│  │ 188/257  │ │1081/1403 │ │ 168/189  │ │  29/33   │ │  29/32   │  │
│  │ 5 CRIT   │ │ 12 CRIT  │ │  0 CRIT  │ │  1 CRIT  │ │  0 CRIT  │  │
│  │ [Open →] │ │ [Open →] │ │ [Open →] │ │ [Open →] │ │ [Open →] │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ← scroll for 14 more frameworks →                                   │
│                                                                       │
│  ROW 3 — LEFT: Multi-cloud heatmap  │  RIGHT: 30-day trend chart    │
│  ┌──────────────────────────────────┤┌────────────────────────────┐  │
│  │           AWS  Az  GCP  K8S  OCI ││ 100%                        │  │
│  │ PCI_DSS   89%  84%  82%  71%  67%││  75%  ───── CIS             │  │
│  │ NIST_53   78%  74%  70%  65%  55%││  50%  ─── NIST              │  │
│  │ SOC2      88%  85%  80%  72%   — ││  25%  ─ Regulatory          │  │
│  │ HIPAA     92%  88%  84%   —    — ││      ─────────────── days   │  │
│  │ [Full matrix →]                  ││      -30d          today    │  │
│  └──────────────────────────────────┘└────────────────────────────┘  │
│                                                                       │
│  ROW 4 — CRITICAL FAILURES (top 10, live)                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ 🔴  PCI_DSS › Req 3 › 3.3.1  Sensitive auth data  aws·az     │   │
│  │     ↳ 22 assets failing  [View Control →]                    │   │
│  │ 🔴  NIST_800_53 › IA › IA-2  MFA not enforced    4 providers │   │
│  │     ↳ 48 assets failing  [View Control →]                    │   │
│  │ 🔴  CIS_AWS › §1 › 1.1.4  Root MFA disabled      aws         │   │
│  │     ↳ 1 asset failing    [View Control →]                    │   │
│  │ [View all 28 critical →]                                      │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Entry Points (every element is a link)
| Click target | Goes to |
|---|---|
| Framework card `[Open →]` | `/framework/:id` |
| Heatmap cell | `/framework/:id?provider=aws` |
| Critical failure row | Framework page scrolled to that section |
| `[View Control →]` | `/framework/:id?control=:control_id` (opens panel) |
| `[Full matrix →]` | Multi-cloud matrix view |
| CIEM ring | `/framework/all?track=ciem` |

## KPIs Shown
- Overall / Config / CIEM posture scores
- Per-framework score + CRITICAL count
- Multi-cloud coverage snapshot
- 30-day score trend per framework family
- Top 10 CRITICAL failures with asset counts
