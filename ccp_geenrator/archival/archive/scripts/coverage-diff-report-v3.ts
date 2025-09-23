#!/usr/bin/env ts-node

import * as fs from 'fs';

// Timestamp for tracking
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
console.log(`📊 Coverage Diff Report v3 - ${timestamp}`);

// Load files
const matrix = JSON.parse(fs.readFileSync('matrices/aws_matrix_v2_complete_fixed_v4_2025-09-11T05-50-34.json', 'utf8'));
const rulesData = JSON.parse(fs.readFileSync('out/aws_rules_exhaustive_v2.json', 'utf8'));
const rules = rulesData.rules;

console.log(`📊 Analyzing coverage differences...`);

// Analyze matrix coverage
const matrixCoverage = {
  assertion_families: Object.keys(matrix).length,
  total_entries: 0,
  services: new Set<string>(),
  by_assertion_family: {} as Record<string, any>,
  by_service: {} as Record<string, any>
};

Object.entries(matrix).forEach(([assertionFamily, tiers]: [string, any]) => {
  const familyData = {
    assertion_family: assertionFamily,
    core: (tiers.core || []).length,
    extended: (tiers.extended || []).length,
    exhaustive: (tiers.exhaustive || []).length,
    total: 0,
    services: new Set<string>()
  };
  
  Object.entries(tiers).forEach(([tier, entries]: [string, any]) => {
    entries.forEach((entry: any) => {
      matrixCoverage.total_entries++;
      familyData.total++;
      matrixCoverage.services.add(entry.service);
      familyData.services.add(entry.service);
      
      if (!matrixCoverage.by_service[entry.service]) {
        matrixCoverage.by_service[entry.service] = {
          service: entry.service,
          assertion_families: new Set<string>(),
          total_entries: 0,
          by_tier: { core: 0, extended: 0, exhaustive: 0 }
        };
      }
      
      matrixCoverage.by_service[entry.service].assertion_families.add(assertionFamily);
      matrixCoverage.by_service[entry.service].total_entries++;
      matrixCoverage.by_service[entry.service].by_tier[tier]++;
    });
  });
  
  matrixCoverage.by_assertion_family[assertionFamily] = familyData;
});

// Analyze rules coverage
const rulesCoverage = {
  total_rules: rules.length,
  services: new Set<string>(),
  by_assertion_family: {} as Record<string, any>,
  by_service: {} as Record<string, any>,
  by_coverage_tier: { core: 0, extended: 0, exhaustive: 0 }
};

rules.forEach((rule: any) => {
  rulesCoverage.services.add(rule.service);
  if (rule.coverage_tier && ['core', 'extended', 'exhaustive'].includes(rule.coverage_tier)) {
    rulesCoverage.by_coverage_tier[rule.coverage_tier as keyof typeof rulesCoverage.by_coverage_tier]++;
  }
  
  const assertionFamily = rule.assertion_id.split('.').slice(0, 2).join('.');
  
  if (!rulesCoverage.by_assertion_family[assertionFamily]) {
    rulesCoverage.by_assertion_family[assertionFamily] = {
      assertion_family: assertionFamily,
      total_rules: 0,
      services: new Set<string>(),
      by_tier: { core: 0, extended: 0, exhaustive: 0 }
    };
  }
  
  rulesCoverage.by_assertion_family[assertionFamily].total_rules++;
  rulesCoverage.by_assertion_family[assertionFamily].services.add(rule.service);
  if (rule.coverage_tier && ['core', 'extended', 'exhaustive'].includes(rule.coverage_tier)) {
    rulesCoverage.by_assertion_family[assertionFamily].by_tier[rule.coverage_tier as keyof typeof rulesCoverage.by_assertion_family[typeof assertionFamily]['by_tier']]++;
  }
  
  if (!rulesCoverage.by_service[rule.service]) {
    rulesCoverage.by_service[rule.service] = {
      service: rule.service,
      total_rules: 0,
      assertion_families: new Set<string>(),
      by_tier: { core: 0, extended: 0, exhaustive: 0 }
    };
  }
  
  rulesCoverage.by_service[rule.service].total_rules++;
  rulesCoverage.by_service[rule.service].assertion_families.add(assertionFamily);
  if (rule.coverage_tier && ['core', 'extended', 'exhaustive'].includes(rule.coverage_tier)) {
    rulesCoverage.by_service[rule.service].by_tier[rule.coverage_tier as keyof typeof rulesCoverage.by_service[typeof rule.service]['by_tier']]++;
  }
});

// Find gaps and mismatches
const gaps = {
  matrix_services_not_in_rules: [] as string[],
  rules_services_not_in_matrix: [] as string[],
  assertion_families_without_rules: [] as string[],
  services_with_matrix_but_no_rules: {} as Record<string, any>,
  assertion_families_with_matrix_but_no_rules: {} as Record<string, any>
};

// Find services in matrix but not in rules
matrixCoverage.services.forEach(service => {
  if (!rulesCoverage.services.has(service)) {
    gaps.matrix_services_not_in_rules.push(service);
    gaps.services_with_matrix_but_no_rules[service] = {
      service,
      matrix_entries: matrixCoverage.by_service[service]?.total_entries || 0,
      assertion_families: Array.from(matrixCoverage.by_service[service]?.assertion_families || [])
    };
  }
});

