# Design Tokens & System
## CSPM Compliance Engine — Competing with Wiz & Orca

---

## Philosophy

**Dark-first. Data-dense. Audit-grade.**

Wiz wins on graph beauty. Orca wins on simplicity. We win on **depth without overwhelm** — every pixel earns its place by answering a compliance question faster than the competition.

Design principle: *If a security engineer can't find their answer in 3 clicks, we failed.*

---

## Color Palette

### Backgrounds (Dark Theme — Primary)
```
--bg-base:        #080D1A   /* page background — deeper than Wiz's */
--bg-surface:     #0F1729   /* cards, panels */
--bg-elevated:    #162040   /* modals, dropdowns */
--bg-overlay:     #1C2B52   /* hover states, selected rows */
--bg-border:      #1E3058   /* dividers, card borders */
```

### Backgrounds (Light Theme — Report/Audit mode)
```
--bg-base-light:     #F8FAFC
--bg-surface-light:  #FFFFFF
--bg-elevated-light: #F1F5F9
--bg-border-light:   #CBD5E1
```

### Brand / Primary
```
--brand-primary:   #3B82F6   /* electric blue */
--brand-secondary: #6366F1   /* indigo */
--brand-gradient:  linear-gradient(135deg, #3B82F6 0%, #6366F1 100%)
--brand-glow:      0 0 20px rgba(59,130,246,0.35)
```

### Severity Colors — CSPM Standard
```
--sev-critical:        #EF4444   /* red-500 */
--sev-critical-bg:     #1C0A0A   /* dark red tint */
--sev-critical-border: #7F1D1D
--sev-critical-text:   #FCA5A5

--sev-high:            #F97316   /* orange-500 */
--sev-high-bg:         #1C1005
--sev-high-border:     #7C2D12
--sev-high-text:       #FDBA74

--sev-medium:          #EAB308   /* yellow-500 */
--sev-medium-bg:       #1C1A05
--sev-medium-border:   #713F12
--sev-medium-text:     #FDE047

--sev-low:             #22C55E   /* green-500 */
--sev-low-bg:          #051C0D
--sev-low-border:      #14532D
--sev-low-text:        #86EFAC

--sev-info:            #06B6D4   /* cyan-500 */
--sev-info-bg:         #051218
--sev-info-border:     #164E63
--sev-info-text:       #67E8F9

--sev-pass:            #10B981   /* emerald-500 — for passing controls */
--sev-pass-bg:         #052010
--sev-na:              #64748B   /* slate-500 — N/A controls */
```

### Cloud Provider Brand Colors
```
--provider-aws:       #FF9900
--provider-azure:     #0078D4
--provider-gcp:       #4285F4
--provider-k8s:       #326CE5
--provider-oci:       #C74634   /* Oracle red */
--provider-ibm:       #0F62FE
--provider-alicloud:  #FF6A00
```

### Status / Semantic
```
--status-pass:     #10B981
--status-fail:     #EF4444
--status-manual:   #A78BFA   /* purple — manual review */
--status-na:       #64748B
--status-error:    #F43F5E
--status-pending:  #F59E0B
```

### Text
```
--text-primary:    #F1F5F9
--text-secondary:  #94A3B8
--text-tertiary:   #64748B
--text-disabled:   #334155
--text-link:       #3B82F6
--text-code:       #E2E8F0
```

---

## Typography

### Font Stack
```css
--font-sans:  'Inter', 'system-ui', sans-serif;
--font-mono:  'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
```
> Inter for all UI text. JetBrains Mono for check IDs, control IDs, code snippets.

### Scale
```
--text-xs:   11px / 16px  — metadata, timestamps, badge labels
--text-sm:   13px / 20px  — table cells, secondary labels
--text-base: 14px / 22px  — body copy, control descriptions
--text-md:   16px / 24px  — card titles, section headers
--text-lg:   20px / 28px  — page section titles
--text-xl:   24px / 32px  — page titles
--text-2xl:  32px / 40px  — dashboard hero numbers
--text-3xl:  48px / 56px  — posture score (big ring number)
```

### Weight
```
--font-regular:   400
--font-medium:    500
--font-semibold:  600
--font-bold:      700
```

---

## Spacing & Layout

```
--space-1:  4px
--space-2:  8px
--space-3:  12px
--space-4:  16px
--space-5:  20px
--space-6:  24px
--space-8:  32px
--space-10: 40px
--space-12: 48px
--space-16: 64px
```

### Grid System
- **Content max-width:** 1440px
- **Sidebar:** 240px collapsed / 64px icon-only
- **Panel:** 380px (right-side detail panels)
- **Main content:** fluid (fills remaining)
- **Card gutter:** 16px
- **Table row height:** 48px (comfortable density)

---

## Border Radius
```
--radius-sm:  4px   /* badges, chips */
--radius-md:  8px   /* cards, inputs */
--radius-lg:  12px  /* modals, panels */
--radius-xl:  16px  /* hero cards */
--radius-full: 9999px /* pills, avatars */
```

---

## Shadows & Elevation
```
--shadow-card:   0 1px 3px rgba(0,0,0,0.4), 0 1px 2px rgba(0,0,0,0.3)
--shadow-panel:  0 4px 16px rgba(0,0,0,0.5)
--shadow-modal:  0 20px 60px rgba(0,0,0,0.7)
--shadow-glow-critical: 0 0 12px rgba(239,68,68,0.4)
--shadow-glow-high:     0 0 12px rgba(249,115,22,0.4)
--shadow-glow-brand:    0 0 20px rgba(59,130,246,0.35)
```

