#!/usr/bin/env ts-node

import * as fs from 'fs';

// Enhanced pass condition templates based on ChatGPT suggestions
const ENHANCED_PASS_CONDITIONS: Record<string, { condition: string; adapter_spec: any }> = {
  // SSM Patch Management
  'aws.ssm.patch_management': {
    condition: 'resource.auto_approve == true && resource.compliance_score >= 0.9',
    adapter_spec: {
      returns: {
        'auto_approve': 'boolean - whether automatic patching is enabled',
        'baseline_name': 'string - name of the patch baseline',
        'compliance_score': 'number - compliance score (0.0-1.0)',
        'patch_groups': 'array - list of patch groups'
      }
    }
  },
  'aws.ssm.patch_groups': {
    condition: 'len(resource.patch_groups) > 0 && resource.auto_approve == true',
    adapter_spec: {
      returns: {
        'patch_groups': 'array - list of patch groups',
        'auto_approve': 'boolean - whether automatic patching is enabled',
        'compliance_score': 'number - compliance score (0.0-1.0)'
      }
    }
  },
  'aws.ssm.maintenance_windows': {
    condition: 'len(resource.maintenance_windows) > 0 && resource.enabled == true',
    adapter_spec: {
      returns: {
        'maintenance_windows': 'array - list of maintenance windows',
        'enabled': 'boolean - whether maintenance windows are enabled',
        'schedule': 'string - maintenance window schedule'
      }
    }
  },

  // IAM Policies
  'aws.iam.managed_policies': {
    condition: 'resource.least_privilege_score >= 0.8 && resource.unused_permissions_count == 0',
    adapter_spec: {
      returns: {
        'least_privilege_score': 'number - least privilege compliance score (0.0-1.0)',
        'unused_permissions_count': 'number - count of unused permissions',
        'policy_count': 'number - total number of managed policies',
        'attached_count': 'number - number of attached policies'
      }
    }
  },
  'aws.iam.inline_policies': {
    condition: 'resource.least_privilege_score >= 0.8 && resource.unused_permissions_count == 0',
    adapter_spec: {
      returns: {
        'least_privilege_score': 'number - least privilege compliance score (0.0-1.0)',
        'unused_permissions_count': 'number - count of unused permissions',
        'policy_count': 'number - total number of inline policies',
        'attached_count': 'number - number of attached policies'
      }
    }
  },
  'aws.iam.organization_policies': {
    condition: 'resource.scp_count > 0 && resource.deny_all_default == true',
    adapter_spec: {
      returns: {
        'scp_count': 'number - number of service control policies',
        'deny_all_default': 'boolean - whether default deny is enabled',
        'policy_count': 'number - total number of organization policies',
        'enabled': 'boolean - whether organization policies are enabled'
      }
    }
  },
  'aws.iam.resource_based_policies': {
    condition: 'resource.least_privilege_score >= 0.8 && resource.public_access_count == 0',
    adapter_spec: {
      returns: {
        'least_privilege_score': 'number - least privilege compliance score (0.0-1.0)',
        'public_access_count': 'number - count of policies allowing public access',
        'policy_count': 'number - total number of resource-based policies',
        'unused_permissions_count': 'number - count of unused permissions'
      }
    }
  },
  'aws.iam.group_memberships': {
    condition: 'resource.least_privilege_score >= 0.8 && resource.unused_groups_count == 0',
    adapter_spec: {
      returns: {
        'least_privilege_score': 'number - least privilege compliance score (0.0-1.0)',
        'unused_groups_count': 'number - count of unused groups',
        'group_count': 'number - total number of groups',
        'member_count': 'number - total number of group members'
      }
    }
  },
  'aws.iam.custom_policies': {
    condition: 'resource.least_privilege_score >= 0.8 && resource.unused_permissions_count == 0',
    adapter_spec: {
      returns: {
        'least_privilege_score': 'number - least privilege compliance score (0.0-1.0)',
        'unused_permissions_count': 'number - count of unused permissions',
        'policy_count': 'number - total number of custom policies',
        'attached_count': 'number - number of attached policies'
      }
    }
  },

  // KMS
  'aws.kms.key_usage': {
    condition: 'resource.usage_count > 0 && resource.rotation_enabled == true',
    adapter_spec: {
      returns: {
        'usage_count': 'number - number of times key has been used',
        'rotation_enabled': 'boolean - whether key rotation is enabled',
        'key_count': 'number - total number of keys',
        'active_count': 'number - number of active keys'
      }
    }
  },
  'aws.kms.key_storage': {
    condition: 'resource.encryption_enabled == true && resource.hsm_protection == true',
    adapter_spec: {
      returns: {
        'encryption_enabled': 'boolean - whether encryption is enabled',
        'hsm_protection': 'boolean - whether HSM protection is enabled',
        'key_count': 'number - total number of keys',
        'customer_managed_count': 'number - number of customer-managed keys'
      }
    }
  },
  'aws.kms.key_protection': {
    condition: 'resource.hsm_protection == true && resource.import_key_material == false',
    adapter_spec: {
      returns: {
        'hsm_protection': 'boolean - whether HSM protection is enabled',
        'import_key_material': 'boolean - whether key material is imported',
        'key_count': 'number - total number of keys',
        'protection_level': 'string - protection level (HSM, SOFTWARE)'
      }
    }
  },
  'aws.kms.key_policies': {
    condition: 'resource.least_privilege_score >= 0.8 && resource.public_access_count == 0',
    adapter_spec: {
      returns: {
        'least_privilege_score': 'number - least privilege compliance score (0.0-1.0)',
        'public_access_count': 'number - count of policies allowing public access',
        'policy_count': 'number - total number of key policies',
        'unused_permissions_count': 'number - count of unused permissions'
      }
    }
  },
  'aws.kms.hsm_protection': {
    condition: 'resource.hsm_protection == true && resource.import_key_material == false',
    adapter_spec: {
      returns: {
        'hsm_protection': 'boolean - whether HSM protection is enabled',
        'import_key_material': 'boolean - whether key material is imported',
        'key_count': 'number - total number of HSM-protected keys',
        'protection_level': 'string - protection level (HSM)'
      }
    }
  },
  'aws.kms.customer_managed_keys': {
    condition: 'resource.customer_managed_count > 0 && resource.rotation_enabled == true',
    adapter_spec: {
      returns: {
        'customer_managed_count': 'number - number of customer-managed keys',
        'rotation_enabled': 'boolean - whether key rotation is enabled',
        'key_count': 'number - total number of keys',
        'hsm_protection': 'boolean - whether HSM protection is enabled'
      }
    }
  },
  'aws.kms.import_key_material': {
    condition: 'resource.import_key_material == false && resource.hsm_protection == true',
    adapter_spec: {
      returns: {
        'import_key_material': 'boolean - whether key material is imported',
        'hsm_protection': 'boolean - whether HSM protection is enabled',
        'key_count': 'number - total number of keys',
        'protection_level': 'string - protection level (HSM, SOFTWARE)'
      }
    }
  },
  'aws.kms.crypto_policies': {
    condition: 'resource.crypto_policies_enabled == true && resource.algorithm_compliance == true',
    adapter_spec: {
      returns: {
        'crypto_policies_enabled': 'boolean - whether crypto policies are enabled',
        'algorithm_compliance': 'boolean - whether algorithms are compliant',
        'policy_count': 'number - total number of crypto policies',
        'compliance_score': 'number - compliance score (0.0-1.0)'
      }
    }
  },

  // CloudWatch
  'aws.cloudwatch.log_collection': {
    condition: 'resource.log_groups_count > 0 && resource.retention_days >= 90',
    adapter_spec: {
      returns: {
        'log_groups_count': 'number - number of log groups',
        'retention_days': 'number - log retention period in days',
        'enabled': 'boolean - whether log collection is enabled',
        'encryption_enabled': 'boolean - whether logs are encrypted'
      }
    }
  },
  'aws.cloudwatch.alarms': {
    condition: 'resource.alarm_count > 0 && resource.enabled_alarms_count > 0',
    adapter_spec: {
      returns: {
        'alarm_count': 'number - total number of alarms',
        'enabled_alarms_count': 'number - number of enabled alarms',
        'action_enabled': 'boolean - whether alarm actions are enabled',
        'threshold_breaches': 'number - number of threshold breaches'
      }
    }
  },
  'aws.cloudwatch.insights_queries': {
    condition: 'resource.query_count > 0 && resource.scheduled_queries_count > 0',
    adapter_spec: {
      returns: {
        'query_count': 'number - total number of queries',
        'scheduled_queries_count': 'number - number of scheduled queries',
        'enabled': 'boolean - whether insights queries are enabled',
        'retention_days': 'number - query retention period in days'
      }
    }
  },

  // CloudTrail
  'aws.cloudtrail.log_collection': {
    condition: 'resource.trail_count > 0 && resource.logging_enabled == true',
    adapter_spec: {
      returns: {
        'trail_count': 'number - number of CloudTrail trails',
        'logging_enabled': 'boolean - whether logging is enabled',
        'encryption_enabled': 'boolean - whether logs are encrypted',
        'multi_region': 'boolean - whether multi-region logging is enabled'
      }
    }
  },
  'aws.cloudtrail.insights': {
    condition: 'resource.insights_enabled == true && resource.anomaly_detection == true',
    adapter_spec: {
      returns: {
        'insights_enabled': 'boolean - whether insights are enabled',
        'anomaly_detection': 'boolean - whether anomaly detection is enabled',
        'event_count': 'number - number of events analyzed',
        'anomaly_count': 'number - number of anomalies detected'
      }
    }
  },

  // S3
  'aws.s3.object_locking': {
    condition: 'resource.object_locking_enabled == true && resource.retention_period_days >= 30',
    adapter_spec: {
      returns: {
        'object_locking_enabled': 'boolean - whether object locking is enabled',
        'retention_period_days': 'number - retention period in days',
        'bucket_count': 'number - number of buckets with object locking',
        'compliance_mode': 'string - compliance mode (GOVERNANCE, COMPLIANCE)'
      }
    }
  },
  'aws.s3.object_classification': {
    condition: 'resource.classification_enabled == true && resource.sensitive_data_count == 0',
    adapter_spec: {
      returns: {
        'classification_enabled': 'boolean - whether classification is enabled',
        'sensitive_data_count': 'number - count of sensitive data objects',
        'bucket_count': 'number - number of buckets with classification',
        'classification_rules_count': 'number - number of classification rules'
      }
    }
  },
  'aws.s3.data_classification': {
    condition: 'resource.classification_enabled == true && resource.sensitive_data_count == 0',
    adapter_spec: {
      returns: {
        'classification_enabled': 'boolean - whether data classification is enabled',
        'sensitive_data_count': 'number - count of sensitive data objects',
        'bucket_count': 'number - number of buckets with data classification',
        'classification_rules_count': 'number - number of classification rules'
      }
    }
  },

  // RDS
  'aws.rds.version_management': {
    condition: 'resource.auto_minor_version_upgrade == true && resource.engine_version_latest == true',
    adapter_spec: {
      returns: {
        'auto_minor_version_upgrade': 'boolean - whether auto minor version upgrade is enabled',
        'engine_version_latest': 'boolean - whether engine version is latest',
        'instance_count': 'number - total number of RDS instances',
        'outdated_count': 'number - number of outdated instances'
      }
    }
  },
  'aws.rds.deprecation_management': {
    condition: 'resource.deprecation_warnings_count == 0 && resource.engine_version_supported == true',
    adapter_spec: {
      returns: {
        'deprecation_warnings_count': 'number - number of deprecation warnings',
        'engine_version_supported': 'boolean - whether engine version is supported',
        'instance_count': 'number - total number of RDS instances',
        'end_of_life_count': 'number - number of instances with end-of-life versions'
      }
    }
  },

  // EKS
  'aws.eks.version_management': {
    condition: 'resource.cluster_version_latest == true && resource.node_group_version_latest == true',
    adapter_spec: {
      returns: {
        'cluster_version_latest': 'boolean - whether cluster version is latest',
        'node_group_version_latest': 'boolean - whether node group version is latest',
        'cluster_count': 'number - total number of EKS clusters',
        'outdated_count': 'number - number of outdated clusters'
      }
    }
  },
  'aws.eks.opa_gatekeeper': {
    condition: 'resource.opa_gatekeeper_enabled == true && resource.policy_violations_count == 0',
    adapter_spec: {
      returns: {
        'opa_gatekeeper_enabled': 'boolean - whether OPA Gatekeeper is enabled',
        'policy_violations_count': 'number - number of policy violations',
        'cluster_count': 'number - number of clusters with OPA Gatekeeper',
        'policies_count': 'number - number of OPA policies'
      }
    }
  },
  'aws.eks.oidc_identity_provider': {
    condition: 'resource.oidc_provider_enabled == true && resource.identity_provider_count > 0',
    adapter_spec: {
      returns: {
        'oidc_provider_enabled': 'boolean - whether OIDC provider is enabled',
        'identity_provider_count': 'number - number of identity providers',
        'cluster_count': 'number - number of clusters with OIDC',
        'trust_relationship_count': 'number - number of trust relationships'
      }
    }
  },
  'aws.eks.kyverno_policies': {
    condition: 'resource.kyverno_enabled == true && resource.policy_violations_count == 0',
    adapter_spec: {
      returns: {
        'kyverno_enabled': 'boolean - whether Kyverno is enabled',
        'policy_violations_count': 'number - number of policy violations',
        'cluster_count': 'number - number of clusters with Kyverno',
        'policies_count': 'number - number of Kyverno policies'
      }
    }
  },
  'aws.eks.cni_addon': {
    condition: 'resource.cni_addon_enabled == true && resource.addon_version_latest == true',
    adapter_spec: {
      returns: {
        'cni_addon_enabled': 'boolean - whether CNI addon is enabled',
        'addon_version_latest': 'boolean - whether addon version is latest',
        'cluster_count': 'number - number of clusters with CNI addon',
        'addon_count': 'number - total number of CNI addons'
      }
    }
  },

  // EC2
  'aws.ec2.vpc_flow_logs': {
    condition: 'resource.flow_logs_enabled == true && resource.traffic_type_all == true',
    adapter_spec: {
      returns: {
        'flow_logs_enabled': 'boolean - whether VPC flow logs are enabled',
        'traffic_type_all': 'boolean - whether all traffic types are logged',
        'vpc_count': 'number - number of VPCs with flow logs',
        'log_destination_count': 'number - number of log destinations'
      }
    }
  },
  'aws.ec2.vpc_peering': {
    condition: 'resource.peering_connections_count > 0 && resource.cross_account_peering_count == 0',
    adapter_spec: {
      returns: {
        'peering_connections_count': 'number - number of peering connections',
        'cross_account_peering_count': 'number - number of cross-account peering connections',
        'vpc_count': 'number - number of VPCs with peering',
        'accepted_connections_count': 'number - number of accepted peering connections'
      }
    }
  },
  'aws.ec2.version_management': {
    condition: 'resource.instance_version_latest == true && resource.deprecated_instance_types_count == 0',
    adapter_spec: {
      returns: {
        'instance_version_latest': 'boolean - whether instance version is latest',
        'deprecated_instance_types_count': 'number - number of deprecated instance types',
        'instance_count': 'number - total number of EC2 instances',
        'outdated_count': 'number - number of outdated instances'
      }
    }
  },
  'aws.ec2.deprecation_management': {
    condition: 'resource.deprecation_warnings_count == 0 && resource.end_of_life_count == 0',
    adapter_spec: {
      returns: {
        'deprecation_warnings_count': 'number - number of deprecation warnings',
        'end_of_life_count': 'number - number of end-of-life instances',
        'instance_count': 'number - total number of EC2 instances',
        'supported_count': 'number - number of supported instances'
      }
    }
  },
  'aws.ec2.route_tables': {
    condition: 'resource.route_tables_count > 0 && resource.public_routes_count == 0',
    adapter_spec: {
      returns: {
        'route_tables_count': 'number - number of route tables',
        'public_routes_count': 'number - number of public routes',
        'vpc_count': 'number - number of VPCs with route tables',
        'private_routes_count': 'number - number of private routes'
      }
    }
  },

  // Route53
  'aws.route53.health_checks': {
    condition: 'resource.health_checks_count > 0 && resource.failed_checks_count == 0',
    adapter_spec: {
      returns: {
        'health_checks_count': 'number - number of health checks',
        'failed_checks_count': 'number - number of failed health checks',
        'enabled_count': 'number - number of enabled health checks',
        'alarm_count': 'number - number of health check alarms'
      }
    }
  },

  // Route53 Resolver
  'aws.r53r.resolver_rules': {
    condition: 'resource.resolver_rules_count > 0 && resource.forwarding_enabled == true',
    adapter_spec: {
      returns: {
        'resolver_rules_count': 'number - number of resolver rules',
        'forwarding_enabled': 'boolean - whether forwarding is enabled',
        'vpc_count': 'number - number of VPCs with resolver rules',
        'dns_queries_count': 'number - number of DNS queries processed'
      }
    }
  },
  'aws.r53r.df.rule_groups': {
    condition: 'resource.rule_groups_count > 0 && resource.blocking_enabled == true',
    adapter_spec: {
      returns: {
        'rule_groups_count': 'number - number of DNS firewall rule groups',
        'blocking_enabled': 'boolean - whether blocking is enabled',
        'vpc_count': 'number - number of VPCs with DNS firewall',
        'blocked_queries_count': 'number - number of blocked DNS queries'
      }
    }
  },

  // Macie
  'aws.macie.data_classification': {
    condition: 'resource.classification_enabled == true && resource.sensitive_data_count == 0',
    adapter_spec: {
      returns: {
        'classification_enabled': 'boolean - whether data classification is enabled',
        'sensitive_data_count': 'number - count of sensitive data findings',
        'bucket_count': 'number - number of buckets scanned',
        'findings_count': 'number - total number of findings'
      }
    }
  },
  'aws.macie.sensitive_data_discovery': {
    condition: 'resource.discovery_enabled == true && resource.sensitive_data_count == 0',
    adapter_spec: {
      returns: {
        'discovery_enabled': 'boolean - whether sensitive data discovery is enabled',
        'sensitive_data_count': 'number - count of sensitive data findings',
        'bucket_count': 'number - number of buckets scanned',
        'findings_count': 'number - total number of findings'
      }
    }
  },

  // Lambda
  'aws.lambda.deprecation_management': {
    condition: 'resource.deprecation_warnings_count == 0 && resource.runtime_supported == true',
    adapter_spec: {
      returns: {
        'deprecation_warnings_count': 'number - number of deprecation warnings',
        'runtime_supported': 'boolean - whether runtime is supported',
        'function_count': 'number - total number of Lambda functions',
        'end_of_life_count': 'number - number of functions with end-of-life runtimes'
      }
    }
  },

  // DynamoDB
  'aws.dynamodb.point_in_time_recovery': {
    condition: 'resource.point_in_time_recovery_enabled == true && resource.backup_enabled == true',
    adapter_spec: {
      returns: {
        'point_in_time_recovery_enabled': 'boolean - whether point-in-time recovery is enabled',
        'backup_enabled': 'boolean - whether backup is enabled',
        'table_count': 'number - total number of DynamoDB tables',
        'protected_count': 'number - number of protected tables'
      }
    }
  },
  'aws.dynamodb.data_masking': {
    condition: 'resource.data_masking_enabled == true && resource.sensitive_data_count == 0',
    adapter_spec: {
      returns: {
        'data_masking_enabled': 'boolean - whether data masking is enabled',
        'sensitive_data_count': 'number - count of sensitive data items',
        'table_count': 'number - total number of DynamoDB tables',
        'masking_rules_count': 'number - number of masking rules'
      }
    }
  },

  // RDS Data Masking
  'aws.rds.data_masking': {
    condition: 'resource.data_masking_enabled == true && resource.sensitive_data_count == 0',
    adapter_spec: {
      returns: {
        'data_masking_enabled': 'boolean - whether data masking is enabled',
        'sensitive_data_count': 'number - count of sensitive data items',
        'instance_count': 'number - total number of RDS instances',
        'masking_rules_count': 'number - number of masking rules'
      }
    }
  },

  // Redshift Data Masking
  'aws.redshift.data_masking': {
    condition: 'resource.data_masking_enabled == true && resource.sensitive_data_count == 0',
    adapter_spec: {
      returns: {
        'data_masking_enabled': 'boolean - whether data masking is enabled',
        'sensitive_data_count': 'number - count of sensitive data items',
        'cluster_count': 'number - total number of Redshift clusters',
        'masking_rules_count': 'number - number of masking rules'
      }
    }
  },

  // Glacier
  'aws.glacier.vault_lock': {
    condition: 'resource.vault_lock_enabled == true && resource.retention_period_days >= 90',
    adapter_spec: {
      returns: {
        'vault_lock_enabled': 'boolean - whether vault lock is enabled',
        'retention_period_days': 'number - retention period in days',
        'vault_count': 'number - number of Glacier vaults',
        'compliance_mode': 'string - compliance mode (GOVERNANCE, COMPLIANCE)'
      }
    }
  },

  // ACM
  'aws.acm.private_ca': {
    condition: 'resource.private_ca_enabled == true && resource.certificate_count > 0',
    adapter_spec: {
      returns: {
        'private_ca_enabled': 'boolean - whether private CA is enabled',
        'certificate_count': 'number - number of certificates issued',
        'ca_count': 'number - number of private CAs',
        'valid_certificates_count': 'number - number of valid certificates'
      }
    }
  },

  // FIS
  'aws.fis.chaos_engineering': {
    condition: 'resource.chaos_experiments_count > 0 && resource.experiments_enabled == true',
    adapter_spec: {
      returns: {
        'chaos_experiments_count': 'number - number of chaos experiments',
        'experiments_enabled': 'boolean - whether experiments are enabled',
        'target_count': 'number - number of experiment targets',
        'successful_experiments_count': 'number - number of successful experiments'
      }
    }
  },

  // Cognito
  'aws.cognito.identity_pools': {
    condition: 'resource.identity_pools_count > 0 && resource.mfa_enabled == true',
    adapter_spec: {
      returns: {
        'identity_pools_count': 'number - number of identity pools',
        'mfa_enabled': 'boolean - whether MFA is enabled',
        'user_pool_count': 'number - number of user pools',
        'authenticated_users_count': 'number - number of authenticated users'
      }
    }
  },

  // CodeArtifact
  'aws.codeartifact.dependency_management': {
    condition: 'resource.dependency_scanning_enabled == true && resource.vulnerability_count == 0',
    adapter_spec: {
      returns: {
        'dependency_scanning_enabled': 'boolean - whether dependency scanning is enabled',
        'vulnerability_count': 'number - number of vulnerabilities found',
        'repository_count': 'number - number of repositories',
        'package_count': 'number - number of packages scanned'
      }
    }
  },

  // ECR
  'aws.ecr.software_bill_of_materials': {
    condition: 'resource.sbom_enabled == true && resource.vulnerability_count == 0',
    adapter_spec: {
      returns: {
        'sbom_enabled': 'boolean - whether SBOM is enabled',
        'vulnerability_count': 'number - number of vulnerabilities found',
        'image_count': 'number - number of container images',
        'repository_count': 'number - number of ECR repositories'
      }
    }
  },

  // Secrets Manager
  'aws.secrets_manager.secret_storage': {
    condition: 'resource.secret_count > 0 && resource.encryption_enabled == true',
    adapter_spec: {
      returns: {
        'secret_count': 'number - number of secrets stored',
        'encryption_enabled': 'boolean - whether secrets are encrypted',
        'rotation_enabled': 'boolean - whether secret rotation is enabled',
        'kms_key_count': 'number - number of KMS keys used'
      }
    }
  },
  'aws.secrets_manager.retrieval': {
    condition: 'resource.retrieval_logging_enabled == true && resource.unauthorized_access_count == 0',
    adapter_spec: {
      returns: {
        'retrieval_logging_enabled': 'boolean - whether retrieval logging is enabled',
        'unauthorized_access_count': 'number - number of unauthorized access attempts',
        'secret_count': 'number - number of secrets accessed',
        'access_count': 'number - total number of access attempts'
      }
    }
  },

  // IAM specific
  'aws.iam.session_duration': {
    condition: 'resource.max_session_duration_hours <= 8 && resource.role_count > 0',
    adapter_spec: {
      returns: {
        'max_session_duration_hours': 'number - maximum session duration in hours',
        'role_count': 'number - number of IAM roles',
        'assumed_role_count': 'number - number of assumed roles',
        'session_count': 'number - total number of active sessions'
      }
    }
  },
  'aws.iam.mfa': {
    condition: 'resource.mfa_enabled_count == resource.user_count && resource.hardware_mfa_count > 0',
    adapter_spec: {
      returns: {
        'mfa_enabled_count': 'number - number of users with MFA enabled',
        'user_count': 'number - total number of users',
        'hardware_mfa_count': 'number - number of users with hardware MFA',
        'software_mfa_count': 'number - number of users with software MFA'
      }
    }
  },
  'aws.iam.entitlement_policies': {
    condition: 'resource.entitlement_policies_count > 0 && resource.least_privilege_score >= 0.8',
    adapter_spec: {
      returns: {
        'entitlement_policies_count': 'number - number of entitlement policies',
        'least_privilege_score': 'number - least privilege compliance score (0.0-1.0)',
        'policy_count': 'number - total number of policies',
        'unused_permissions_count': 'number - count of unused permissions'
      }
    }
  },
  'aws.iam.crypto_policies': {
    condition: 'resource.crypto_policies_enabled == true && resource.algorithm_compliance == true',
    adapter_spec: {
      returns: {
        'crypto_policies_enabled': 'boolean - whether crypto policies are enabled',
        'algorithm_compliance': 'boolean - whether algorithms are compliant',
        'policy_count': 'number - total number of crypto policies',
        'compliance_score': 'number - compliance score (0.0-1.0)'
      }
    }
  },

  // SSO
  'aws.sso.mfa': {
    condition: 'resource.mfa_required == true && resource.identity_provider_count > 0',
    adapter_spec: {
      returns: {
        'mfa_required': 'boolean - whether MFA is required',
        'identity_provider_count': 'number - number of identity providers',
        'user_count': 'number - total number of SSO users',
        'mfa_enabled_count': 'number - number of users with MFA enabled'
      }
    }
  },

  // SAML/OIDC
  'aws.iam.saml_providers': {
    condition: 'resource.saml_providers_count > 0 && resource.trust_relationship_count > 0',
    adapter_spec: {
      returns: {
        'saml_providers_count': 'number - number of SAML providers',
        'trust_relationship_count': 'number - number of trust relationships',
        'enabled_count': 'number - number of enabled SAML providers',
        'federation_count': 'number - number of federated users'
      }
    }
  },
  'aws.iam.oidc_providers': {
    condition: 'resource.oidc_providers_count > 0 && resource.trust_relationship_count > 0',
    adapter_spec: {
      returns: {
        'oidc_providers_count': 'number - number of OIDC providers',
        'trust_relationship_count': 'number - number of trust relationships',
        'enabled_count': 'number - number of enabled OIDC providers',
        'federation_count': 'number - number of federated users'
      }
    }
  },
  'aws.sso.external_identity_providers': {
    condition: 'resource.external_providers_count > 0 && resource.federation_enabled == true',
    adapter_spec: {
      returns: {
        'external_providers_count': 'number - number of external identity providers',
        'federation_enabled': 'boolean - whether federation is enabled',
        'user_count': 'number - total number of federated users',
        'active_providers_count': 'number - number of active providers'
      }
    }
  }
};

