#!/usr/bin/env ts-node

import * as fs from 'fs';

// Timestamp for tracking
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
console.log(`🧪 Improving Dry Run v4 - ${timestamp}`);

// Load rules
const rulesData = JSON.parse(fs.readFileSync('out/aws_rules_exhaustive_v2.json', 'utf8'));
const rules = rulesData.rules;

// Representative services for testing
const representativeServices = [
  's3', 'rds', 'ebs', 'kinesis', 'firehose', 
  'elb', 'alb', 'nlb', 'eks', 'backup', 
  'route53', 'drs'
];

console.log(`📊 Testing ${representativeServices.length} representative services...`);

// Enhanced mock adapter payloads for testing
const mockPayloads: Record<string, any> = {
  s3: {
    bucket_name: 'test-bucket',
    default_encryption: {
      enabled: true,
      algorithm: 'AES256',
      key_type: 'AES256'
    },
    public_access_block: {
      block_public_acls: true,
      block_public_policy: true,
      ignore_public_acls: true,
      restrict_public_buckets: true
    },
    versioning: {
      enabled: true
    },
    enabled: true,
    sse_algorithm: 'AES256',
    kms_key_id: 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
  },
  rds: {
    instance_id: 'test-instance',
    storage_encrypted: true,
    kms_key_id: 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012',
    backup_retention_period: 7,
    multi_az: true,
    enabled: true,
    sse_enabled: true
  },
  ebs: {
    volume_id: 'vol-12345678',
    encrypted: true,
    kms_key_id: 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012',
    volume_type: 'gp3',
    enabled: true
  },
  kinesis: {
    stream_name: 'test-stream',
    encryption_enabled: true,
    kms_key_count: 1,
    shard_count: 2,
    enabled: true
  },
  firehose: {
    delivery_stream_name: 'test-stream',
    encryption_enabled: true,
    kms_key_count: 1,
    destination: 's3',
    enabled: true
  },
  elb: {
    load_balancer_name: 'test-elb',
    scheme: 'internet-facing',
    security_groups: ['sg-12345678'],
    listeners: [
      {
        port: 80,
        protocol: 'HTTP'
      }
    ],
    enabled: true
  },
  alb: {
    load_balancer_name: 'test-alb',
    scheme: 'internet-facing',
    security_groups: ['sg-12345678'],
    listeners: [
      {
        port: 443,
        protocol: 'HTTPS',
        ssl_policy: 'ELBSecurityPolicy-TLS-1-2-2017-01'
      }
    ],
    enabled: true
  },
  nlb: {
    load_balancer_name: 'test-nlb',
    scheme: 'internet-facing',
    security_groups: ['sg-12345678'],
    listeners: [
      {
        port: 80,
        protocol: 'TCP'
      }
    ],
    enabled: true
  },
  eks: {
    cluster_name: 'test-cluster',
    encryption_config: {
      enabled: true,
      kms_key_id: 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
    },
    logging: {
      enabled: true
    },
    enabled: true
  },
  backup: {
    backup_vault_name: 'test-vault',
    encryption_key_arn: 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012',
    backup_plan_count: 1,
    enabled: true
  },
  route53: {
    hosted_zone_id: 'Z1234567890',
    name: 'example.com',
    private_zone: false,
    vpc_count: 0,
    enabled: true
  },
  drs: {
    replication_configuration: {
      enabled: true,
      regions: ['us-west-2']
    },
    disaster_recovery_plan_count: 1,
    enabled: true
  }
};

// Test results
const testResults = {
  total_tests: 0,
  passed: 0,
  failed: 0,
  errors: [] as string[],
  warnings: [] as string[],
  service_results: {} as Record<string, any>
};

