#!/usr/bin/env ts-node

import * as fs from 'fs';

function main() {
  try {
    // Load the current matrix
    const matrix = JSON.parse(fs.readFileSync('matrices/aws_comprehensive.json', 'utf8'));
    
    // Fix 1: Strong authentication mapping
    matrix['identity_access.authentication'] = {
      "core": [
        {
          "service": "iam",
          "resource": "identity.user",
          "adapter": "aws.iam.user_mfa_status",
          "not_applicable_when": "no_console_users"
        },
        {
          "service": "iam", 
          "resource": "identity.user",
          "adapter": "aws.iam.root_account_status",
          "not_applicable_when": "root_user_not_used"
        }
      ],
      "extended": [
        {
          "service": "identity-center",
          "resource": "identity.tenant",
          "adapter": "aws.identity_center.mfa_settings",
          "not_applicable_when": "identity_center_not_configured"
        }
      ],
      "exhaustive": [
        {
          "service": "cognito",
          "resource": "identity.user",
          "adapter": "aws.cognito.user_pool_mfa_policy",
          "not_applicable_when": "cognito_not_used_for_console_auth"
        }
      ]
    };

    // Fix 2: WAF mapping
    matrix['network_perimeter.firewall_rules'] = {
      "core": [
        {
          "service": "ec2",
          "resource": "network.security_group",
          "adapter": "aws.ec2.security_groups_deny_all_default",
          "not_applicable_when": "no_ec2_instances"
        },
        {
          "service": "wafv2",
          "resource": "edge.waf",
          "adapter": "aws.wafv2.web_acl",
          "not_applicable_when": "no_public_web_applications"
        }
      ],
      "extended": [
        {
          "service": "network-firewall",
          "resource": "network.firewall",
          "adapter": "aws.network_firewall.policy_enforcement",
          "not_applicable_when": "network_firewall_not_configured"
        },
        {
          "service": "cloudfront",
          "resource": "edge.cdn",
          "adapter": "aws.cloudfront.waf_enabled",
          "not_applicable_when": "no_cloudfront_distributions"
        }
      ],
      "exhaustive": [
        {
          "service": "api-gateway",
          "resource": "platform.api_endpoint",
          "adapter": "aws.apigateway.waf_enabled",
          "not_applicable_when": "no_api_gateway_apis"
        }
      ]
    };

    // Fix 3: Encryption-at-rest service mappings
    matrix['crypto_data_protection.encryption_at_rest'] = {
      "core": [
        {
          "service": "s3",
          "resource": "storage.bucket",
          "adapter": "aws.s3.bucket_encryption",
          "not_applicable_when": "no_s3_buckets"
        },
        {
          "service": "rds",
          "resource": "db.instance",
          "adapter": "aws.rds.instance_encryption",
          "not_applicable_when": "no_rds_instances"
        },
        {
          "service": "ec2",
          "resource": "compute.disk",
          "adapter": "aws.ebs.volume_encryption",
          "not_applicable_when": "no_ebs_volumes"
        }
      ],
      "extended": [
        {
          "service": "dynamodb",
          "resource": "storage.table",
          "adapter": "aws.dynamodb.kms_cmk",
          "not_applicable_when": "no_dynamodb_tables"
        },
        {
          "service": "redshift",
          "resource": "db.cluster",
          "adapter": "aws.redshift.cluster_encryption",
          "not_applicable_when": "no_redshift_clusters"
        }
      ],
      "exhaustive": [
        {
          "service": "efs",
          "resource": "storage.fileshare",
          "adapter": "aws.efs.encryption_at_rest",
          "not_applicable_when": "no_efs_filesystems"
        }
      ]
    };

    // Fix 4: Customer managed keys mapping
    matrix['crypto_data_protection.key_management'] = {
      "core": [
        {
          "service": "s3",
          "resource": "storage.bucket",
          "adapter": "aws.s3.bucket_kms",
          "not_applicable_when": "no_s3_buckets"
        },
        {
          "service": "kms",
          "resource": "crypto.kms.key",
          "adapter": "aws.kms.customer_managed_keys",
          "not_applicable_when": "no_kms_keys"
        }
      ],
      "extended": [
        {
          "service": "rds",
          "resource": "db.instance",
          "adapter": "aws.rds.kms_encryption",
          "not_applicable_when": "no_rds_instances"
        },
        {
          "service": "dynamodb",
          "resource": "storage.table",
          "adapter": "aws.dynamodb.kms_cmk",
          "not_applicable_when": "no_dynamodb_tables"
        }
      ],
      "exhaustive": [
        {
          "service": "ec2",
          "resource": "compute.disk",
          "adapter": "aws.ebs.kms_encryption",
          "not_applicable_when": "no_ebs_volumes"
        }
      ]
    };

    // Write the fixed matrix
    fs.writeFileSync('matrices/aws_fixed.json', JSON.stringify(matrix, null, 2));
    
    console.log('✅ Fixed matrix saved to matrices/aws_fixed.json');
    console.log('🔧 Applied fixes:');
    console.log('  - Strong authn: password policy → MFA checks');
    console.log('  - WAF: security groups → wafv2');
    console.log('  - Encryption: fixed service mappings');
    console.log('  - CMK: proper service assignments');
    
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
