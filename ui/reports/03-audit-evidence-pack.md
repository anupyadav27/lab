# Report 03 — Audit Evidence Pack
**Audience:** External Auditors, QSA, Assessors
**Length:** Full (1 page per failing control)  |  **Format:** PDF (signed)

---

## Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  [LOGO]   COMPLIANCE AUDIT EVIDENCE PACK                           │
│           PCI DSS v4.0.1  ·  acme-corp  ·  April 20, 2026          │
│           Scan ID: scan_20260420_143022  ·  SHA256: abc123...       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  TABLE OF CONTENTS                                                  │
│  1. Scope and Methodology .............. 2                          │
│  2. Executive Summary .................. 3                          │
│  3. Control Evidence (by Requirement) .. 4-187                     │
│  4. Manual Controls Attestation ........ 188                        │
│  5. Remediation Plan ................... 189                        │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CONTROL EVIDENCE PAGE (one per control)                            │
│  ──────────────────────────────────────────────────────────────    │
│  Control Reference: PCI DSS v4.0.1 / Requirement 3 / Control 3.3.1│
│  Unique ID: pci_dss_req_3_3_1                                      │
│  Title: Sensitive authentication data must not be stored           │
│  Description: SAD including full track data, CVV/CVC, PIN blocks    │
│               must not be stored after authorization.              │
│  Severity: CRITICAL  ·  Automation: Automated                      │
│  Section: Requirement 3 — Protect Account Data                     │
│                                                                      │
│  ASSESSMENT RESULT: ❌ FAIL                                         │
│  ──────────────────────────────────────────────────────────────    │
│                                                                      │
│  Evidence by Cloud Provider:                                        │
│                                                                      │
│  [AWS] Check: aws.rds.instance.encryption_at_rest                   │
│        Status: FAIL                                                 │
│        Resources checked: 28                                        │
│        Resources passing: 14                                        │
│        Resources failing: 14                                        │
│        Failing: rds-prod-01, rds-prod-02, rds-replica-03…         │
│        Timestamp: 2026-04-20T14:30:22Z                             │
│        Evidence hash: SHA256::d4e5f6...                            │
│                                                                      │
│  [Azure] Check: azure.sql.transparent_data_encryption               │
│          Status: FAIL                                               │
│          Resources checked: 12  ·  Failing: 8                      │
│          Failing: sqlsrv-prod-eus, sqlsrv-prod-wus…               │
│                                                                      │
│  [GCP]  Check: gcp.sql.instance.encryption_at_rest                 │
│         Status: PASS  ✓  All 22 resources compliant                │
│                                                                      │
│  CIEM Checks:                                                       │
│  [AWS] aws.iam.user.accesskey_unused_configured  ·  PASS ✓         │
│                                                                      │
│  REMEDIATION GUIDANCE:                                              │
│  Enable encryption at rest on all database instances. Use          │
│  provider-managed KMS keys (AWS: aws/rds, Azure: TDE with CMK,     │
│  GCP: CMEK). Apply via IaC (Terraform aws_db_instance.storage_    │
│  encrypted = true). Verify with aws rds describe-db-instances.     │
│                                                                      │
│  ────────────────────────────────────────────────────────────────   │
│  Page 47 of 189  ·  Evidence chain: scan_20260420 → control_hash   │
└─────────────────────────────────────────────────────────────────────┘
```

## Fields Used
```
unique_compliance_id, control_id, section, title, description,
severity, automation_type, framework, framework_version,
aws_checks + status, azure_checks + status, gcp_checks + status,
k8s_checks + status, oci_checks + status, ibm_checks + status,
alicloud_checks + status, *_ciem_checks + status,
remediation, scan_id, scan_timestamp, evidence_hash
```
