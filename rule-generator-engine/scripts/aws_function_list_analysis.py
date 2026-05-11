#!/usr/bin/env python3
"""
AWS Function List Analysis

This script analyzes the AWS function list to:
1. Extract all services and their security functions
2. Map them to our domain+subcat taxonomy
3. Identify missing services and security checks
4. Create a comprehensive mapping for matrix inclusion
"""

import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Set, Tuple

# Input files
AWS_FUNCTION_LIST_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws fucntion list"
TAXONOMY_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-1-common-taxonomy/subcategories_taxonomy_clean_2025-09-11T17-30-20.json"
CURRENT_MATRIX_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_matrix_structured_comprehensive_v2_2025-09-24.json"

# Output files
ANALYSIS_OUTPUT = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_function_list_analysis_2025-09-24.json"
MAPPING_OUTPUT = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_services_domain_mapping_2025-09-24.json"


def load_json(path: str) -> Any:
    """Load JSON file"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: Any) -> None:
    """Save JSON file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def analyze_aws_function_list(aws_functions: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze the AWS function list to extract services and categorize functions"""
    
    # Handle different file formats
    if "unique_functions" in aws_functions:
        # New format: list of unique functions
        function_list = aws_functions["unique_functions"]
        # Group functions by service prefix
        services = {}
        for func in function_list:
            service = func.split('_')[0]  # Extract service from function name
            if service not in services:
                services[service] = []
            services[service].append(func)
        aws_functions = services
    elif isinstance(list(aws_functions.values())[0], list):
        # Original format: service -> list of functions
        pass
    else:
        raise ValueError("Unknown AWS function list format")
    
    analysis = {
        "total_services": len(aws_functions),
        "total_functions": sum(len(functions) for functions in aws_functions.values()),
        "services": {},
        "function_categories": {},
        "security_patterns": {}
    }
    
    # Security function patterns to categorize
    security_patterns = {
        "encryption": ["encrypt", "encrypted", "encryption", "kms", "ssl", "tls"],
        "access_control": ["access", "public", "private", "restrict", "block", "acl"],
        "authentication": ["auth", "mfa", "login", "password", "certificate"],
        "authorization": ["policy", "permission", "role", "privilege", "admin"],
        "logging": ["log", "logging", "audit", "trail", "monitor"],
        "backup": ["backup", "snapshot", "recovery", "restore"],
        "compliance": ["compliance", "policy", "standard", "requirement"],
        "monitoring": ["monitor", "alarm", "metric", "watch", "alert"],
        "network_security": ["vpc", "subnet", "security_group", "firewall", "waf"],
        "data_protection": ["data", "classification", "retention", "lifecycle"],
        "vulnerability": ["vulnerability", "scan", "inspect", "finding", "threat"],
        "configuration": ["config", "setting", "parameter", "default", "enabled"]
    }
    
    for service, functions in aws_functions.items():
        service_analysis = {
            "service_name": service,
            "function_count": len(functions),
            "functions": functions,
            "security_categories": {},
            "domain_mapping": []
        }
        
        # Categorize functions by security patterns
        for pattern, keywords in security_patterns.items():
            matching_functions = []
            for func in functions:
                if any(keyword in func.lower() for keyword in keywords):
                    matching_functions.append(func)
            if matching_functions:
                service_analysis["security_categories"][pattern] = matching_functions
        
        analysis["services"][service] = service_analysis
    
    return analysis


def map_services_to_domains(aws_functions: Dict[str, Any], taxonomy: Dict[str, Any]) -> Dict[str, Any]:
    """Map AWS services to security domains based on their functions"""
    
    # Domain mapping rules based on service functions
    domain_mapping_rules = {
        # Identity & Access Management
        "identity_access": {
            "services": ["iam", "cognito", "identity_center", "directoryservice", "sts"],
            "patterns": ["auth", "mfa", "password", "policy", "role", "user", "group", "access", "permission"]
        },
        
        # RBAC & Entitlements
        "rbac_entitlements": {
            "services": ["iam", "identity_center", "organizations"],
            "patterns": ["role", "policy", "permission", "entitlement", "privilege", "admin", "access"]
        },
        
        # Secrets & Key Management
        "secrets_key_mgmt": {
            "services": ["kms", "secretsmanager", "ssm", "parameter"],
            "patterns": ["secret", "key", "kms", "encrypt", "rotation", "credential", "password"]
        },
        
        # Cryptography & Data Protection
        "crypto_data_protection": {
            "services": ["kms", "acm", "s3", "rds", "dynamodb", "redshift", "efs", "ebs", "glacier"],
            "patterns": ["encrypt", "ssl", "tls", "certificate", "key", "crypto", "cipher"]
        },
        
        # Data Protection & Storage
        "data_protection_storage": {
            "services": ["s3", "ebs", "efs", "glacier", "backup", "rds", "dynamodb", "redshift"],
            "patterns": ["backup", "snapshot", "retention", "lifecycle", "versioning", "replication", "storage"]
        },
        
        # Network & Perimeter
        "network_perimeter": {
            "services": ["vpc", "elb", "elbv2", "cloudfront", "route53", "apigateway", "waf", "wafv2", "networkfirewall", "shield"],
            "patterns": ["vpc", "subnet", "security_group", "firewall", "waf", "ddos", "load_balancer", "dns", "api"]
        },
        
        # Compute & Host Security
        "compute_host_security": {
            "services": ["ec2", "ecs", "eks", "lambda", "autoscaling", "lightsail", "workspaces"],
            "patterns": ["instance", "container", "server", "host", "vulnerability", "patch", "monitor", "imds"]
        },
        
        # Governance & Compliance
        "governance_compliance": {
            "services": ["cloudtrail", "config", "securityhub", "guardduty", "organizations", "cloudformation"],
            "patterns": ["audit", "log", "trail", "config", "compliance", "policy", "governance", "monitor"]
        },
        
        # Containers & Kubernetes
        "containers_kubernetes": {
            "services": ["eks", "ecs", "ecr", "fargate"],
            "patterns": ["cluster", "pod", "container", "kubernetes", "image", "registry", "namespace"]
        },
        
        # Serverless & PaaS
        "serverless_paas": {
            "services": ["lambda", "apigateway", "stepfunctions", "sns", "sqs", "eventbridge"],
            "patterns": ["function", "api", "serverless", "event", "trigger", "workflow"]
        },
        
        # Database Security
        "database_security": {
            "services": ["rds", "dynamodb", "redshift", "elasticache", "neptune", "documentdb", "dms"],
            "patterns": ["database", "db", "rds", "dynamodb", "redshift", "cache", "cluster", "instance"]
        },
        
        # Application Security
        "application_security": {
            "services": ["waf", "wafv2", "apigateway", "cloudfront", "appsync"],
            "patterns": ["waf", "api", "application", "web", "http", "https", "cors", "authorizer"]
        },
        
        # Monitoring & Observability
        "monitoring_observability": {
            "services": ["cloudwatch", "xray", "cloudtrail", "logs"],
            "patterns": ["log", "metric", "alarm", "monitor", "watch", "trace", "observability"]
        },
        
        # Incident Response
        "incident_response": {
            "services": ["guardduty", "securityhub", "inspector", "macie", "detective"],
            "patterns": ["threat", "finding", "incident", "detection", "response", "alert", "security"]
        },
        
        # Business Continuity
        "business_continuity": {
            "services": ["backup", "drs", "cloudendure", "disaster"],
            "patterns": ["backup", "recovery", "disaster", "continuity", "restore", "failover"]
        }
    }
    
    mapping = {
        "service_domain_mapping": {},
        "domain_service_mapping": {},
        "unmapped_services": [],
        "coverage_analysis": {}
    }
    
    # Initialize domain mappings
    for domain in domain_mapping_rules.keys():
        mapping["domain_service_mapping"][domain] = []
    
    # Handle different file formats for mapping
    if "unique_functions" in aws_functions:
        # New format: list of unique functions
        function_list = aws_functions["unique_functions"]
        # Group functions by service prefix
        services = {}
        for func in function_list:
            service = func.split('_')[0]  # Extract service from function name
            if service not in services:
                services[service] = []
            services[service].append(func)
        aws_functions = services
    
    # Map each service to domains
    for service, functions in aws_functions.items():
        service_domains = []
        
        for domain, rules in domain_mapping_rules.items():
            # Check if service is explicitly listed
            if service in rules["services"]:
                service_domains.append(domain)
                mapping["domain_service_mapping"][domain].append(service)
            else:
                # Check if any function matches domain patterns
                for func in functions:
                    if any(pattern in func.lower() for pattern in rules["patterns"]):
                        if domain not in service_domains:
                            service_domains.append(domain)
                            mapping["domain_service_mapping"][domain].append(service)
                        break
        
        mapping["service_domain_mapping"][service] = service_domains
        
        if not service_domains:
            mapping["unmapped_services"].append(service)
    
    # Analyze coverage
    for domain, services in mapping["domain_service_mapping"].items():
        mapping["coverage_analysis"][domain] = {
            "total_services": len(services),
            "services": services,
            "coverage_percentage": len(services) / len(aws_functions) * 100
        }
    
    return mapping


def identify_missing_services(current_matrix: Dict[str, Any], aws_functions: Dict[str, List[str]]) -> Dict[str, Any]:
    """Identify services that are in the function list but missing from current matrix"""
    
    # Extract services from current matrix
    current_services = set()
    if "matrix" in current_matrix:
        for domain_subcat, checks in current_matrix["matrix"].items():
            for check in checks:
                if "service" in check:
                    current_services.add(check["service"])
    
    # Get all services from function list
    function_list_services = set(aws_functions.keys())
    
    # Find missing services
    missing_services = function_list_services - current_services
    
    # Find additional services in current matrix
    additional_services = current_services - function_list_services
    
    return {
        "current_matrix_services": list(current_services),
        "function_list_services": list(function_list_services),
        "missing_services": list(missing_services),
        "additional_services": list(additional_services),
        "coverage_percentage": len(current_services & function_list_services) / len(function_list_services) * 100
    }


def create_comprehensive_mapping(aws_functions: Dict[str, List[str]], taxonomy: Dict[str, Any], current_matrix: Dict[str, Any]) -> Dict[str, Any]:
    """Create comprehensive mapping for matrix inclusion"""
    
    # Analyze function list
    analysis = analyze_aws_function_list(aws_functions)
    
    # Map services to domains
    domain_mapping = map_services_to_domains(aws_functions, taxonomy)
    
    # Identify missing services
    missing_analysis = identify_missing_services(current_matrix, aws_functions)
    
    # Create comprehensive mapping
    comprehensive_mapping = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total_services_in_function_list": len(aws_functions),
            "total_functions": sum(len(functions) for functions in aws_functions.values()),
            "services_in_current_matrix": len(missing_analysis["current_matrix_services"]),
            "missing_services_count": len(missing_analysis["missing_services"]),
            "coverage_percentage": missing_analysis["coverage_percentage"]
        },
        "analysis": analysis,
        "domain_mapping": domain_mapping,
        "missing_services_analysis": missing_analysis,
        "recommendations": {
            "high_priority_services": [],
            "medium_priority_services": [],
            "low_priority_services": []
        }
    }
    
    # Categorize missing services by priority
    high_priority_services = ["iam", "s3", "ec2", "rds", "kms", "cloudtrail", "config", "guardduty", "securityhub"]
    medium_priority_services = ["lambda", "apigateway", "cloudfront", "vpc", "elbv2", "secretsmanager", "ssm"]
    
    for service in missing_analysis["missing_services"]:
        if service in high_priority_services:
            comprehensive_mapping["recommendations"]["high_priority_services"].append(service)
        elif service in medium_priority_services:
            comprehensive_mapping["recommendations"]["medium_priority_services"].append(service)
        else:
            comprehensive_mapping["recommendations"]["low_priority_services"].append(service)
    
    return comprehensive_mapping


def main() -> None:
    """Main function"""
    print("Analyzing AWS Function List...")
    
    # Load input files
    aws_functions = load_json(AWS_FUNCTION_LIST_PATH)
    taxonomy = load_json(TAXONOMY_PATH)
    current_matrix = load_json(CURRENT_MATRIX_PATH)
    
    print(f"Found {len(aws_functions)} services in function list")
    print(f"Total functions: {sum(len(functions) for functions in aws_functions.values())}")
    
    # Create comprehensive mapping
    mapping = create_comprehensive_mapping(aws_functions, taxonomy, current_matrix)
    
    # Save outputs
    save_json(ANALYSIS_OUTPUT, mapping)
    save_json(MAPPING_OUTPUT, mapping)
    
    print(f"Saved analysis to {ANALYSIS_OUTPUT}")
    print(f"Saved mapping to {MAPPING_OUTPUT}")
    
    # Print summary
    print("\n=== COVERAGE ANALYSIS ===")
    print(f"Services in function list: {mapping['summary']['total_services_in_function_list']}")
    print(f"Services in current matrix: {mapping['summary']['services_in_current_matrix']}")
    print(f"Missing services: {mapping['summary']['missing_services_count']}")
    print(f"Coverage percentage: {mapping['summary']['coverage_percentage']:.1f}%")
    
    print("\n=== MISSING SERVICES ===")
    for service in mapping['missing_services_analysis']['missing_services']:
        print(f"- {service}")
    
    print("\n=== HIGH PRIORITY SERVICES TO ADD ===")
    for service in mapping['recommendations']['high_priority_services']:
        print(f"- {service}")
    
    print("\n=== DOMAIN COVERAGE ===")
    for domain, analysis in mapping['domain_mapping']['coverage_analysis'].items():
        print(f"{domain}: {analysis['total_services']} services ({analysis['coverage_percentage']:.1f}%)")


if __name__ == "__main__":
    main()
