## Phase 4: Generate Rules

Goal: create executable rules per matrix adapter.

Rule schema:
- rule_id: {adapter}.{assertion_tail}
- assertion_id: {domain}.{risk}.{control_name}
- provider, service, resource_type, adapter
- params, pass_condition, not_applicable_when, severity, coverage_tier, evidence_type
- adapter_spec.returns: fields used in pass_condition

Conventions:
- Ensure rule_id tail == assertion tail
- severity: identity/crypto/ddos/ransomware often high; hygiene medium/low
- coverage_tier: core for direct config checks, extended for audit/analytics

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