---

## Core Components

### SeverityBadge
```
Props: severity (CRITICAL|HIGH|MEDIUM|LOW|INFO|PASS|MANUAL|N/A)

Sizes:
  sm:  px-1.5 py-0.5 text-xs  — table cells
  md:  px-2   py-1   text-sm  — cards
  lg:  px-3   py-1.5 text-md  — detail headers

Visual: colored dot + uppercase label + colored border
Example: ● CRITICAL  [red dot, red text, dark red bg, red border]
```

### ProviderBadge
```
Props: provider (aws|azure|gcp|k8s|oci|ibm|alicloud), count?, status?

Visual: provider logo/icon + abbreviated name + optional check count
Colors: use provider brand colors from palette
```

### ComplianceScoreRing
```
Props: score (0-100), size (sm|md|lg), animated?

Visual:
  - SVG donut chart, 120° gap at bottom
  - Ring color: 0-49% red, 50-74% amber, 75-89% blue, 90-100% green
  - Center: large score number + "%" subscript
  - Below ring: "X/Y Controls" in secondary text
  - Animation: draws from 0 on mount (500ms ease-out)

Sizes:
  sm: 80px ring  — framework cards in explorer
  md: 140px ring — framework detail header
  lg: 200px ring — dashboard hero
```

### ControlStatusBar
```
Props: passing, failing, manual, na, total

Visual: horizontal stacked bar
  Green (pass) | Red (fail) | Purple (manual) | Gray (N/A)
  Each segment shows count on hover tooltip
  Height: 6px (compact) or 10px (detail)
```

### CheckIDChip
```
Props: checkId, provider, status?

Visual: mono font, small pill with provider color left-border
Example: [aws] aws.iam.user.accesskey_unused_configured
Click: opens check detail side panel
```

### FrameworkTag
```
Props: framework, version?

Visual: outlined pill with framework abbreviation
Color: unique per framework family
  CIS_*:     teal outline
  NIST_*:    blue outline
  PCI_DSS:   purple outline
  HIPAA:     pink outline
  SOC2:      indigo outline
  ISO27001:  orange outline
  FedRAMP:   navy outline
  GDPR:      green outline
  Regional:  amber outline (CANADA_PBMM, RBI_*, CISA_CE)
```

### RemediationCard
```
Props: text, severity, automationType, provider?

Visual:
  - Left border: severity color
  - Icon: wrench (config) or shield (CIEM)
  - Title: "Remediation Guidance"
  - Body: AI-generated remediation text
  - Footer: "Generated by AI · Review before applying"
  - CTA button: "Copy as IaC Comment" | "Create Ticket"
```

### DataTable
```
Features:
  - Virtual scroll (handles 4117 rows without pagination lag)
  - Sticky header
  - Multi-column sort
  - Column visibility toggle
  - Bulk select + actions
  - Inline severity filter chips
  - Row click → right-side detail panel
  - Keyboard navigation (arrow keys, enter to open)
  - Density toggle: Compact / Default / Comfortable
```

### FilterBar
```
Features:
  - Provider multi-select (7 providers + K8S)
  - Framework multi-select (19 frameworks)
  - Severity multi-select
  - Automation type toggle (Automated / Manual / Both)
  - Section/family filter (context-aware per framework)
  - Status filter (PASS / FAIL / MANUAL / N/A)
  - Free text search (searches title + control_id + description)
  - Active filters shown as removable chips
  - "Reset all" link
  - Filter state saved to URL params
```

---

## Navigation

### Left Sidebar (240px)
```
Logo / Brand (top)
─────────────────────────────
[🏠] Dashboard              (Compliance Posture)
[📋] Frameworks             (Framework Explorer)
[🌐] Multi-Cloud Matrix     (Provider Coverage)
[🔐] CIEM Posture           (Identity Risk)
[🔧] Remediation Queue      (Fix Actions)
[🔍] Gap Analysis           (Coverage Gaps)
[📊] Reports                (Report Builder)
[📁] Audit Evidence         (Evidence Trail)
─────────────────────────────
[⚙️] Settings
[?]  Help
```

### Top Bar (56px)
```
[Sidebar toggle] [Breadcrumb] ─────── [Account selector ▾] [Scan: 4h ago 🔄] [🔔 3] [Avatar]
```

### Breadcrumb Examples
```
Dashboard
Frameworks › PCI_DSS v4.0.1
Frameworks › PCI_DSS v4.0.1 › Req 3 › Control 3.1.1
Multi-Cloud Matrix
Remediation Queue › HIGH
```

---

## Competitive Edge: Design Differentiators

| Feature | Wiz | Orca | **Our Platform** |
|---|---|---|---|
| Frameworks | ~12 | ~15 | **19** |
| Cloud providers | 3+K8S | 5+K8S | **7+K8S** |
| CIEM separate track | Partial | No | **Yes** |
| Cross-framework mapping | No | No | **Yes** |
| AI remediation inline | No | No | **Yes (DeepSeek)** |
| Audit PDF per control | No | Partial | **Yes** |
| Section-level grouping | No | No | **Yes (NIST families)** |
| IBM/AliCloud/OCI coverage | No | Partial | **Yes** |
| Framework score ring | Yes | Yes | **Yes + CIEM split** |
