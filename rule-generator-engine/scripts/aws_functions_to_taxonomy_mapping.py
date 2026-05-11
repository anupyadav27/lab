#!/usr/bin/env python3
"""
AWS Functions to Taxonomy Mapping

This script maps AWS security functions to domain+subcat combinations
from our taxonomy to understand mapping possibilities.
"""

import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Set, Tuple

# Input files
AWS_FUNCTION_LIST_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws fucntion list"
TAXONOMY_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-1-common-taxonomy/subcategories_taxonomy_clean_2025-09-11T17-30-20.json"

# Output files
MAPPING_OUTPUT = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_functions_taxonomy_mapping_2025-09-24.json"


def load_json(path: str) -> Any:
    """Load JSON file"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: Any) -> None:
    """Save JSON file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def extract_service_from_function(func_name: str) -> str:
    """Extract service name from function name"""
    # Handle special cases
    special_cases = {
        "awslambda": "lambda",
        "apigatewayv2": "apigateway",
        "elbv2": "elb",
        "wafv2": "waf",
        "directoryservice": "directoryservice",
        "identity_center": "identity_center",
        "storagegateway": "storagegateway",
        "wellarchitected": "wellarchitected"
    }
    
    # Extract first part before underscore
    service = func_name.split('_')[0]
    
    # Apply special cases
    if service in special_cases:
        return special_cases[service]
    
    return service


