## Phase 3: Generate Matrix

Goal: map each {domain.risk} to concrete provider services/resources/adapters that supply evidence.

Matrix entry format:
"{domain}.{risk}": [
  { "service": "...", "resource": "{scope}", "adapter": "provider.service.feature", "resource_type": "{scope}", "not_applicable_when": "predicate" }
]

Adapter selection logic:
- Prefer authoritative, read-only config APIs
- If not available, use inventory/metrics/log APIs; last resort derived analytics
- Name: provider.service.feature_action (e.g., vmware.vcenter.sso_mfa_policy)

Coverage tiers:
- core: direct configuration controls
- extended: audits/derived checks
- exhaustive: deep/env-specific

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