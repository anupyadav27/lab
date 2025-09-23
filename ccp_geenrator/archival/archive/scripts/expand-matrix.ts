#!/usr/bin/env ts-node

import * as fs from 'fs';

// Resource type mapping from old to new standardized types
const RESOURCE_TYPE_MAPPING: Record<string, string> = {
  'account': 'identity.user',
  'user': 'identity.user',
  'role': 'rbac.role',
  'policy': 'rbac.policy',
  'group': 'rbac.group',
  'permission_boundary': 'rbac.policy',
  'saml_provider': 'identity.tenant',
  'oidc_provider': 'identity.tenant',
  'user_pool': 'identity.user',
  'identity_pool': 'identity.tenant',
  'instance': 'identity.tenant',
  'directory': 'identity.tenant',
  'trust': 'identity.tenant',
  'analyzer': 'governance.org',
  'bucket': 'storage.bucket',
  'object': 'storage.object',
  'fileshare': 'storage.fileshare',
  'table': 'storage.table',
  'queue': 'storage.queue',
  'snapshot': 'storage.snapshot',
  'vm': 'compute.vm',
  'image': 'compute.image',
  'disk': 'compute.disk',
  'vpc': 'network.vpc',
  'subnet': 'network.subnet',
  'security_group': 'network.security_group',
  'firewall': 'network.firewall',
  'load_balancer': 'network.load_balancer',
  'gateway': 'network.gateway',
  'endpoint': 'network.endpoint',
  'zone': 'dns.zone',
  'waf': 'edge.waf',
  'cdn': 'edge.cdn',
  'cluster': 'k8s.cluster',
  'node_pool': 'k8s.node_pool',
  'namespace': 'k8s.namespace',
  'workload': 'k8s.workload',
  'admission': 'k8s.admission',
  'network_policy': 'k8s.network_policy',
  'function': 'serverless.function',
  'app': 'paas.app',
  'repo': 'registry.repo',
  'sink': 'logging.sink',
  'store': 'logging.store',
  'alert': 'monitoring.alert',
  'metric': 'monitoring.metric',
  'control_plane': 'platform.control_plane',
  'api_endpoint': 'platform.api_endpoint',
  'plan': 'backup.plan',
  'vault': 'backup.vault',
  'dr_plan': 'dr.plan',
  'org': 'governance.org',
  'project': 'governance.project',
  'key': 'crypto.kms.key',
  'secret': 'secrets.secret'
};

// Common N/A conditions
const COMMON_NA_CONDITIONS: Record<string, string> = {
  'iam': 'no_iam_resources',
  'cognito': 'cognito_not_used',
  'identity-center': 'identity_center_not_configured',
  'directory-service': 'directory_service_not_configured',
  'organizations': 'not_using_organizations',
  'access-analyzer': 'access_analyzer_not_configured',
  'secrets-manager': 'no_secrets_manager_secrets',
  'ssm': 'no_ssm_parameters',
  'kms': 'no_kms_keys',
  's3': 'no_s3_buckets',
  'rds': 'no_rds_instances',
  'redshift': 'no_redshift_clusters',
  'dynamodb': 'no_dynamodb_tables',
  'ec2': 'no_ec2_instances',
  'vpc': 'no_vpc_resources',
  'cloudtrail': 'cloudtrail_not_configured',
  'cloudwatch': 'no_cloudwatch_logs',
  'backup': 'backup_service_not_used',
  'ecr': 'no_ecr_repositories',
  'eks': 'no_eks_clusters',
  'lambda': 'no_lambda_functions',
  'api-gateway': 'no_api_gateway_apis',
  'security-hub': 'security_hub_not_configured',
  'config': 'config_not_configured',
  'audit-manager': 'audit_manager_not_configured',
  'inspector': 'inspector_not_configured',
  'guardduty': 'guardduty_not_configured',
  'network-firewall': 'network_firewall_not_configured',
  'wafv2': 'no_public_web_applications',
  'cloudfront': 'no_cloudfront_distributions',
  'route53-resolver': 'dns_firewall_not_configured',
  'vpc-endpoints': 'no_vpc_endpoints'
};

function improveServiceMapping(mapping: any): any {
  const improved = { ...mapping };
  
  // Update resource type if mapping exists
  if (RESOURCE_TYPE_MAPPING[mapping.resource]) {
    improved.resource = RESOURCE_TYPE_MAPPING[mapping.resource];
  }
  
  // Add N/A condition if not present
  if (!improved.not_applicable_when) {
    const serviceName = mapping.service.split('-')[0]; // Handle services like 'identity-center'
    if (COMMON_NA_CONDITIONS[serviceName]) {
      improved.not_applicable_when = COMMON_NA_CONDITIONS[serviceName];
    }
  }
  
  return improved;
}

function main() {
  try {
    // Load original matrix
    const originalMatrix = JSON.parse(fs.readFileSync('matrices/aws.json', 'utf8'));
    
    // Improve each assertion family
    const improvedMatrix: any = {};
    
    for (const [assertionFamily, coverageTiers] of Object.entries(originalMatrix)) {
      improvedMatrix[assertionFamily] = {
        core: (coverageTiers as any).core.map(improveServiceMapping),
        extended: (coverageTiers as any).extended.map(improveServiceMapping),
        exhaustive: (coverageTiers as any).exhaustive.map(improveServiceMapping)
      };
    }
    
    // Write improved matrix
    fs.writeFileSync('matrices/aws_comprehensive.json', JSON.stringify(improvedMatrix, null, 2));
    
    console.log(`✅ Expanded matrix with ${Object.keys(improvedMatrix).length} assertion families`);
    console.log(`📊 Original: ${Object.keys(originalMatrix).length} families`);
    console.log(`📊 Improved: ${Object.keys(improvedMatrix).length} families`);
    
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
