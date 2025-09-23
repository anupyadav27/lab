#!/usr/bin/env ts-node

import * as fs from 'fs';

// Timestamp for tracking
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
console.log(`🔍 Schema Lint v3 - ${timestamp}`);

// Load files
const rulesData = JSON.parse(fs.readFileSync('out/aws_rules_exhaustive_v2_fixed_2025-09-10T17-02-37.json', 'utf8'));
const rules = rulesData.rules;
const assertions = JSON.parse(fs.readFileSync('assertions_pack_2025-01-09.json', 'utf8'));

console.log(`📊 Validating ${rules.length} rules...`);

// Resource type allowlist
const resourceTypeAllowlist = [
  'identity.user', 'identity.role', 'identity.service_account', 'identity.tenant',
  'rbac.role', 'rbac.group', 'rbac.policy',
  'secrets.store', 'secrets.secret', 'crypto.kms', 'crypto.kms.key',
  'storage.bucket', 'storage.object', 'storage.fileshare', 'storage.queue', 'storage.table', 'storage.snapshot',
  'db.instance', 'db.cluster', 'db.user',
  'compute.vm', 'compute.image', 'compute.disk',
  'network.vpc', 'network.subnet', 'network.security_group', 'network.firewall', 'network.load_balancer', 'network.gateway', 'network.endpoint',
  'dns.zone', 'edge.waf', 'edge.cdn',
  'k8s.cluster', 'k8s.node_pool', 'k8s.namespace', 'k8s.workload', 'k8s.admission', 'k8s.network_policy',
  'serverless.function', 'paas.app',
  'registry.repo', 'registry.policy',
  'logging.sink', 'logging.store', 'monitoring.alert', 'monitoring.metric',
  'platform.control_plane', 'platform.api_endpoint',
  'backup.plan', 'backup.vault', 'dr.plan',
  'governance.org', 'governance.project'
];

// Service name pattern (lowercase, numbers, underscores, hyphens)
const serviceNamePattern = /^[a-z0-9_-]+$/;

// Assertion ID set
const assertionIds = new Set(assertions.assertions.map((a: any) => a.assertion_id));

// Validation results
const results = {
  totalRules: rules.length,
  errors: [] as string[],
  warnings: [] as string[],
  passed: 0,
  failed: 0
};

console.log('\n🔍 Running validation checks...');

