#!/usr/bin/env python3
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple, Optional

AWS_MATRIX_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_matrix_2025-09-11T20-00-38.json.backup"
ASSERTIONS_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14.json"
OUTPUT_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step4-rune-per-cloud-provider/aws_matrix_enriched_atomic_full_plus5_2025-09-24.json"


# --- Utilities ---

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# --- Assertions indexing ---

def index_assertions_by_domain_subcat(assertions_root: Dict[str, Any]) -> Dict[Tuple[str, str], List[Dict[str, Any]]]:
    by_key: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    assertions = assertions_root.get("assertions") or assertions_root.get("data") or []
    for a in assertions:
        subref = a.get("subcat_ref") or {}
        domain_key = subref.get("domain_key")
        subcat_id = subref.get("subcat_id")
        if not domain_key or not subcat_id:
            continue
        by_key.setdefault((domain_key, subcat_id), []).append(a)
    return by_key


def pick_params_for(domain_key: str, subcat_id: str, assertions_by_key: Dict[Tuple[str, str], List[Dict[str, Any]]]) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    for a in assertions_by_key.get((domain_key, subcat_id), []):
        a_params = a.get("params")
        if isinstance(a_params, dict):
            params.update({k: v for k, v in a_params.items() if v is not None})
    return params


# --- Heuristic signal mapping ---

class SignalSpec:
    def __init__(self, fields: List[str], predicate: str, paths_doc: List[str], evidence_type: str = "config_read") -> None:
        self.fields = fields
        self.predicate = predicate
        self.paths_doc = paths_doc
        self.evidence_type = evidence_type


