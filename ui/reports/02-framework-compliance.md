# Report 02 — Framework Compliance Report
**Audience:** Compliance Manager, Auditor
**Length:** 5-20 pages  |  **Format:** PDF + CSV

---

## Layout (per-framework)

```
┌─────────────────────────────────────────────────────────────────────┐
│  [LOGO]  PCI DSS v4.0.1 — COMPLIANCE REPORT                        │
│          Account: acme-corp  ·  Scan: April 20, 2026               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  SECTION 1: EXECUTIVE OVERVIEW                                      │
│  Overall Score: 73%  (188/257 controls passing)                    │
│  Config Score: 76%   CIEM Score: 68%                               │
│  ▲ +4% vs March 2026  ·  5 CRITICAL  ·  28 HIGH  ·  20 MEDIUM     │
│                                                                      │
│  Cloud Provider Coverage:                                           │
│  AWS    ████████████████████  89%  (229/257)                       │
│  Azure  ████████████████░░░░  84%  (216/257)                       │
│  GCP    ███████████████░░░░░  82%  (211/257)                       │
│  K8S    ██████████████░░░░░░  71%  (182/257)                       │
│  OCI    █████████████░░░░░░░  67%  (172/257)                       │
│  IBM    ████████████░░░░░░░░  61%  (157/257)                       │
│  Ali    ███████████░░░░░░░░░  58%  (149/257)                       │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  SECTION 2: CONTROL DETAIL BY SECTION                               │
│                                                                      │
│  Requirement 1 — Network Security Controls  (32 controls, 91%)     │
│  ──────────────────────────────────────────────────────────────    │
│  Control ID │ Title              │ Sev  │ Status │ Providers        │
│  ──────────────────────────────────────────────────────────────    │
│  1.1.1      │ Security policies  │ LOW  │ ✅PASS │ all providers    │
│  1.2.1      │ Restrict inbound.. │ HIGH │ ✅PASS │ aws az gcp       │
│  1.3.1      │ Restrict outbound  │ HIGH │ ❌FAIL │ k8s oci          │
│  1.3.2      │ Private IPs only   │ MED  │ ✅PASS │ aws az gcp k8s   │
│                                                                      │
│  Requirement 3 — Protect Account Data  (48 controls, 60%) ⚠        │
│  ──────────────────────────────────────────────────────────────    │
│  3.3.1      │ Sensitive auth..   │ CRIT │ ❌FAIL │ aws azure        │
│             │ Remediation: Enable encryption at rest on all...      │
│  3.5.1      │ PAN masked display │ CRIT │ ❌FAIL │ aws azure gcp    │
│             │ Remediation: Implement data masking for PAN...        │
│  ...                                                                │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  SECTION 3: MANUAL CONTROLS (12 controls requiring human review)   │
│  ──────────────────────────────────────────────────────────────    │
│  Control    │ Title                   │ Notes                       │
│  3.1.1      │ Data retention policy   │ Policy document required    │
│  12.1.1     │ Security policies doc   │ Annual review required      │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  SECTION 4: REMEDIATION SUMMARY                                     │
│  Critical (fix immediately): 5 items                               │
│  High (fix within 30 days): 28 items                               │
│  Medium (fix within 90 days): 20 items                             │
│  Estimated effort: 3-4 weeks for CRITICAL+HIGH                     │
│                                                                      │
│  ─────────────────────────────────────────────────────────────────  │
│  Evidence hash: SHA256::xyz789...  ·  Generated: 2026-04-20        │
└─────────────────────────────────────────────────────────────────────┘
```

## CSV Export Columns
```
unique_compliance_id, framework, framework_version, control_id, section,
title, description, severity, automation_type, status (PASS/FAIL/MANUAL/N/A),
aws_status, azure_status, gcp_status, k8s_status, oci_status, ibm_status,
alicloud_status, remediation, scan_id, scan_date
```

## Fields Used
All fields from enriched CSV + computed `status` per provider from scan results.
