# Taxonomy Learnings (Reusable Patterns)

Purpose: concise guidelines to author high-quality, reusable taxonomies and downstream assets (assertions → matrix → rules) across categories (databases, middleware, web, network, containers, OS, workspace, office, etc.).

## Core conventions
- Domain key = scope_prefix (e.g., identity, rbac, secrets, crypto, storage, network, compute, mgmt, logging, backup, governance, monitoring, db)
- risk_id: lower_snake_case; single-responsibility control concept; vendor-neutral
- assertion_id: {domain_key}.{risk_id}.{control_name}
- rule_id: {adapter}.{assertion_tail}
- scope_allowlist: resource categories the domain may target (e.g., db.user, virt.identity.user)

## Structure and depth
- Keep domains stable, expand via risk_ids
- Add risks in layers: identity → authZ → secrets/crypto → network → audit/monitoring → baseline/hardening → backup/DR → governance/ops → multi-tenant
- Prefer small, evaluable risks over large, vague buckets

## Mapping logic
- Taxonomy (domain/risk) → Assertions (scoped controls) → Matrix (service/resource/adapter evidence) → Rules (executable checks)
- One risk_id can map to multiple scopes and adapters; ensure each has at least one rule

## Adapter selection
- Prefer authoritative, read-only configuration APIs
- If unavailable: inventory/metrics/log APIs; last resort: derived analytics
- Name: provider.service.feature_action (e.g., vmware.vcenter.sso_mfa_policy, sql.server.tde_status)

## Severity and coverage
- severity: high for identity/crypto, exposure, DDoS/ransomware, critical hardening; medium for hygiene/config drift; low for housekeeping
- coverage_tier: core (direct config), extended (audits/analytics), exhaustive (deep/env-specific)

## Naming and consistency checks
- rule_id tail MUST equal assertion tail
- resource_type matches scope (virt.* or db.*)
- not_applicable_when is computable (has a deterministic probe)
- adapter_spec.returns must include every field referenced in pass_condition

## Category vs technology
- Organize by category folders (e.g., databases_matrix, database_rules) not per-product
- Use a single shared taxonomy per category; extend with tech-specific risks only when unavoidable (e.g., NoSQL: shard_key_design)

## SQL-specific learnings (extendable to NoSQL)
- Identity/AuthN: service_accounts, break_glass_access, password_policy, session_management, login_throttling, disable_unused_logins
- AuthZ: role_design, role_assignment, least_privilege_review, segregation_of_duties, row_level_security, column_permissions, schema_permissions
- Crypto: tde_enabled, column_encryption, backup_encryption, key_rotation_policy, tls_min_version_policy, cipher_policy, replication_link_encryption
- Network: private_endpoints, ip_allowlist, db_firewall_rules
- Audit/Monitoring: audit_categories_coverage, audit_tamper_evidence, audit_retention, siem_forwarding, anomaly_detection_db_activity
- Baseline/Hardening: surface_area_reduction, extension_control, secure_defaults, patch_level_compliance
- Backup/DR: backup_policies, pitr_enabled, restore_testing, immutable_backups, dr_replication, dr_runbooks
- Governance/Ops: quotas, workload_isolation, query_governor, index_maintenance_policy, schema_change_approval, migration_pipeline_controls, versioning_of_objects
- Data Governance: data_classification, data_masking, pii_access_controls, legal_hold
- Platform Ops: capacity_planning, maintenance_windows, deprecation_tracking
- Multi-tenant: tenant_isolation, tenant_data_boundaries

## Database Expert-Identified Critical Gaps (SQL)
**Authentication & Session Security:**
- connection_pooling_security, database_user_provisioning, privileged_account_monitoring, database_federation

**Application Security:**
- sql_injection_prevention, stored_procedure_security, dynamic_sql_controls, application_whitelisting

**Database-Specific Encryption:**
- tde_key_management, always_encrypted, encrypted_backup_verification, database_masking

**Performance & Availability Security:**
- query_performance_monitoring, database_availability_monitoring, resource_contention_monitoring, deadlock_monitoring

**Database-Specific Auditing:**
- data_access_auditing, schema_change_auditing, privilege_escalation_monitoring, database_activity_monitoring

**Backup & Recovery Security:**
- backup_verification, backup_retention_policy, cross_region_backup, backup_encryption_at_rest

**Database Configuration:**
- database_parameter_hardening, unused_feature_disablement, database_patch_management, database_version_control

**Database Network Security:**
- database_network_segmentation, database_connection_encryption, database_port_security, database_proxy_security

**Database Compliance:**
- data_retention_policy, data_anonymization, database_compliance_reporting, database_risk_assessment

**Database Monitoring:**
- database_security_alerting, database_performance_alerting, database_availability_alerting, database_capacity_alerting

**Database Incident Response:**
- database_incident_response, database_forensics, database_breach_detection, database_recovery_procedures

**Database Threat Protection:**
- database_threat_detection, database_vulnerability_scanning, database_penetration_testing, database_security_baseline

**Database Data Protection:**
- database_data_loss_prevention, database_data_classification, database_privacy_controls, database_consent_management

**Database Operations:**
- database_change_management, database_release_management, database_environment_separation, database_access_review

**Database Business Continuity:**
- database_business_continuity, database_disaster_recovery, database_high_availability, database_load_balancing

**Database Compliance Frameworks:**
- database_sox_compliance, database_pci_compliance, database_hipaa_compliance, database_gdpr_compliance

**Database Observability:**
- database_metrics_collection, database_log_aggregation, database_correlation_analysis, database_behavioral_analysis

## Phase-specific Quality Gates
- Domain-SME review:
  - Validate scope_prefix and domain coverage completeness
  - Confirm risk_id definitions and non-overlap
  - Ensure vendor-neutral language
- CSPM content review:
  - Naming patterns (assertion_id/rule_id) conform
  - Evidence source authoritative and read-only
  - Severity/coverage_tier justified and consistent
  - not_applicable_when is computable
  - adapter_spec.returns aligns with pass_condition
- Coverage and integrity checks:
  - 100% matrix adapters have ≥1 rule
  - 100% rules map back to matrix and assertions
  - jq JSON validation passes

## Automation tips
- Generate missing rules: rule_id = {adapter}.{assertion_tail}
- Tail-fix: ensure rule_id tail == assertion tail
- Re-tier auto-generated rules by adapter keywords: config/enable → core; detect/scan → extended
- Add NA guards tied to probeable conditions (e.g., no_tls_endpoints)

## Key Learnings from Database Expert Review
1. **Database-specific controls are critical**: Generic cloud controls miss database-specific threats (SQL injection, TDE, stored procedures)
2. **Performance security matters**: Resource contention, query monitoring, and availability are security concerns
3. **Compliance frameworks need specific controls**: SOX, PCI, HIPAA, GDPR have database-specific requirements
4. **Operational security is essential**: Change management, release management, environment separation
5. **Threat-specific controls needed**: Database forensics, breach detection, vulnerability scanning
6. **Observability is security**: Metrics, logs, correlation analysis, behavioral analysis
7. **Business continuity is security**: High availability, disaster recovery, load balancing
8. **Data protection goes beyond encryption**: Data loss prevention, classification, privacy controls, consent management