def signal_from_adapter(adapter: str, service: str, resource_type: str) -> SignalSpec:
    a = adapter.lower()

    # S3 encryption, PAB, logging, versioning, object lock
    if "s3.bucket_encryption" in a:
        return SignalSpec(
            fields=["serverSideEncryption.enabled", "serverSideEncryption.kmsKeyId"],
            predicate="serverSideEncryption.enabled === true",
            paths_doc=["S3:GetBucketEncryption -> ServerSideEncryptionConfiguration"],
        )
    if "s3.public_access_block" in a:
        return SignalSpec(
            fields=[
                "publicAccessBlock.blockPublicAcls",
                "publicAccessBlock.ignorePublicAcls",
                "publicAccessBlock.blockPublicPolicy",
                "publicAccessBlock.restrictPublicBuckets",
            ],
            predicate="blockPublicAcls === true && ignorePublicAcls === true && blockPublicPolicy === true && restrictPublicBuckets === true",
            paths_doc=["S3:GetPublicAccessBlock -> PublicAccessBlockConfiguration"],
        )
    if "s3.access_logging" in a:
        return SignalSpec(
            fields=["logging.enabled", "logging.targetBucket"],
            predicate="logging.enabled === true && logging.targetBucket != null",
            paths_doc=["S3:GetBucketLogging -> LoggingEnabled"],
        )
    if "s3.versioning" in a:
        return SignalSpec(
            fields=["versioning.status"],
            predicate="versioning.status === 'Enabled'",
            paths_doc=["S3:GetBucketVersioning -> Status"],
        )
    if "s3.object_lock" in a or "s3.bucket_versioning_lock" in a or "s3.lifecycle_management" in a:
        return SignalSpec(
            fields=["objectLock.enabled", "versioning.status", "lifecycle.rules[].status"],
            predicate="(objectLock.enabled === true && versioning.status === 'Enabled') || lifecycle.rules.length >= 1",
            paths_doc=["S3:GetObjectLockConfiguration", "S3:GetBucketVersioning", "S3:GetBucketLifecycleConfiguration"],
        )

    # CloudTrail collection, retention, integrity
    if "cloudtrail.log_collection" in a or "cloudtrail.audit_logging" in a:
        return SignalSpec(
            fields=["trail.enabled", "trail.multiRegion", "trail.logFileValidation"],
            predicate="trail.enabled === true && trail.multiRegion === true && trail.logFileValidation === true",
            paths_doc=["CloudTrail:DescribeTrails", "CloudTrail:GetTrailStatus"],
        )
    if "cloudtrail.log_retention" in a:
        return SignalSpec(
            fields=["destination.retentionDays"],
            predicate="destination.retentionDays >= params.minRetentionDays",
            paths_doc=["CloudTrail:DescribeTrails", "S3:GetBucketLifecycleConfiguration"],
        )
    if "cloudtrail.log_integrity" in a or "cloudtrail.s3_object_lock" in a:
        return SignalSpec(
            fields=["destination.bucketObjectLock.enabled"],
            predicate="destination.bucketObjectLock.enabled === true",
            paths_doc=["S3:GetObjectLockConfiguration"],
        )

    # AWS Config enablement / recorder / delivery / rules
    if "config.compliance_rules" in a or "config.audit_rules" in a or "config.deprecation_rules" in a:
        return SignalSpec(
            fields=["recorder.enabled", "delivery.channelConfigured", "rules.count"],
            predicate="recorder.enabled === true && delivery.channelConfigured === true && rules.count >= 1",
            paths_doc=["Config:DescribeConfigurationRecorders", "Config:DescribeDeliveryChannels", "Config:DescribeConfigRules"],
        )

    # KMS key rotation / policies / crypto policies
    if ".kms." in a and ("rotation" in a or "key_rotation" in a):
        return SignalSpec(
            fields=["rotationEnabled"],
            predicate="rotationEnabled === true",
            paths_doc=["KMS:ListKeys", "KMS:GetKeyRotationStatus"],
        )
    if "kms.key_policies" in a or "kms.crypto_policies" in a or "kms.import_key_material" in a:
        return SignalSpec(
            fields=["keyPolicy.principals", "keyPolicy.conditions"],
            predicate="keyPolicy.principals.length >= 1",
            paths_doc=["KMS:GetKeyPolicy"],
        )

    # Secrets Manager rotation / storage
    if "secrets_manager.rotation" in a or "secretsmanager.rotation" in a:
        return SignalSpec(
            fields=["rotationEnabled", "rotationLambdaArn"],
            predicate="rotationEnabled === true",
            paths_doc=["SecretsManager:DescribeSecret -> RotationEnabled, RotationRules, RotationLambdaARN"],
        )
    if "secrets_manager.secret_storage" in a or "secretsmanager.unused_secrets" in a:
        return SignalSpec(
            fields=["kmsKeyId", "lastAccessedDate"],
            predicate="kmsKeyId != null",
            paths_doc=["SecretsManager:DescribeSecret -> KmsKeyId, LastAccessedDate"],
        )

    # EBS / RDS / DynamoDB at-rest encryption
    if "ebs.volume_encryption" in a or "ebs.kms_encryption" in a:
        return SignalSpec(
            fields=["encrypted", "kmsKeyId"],
            predicate="encrypted === true",
            paths_doc=["EC2:DescribeVolumes -> Encrypted, KmsKeyId"],
        )
    if "ebs.snapshot_encryption" in a:
        return SignalSpec(
            fields=["encrypted", "kmsKeyId"],
            predicate="encrypted === true",
            paths_doc=["EC2:DescribeSnapshots -> Encrypted, KmsKeyId"],
        )
    if "rds.instance_encryption" in a or "rds.kms_encryption" in a or "rds.master_key_rotation" in a:
        return SignalSpec(
            fields=["storageEncrypted", "kmsKeyId"],
            predicate="storageEncrypted === true",
            paths_doc=["RDS:DescribeDBInstances -> StorageEncrypted, KmsKeyId"],
        )
    if "rds.snapshots" in a:
        return SignalSpec(
            fields=["snapshots[].encrypted"],
            predicate="snapshots.every(s => s.encrypted === true)",
            paths_doc=["RDS:DescribeDBSnapshots -> Encrypted"],
        )
    if "dynamodb.table_encryption" in a or "dynamodb.kms_cmk" in a:
        return SignalSpec(
            fields=["sseDescription.status", "sseDescription.kmsMasterKeyArn"],
            predicate="sseDescription.status === 'ENABLED'",
            paths_doc=["DynamoDB:DescribeTable -> SSEDescription"],
        )

    # IAM MFA + policy surface
    if "iam.mfa" in a or "iam.user_mfa_status" in a or "iam.group_mfa_enforcement" in a:
        return SignalSpec(
            fields=["mfaDevicesRegistered", "mfaRequired"],
            predicate="mfaRequired === true && mfaDevicesRegistered >= 1",
            paths_doc=["IAM:ListMFADevices", "IAM:GetAccountSummary or IAM:GetLoginProfile"],
        )
    if "iam.role_policies" in a:
        return SignalSpec(
            fields=["inlinePolicies.count", "attachedPolicies[].policyArn"],
            predicate="inlinePolicies.count >= 0",
            paths_doc=["IAM:ListRolePolicies", "IAM:ListAttachedRolePolicies"],
        )
    if "iam.managed_policies" in a or "iam.custom_policies" in a or "iam.organization_policies" in a or "iam.entitlement_policies" in a or "iam.policy_management" in a:
        return SignalSpec(
            fields=["policies[].policyArn", "policies[].defaultVersionId"],
            predicate="policies.length >= 1",
            paths_doc=["IAM:ListPolicies", "IAM:GetPolicy"],
        )
    if "iam.permission_boundaries" in a:
        return SignalSpec(
            fields=["permissionBoundary.policyArn"],
            predicate="permissionBoundary.policyArn != null",
            paths_doc=["IAM:GetUser or GetRole -> PermissionBoundary"],
        )
    if "iam.inline_policies" in a or "iam.group_policies" in a:
        return SignalSpec(
            fields=["inlinePolicies.count"],
            predicate="inlinePolicies.count >= 0",
            paths_doc=["IAM:ListUserPolicies or ListGroupPolicies"],
        )

    # ELB/ELBV2 TLS and security groups, WAF integration
    if "elbv2.ssl_certificates" in a or "elb.ssl_termination" in a:
        return SignalSpec(
            fields=["listeners[].protocol", "listeners[].sslPolicy"],
            predicate="listeners.every(l => l.protocol === 'HTTPS' && compareTls(l.sslPolicy, params.minTlsPolicy) >= 0)",
            paths_doc=["ELBv2:DescribeListeners -> Protocol, SslPolicy"],
        )
    if "elbv2.security_groups" in a:
        return SignalSpec(
            fields=["securityGroups[].groupId"],
            predicate="securityGroups.length >= 1",
            paths_doc=["ELBv2:DescribeLoadBalancers -> SecurityGroups"],
        )
    if "elbv2.waf_integration" in a or "cloudfront.waf_enabled" in a or "apigateway.waf_enabled" in a:
        return SignalSpec(
            fields=["webACLId"],
            predicate="webACLId != null",
            paths_doc=["WAFv2:GetWebACLForResource or CloudFront:GetDistribution -> WebACLId"],
        )

    # CloudFront HTTPS/TLS
    if "cloudfront.https_enforcement" in a:
        return SignalSpec(
            fields=["viewerProtocolPolicy", "minimumProtocolVersion"],
            predicate="viewerProtocolPolicy === 'redirect-to-https' && compareTls(minimumProtocolVersion, params.minTlsVersion) >= 0",
            paths_doc=["CloudFront:GetDistributionConfig -> DefaultCacheBehavior.ViewerProtocolPolicy, ViewerCertificate.MinimumProtocolVersion"],
        )

    # API Gateway SSL enforcement / keys / rate limiting
    if "apigateway.ssl_enforcement" in a:
        return SignalSpec(
            fields=["endpointConfiguration.types[]", "minimumTlsVersion"],
            predicate="endpointConfiguration.types.includes('EDGE') || compareTls(minimumTlsVersion, params.minTlsVersion) >= 0",
            paths_doc=["APIGateway:GET /restapis/{id} -> endpointConfiguration, minimumTlsVersion"],
        )
    if "apigateway.api_keys" in a:
        return SignalSpec(
            fields=["apiKeys.count"],
            predicate="apiKeys.count >= 0",
            paths_doc=["APIGateway:GET /apikeys"],
        )
    if "apigateway.rate_limiting" in a or "apigateway.api_management" in a:
        return SignalSpec(
            fields=["usagePlans[].throttle"],
            predicate="usagePlans.length >= 0",
            paths_doc=["APIGateway:GET /usageplans"],
        )

    # VPC: security groups, route tables, endpoints, peering
    if "ec2.security_groups_deny_all_default" in a or "ec2.security_group_rules" in a:
        return SignalSpec(
            fields=["ingressRules[]", "egressRules[]"],
            predicate="ingressRules.every(r => r.cidr != '0.0.0.0/0')",
            paths_doc=["EC2:DescribeSecurityGroups -> IpPermissions, IpPermissionsEgress"],
        )
    if "ec2.route_table_routes" in a or "ec2.route_tables" in a:
        return SignalSpec(
            fields=["routes[]"],
            predicate="routes.length >= 0",
            paths_doc=["EC2:DescribeRouteTables -> Routes"],
        )
    if "ec2.vpc_endpoints" in a or "vpc.private_endpoints" in a or "ec2.interface_endpoints" in a:
        return SignalSpec(
            fields=["endpoints[].vpcEndpointId", "endpoints[].policyDocument"],
            predicate="endpoints.length >= 0",
            paths_doc=["EC2:DescribeVpcEndpoints"],
        )

    # WAFv2
    if "wafv2.web_acl" in a or "wafv2.rule_groups" in a:
        return SignalSpec(
            fields=["webACLs[].id", "webACLs[].defaultAction"],
            predicate="webACLs.length >= 0",
            paths_doc=["WAFv2:ListWebACLs", "WAFv2:GetWebACL"],
        )

    # Network Firewall / Route53 Resolver
    if "networkfirewall.firewall_policy" in a or "networkfirewall.rule_groups" in a or "network_firewall.policy_enforcement" in a:
        return SignalSpec(
            fields=["firewallPolicy.policyArn"],
            predicate="firewallPolicy.policyArn != null",
            paths_doc=["NetworkFirewall:DescribeFirewallPolicy"],
        )
    if "route53" in a and "dns_security" in a:
        return SignalSpec(
            fields=["dnssecStatus"],
            predicate="dnssecStatus === 'ENABLED'",
            paths_doc=["Route53:GetDNSSEC"],
        )
    if "route53-resolver" in a and ("resolver" in a or "firewall" in a or "df" in a):
        return SignalSpec(
            fields=["resolverRules[].ruleId"],
            predicate="resolverRules.length >= 0",
            paths_doc=["Route53Resolver:ListResolverRules"],
        )

    # Shield Advanced
    if "shield.advanced_protection" in a or "shield.protection_enabled" in a:
        return SignalSpec(
            fields=["subscription.active", "protections[].resourceArn"],
            predicate="subscription.active === true",
            paths_doc=["Shield:DescribeSubscription", "Shield:ListProtections"],
        )

    # ECR
    if "ecr.image_scanning" in a or "ecr.image_vulnerability_scanning" in a or "inspector2.container_scanning" in a:
        return SignalSpec(
            fields=["scanningConfiguration.scanOnPush", "findings.severityCounts"],
            predicate="scanningConfiguration.scanOnPush === true",
            paths_doc=["ECR:GetRegistryScanningConfiguration", "ECR:DescribeImageScanFindings"],
        )
    if "ecr.image_signing" in a or "ecr.signed_images" in a:
        return SignalSpec(
            fields=["signatures[].signatureArn"],
            predicate="signatures.length >= 0",
            paths_doc=["ECR:ListImages + Notary V2 metadata"]
        )
    if "ecr.lifecycle_policies" in a or "ecr.repository_policy" in a or "ecr.repository_policies" in a or "ecr.registry_security" in a:
        return SignalSpec(
            fields=["lifecyclePolicyText", "policyText"],
            predicate="true === true",
            paths_doc=["ECR:GetLifecyclePolicy", "ECR:GetRepositoryPolicy"],
        )

    # EKS (logging etc.)
    if "eks.cluster_logging" in a:
        return SignalSpec(
            fields=["cluster.logging.enabledTypes[]"],
            predicate="cluster.logging.enabledTypes.includes('audit') && cluster.logging.enabledTypes.includes('api')",
            paths_doc=["EKS:DescribeCluster -> logging"],
        )
    if "eks.runtime_security" in a or "eks.network_policies" in a or "eks.rbac_configuration" in a or "eks.admission_controllers" in a or "eks.oidc_identity_provider" in a or "eks.version_management" in a or "eks.cluster_encryption" in a or "eks.node_security" in a or "eks.nodegroup_security" in a:
        return SignalSpec(
            fields=["addons[].name", "cluster.logging", "encryptionConfig.kmsKeyId"],
            predicate="encryptionConfig.kmsKeyId != null",
            paths_doc=["EKS:DescribeCluster -> logging, encryptionConfig", "EKS:ListAddons"],
        )

    # ECS / Fargate
    if "ecs.task_definition" in a or "ecs.service_configuration" in a or "ecs.vulnerability_scanning" in a:
        return SignalSpec(
            fields=["taskDefinition.executionRoleArn", "taskDefinition.networkMode"],
            predicate="taskDefinition.executionRoleArn != null",
            paths_doc=["ECS:DescribeTaskDefinition"],
        )
    if "eks.fargate_security" in a or "fargate" in a:
        return SignalSpec(
            fields=["fargateProfileArn"],
            predicate="fargateProfileArn != null",
            paths_doc=["EKS:ListFargateProfiles"],
        )

    # CloudWatch insights / logs / metrics
    if "cloudwatch.insights_queries" in a:
        return SignalSpec(
            fields=["queryDefinitions[].name"],
            predicate="queryDefinitions.length >= 0",
            paths_doc=["CloudWatchLogs:DescribeQueryDefinitions"],
        )

    # Backup
    if "backup.vault_policies" in a or "backup.backup_strategy" in a or "backup.backup_plans" in a or "backup.backup_selections" in a or "backup.disaster_recovery" in a or "backup.immutable_vault" in a:
        return SignalSpec(
            fields=["backupVaultArn", "policy", "lockConfiguration"],
            predicate="backupVaultArn != null",
            paths_doc=["Backup:ListBackupVaults", "Backup:DescribeBackupVault"],
        )

    # EFS / FSx
    if "efs.encryption_at_rest" in a or "efs.backup_policies" in a or "efs.access_points" in a:
        return SignalSpec(
            fields=["encrypted", "backupPolicy.status"],
            predicate="encrypted === true",
            paths_doc=["EFS:DescribeFileSystems", "EFS:DescribeBackupPolicy"],
        )
    if "fsx.access_control" in a:
        return SignalSpec(
            fields=["administrativeActions[]"],
            predicate="administrativeActions.length >= 0",
            paths_doc=["FSx:DescribeFileSystems"],
        )

    # Kinesis / Firehose / MQ / Kafka
    if "kinesis.stream_encryption" in a or "firehose.delivery_stream_encryption" in a or "mq.broker_encryption" in a or "kafka.cluster_encryption" in a or "dynamodbstreams.stream_encryption" in a:
        return SignalSpec(
            fields=["encryption.type", "encryption.kmsKeyId"],
            predicate="encryption.type != null",
            paths_doc=["Kinesis:DescribeStreamSummary", "Firehose:DescribeDeliveryStream", "MQ:DescribeBroker", "Kafka:DescribeCluster"],
        )

    # SQS
    if "sqs.queue_encryption" in a or "sqs.queue_security" in a:
        return SignalSpec(
            fields=["kmsMasterKeyId", "sseEnabled"],
            predicate="kmsMasterKeyId != null || sseEnabled === true",
            paths_doc=["SQS:GetQueueAttributes -> KmsMasterKeyId, SSE"],
        )

    # Redshift
    if "redshift.cluster_encryption" in a or "redshift.ssl_enforcement" in a:
        return SignalSpec(
            fields=["encrypted", "kmsKeyId", "requireSSL"],
            predicate="encrypted === true && (requireSSL === true || compareTls(params.minTlsVersion, 'TLS1_2') <= 0)",
            paths_doc=["Redshift:DescribeClusters", "Redshift:DescribeClusterParameters"],
        )

    # GuardDuty / SecurityHub / Detective / Macie
    if "guardduty.threat_detection" in a:
        return SignalSpec(
            fields=["detector.status"],
            predicate="detector.status === 'ENABLED'",
            paths_doc=["GuardDuty:ListDetectors", "GuardDuty:GetDetector"],
        )
    if "securityhub.findings" in a or "security_hub.findings" in a:
        return SignalSpec(
            fields=["standardsSubscriptionArn", "findings[].id"],
            predicate="true === true",
            paths_doc=["SecurityHub:GetFindings", "SecurityHub:GetEnabledStandards"],
        )
    if "securityhub.standards" in a or "security_hub.compliance_standards" in a or "security_hub.compliance_frameworks" in a:
        return SignalSpec(
            fields=["standards[].standardsArn"],
            predicate="standards.length >= 0",
            paths_doc=["SecurityHub:GetEnabledStandards"],
        )
    if "detective.graph_enabled" in a or "detective.findings" in a or "detective.threat_detection" in a:
        return SignalSpec(
            fields=["graphArn"],
            predicate="graphArn != null",
            paths_doc=["Detective:ListGraphs"],
        )
    if "macie" in a:
        return SignalSpec(
            fields=["macieStatus", "classificationJobs[].jobId"],
            predicate="macieStatus === 'ENABLED'",
            paths_doc=["Macie2:GetMacieSession", "Macie2:ListClassificationJobs"],
        )

    # Organizations / Tagging / Budgets / Cost Explorer
    if "tag.tag_policies" in a or "tag.resource_tagging_enforcement" in a:
        return SignalSpec(
            fields=["tagPoliciesEnabled", "policies[].id"],
            predicate="tagPoliciesEnabled === true",
            paths_doc=["Organizations:ListPolicies(Type=TAG_POLICY)", "Organizations:ListPoliciesForTarget"],
        )
    if "organizations.policy_management" in a or "organizations.scp_exceptions" in a or "organizations.resource_governance" in a:
        return SignalSpec(
            fields=["policies[].id"],
            predicate="policies.length >= 0",
            paths_doc=["Organizations:ListPolicies", "Organizations:ListPoliciesForTarget"],
        )
    if "budgets.cost_governance" in a or "budgets.cost_anomaly_detection" in a:
        return SignalSpec(
            fields=["budgets[].budgetName"],
            predicate="budgets.length >= 0",
            paths_doc=["Budgets:DescribeBudgets"],
        )
    if "cost_explorer" in a:
        return SignalSpec(
            fields=["reports[].name"],
            predicate="reports.length >= 0",
            paths_doc=["CE:GetCostAndUsageReports or CostExplorer APIs"],
        )

    # Lambda secret management (env enc)
    if "lambda.environment_encryption" in a:
        return SignalSpec(
            fields=["kmsKeyArn"],
            predicate="kmsKeyArn != null",
            paths_doc=["Lambda:GetFunctionConfiguration -> KMSKeyArn"],
        )

    # EC2 instance lifecycle
    if "ec2.instance_lifecycle" in a:
        return SignalSpec(
            fields=["disableApiTermination", "instanceInitiatedShutdownBehavior"],
            predicate="disableApiTermination === true",
            paths_doc=["EC2:DescribeInstances -> DisableApiTermination, InstanceInitiatedShutdownBehavior"],
        )

    # Default fallback
    return SignalSpec(
        fields=["compliant", "details"],
        predicate="compliant === true",
        paths_doc=[f"{service.upper()}:Describe* or Get* for {resource_type}"],
    )


