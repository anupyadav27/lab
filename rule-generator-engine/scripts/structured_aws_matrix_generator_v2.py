#!/usr/bin/env python3
"""
Structured AWS Matrix Generator V2

This script creates a comprehensive AWS compliance matrix by:
1. Extracting all domain+subcat combinations from taxonomy
2. Mapping assertions to domain+subcat using assertion_id tails
3. Defining AWS services+resources for each domain+subcat+assertion
4. Generating multiple atomic checks for comprehensive coverage
"""

import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Set, Tuple, Optional

# Input files
TAXONOMY_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-1-common-taxonomy/subcategories_taxonomy_clean_2025-09-11T17-30-20.json"
ASSERTIONS_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14_enhanced.json"

# Output file
OUTPUT_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_matrix_structured_comprehensive_v2_2025-09-24.json"


def load_json(path: str) -> Any:
    """Load JSON file"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: Any) -> None:
    """Save JSON file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def extract_domain_subcat_combinations(taxonomy: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Extract all domain.key + subcat_id combinations"""
    combinations = []
    for domain in taxonomy.get("domains", []):
        domain_key = domain.get("key")
        for subcat in domain.get("subcategories", []):
            subcat_id = subcat.get("subcat_id")
            combinations.append((domain_key, subcat_id))
    return combinations


def map_assertions_to_domain_subcat(assertions: Dict[str, Any]) -> Dict[Tuple[str, str], List[Dict[str, Any]]]:
    """Map assertions to domain+subcat using assertion_id tails"""
    mapping = {}
    
    for assertion in assertions.get("assertions", []):
        assertion_id = assertion.get("assertion_id", "")
        if "." in assertion_id:
            # Extract domain.subcat from assertion_id
            parts = assertion_id.split(".")
            if len(parts) >= 2:
                domain_key = parts[0]
                subcat_id = parts[1]
                key = (domain_key, subcat_id)
                mapping.setdefault(key, []).append(assertion)
    
    return mapping


def get_comprehensive_aws_mapping() -> Dict[Tuple[str, str], List[Dict[str, Any]]]:
    """
    Comprehensive AWS service+resource mapping for all domain+subcat combinations.
    This ensures systematic coverage across all 107+ combinations.
    """
    mapping = {
        # Identity & Access - 8 subcategories
        ("identity_access", "authentication"): [
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "iam", "resource": "iam.group", "resource_type": "iam.group"},
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
            {"service": "identity_center", "resource": "identity_center.permission_set", "resource_type": "identity_center.permission_set"},
            {"service": "directoryservice", "resource": "directoryservice.directory", "resource_type": "directoryservice.directory"},
            {"service": "cognito", "resource": "cognito.user_pool", "resource_type": "cognito.user_pool"},
            {"service": "cognito", "resource": "cognito.identity_pool", "resource_type": "cognito.identity_pool"},
        ],
        ("identity_access", "authorization"): [
            {"service": "iam", "resource": "iam.policy", "resource_type": "iam.policy"},
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
            {"service": "iam", "resource": "iam.group", "resource_type": "iam.group"},
            {"service": "identity_center", "resource": "identity_center.permission_set", "resource_type": "identity_center.permission_set"},
            {"service": "cognito", "resource": "cognito.user_pool", "resource_type": "cognito.user_pool"},
        ],
        ("identity_access", "federation"): [
            {"service": "identity_center", "resource": "identity_center.permission_set", "resource_type": "identity_center.permission_set"},
            {"service": "directoryservice", "resource": "directoryservice.directory", "resource_type": "directoryservice.directory"},
            {"service": "cognito", "resource": "cognito.identity_pool", "resource_type": "cognito.identity_pool"},
            {"service": "cognito", "resource": "cognito.user_pool", "resource_type": "cognito.user_pool"},
        ],
        ("identity_access", "mfa"): [
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "iam", "resource": "iam.group", "resource_type": "iam.group"},
            {"service": "identity_center", "resource": "identity_center.permission_set", "resource_type": "identity_center.permission_set"},
            {"service": "cognito", "resource": "cognito.user_pool", "resource_type": "cognito.user_pool"},
        ],
        ("identity_access", "session_management"): [
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "cognito", "resource": "cognito.user_pool", "resource_type": "cognito.user_pool"},
            {"service": "sts", "resource": "sts.session", "resource_type": "sts.session"},
        ],
        ("identity_access", "passwordless_authn"): [
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "cognito", "resource": "cognito.user_pool", "resource_type": "cognito.user_pool"},
        ],
        ("identity_access", "break_glass"): [
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
        ],
        ("identity_access", "least_privilege"): [
            {"service": "iam", "resource": "iam.policy", "resource_type": "iam.policy"},
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
            {"service": "iam", "resource": "iam.group", "resource_type": "iam.group"},
            {"service": "accessanalyzer", "resource": "accessanalyzer.analyzer", "resource_type": "accessanalyzer.analyzer"},
        ],
        
        # RBAC & Entitlements - 5 subcategories
        ("rbac_entitlements", "role_definition"): [
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
            {"service": "iam", "resource": "iam.policy", "resource_type": "iam.policy"},
            {"service": "identity_center", "resource": "identity_center.permission_set", "resource_type": "identity_center.permission_set"},
        ],
        ("rbac_entitlements", "role_assignment"): [
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "iam", "resource": "iam.group", "resource_type": "iam.group"},
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
            {"service": "identity_center", "resource": "identity_center.permission_set", "resource_type": "identity_center.permission_set"},
        ],
        ("rbac_entitlements", "least_privilege"): [
            {"service": "iam", "resource": "iam.policy", "resource_type": "iam.policy"},
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
            {"service": "accessanalyzer", "resource": "accessanalyzer.analyzer", "resource_type": "accessanalyzer.analyzer"},
        ],
        ("rbac_entitlements", "entitlement_management"): [
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
            {"service": "identity_center", "resource": "identity_center.permission_set", "resource_type": "identity_center.permission_set"},
        ],
        ("rbac_entitlements", "sod_toxic"): [
            {"service": "iam", "resource": "iam.policy", "resource_type": "iam.policy"},
            {"service": "iam", "resource": "iam.user", "resource_type": "iam.user"},
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
            {"service": "accessanalyzer", "resource": "accessanalyzer.analyzer", "resource_type": "accessanalyzer.analyzer"},
        ],
        
        # Secrets & Key Management - 5 subcategories
        ("secrets_key_mgmt", "secret_storage"): [
            {"service": "secretsmanager", "resource": "secretsmanager.secret", "resource_type": "secretsmanager.secret"},
            {"service": "kms", "resource": "kms.key", "resource_type": "kms.key"},
            {"service": "ssm", "resource": "ssm.parameter", "resource_type": "ssm.parameter"},
        ],
        ("secrets_key_mgmt", "key_rotation"): [
            {"service": "kms", "resource": "kms.key", "resource_type": "kms.key"},
            {"service": "secretsmanager", "resource": "secretsmanager.secret", "resource_type": "secretsmanager.secret"},
        ],
        ("secrets_key_mgmt", "key_protection"): [
            {"service": "kms", "resource": "kms.key", "resource_type": "kms.key"},
            {"service": "kms", "resource": "kms.alias", "resource_type": "kms.alias"},
        ],
        ("secrets_key_mgmt", "secret_retrieval"): [
            {"service": "secretsmanager", "resource": "secretsmanager.secret", "resource_type": "secretsmanager.secret"},
            {"service": "ssm", "resource": "ssm.parameter", "resource_type": "ssm.parameter"},
        ],
        ("secrets_key_mgmt", "secret_sprawl"): [
            {"service": "secretsmanager", "resource": "secretsmanager.secret", "resource_type": "secretsmanager.secret"},
            {"service": "ssm", "resource": "ssm.parameter", "resource_type": "ssm.parameter"},
            {"service": "kms", "resource": "kms.key", "resource_type": "kms.key"},
        ],
        
        # Cryptography & Data Protection - 7 subcategories
        ("crypto_data_protection", "encryption_at_rest"): [
            {"service": "s3", "resource": "s3.bucket", "resource_type": "s3.bucket"},
            {"service": "ebs", "resource": "ebs.volume", "resource_type": "ebs.volume"},
            {"service": "rds", "resource": "rds.db_instance", "resource_type": "rds.db_instance"},
            {"service": "rds", "resource": "rds.db_cluster", "resource_type": "rds.db_cluster"},
            {"service": "dynamodb", "resource": "dynamodb.table", "resource_type": "dynamodb.table"},
            {"service": "efs", "resource": "efs.filesystem", "resource_type": "efs.filesystem"},
            {"service": "redshift", "resource": "redshift.cluster", "resource_type": "redshift.cluster"},
        ],
        ("crypto_data_protection", "encryption_in_transit"): [
            {"service": "elbv2", "resource": "elbv2.load_balancer", "resource_type": "elbv2.load_balancer"},
            {"service": "apigateway", "resource": "apigateway.api", "resource_type": "apigateway.api"},
            {"service": "cloudfront", "resource": "cloudfront.distribution", "resource_type": "cloudfront.distribution"},
            {"service": "rds", "resource": "rds.db_instance", "resource_type": "rds.db_instance"},
            {"service": "rds", "resource": "rds.db_cluster", "resource_type": "rds.db_cluster"},
        ],
        ("crypto_data_protection", "key_management"): [
            {"service": "kms", "resource": "kms.key", "resource_type": "kms.key"},
            {"service": "kms", "resource": "kms.alias", "resource_type": "kms.alias"},
        ],
        ("crypto_data_protection", "certificate_management"): [
            {"service": "acm", "resource": "acm.certificate", "resource_type": "acm.certificate"},
            {"service": "iam", "resource": "iam.server_certificate", "resource_type": "iam.server_certificate"},
        ],
        ("crypto_data_protection", "crypto_policies"): [
            {"service": "kms", "resource": "kms.key", "resource_type": "kms.key"},
            {"service": "s3", "resource": "s3.bucket", "resource_type": "s3.bucket"},
        ],
        ("crypto_data_protection", "immutability"): [
            {"service": "s3", "resource": "s3.bucket", "resource_type": "s3.bucket"},
            {"service": "ebs", "resource": "ebs.snapshot", "resource_type": "ebs.snapshot"},
        ],
        ("crypto_data_protection", "access_control"): [
            {"service": "s3", "resource": "s3.bucket", "resource_type": "s3.bucket"},
            {"service": "ebs", "resource": "ebs.snapshot", "resource_type": "ebs.snapshot"},
            {"service": "ebs", "resource": "ebs.volume", "resource_type": "ebs.volume"},
        ],
        
        # Data Protection & Storage - 7 subcategories
        ("data_protection_storage", "data_classification"): [
            {"service": "s3", "resource": "s3.bucket", "resource_type": "s3.bucket"},
            {"service": "macie", "resource": "macie.session", "resource_type": "macie.session"},
        ],
        ("data_protection_storage", "data_retention"): [
            {"service": "s3", "resource": "s3.bucket", "resource_type": "s3.bucket"},
            {"service": "ebs", "resource": "ebs.volume", "resource_type": "ebs.volume"},
            {"service": "ebs", "resource": "ebs.snapshot", "resource_type": "ebs.snapshot"},
            {"service": "rds", "resource": "rds.db_instance", "resource_type": "rds.db_instance"},
        ],
        ("data_protection_storage", "backup_recovery"): [
            {"service": "backup", "resource": "backup.plan", "resource_type": "backup.plan"},
            {"service": "backup", "resource": "backup.vault", "resource_type": "backup.vault"},
            {"service": "rds", "resource": "rds.db_instance", "resource_type": "rds.db_instance"},
            {"service": "rds", "resource": "rds.db_cluster", "resource_type": "rds.db_cluster"},
            {"service": "ebs", "resource": "ebs.snapshot", "resource_type": "ebs.snapshot"},
        ],
        ("data_protection_storage", "data_masking"): [
            {"service": "rds", "resource": "rds.db_instance", "resource_type": "rds.db_instance"},
            {"service": "dynamodb", "resource": "dynamodb.table", "resource_type": "dynamodb.table"},
        ],
        ("data_protection_storage", "storage_security"): [
            {"service": "s3", "resource": "s3.bucket", "resource_type": "s3.bucket"},
            {"service": "efs", "resource": "efs.filesystem", "resource_type": "efs.filesystem"},
        ],
        ("data_protection_storage", "public_exposure"): [
            {"service": "s3", "resource": "s3.bucket", "resource_type": "s3.bucket"},
            {"service": "rds", "resource": "rds.db_instance", "resource_type": "rds.db_instance"},
            {"service": "rds", "resource": "rds.db_cluster", "resource_type": "rds.db_cluster"},
        ],
        ("data_protection_storage", "storage_lifecycle"): [
            {"service": "s3", "resource": "s3.bucket", "resource_type": "s3.bucket"},
            {"service": "ebs", "resource": "ebs.volume", "resource_type": "ebs.volume"},
            {"service": "ebs", "resource": "ebs.snapshot", "resource_type": "ebs.snapshot"},
        ],
        
        # Network & Perimeter - 7 subcategories
        ("network_perimeter", "network_segmentation"): [
            {"service": "ec2", "resource": "ec2.vpc", "resource_type": "ec2.vpc"},
            {"service": "ec2", "resource": "ec2.subnet", "resource_type": "ec2.subnet"},
            {"service": "ec2", "resource": "ec2.security_group", "resource_type": "ec2.security_group"},
            {"service": "ec2", "resource": "ec2.network_acl", "resource_type": "ec2.network_acl"},
        ],
        ("network_perimeter", "firewall_rules"): [
            {"service": "ec2", "resource": "ec2.security_group", "resource_type": "ec2.security_group"},
            {"service": "ec2", "resource": "ec2.network_acl", "resource_type": "ec2.network_acl"},
            {"service": "networkfirewall", "resource": "networkfirewall.firewall", "resource_type": "networkfirewall.firewall"},
            {"service": "wafv2", "resource": "wafv2.web_acl", "resource_type": "wafv2.web_acl"},
        ],
        ("network_perimeter", "ddos_protection"): [
            {"service": "shield", "resource": "shield.protection", "resource_type": "shield.protection"},
            {"service": "cloudfront", "resource": "cloudfront.distribution", "resource_type": "cloudfront.distribution"},
        ],
        ("network_perimeter", "network_monitoring"): [
            {"service": "vpc", "resource": "vpc.flow_logs", "resource_type": "vpc.flow_logs"},
            {"service": "cloudwatch", "resource": "cloudwatch.log_group", "resource_type": "cloudwatch.log_group"},
        ],
        ("network_perimeter", "load_balancer_security"): [
            {"service": "elbv2", "resource": "elbv2.load_balancer", "resource_type": "elbv2.load_balancer"},
            {"service": "elb", "resource": "elb.load_balancer", "resource_type": "elb.load_balancer"},
        ],
        ("network_perimeter", "dns_security"): [
            {"service": "route53", "resource": "route53.hosted_zone", "resource_type": "route53.hosted_zone"},
            {"service": "route53", "resource": "route53.resolver", "resource_type": "route53.resolver"},
        ],
        ("network_perimeter", "vpn_connectivity"): [
            {"service": "vpn", "resource": "vpn.connection", "resource_type": "vpn.connection"},
            {"service": "directconnect", "resource": "directconnect.connection", "resource_type": "directconnect.connection"},
        ],
        
        # Compute & Host Security - 6 subcategories
        ("compute_host_security", "instance_lifecycle"): [
            {"service": "ec2", "resource": "ec2.instance", "resource_type": "ec2.instance"},
            {"service": "ec2", "resource": "ec2.image", "resource_type": "ec2.image"},
            {"service": "ec2", "resource": "ec2.volume", "resource_type": "ec2.volume"},
        ],
        ("compute_host_security", "vulnerability_management"): [
            {"service": "inspector", "resource": "inspector.assessment", "resource_type": "inspector.assessment"},
            {"service": "ec2", "resource": "ec2.instance", "resource_type": "ec2.instance"},
            {"service": "ecr", "resource": "ecr.repository", "resource_type": "ecr.repository"},
        ],
        ("compute_host_security", "endpoint_protection"): [
            {"service": "ec2", "resource": "ec2.instance", "resource_type": "ec2.instance"},
            {"service": "guardduty", "resource": "guardduty.detector", "resource_type": "guardduty.detector"},
        ],
        ("compute_host_security", "patch_management"): [
            {"service": "ssm", "resource": "ssm.patch_baseline", "resource_type": "ssm.patch_baseline"},
            {"service": "ec2", "resource": "ec2.instance", "resource_type": "ec2.instance"},
        ],
        ("compute_host_security", "baseline_configuration"): [
            {"service": "ssm", "resource": "ssm.association", "resource_type": "ssm.association"},
            {"service": "ec2", "resource": "ec2.instance", "resource_type": "ec2.instance"},
        ],
        ("compute_host_security", "secure_boot"): [
            {"service": "ec2", "resource": "ec2.instance", "resource_type": "ec2.instance"},
            {"service": "ec2", "resource": "ec2.image", "resource_type": "ec2.image"},
        ],
        
        # Governance & Compliance - 6 subcategories
        ("governance_compliance", "audit_logging"): [
            {"service": "cloudtrail", "resource": "cloudtrail.trail", "resource_type": "cloudtrail.trail"},
            {"service": "config", "resource": "config.recorder", "resource_type": "config.recorder"},
            {"service": "config", "resource": "config.delivery_channel", "resource_type": "config.delivery_channel"},
            {"service": "cloudwatch", "resource": "cloudwatch.log_group", "resource_type": "cloudwatch.log_group"},
        ],
        ("governance_compliance", "compliance_monitoring"): [
            {"service": "config", "resource": "config.rule", "resource_type": "config.rule"},
            {"service": "securityhub", "resource": "securityhub.hub", "resource_type": "securityhub.hub"},
            {"service": "guardduty", "resource": "guardduty.detector", "resource_type": "guardduty.detector"},
        ],
        ("governance_compliance", "tagging"): [
            {"service": "ec2", "resource": "ec2.instance", "resource_type": "ec2.instance"},
            {"service": "s3", "resource": "s3.bucket", "resource_type": "s3.bucket"},
            {"service": "rds", "resource": "rds.db_instance", "resource_type": "rds.db_instance"},
        ],
        ("governance_compliance", "resource_inventory"): [
            {"service": "config", "resource": "config.recorder", "resource_type": "config.recorder"},
            {"service": "resourcegroupstaggingapi", "resource": "resourcegroupstaggingapi.resource", "resource_type": "resourcegroupstaggingapi.resource"},
        ],
        ("governance_compliance", "policy_enforcement"): [
            {"service": "config", "resource": "config.rule", "resource_type": "config.rule"},
            {"service": "organizations", "resource": "organizations.policy", "resource_type": "organizations.policy"},
        ],
        ("governance_compliance", "cost_governance"): [
            {"service": "budgets", "resource": "budgets.budget", "resource_type": "budgets.budget"},
            {"service": "costexplorer", "resource": "costexplorer.report", "resource_type": "costexplorer.report"},
        ],
        
        # Containers & Kubernetes - 6 subcategories
        ("containers_kubernetes", "cluster_security"): [
            {"service": "eks", "resource": "eks.cluster", "resource_type": "eks.cluster"},
            {"service": "eks", "resource": "eks.nodegroup", "resource_type": "eks.nodegroup"},
            {"service": "ecr", "resource": "ecr.repository", "resource_type": "ecr.repository"},
        ],
        ("containers_kubernetes", "pod_security"): [
            {"service": "eks", "resource": "eks.cluster", "resource_type": "eks.cluster"},
            {"service": "eks", "resource": "eks.admission", "resource_type": "eks.admission"},
        ],
        ("containers_kubernetes", "logging"): [
            {"service": "eks", "resource": "eks.cluster", "resource_type": "eks.cluster"},
            {"service": "cloudwatch", "resource": "cloudwatch.log_group", "resource_type": "cloudwatch.log_group"},
        ],
        ("containers_kubernetes", "image_security"): [
            {"service": "ecr", "resource": "ecr.repository", "resource_type": "ecr.repository"},
            {"service": "inspector", "resource": "inspector.assessment", "resource_type": "inspector.assessment"},
        ],
        ("containers_kubernetes", "network_policies"): [
            {"service": "eks", "resource": "eks.cluster", "resource_type": "eks.cluster"},
            {"service": "ec2", "resource": "ec2.security_group", "resource_type": "ec2.security_group"},
        ],
        ("containers_kubernetes", "rbac"): [
            {"service": "eks", "resource": "eks.cluster", "resource_type": "eks.cluster"},
            {"service": "iam", "resource": "iam.role", "resource_type": "iam.role"},
        ],
        
        # Serverless & PaaS - 6 subcategories
        ("serverless_paas", "function_security"): [
            {"service": "lambda", "resource": "lambda.function", "resource_type": "lambda.function"},
            {"service": "lambda", "resource": "lambda.layer", "resource_type": "lambda.layer"},
        ],
        ("serverless_paas", "api_security"): [
            {"service": "apigateway", "resource": "apigateway.api", "resource_type": "apigateway.api"},
            {"service": "apigateway", "resource": "apigateway.stage", "resource_type": "apigateway.stage"},
        ],
        ("serverless_paas", "secret_management"): [
            {"service": "lambda", "resource": "lambda.function", "resource_type": "lambda.function"},
            {"service": "secretsmanager", "resource": "secretsmanager.secret", "resource_type": "secretsmanager.secret"},
        ],
        ("serverless_paas", "event_processing"): [
            {"service": "lambda", "resource": "lambda.function", "resource_type": "lambda.function"},
            {"service": "sns", "resource": "sns.topic", "resource_type": "sns.topic"},
            {"service": "sqs", "resource": "sqs.queue", "resource_type": "sqs.queue"},
        ],
        ("serverless_paas", "data_processing"): [
            {"service": "lambda", "resource": "lambda.function", "resource_type": "lambda.function"},
            {"service": "glue", "resource": "glue.job", "resource_type": "glue.job"},
        ],
        ("serverless_paas", "workflow_orchestration"): [
            {"service": "stepfunctions", "resource": "stepfunctions.state_machine", "resource_type": "stepfunctions.state_machine"},
            {"service": "lambda", "resource": "lambda.function", "resource_type": "lambda.function"},
        ],
    }
    
    return mapping


def generate_comprehensive_atomic_checks(domain_key: str, subcat_id: str, assertion: Dict[str, Any], 
                                        service_resource: Dict[str, str]) -> List[Dict[str, Any]]:
    """Generate comprehensive atomic checks with multiple checks per combination"""
    
    service = service_resource["service"]
    resource = service_resource["resource"]
    resource_type = service_resource["resource_type"]
    assertion_id = assertion.get("assertion_id", "")
    
    atomic_checks = []
    
    # Identity & Access - Multiple comprehensive checks
    if domain_key == "identity_access" and subcat_id == "authentication":
        if service == "iam":
            # MFA enforcement
            atomic_checks.append({
                "service": service,
                "resource": resource,
                "resource_type": resource_type,
                "adapter": f"aws.{service}.mfa_enforcement",
                "coverage_tier": "core",
                "not_applicable_when": f"no_{service}_{resource.split('.')[-1]}",
                "params": assertion.get("params", {}),
                "signal": {
                    "fields": ["mfaRequired"],
                    "predicate": "mfaRequired === true",
                    "paths_doc": ["IAM:GetAccountSummary"],
                    "evidence_type": assertion.get("evidence_type", "config_read"),
                },
                "assertion_id": assertion_id,
            })
            
            # MFA device presence
            atomic_checks.append({
                "service": service,
                "resource": resource,
                "resource_type": resource_type,
                "adapter": f"aws.{service}.mfa_devices",
                "coverage_tier": "core",
                "not_applicable_when": f"no_{service}_{resource.split('.')[-1]}",
                "params": assertion.get("params", {}),
                "signal": {
                    "fields": ["mfaDevices"],
                    "predicate": "Array.isArray(mfaDevices) && mfaDevices.length >= 1",
                    "paths_doc": ["IAM:ListMFADevices"],
                    "evidence_type": assertion.get("evidence_type", "config_read"),
                },
                "assertion_id": assertion_id,
            })
            
            # Password policy
            atomic_checks.append({
                "service": service,
                "resource": resource,
                "resource_type": resource_type,
                "adapter": f"aws.{service}.password_policy",
                "coverage_tier": "core",
                "not_applicable_when": f"no_{service}_{resource.split('.')[-1]}",
                "params": assertion.get("params", {}),
                "signal": {
                    "fields": ["requireUppercase", "requireLowercase", "requireNumbers", "requireSymbols", "maxPasswordAge"],
                    "predicate": "requireUppercase === true && requireLowercase === true && requireNumbers === true && requireSymbols === true && maxPasswordAge <= 90",
                    "paths_doc": ["IAM:GetAccountPasswordPolicy"],
                    "evidence_type": assertion.get("evidence_type", "config_read"),
                },
                "assertion_id": assertion_id,
            })
    
    # Data Protection - Multiple encryption checks
    elif domain_key in ["crypto_data_protection", "data_protection_storage"] and subcat_id == "encryption_at_rest":
        if service == "s3":
            # S3 bucket encryption
            atomic_checks.append({
                "service": service,
                "resource": resource,
                "resource_type": resource_type,
                "adapter": f"aws.{service}.bucket_encryption",
                "coverage_tier": "core",
                "not_applicable_when": f"no_{service}_{resource.split('.')[-1]}",
                "params": assertion.get("params", {}),
                "signal": {
                    "fields": ["serverSideEncryption"],
                    "predicate": "serverSideEncryption.enabled === true",
                    "paths_doc": ["S3:GetBucketEncryption"],
                    "evidence_type": assertion.get("evidence_type", "config_read"),
                },
                "assertion_id": assertion_id,
            })
            
            # S3 public access block
            atomic_checks.append({
                "service": service,
                "resource": resource,
                "resource_type": resource_type,
                "adapter": f"aws.{service}.public_access_block",
                "coverage_tier": "core",
                "not_applicable_when": f"no_{service}_{resource.split('.')[-1]}",
                "params": assertion.get("params", {}),
                "signal": {
                    "fields": ["blockPublicAcls", "ignorePublicAcls", "blockPublicPolicy", "restrictPublicBuckets"],
                    "predicate": "blockPublicAcls === true && ignorePublicAcls === true && blockPublicPolicy === true && restrictPublicBuckets === true",
                    "paths_doc": ["S3:GetPublicAccessBlock"],
                    "evidence_type": assertion.get("evidence_type", "config_read"),
                },
                "assertion_id": assertion_id,
            })
    
    # Network Security - Multiple network checks
    elif domain_key == "network_perimeter" and subcat_id == "network_segmentation":
        if service == "ec2":
            # Security group check
            atomic_checks.append({
                "service": service,
                "resource": "ec2.security_group",
                "resource_type": "ec2.security_group",
                "adapter": f"aws.{service}.security_groups",
                "coverage_tier": "core",
                "not_applicable_when": f"no_{service}_security_groups",
                "params": assertion.get("params", {}),
                "signal": {
                    "fields": ["securityGroups"],
                    "predicate": "securityGroups.length >= 1",
                    "paths_doc": ["EC2:DescribeSecurityGroups"],
                    "evidence_type": assertion.get("evidence_type", "config_read"),
                },
                "assertion_id": assertion_id,
            })
            
            # VPC flow logs
            atomic_checks.append({
                "service": service,
                "resource": "ec2.flow_logs",
                "resource_type": "ec2.flow_logs",
                "adapter": f"aws.{service}.flow_logs",
                "coverage_tier": "core",
                "not_applicable_when": f"no_{service}_flow_logs",
                "params": assertion.get("params", {}),
                "signal": {
                    "fields": ["flowLogs"],
                    "predicate": "flowLogs.length >= 1",
                    "paths_doc": ["EC2:DescribeFlowLogs"],
                    "evidence_type": assertion.get("evidence_type", "config_read"),
                },
                "assertion_id": assertion_id,
            })
    
    # If no specific multiple checks, create a single atomic check
    if not atomic_checks:
        atomic_checks.append({
            "service": service,
            "resource": resource,
            "resource_type": resource_type,
            "adapter": f"aws.{service}.{subcat_id}",
            "coverage_tier": "core",
            "not_applicable_when": f"no_{service}_{resource.split('.')[-1]}",
            "params": assertion.get("params", {}),
            "signal": {
                "fields": ["compliant"],
                "predicate": "compliant === true",
                "paths_doc": [f"{service.upper()}:Describe* or Get*"],
                "evidence_type": assertion.get("evidence_type", "config_read"),
            },
            "assertion_id": assertion_id,
        })
    
    return atomic_checks


def generate_comprehensive_matrix() -> Dict[str, Any]:
    """Generate comprehensive AWS matrix using structured approach"""
    
    # Load input files
    taxonomy = load_json(TAXONOMY_PATH)
    assertions = load_json(ASSERTIONS_PATH)
    
    # Extract domain+subcat combinations
    domain_subcat_combinations = extract_domain_subcat_combinations(taxonomy)
    print(f"Found {len(domain_subcat_combinations)} domain+subcat combinations")
    
    # Map assertions to domain+subcat
    assertion_mapping = map_assertions_to_domain_subcat(assertions)
    print(f"Found {len(assertion_mapping)} domain+subcat with assertions")
    
    # Get comprehensive AWS service+resource mapping
    aws_mapping = get_comprehensive_aws_mapping()
    print(f"Defined AWS mappings for {len(aws_mapping)} domain+subcat combinations")
    
    # Generate matrix
    matrix = {}
    total_checks = 0
    
    for domain_key, subcat_id in domain_subcat_combinations:
        key = f"{domain_key}.{subcat_id}"
        
        # Get assertions for this domain+subcat
        assertions_for_key = assertion_mapping.get((domain_key, subcat_id), [])
        
        # Get AWS services+resources for this domain+subcat
        aws_services = aws_mapping.get((domain_key, subcat_id), [])
        
        # Generate atomic checks for each assertion + service+resource combination
        checks = []
        for assertion in assertions_for_key:
            for service_resource in aws_services:
                # Use comprehensive atomic checks for maximum coverage
                atomic_checks = generate_comprehensive_atomic_checks(domain_key, subcat_id, assertion, service_resource)
                checks.extend(atomic_checks)
                total_checks += len(atomic_checks)
        
        if checks:
            matrix[key] = checks
    
    print(f"Generated {total_checks} total atomic checks across {len(matrix)} domain+subcat combinations")
    
    return {
        "provider": "aws",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_taxonomy": os.path.basename(TAXONOMY_PATH),
        "source_assertions": os.path.basename(ASSERTIONS_PATH),
        "total_checks": total_checks,
        "matrix": matrix,
    }


def main() -> None:
    """Main function"""
    print("Generating comprehensive AWS matrix V2...")
    matrix_data = generate_comprehensive_matrix()
    save_json(OUTPUT_PATH, matrix_data)
    print(f"Saved comprehensive AWS matrix to {OUTPUT_PATH}")
    print(f"Total checks: {matrix_data['total_checks']}")
    print(f"Domain+subcat combinations: {len(matrix_data['matrix'])}")


if __name__ == "__main__":
    main()