// Resource type corrections based on ChatGPT suggestions
const RESOURCE_TYPE_CORRECTIONS: Record<string, string> = {
  'identity.tenant': 'platform.control_plane', // For account-level controls
  'k8s.cluster': 'platform.control_plane', // For cluster-level controls
  'governance.org': 'platform.control_plane', // For organization-level controls
  'rbac.policy': 'rbac.policy', // Keep as is
  'rbac.role': 'rbac.role', // Keep as is
  'rbac.group': 'rbac.group', // Keep as is
  'identity.user': 'identity.user', // Keep as is
  'compute.vm': 'compute.vm', // Keep as is
  'db.instance': 'db.instance', // Keep as is
  'storage.bucket': 'storage.bucket', // Keep as is
  'network.security_group': 'network.security_group', // Keep as is
  'edge.waf': 'edge.waf', // Keep as is
  'crypto.kms.key': 'crypto.kms.key' // Keep as is
};

function fixRules() {
  try {
    // Load the current rules
    const rulesData = JSON.parse(fs.readFileSync('out/aws_rules_exhaustive.json', 'utf8'));
    const rules = rulesData.rules || rulesData;

    console.log(`Loaded ${rules.length} rules`);

    let fixedCount = 0;
    let resourceTypeFixedCount = 0;

    // Fix each rule
    for (const rule of rules) {
      // Fix 1: Replace TBD-by-adapter with concrete pass conditions
      if (rule.pass_condition === 'TBD-by-adapter') {
        const adapter = rule.adapter;
        if (ENHANCED_PASS_CONDITIONS[adapter]) {
          rule.pass_condition = ENHANCED_PASS_CONDITIONS[adapter].condition;
          rule.adapter_spec = ENHANCED_PASS_CONDITIONS[adapter].adapter_spec;
          fixedCount++;
        }
      }

      // Fix 2: Correct resource_type values
      if (RESOURCE_TYPE_CORRECTIONS[rule.resource_type]) {
        rule.resource_type = RESOURCE_TYPE_CORRECTIONS[rule.resource_type];
        resourceTypeFixedCount++;
      }

      // Fix 3: Ensure adapter_spec exists for non-TBD rules
      if (rule.pass_condition !== 'TBD-by-adapter' && !rule.adapter_spec) {
        rule.adapter_spec = {
          returns: {
            'resource': 'object - adapter-specific resource data'
          }
        };
      }
    }

    // Write the fixed rules
    fs.writeFileSync('out/aws_rules_exhaustive_fixed.json', JSON.stringify(rulesData, null, 2));

    console.log(`✅ Fixed ${fixedCount} TBD-by-adapter pass conditions`);
    console.log(`✅ Fixed ${resourceTypeFixedCount} resource_type values`);
    console.log(`✅ Added adapter_spec to rules missing it`);
    console.log(`📁 Saved to out/aws_rules_exhaustive_fixed.json`);

  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  fixRules();
}
