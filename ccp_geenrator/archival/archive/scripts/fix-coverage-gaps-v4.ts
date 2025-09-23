#!/usr/bin/env ts-node

import * as fs from 'fs';

// Timestamp for tracking
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
console.log(`🔧 Fixing Coverage Gaps v4 - ${timestamp}`);

// Load files
const matrix = JSON.parse(fs.readFileSync('matrices/aws_matrix_v2_complete_fixed_2025-09-10T17-02-37.json', 'utf8'));
const rulesData = JSON.parse(fs.readFileSync('out/aws_rules_exhaustive_v2_fixed_2025-09-10T17-02-37.json', 'utf8'));
const rules = rulesData.rules;

console.log(`📊 Current state:`);
console.log(`   Matrix services: ${new Set(Object.values(matrix).flatMap((tiers: any) => 
  Object.values(tiers).flatMap((entries: any) => entries.map((e: any) => e.service))
)).size}`);
console.log(`   Rules services: ${new Set(rules.map((r: any) => r.service)).size}`);

// Service name mapping: matrix (hyphenated) -> rules (underscore)
const serviceNameMapping: Record<string, string> = {
  'identity-center': 'identity_center',
  'directory-service': 'directory_service',
  'parameter-store': 'parameter_store',
  'api-gateway': 'api_gateway',
  'network-firewall': 'network_firewall',
  'route53-resolver': 'route53_resolver',
  'route53-resolver-dns-firewall': 'route53_resolver_dns_firewall',
  'direct-connect': 'direct_connect',
  'transit-gateway': 'transit_gateway',
  'security-hub': 'security_hub',
  'audit-manager': 'audit_manager',
  'elastic-beanstalk': 'elastic_beanstalk',
  'app-runner': 'app_runner',
  'vpc-flow-logs': 'vpc_flow_logs',
  'elasticdisasterrecovery': 'elastic_disaster_recovery',
  'resource-groups': 'resource_groups',
  'cost-explorer': 'cost_explorer',
  'x-ray': 'x_ray',
  'ssmincidents': 'ssm_incidents',
  'kubernetes': 'eks',
  'workdocs': 'work_docs',
  'servicecatalog': 'service_catalog',
  'wellarchitected': 'well_architected',
  'resourceexplorer2': 'resource_explorer2',
  'trustedadvisor': 'trusted_advisor'
};

// Fix 1: Update matrix service names to match rules
console.log('\n🔧 1. Updating matrix service names to match rules...');
let matrixServiceFixes = 0;

Object.entries(matrix).forEach(([assertionFamily, tiers]: [string, any]) => {
  Object.entries(tiers).forEach(([tier, entries]: [string, any]) => {
    entries.forEach((entry: any) => {
      if (serviceNameMapping[entry.service]) {
        entry.service = serviceNameMapping[entry.service];
        matrixServiceFixes++;
      }
    });
  });
});

console.log(`   ✅ Fixed ${matrixServiceFixes} matrix service names`);

// Fix 2: Add missing assertion families to matrix
console.log('\n🔧 2. Adding missing assertion families to matrix...');
let missingFamiliesAdded = 0;

const missingAssertionFamilies = [
  'identity_access.least_privilege',
  'monitoring_security.incident_response',
  'monitoring_security.threat_detection',
  'host_security.vulnerability_management',
  'network_perimeter.ddos_protection',
  'containers_kubernetes.workload_security',
  'data_protection.data_classification',
  'monitoring_security.logging',
  'governance_compliance.infrastructure_as_code',
  'governance_compliance.risk_management'
];

missingAssertionFamilies.forEach(assertionFamily => {
  if (!matrix[assertionFamily]) {
    matrix[assertionFamily] = {
      core: [],
      extended: [],
      exhaustive: []
    };
    missingFamiliesAdded++;
  }
});

console.log(`   ✅ Added ${missingFamiliesAdded} missing assertion families`);

// Fix 3: Add missing services to appropriate assertion families
console.log('\n🔧 3. Adding missing services to assertion families...');
let missingServicesAdded = 0;

