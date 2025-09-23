#!/usr/bin/env ts-node

import * as fs from 'fs';

// Load original rules
const originalRules = JSON.parse(fs.readFileSync('out/aws_rules_exhaustive_fixed.json', 'utf8'));
const originalRulesList = originalRules.rules || originalRules;

// Load new rules
const newRules = JSON.parse(fs.readFileSync('out/aws_rules_exhaustive_v2.json', 'utf8'));

// Load function list services
const functionServices = fs.readFileSync('/Users/apple/Desktop/compliance_Database/Final_Compliance_aws/function_services.txt', 'utf8').trim().split('\n');

// Analyze coverage
function analyzeCoverage() {
  // Original coverage
  const originalServices = new Set(originalRulesList.map((r: any) => r.service));
  const originalServicesCount = originalServices.size;
  const originalRulesCount = originalRulesList.length;

  // New coverage
  const newServices = new Set(newRules.rules.map((r: any) => r.service));
  const newServicesCount = newServices.size;
  const newRulesCount = newRules.rules.length;

  // Function list services (filtered)
  const awsServices = functionServices.filter(service => 
    !['N/A', 'account', 'awareness_training', 'awsbackup', 'awscli', 'awslambda', 
      'disaster_recovery', 'edr', 'personnel_security', 'unmapped'].includes(service)
  );
  const totalAwsServices = awsServices.length;

  // Missing services analysis
  const stillMissing = awsServices.filter(service => !newServices.has(service));
  const newlyAdded = Array.from(newServices).filter(service => !originalServices.has(service));

  // Service coverage by tier
  const coreServices = new Set(newRules.rules.filter((r: any) => r.coverage_tier === 'core').map((r: any) => r.service));
  const extendedServices = new Set(newRules.rules.filter((r: any) => r.coverage_tier === 'extended').map((r: any) => r.service));
  const exhaustiveServices = new Set(newRules.rules.filter((r: any) => r.coverage_tier === 'exhaustive').map((r: any) => r.service));

  // Rules by domain
  const rulesByDomain: Record<string, number> = {};
  newRules.rules.forEach((rule: any) => {
    const domain = rule.assertion_id.split('.')[0];
    rulesByDomain[domain] = (rulesByDomain[domain] || 0) + 1;
  });

  // Priority services coverage
  const priorityServices = [
    'accessanalyzer', 'detective', 'inspector2', 'securityhub', 'shield', 
    'wafv2', 'networkfirewall', 'elbv2', 'directconnect', 'cloudformation', 
    'stepfunctions', 'ecs', 'eks', 'emr', 'glue', 'kinesis', 'firehose', 
    'sagemaker', 'neptune', 'timestream'
  ];
  
  const coveredPriority = priorityServices.filter(service => newServices.has(service));
  const missingPriority = priorityServices.filter(service => !newServices.has(service));

  // Check if we met the ChatGPT requirements
  const requirements = {
    at_least_30_services: (newServicesCount - originalServicesCount) >= 30,
    no_waf_v1: !Array.from(newServices).some((s: any) => s.includes('waf') && !s.includes('wafv2')),
    no_placeholder_conditions: newRules.rules.filter((r: any) => r.pass_condition !== 'TBD-by-adapter').length === newRulesCount,
    priority_services_covered: coveredPriority.length >= 15
  };

  return {
    analysis_date: new Date().toISOString(),
    before: {
      services_count: originalServicesCount,
      rules_count: originalRulesCount,
      coverage_percentage: Math.round((originalServicesCount / totalAwsServices) * 100)
    },
    after: {
      services_count: newServicesCount,
      rules_count: newRulesCount,
      coverage_percentage: Math.round((newServicesCount / totalAwsServices) * 100)
    },
    improvement: {
      services_added: newServicesCount - originalServicesCount,
      rules_added: newRulesCount - originalRulesCount,
      coverage_improvement: Math.round(((newServicesCount - originalServicesCount) / totalAwsServices) * 100)
    },
    services: {
      total_aws_services: totalAwsServices,
      newly_added_services: newlyAdded,
      still_missing_services: stillMissing,
      priority_services_covered: coveredPriority,
      priority_services_missing: missingPriority
    },
    coverage_by_tier: {
      core_services: coreServices.size,
      extended_services: extendedServices.size,
      exhaustive_services: exhaustiveServices.size
    },
    rules_by_domain: rulesByDomain,
    quality_metrics: {
      no_tbd_conditions: newRules.rules.filter((r: any) => r.pass_condition !== 'TBD-by-adapter').length,
      with_adapter_spec: newRules.rules.filter((r: any) => r.adapter_spec).length,
      with_not_applicable: newRules.rules.filter((r: any) => r.not_applicable_when).length,
      critical_severity: newRules.rules.filter((r: any) => r.severity === 'critical').length,
      high_severity: newRules.rules.filter((r: any) => r.severity === 'high').length
    },
    requirements: requirements
  };
}

