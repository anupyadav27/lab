#!/usr/bin/env ts-node

import * as fs from 'fs';

// Timestamp for tracking
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
console.log(`🔧 Starting ChatGPT Feedback Fixes v3 - ${timestamp}`);

// Load current files
const matrix = JSON.parse(fs.readFileSync('matrices/aws_matrix_v2_complete.json', 'utf8'));
const rulesData = JSON.parse(fs.readFileSync('out/aws_rules_exhaustive_v2.json', 'utf8'));
const rules = rulesData.rules;
const assertions = JSON.parse(fs.readFileSync('assertions_pack_2025-01-09.json', 'utf8'));

console.log('📊 Current state:');
console.log(`   Matrix entries: ${Object.keys(matrix).length} assertion families`);
console.log(`   Rules: ${rules.length}`);
console.log(`   Assertions: ${assertions.assertions.length}`);

// 1. Fix resource vs resource_type standardization in matrix
console.log('\n🔧 1. Standardizing resource vs resource_type in matrix...');
let matrixFixes = 0;

Object.entries(matrix).forEach(([assertionFamily, tiers]: [string, any]) => {
  Object.entries(tiers).forEach(([tier, entries]: [string, any]) => {
    entries.forEach((entry: any) => {
      // If entry has 'resource' but no 'resource_type', copy it over
      if (entry.resource && !entry.resource_type) {
        entry.resource_type = entry.resource;
        matrixFixes++;
      }
      // If entry has 'resource_type' but no 'resource', copy it over for backward compatibility
      if (entry.resource_type && !entry.resource) {
        entry.resource = entry.resource_type;
        matrixFixes++;
      }
    });
  });
});

console.log(`   ✅ Fixed ${matrixFixes} matrix entries`);

// 2. Fix Kinesis/Firehose resource_type in rules to match matrix
console.log('\n🔧 2. Fixing Kinesis/Firehose resource_type in rules...');
let kinesisFirehoseFixes = 0;

rules.forEach((rule: any) => {
  if ((rule.service === 'kinesis' || rule.service === 'firehose') && 
      rule.resource_type === 'platform.control_plane') {
    rule.resource_type = 'storage.queue';
    kinesisFirehoseFixes++;
  }
});

console.log(`   ✅ Fixed ${kinesisFirehoseFixes} Kinesis/Firehose rules`);

// 3. Tighten pass conditions - replace generic resource.enabled
console.log('\n🔧 3. Tightening pass conditions...');
let passConditionFixes = 0;

const specificPassConditions: Record<string, string> = {
  // S3 encryption
  'aws.s3.bucket_encryption': 'resource.default_encryption.enabled == true && resource.default_encryption.algorithm != "NONE"',
  'aws.s3.bucket_kms': 'resource.default_encryption.enabled == true && resource.default_encryption.key_type == "CMK"',
  
  // RDS encryption
  'aws.rds.instance_encryption': 'resource.storage_encrypted == true && resource.kms_key_id != null',
  'aws.rds.cluster_encryption': 'resource.storage_encrypted == true && resource.kms_key_id != null',
  
  // EBS encryption
  'aws.ebs.volume_encryption': 'resource.encrypted == true && resource.kms_key_id != null',
  
  // DynamoDB encryption
  'aws.dynamodb.table_encryption': 'resource.sse_enabled == true && resource.kms_key_id != null',
  
  // EFS encryption
  'aws.efs.filesystem_encryption': 'resource.encrypted == true && resource.kms_key_id != null',
  
  // Lambda encryption
  'aws.lambda.function_encryption': 'resource.kms_key_arn != null',
  
  // ECS encryption
  'aws.ecs.task_definition': 'resource.encryption_configuration != null',
  
  // EKS encryption
  'aws.eks.cluster_encryption': 'resource.encryption_config != null',
  
  // Backup encryption
  'aws.backup.vault_encryption': 'resource.encryption_key_arn != null',
  
  // Secrets Manager
  'aws.secretsmanager.secret_encryption': 'resource.kms_key_id != null',
  
  // Parameter Store
  'aws.ssm.parameter_encryption': 'resource.type == "SecureString"',
  
  // CloudTrail encryption
  'aws.cloudtrail.trail_encryption': 'resource.kms_key_id != null',
  
  // CloudWatch Logs encryption
  'aws.cloudwatch.log_group_encryption': 'resource.kms_key_id != null',
  
  // SNS encryption
  'aws.sns.topic_encryption': 'resource.kms_master_key_id != null',
  
  // SQS encryption
  'aws.sqs.queue_encryption': 'resource.kms_master_key_id != null'
};

rules.forEach((rule: any) => {
  if (rule.pass_condition === 'resource.enabled == true' && specificPassConditions[rule.adapter]) {
    rule.pass_condition = specificPassConditions[rule.adapter];
    passConditionFixes++;
  }
});

console.log(`   ✅ Fixed ${passConditionFixes} pass conditions`);

// 4. Fix assertion ID alignment - check if child assertions exist
console.log('\n🔧 4. Fixing assertion ID alignment...');
let assertionFixes = 0;

const assertionIds = new Set(assertions.assertions.map((a: any) => a.assertion_id));

rules.forEach((rule: any) => {
  if (!assertionIds.has(rule.assertion_id)) {
    // Try to find parent assertion by removing the last segment
    const parts = rule.assertion_id.split('.');
    if (parts.length > 3) {
      const parentId = parts.slice(0, 3).join('.');
      if (assertionIds.has(parentId)) {
        rule.assertion_id = parentId;
        assertionFixes++;
      }
    }
  }
});

console.log(`   ✅ Fixed ${assertionFixes} assertion IDs`);

