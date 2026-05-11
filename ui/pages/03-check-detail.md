# Page 03 — Check Detail
**Route:** `/check/:provider/:check_id`
**Example:** `/check/aws/aws.rds.instance.encryption_at_rest`
**Entry from:** Control detail panel → click any check_id link
**Purpose:** "Which assets are failing this check? Show me everything about it."

---

## Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ ← PCI_DSS › Req 3 › 3.3.1              [📄 Evidence] [🎫 Ticket]   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  CHECK HEADER                                                        │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  [aws]  aws.rds.instance.encryption_at_rest                    │  │
│  │                                                                │  │
│  │  Status: ❌ FAIL            Provider: AWS                      │  │
│  │  Checked: 28 resources      Scan: 2026-04-20T14:30:22Z        │  │
│  │  Passing: 14 ✅             Scan ID: scan_20260420_143022      │  │
│  │  Failing: 14 ❌                                                │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  MAPPED COMPLIANCE CONTROLS (which rules reference this check)      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Framework     │ Control   │ Title                   │ Section │  │
│  │  PCI_DSS       │ 3.3.1     │ Sensitive auth data..   │ Req 3   │  │  ← click → framework panel
│  │  PCI_DSS       │ 3.5.1     │ PAN render unreadable   │ Req 3   │  │
│  │  NIST_800_53   │ SC-28     │ Protection at rest      │ SC      │  │
│  │  FedRAMP_Mod   │ SC-28     │ Protection at rest      │ SC      │  │
│  │  CIS_AWS       │ 2.3.1     │ Ensure S3 encryption    │ §2      │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  FAILING ASSETS  (14)                                               │
│  [Filter: region ▾] [account ▾] [tag ▾]  [🔍 search asset ID]      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Asset ID            │ Type        │ Region     │ Account      │  │
│  │  ──────────────────────────────────────────────────────────── │  │
│  │  rds-prod-01         │ RDS DB      │ us-east-1  │ prod-123456  │  │  ← click → /asset/…
│  │  rds-prod-02         │ RDS DB      │ us-east-1  │ prod-123456  │  │
│  │  rds-replica-03      │ RDS Replica │ us-west-2  │ prod-123456  │  │
│  │  rds-dev-staging-01  │ RDS DB      │ eu-west-1  │ dev-789012   │  │
│  │  rds-analytics-01    │ RDS DB      │ ap-south-1 │ data-345678  │  │
│  │  … 9 more            │             │            │              │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  REMEDIATION                                                         │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Enable storage encryption on RDS instances. Set               │  │
│  │  storage_encrypted = true in Terraform aws_db_instance.        │  │
│  │  For existing instances: create encrypted snapshot and         │  │
│  │  restore. AWS KMS key: alias/aws/rds (or CMK).                │  │
│  │                                                                │  │
│  │  [📋 Copy Terraform snippet]  [🎫 Create Jira ticket]          │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  EVIDENCE                                                            │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Scan ID:    scan_20260420_143022                               │  │
│  │  Timestamp:  2026-04-20T14:30:22Z                              │  │
│  │  Check hash: SHA256::d4e5f6a7b8c9...                           │  │
│  │  [📄 Download evidence JSON]                                   │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Binding

```
URL: /check/aws/aws.rds.instance.encryption_at_rest

1. Check metadata:
   provider = "aws"
   check_id = "aws.rds.instance.encryption_at_rest"
   → load from runtime scan: { status, resources_total, resources_failing,
                               failing_assets[], scan_id, timestamp }

2. Mapped controls:
   → query CSV: rows where aws_checks CONTAINS "aws.rds.instance.encryption_at_rest"
   → also query azure_checks, gcp_checks, etc. for same check across providers
   → return: [ { framework, control_id, title, section, unique_compliance_id } ]

3. Failing assets:
   → from runtime scan result: failing_assets[]
   → each asset: { asset_id, asset_type, region, account_id, tags }
   → click → /asset/:asset_id

4. Remediation:
   → from CSV: first matched control row's `remediation` field
   → or check-level remediation from CSPM engine knowledge base

5. Evidence:
   → scan_id + check_id + timestamp + SHA256(check_result_json)
```
