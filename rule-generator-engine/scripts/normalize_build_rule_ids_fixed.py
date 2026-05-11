#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

INPUT_MATRIX_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_matrix_enriched_atomic_merged_2025-09-24.json"
ASSERTIONS_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14.json"
OUTPUT_PATH = \
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step4-rune-per-cloud-provider/aws_rules_with_ids_fixed_2025-09-24.json"


# --- Load/save helpers ---

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# --- High-impact fixes ---

def fix_placeholder_predicates(predicate: str, fields: List[str], service: str, adapter: str) -> str:
    """Replace placeholder predicates with field-level logic"""
    if predicate == "compliant === true":
        if "mfa" in adapter.lower():
            if "mfaDevices" in fields:
                return "Array.isArray(mfaDevices) && mfaDevices.length >= 1"
            if "mfaRequired" in fields:
                return "mfaRequired === true"
        if "password" in adapter.lower():
            if "requireUppercase" in fields:
                return "requireUppercase === true"
            if "requireLowercase" in fields:
                return "requireLowercase === true"
            if "requireNumbers" in fields:
                return "requireNumbers === true"
            if "requireSymbols" in fields:
                return "requireSymbols === true"
            if "maxPasswordAge" in fields:
                return "maxPasswordAge <= 90"
        if "encryption" in adapter.lower():
            if "encrypted" in fields:
                return "encrypted === true"
            if "serverSideEncryption" in fields:
                return "serverSideEncryption.enabled === true"
        if "public" in adapter.lower():
            if "blockPublicAcls" in fields:
                return "blockPublicAcls === true && blockPublicPolicy === true"
        if "tls" in adapter.lower() or "ssl" in adapter.lower():
            if "protocol" in fields:
                return "protocol === 'HTTPS'"
        if "rotation" in adapter.lower():
            if "rotationEnabled" in fields:
                return "rotationEnabled === true"
        if "logging" in adapter.lower():
            if "enabled" in fields:
                return "enabled === true"
        # Fallback for unknown cases
        if fields and fields[0] != "compliant":
            return f"{fields[0]} === true"
    return predicate


def fix_tautology_predicates(predicate: str, fields: List[str]) -> str:
    """Fix tautological predicates like 'count >= 0'"""
    if "count >= 0" in predicate:
        if "inlinePolicies" in fields:
            return "inlinePolicies.length === 0"
        if "attachedPolicies" in fields:
            return "attachedPolicies.length >= 1"
    if "length >= 0" in predicate:
        return predicate.replace("length >= 0", "length >= 1")
    return predicate


def normalize_tls_params(params: Dict[str, Any], predicate: str) -> Tuple[Dict[str, Any], str]:
    """Normalize TLS parameter names to min_tls_version"""
    new_params = dict(params)
    new_predicate = predicate
    
    # Map various TLS param names to min_tls_version
    tls_param_mappings = {
        "minTlsPolicy": "min_tls_version",
        "tlsPolicy": "min_tls_version", 
        "sslPolicy": "min_tls_version",
        "tlsVersion": "min_tls_version"
    }
    
    for old_name, new_name in tls_param_mappings.items():
        if old_name in new_params:
            new_params[new_name] = new_params.pop(old_name)
            # Update predicate to use new param name
            new_predicate = new_predicate.replace(old_name, new_name)
    
    return new_params, new_predicate


def fix_redshift_resource_types(service: str, resource: str, resource_type: str) -> Tuple[str, str]:
    """Fix Redshift resource types that incorrectly use k8s.cluster"""
    if service == "redshift":
        if resource == "k8s.cluster" or resource_type == "k8s.cluster":
            return "redshift.cluster", "redshift.cluster"
    return resource, resource_type