const serviceToAssertionMapping: Record<string, string[]> = {
  'identity_center': ['identity_access.authentication', 'identity_access.mfa'],
  'directory_service': ['identity_access.authentication', 'identity_access.mfa'],
  'parameter_store': ['secrets_key_mgmt.secret_storage', 'secrets_key_mgmt.key_protection'],
  'api_gateway': ['serverless_paas.api_security', 'network_perimeter.firewall_rules'],
  'network_firewall': ['network_perimeter.firewall_rules', 'network_perimeter.network_segmentation'],
  'route53_resolver': ['network_perimeter.dns_security', 'network_perimeter.firewall_rules'],
  'route53_resolver_dns_firewall': ['network_perimeter.dns_security', 'network_perimeter.firewall_rules'],
  'direct_connect': ['network_perimeter.vpn_connectivity', 'network_perimeter.network_segmentation'],
  'transit_gateway': ['network_perimeter.network_segmentation', 'network_perimeter.vpn_connectivity'],
  'security_hub': ['compute_host_security.compliance_monitoring', 'compute_host_security.vulnerability_management'],
  'audit_manager': ['governance_compliance.compliance_framework', 'logging_monitoring.audit_logging'],
  'elastic_beanstalk': ['serverless_paas.paas_security', 'compute_host_security.endpoint_protection'],
  'app_runner': ['serverless_paas.paas_security', 'containers_kubernetes.runtime_security'],
  'vpc_flow_logs': ['logging_monitoring.log_collection', 'network_perimeter.firewall_rules'],
  'elastic_disaster_recovery': ['resilience_recovery.disaster_recovery', 'resilience_recovery.recovery_testing'],
  'resource_groups': ['governance_compliance.resource_governance', 'platform_surfaces_versions.platform_monitoring'],
  'cost_explorer': ['governance_compliance.cost_governance', 'governance_compliance.resource_governance'],
  'x_ray': ['logging_monitoring.log_analysis', 'monitoring_security.incident_response'],
  'ssm_incidents': ['monitoring_security.incident_response', 'compute_host_security.compliance_monitoring'],
  'batch': ['compute_host_security.endpoint_protection', 'serverless_paas.paas_security'],
  'work_docs': ['data_protection_storage.data_classification', 'identity_access.authorization'],
  'bedrock': ['data_protection_storage.data_classification', 'crypto_data_protection.encryption_at_rest'],
  'service_catalog': ['governance_compliance.resource_governance', 'governance_compliance.policy_management'],
  'well_architected': ['governance_compliance.compliance_framework', 'platform_surfaces_versions.platform_monitoring'],
  'artifact': ['supply_chain_registries.registry_security', 'supply_chain_registries.build_security'],
  'resource_explorer2': ['governance_compliance.resource_governance', 'platform_surfaces_versions.platform_monitoring'],
  'trusted_advisor': ['governance_compliance.compliance_framework', 'compute_host_security.compliance_monitoring'],
  'dlm': ['data_protection_storage.backup_recovery', 'resilience_recovery.backup_strategy']
};

Object.entries(serviceToAssertionMapping).forEach(([service, assertionFamilies]) => {
  assertionFamilies.forEach(assertionFamily => {
    if (matrix[assertionFamily]) {
      // Check if service already exists in any tier
      const exists = Object.values(matrix[assertionFamily]).some((tier: any) => 
        tier.some((entry: any) => entry.service === service)
      );
      
      if (!exists) {
        // Add to extended tier
        matrix[assertionFamily].extended.push({
          service: service,
          resource: 'platform.control_plane',
          resource_type: 'platform.control_plane',
          adapter: `aws.${service.replace(/_/g, '-')}.${service.split('_').pop()}`,
          not_applicable_when: `no_${service}_configured`
        });
        missingServicesAdded++;
      }
    }
  });
});

console.log(`   ✅ Added ${missingServicesAdded} missing service mappings`);

// Save updated matrix
const matrixOutput = `matrices/aws_matrix_v2_complete_fixed_v4_${timestamp}.json`;
fs.writeFileSync(matrixOutput, JSON.stringify(matrix, null, 2));

console.log('\n📊 Coverage Gap Fix Summary:');
console.log(`   Matrix service name fixes: ${matrixServiceFixes}`);
console.log(`   Missing assertion families added: ${missingFamiliesAdded}`);
console.log(`   Missing services added: ${missingServicesAdded}`);

console.log(`\n📁 Updated matrix saved to: ${matrixOutput}`);

console.log(`\n✅ Coverage Gap Fixes v4 Complete - ${timestamp}`);