def create_function_to_taxonomy_mapping() -> Dict[str, List[str]]:
    """Create mapping from function patterns to domain+subcat combinations"""
    
    # Simplified mapping focusing on key patterns
    mapping = {
        # Identity & Access Management
        "identity_access.authentication": [
            "iam_user_mfa_enabled", "iam_user_hardware_mfa_enabled", "iam_root_mfa_enabled",
            "iam_root_hardware_mfa_enabled", "iam_password_policy_*", "cognito_user_pool_mfa_enabled",
            "cognito_user_pool_password_policy_*", "directoryservice_supported_mfa_radius_enabled",
            "iam_administrator_access_with_mfa", "iam_avoid_root_usage"
        ],
        
        "identity_access.authorization": [
            "iam_*_policy_*", "iam_role_*", "iam_group_*", "iam_user_*", "cognito_*_policy_*",
            "identity_center_*", "organizations_*", "iam_policy_attached_only_to_group_or_roles"
        ],
        
        "identity_access.federation": [
            "cognito_*", "identity_center_*", "directoryservice_*", "saml_*", "oidc_*"
        ],
        
        "identity_access.mfa": [
            "iam_*_mfa_*", "cognito_user_pool_mfa_enabled", "directoryservice_supported_mfa_radius_enabled"
        ],
        
        "identity_access.session_management": [
            "iam_user_console_access_*", "iam_user_accesskey_*", "iam_rotate_access_key_*",
            "cognito_user_pool_client_token_revocation_enabled", "cognito_user_pool_temporary_password_expiration"
        ],
        
        "identity_access.least_privilege": [
            "iam_*_no_administrative_privileges", "iam_*_no_full_access_*", "iam_*_least_privilege",
            "iam_policy_attached_only_to_group_or_roles"
        ],
        
        # RBAC & Entitlements
        "rbac_entitlements.role_definition": [
            "iam_role_*", "iam_policy_*", "identity_center_permission_set_*", "organizations_*"
        ],
        
        "rbac_entitlements.role_assignment": [
            "iam_*_policy_*", "cognito_*_policy_*", "identity_center_*", "organizations_tags_policies_*"
        ],
        
        "rbac_entitlements.least_privilege": [
            "iam_*_no_administrative_privileges", "iam_*_no_full_access_*", "iam_*_least_privilege",
            "iam_policy_attached_only_to_group_or_roles"
        ],
        
        "rbac_entitlements.entitlement_management": [
            "iam_*_policy_*", "cognito_*_policy_*", "identity_center_*", "organizations_tags_policies_*"
        ],
        
        # Secrets & Key Management
        "secrets_key_mgmt.secret_storage": [
            "secretsmanager_*", "ssm_*", "parameter_*", "kms_*", "iam_no_expired_server_certificates_stored"
        ],
        
        "secrets_key_mgmt.key_rotation": [
            "kms_*_rotation_*", "secretsmanager_automatic_rotation_enabled", "iam_rotate_access_key_*"
        ],
        
        "secrets_key_mgmt.key_protection": [
            "kms_*", "acm_*", "iam_*_certificate_*", "secretsmanager_*"
        ],
        
        "secrets_key_mgmt.secret_retrieval": [
            "secretsmanager_*", "ssm_*", "parameter_*", "kms_*"
        ],
        
        "secrets_key_mgmt.secret_sprawl": [
            "secretsmanager_secret_unused", "iam_user_accesskey_unused", "iam_user_console_access_unused"
        ],
        
        # Cryptography & Data Protection
        "crypto_data_protection.encryption_at_rest": [
            "*_encryption_enabled", "*_encrypted_at_rest", "*_kms_encryption", "*_storage_encrypted",
            "s3_*_encryption", "rds_*_encryption", "dynamodb_*_encryption", "efs_encryption_at_rest_enabled",
            "ebs_*_encryption", "glacier_*_encryption"
        ],
        
        "crypto_data_protection.encryption_in_transit": [
            "*_ssl_enabled", "*_tls_*", "*_https_*", "*_in_transit_encryption", "*_transport_encrypted",
            "elb_*_ssl_*", "apigateway_*_ssl_*", "rds_*_transport_encrypted", "dms_*_ssl_enabled"
        ],
        
        "crypto_data_protection.key_management": [
            "kms_*", "acm_*", "iam_*_certificate_*", "secretsmanager_automatic_rotation_enabled"
        ],
        
        "crypto_data_protection.certificate_management": [
            "acm_*", "iam_*_certificate_*", "*_certificate_*", "*_ssl_certificate_*"
        ],
        
        # Data Protection & Storage
        "data_protection_storage.backup_recovery": [
            "*_backup_enabled", "*_snapshot_*", "*_recovery_*", "*_restore_*", "backup_*",
            "rds_*_backup", "dynamodb_*_backup", "redshift_*_backup", "neptune_*_backup"
        ],
        
        "data_protection_storage.data_classification": [
            "macie_*", "*_data_*", "*_classification_*", "*_sensitive_*"
        ],
        
        "data_protection_storage.data_retention": [
            "*_retention_*", "*_lifecycle_*", "*_versioning_*", "*_expiration_*"
        ],
        
        # Network & Perimeter
        "network_perimeter.network_segmentation": [
            "vpc_*", "subnet_*", "security_group_*", "networkacl_*", "route_table_*"
        ],
        
        "network_perimeter.firewall_rules": [
            "waf_*", "networkfirewall_*", "shield_*", "*_firewall_*"
        ],
        
        "network_perimeter.load_balancing": [
            "elb_*", "elbv2_*", "*_load_balancer_*", "*_listener_*"
        ],
        
        "network_perimeter.dns_security": [
            "route53_*", "*_dns_*", "*_domain_*"
        ],
        
        # Compute & Host Security
        "compute_host_security.vulnerability_management": [
            "inspector_*", "*_vulnerability_*", "*_scan_*", "*_finding_*", "ecr_*_scan_*"
        ],
        
        "compute_host_security.patch_management": [
            "*_patch_*", "*_update_*", "*_upgrade_*", "*_version_*", "ssm_managed_compliant_patching"
        ],
        
        "compute_host_security.endpoint_protection": [
            "ec2_*_security_*", "*_endpoint_*", "*_protection_*", "*_antivirus_*"
        ],
        
        "compute_host_security.os_hardening": [
            "ec2_*_hardening", "*_hardening_*", "*_secure_*", "*_hardened_*"
        ],
        
        # Governance & Compliance
        "governance_compliance.policy_management": [
            "*_policy_*", "*_compliance_*", "*_standard_*", "*_requirement_*"
        ],
        
        "governance_compliance.compliance_framework": [
            "*_compliance_*", "*_framework_*", "*_standard_*", "*_requirement_*"
        ],
        
        "governance_compliance.resource_governance": [
            "*_governance_*", "*_resource_*", "*_management_*", "*_control_*"
        ],
        
        "governance_compliance.risk_management": [
            "*_risk_*", "*_threat_*", "*_security_*", "*_assessment_*"
        ],
        
        # Containers & Kubernetes
        "containers_kubernetes.image_security": [
            "ecr_*", "*_image_*", "*_registry_*", "*_scan_*"
        ],
        
        "containers_kubernetes.runtime_security": [
            "ecs_*", "fargate_*", "*_container_*", "*_pod_*", "*_namespace_*"
        ],
        
        "containers_kubernetes.network_policies": [
            "eks_*", "*_kubernetes_*", "*_cluster_*", "*_node_*"
        ],
        
        # Serverless & PaaS
        "serverless_paas.function_security": [
            "lambda_*", "awslambda_*", "*_function_*", "*_serverless_*"
        ],
        
        "serverless_paas.api_security": [
            "apigateway_*", "*_api_*", "*_endpoint_*", "*_gateway_*"
        ],
        
        "serverless_paas.event_security": [
            "eventbridge_*", "sns_*", "sqs_*", "*_event_*", "*_trigger_*"
        ],
        
        # Logging & Monitoring
        "logging_monitoring.log_collection": [
            "cloudwatch_*_log_*", "*_logging_enabled", "*_log_*", "cloudtrail_*"
        ],
        
        "logging_monitoring.monitoring_alerting": [
            "cloudwatch_*_metric_*", "*_monitoring_*", "*_metric_*", "*_alarm_*"
        ],
        
        "logging_monitoring.audit_logging": [
            "cloudtrail_*", "*_audit_*", "*_audit_logging_*", "*_audit_log_*"
        ],
        
        # Monitoring & Security Operations
        "monitoring_security.threat_detection": [
            "guardduty_*", "*_threat_*", "*_detection_*", "*_finding_*"
        ],
        
        "monitoring_security.incident_response": [
            "securityhub_*", "*_incident_*", "*_response_*", "*_management_*"
        ],
        
        "monitoring_security.logging": [
            "*_forensic_*", "*_investigation_*", "*_analysis_*", "*_evidence_*"
        ],
        
        # Resilience & Recovery
        "resilience_recovery.backup_strategy": [
            "*_backup_*", "*_recovery_*", "*_restore_*", "*_disaster_*"
        ],
        
        "resilience_recovery.disaster_recovery": [
            "*_disaster_*", "*_failover_*", "*_redundancy_*", "*_continuity_*"
        ],
        
        "resilience_recovery.high_availability": [
            "*_availability_*", "*_uptime_*", "*_reliability_*", "*_resilience_*"
        ]
    }
    
    return mapping


