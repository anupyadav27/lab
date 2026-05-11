# CSPM Compliance Engine — UI Design
## Flow-first. Every click answers the next question.

---

## Files

```
ui/
├── README.md                       ← this file
├── FLOW.md                         ← full story flow + data binding logic
├── design-system/
│   └── 00-design-tokens.md         ← colors, typography, components
├── pages/
│   ├── 01-dashboard.md             ← single page, all graphs, all entry points
│   ├── 02-framework-view.md        ← sections accordion + control panel + checks
│   ├── 03-check-detail.md          ← check → failing assets + evidence
│   ├── 04-asset-detail.md          ← asset → all failing checks + fix history
│   └── 05-supporting-views.md      ← matrix, CIEM, remediation queue, reports
└── reports/
    ├── 01-executive-summary.md
    ├── 02-framework-compliance.md
    ├── 03-audit-evidence-pack.md
    ├── 04-gap-analysis-report.md
    └── 05-multicloud-coverage.md
```

---

## The Flow (5 levels deep)

```
Dashboard  →  Framework  →  Control panel  →  Check detail  →  Asset detail
   (1)            (2)             (2b)              (3)              (4)
```

**Level 1 — Dashboard `/`**
One page. Score rings + framework cards + heatmap + trend + critical failures.
No drill-down on this page — only entry points to level 2.

**Level 2 — Framework View `/framework/:id`**
Sections accordion. Click section → expands in-page showing controls table.
Click control row → right panel slides in (level 2b).

**Level 2b — Control Detail Panel (right slide-in)**
Title, description, severity. Config checks list. CIEM checks list. Remediation.
Each check ID is a link → level 3.

**Level 3 — Check Detail `/check/:provider/:check_id`**
Which controls map to this check. Failing assets table. Evidence. Remediation.
Each asset row → level 4.

**Level 4 — Asset Detail `/asset/:asset_id`**
All failing checks on this asset across all frameworks. Remediation priority list.
Fix history.

---

## Key Design Principle

> Evidence is not a separate page — it lives inside Check Detail.
> Reports are not a separate flow — they export the same data shown in the live views.
> CIEM and Config are not separate tracks — they appear together on every control.

---

## Data Source

`final_compliance_rules/final_compliance_rules_enriched.csv`

The CSV provides the **compliance layer** (control → check IDs).
The CSPM runtime provides the **execution layer** (check ID → assets → pass/fail).
The binding: `control.*_checks.split(";")` → lookup in runtime scan results.
