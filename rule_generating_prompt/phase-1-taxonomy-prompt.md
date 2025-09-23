## Phase 1: Generate Subcategory (Risk) Taxonomy

Goal: produce domains with risk_id lists and definitions, aligned to CSPM scope prefixes.

Input:
- High-level domain set for the target area (e.g., databases, middleware, etc.)
- Prior art (benchmarks, best practices)

Output JSON schema:
{
  "version": "1.0",
  "mode": "subcategories",
  "domains": [
    {
      "domain": "Identity & Access",
      "key": "identity",
      "subcategories": [
        { "risk_id": "authentication", "title": "Authentication", "definition": "..." }
      ]
    }
  ]
}

Rules:
- key == scope_prefix (identity, rbac, crypto, storage, network, compute, mgmt, logging, backup, governance, monitoring)
- risk_id in lower_snake_case; concise, control-oriented definitions

## Quality Gates

- Domain-SME review:
  - Validate scope_prefix and domain coverage completeness
  - Confirm risk_id definitions and non-overlap
  - Ensure vendor-neutral language (no provider lock-in)
- CSPM content review:
  - Naming patterns (assertion_id/rule_id) conform
  - Evidence source authoritative and read-only
  - Severity/coverage_tier justified and consistent
  - not_applicable_when is computable and avoids false positives
  - adapter_spec.returns aligns with pass_condition fields
- Coverage checks:
  - 100
## Enterprise-grade guardrails (Databases)

- Canonical domain set (use exactly these unless justified):
  - Identity & Authentication (key: db)
  - Authorization (key: db)
  - Secrets & Cryptography (key: db)
  - Network & Exposure (key: db)
  - Audit & Monitoring (key: db)
  - Configuration Baseline & Hardening (key: db)
  - Backup, Recovery & DR (key: db)
  - Governance & Operations (key: db)
  - Performance & Availability (key: db)
  - Data Governance & Privacy (key: db)
  - Multi-tenant Controls (key: db)
- Zero-uncategorized rule: no risk_id may remain uncategorized at the end of Phase-1.
- Balance thresholds (targets, not hard fails):
  - Performance & Availability ≥ 10 items; Multi-tenant ≥ 6; Network ≥ 10; Data Governance ≥ 10
- Naming: risk_id is lower_snake_case, single-responsibility, vendor-neutral.
- Scope alignment: domain key equals scope_prefix used in downstream assertions (db.*).

### SQL seed catalog (must consider at least these)
- Identity/AuthN: service_accounts, break_glass_access, password_policy, session_management, login_throttling, disable_unused_logins
- AuthZ: role_design, role_assignment, least_privilege_review, segregation_of_duties, row_level_security, column_permissions, schema_permissions
- Crypto: tde_enabled, column_encryption, backup_encryption, key_rotation_policy, tls_min_version_policy, cipher_policy, replication_link_encryption, cmk_hsm_integration
- Network: private_endpoints, ip_allowlist, db_firewall_rules, inbound_egress_controls_by_role, bastion_only_admin_access, dns_resolution_policies_for_db, mtls_client_cert_pinning
- Audit/Monitoring: audit_categories_coverage, audit_tamper_evidence, audit_retention, siem_forwarding, data_access_auditing, schema_change_auditing, privilege_escalation_monitoring, database_activity_monitoring
- Baseline/Hardening: surface_area_reduction, extension_control, secure_defaults, patch_level_compliance, database_parameter_hardening, unused_feature_disablement, vulnerability_management, sql_injection_prevention, stored_procedure_security, dynamic_sql_controls, database_vulnerability_scanning, database_penetration_testing
- Backup/DR: backup_policies, pitr_enabled, restore_testing, immutable_backups, dr_replication, dr_runbooks, backup_verification, backup_retention_policy, cross_region_backup
- Governance/Ops: schema_change_approval, migration_pipeline_controls, versioning_of_objects, maintenance_windows, deprecation_tracking, database_incident_response, database_forensics, database_recovery_procedures
- Performance/Availability: query_performance_monitoring, database_availability_monitoring, resource_contention_monitoring, deadlock_monitoring, slow_query_baselines, plan_cache_security, resource_governor_policies, failover_readiness_checks, ha_topology_drift_detection
- Data Governance/Privacy: data_classification, data_masking, pii_access_controls, legal_hold, data_retention_policy, data_anonymization, database_privacy_controls, database_consent_management, data_retention_automations, right_to_erasure_support, data_subject_access_controls, lineage_tracking_minimums
- Multi-tenant: tenant_isolation, tenant_data_boundaries, tenant_perf_isolation, tenant_encryption_keys_ownership, tenant_data_sharding_policy, cross_tenant_reporting_controls, per_tenant_audit_streams, tenant_backup_isolation

### Exit criteria (Phase-1)
- All domains present; zero Uncategorized.
- Domain counts meet target thresholds above.
- jq parse passes; JSON schema matches sample.
- Domain-SME and CSPM reviews recorded.