def fix_paths_doc(paths_doc: List[str], service: str, adapter: str, fields: List[str]) -> List[str]:
    """Align paths_doc with actual AWS APIs"""
    svc = service.lower()
    a = adapter.lower()
    
    # Service-specific API mappings
    api_mappings = {
        "iam": {
            "user_mfa": ["IAM:ListMFADevices", "IAM:GetAccountSummary"],
            "password_policy": ["IAM:GetAccountPasswordPolicy"],
            "inline_policies": ["IAM:ListUserPolicies", "IAM:GetUserPolicy"],
            "attached_policies": ["IAM:ListAttachedUserPolicies"],
        },
        "s3": {
            "public_access_block": ["S3:GetPublicAccessBlock"],
            "bucket_encryption": ["S3:GetBucketEncryption"],
            "bucket_logging": ["S3:GetBucketLogging"],
        },
        "ec2": {
            "instance_metadata": ["EC2:DescribeInstances -> MetadataOptions"],
            "security_groups": ["EC2:DescribeSecurityGroups"],
            "flow_logs": ["EC2:DescribeFlowLogs"],
        },
        "rds": {
            "instance_attributes": ["RDS:DescribeDBInstances"],
            "cluster_attributes": ["RDS:DescribeDBClusters"],
        },
        "kms": {
            "key_rotation": ["KMS:GetKeyRotationStatus"],
            "key_policy": ["KMS:GetKeyPolicy"],
        },
        "elbv2": {
            "listeners": ["ELBv2:DescribeListeners"],
            "ssl_policies": ["ELBv2:DescribeSSLPolicies"],
        },
        "cloudtrail": {
            "trail_status": ["CloudTrail:DescribeTrails", "CloudTrail:GetTrailStatus"],
        },
        "config": {
            "recorder_status": ["Config:DescribeConfigurationRecorders"],
            "delivery_channel": ["Config:DescribeDeliveryChannels"],
        },
    }
    
    if svc in api_mappings:
        for key, apis in api_mappings[svc].items():
            if key in a:
                return apis
    
    # Fallback: construct from service and fields
    if not paths_doc or paths_doc == ["API call to fetch configuration"]:
        return [f"{svc.upper()}:Describe* or Get* for {', '.join(fields)}"]
    
    return paths_doc


def enrich_identity_providers(service: str, adapter: str, fields: List[str], predicate: str) -> Tuple[List[str], str]:
    """Enrich identity provider rows with explicit fields"""
    if service in ["sso", "directoryservice", "cognito"]:
        if "sso" in adapter.lower():
            new_fields = ["identityStoreId", "permissionSets", "provisioningEnabled"]
            new_predicate = "identityStoreId && permissionSets.length >= 1 && provisioningEnabled === true"
        elif "directory" in adapter.lower():
            new_fields = ["directoryId", "type", "vpcSettings", "connectSettings"]
            new_predicate = "directoryId && (type === 'SimpleAD' || type === 'MicrosoftAD')"
        elif "cognito" in adapter.lower():
            new_fields = ["userPoolId", "mfaConfiguration", "passwordPolicy"]
            new_predicate = "userPoolId && mfaConfiguration !== 'OFF'"
        else:
            return fields, predicate
        return new_fields, new_predicate
    
    return fields, predicate


# --- Normalization helpers ---

def normalize_service(raw_service: str) -> str:
    s = (raw_service or "").lower().replace("_", "-")
    aliases = {
        "elb": "elbv2",
        "alb": "elbv2",
        "nlb": "elbv2",
        "waf": "wafv2",
        "work-docs": "workdocs",
        "x_ray": "xray",
        "security_hub": "securityhub",
        "identity-center": "identity_center",
        "directory_service": "directoryservice",
        "network_firewall": "networkfirewall",
        "route53_resolver": "route53-resolver",
        "route53_resolver_dns_firewall": "route53-resolver",
        "access-analyzer": "accessanalyzer",
        "vpc_flow_logs": "ec2",
        "direct_connect": "directconnect",
        "service_catalog": "servicecatalog",
        "trusted_advisor": "trustedadvisor",
        "well_architected": "wellarchitected",
        "x-ray": "xray",
    }
    s = aliases.get(s, s)
    return s