// Find services in rules but not in matrix
rulesCoverage.services.forEach(service => {
  if (!matrixCoverage.services.has(service)) {
    gaps.rules_services_not_in_matrix.push(service);
  }
});

// Find assertion families in matrix but not in rules
Object.keys(matrixCoverage.by_assertion_family).forEach(assertionFamily => {
  if (!rulesCoverage.by_assertion_family[assertionFamily]) {
    gaps.assertion_families_without_rules.push(assertionFamily);
    gaps.assertion_families_with_matrix_but_no_rules[assertionFamily] = {
      assertion_family: assertionFamily,
      matrix_entries: matrixCoverage.by_assertion_family[assertionFamily].total,
      services: Array.from(matrixCoverage.by_assertion_family[assertionFamily].services)
    };
  }
});

// Generate report
const report = {
  timestamp,
  summary: {
    matrix: {
      assertion_families: matrixCoverage.assertion_families,
      total_entries: matrixCoverage.total_entries,
      unique_services: matrixCoverage.services.size
    },
    rules: {
      total_rules: rulesCoverage.total_rules,
      unique_services: rulesCoverage.services.size,
      by_tier: rulesCoverage.by_coverage_tier
    },
    gaps: {
      matrix_services_not_in_rules: gaps.matrix_services_not_in_rules.length,
      rules_services_not_in_matrix: gaps.rules_services_not_in_matrix.length,
      assertion_families_without_rules: gaps.assertion_families_without_rules.length
    }
  },
  matrix_coverage: {
    by_assertion_family: Object.values(matrixCoverage.by_assertion_family).map((family: any) => ({
      ...family,
      services: Array.from(family.services)
    })),
    by_service: Object.values(matrixCoverage.by_service).map((service: any) => ({
      ...service,
      assertion_families: Array.from(service.assertion_families)
    }))
  },
  rules_coverage: {
    by_assertion_family: Object.values(rulesCoverage.by_assertion_family).map((family: any) => ({
      ...family,
      services: Array.from(family.services)
    })),
    by_service: Object.values(rulesCoverage.by_service).map((service: any) => ({
      ...service,
      assertion_families: Array.from(service.assertion_families)
    }))
  },
  gaps: {
    matrix_services_not_in_rules: gaps.matrix_services_not_in_rules,
    rules_services_not_in_matrix: gaps.rules_services_not_in_matrix,
    assertion_families_without_rules: gaps.assertion_families_without_rules,
    services_with_matrix_but_no_rules: gaps.services_with_matrix_but_no_rules,
    assertion_families_with_matrix_but_no_rules: gaps.assertion_families_with_matrix_but_no_rules
  }
};

// Save report
const reportFile = `coverage_diff_report_v3_${timestamp}.json`;
fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));

console.log('\n📊 Coverage Diff Results:');
console.log(`   Matrix: ${matrixCoverage.assertion_families} families, ${matrixCoverage.total_entries} entries, ${matrixCoverage.services.size} services`);
console.log(`   Rules: ${rulesCoverage.total_rules} rules, ${rulesCoverage.services.size} services`);
console.log(`   Matrix services not in rules: ${gaps.matrix_services_not_in_rules.length}`);
console.log(`   Rules services not in matrix: ${gaps.rules_services_not_in_matrix.length}`);
console.log(`   Assertion families without rules: ${gaps.assertion_families_without_rules.length}`);

if (gaps.matrix_services_not_in_rules.length > 0) {
  console.log('\n⚠️  Matrix services not in rules:');
  gaps.matrix_services_not_in_rules.slice(0, 10).forEach(service => console.log(`   ${service}`));
  if (gaps.matrix_services_not_in_rules.length > 10) {
    console.log(`   ... and ${gaps.matrix_services_not_in_rules.length - 10} more`);
  }
}

if (gaps.rules_services_not_in_matrix.length > 0) {
  console.log('\n⚠️  Rules services not in matrix:');
  gaps.rules_services_not_in_matrix.slice(0, 10).forEach(service => console.log(`   ${service}`));
  if (gaps.rules_services_not_in_matrix.length > 10) {
    console.log(`   ... and ${gaps.rules_services_not_in_matrix.length - 10} more`);
  }
}

if (gaps.assertion_families_without_rules.length > 0) {
  console.log('\n⚠️  Assertion families without rules:');
  gaps.assertion_families_without_rules.slice(0, 10).forEach(family => console.log(`   ${family}`));
  if (gaps.assertion_families_without_rules.length > 10) {
    console.log(`   ... and ${gaps.assertion_families_without_rules.length - 10} more`);
  }
}

console.log(`\n📁 Report saved to: ${reportFile}`);

if (gaps.matrix_services_not_in_rules.length === 0 && 
    gaps.rules_services_not_in_matrix.length === 0 && 
    gaps.assertion_families_without_rules.length === 0) {
  console.log('\n✅ Perfect coverage alignment!');
} else {
  console.log('\n⚠️  Coverage gaps detected - review report for details');
}
