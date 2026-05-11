## Consistency Checks & Automation

Checks:
- Every matrix adapter has ≥1 rule
- rule_id tail equals assertion tail
- resource_type uses the scope's virt.* (or service-specific) type
- not_applicable_when is computable
- adapter_spec.returns covers all pass_condition fields

Automation snippets:
- Tail fix: set rule_id = {adapter}.{assertion_tail}
- Generate missing rules from matrix: derive assertion tail from adapter tail, set minimal pass_condition and adapter_spec, then refine
- Re-tiering: core vs extended by adapter keywords (config/enable vs detect/scan)

Regeneration workflow:
1) Build taxonomy (Phase 1)
2) Generate assertions (Phase 2)
3) Produce matrix (Phase 3)
4) Emit rules (Phase 4)
5) Run consistency checks and auto-fixes
\n## Verification checklist (add to every phase)\n\nBefore moving to next phase, verify:\n- Folders exist:\n  - Step3-matrices-per-cloud-provider/<category>_matrix/\n  - step4-rune-per-cloud-provider/<category>_rules/\n  - step-1-common-taxonomy/\n  - step-2-common-assercian-id/\n- Files created for this run (current timestamp in filename).\n- JSON schema validates (jq parses).\n- rule_id tail == assertion tail.\n- Every matrix adapter has ≥1 rule.\n- Severity and coverage_tier set per conventions.\n- not_applicable_when is computable.\n- adapter_spec.returns covers all pass_condition fields.\n
## Phase-1 enforcement (automation-ready)
- Fail build if any risk_id appears under an 'Uncategorized' domain
- Warn if domain counts below targets (Perf ≥10, Multi-tenant ≥6, Network ≥10, Data Gov ≥10)
- Emit CSV summary: domain,risk_id,title
- Provide remediation hints for low-balance domains (seed items list)