def normalize_resource(service: str, raw_resource: str, raw_type: str) -> Tuple[str, str]:
    svc = normalize_service(service)
    r = raw_resource or raw_type or ""
    # Map common logical to canonical
    mapping_by_type = {
        "identity.user": "iam.user",
        "identity.group": "iam.group",
        "rbac.role": "iam.role",
        "rbac.group": "iam.group",
        "rbac.policy": "iam.policy",
        "crypto.kms.key": "kms.key",
        "storage.bucket": "s3.bucket",
        "storage.object": "s3.object",
        "storage.fileshare": "efs.filesystem",
        "storage.table": "dynamodb.table",
        "storage.volume": "ec2.volume",
        "storage.snapshot": "ebs.snapshot",
        "db.instance": "rds.db_instance",
        "db.cluster": "rds.db_cluster",
        "k8s.cluster": "eks.cluster",
        "k8s.node_pool": "eks.nodegroup",
        "k8s.workload": "ecs.task",
        "k8s.admission": "eks.admission",
        "network.load_balancer": "elbv2.load_balancer",
        "network.security_group": "ec2.security_group",
        "network.route_table": "ec2.route_table",
        "network.vpc": "ec2.vpc",
        "network.subnet": "ec2.subnet",
        "network.endpoint": "ec2.vpc_endpoint",
        "platform.api_endpoint": "apigateway.api",
        "logging.store": "s3.bucket",
        "platform.control_plane": f"{svc}.control_plane",
        "governance.org": "organizations.org",
        "monitoring.metric": "cloudwatch.metric",
        "monitoring.alert": "cloudwatch.alarm",
        "backup.plan": "backup.plan",
        "backup.vault": "backup.vault",
        "dr.plan": "drs.plan",
        "distribution": "cloudfront.distribution",
        "repository": "ecr.repository",
        "certificate": "acm.certificate",
        "api": "apigateway.api",
        "assessment": "inspector.assessment",
        "rule": "config.rule",
        "insight": "cloudtrail.insight",
        "trace": "xray.trace",
    }
    canon = mapping_by_type.get(r, r)
    if svc == "redshift":
        canon = "redshift.cluster"
    if svc == "ec2" and raw_resource == "flow_log":
        canon = "ec2.flow_log"
    if svc in ("elb", "elbv2"):
        canon = "elbv2.load_balancer"
    if svc == "guardduty":
        canon = "guardduty.detector"
    if svc == "kms":
        canon = "kms.key"
    return canon, canon


def normalize_adapter(service: str, raw_adapter: str) -> str:
    svc = normalize_service(service)
    a = (raw_adapter or "").lower()
    m = re.search(r"(?:^|\b)(?:aws\.)?" + re.escape(svc) + r"\.([a-z0-9_\-\.]+)$", a)
    if m:
        slug = m.group(1)
    else:
        slug = a.split(".")[-1]
    slug = slug.replace("-", "_")
    slug = re.sub(r"^" + re.escape(svc) + r"_", "", slug)
    return f"aws.{svc}.{slug}"


def derive_signal_slug(adapter: str, predicate: str) -> Optional[str]:
    a = adapter
    p = predicate or ""
    checks = [
        ("mfa", ["mfa"], "any_mfa"),
        ("password_policy", ["password"], "strong_pw_not_disabled"),
        ("instance_metadata_options", ["httpTokens === 'required'"], "imdsv2_required"),
        ("public_access_block", ["blockPublicAcls", "blockPublicPolicy"], "all_blocks_enabled"),
        ("listeners", ["protocol === 'HTTPS'"], "https_required"),
        ("tls", ["compareTls"], "tls_min"),
        ("encryption", ["serverSideEncryption", "StorageEncrypted", "encrypted === true"], "encrypted"),
        ("key_rotation", ["rotation"], "rotation_enabled"),
        ("instance_attributes", ["publiclyAccessible === false"], "public_access_disabled"),
        ("cluster_logging", ["logging.enabledTypes"], "logging_enabled"),
        ("object_lock", ["objectLock"], "immutability_enabled"),
        ("config", ["recorder.enabled", "delivery.channelConfigured"], "recorder_and_channel_active"),
    ]
    for key, needles, slug in checks:
        if key in a and all(n in p for n in needles):
            return slug
    tokens = re.findall(r"[A-Za-z_]+", p)
    for t in ["required","enabled","disabled","present","blocked","restricted"]:
        if t in tokens:
            return t
    return None