def map_functions_to_taxonomy(aws_functions: List[str], taxonomy: Dict[str, Any]) -> Dict[str, Any]:
    """Map AWS functions to domain+subcat combinations"""
    
    # Get function-to-taxonomy mapping
    function_mapping = create_function_to_taxonomy_mapping()
    
    # Get all domain+subcat combinations from taxonomy
    domain_subcats = []
    if "domains" in taxonomy:
        # New format with domains array
        for domain_obj in taxonomy["domains"]:
            domain_key = domain_obj["key"]
            for subcat_obj in domain_obj["subcategories"]:
                subcat_id = subcat_obj["subcat_id"]
                domain_subcats.append(f"{domain_key}.{subcat_id}")
    else:
        # Old format
        for domain, subcats in taxonomy.items():
            for subcat in subcats:
                domain_subcats.append(f"{domain}.{subcat}")
    
    # Initialize results
    results = {
        "mapping_summary": {
            "total_functions": len(aws_functions),
            "total_domain_subcats": len(domain_subcats),
            "mapped_functions": 0,
            "unmapped_functions": 0
        },
        "function_to_taxonomy": {},
        "taxonomy_to_functions": {},
        "service_analysis": {},
        "unmapped_functions": []
    }
    
    # Initialize taxonomy mappings
    for domain_subcat in domain_subcats:
        results["taxonomy_to_functions"][domain_subcat] = []
    
    # Map each function
    for func in aws_functions:
        service = extract_service_from_function(func)
        mapped_domains = []
        
        # Check against function mapping patterns
        for domain_subcat, patterns in function_mapping.items():
            for pattern in patterns:
                if pattern.endswith('*'):
                    # Wildcard pattern
                    prefix = pattern[:-1]
                    if func.startswith(prefix):
                        mapped_domains.append(domain_subcat)
                        break
                elif '*' in pattern:
                    # Pattern with wildcard in middle
                    parts = pattern.split('*')
                    if len(parts) == 2 and parts[0] in func and parts[1] in func:
                        mapped_domains.append(domain_subcat)
                        break
                else:
                    # Exact match
                    if func == pattern:
                        mapped_domains.append(domain_subcat)
                        break
        
        # Store mapping
        results["function_to_taxonomy"][func] = {
            "service": service,
            "mapped_domains": mapped_domains,
            "mapped_count": len(mapped_domains)
        }
        
        # Add to taxonomy mappings
        for domain_subcat in mapped_domains:
            results["taxonomy_to_functions"][domain_subcat].append(func)
        
        # Track mapping status
        if mapped_domains:
            results["mapping_summary"]["mapped_functions"] += 1
        else:
            results["mapping_summary"]["unmapped_functions"] += 1
            results["unmapped_functions"].append(func)
    
    # Analyze by service
    services = {}
    for func in aws_functions:
        service = extract_service_from_function(func)
        if service not in services:
            services[service] = {
                "functions": [],
                "mapped_functions": [],
                "unmapped_functions": []
            }
        
        services[service]["functions"].append(func)
        if results["function_to_taxonomy"][func]["mapped_domains"]:
            services[service]["mapped_functions"].append(func)
        else:
            services[service]["unmapped_functions"].append(func)
    
    results["service_analysis"] = services
    
    return results