// Enhanced expression evaluator for pass conditions
function evaluatePassCondition(condition: string, resource: any): boolean {
  try {
    // Replace resource.field with actual values
    let expression = condition;
    const fieldMatches = condition.match(/resource\.(\w+(?:\.\w+)*)/g);
    
    if (fieldMatches) {
      fieldMatches.forEach(match => {
        const fieldPath = match.replace('resource.', '');
        const value = getNestedValue(resource, fieldPath);
        expression = expression.replace(match, JSON.stringify(value));
      });
    }
    
    // Handle common operators and functions
    expression = expression
      .replace(/==/g, '===')
      .replace(/!=/g, '!==')
      .replace(/len\(/g, 'Object.keys(')
      .replace(/max\(/g, 'Math.max(')
      .replace(/min\(/g, 'Math.min(');
    
    // Evaluate the expression safely
    return eval(expression);
  } catch (error) {
    console.log(`   ⚠️  Error evaluating condition: ${condition} - ${error}`);
    return false;
  }
}

// Helper to get nested object values
function getNestedValue(obj: any, path: string): any {
  return path.split('.').reduce((current, key) => current?.[key], obj);
}

// Test each representative service
representativeServices.forEach(service => {
  console.log(`\n🔍 Testing service: ${service}`);
  
  const serviceRules = rules.filter((rule: any) => rule.service === service);
  const mockResource = mockPayloads[service];
  
  if (!mockResource) {
    testResults.warnings.push(`No mock payload for service: ${service}`);
    return;
  }
  
  const serviceResult = {
    service,
    rule_count: serviceRules.length,
    tests: [] as any[]
  };
  
  serviceRules.forEach((rule: any) => {
    testResults.total_tests++;
    
    try {
      const result = evaluatePassCondition(rule.pass_condition, mockResource);
      
      const testResult = {
        rule_id: rule.rule_id,
        assertion_id: rule.assertion_id,
        pass_condition: rule.pass_condition,
        result,
        error: null
      };
      
      serviceResult.tests.push(testResult);
      
      if (result) {
        testResults.passed++;
      } else {
        testResults.failed++;
        testResults.errors.push(`${rule.rule_id}: Pass condition failed - ${rule.pass_condition}`);
      }
    } catch (error) {
      testResults.failed++;
      testResults.errors.push(`${rule.rule_id}: Error evaluating pass condition - ${error}`);
      
      serviceResult.tests.push({
        rule_id: rule.rule_id,
        assertion_id: rule.assertion_id,
        pass_condition: rule.pass_condition,
        result: false,
        error: String(error)
      });
    }
  });
  
  testResults.service_results[service] = serviceResult;
});

// Generate report
const report = {
  timestamp,
  summary: {
    total_tests: testResults.total_tests,
    passed: testResults.passed,
    failed: testResults.failed,
    success_rate: Math.round((testResults.passed / testResults.total_tests) * 100),
    error_count: testResults.errors.length,
    warning_count: testResults.warnings.length
  },
  errors: testResults.errors,
  warnings: testResults.warnings,
  service_results: testResults.service_results
};

// Save report
const reportFile = `dry_run_report_v4_${timestamp}.json`;
fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));

console.log('\n📊 Dry Run Results:');
console.log(`   Total tests: ${testResults.total_tests}`);
console.log(`   Passed: ${testResults.passed}`);
console.log(`   Failed: ${testResults.failed}`);
console.log(`   Success rate: ${report.summary.success_rate}%`);
console.log(`   Errors: ${testResults.errors.length}`);
console.log(`   Warnings: ${testResults.warnings.length}`);

if (testResults.errors.length > 0) {
  console.log('\n❌ Top Errors:');
  testResults.errors.slice(0, 10).forEach(error => console.log(`   ${error}`));
  if (testResults.errors.length > 10) {
    console.log(`   ... and ${testResults.errors.length - 10} more errors`);
  }
}

if (testResults.warnings.length > 0) {
  console.log('\n⚠️  Warnings:');
  testResults.warnings.forEach(warning => console.log(`   ${warning}`));
}

console.log(`\n📁 Report saved to: ${reportFile}`);

if (testResults.failed === 0) {
  console.log('\n✅ All dry run tests passed!');
} else {
  console.log(`\n❌ ${testResults.failed} tests failed`);
}