def index_assertions_by_domain_subcat(assertions_root: Dict[str, Any]) -> Dict[Tuple[str, str], List[Dict[str, Any]]]:
    idx: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for a in assertions_root.get("assertions", []):
        sub = a.get("subcat_ref") or {}
        dk = sub.get("domain_key")
        sc = sub.get("subcat_id")
        if dk and sc:
            idx.setdefault((dk, sc), []).append(a)
    return idx


def pick_assertion_id(domain_subcat: str, resource: str, assertions_idx: Dict[Tuple[str, str], List[Dict[str, Any]]]) -> Optional[str]:
    if "." in domain_subcat:
        dk, sc = domain_subcat.split(".", 1)
    else:
        return None
    candidates = assertions_idx.get((dk, sc), [])
    for a in candidates:
        scope = a.get("scope") or ""
        if scope and scope.split(".")[0] in resource:
            return a.get("assertion_id")
    return candidates[0]["assertion_id"] if candidates else None


def transform() -> Dict[str, Any]:
    matrix_root = load_json(INPUT_MATRIX_PATH)
    assertions_root = load_json(ASSERTIONS_PATH)
    assertions_idx = index_assertions_by_domain_subcat(assertions_root)

    enriched = matrix_root.get("matrix", {})
    out_rules: List[Dict[str, Any]] = []

    for domain_subcat, rows in enriched.items():
        for row in rows:
            raw_service = row.get("service")
            service = normalize_service(raw_service)
            
            # Fix Redshift resource types
            resource_canon, resource_type_canon = fix_redshift_resource_types(
                service, row.get("resource"), row.get("resource_type")
            )
            if resource_canon == row.get("resource"):  # Only apply if not already fixed
                resource_canon, resource_type_canon = normalize_resource(service, row.get("resource"), row.get("resource_type"))
            
            adapter_norm = normalize_adapter(service, row.get("adapter") or "")

            signal = row.get("signal") or {}
            fields = signal.get("fields") or []
            predicate = signal.get("predicate") or ""
            paths_doc = signal.get("paths_doc") or []
            evidence_type = signal.get("evidence_type") or "config_read"
            params = row.get("params") or {}

            # Apply high-impact fixes
            predicate = fix_placeholder_predicates(predicate, fields, service, adapter_norm)
            predicate = fix_tautology_predicates(predicate, fields)
            params, predicate = normalize_tls_params(params, predicate)
            paths_doc = fix_paths_doc(paths_doc, service, adapter_norm, fields)
            fields, predicate = enrich_identity_providers(service, adapter_norm, fields, predicate)

            signal_slug = derive_signal_slug(adapter_norm, predicate)

            adapter_slug = adapter_norm.split(".", 2)[-1]
            rule_id = f"aws.{service}.{resource_canon}.{adapter_slug}"
            if signal_slug:
                rule_id += f".{signal_slug}"

            assertion_id = row.get("assertion_id") or pick_assertion_id(domain_subcat, resource_canon, assertions_idx)

            new_row = {
                "provider": "aws",
                "service": service,
                "resource": resource_canon,
                "resource_type": resource_type_canon,
                "adapter": adapter_norm,
                "signal": {
                    "fields": fields,
                    "predicate": predicate,
                    "paths_doc": paths_doc,
                    "evidence_type": evidence_type,
                },
                "signal_slug": signal_slug,
                "rule_id": rule_id,
                "assertion_id": assertion_id,
                "coverage_tier": row.get("coverage_tier") or "core",
                "not_applicable_when": row.get("not_applicable_when"),
                "params": params,
            }
            out_rules.append(new_row)

    return {
        "provider": "aws",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_matrix": os.path.basename(INPUT_MATRIX_PATH),
        "source_assertions": os.path.basename(ASSERTIONS_PATH),
        "rule_count": len(out_rules),
        "rules": out_rules,
    }


def main() -> None:
    data = transform()
    save_json(OUTPUT_PATH, data)
    print(f"Wrote {data['rule_count']} rules with high-impact fixes to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