rules.forEach((rule: any, index: number) => {
  const ruleId = rule.rule_id || `rule_${index}`;
  let ruleErrors = 0;
  let ruleWarnings = 0;

  // 1. Check resource_type is required and from allowlist
  if (!rule.resource_type) {
    results.errors.push(`${ruleId}: Missing resource_type`);
    ruleErrors++;
  } else if (!resourceTypeAllowlist.includes(rule.resource_type)) {
    results.errors.push(`${ruleId}: Invalid resource_type '${rule.resource_type}' (not in allowlist)`);
    ruleErrors++;
  }

  // 2. Check service naming convention
  if (!rule.service) {
    results.errors.push(`${ruleId}: Missing service`);
    ruleErrors++;
  } else if (!serviceNamePattern.test(rule.service)) {
    results.errors.push(`${ruleId}: Invalid service name '${rule.service}' (must match [a-z0-9_-]+)`);
    ruleErrors++;
  }

  // 3. Check pass_condition only references fields in adapter_spec.returns
  if (!rule.pass_condition) {
    results.errors.push(`${ruleId}: Missing pass_condition`);
    ruleErrors++;
  } else if (rule.adapter_spec && rule.adapter_spec.returns) {
    const adapterFields = Object.keys(rule.adapter_spec.returns);
    const passConditionFields = rule.pass_condition.match(/resource\.(\w+)/g) || [];
    const referencedFields = passConditionFields.map((f: string) => f.replace('resource.', ''));
    
    const invalidFields = referencedFields.filter((field: string) => !adapterFields.includes(field));
    if (invalidFields.length > 0) {
      results.warnings.push(`${ruleId}: pass_condition references fields not in adapter_spec.returns: ${invalidFields.join(', ')}`);
      ruleWarnings++;
    }
  }

  // 4. Check assertion_id exists in assertions pack
  if (!rule.assertion_id) {
    results.errors.push(`${ruleId}: Missing assertion_id`);
    ruleErrors++;
  } else if (!assertionIds.has(rule.assertion_id)) {
    results.errors.push(`${ruleId}: assertion_id '${rule.assertion_id}' not found in assertions pack`);
    ruleErrors++;
  }

  // 5. Check required fields
  const requiredFields = ['rule_id', 'provider', 'adapter', 'severity', 'coverage_tier', 'evidence_type'];
  requiredFields.forEach(field => {
    if (!rule[field]) {
      results.errors.push(`${ruleId}: Missing required field '${field}'`);
      ruleErrors++;
    }
  });

  // 6. Check severity values
  const validSeverities = ['low', 'medium', 'high', 'critical'];
  if (rule.severity && !validSeverities.includes(rule.severity)) {
    results.errors.push(`${ruleId}: Invalid severity '${rule.severity}' (must be one of: ${validSeverities.join(', ')})`);
    ruleErrors++;
  }

  // 7. Check coverage_tier values
  const validTiers = ['core', 'extended', 'exhaustive'];
  if (rule.coverage_tier && !validTiers.includes(rule.coverage_tier)) {
    results.errors.push(`${ruleId}: Invalid coverage_tier '${rule.coverage_tier}' (must be one of: ${validTiers.join(', ')})`);
    ruleErrors++;
  }

  // 8. Check evidence_type values
  const validEvidenceTypes = ['config_read', 'log_query', 'runtime_observe', 'event_log', 'metric'];
  if (rule.evidence_type && !validEvidenceTypes.includes(rule.evidence_type)) {
    results.errors.push(`${ruleId}: Invalid evidence_type '${rule.evidence_type}' (must be one of: ${validEvidenceTypes.join(', ')})`);
    ruleErrors++;
  }

  // 9. Check for generic pass conditions
  if (rule.pass_condition === 'resource.enabled == true') {
    results.warnings.push(`${ruleId}: Using generic pass_condition 'resource.enabled == true' - consider more specific conditions`);
    ruleWarnings++;
  }

  // 10. Check for missing adapter_spec
  if (!rule.adapter_spec || !rule.adapter_spec.returns) {
    results.warnings.push(`${ruleId}: Missing adapter_spec.returns - consider adding for better documentation`);
    ruleWarnings++;
  }

  if (ruleErrors === 0) {
    results.passed++;
  } else {
    results.failed++;
  }
});

// Generate report
const report = {
  timestamp,
  summary: {
    total_rules: results.totalRules,
    passed: results.passed,
    failed: results.failed,
    error_count: results.errors.length,
    warning_count: results.warnings.length,
    quality_score: Math.round((results.passed / results.totalRules) * 100)
  },
  errors: results.errors,
  warnings: results.warnings,
  resource_type_coverage: {
    used_types: [...new Set(rules.map((r: any) => r.resource_type).filter(Boolean))],
    unused_types: resourceTypeAllowlist.filter(type => !rules.some((r: any) => r.resource_type === type))
  },
  service_coverage: {
    total_services: new Set(rules.map((r: any) => r.service)).size,
    services: [...new Set(rules.map((r: any) => r.service))].sort()
  }
};

// Save report
const reportFile = `schema_lint_report_v3_${timestamp}.json`;
fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));

console.log('\n📊 Schema Lint Results:');
console.log(`   Total rules: ${results.totalRules}`);
console.log(`   Passed: ${results.passed}`);
console.log(`   Failed: ${results.failed}`);
console.log(`   Errors: ${results.errors.length}`);
console.log(`   Warnings: ${results.warnings.length}`);
console.log(`   Quality Score: ${report.summary.quality_score}%`);

if (results.errors.length > 0) {
  console.log('\n❌ Errors:');
  results.errors.slice(0, 10).forEach(error => console.log(`   ${error}`));
  if (results.errors.length > 10) {
    console.log(`   ... and ${results.errors.length - 10} more errors`);
  }
}

if (results.warnings.length > 0) {
  console.log('\n⚠️  Warnings:');
  results.warnings.slice(0, 10).forEach(warning => console.log(`   ${warning}`));
  if (results.warnings.length > 10) {
    console.log(`   ... and ${results.warnings.length - 10} more warnings`);
  }
}

console.log(`\n📁 Report saved to: ${reportFile}`);

if (results.failed === 0) {
  console.log('\n✅ All schema validation checks passed!');
} else {
  console.log(`\n❌ ${results.failed} rules failed validation`);
}
