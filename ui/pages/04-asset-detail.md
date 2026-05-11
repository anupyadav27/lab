# Page 04 — Asset Detail
**Route:** `/asset/:asset_id`
**Example:** `/asset/rds-prod-01`
**Entry from:** Check Detail → failing assets table row click
**Purpose:** "What else is wrong with this asset? Full picture for one resource."

---

## Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ ← aws.rds.instance.encryption_at_rest  /  rds-prod-01              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ASSET HEADER                                                        │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  [aws] rds-prod-01                                             │  │
│  │  Type: RDS DB Instance · Region: us-east-1 · Acct: prod-123   │  │
│  │  Tags: env=production, team=payments, pci-scope=true           │  │
│  │                                                                │  │
│  │  Failing checks:  7     Passing checks: 43    Total: 50       │  │
│  │  Frameworks affected: PCI_DSS, NIST_800_53, CIS_AWS, SOC2     │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  FAILING CHECKS ON THIS ASSET  (7)                                  │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Sev    │ Check ID                           │ Frameworks       │  │
│  │  ───────┼────────────────────────────────────┼──────────────── │  │
│  │  🔴CRIT │ aws.rds.instance.encryption_at_..  │ PCI 3.3.1       │  │  ← click → /check/aws/…
│  │  🔴CRIT │ aws.rds.instance.no_public_access  │ PCI 1.3.2       │  │
│  │  🟠HIGH │ aws.rds.instance.backup_enabled    │ NIST CP-9       │  │
│  │  🟠HIGH │ aws.rds.instance.minor_upgrade_..  │ CIS_AWS 2.3.3   │  │
│  │  🟡MED  │ aws.rds.instance.deletion_protect  │ CIS_AWS 2.3.5   │  │
│  │  🟡MED  │ aws.rds.snapshot.public_access     │ PCI 1.3.1       │  │
│  │  🟢LOW  │ aws.rds.instance.log_retention     │ NIST AU-11      │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  COMPLIANCE IMPACT                                                   │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Framework    │ Controls impacted by this asset                │  │
│  │  PCI_DSS      │ 3.3.1, 1.3.2, 1.3.1 (3 controls — CRITICAL)  │  │
│  │  NIST_800_53  │ CP-9, AU-11 (2 controls — HIGH, LOW)          │  │
│  │  CIS_AWS      │ 2.3.3, 2.3.5 (2 controls — HIGH, MED)         │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  REMEDIATION PRIORITY                                               │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Fix 1 (CRITICAL): Enable encryption at rest                   │  │
│  │  → terraform: storage_encrypted = true  [Copy]                 │  │
│  │                                                                │  │
│  │  Fix 2 (CRITICAL): Disable public accessibility               │  │
│  │  → terraform: publicly_accessible = false  [Copy]              │  │
│  │                                                                │  │
│  │  Fix 3 (HIGH): Enable automated backups                        │  │
│  │  → terraform: backup_retention_period = 7  [Copy]              │  │
│  │                                                                │  │
│  │  [🎫 Create ticket for all fixes]                              │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  FIX HISTORY                                                         │
│  ✅ Apr 15 — aws.rds.instance.multi_az_enabled — FIXED              │
│  ✅ Apr 10 — aws.rds.instance.ca_certificate_upgrade — FIXED        │
│  ❌ Apr 01 — aws.rds.instance.encryption_at_rest — still failing    │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Binding

```
URL: /asset/rds-prod-01

1. Asset metadata:
   → from runtime scan: { asset_id, asset_type, region, account_id, tags }

2. Failing checks:
   → query runtime: all checks where this asset_id is in failing_assets[]
   → for each failing check_id:
       → query CSV: rows where *_checks CONTAINS check_id
       → extract: framework, control_id, section, severity

3. Compliance impact:
   → group by framework
   → show which controls are affected

4. Remediation:
   → for each failing check, load remediation from matched CSV control row
   → sort by severity (CRITICAL first)

5. Fix history:
   → from scan history: checks on this asset across past scans
   → show status change events (FAIL→PASS = fixed)
```