// Generate coverage report
const report = analyzeCoverage();

// Save report
fs.writeFileSync('coverage_report_v2.json', JSON.stringify(report, null, 2));

console.log('=== AWS Rules Coverage Report v2 ===\n');

console.log('📊 BEFORE vs AFTER:');
console.log(`   Services: ${report.before.services_count} → ${report.after.services_count} (+${report.improvement.services_added})`);
console.log(`   Rules: ${report.before.rules_count} → ${report.after.rules_count} (+${report.improvement.rules_added})`);
console.log(`   Coverage: ${report.before.coverage_percentage}% → ${report.after.coverage_percentage}% (+${report.improvement.coverage_improvement}%)\n`);

console.log('🎯 PRIORITY SERVICES COVERAGE:');
console.log(`   Covered: ${report.services.priority_services_covered.length}/20`);
console.log(`   ✅ ${report.services.priority_services_covered.join(', ')}`);
if (report.services.priority_services_missing.length > 0) {
  console.log(`   ❌ Missing: ${report.services.priority_services_missing.join(', ')}`);
}

console.log('\n📈 COVERAGE BY TIER:');
console.log(`   Core: ${report.coverage_by_tier.core_services} services`);
console.log(`   Extended: ${report.coverage_by_tier.extended_services} services`);
console.log(`   Exhaustive: ${report.coverage_by_tier.exhaustive_services} services`);

console.log('\n🔧 NEWLY ADDED SERVICES:');
report.services.newly_added_services.forEach(service => {
  console.log(`   ✅ ${service}`);
});

console.log('\n📋 RULES BY DOMAIN:');
Object.entries(report.rules_by_domain).forEach(([domain, count]) => {
  console.log(`   ${domain}: ${count} rules`);
});

console.log('\n✅ QUALITY METRICS:');
console.log(`   No TBD conditions: ${report.quality_metrics.no_tbd_conditions}/${report.after.rules_count}`);
console.log(`   With adapter spec: ${report.quality_metrics.with_adapter_spec}/${report.after.rules_count}`);
console.log(`   With N/A logic: ${report.quality_metrics.with_not_applicable}/${report.after.rules_count}`);
console.log(`   Critical severity: ${report.quality_metrics.critical_severity}`);
console.log(`   High severity: ${report.quality_metrics.high_severity}`);

console.log(`\n📁 Detailed report saved to coverage_report_v2.json`);

console.log('\n🎯 CHATGPT REQUIREMENTS CHECK:');
console.log(`   ✅ +30 services: ${report.requirements.at_least_30_services ? 'PASS' : 'FAIL'} (${report.improvement.services_added})`);
console.log(`   ✅ No WAF v1: ${report.requirements.no_waf_v1 ? 'PASS' : 'FAIL'}`);
console.log(`   ✅ No placeholder conditions: ${report.requirements.no_placeholder_conditions ? 'PASS' : 'FAIL'}`);
console.log(`   ✅ Priority services: ${report.requirements.priority_services_covered ? 'PASS' : 'FAIL'} (${report.services.priority_services_covered.length}/20)`);

const allRequirementsMet = Object.values(report.requirements).every(Boolean);
console.log(`\n🏆 ALL REQUIREMENTS MET: ${allRequirementsMet ? 'YES' : 'NO'}`);