// 5. Normalize service names
console.log('\n🔧 5. Normalizing service names...');
let serviceNameFixes = 0;

const serviceNameMappings: Record<string, string> = {
  'route53-resolver-dns-firewall': 'route53_resolver_dns_firewall',
  'route53-resolver': 'route53_resolver',
  'parameter-store': 'parameter_store',
  'identity-center': 'identity_center',
  'directory-service': 'directory_service',
  'network-firewall': 'network_firewall',
  'security-hub': 'security_hub',
  'vpc-flow-logs': 'vpc_flow_logs',
  'transit-gateway': 'transit_gateway',
  'elastic-beanstalk': 'elastic_beanstalk',
  'elasticache': 'elasticache',
  'elasticdisasterrecovery': 'elastic_disaster_recovery',
  'cost-explorer': 'cost_explorer',
  'resource-groups': 'resource_groups',
  'api-gateway': 'api_gateway',
  'app-runner': 'app_runner',
  'audit-manager': 'audit_manager',
  'code-artifact': 'code_artifact',
  'code-build': 'code_build',
  'code-commit': 'code_commit',
  'code-pipeline': 'code_pipeline',
  'direct-connect': 'direct_connect',
  'step-functions': 'step_functions',
  'storage-gateway': 'storage_gateway',
  'trusted-advisor': 'trusted_advisor',
  'well-architected': 'well_architected',
  'work-docs': 'work_docs',
  'x-ray': 'x_ray'
};

rules.forEach((rule: any) => {
  if (serviceNameMappings[rule.service]) {
    rule.service = serviceNameMappings[rule.service];
    serviceNameFixes++;
  }
});

console.log(`   ✅ Fixed ${serviceNameFixes} service names`);

// 6. Add N/A guards for null values
console.log('\n🔧 6. Adding N/A guards for null values...');
let naGuardFixes = 0;

const naGuardMappings: Record<string, string> = {
  'drs': 'no_dr_plans_configured',
  'fis': 'no_chaos_experiments_configured',
  'elb': 'no_load_balancers_configured',
  'nlb': 'no_network_load_balancers_configured',
  'alb': 'no_application_load_balancers_configured',
  'shield': 'no_public_resources',
  'wafv2': 'no_web_applications',
  'cloudfront': 'no_cloudfront_distributions',
  'route53': 'no_dns_zones_configured',
  'backup': 'no_backup_plans_configured',
  'disaster-recovery': 'no_dr_plans_configured',
  'chaos-engineering': 'no_chaos_experiments_configured'
};

rules.forEach((rule: any) => {
  if (rule.not_applicable_when === null && naGuardMappings[rule.service]) {
    rule.not_applicable_when = naGuardMappings[rule.service];
    naGuardFixes++;
  }
});

console.log(`   ✅ Added ${naGuardFixes} N/A guards`);

// 7. Update adapter specs for tightened pass conditions
console.log('\n🔧 7. Updating adapter specs...');
let adapterSpecFixes = 0;

const enhancedAdapterSpecs: Record<string, any> = {
  'aws.s3.bucket_encryption': {
    returns: {
      'default_encryption': 'object - encryption configuration',
      'default_encryption.enabled': 'boolean - whether encryption is enabled',
      'default_encryption.algorithm': 'string - encryption algorithm (AES256, aws:kms, etc.)',
      'default_encryption.key_type': 'string - key type (AES256, CMK)'
    }
  },
  'aws.rds.instance_encryption': {
    returns: {
      'storage_encrypted': 'boolean - whether storage is encrypted',
      'kms_key_id': 'string - KMS key ID for encryption'
    }
  },
  'aws.ebs.volume_encryption': {
    returns: {
      'encrypted': 'boolean - whether volume is encrypted',
      'kms_key_id': 'string - KMS key ID for encryption'
    }
  },
  'aws.dynamodb.table_encryption': {
    returns: {
      'sse_enabled': 'boolean - whether server-side encryption is enabled',
      'kms_key_id': 'string - KMS key ID for encryption'
    }
  }
};

rules.forEach((rule: any) => {
  if (enhancedAdapterSpecs[rule.adapter]) {
    rule.adapter_spec = enhancedAdapterSpecs[rule.adapter];
    adapterSpecFixes++;
  }
});

console.log(`   ✅ Updated ${adapterSpecFixes} adapter specs`);

// Save fixed files with timestamps
const matrixOutput = `matrices/aws_matrix_v2_complete_fixed_${timestamp}.json`;
const rulesOutput = `out/aws_rules_exhaustive_v2_fixed_${timestamp}.json`;

// Update the rules data with fixed rules
rulesData.rules = rules;
rulesData.rule_count = rules.length;

fs.writeFileSync(matrixOutput, JSON.stringify(matrix, null, 2));
fs.writeFileSync(rulesOutput, JSON.stringify(rulesData, null, 2));

console.log('\n📊 Fix Summary:');
console.log(`   Matrix fixes: ${matrixFixes}`);
console.log(`   Kinesis/Firehose fixes: ${kinesisFirehoseFixes}`);
console.log(`   Pass condition fixes: ${passConditionFixes}`);
console.log(`   Assertion ID fixes: ${assertionFixes}`);
console.log(`   Service name fixes: ${serviceNameFixes}`);
console.log(`   N/A guard fixes: ${naGuardFixes}`);
console.log(`   Adapter spec fixes: ${adapterSpecFixes}`);

console.log('\n📁 Output files:');
console.log(`   Matrix: ${matrixOutput}`);
console.log(`   Rules: ${rulesOutput}`);

console.log(`\n✅ ChatGPT Feedback Fixes v3 Complete - ${timestamp}`);
