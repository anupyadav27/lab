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
    "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step4-rune-per-cloud-provider/aws_rules_with_ids_2025-09-24.json"


# --- Load/save helpers ---

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


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
            resource_canon, resource_type_canon = normalize_resource(service, row.get("resource"), row.get("resource_type"))
            adapter_norm = normalize_adapter(service, row.get("adapter") or "")

            signal = row.get("signal") or {}
            fields = signal.get("fields") or []
            predicate = signal.get("predicate") or ""
            paths_doc = signal.get("paths_doc") or []
            evidence_type = signal.get("evidence_type") or "config_read"

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
                "params": row.get("params") or {},
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
    print(f"Wrote {data['rule_count']} rules to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
