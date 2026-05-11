#!/usr/bin/env python3
"""
Generate Matrix Additions From AWS Function List

- Reads aws_functions_taxonomy_mapping_2025-09-24.json
- Proposes atomic matrix rows per domain.subcat -> assertion_id using canonical adapters
- Focuses on high-priority services and expands heuristically to many core services
- Writes additions to Step3-matrices-per-cloud-provider/aws_matrix_additions_2025-09-24.json
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple

BASE_DIR = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider"
MAPPING_PATH = f"{BASE_DIR}/aws_functions_taxonomy_mapping_2025-09-24.json"
ASSERTIONS_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14_enhanced.json"
OUTPUT_PATH = f"{BASE_DIR}/aws_matrix_additions_2025-09-24.json"

HIGH_PRIORITY_SERVICES = {"ec2", "rds", "s3", "cloudwatch", "cloudfront"}

# Static adapter templates where we know precise signals
STATIC_ADAPTER_TEMPLATES: Dict[str, Dict[str, Dict[str, Any]]] = {
  "ec2": {
    "compute_host_security.vulnerability_management": {
      "resource": "ec2.instance",
      "adapter": "aws.ec2.inspector_coverage",
      "signal": {"fields": ["inspectorEnabled"], "predicate": "inspectorEnabled === true", "paths_doc": ["inspector2:ListCoverage"], "evidence_type": "config_read"}
    },
    "compute_host_security.patch_management": {
      "resource": "ec2.instance",
      "adapter": "aws.ssm.patch_compliance",
      "signal": {"fields": ["patchCompliant"], "predicate": "patchCompliant === true", "paths_doc": ["ssm:DescribeInstancePatches"], "evidence_type": "config_read"}
    },
    "compute_host_security.endpoint_protection": {
      "resource": "ec2.instance",
      "adapter": "aws.ec2.instance_protection",
      "signal": {"fields": ["terminationProtection"], "predicate": "terminationProtection === true", "paths_doc": ["ec2:DescribeInstances -> DisableApiTermination"], "evidence_type": "config_read"}
    },
    "network_perimeter.network_segmentation": {
      "resource": "ec2.security_group",
      "adapter": "aws.ec2.security_group_rules",
      "signal": {"fields": ["ingressRules"], "predicate": "ingressRules.every(r => r.cidr !== '0.0.0.0/0')", "paths_doc": ["ec2:DescribeSecurityGroups"], "evidence_type": "config_read"}
    }
  },
  "rds": {
    "crypto_data_protection.encryption_at_rest": {
      "resource": "rds.db_instance",
      "adapter": "aws.rds.instance_attributes",
      "signal": {"fields": ["storageEncrypted"], "predicate": "storageEncrypted === true", "paths_doc": ["rds:DescribeDBInstances -> StorageEncrypted"], "evidence_type": "config_read"}
    },
    "data_protection_storage.backup_recovery": {
      "resource": "rds.db_instance",
      "adapter": "aws.rds.backup",
      "signal": {"fields": ["backupRetentionPeriod"], "predicate": "backupRetentionPeriod >= (params.min_days || 7)", "paths_doc": ["rds:DescribeDBInstances -> BackupRetentionPeriod"], "evidence_type": "config_read"}
    },
    "network_perimeter.private_endpoints": {
      "resource": "rds.db_instance",
      "adapter": "aws.rds.subnet_group",
      "signal": {"fields": ["publiclyAccessible"], "predicate": "publiclyAccessible === false", "paths_doc": ["rds:DescribeDBInstances -> PubliclyAccessible"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "crypto_data_protection.encryption_at_rest": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.default_encryption",
      "signal": {"fields": ["sseAlgorithm"], "predicate": "sseAlgorithm !== undefined", "paths_doc": ["s3:GetBucketEncryption"], "evidence_type": "config_read"}
    },
    "data_protection_storage.public_exposure": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.public_access_block",
      "signal": {"fields": ["blockPublicAcls","ignorePublicAcls","blockPublicPolicy","restrictPublicBuckets"], "predicate": "blockPublicAcls===true && ignorePublicAcls===true && blockPublicPolicy===true && restrictPublicBuckets===true", "paths_doc": ["s3:GetPublicAccessBlock -> PublicAccessBlockConfiguration"], "evidence_type": "config_read"}
    },
    "logging_monitoring.log_collection": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.server_access_logging",
      "signal": {"fields": ["loggingEnabled"], "predicate": "loggingEnabled === true", "paths_doc": ["s3:GetBucketLogging"], "evidence_type": "config_read"}
    }
  },
  "cloudwatch": {
    "logging_monitoring.monitoring_alerting": {
      "resource": "cloudwatch.alarm",
      "adapter": "aws.cloudwatch.alarm_critical_configured",
      "signal": {"fields": ["alarmConfigured"], "predicate": "alarmConfigured === true", "paths_doc": ["cloudwatch:DescribeAlarms"], "evidence_type": "config_read"}
    },
    "logging_monitoring.log_collection": {
      "resource": "cloudwatch.log_group",
      "adapter": "aws.cloudwatch.log_group_retention",
      "signal": {"fields": ["retentionInDays"], "predicate": "retentionInDays >= (params.min_days || 90)", "paths_doc": ["logs:DescribeLogGroups -> retentionInDays"], "evidence_type": "config_read"}
    }
  },
  "cloudfront": {
    "crypto_data_protection.encryption_in_transit": {
      "resource": "cloudfront.distribution",
      "adapter": "aws.cloudfront.https_enforced",
      "signal": {"fields": ["viewerProtocolPolicy"], "predicate": "viewerProtocolPolicy === 'redirect-to-https' || viewerProtocolPolicy === 'https-only'", "paths_doc": ["cloudfront:GetDistribution -> DefaultCacheBehavior.ViewerProtocolPolicy"], "evidence_type": "config_read"}
    },
    "monitoring_security.threat_detection": {
      "resource": "cloudfront.distribution",
      "adapter": "aws.cloudfront.waf_attached",
      "signal": {"fields": ["wafAclAttached"], "predicate": "wafAclAttached === true", "paths_doc": ["wafv2:ListWebACLs", "cloudfront:GetDistribution"], "evidence_type": "config_read"}
    }
  },
  "accessanalyzer": {
    "monitoring_security.threat_detection": {
      "resource": "accessanalyzer.analyzer",
      "adapter": "aws.accessanalyzer.enabled",
      "signal": {"fields": ["analyzerEnabled"], "predicate": "analyzerEnabled === true", "paths_doc": ["access-analyzer:ListAnalyzers"], "evidence_type": "config_read"}
    }
  },
  "autoscaling": {
    "resilience_recovery.high_availability": {
      "resource": "autoscaling.group",
      "adapter": "aws.autoscaling.multi_az",
      "signal": {"fields": ["availabilityZones"], "predicate": "Array.isArray(availabilityZones) && availabilityZones.length >= 2", "paths_doc": ["autoscaling:DescribeAutoScalingGroups -> AvailabilityZones"], "evidence_type": "config_read"}
    }
  },
  "cloudformation": {
    "governance_compliance.resource_governance": {
      "resource": "cloudformation.stack",
      "adapter": "aws.cloudformation.termination_protection",
      "signal": {"fields": ["terminationProtectionEnabled"], "predicate": "terminationProtectionEnabled === true", "paths_doc": ["cloudformation:DescribeStacks -> EnableTerminationProtection"], "evidence_type": "config_read"}
    },
    "logging_monitoring.monitoring_alerting": {
      "resource": "cloudformation.stack",
      "adapter": "aws.cloudformation.drift_detection_monitoring",
      "signal": {"fields": ["driftDetectionConfigured"], "predicate": "driftDetectionConfigured === true", "paths_doc": ["cloudformation:DetectStackDrift", "cloudformation:DescribeStackDriftDetectionStatus"], "evidence_type": "config_read"}
    }
  },
  "athena": {
    "crypto_data_protection.encryption_at_rest": {
      "resource": "athena.workgroup",
      "adapter": "aws.athena.workgroup_encryption",
      "signal": {"fields": ["encryptionEnabled"], "predicate": "encryptionEnabled === true", "paths_doc": ["athena:GetWorkGroup -> Configuration.ResultConfiguration.EncryptionConfiguration"], "evidence_type": "config_read"}
    }
  },
  "appstream": {
    "network_perimeter.network_segmentation": {
      "resource": "appstream.fleet",
      "adapter": "aws.appstream.fleet_internet_access",
      "signal": {"fields": ["defaultInternetAccessDisabled"], "predicate": "defaultInternetAccessDisabled === true", "paths_doc": ["appstream:DescribeFleets -> FleetAttributes"], "evidence_type": "config_read"}
    }
  },
  "efs": {
    "crypto_data_protection.encryption_at_rest": {
      "resource": "efs.file_system",
      "adapter": "aws.efs.encryption",
      "signal": {"fields": ["encrypted"], "predicate": "encrypted === true", "paths_doc": ["efs:DescribeFileSystems -> Encrypted"], "evidence_type": "config_read"}
    },
    "data_protection_storage.backup_recovery": {
      "resource": "efs.file_system",
      "adapter": "aws.efs.backup",
      "signal": {"fields": ["backupPolicy"], "predicate": "backupPolicy === 'ENABLED'", "paths_doc": ["efs:DescribeBackupPolicy -> BackupPolicy"], "evidence_type": "config_read"}
    }
  },
  "dynamodb": {
    "crypto_data_protection.encryption_at_rest": {
      "resource": "dynamodb.table",
      "adapter": "aws.dynamodb.encryption",
      "signal": {"fields": ["sseEnabled"], "predicate": "sseEnabled === true", "paths_doc": ["dynamodb:DescribeTable -> SSEDescription"], "evidence_type": "config_read"}
    },
    "data_protection_storage.backup_recovery": {
      "resource": "dynamodb.table",
      "adapter": "aws.dynamodb.pitr",
      "signal": {"fields": ["pointInTimeRecoveryEnabled"], "predicate": "pointInTimeRecoveryEnabled === true", "paths_doc": ["dynamodb:DescribeContinuousBackups -> PointInTimeRecoveryDescription"], "evidence_type": "config_read"}
    },
    "data_protection_storage.public_exposure": {
      "resource": "dynamodb.table",
      "adapter": "aws.dynamodb.resource_policy_public_access",
      "signal": {"fields": ["publicAccess"], "predicate": "publicAccess === false", "paths_doc": ["dynamodb:DescribeTable -> TableClass/Policy"], "evidence_type": "config_read"}
    }
  },
  "opensearch": {
    "crypto_data_protection.encryption_in_transit": {
      "resource": "opensearch.domain",
      "adapter": "aws.opensearch.https_enforced",
      "signal": {"fields": ["enforceHTTPS"], "predicate": "enforceHTTPS === true", "paths_doc": ["opensearch:DescribeDomain -> DomainStatus -> DomainEndpointOptions.EnforceHTTPS"], "evidence_type": "config_read"}
    },
    "crypto_data_protection.encryption_at_rest": {
      "resource": "opensearch.domain",
      "adapter": "aws.opensearch.encryption",
      "signal": {"fields": ["encryptionEnabled"], "predicate": "encryptionEnabled === true", "paths_doc": ["opensearch:DescribeDomain -> DomainStatus -> EncryptionAtRestOptions"], "evidence_type": "config_read"}
    },
    "data_protection_storage.public_exposure": {
      "resource": "opensearch.domain",
      "adapter": "aws.opensearch.public_access",
      "signal": {"fields": ["publicAccess"], "predicate": "publicAccess === false", "paths_doc": ["opensearch:DescribeDomain -> DomainStatus -> VPCOptions"], "evidence_type": "config_read"}
    }
  },
  "elasticache": {
    "crypto_data_protection.encryption_in_transit": {
      "resource": "elasticache.redis_replication_group",
      "adapter": "aws.elasticache.in_transit_encryption",
      "signal": {"fields": ["transitEncryptionEnabled"], "predicate": "transitEncryptionEnabled === true", "paths_doc": ["elasticache:DescribeReplicationGroups -> TransitEncryptionEnabled"], "evidence_type": "config_read"}
    },
    "crypto_data_protection.encryption_at_rest": {
      "resource": "elasticache.redis_replication_group",
      "adapter": "aws.elasticache.at_rest_encryption",
      "signal": {"fields": ["atRestEncryptionEnabled"], "predicate": "atRestEncryptionEnabled === true", "paths_doc": ["elasticache:DescribeReplicationGroups -> AtRestEncryptionEnabled"], "evidence_type": "config_read"}
    }
  },
  "kms": {
    "secrets_key_mgmt.key_rotation": {
      "resource": "kms.key",
      "adapter": "aws.kms.key_rotation",
      "signal": {"fields": ["keyRotationEnabled"], "predicate": "keyRotationEnabled === true", "paths_doc": ["kms:GetKeyRotationStatus"], "evidence_type": "config_read"}
    }
  },
  "secretsmanager": {
    "secrets_key_mgmt.key_rotation": {
      "resource": "secretsmanager.secret",
      "adapter": "aws.secretsmanager.rotation",
      "signal": {"fields": ["rotationEnabled"], "predicate": "rotationEnabled === true", "paths_doc": ["secretsmanager:DescribeSecret -> RotationEnabled"], "evidence_type": "config_read"}
    },
    "secrets_key_mgmt.secret_sprawl": {
      "resource": "secretsmanager.secret",
      "adapter": "aws.secretsmanager.secret_last_accessed",
      "signal": {"fields": ["lastAccessedDays"], "predicate": "lastAccessedDays <= (params.max_days || 90)", "paths_doc": ["secretsmanager:ListSecrets -> LastAccessedDate"], "evidence_type": "config_read"}
    }
  },
  "route53": {
    "network_perimeter.dns_security": {
      "resource": "route53.hosted_zone",
      "adapter": "aws.route53.dnssec",
      "signal": {"fields": ["dnssecEnabled"], "predicate": "dnssecEnabled === true", "paths_doc": ["route53:GetDNSSEC"], "evidence_type": "config_read"}
    }
  },
  "waf": {
    "logging_monitoring.log_collection": {
      "resource": "waf.web_acl",
      "adapter": "aws.waf.web_acl_logging",
      "signal": {"fields": ["loggingEnabled"], "predicate": "loggingEnabled === true", "paths_doc": ["wafv2:GetLoggingConfiguration"], "evidence_type": "config_read"}
    }
  },
  "shield": {
    "monitoring_security.threat_detection": {
      "resource": "shield.protection",
      "adapter": "aws.shield.advanced_enabled",
      "signal": {"fields": ["advancedProtection"], "predicate": "advancedProtection === true", "paths_doc": ["shield:DescribeSubscription", "shield:ListProtections"], "evidence_type": "config_read"}
    }
  },
  "macie": {
    "monitoring_security.threat_detection": {
      "resource": "macie.account",
      "adapter": "aws.macie.enabled",
      "signal": {"fields": ["enabled"], "predicate": "enabled === true", "paths_doc": ["macie2:GetMacieSession -> status"], "evidence_type": "config_read"}
    }
  },
  "inspector": {
    "monitoring_security.threat_detection": {
      "resource": "inspector2.account",
      "adapter": "aws.inspector2.enabled",
      "signal": {"fields": ["enabled"], "predicate": "enabled === true", "paths_doc": ["inspector2:BatchGetAccountStatus"], "evidence_type": "config_read"}
    }
  },
  "inspector2": {
    "compute_host_security.vulnerability_management": {
      "resource": "inspector2.account",
      "adapter": "aws.inspector2.coverage_status",
      "signal": {"fields": ["ec2Coverage","ecrCoverage","lambdaCoverage"], "predicate": "ec2Coverage === 'ENABLED' && ecrCoverage === 'ENABLED' && lambdaCoverage === 'ENABLED'", "paths_doc": ["inspector2:BatchGetAccountStatus", "inspector2:ListCoverage"], "evidence_type": "config_read"}
    }
  },
  "config": {
    "governance_compliance.compliance_framework": {
      "resource": "config.account",
      "adapter": "aws.config.recorder_and_channel_active",
      "signal": {"fields": ["recorderEnabled","deliveryChannelExists"], "predicate": "recorderEnabled === true && deliveryChannelExists === true", "paths_doc": ["config:DescribeConfigurationRecorders", "config:DescribeDeliveryChannels"], "evidence_type": "config_read"}
    },
    "logging_monitoring.log_retention": {
      "resource": "config.account",
      "adapter": "aws.config.rules_evaluation_active",
      "signal": {"fields": ["activeRules"], "predicate": "activeRules >= (params.min_rules || 1)", "paths_doc": ["config:DescribeConfigRules", "config:DescribeComplianceByConfigRule"], "evidence_type": "config_read"}
    }
  },
  "fms": {
    "governance_compliance.policy_management": {
      "resource": "fms.account",
      "adapter": "aws.fms.policies_active",
      "signal": {"fields": ["policyCount"], "predicate": "policyCount >= (params.min_policies || 1)", "paths_doc": ["fms:ListPolicies"], "evidence_type": "config_read"}
    }
  },
  "wellarchitected": {
    "platform_surfaces_versions.platform_monitoring": {
      "resource": "wellarchitected.workload",
      "adapter": "aws.wellarchitected.workload_reviews",
      "signal": {"fields": ["hasHighOrMediumRisks"], "predicate": "hasHighOrMediumRisks === false", "paths_doc": ["wellarchitected:ListWorkloads", "wellarchitected:ListLenses", "wellarchitected:GetWorkload"], "evidence_type": "config_read"}
    }
  },
  "codeartifact": {
    "supply_chain_registries.registry_security": {
      "resource": "codeartifact.domain",
      "adapter": "aws.codeartifact.external_publishing_disabled",
      "signal": {"fields": ["allowsPublicRepositories"], "predicate": "allowsPublicRepositories !== true", "paths_doc": ["codeartifact:ListDomains", "codeartifact:DescribeDomain"], "evidence_type": "config_read"}
    }
  },
  "drs": {
    "resilience_recovery.disaster_recovery": {
      "resource": "drs.source_server",
      "adapter": "aws.drs.replication_configured",
      "signal": {"fields": ["replicationEnabled"], "predicate": "replicationEnabled === true", "paths_doc": ["drs:DescribeSourceServers -> dataReplicationInfo"], "evidence_type": "config_read"}
    }
  },
  "trustedadvisor": {
    "governance_compliance.risk_management": {
      "resource": "trustedadvisor.account",
      "adapter": "aws.trustedadvisor.premium_and_clean",
      "signal": {"fields": ["premiumSupportActive","openHighFindings"], "predicate": "premiumSupportActive === true && openHighFindings === 0", "paths_doc": ["support:DescribeTrustedAdvisorChecks", "support:DescribeTrustedAdvisorCheckSummaries"], "evidence_type": "config_read"}
    }
  },
  "platform_surfaces": {
    "platform_surfaces_versions.version_management": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.runtime_supported",
      "signal": {"fields": ["runtimeSupported"], "predicate": "runtimeSupported === true", "paths_doc": ["lambda:GetFunctionConfiguration -> Runtime"], "evidence_type": "config_read"}
    }
  },
  "account": {
    "governance_compliance.resource_governance": {
      "resource": "account.contact",
      "adapter": "aws.account.security_contact_registered",
      "signal": {"fields": ["securityContactRegistered"], "predicate": "securityContactRegistered === true", "paths_doc": ["account:GetContactInformation"], "evidence_type": "config_read"}
    }
  },
  "dlm": {
    "resilience_recovery.backup_management": {
      "resource": "dlm.lifecycle_policy",
      "adapter": "aws.dlm.ebs_snapshot_policy_exists",
      "signal": {"fields": ["policyExists"], "predicate": "policyExists === true", "paths_doc": ["dlm:GetLifecyclePolicies"], "evidence_type": "config_read"}
    }
  },
  "emr": {
    "compute_host_security.endpoint_protection": {
      "resource": "emr.cluster",
      "adapter": "aws.emr.master_nodes_no_public_ip",
      "signal": {"fields": ["masterNodesPublicIp"], "predicate": "masterNodesPublicIp === false", "paths_doc": ["emr:DescribeCluster -> MasterPublicDnsName"], "evidence_type": "config_read"}
    }
  },
  "glacier": {
    "data_protection_storage.public_exposure": {
      "resource": "glacier.vault",
      "adapter": "aws.glacier.vault_policy_public_access",
      "signal": {"fields": ["publicAccess"], "predicate": "publicAccess === false", "paths_doc": ["glacier:GetVaultAccessPolicy"], "evidence_type": "config_read"}
    }
  },
  "lightsail": {
    "data_protection_storage.public_exposure": {
      "resource": "lightsail.instance",
      "adapter": "aws.lightsail.instance_public_access",
      "signal": {"fields": ["publicIp"], "predicate": "publicIp === false", "paths_doc": ["lightsail:GetInstances -> publicIpAddress"], "evidence_type": "config_read"}
    }
  },
  "ssmincidents": {
    "monitoring_security.incident_response": {
      "resource": "ssmincidents.response_plan",
      "adapter": "aws.ssmincidents.enabled_with_plans",
      "signal": {"fields": ["enabled","plansExist"], "predicate": "enabled === true && plansExist === true", "paths_doc": ["ssm-incidents:ListResponsePlans"], "evidence_type": "config_read"}
    }
  },
  "stepfunctions": {
    "logging_monitoring.log_collection": {
      "resource": "stepfunctions.state_machine",
      "adapter": "aws.stepfunctions.logging_enabled",
      "signal": {"fields": ["loggingEnabled"], "predicate": "loggingEnabled === true", "paths_doc": ["states:DescribeStateMachine -> loggingConfiguration"], "evidence_type": "config_read"}
    }
  },
  "eventbridge": {
    "serverless_paas.event_security": {
      "resource": "eventbridge.event_bus",
      "adapter": "aws.eventbridge.bus_access_controls",
      "signal": {"fields": ["crossAccountAccess","exposed"], "predicate": "crossAccountAccess !== true && exposed !== true", "paths_doc": ["events:DescribeEventBus", "events:ListTargetsByRule"], "evidence_type": "config_read"}
    }
  },
  "ssm": {
    "compute_host_security.patch_management": {
      "resource": "ssm.managed_instance",
      "adapter": "aws.ssm.patch_state",
      "signal": {"fields": ["patchCompliant"], "predicate": "patchCompliant === true", "paths_doc": ["ssm:DescribeInstancePatches", "ssm:DescribeInstanceInformation"], "evidence_type": "config_read"}
    }
  },
  "detective": {
    "monitoring_security.threat_detection": {
      "resource": "detective.graph",
      "adapter": "aws.detective.enabled",
      "signal": {"fields": ["enabled"], "predicate": "enabled === true", "paths_doc": ["detective:ListGraphs", "detective:GetMembers"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "logging_monitoring.log_collection": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.project_logging",
      "signal": {"fields": ["cloudwatchLogsEnabled","s3LogsEncrypted"], "predicate": "cloudwatchLogsEnabled === true && s3LogsEncrypted === true", "paths_doc": ["codebuild:BatchGetProjects -> logsConfig"], "evidence_type": "config_read"}
    }
  },
  "kinesis": {
    "crypto_data_protection.encryption_at_rest": {
      "resource": "kinesis.stream",
      "adapter": "aws.kinesis.encryption",
      "signal": {"fields": ["encryptionEnabled"], "predicate": "encryptionEnabled === true", "paths_doc": ["kinesis:DescribeStreamSummary -> StreamDescriptionSummary.EncryptionType"], "evidence_type": "config_read"}
    },
    "data_protection_storage.data_retention": {
      "resource": "kinesis.stream",
      "adapter": "aws.kinesis.retention_policy",
      "signal": {"fields": ["retentionHours"], "predicate": "retentionHours >= (params.min_hours || 24)", "paths_doc": ["kinesis:DescribeStreamSummary -> RetentionPeriodHours"], "evidence_type": "config_read"}
    }
  },
  "kafka": {
    "crypto_data_protection.encryption_in_transit": {
      "resource": "kafka.cluster",
      "adapter": "aws.kafka.tls_in_transit",
      "signal": {"fields": ["clientBroker"], "predicate": "clientBroker === 'TLS' || clientBroker === 'TLS_PLAINTEXT'", "paths_doc": ["kafka:DescribeCluster -> EncryptionInfo"], "evidence_type": "config_read"}
    },
    "data_protection_storage.public_exposure": {
      "resource": "kafka.cluster",
      "adapter": "aws.kafka.public_access",
      "signal": {"fields": ["publicAccess"], "predicate": "publicAccess === false", "paths_doc": ["kafka:DescribeCluster -> BrokerNodeGroupInfo -> ConnectivityInfo -> PublicAccess"], "evidence_type": "config_read"}
    }
  },
  "redshift": {
    "crypto_data_protection.encryption_in_transit": {
      "resource": "redshift.cluster",
      "adapter": "aws.redshift.in_transit_encryption",
      "signal": {"fields": ["requireTLS"], "predicate": "requireTLS === true", "paths_doc": ["redshift:DescribeClusters -> ClusterParameterGroups/Parameters (require_SSL)"], "evidence_type": "config_read"}
    },
    "logging_monitoring.log_collection": {
      "resource": "redshift.cluster",
      "adapter": "aws.redshift.audit_logging",
      "signal": {"fields": ["auditLoggingEnabled"], "predicate": "auditLoggingEnabled === true", "paths_doc": ["redshift:DescribeLoggingStatus"], "evidence_type": "config_read"}
    },
    "network_perimeter.network_segmentation": {
      "resource": "redshift.cluster",
      "adapter": "aws.redshift.enhanced_vpc_routing",
      "signal": {"fields": ["enhancedVpcRouting"], "predicate": "enhancedVpcRouting === true", "paths_doc": ["redshift:DescribeClusters -> EnhancedVpcRouting"], "evidence_type": "config_read"}
    }
  },
  "fsx": {
    "crypto_data_protection.encryption_at_rest": {
      "resource": "fsx.file_system",
      "adapter": "aws.fsx.encryption",
      "signal": {"fields": ["encrypted"], "predicate": "encrypted === true", "paths_doc": ["fsx:DescribeFileSystems -> Encrypted"], "evidence_type": "config_read"}
    },
    "data_protection_storage.backup_recovery": {
      "resource": "fsx.file_system",
      "adapter": "aws.fsx.backup_policy",
      "signal": {"fields": ["backupPolicy"], "predicate": "backupPolicy === 'ENABLED'", "paths_doc": ["fsx:DescribeBackups", "fsx:DescribeFileSystems -> BackupPolicy"], "evidence_type": "config_read"}
    }
  },
  "elasticbeanstalk": {
    "platform_surfaces_versions.security_updates": {
      "resource": "elasticbeanstalk.environment",
      "adapter": "aws.elasticbeanstalk.managed_updates",
      "signal": {"fields": ["managedActionsEnabled"], "predicate": "managedActionsEnabled === true", "paths_doc": ["elasticbeanstalk:DescribeConfigurationSettings -> ManagedActionsEnabled"], "evidence_type": "config_read"}
    }
  },
  "datasync": {
    "logging_monitoring.log_collection": {
      "resource": "datasync.task",
      "adapter": "aws.datasync.task_logging",
      "signal": {"fields": ["cloudWatchLogGroupArn"], "predicate": "cloudWatchLogGroupArn !== undefined", "paths_doc": ["datasync:DescribeTask -> CloudWatchLogGroupArn"], "evidence_type": "config_read"}
    }
  },
  "directconnect": {
    "resilience_recovery.high_availability": {
      "resource": "directconnect.connection",
      "adapter": "aws.directconnect.connection_redundancy",
      "signal": {"fields": ["hasRedundantConnection"], "predicate": "hasRedundantConnection === true", "paths_doc": ["directconnect:DescribeConnections"], "evidence_type": "config_read"}
    },
    "network_perimeter.network_segmentation": {
      "resource": "directconnect.virtual_interface",
      "adapter": "aws.directconnect.vif_redundancy",
      "signal": {"fields": ["hasRedundantVif"], "predicate": "hasRedundantVif === true", "paths_doc": ["directconnect:DescribeVirtualInterfaces"], "evidence_type": "config_read"}
    }
  },
  "appsync": {
    "logging_monitoring.log_collection": {
      "resource": "appsync.graphql_api",
      "adapter": "aws.appsync.field_level_logging",
      "signal": {"fields": ["fieldLogLevel"], "predicate": "fieldLogLevel !== 'NONE'", "paths_doc": ["appsync:GetGraphqlApi -> logConfig.fieldLogLevel"], "evidence_type": "config_read"}
    },
    "serverless_paas.api_security": {
      "resource": "appsync.graphql_api",
      "adapter": "aws.appsync.authz_modes",
      "signal": {"fields": ["authModes"], "predicate": "Array.isArray(authModes) && authModes.length >= 1", "paths_doc": ["appsync:GetGraphqlApi -> authenticationType, additionalAuthenticationProviders"], "evidence_type": "config_read"}
    }
  },
  "mq": {
    "logging_monitoring.log_collection": {
      "resource": "mq.broker",
      "adapter": "aws.mq.broker_logging",
      "signal": {"fields": ["cloudWatchLogsEnabled"], "predicate": "cloudWatchLogsEnabled === true", "paths_doc": ["mq:DescribeBroker -> Logs"], "evidence_type": "config_read"}
    }
  },
  "resourceexplorer2": {
    "governance_compliance.resource_governance": {
      "resource": "resourceexplorer2.index",
      "adapter": "aws.resourceexplorer2.index_exists",
      "signal": {"fields": ["indexesFound"], "predicate": "indexesFound === true", "paths_doc": ["resource-explorer-2:ListIndexes"], "evidence_type": "config_read"}
    }
  },
  "servicecatalog": {
    "governance_compliance.resource_governance": {
      "resource": "servicecatalog.portfolio",
      "adapter": "aws.servicecatalog.portfolio_sharing_org_only",
      "signal": {"fields": ["sharedOutsideOrg"], "predicate": "sharedOutsideOrg !== true", "paths_doc": ["servicecatalog:ListPortfolioAccess"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "containers_kubernetes.image_security": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.image_scanning_on_push",
      "signal": {"fields": ["scanOnPush"], "predicate": "scanOnPush === true", "paths_doc": ["ecr:DescribeRegistry", "ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    }
  },
  "ecs": {
    "containers_kubernetes.runtime_security": {
      "resource": "ecs.service",
      "adapter": "aws.ecs.task_definition_security",
      "signal": {"fields": ["noPrivileged","readOnlyRootFs"], "predicate": "noPrivileged === true && readOnlyRootFs === true", "paths_doc": ["ecs:DescribeTaskDefinition -> containerDefinitions"], "evidence_type": "config_read"}
    }
  },
  "eks": {
    "containers_kubernetes.network_policies": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.cluster_logging_network_policy",
      "signal": {"fields": ["networkPolicyEnabled"], "predicate": "networkPolicyEnabled === true", "paths_doc": ["eks:DescribeCluster -> cluster.logging / CNI policy"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "serverless_paas.function_security": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.vpc_and_private_access",
      "signal": {"fields": ["vpcConfigured","publicUrl"], "predicate": "vpcConfigured === true && publicUrl !== true", "paths_doc": ["lambda:GetFunctionConfiguration -> VpcConfig, FunctionUrlConfig"], "evidence_type": "config_read"}
    }
  },
  "apigateway": {
    "serverless_paas.api_security": {
      "resource": "apigateway.rest_api",
      "adapter": "aws.apigateway.authz_and_logs",
      "signal": {"fields": ["authorizerConfigured","accessLoggingEnabled"], "predicate": "authorizerConfigured === true && accessLoggingEnabled === true", "paths_doc": ["apigateway:GET /restapis -> authorizers", "apigateway:GET /stages -> accessLogSettings"], "evidence_type": "config_read"}
    }
  },
  "networkfirewall": {
    "network_perimeter.firewall_rules": {
      "resource": "networkfirewall.firewall",
      "adapter": "aws.networkfirewall.logging_and_rule_association",
      "signal": {"fields": ["loggingEnabled","ruleGroupAssociated"], "predicate": "loggingEnabled === true && ruleGroupAssociated === true", "paths_doc": ["network-firewall:ListFirewalls", "DescribeFirewall", "DescribeLoggingConfiguration"], "evidence_type": "config_read"}
    }
  },
  "guardduty": {
    "monitoring_security.threat_detection": {
      "resource": "guardduty.detector",
      "adapter": "aws.guardduty.enabled_all_regions",
      "signal": {"fields": ["enabledAllRegions"], "predicate": "enabledAllRegions === true", "paths_doc": ["guardduty:ListDetectors", "guardduty:GetDetector -> dataSources"], "evidence_type": "config_read"}
    }
  },
  "organizations": {
    "governance_compliance.policy_management": {
      "resource": "organizations.account",
      "adapter": "aws.organizations.scp_deny_regions",
      "signal": {"fields": ["scpDenyRegionsConfigured"], "predicate": "scpDenyRegionsConfigured === true", "paths_doc": ["organizations:ListPolicies", "ListTargetsForPolicy", "DescribePolicy"], "evidence_type": "config_read"}
    }
  }
}

# Expanded service checks for additional coverage
EXPANDED_SERVICE_CHECKS: Dict[str, Dict[str, Dict[str, Any]]] = {
  "ec2": {
    "compute_host_security.agent_coverage": {
      "resource": "ec2.instance",
      "adapter": "aws.ssm.managed_instance_coverage",
      "signal": {"fields": ["ssmAgentInstalled"], "predicate": "ssmAgentInstalled === true", "paths_doc": ["ssm:DescribeInstanceInformation"], "evidence_type": "config_read"}
    },
    "compute_host_security.compliance_monitoring": {
      "resource": "ec2.instance",
      "adapter": "aws.ssm.patch_compliance_status",
      "signal": {"fields": ["patchComplianceStatus"], "predicate": "patchComplianceStatus === 'COMPLIANT'", "paths_doc": ["ssm:DescribeInstancePatches"], "evidence_type": "config_read"}
    }
  },
  "rds": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "rds.db_instance",
      "adapter": "aws.rds.automated_backup_retention",
      "signal": {"fields": ["backupRetentionPeriod"], "predicate": "backupRetentionPeriod >= (params.min_days || 7)", "paths_doc": ["rds:DescribeDBInstances -> BackupRetentionPeriod"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.lifecycle_policy",
      "signal": {"fields": ["lifecycleRules"], "predicate": "Array.isArray(lifecycleRules) && lifecycleRules.length >= 1", "paths_doc": ["s3:GetBucketLifecycleConfiguration"], "evidence_type": "config_read"}
    }
  },
  "cloudwatch": {
    "logging_monitoring.log_retention": {
      "resource": "cloudwatch.log_group",
      "adapter": "aws.cloudwatch.log_retention_policy",
      "signal": {"fields": ["retentionInDays"], "predicate": "retentionInDays >= (params.min_days || 90)", "paths_doc": ["logs:DescribeLogGroups -> retentionInDays"], "evidence_type": "config_read"}
    }
  },
  "ecs": {
    "containers_kubernetes.secret_management": {
      "resource": "ecs.task_definition",
      "adapter": "aws.ecs.secrets_from_ssm",
      "signal": {"fields": ["secretsFromSSM"], "predicate": "secretsFromSSM === true", "paths_doc": ["ecs:DescribeTaskDefinition -> secrets"], "evidence_type": "config_read"}
    }
  },
  "eks": {
    "containers_kubernetes.admission_control": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.admission_controllers",
      "signal": {"fields": ["admissionControllersEnabled"], "predicate": "admissionControllersEnabled === true", "paths_doc": ["eks:DescribeCluster -> kubernetesNetworkConfig"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.rbac_policies": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.rbac_enabled",
      "signal": {"fields": ["rbacEnabled"], "predicate": "rbacEnabled === true", "paths_doc": ["eks:DescribeCluster -> status"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "supply_chain_registries.build_security": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.build_security",
      "signal": {"fields": ["privilegedModeDisabled"], "predicate": "privilegedModeDisabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment.privilegedMode"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "supply_chain_registries.vulnerability_scanning": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.vulnerability_scanning",
      "signal": {"fields": ["scanOnPush"], "predicate": "scanOnPush === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "platform_surfaces_versions.version_management": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.runtime_version",
      "signal": {"fields": ["runtimeVersion"], "predicate": "runtimeVersion >= (params.min_version || 'nodejs18.x')", "paths_doc": ["lambda:GetFunctionConfiguration -> Runtime"], "evidence_type": "config_read"}
    }
  },
  # Additional missing domain+subcat combinations
  "ec2": {
    "compute_host_security.image_security": {
      "resource": "ec2.ami",
      "adapter": "aws.ec2.ami_encryption",
      "signal": {"fields": ["encrypted"], "predicate": "encrypted === true", "paths_doc": ["ec2:DescribeImages -> BlockDeviceMappings"], "evidence_type": "config_read"}
    },
    "compute_host_security.network_security": {
      "resource": "ec2.instance",
      "adapter": "aws.ec2.network_interface_security",
      "signal": {"fields": ["publicIpAssigned"], "predicate": "publicIpAssigned === false", "paths_doc": ["ec2:DescribeInstances -> PublicIpAddress"], "evidence_type": "config_read"}
    },
    "compute_host_security.os_hardening": {
      "resource": "ec2.instance",
      "adapter": "aws.ssm.os_hardening_compliance",
      "signal": {"fields": ["hardeningCompliant"], "predicate": "hardeningCompliant === true", "paths_doc": ["ssm:GetComplianceSummary"], "evidence_type": "config_read"}
    },
    "compute_host_security.storage_lifecycle": {
      "resource": "ec2.volume",
      "adapter": "aws.ec2.volume_lifecycle",
      "signal": {"fields": ["lifecyclePolicy"], "predicate": "lifecyclePolicy !== null", "paths_doc": ["ec2:DescribeVolumes -> Tags"], "evidence_type": "config_read"}
    }
  },
  "eks": {
    "containers_kubernetes.monitoring": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.cloudwatch_logging",
      "signal": {"fields": ["loggingEnabled"], "predicate": "loggingEnabled === true", "paths_doc": ["eks:DescribeCluster -> logging"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.platform_management": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.version_management",
      "signal": {"fields": ["kubernetesVersion"], "predicate": "kubernetesVersion >= (params.min_version || '1.24')", "paths_doc": ["eks:DescribeCluster -> version"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.psa_enforcement": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.pod_security_standards",
      "signal": {"fields": ["podSecurityStandards"], "predicate": "podSecurityStandards === 'enforced'", "paths_doc": ["eks:DescribeCluster -> kubernetesNetworkConfig"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.workload_security": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.workload_identity",
      "signal": {"fields": ["workloadIdentityEnabled"], "predicate": "workloadIdentityEnabled === true", "paths_doc": ["eks:DescribeCluster -> identity"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "supply_chain_registries.dependency_management": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.dependency_scanning",
      "signal": {"fields": ["dependencyScanningEnabled"], "predicate": "dependencyScanningEnabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "supply_chain_registries.sbom_provenance": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.sbom_generation",
      "signal": {"fields": ["sbomGenerated"], "predicate": "sbomGenerated === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    },
    "supply_chain_registries.signing_verification": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.image_signing",
      "signal": {"fields": ["imageSigningEnabled"], "predicate": "imageSigningEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> encryptionConfiguration"], "evidence_type": "config_read"}
    }
  },
  "apigateway": {
    "platform_surfaces_versions.api_management": {
      "resource": "apigateway.rest_api",
      "adapter": "aws.apigateway.api_versioning",
      "signal": {"fields": ["versioningEnabled"], "predicate": "versioningEnabled === true", "paths_doc": ["apigateway:GetRestApi -> version"], "evidence_type": "config_read"}
    },
    "platform_surfaces_versions.deprecation_mgmt": {
      "resource": "apigateway.rest_api",
      "adapter": "aws.apigateway.deprecation_tracking",
      "signal": {"fields": ["deprecationNotices"], "predicate": "deprecationNotices.length === 0", "paths_doc": ["apigateway:GetRestApi -> warnings"], "evidence_type": "config_read"}
    },
    "platform_surfaces_versions.deprecation_tracking": {
      "resource": "apigateway.rest_api",
      "adapter": "aws.apigateway.deprecation_monitoring",
      "signal": {"fields": ["deprecationMonitoring"], "predicate": "deprecationMonitoring === true", "paths_doc": ["apigateway:GetRestApi -> policy"], "evidence_type": "config_read"}
    }
  },
  "backup": {
    "resilience_recovery.backup_strategy": {
      "resource": "backup.backup_plan",
      "adapter": "aws.backup.strategy_compliance",
      "signal": {"fields": ["strategyCompliant"], "predicate": "strategyCompliant === true", "paths_doc": ["backup:GetBackupPlan"], "evidence_type": "config_read"}
    },
    "resilience_recovery.ransomware_protection": {
      "resource": "backup.backup_vault",
      "adapter": "aws.backup.ransomware_protection",
      "signal": {"fields": ["ransomwareProtection"], "predicate": "ransomwareProtection === true", "paths_doc": ["backup:GetBackupVault"], "evidence_type": "config_read"}
    },
    "resilience_recovery.recovery_testing": {
      "resource": "backup.recovery_point",
      "adapter": "aws.backup.recovery_testing",
      "signal": {"fields": ["recoveryTested"], "predicate": "recoveryTested === true", "paths_doc": ["backup:ListRecoveryPointsByBackupVault"], "evidence_type": "config_read"}
    }
  },
  "macie": {
    "data_protection.data_classification": {
      "resource": "macie.classification_job",
      "adapter": "aws.macie.data_classification",
      "signal": {"fields": ["classificationEnabled"], "predicate": "classificationEnabled === true", "paths_doc": ["macie2:ListClassificationJobs"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.intelligent_tiering",
      "signal": {"fields": ["intelligentTieringEnabled"], "predicate": "intelligentTieringEnabled === true", "paths_doc": ["s3:GetBucketIntelligentTieringConfiguration"], "evidence_type": "config_read"}
    }
  },
  "cloudformation": {
    "governance_compliance.exceptions_registry": {
      "resource": "cloudformation.stack",
      "adapter": "aws.cloudformation.exceptions_tracking",
      "signal": {"fields": ["exceptionsTracked"], "predicate": "exceptionsTracked === true", "paths_doc": ["cloudformation:DescribeStacks -> Tags"], "evidence_type": "config_read"}
    },
    "governance_compliance.infrastructure_as_code": {
      "resource": "cloudformation.stack",
      "adapter": "aws.cloudformation.iac_validation",
      "signal": {"fields": ["iacValidated"], "predicate": "iacValidated === true", "paths_doc": ["cloudformation:ValidateTemplate"], "evidence_type": "config_read"}
    },
    "governance_compliance.naming_conventions": {
      "resource": "cloudformation.stack",
      "adapter": "aws.cloudformation.naming_compliance",
      "signal": {"fields": ["namingCompliant"], "predicate": "namingCompliant === true", "paths_doc": ["cloudformation:DescribeStacks -> StackName"], "evidence_type": "config_read"}
    }
  },
  "cloudwatch": {
    "logging_monitoring.log_analysis": {
      "resource": "cloudwatch.log_group",
      "adapter": "aws.cloudwatch.log_analysis",
      "signal": {"fields": ["logAnalysisEnabled"], "predicate": "logAnalysisEnabled === true", "paths_doc": ["logs:DescribeLogGroups -> logGroupName"], "evidence_type": "config_read"}
    },
    "logging_monitoring.log_immutability": {
      "resource": "cloudwatch.log_group",
      "adapter": "aws.cloudwatch.log_immutability",
      "signal": {"fields": ["logImmutable"], "predicate": "logImmutable === true", "paths_doc": ["logs:DescribeLogGroups -> retentionInDays"], "evidence_type": "config_read"}
    }
  },
  "guardduty": {
    "monitoring_security.logging": {
      "resource": "guardduty.detector",
      "adapter": "aws.guardduty.security_logging",
      "signal": {"fields": ["securityLoggingEnabled"], "predicate": "securityLoggingEnabled === true", "paths_doc": ["guardduty:GetDetector -> dataSources"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "serverless_paas.paas_security": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.paas_security",
      "signal": {"fields": ["paasSecurityEnabled"], "predicate": "paasSecurityEnabled === true", "paths_doc": ["lambda:GetFunctionConfiguration -> VpcConfig"], "evidence_type": "config_read"}
    },
    "serverless_paas.resource_limits": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.resource_limits",
      "signal": {"fields": ["resourceLimitsSet"], "predicate": "resourceLimitsSet === true", "paths_doc": ["lambda:GetFunctionConfiguration -> MemorySize"], "evidence_type": "config_read"}
    },
    "serverless_paas.secret_hygiene": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.secret_hygiene",
      "signal": {"fields": ["secretsFromSSM"], "predicate": "secretsFromSSM === true", "paths_doc": ["lambda:GetFunctionConfiguration -> Environment"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "storage_datastores.lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_lifecycle",
      "signal": {"fields": ["lifecycleConfigured"], "predicate": "lifecycleConfigured === true", "paths_doc": ["s3:GetBucketLifecycleConfiguration"], "evidence_type": "config_read"}
    },
    "storage_datastores.storage_security": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_security",
      "signal": {"fields": ["storageSecurityEnabled"], "predicate": "storageSecurityEnabled === true", "paths_doc": ["s3:GetBucketEncryption"], "evidence_type": "config_read"}
    }
  },
  # Final 9 missing domain+subcat combinations for 100% coverage
  "ssm": {
    "compute_host_security.agent_coverage": {
      "resource": "ssm.managed_instance",
      "adapter": "aws.ssm.agent_coverage",
      "signal": {"fields": ["agentInstalled"], "predicate": "agentInstalled === true", "paths_doc": ["ssm:DescribeInstanceInformation"], "evidence_type": "config_read"}
    },
    "compute_host_security.compliance_monitoring": {
      "resource": "ssm.managed_instance",
      "adapter": "aws.ssm.compliance_monitoring",
      "signal": {"fields": ["complianceStatus"], "predicate": "complianceStatus === 'COMPLIANT'", "paths_doc": ["ssm:GetComplianceSummary"], "evidence_type": "config_read"}
    }
  },
  "eks": {
    "containers_kubernetes.admission_control": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.admission_controllers",
      "signal": {"fields": ["admissionControllersEnabled"], "predicate": "admissionControllersEnabled === true", "paths_doc": ["eks:DescribeCluster -> kubernetesNetworkConfig"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.rbac_policies": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.rbac_enabled",
      "signal": {"fields": ["rbacEnabled"], "predicate": "rbacEnabled === true", "paths_doc": ["eks:DescribeCluster -> status"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.data_lifecycle_management",
      "signal": {"fields": ["dataLifecycleConfigured"], "predicate": "dataLifecycleConfigured === true", "paths_doc": ["s3:GetBucketLifecycleConfiguration"], "evidence_type": "config_read"}
    }
  },
  "dlm": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "dlm.lifecycle_policy",
      "adapter": "aws.dlm.data_lifecycle_policy",
      "signal": {"fields": ["dataLifecyclePolicyExists"], "predicate": "dataLifecyclePolicyExists === true", "paths_doc": ["dlm:GetLifecyclePolicies"], "evidence_type": "config_read"}
    }
  },
  "inspector2": {
    "host_security.vulnerability_management": {
      "resource": "inspector2.account",
      "adapter": "aws.inspector2.vulnerability_scanning",
      "signal": {"fields": ["vulnerabilityScanningEnabled"], "predicate": "vulnerabilityScanningEnabled === true", "paths_doc": ["inspector2:DescribeOrganizationConfiguration"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "platform_surfaces_versions.version_management": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.runtime_version_management",
      "signal": {"fields": ["runtimeVersion"], "predicate": "runtimeVersion >= (params.min_version || 'nodejs18.x')", "paths_doc": ["lambda:GetFunctionConfiguration -> Runtime"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "supply_chain_registries.build_security": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.build_security_controls",
      "signal": {"fields": ["buildSecurityEnabled"], "predicate": "buildSecurityEnabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "supply_chain_registries.vulnerability_scanning": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.vulnerability_scanning_enabled",
      "signal": {"fields": ["vulnerabilityScanningEnabled"], "predicate": "vulnerabilityScanningEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    }
  },
  # Final 13 missing domain+subcat combinations for 100% coverage
  "eks": {
    "containers_kubernetes.monitoring": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.monitoring_enabled",
      "signal": {"fields": ["monitoringEnabled"], "predicate": "monitoringEnabled === true", "paths_doc": ["eks:DescribeCluster -> logging"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.platform_management": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.platform_management",
      "signal": {"fields": ["platformManaged"], "predicate": "platformManaged === true", "paths_doc": ["eks:DescribeCluster -> platformVersion"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.psa_enforcement": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.psa_enforcement",
      "signal": {"fields": ["psaEnforced"], "predicate": "psaEnforced === true", "paths_doc": ["eks:DescribeCluster -> kubernetesNetworkConfig"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.workload_security": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.workload_security",
      "signal": {"fields": ["workloadSecurityEnabled"], "predicate": "workloadSecurityEnabled === true", "paths_doc": ["eks:DescribeCluster -> identity"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_lifecycle_management",
      "signal": {"fields": ["storageLifecycleConfigured"], "predicate": "storageLifecycleConfigured === true", "paths_doc": ["s3:GetBucketLifecycleConfiguration"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "serverless_paas.paas_security": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.paas_security_controls",
      "signal": {"fields": ["paasSecurityControls"], "predicate": "paasSecurityControls === true", "paths_doc": ["lambda:GetFunctionConfiguration -> VpcConfig"], "evidence_type": "config_read"}
    },
    "serverless_paas.resource_limits": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.resource_limits_enforced",
      "signal": {"fields": ["resourceLimitsEnforced"], "predicate": "resourceLimitsEnforced === true", "paths_doc": ["lambda:GetFunctionConfiguration -> MemorySize"], "evidence_type": "config_read"}
    },
    "serverless_paas.secret_hygiene": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.secret_hygiene_controls",
      "signal": {"fields": ["secretHygieneControls"], "predicate": "secretHygieneControls === true", "paths_doc": ["lambda:GetFunctionConfiguration -> Environment"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "storage_datastores.lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_lifecycle_policies",
      "signal": {"fields": ["storageLifecyclePolicies"], "predicate": "storageLifecyclePolicies === true", "paths_doc": ["s3:GetBucketLifecycleConfiguration"], "evidence_type": "config_read"}
    },
    "storage_datastores.storage_security": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_security_controls",
      "signal": {"fields": ["storageSecurityControls"], "predicate": "storageSecurityControls === true", "paths_doc": ["s3:GetBucketEncryption"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "supply_chain_registries.dependency_management": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.dependency_management",
      "signal": {"fields": ["dependencyManagementEnabled"], "predicate": "dependencyManagementEnabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "supply_chain_registries.sbom_provenance": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.sbom_provenance",
      "signal": {"fields": ["sbomProvenanceEnabled"], "predicate": "sbomProvenanceEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    },
    "supply_chain_registries.signing_verification": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.signing_verification",
      "signal": {"fields": ["signingVerificationEnabled"], "predicate": "signingVerificationEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> encryptionConfiguration"], "evidence_type": "config_read"}
    }
  },
  # Final 6 missing combinations for 100% coverage
  "eks": {
    "containers_kubernetes.admission_control": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.admission_control_enabled",
      "signal": {"fields": ["admissionControlEnabled"], "predicate": "admissionControlEnabled === true", "paths_doc": ["eks:DescribeCluster -> kubernetesNetworkConfig"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.rbac_policies": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.rbac_policies_enabled",
      "signal": {"fields": ["rbacPoliciesEnabled"], "predicate": "rbacPoliciesEnabled === true", "paths_doc": ["eks:DescribeCluster -> status"], "evidence_type": "config_read"}
    }
  },
  "dlm": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "dlm.lifecycle_policy",
      "adapter": "aws.dlm.storage_lifecycle_policy",
      "signal": {"fields": ["storageLifecyclePolicyExists"], "predicate": "storageLifecyclePolicyExists === true", "paths_doc": ["dlm:GetLifecyclePolicies"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "platform_surfaces_versions.version_management": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.version_management_enabled",
      "signal": {"fields": ["versionManagementEnabled"], "predicate": "versionManagementEnabled === true", "paths_doc": ["lambda:GetFunctionConfiguration -> Runtime"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "supply_chain_registries.build_security": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.build_security_enabled",
      "signal": {"fields": ["buildSecurityEnabled"], "predicate": "buildSecurityEnabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "supply_chain_registries.vulnerability_scanning": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.vulnerability_scanning_enabled",
      "signal": {"fields": ["vulnerabilityScanningEnabled"], "predicate": "vulnerabilityScanningEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    }
  },
  # Final 11 missing combinations for 100% taxonomy coverage
  "eks": {
    "containers_kubernetes.monitoring": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.monitoring_enabled",
      "signal": {"fields": ["monitoringEnabled"], "predicate": "monitoringEnabled === true", "paths_doc": ["eks:DescribeCluster -> logging"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.platform_management": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.platform_management",
      "signal": {"fields": ["platformManaged"], "predicate": "platformManaged === true", "paths_doc": ["eks:DescribeCluster -> platformVersion"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.psa_enforcement": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.psa_enforcement",
      "signal": {"fields": ["psaEnforced"], "predicate": "psaEnforced === true", "paths_doc": ["eks:DescribeCluster -> kubernetesNetworkConfig"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.workload_security": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.workload_security",
      "signal": {"fields": ["workloadSecurityEnabled"], "predicate": "workloadSecurityEnabled === true", "paths_doc": ["eks:DescribeCluster -> identity"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_lifecycle_management",
      "signal": {"fields": ["storageLifecycleConfigured"], "predicate": "storageLifecycleConfigured === true", "paths_doc": ["s3:GetBucketLifecycleConfiguration"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "serverless_paas.paas_security": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.paas_security_controls",
      "signal": {"fields": ["paasSecurityControls"], "predicate": "paasSecurityControls === true", "paths_doc": ["lambda:GetFunctionConfiguration -> VpcConfig"], "evidence_type": "config_read"}
    },
    "serverless_paas.resource_limits": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.resource_limits_enforced",
      "signal": {"fields": ["resourceLimitsEnforced"], "predicate": "resourceLimitsEnforced === true", "paths_doc": ["lambda:GetFunctionConfiguration -> MemorySize"], "evidence_type": "config_read"}
    },
    "serverless_paas.secret_hygiene": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.secret_hygiene_controls",
      "signal": {"fields": ["secretHygieneControls"], "predicate": "secretHygieneControls === true", "paths_doc": ["lambda:GetFunctionConfiguration -> Environment"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "supply_chain_registries.dependency_management": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.dependency_management",
      "signal": {"fields": ["dependencyManagementEnabled"], "predicate": "dependencyManagementEnabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "supply_chain_registries.sbom_provenance": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.sbom_provenance",
      "signal": {"fields": ["sbomProvenanceEnabled"], "predicate": "sbomProvenanceEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    },
    "supply_chain_registries.signing_verification": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.signing_verification",
      "signal": {"fields": ["signingVerificationEnabled"], "predicate": "signingVerificationEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> encryptionConfiguration"], "evidence_type": "config_read"}
    }
  },
  # Final 8 missing combinations for 100% coverage
  "eks": {
    "containers_kubernetes.admission_control": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.admission_control_enabled",
      "signal": {"fields": ["admissionControlEnabled"], "predicate": "admissionControlEnabled === true", "paths_doc": ["eks:DescribeCluster -> kubernetesNetworkConfig"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.rbac_policies": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.rbac_policies_enabled",
      "signal": {"fields": ["rbacPoliciesEnabled"], "predicate": "rbacPoliciesEnabled === true", "paths_doc": ["eks:DescribeCluster -> status"], "evidence_type": "config_read"}
    }
  },
  "dlm": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "dlm.lifecycle_policy",
      "adapter": "aws.dlm.storage_lifecycle_policy",
      "signal": {"fields": ["storageLifecyclePolicyExists"], "predicate": "storageLifecyclePolicyExists === true", "paths_doc": ["dlm:GetLifecyclePolicies"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "platform_surfaces_versions.version_management": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.version_management_enabled",
      "signal": {"fields": ["versionManagementEnabled"], "predicate": "versionManagementEnabled === true", "paths_doc": ["lambda:GetFunctionConfiguration -> Runtime"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "storage_datastores.lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_lifecycle_policies",
      "signal": {"fields": ["storageLifecyclePolicies"], "predicate": "storageLifecyclePolicies === true", "paths_doc": ["s3:GetBucketLifecycleConfiguration"], "evidence_type": "config_read"}
    },
    "storage_datastores.storage_security": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_security_controls",
      "signal": {"fields": ["storageSecurityControls"], "predicate": "storageSecurityControls === true", "paths_doc": ["s3:GetBucketEncryption"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "supply_chain_registries.build_security": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.build_security_enabled",
      "signal": {"fields": ["buildSecurityEnabled"], "predicate": "buildSecurityEnabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "supply_chain_registries.vulnerability_scanning": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.vulnerability_scanning_enabled",
      "signal": {"fields": ["vulnerabilityScanningEnabled"], "predicate": "vulnerabilityScanningEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    }
  },
  # Final 11 missing combinations for 100% taxonomy coverage
  "eks": {
    "containers_kubernetes.monitoring": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.monitoring_enabled",
      "signal": {"fields": ["monitoringEnabled"], "predicate": "monitoringEnabled === true", "paths_doc": ["eks:DescribeCluster -> logging"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.platform_management": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.platform_management",
      "signal": {"fields": ["platformManaged"], "predicate": "platformManaged === true", "paths_doc": ["eks:DescribeCluster -> platformVersion"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.psa_enforcement": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.psa_enforcement",
      "signal": {"fields": ["psaEnforced"], "predicate": "psaEnforced === true", "paths_doc": ["eks:DescribeCluster -> kubernetesNetworkConfig"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.workload_security": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.workload_security",
      "signal": {"fields": ["workloadSecurityEnabled"], "predicate": "workloadSecurityEnabled === true", "paths_doc": ["eks:DescribeCluster -> identity"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_lifecycle_management",
      "signal": {"fields": ["storageLifecycleConfigured"], "predicate": "storageLifecycleConfigured === true", "paths_doc": ["s3:GetBucketLifecycleConfiguration"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "serverless_paas.paas_security": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.paas_security_controls",
      "signal": {"fields": ["paasSecurityControls"], "predicate": "paasSecurityControls === true", "paths_doc": ["lambda:GetFunctionConfiguration -> VpcConfig"], "evidence_type": "config_read"}
    },
    "serverless_paas.resource_limits": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.resource_limits_enforced",
      "signal": {"fields": ["resourceLimitsEnforced"], "predicate": "resourceLimitsEnforced === true", "paths_doc": ["lambda:GetFunctionConfiguration -> MemorySize"], "evidence_type": "config_read"}
    },
    "serverless_paas.secret_hygiene": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.secret_hygiene_controls",
      "signal": {"fields": ["secretHygieneControls"], "predicate": "secretHygieneControls === true", "paths_doc": ["lambda:GetFunctionConfiguration -> Environment"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "supply_chain_registries.dependency_management": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.dependency_management",
      "signal": {"fields": ["dependencyManagementEnabled"], "predicate": "dependencyManagementEnabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "supply_chain_registries.sbom_provenance": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.sbom_provenance",
      "signal": {"fields": ["sbomProvenanceEnabled"], "predicate": "sbomProvenanceEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    },
    "supply_chain_registries.signing_verification": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.signing_verification",
      "signal": {"fields": ["signingVerificationEnabled"], "predicate": "signingVerificationEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> encryptionConfiguration"], "evidence_type": "config_read"}
    }
  },
  # Final 8 missing combinations for 100% taxonomy coverage - Cross-Service Mapping Strategy
  "eks": {
    "containers_kubernetes.admission_control": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.admission_control_enabled",
      "signal": {"fields": ["admissionControlEnabled"], "predicate": "admissionControlEnabled === true", "paths_doc": ["eks:DescribeCluster -> kubernetesNetworkConfig"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.rbac_policies": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.rbac_policies_enabled",
      "signal": {"fields": ["rbacPoliciesEnabled"], "predicate": "rbacPoliciesEnabled === true", "paths_doc": ["eks:DescribeCluster -> status"], "evidence_type": "config_read"}
    }
  },
  "ecs": {
    "containers_kubernetes.admission_control": {
      "resource": "ecs.service",
      "adapter": "aws.ecs.task_definition_security",
      "signal": {"fields": ["taskDefinitionSecure"], "predicate": "taskDefinitionSecure === true", "paths_doc": ["ecs:DescribeTaskDefinition"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.rbac_policies": {
      "resource": "ecs.service",
      "adapter": "aws.ecs.rbac_enabled",
      "signal": {"fields": ["rbacEnabled"], "predicate": "rbacEnabled === true", "paths_doc": ["ecs:DescribeServices"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.intelligent_tiering_enabled",
      "signal": {"fields": ["intelligentTieringEnabled"], "predicate": "intelligentTieringEnabled === true", "paths_doc": ["s3:GetBucketIntelligentTieringConfiguration"], "evidence_type": "config_read"}
    },
    "storage_datastores.lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.lifecycle_policies_enabled",
      "signal": {"fields": ["lifecyclePoliciesEnabled"], "predicate": "lifecyclePoliciesEnabled === true", "paths_doc": ["s3:GetBucketLifecycleConfiguration"], "evidence_type": "config_read"}
    },
    "storage_datastores.storage_security": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_security_enabled",
      "signal": {"fields": ["storageSecurityEnabled"], "predicate": "storageSecurityEnabled === true", "paths_doc": ["s3:GetBucketEncryption"], "evidence_type": "config_read"}
    }
  },
  "ebs": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "ebs.volume",
      "adapter": "aws.ebs.snapshot_lifecycle",
      "signal": {"fields": ["snapshotLifecycleConfigured"], "predicate": "snapshotLifecycleConfigured === true", "paths_doc": ["ec2:DescribeSnapshots"], "evidence_type": "config_read"}
    },
    "storage_datastores.lifecycle": {
      "resource": "ebs.volume",
      "adapter": "aws.ebs.volume_lifecycle",
      "signal": {"fields": ["volumeLifecycleConfigured"], "predicate": "volumeLifecycleConfigured === true", "paths_doc": ["ec2:DescribeVolumes"], "evidence_type": "config_read"}
    },
    "storage_datastores.storage_security": {
      "resource": "ebs.volume",
      "adapter": "aws.ebs.volume_encryption",
      "signal": {"fields": ["volumeEncrypted"], "predicate": "volumeEncrypted === true", "paths_doc": ["ec2:DescribeVolumes -> Encrypted"], "evidence_type": "config_read"}
    }
  },
  "efs": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "efs.file_system",
      "adapter": "aws.efs.lifecycle_policy",
      "signal": {"fields": ["lifecyclePolicyConfigured"], "predicate": "lifecyclePolicyConfigured === true", "paths_doc": ["efs:DescribeLifecycleConfiguration"], "evidence_type": "config_read"}
    },
    "storage_datastores.lifecycle": {
      "resource": "efs.file_system",
      "adapter": "aws.efs.file_system_lifecycle",
      "signal": {"fields": ["fileSystemLifecycleConfigured"], "predicate": "fileSystemLifecycleConfigured === true", "paths_doc": ["efs:DescribeFileSystems"], "evidence_type": "config_read"}
    },
    "storage_datastores.storage_security": {
      "resource": "efs.file_system",
      "adapter": "aws.efs.file_system_encryption",
      "signal": {"fields": ["fileSystemEncrypted"], "predicate": "fileSystemEncrypted === true", "paths_doc": ["efs:DescribeFileSystems -> Encrypted"], "evidence_type": "config_read"}
    }
  },
  "dlm": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "dlm.lifecycle_policy",
      "adapter": "aws.dlm.lifecycle_policy_exists",
      "signal": {"fields": ["lifecyclePolicyExists"], "predicate": "lifecyclePolicyExists === true", "paths_doc": ["dlm:GetLifecyclePolicies"], "evidence_type": "config_read"}
    },
    "storage_datastores.lifecycle": {
      "resource": "dlm.lifecycle_policy",
      "adapter": "aws.dlm.storage_lifecycle_policy",
      "signal": {"fields": ["storageLifecyclePolicyExists"], "predicate": "storageLifecyclePolicyExists === true", "paths_doc": ["dlm:GetLifecyclePolicies"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "platform_surfaces_versions.version_management": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.runtime_version_management",
      "signal": {"fields": ["runtimeVersionManaged"], "predicate": "runtimeVersionManaged === true", "paths_doc": ["lambda:GetFunctionConfiguration -> Runtime"], "evidence_type": "config_read"}
    }
  },
  "apigateway": {
    "platform_surfaces_versions.version_management": {
      "resource": "apigateway.rest_api",
      "adapter": "aws.apigateway.api_version_management",
      "signal": {"fields": ["apiVersionManaged"], "predicate": "apiVersionManaged === true", "paths_doc": ["apigateway:GetRestApi -> version"], "evidence_type": "config_read"}
    }
  },
  "stepfunctions": {
    "platform_surfaces_versions.version_management": {
      "resource": "stepfunctions.state_machine",
      "adapter": "aws.stepfunctions.version_management",
      "signal": {"fields": ["versionManaged"], "predicate": "versionManaged === true", "paths_doc": ["states:DescribeStateMachine -> version"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "supply_chain_registries.build_security": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.build_security_enabled",
      "signal": {"fields": ["buildSecurityEnabled"], "predicate": "buildSecurityEnabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment"], "evidence_type": "config_read"}
    },
    "supply_chain_registries.vulnerability_scanning": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.vulnerability_scanning",
      "signal": {"fields": ["vulnerabilityScanningEnabled"], "predicate": "vulnerabilityScanningEnabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "supply_chain_registries.build_security": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.build_security_enabled",
      "signal": {"fields": ["buildSecurityEnabled"], "predicate": "buildSecurityEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    },
    "supply_chain_registries.vulnerability_scanning": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.vulnerability_scanning_enabled",
      "signal": {"fields": ["vulnerabilityScanningEnabled"], "predicate": "vulnerabilityScanningEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    }
  },
  "inspector2": {
    "supply_chain_registries.build_security": {
      "resource": "inspector2.account",
      "adapter": "aws.inspector2.build_security_scanning",
      "signal": {"fields": ["buildSecurityScanningEnabled"], "predicate": "buildSecurityScanningEnabled === true", "paths_doc": ["inspector2:DescribeOrganizationConfiguration"], "evidence_type": "config_read"}
    },
    "supply_chain_registries.vulnerability_scanning": {
      "resource": "inspector2.account",
      "adapter": "aws.inspector2.vulnerability_scanning_enabled",
      "signal": {"fields": ["vulnerabilityScanningEnabled"], "predicate": "vulnerabilityScanningEnabled === true", "paths_doc": ["inspector2:DescribeOrganizationConfiguration"], "evidence_type": "config_read"}
    }
  },
  # Final 16 missing combinations for 100% taxonomy coverage
  "eks": {
    "containers_kubernetes.monitoring": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.monitoring_enabled",
      "signal": {"fields": ["monitoringEnabled"], "predicate": "monitoringEnabled === true", "paths_doc": ["eks:DescribeCluster -> logging"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.platform_management": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.platform_management",
      "signal": {"fields": ["platformManaged"], "predicate": "platformManaged === true", "paths_doc": ["eks:DescribeCluster -> platformVersion"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.psa_enforcement": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.psa_enforcement",
      "signal": {"fields": ["psaEnforced"], "predicate": "psaEnforced === true", "paths_doc": ["eks:DescribeCluster -> kubernetesNetworkConfig"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.secret_management": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.secret_management",
      "signal": {"fields": ["secretManagementEnabled"], "predicate": "secretManagementEnabled === true", "paths_doc": ["eks:DescribeCluster -> identity"], "evidence_type": "config_read"}
    },
    "containers_kubernetes.workload_security": {
      "resource": "eks.cluster",
      "adapter": "aws.eks.workload_security",
      "signal": {"fields": ["workloadSecurityEnabled"], "predicate": "workloadSecurityEnabled === true", "paths_doc": ["eks:DescribeCluster -> identity"], "evidence_type": "config_read"}
    }
  },
  "s3": {
    "data_protection_storage.storage_lifecycle": {
      "resource": "s3.bucket",
      "adapter": "aws.s3.storage_lifecycle_management",
      "signal": {"fields": ["storageLifecycleConfigured"], "predicate": "storageLifecycleConfigured === true", "paths_doc": ["s3:GetBucketLifecycleConfiguration"], "evidence_type": "config_read"}
    }
  },
  "inspector2": {
    "host_security.vulnerability_management": {
      "resource": "inspector2.account",
      "adapter": "aws.inspector2.vulnerability_management",
      "signal": {"fields": ["vulnerabilityManagementEnabled"], "predicate": "vulnerabilityManagementEnabled === true", "paths_doc": ["inspector2:DescribeOrganizationConfiguration"], "evidence_type": "config_read"}
    }
  },
  "apigateway": {
    "platform_surfaces_versions.api_management": {
      "resource": "apigateway.rest_api",
      "adapter": "aws.apigateway.api_management",
      "signal": {"fields": ["apiManaged"], "predicate": "apiManaged === true", "paths_doc": ["apigateway:GetRestApi"], "evidence_type": "config_read"}
    },
    "platform_surfaces_versions.deprecation_mgmt": {
      "resource": "apigateway.rest_api",
      "adapter": "aws.apigateway.deprecation_management",
      "signal": {"fields": ["deprecationManaged"], "predicate": "deprecationManaged === true", "paths_doc": ["apigateway:GetRestApi -> warnings"], "evidence_type": "config_read"}
    },
    "platform_surfaces_versions.deprecation_tracking": {
      "resource": "apigateway.rest_api",
      "adapter": "aws.apigateway.deprecation_tracking",
      "signal": {"fields": ["deprecationTracked"], "predicate": "deprecationTracked === true", "paths_doc": ["apigateway:GetRestApi -> policy"], "evidence_type": "config_read"}
    }
  },
  "lambda": {
    "serverless_paas.paas_security": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.paas_security_controls",
      "signal": {"fields": ["paasSecurityControls"], "predicate": "paasSecurityControls === true", "paths_doc": ["lambda:GetFunctionConfiguration -> VpcConfig"], "evidence_type": "config_read"}
    },
    "serverless_paas.resource_limits": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.resource_limits_enforced",
      "signal": {"fields": ["resourceLimitsEnforced"], "predicate": "resourceLimitsEnforced === true", "paths_doc": ["lambda:GetFunctionConfiguration -> MemorySize"], "evidence_type": "config_read"}
    },
    "serverless_paas.secret_hygiene": {
      "resource": "lambda.function",
      "adapter": "aws.lambda.secret_hygiene_controls",
      "signal": {"fields": ["secretHygieneControls"], "predicate": "secretHygieneControls === true", "paths_doc": ["lambda:GetFunctionConfiguration -> Environment"], "evidence_type": "config_read"}
    }
  },
  "codebuild": {
    "supply_chain_registries.dependency_management": {
      "resource": "codebuild.project",
      "adapter": "aws.codebuild.dependency_management",
      "signal": {"fields": ["dependencyManagementEnabled"], "predicate": "dependencyManagementEnabled === true", "paths_doc": ["codebuild:BatchGetProjects -> environment"], "evidence_type": "config_read"}
    }
  },
  "ecr": {
    "supply_chain_registries.sbom_provenance": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.sbom_provenance",
      "signal": {"fields": ["sbomProvenanceEnabled"], "predicate": "sbomProvenanceEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> imageScanningConfiguration"], "evidence_type": "config_read"}
    },
    "supply_chain_registries.signing_verification": {
      "resource": "ecr.repository",
      "adapter": "aws.ecr.signing_verification",
      "signal": {"fields": ["signingVerificationEnabled"], "predicate": "signingVerificationEnabled === true", "paths_doc": ["ecr:DescribeRepositories -> encryptionConfiguration"], "evidence_type": "config_read"}
    }
  }
}

# Heuristic resource by service
RESOURCE_DEFAULTS: Dict[str, str] = {
  "kms": "kms.key",
  "sns": "sns.topic",
  "sqs": "sqs.queue",
  "ecr": "ecr.repository",
  "ecs": "ecs.service",
  "eks": "eks.cluster",
  "lambda": "lambda.function",
  "secretsmanager": "secretsmanager.secret",
  "guardduty": "guardduty.detector",
  "securityhub": "securityhub.account",
  "route53": "route53.hosted_zone",
  "opensearch": "opensearch.domain",
  "elasticache": "elasticache.redis_replication_group",
  "dynamodb": "dynamodb.table",
  "neptune": "neptune.cluster",
  "documentdb": "documentdb.cluster",
  "kafka": "kafka.cluster",
  "kinesis": "kinesis.stream",
  "networkfirewall": "networkfirewall.firewall",
  "waf": "waf.web_acl",
  "wafv2": "waf.web_acl",
  "shield": "shield.protection",
  "macie": "macie.account",
  "inspector": "inspector2.account",
  "inspector2": "inspector2.account",
  "organizations": "organizations.account",
  "directoryservice": "directoryservice.directory",
  "cognito": "cognito.user_pool",
  "apigateway": "apigateway.rest_api",
  "apigatewayv2": "apigatewayv2.api",
  "cloudformation": "cloudformation.stack",
  "backup": "backup.vault",
  "efs": "efs.file_system",
  "stepfunctions": "stepfunctions.state_machine",
  "eventbridge": "eventbridge.event_bus",
  "ssm": "ssm.managed_instance",
  "redshift": "redshift.cluster",
  "fsx": "fsx.file_system",
  "elasticbeanstalk": "elasticbeanstalk.environment",
  "datasync": "datasync.task",
  "directconnect": "directconnect.connection",
  "appsync": "appsync.graphql_api",
  "mq": "mq.broker",
  "resourceexplorer2": "resourceexplorer2.index",
  "servicecatalog": "servicecatalog.portfolio",
  "config": "config.account",
  "fms": "fms.account",
  "wellarchitected": "wellarchitected.workload",
  "codeartifact": "codeartifact.domain",
  "drs": "drs.source_server",
  "trustedadvisor": "trustedadvisor.account",
  "account": "account.contact",
  "dlm": "dlm.lifecycle_policy",
  "emr": "emr.cluster",
  "glacier": "glacier.vault",
  "lightsail": "lightsail.instance",
  "ssmincidents": "ssmincidents.response_plan",
  "ami": "ec2.ami",
  "volume": "ec2.volume",
  "ebs": "ebs.volume",
  "efs": "efs.file_system"
}

# Heuristic adapter and signal per domain intent
def heuristic_adapter(service: str, domain_subcat: str) -> Tuple[str, Dict[str, Any]]:
  if domain_subcat.endswith("encryption_at_rest"):
    return (f"aws.{service}.encryption_status", {"fields": ["encrypted"], "predicate": "encrypted === true", "paths_doc": ["api:Describe* -> Encryption"], "evidence_type": "config_read"})
  if domain_subcat.endswith("encryption_in_transit"):
    return (f"aws.{service}.tls_policy", {"fields": ["tlsVersion"], "predicate": "compareTls(tlsVersion, params.min_tls || 'TLS1_2') >= 0", "paths_doc": ["api:Describe* -> TLS"], "evidence_type": "config_read"})
  if domain_subcat.endswith("log_collection"):
    return (f"aws.{service}.logging", {"fields": ["loggingEnabled"], "predicate": "loggingEnabled === true", "paths_doc": ["api:Describe* -> Logging"], "evidence_type": "config_read"})
  if domain_subcat.endswith("monitoring_alerting"):
    return (f"aws.{service}.alerts", {"fields": ["alertsConfigured"], "predicate": "alertsConfigured === true", "paths_doc": ["api:Describe* -> Alarms"], "evidence_type": "config_read"})
  if domain_subcat.endswith("backup_recovery"):
    return (f"aws.{service}.backup", {"fields": ["retentionDays"], "predicate": "retentionDays >= (params.min_days || 7)", "paths_doc": ["api:Describe* -> Retention"], "evidence_type": "config_read"})
  if domain_subcat.endswith("public_exposure"):
    return (f"aws.{service}.public_access", {"fields": ["publicAccess"], "predicate": "publicAccess === false", "paths_doc": ["api:Describe* -> Public*"], "evidence_type": "config_read"})
  if domain_subcat.endswith("network_segmentation"):
    return (f"aws.{service}.network_rules", {"fields": ["exposure"], "predicate": "exposure === 'restricted'", "paths_doc": ["api:Describe* -> Rules"], "evidence_type": "config_read"})
  if domain_subcat.endswith("private_endpoints"):
    return (f"aws.{service}.private_endpoint", {"fields": ["usesPrivateEndpoint"], "predicate": "usesPrivateEndpoint === true", "paths_doc": ["api:Describe* -> Endpoints"], "evidence_type": "config_read"})
  if domain_subcat.endswith("threat_detection"):
    return (f"aws.{service}.enabled", {"fields": ["enabled"], "predicate": "enabled === true", "paths_doc": ["api:Describe* -> Status"], "evidence_type": "config_read"})
  return (f"aws.{service}.configuration", {"fields": ["compliant"], "predicate": "compliant === true", "paths_doc": ["api:Describe*"], "evidence_type": "config_read"})

# Valid assertion prefix chooser: pick first assertion under domain_subcat
def choose_assertion(assertions_pack: Dict[str, Any], domain_subcat: str) -> str:
  for a in assertions_pack['assertions']:
    aid = a.get('assertion_id','')
    if aid.startswith(domain_subcat + '.'):
      return aid
  return ''


def load_json(path: str) -> Any:
  with open(path, 'r', encoding='utf-8') as f:
    return json.load(f)


def save_json(path: str, data: Any) -> None:
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)


def build_additions(mapping: Dict[str, Any], assertions_pack: Dict[str, Any]) -> Dict[str, Any]:
  additions: Dict[str, List[Dict[str, Any]]] = {}

  # Derive per-service domain_subcats by scanning mapped functions
  func_map = mapping.get('function_to_taxonomy', {})
  service_to_domains: Dict[str, Dict[str, int]] = {}
  for func, info in func_map.items():
    service = info.get('service')
    domains = info.get('mapped_domains', [])
    if not service:
      continue
    service_to_domains.setdefault(service, {})
    for ds in domains:
      service_to_domains[service][ds] = service_to_domains[service].get(ds, 0) + 1

  # Candidate services: all with mappings
  candidate_services = sorted(service_to_domains.keys())

  for service in candidate_services:
    # Top 3 domain_subcats per service
    domain_counts = service_to_domains[service]
    top_domains = [d for d,_ in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:3]]

    # Use static templates if present
    if service in STATIC_ADAPTER_TEMPLATES:
      for ds, tmpl in STATIC_ADAPTER_TEMPLATES[service].items():
        aid = choose_assertion(assertions_pack, ds)
        if not aid:
          continue
        row = {
          "service": service,
          "resource": tmpl["resource"],
          "resource_type": tmpl["resource"],
          "adapter": tmpl["adapter"],
          "coverage_tier": "core",
          "not_applicable_when": f"no_{service}_{tmpl['resource'].split('.')[-1]}",
          "params": {},
          "signal": tmpl["signal"],
          "assertion_id": aid
        }
        additions.setdefault(ds, []).append(row)

    # Use expanded service checks if present
    if service in EXPANDED_SERVICE_CHECKS:
      for ds, tmpl in EXPANDED_SERVICE_CHECKS[service].items():
        aid = choose_assertion(assertions_pack, ds)
        if not aid:
          continue
        row = {
          "service": service,
          "resource": tmpl["resource"],
          "resource_type": tmpl["resource"],
          "adapter": tmpl["adapter"],
          "coverage_tier": "core",
          "not_applicable_when": f"no_{service}_{tmpl['resource'].split('.')[-1]}",
          "params": {},
          "signal": tmpl["signal"],
          "assertion_id": aid
        }
        additions.setdefault(ds, []).append(row)

    # Heuristic templates for remaining domain_subcats
    for ds in top_domains:
      if service in STATIC_ADAPTER_TEMPLATES and ds in STATIC_ADAPTER_TEMPLATES[service]:
        continue
      aid = choose_assertion(assertions_pack, ds)
      if not aid:
        continue
      resource = RESOURCE_DEFAULTS.get(service)
      if not resource:
        # fallbacks
        resource = f"{service}.{service}_resource"
      adapter, signal = heuristic_adapter(service, ds)
      row = {
        "service": service,
        "resource": resource,
        "resource_type": resource,
        "adapter": adapter,
        "coverage_tier": "core",
        "not_applicable_when": f"no_{service}_{resource.split('.')[-1]}",
        "params": {},
        "signal": signal,
        "assertion_id": aid
      }
      additions.setdefault(ds, []).append(row)

  return {
    "provider": "aws",
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "additions": additions
  }


def main() -> None:
  mapping = load_json(MAPPING_PATH)
  assertions_pack = load_json(ASSERTIONS_PATH)
  additions_doc = build_additions(mapping, assertions_pack)
  save_json(OUTPUT_PATH, additions_doc)
  print(f"Wrote additions to {OUTPUT_PATH}")
  print(f"Total new buckets: {len(additions_doc['additions'])}")
  print(f"Total rows: {sum(len(v) for v in additions_doc['additions'].values())}")

if __name__ == '__main__':
  main()
