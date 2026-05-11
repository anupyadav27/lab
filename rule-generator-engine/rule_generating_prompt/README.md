# Rule Generation Prompts

Purpose: reusable prompts and guidelines to regenerate taxonomy (subcat/risk), assertions, matrix, and rules across domains (OS, middleware, databases, network-firewall, load balancer, Docker, workspace, office, web servers, etc.).

Contents:
- phase-1-taxonomy-prompt.md
- phase-2-assertions-prompt.md
- phase-3-matrix-prompt.md
- phase-4-rules-prompt.md
- consistency-checks.md

Naming conventions:
- domain keys use scope-style prefixes: identity, rbac, secrets, crypto, storage, network, compute, mgmt, logging, backup, governance, monitoring
- risk identifiers: lower_snake_case tails (e.g., mfa, certificate_management)
- assertion_id: {domain}.{risk_id}.{control_name}
- rule_id: {adapter}.{assertion_tail}

Mapping logic:
- scope_prefix (domain key) ↔ assertion.scope prefix
- matrix maps each {domain.risk} to provider service/resource/adapter
- rules derive from matrix; adapter provides evidence to satisfy assertion pass_condition