# --- Matrix flattening ---

def flatten_matrix(matrix: Dict[str, Any]) -> List[Tuple[str, str, Dict[str, Any]]]:
    items: List[Tuple[str, str, Dict[str, Any]]] = []
    for domain_subcat, value in matrix.items():
        if "." in domain_subcat:
            domain_key, subcat_id = domain_subcat.split(".", 1)
        else:
            domain_key, subcat_id = domain_subcat, ""
        # The AWS matrix here appears to be a list (no tier buckets). Support both.
        if isinstance(value, list):
            for entry in value:
                e = dict(entry)
                if "coverage_tier" not in e:
                    e["coverage_tier"] = "core"
                items.append((domain_key, subcat_id, e))
        elif isinstance(value, dict):
            for coverage_tier, entries in value.items():
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    e = dict(entry)
                    e["coverage_tier"] = coverage_tier
                    items.append((domain_key, subcat_id, e))
    return items


# --- Enrichment ---

def enrich_entry(domain_key: str, subcat_id: str, entry: Dict[str, Any], assertions_by_key: Dict[Tuple[str, str], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    # Preserve existing
    service = entry.get("service") or ""
    resource = entry.get("resource") or ""
    resource_type = entry.get("resource_type") or resource
    adapter = entry.get("adapter") or entry.get("adapter_id") or ""
    coverage_tier = entry.get("coverage_tier") or "core"
    not_applicable_when = entry.get("not_applicable_when")

    # Expanded atomic splits
    split_adapters: Dict[str, List[Tuple[str, str]]] = {
        # IAM MFA
        "aws.iam.user_mfa_status": [
            ("mfa_enforced", "mfaRequired === true"),
            ("mfa_device_present", "mfaDevicesRegistered >= 1"),
        ],
        # ELBv2 TLS
        "aws.elbv2.ssl_certificates": [
            ("https_listeners_only", "listeners.every(l => l.protocol === 'HTTPS')"),
            ("tls_policy_minimum", "listeners.every(l => compareTls(l.sslPolicy, params.minTlsPolicy) >= 0)"),
        ],
        # S3 PAB flags
        "aws.s3.public_access_block": [
            ("block_public_acls", "blockPublicAcls === true"),
            ("ignore_public_acls", "ignorePublicAcls === true"),
            ("block_public_policy", "blockPublicPolicy === true"),
            ("restrict_public_buckets", "restrictPublicBuckets === true"),
        ],
        # CloudTrail collection facets
        "aws.cloudtrail.log_collection": [
            ("enabled", "trail.enabled === true"),
            ("multi_region", "trail.multiRegion === true"),
            ("log_file_validation", "trail.logFileValidation === true"),
        ],
        "aws.cloudtrail.audit_logging": [
            ("enabled", "trail.enabled === true"),
            ("multi_region", "trail.multiRegion === true"),
            ("log_file_validation", "trail.logFileValidation === true"),
        ],
        # CloudTrail retention vs integrity
        "aws.cloudtrail.log_retention": [
            ("retention_threshold", "destination.retentionDays >= params.minRetentionDays"),
        ],
        "aws.cloudtrail.log_integrity": [
            ("s3_object_lock", "destination.bucketObjectLock.enabled === true"),
        ],
        "aws.cloudtrail.s3_object_lock": [
            ("s3_object_lock", "destination.bucketObjectLock.enabled === true"),
        ],
        # AWS Config enablement facets
        "aws.config.compliance_rules": [
            ("recorder_enabled", "recorder.enabled === true"),
            ("delivery_channel", "delivery.channelConfigured === true"),
            ("rules_present", "rules.count >= 1"),
        ],
        "aws.config.audit_rules": [
            ("recorder_enabled", "recorder.enabled === true"),
            ("delivery_channel", "delivery.channelConfigured === true"),
            ("rules_present", "rules.count >= 1"),
        ],
        "aws.config.deprecation_rules": [
            ("recorder_enabled", "recorder.enabled === true"),
            ("delivery_channel", "delivery.channelConfigured === true"),
            ("rules_present", "rules.count >= 1"),
        ],
    }

    params = pick_params_for(domain_key, subcat_id, assertions_by_key)

    def build_row(name_suffix: Optional[str] = None, predicate_override: Optional[str] = None) -> Dict[str, Any]:
        sig = signal_from_adapter(adapter, service, resource_type)
        predicate = predicate_override or sig.predicate
        signal = {
            "fields": sig.fields,
            "predicate": predicate,
            "paths_doc": sig.paths_doc,
            "evidence_type": "config_read",
        }
        row: Dict[str, Any] = {
            "service": service,
            "resource": resource,
            "resource_type": resource_type,
            "adapter": adapter if not name_suffix else f"{adapter}#{name_suffix}",
            "coverage_tier": coverage_tier,
            "not_applicable_when": not_applicable_when,
            "params": params or {},
            "signal": signal,
        }
        # Keep any unknown extras (but avoid overriding our keys)
        for k, v in entry.items():
            if k not in row:
                row[k] = v
        return row

    # Apply split if configured
    key = adapter
    rows: List[Dict[str, Any]] = []
    if key in split_adapters:
        for suffix, pred in split_adapters[key]:
            rows.append(build_row(name_suffix=suffix, predicate_override=pred))
        return rows

    rows.append(build_row())
    return rows


def inject_missing_atomic_rows(enriched: Dict[str, List[Dict[str, Any]]]) -> int:
    added = 0
    def add(domain_subcat: str, row: Dict[str, Any]) -> None:
        nonlocal added
        enriched.setdefault(domain_subcat, []).append(row)
        added += 1

    # 1) governance_compliance.tagging
    if "governance_compliance.tagging" not in enriched:
        add("governance_compliance.tagging", {
            "service": "tag",
            "resource": "platform.control_plane",
            "resource_type": "platform.control_plane",
            "adapter": "aws.tag.resource_tagging_enforcement",
            "coverage_tier": "core",
            "not_applicable_when": "not_using_organizations",
            "params": {},
            "signal": {
                "fields": ["tagPoliciesEnabled", "policies[].id"],
                "predicate": "tagPoliciesEnabled === true",
                "paths_doc": ["Organizations:ListPolicies(Type=TAG_POLICY)", "Organizations:ListPoliciesForTarget"],
                "evidence_type": "config_read"
            }
        })
    # 2) serverless_paas.secret_management
    if "serverless_paas.secret_management" not in enriched:
        add("serverless_paas.secret_management", {
            "service": "lambda",
            "resource": "serverless.function",
            "resource_type": "serverless.function",
            "adapter": "aws.lambda.environment_encryption",
            "coverage_tier": "core",
            "not_applicable_when": "no_lambda_functions",
            "params": {},
            "signal": {
                "fields": ["kmsKeyArn"],
                "predicate": "kmsKeyArn != null",
                "paths_doc": ["Lambda:GetFunctionConfiguration -> KMSKeyArn"],
                "evidence_type": "config_read"
            }
        })
    # 3) containers_kubernetes.logging
    if "containers_kubernetes.logging" not in enriched:
        add("containers_kubernetes.logging", {
            "service": "eks",
            "resource": "k8s.cluster",
            "resource_type": "k8s.cluster",
            "adapter": "aws.eks.cluster_logging",
            "coverage_tier": "core",
            "not_applicable_when": "no_eks_clusters",
            "params": {},
            "signal": {
                "fields": ["cluster.logging.enabledTypes[]"],
                "predicate": "cluster.logging.enabledTypes.includes('audit') && cluster.logging.enabledTypes.includes('api')",
                "paths_doc": ["EKS:DescribeCluster -> logging"],
                "evidence_type": "config_read"
            }
        })
    # 4) compute_host_security.instance_lifecycle
    if "compute_host_security.instance_lifecycle" not in enriched:
        add("compute_host_security.instance_lifecycle", {
            "service": "ec2",
            "resource": "compute.vm",
            "resource_type": "compute.vm",
            "adapter": "aws.ec2.instance_lifecycle",
            "coverage_tier": "core",
            "not_applicable_when": "no_ec2_instances",
            "params": {},
            "signal": {
                "fields": ["disableApiTermination", "instanceInitiatedShutdownBehavior"],
                "predicate": "disableApiTermination === true",
                "paths_doc": ["EC2:DescribeInstances -> DisableApiTermination, InstanceInitiatedShutdownBehavior"],
                "evidence_type": "config_read"
            }
        })
    # 5) data_protection_storage.storage_lifecycle
    if "data_protection_storage.storage_lifecycle" not in enriched:
        add("data_protection_storage.storage_lifecycle", {
            "service": "s3",
            "resource": "storage.bucket",
            "resource_type": "storage.bucket",
            "adapter": "aws.s3.lifecycle_management",
            "coverage_tier": "core",
            "not_applicable_when": "no_s3_buckets",
            "params": {},
            "signal": {
                "fields": ["lifecycle.rules[].status"],
                "predicate": "lifecycle.rules.length >= 1",
                "paths_doc": ["S3:GetBucketLifecycleConfiguration"],
                "evidence_type": "config_read"
            }
        })

    return added


def enrich_matrix() -> Dict[str, Any]:
    matrix = load_json(AWS_MATRIX_PATH)
    assertions_root = load_json(ASSERTIONS_PATH)
    assertions_by_key = index_assertions_by_domain_subcat(assertions_root)

    items = flatten_matrix(matrix)

    enriched: Dict[str, List[Dict[str, Any]]] = {}
    total_out = 0

    for domain_key, subcat_id, entry in items:
        out_rows = enrich_entry(domain_key, subcat_id, entry, assertions_by_key)
        total_out += len(out_rows)
        domain_subcat = f"{domain_key}.{subcat_id}" if subcat_id else domain_key
        enriched.setdefault(domain_subcat, []).extend(out_rows)

    # Inject the five missing taxonomy subcats with atomic rows
    added = inject_missing_atomic_rows(enriched)
    total_out += added

    return {
        "provider": "aws",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_matrix": os.path.basename(AWS_MATRIX_PATH),
        "source_assertions": os.path.basename(ASSERTIONS_PATH),
        "total_rows": total_out,
        "matrix": enriched,
    }


def main() -> None:
    data = enrich_matrix()
    save_json(OUTPUT_PATH, data)
    print(f"Wrote enriched AWS matrix with {data['total_rows']} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
