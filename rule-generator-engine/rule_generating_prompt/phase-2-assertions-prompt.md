## Phase 2: Generate Assertions

Goal: assertions list binding risks to concrete scoped resources.

Assertion schema fields:
- assertion_id: {domain}.{risk_id}.{control_name}
- scope: provider/resource scope (e.g., virt.identity.user)
- subcat_ref: { domain_key: "identity", risk_id: "authentication" }
- params: null or object
- evidence_type: config_read | log_query | metric_query
- rationale, severity

Rules:
- assertion_id uses domain key (scope prefix), not full domain name
- control_name is lower_snake_case and specific (e.g., mfa_enforced_for_admins)
- scope maps to the service categories allowed for the domain

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
## Enterprise guardrails (Databases SQL)
- assertion_id: db.{risk_id}.{control_name} where control_name is specific (no generic 'configured')
- scope_allowlist: pick concrete scopes per risk
  - Identity/AuthN: db.user, db.login, db.instance
  - Authorization: db.role, db.schema, db.table, db.view, db.instance
  - Secrets/Crypto: db.crypto, db.instance, db.backup
  - Network: db.endpoint, db.network, db.instance
  - Audit/Monitoring: db.audit, db.instance
  - Backup/DR: db.backup, db.instance
  - Data governance: db.table, db.data, db.instance
  - Multi-tenant: db.tenant, db.instance
- evidence_type by control intent
  - config_read: static configuration/state (TDE, TLS, private endpoints, grants)
  - log_query: dynamic behaviors (audit completeness, brute-force detection)
  - metric_query: performance/replication health
- params must be present when needed (min_tls_version, required_audit_categories, max_failed_logins, pitr_hours, min_retention_days)
- not_applicable_when guards for feature-disabled states (e.g., replication_enabled=false)
- severity/coverage_tier per control, not just domain (e.g., tde_enabled=high/core, private_endpoints_required=high/core, least_privilege_review=medium/extended)
- Coverage: generate for all risk_ids (no per-domain cap)

### Control name patterns (examples)
- authentication → mfa_enforced_for_admins, login_throttling_enabled, session_timeout_configured
- authorization → least_privilege_roles_enforced, row_level_security_enabled, column_permissions_restricted
- crypto → tde_enabled, tls_min_version_enforced, key_rotation_policy_defined
- network → private_endpoints_required, ip_allowlist_restricted, db_firewall_rules_minimized
- audit → audit_categories_complete, siem_forwarding_configured, audit_retention_policy_met
- backup/dr → backup_policies_meet_slo, pitr_enabled, restore_testing_scheduled, immutable_backups_enabled
- governance/ops → schema_change_approval_required, migration_pipeline_controls_enforced
- data governance → data_classification_applied, data_masking_enforced
- performance → query_governor_enabled, workload_isolation_configured
- multi-tenant → tenant_isolation_enforced, tenant_audit_streams_segregated

### Exit checks
- All assertions parse (jq)
- rule_id tail will equal assertion tail in Phase-4
- Random sample per domain reviewed by SME; no generic control_names remain