def main() -> None:
    """Main function"""
    print("Mapping AWS Functions to Taxonomy...")
    
    # Load input files
    aws_data = load_json(AWS_FUNCTION_LIST_PATH)
    taxonomy = load_json(TAXONOMY_PATH)
    
    # Extract functions list
    if "unique_functions" in aws_data:
        aws_functions = aws_data["unique_functions"]
    else:
        # Handle other formats
        aws_functions = []
        for service, functions in aws_data.items():
            if isinstance(functions, list):
                aws_functions.extend(functions)
    
    print(f"Found {len(aws_functions)} AWS functions")
    
    # Count domains in taxonomy
    if "domains" in taxonomy:
        domain_count = len(taxonomy["domains"])
        subcat_count = sum(len(domain["subcategories"]) for domain in taxonomy["domains"])
        print(f"Found {domain_count} domains with {subcat_count} subcategories in taxonomy")
    else:
        print(f"Found {len(taxonomy)} domains in taxonomy")
    
    # Map functions to taxonomy
    mapping_results = map_functions_to_taxonomy(aws_functions, taxonomy)
    
    # Save results
    save_json(MAPPING_OUTPUT, mapping_results)
    
    print(f"Saved mapping results to {MAPPING_OUTPUT}")
    
    # Print summary
    print("\n=== MAPPING SUMMARY ===")
    print(f"Total functions: {mapping_results['mapping_summary']['total_functions']}")
    print(f"Mapped functions: {mapping_results['mapping_summary']['mapped_functions']}")
    print(f"Unmapped functions: {mapping_results['mapping_summary']['unmapped_functions']}")
    print(f"Mapping rate: {mapping_results['mapping_summary']['mapped_functions'] / mapping_results['mapping_summary']['total_functions'] * 100:.1f}%")
    
    print("\n=== TOP SERVICES BY FUNCTION COUNT ===")
    service_counts = [(service, len(data["functions"])) for service, data in mapping_results["service_analysis"].items()]
    service_counts.sort(key=lambda x: x[1], reverse=True)
    for service, count in service_counts[:10]:
        mapped = len(mapping_results["service_analysis"][service]["mapped_functions"])
        print(f"{service}: {count} functions ({mapped} mapped)")
    
    print("\n=== TOP DOMAIN+SUBCAT BY FUNCTION COUNT ===")
    domain_counts = [(domain, len(functions)) for domain, functions in mapping_results["taxonomy_to_functions"].items() if functions]
    domain_counts.sort(key=lambda x: x[1], reverse=True)
    for domain, count in domain_counts[:10]:
        print(f"{domain}: {count} functions")
    
    print("\n=== UNMAPPED FUNCTIONS (first 20) ===")
    for func in mapping_results["unmapped_functions"][:20]:
        print(f"- {func}")


if __name__ == "__main__":
    main()
