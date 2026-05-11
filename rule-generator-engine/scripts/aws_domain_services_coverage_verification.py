#!/usr/bin/env python3
"""
AWS Domain and Services Coverage Verification

This script creates comprehensive lists of:
1. All domains and subcategories from taxonomy
2. All AWS services that should be covered
3. Verification matrix to ensure complete coverage
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Set, Tuple

# Input files
TAXONOMY_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-1-common-taxonomy/subcategories_taxonomy_clean_2025-09-11T17-30-20.json"
ASSERTIONS_PATH = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/step-2-common-assercian-id/assertions_pack_final_2025-09-11T18-41-14_enhanced.json"

# Output files
DOMAIN_SERVICES_OUTPUT = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_domain_services_coverage_verification_2025-09-24.json"
COVERAGE_MATRIX_OUTPUT = "/Users/apple/Desktop/compliance_Database/rule-generator-engine/Step3-matrices-per-cloud-provider/aws_coverage_matrix_verification_2025-09-24.json"


def load_json(path: str) -> Any:
    """Load JSON file"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: Any) -> None:
    """Save JSON file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_all_domains_and_subcategories(taxonomy: Dict[str, Any]) -> Dict[str, List[str]]:
    """Extract all domains and their subcategories"""
    domains = {}
    for domain in taxonomy.get("domains", []):
        domain_name = domain.get("domain")
        domain_key = domain.get("key")
        subcategories = []
        
        for subcat in domain.get("subcategories", []):
            subcategories.append({
                "subcat_id": subcat.get("subcat_id"),
                "title": subcat.get("title"),
                "definition": subcat.get("definition")
            })
        
        domains[domain_key] = {
            "domain_name": domain_name,
            "domain_key": domain_key,
            "subcategories": subcategories
        }
    
    return domains


def get_comprehensive_aws_services() -> Dict[str, Dict[str, Any]]:
    """
    Comprehensive list of all AWS services that should be covered
    Organized by service category for better verification
    """
    aws_services = {
        # Identity & Access Management
        "identity_access": {
            "iam": {
                "service_name": "Identity and Access Management",
                "resources": ["iam.user", "iam.group", "iam.role", "iam.policy", "iam.server_certificate"],
                "description": "Core identity and access management"
            },
            "identity_center": {
                "service_name": "AWS Identity Center (SSO)",
                "resources": ["identity_center.permission_set", "identity_center.instance"],
                "description": "Single sign-on and identity federation"
            },
            "directoryservice": {
                "service_name": "AWS Directory Service",
                "resources": ["directoryservice.directory", "directoryservice.trust"],
                "description": "Managed Microsoft Active Directory"
            },
            "cognito": {
                "service_name": "Amazon Cognito",
                "resources": ["cognito.user_pool", "cognito.identity_pool"],
                "description": "User authentication and authorization"
            },
            "sts": {
                "service_name": "AWS Security Token Service",
                "resources": ["sts.session", "sts.assumed_role"],
                "description": "Temporary security credentials"
            }
        },
        
        # Compute Services
        "compute": {
            "ec2": {
                "service_name": "Amazon Elastic Compute Cloud",
                "resources": ["ec2.instance", "ec2.image", "ec2.volume", "ec2.snapshot", "ec2.security_group", "ec2.network_acl", "ec2.vpc", "ec2.subnet", "ec2.route_table", "ec2.vpc_endpoint", "ec2.flow_logs"],
                "description": "Virtual servers and networking"
            },
            "ecs": {
                "service_name": "Amazon Elastic Container Service",
                "resources": ["ecs.cluster", "ecs.service", "ecs.task", "ecs.task_definition"],
                "description": "Container orchestration service"
            },
            "eks": {
                "service_name": "Amazon Elastic Kubernetes Service",
                "resources": ["eks.cluster", "eks.nodegroup", "eks.addon", "eks.admission"],
                "description": "Managed Kubernetes service"
            },
            "lambda": {
                "service_name": "AWS Lambda",
                "resources": ["lambda.function", "lambda.layer", "lambda.event_source_mapping"],
                "description": "Serverless compute service"
            },
            "batch": {
                "service_name": "AWS Batch",
                "resources": ["batch.job_queue", "batch.compute_environment", "batch.job_definition"],
                "description": "Batch computing service"
            },
            "lightsail": {
                "service_name": "Amazon Lightsail",
                "resources": ["lightsail.instance", "lightsail.database", "lightsail.load_balancer"],
                "description": "Virtual private servers"
            }
        },
        
        # Storage Services
        "storage": {
            "s3": {
                "service_name": "Amazon Simple Storage Service",
                "resources": ["s3.bucket", "s3.object"],
                "description": "Object storage service"
            },
            "ebs": {
                "service_name": "Amazon Elastic Block Store",
                "resources": ["ebs.volume", "ebs.snapshot"],
                "description": "Block storage for EC2"
            },
            "efs": {
                "service_name": "Amazon Elastic File System",
                "resources": ["efs.filesystem", "efs.mount_target"],
                "description": "Managed NFS file system"
            },
            "fsx": {
                "service_name": "Amazon FSx",
                "resources": ["fsx.file_system", "fsx.backup"],
                "description": "Managed file systems"
            },
            "glacier": {
                "service_name": "Amazon S3 Glacier",
                "resources": ["glacier.vault", "glacier.archive"],
                "description": "Long-term archival storage"
            },
            "storage_gateway": {
                "service_name": "AWS Storage Gateway",
                "resources": ["storage_gateway.gateway", "storage_gateway.volume"],
                "description": "Hybrid cloud storage"
            }
        },
        
        # Database Services
        "database": {
            "rds": {
                "service_name": "Amazon Relational Database Service",
                "resources": ["rds.db_instance", "rds.db_cluster", "rds.db_snapshot", "rds.db_parameter_group"],
                "description": "Managed relational databases"
            },
            "dynamodb": {
                "service_name": "Amazon DynamoDB",
                "resources": ["dynamodb.table", "dynamodb.global_table", "dynamodb.backup"],
                "description": "NoSQL database service"
            },
            "redshift": {
                "service_name": "Amazon Redshift",
                "resources": ["redshift.cluster", "redshift.snapshot", "redshift.parameter_group"],
                "description": "Data warehouse service"
            },
            "elasticache": {
                "service_name": "Amazon ElastiCache",
                "resources": ["elasticache.cluster", "elasticache.replication_group", "elasticache.snapshot"],
                "description": "In-memory caching service"
            },
            "neptune": {
                "service_name": "Amazon Neptune",
                "resources": ["neptune.cluster", "neptune.db_instance", "neptune.snapshot"],
                "description": "Graph database service"
            },
            "documentdb": {
                "service_name": "Amazon DocumentDB",
                "resources": ["documentdb.cluster", "documentdb.db_instance", "documentdb.snapshot"],
                "description": "MongoDB-compatible database"
            }
        },
        
        # Networking Services
        "networking": {
            "vpc": {
                "service_name": "Amazon Virtual Private Cloud",
                "resources": ["vpc.vpc", "vpc.subnet", "vpc.route_table", "vpc.internet_gateway", "vpc.nat_gateway", "vpc.vpc_endpoint", "vpc.flow_logs"],
                "description": "Isolated cloud resources"
            },
            "elb": {
                "service_name": "Elastic Load Balancing (Classic)",
                "resources": ["elb.load_balancer"],
                "description": "Classic load balancer"
            },
            "elbv2": {
                "service_name": "Elastic Load Balancing (Application/Network)",
                "resources": ["elbv2.load_balancer", "elbv2.target_group", "elbv2.listener"],
                "description": "Application and network load balancer"
            },
            "cloudfront": {
                "service_name": "Amazon CloudFront",
                "resources": ["cloudfront.distribution", "cloudfront.origin_access_identity"],
                "description": "Content delivery network"
            },
            "route53": {
                "service_name": "Amazon Route 53",
                "resources": ["route53.hosted_zone", "route53.record_set", "route53.resolver", "route53.health_check"],
                "description": "DNS and domain name service"
            },
            "api_gateway": {
                "service_name": "Amazon API Gateway",
                "resources": ["apigateway.api", "apigateway.stage", "apigateway.deployment", "apigateway.usage_plan"],
                "description": "API management service"
            },
            "directconnect": {
                "service_name": "AWS Direct Connect",
                "resources": ["directconnect.connection", "directconnect.virtual_interface"],
                "description": "Dedicated network connection"
            },
            "vpn": {
                "service_name": "AWS VPN",
                "resources": ["vpn.connection", "vpn.customer_gateway", "vpn.vpn_gateway"],
                "description": "Site-to-site VPN connections"
            },
            "transit_gateway": {
                "service_name": "AWS Transit Gateway",
                "resources": ["transit_gateway.gateway", "transit_gateway.attachment", "transit_gateway.route_table"],
                "description": "Network transit hub"
            }
        },
        
        # Security Services
        "security": {
            "kms": {
                "service_name": "AWS Key Management Service",
                "resources": ["kms.key", "kms.alias", "kms.grant"],
                "description": "Encryption key management"
            },
            "secretsmanager": {
                "service_name": "AWS Secrets Manager",
                "resources": ["secretsmanager.secret", "secretsmanager.secret_version"],
                "description": "Secrets and credential management"
            },
            "ssm": {
                "service_name": "AWS Systems Manager",
                "resources": ["ssm.parameter", "ssm.document", "ssm.patch_baseline", "ssm.association", "ssm.maintenance_window"],
                "description": "Systems management and operations"
            },
            "guardduty": {
                "service_name": "Amazon GuardDuty",
                "resources": ["guardduty.detector", "guardduty.finding", "guardduty.threat_intel_set"],
                "description": "Threat detection service"
            },
            "securityhub": {
                "service_name": "AWS Security Hub",
                "resources": ["securityhub.hub", "securityhub.finding", "securityhub.insight"],
                "description": "Security findings aggregation"
            },
            "inspector": {
                "service_name": "Amazon Inspector",
                "resources": ["inspector.assessment", "inspector.finding", "inspector.assessment_template"],
                "description": "Vulnerability assessment"
            },
            "macie": {
                "service_name": "Amazon Macie",
                "resources": ["macie.session", "macie.finding", "macie.custom_data_identifier"],
                "description": "Data security and privacy"
            },
            "accessanalyzer": {
                "service_name": "AWS Access Analyzer",
                "resources": ["accessanalyzer.analyzer", "accessanalyzer.finding"],
                "description": "Access policy analysis"
            },
            "wafv2": {
                "service_name": "AWS WAF v2",
                "resources": ["wafv2.web_acl", "wafv2.rule_group", "wafv2.ip_set"],
                "description": "Web application firewall"
            },
            "shield": {
                "service_name": "AWS Shield",
                "resources": ["shield.protection", "shield.subscription"],
                "description": "DDoS protection"
            },
            "networkfirewall": {
                "service_name": "AWS Network Firewall",
                "resources": ["networkfirewall.firewall", "networkfirewall.firewall_policy", "networkfirewall.rule_group"],
                "description": "Network-level firewall"
            }
        },
        
        # Monitoring & Logging
        "monitoring": {
            "cloudwatch": {
                "service_name": "Amazon CloudWatch",
                "resources": ["cloudwatch.metric", "cloudwatch.alarm", "cloudwatch.log_group", "cloudwatch.dashboard"],
                "description": "Monitoring and observability"
            },
            "cloudtrail": {
                "service_name": "AWS CloudTrail",
                "resources": ["cloudtrail.trail", "cloudtrail.event"],
                "description": "API activity logging"
            },
            "config": {
                "service_name": "AWS Config",
                "resources": ["config.recorder", "config.rule", "config.delivery_channel", "config.configuration_item"],
                "description": "Configuration compliance monitoring"
            },
            "xray": {
                "service_name": "AWS X-Ray",
                "resources": ["xray.trace", "xray.sampling_rule", "xray.group"],
                "description": "Distributed tracing"
            }
        },
        
        # Application Services
        "application": {
            "sns": {
                "service_name": "Amazon Simple Notification Service",
                "resources": ["sns.topic", "sns.subscription"],
                "description": "Pub/sub messaging service"
            },
            "sqs": {
                "service_name": "Amazon Simple Queue Service",
                "resources": ["sqs.queue", "sqs.message"],
                "description": "Message queuing service"
            },
            "eventbridge": {
                "service_name": "Amazon EventBridge",
                "resources": ["eventbridge.event_bus", "eventbridge.rule", "eventbridge.target"],
                "description": "Event-driven architecture"
            },
            "stepfunctions": {
                "service_name": "AWS Step Functions",
                "resources": ["stepfunctions.state_machine", "stepfunctions.execution"],
                "description": "Workflow orchestration"
            },
            "appsync": {
                "service_name": "AWS AppSync",
                "resources": ["appsync.graphql_api", "appsync.resolver", "appsync.data_source"],
                "description": "GraphQL API service"
            }
        },
        
        # Analytics & Big Data
        "analytics": {
            "kinesis": {
                "service_name": "Amazon Kinesis",
                "resources": ["kinesis.stream", "kinesis.firehose", "kinesis.analytics"],
                "description": "Real-time data streaming"
            },
            "emr": {
                "service_name": "Amazon EMR",
                "resources": ["emr.cluster", "emr.step", "emr.instance_group"],
                "description": "Big data processing"
            },
            "glue": {
                "service_name": "AWS Glue",
                "resources": ["glue.job", "glue.crawler", "glue.database", "glue.table"],
                "description": "ETL and data catalog"
            },
            "athena": {
                "service_name": "Amazon Athena",
                "resources": ["athena.query", "athena.workgroup"],
                "description": "Interactive query service"
            },
            "quicksight": {
                "service_name": "Amazon QuickSight",
                "resources": ["quicksight.dashboard", "quicksight.dataset", "quicksight.analysis"],
                "description": "Business intelligence"
            }
        },
        
        # Machine Learning & AI
        "machine_learning": {
            "sagemaker": {
                "service_name": "Amazon SageMaker",
                "resources": ["sagemaker.model", "sagemaker.endpoint", "sagemaker.training_job", "sagemaker.notebook_instance"],
                "description": "Machine learning platform"
            },
            "comprehend": {
                "service_name": "Amazon Comprehend",
                "resources": ["comprehend.document_classifier", "comprehend.entity_recognizer"],
                "description": "Natural language processing"
            },
            "rekognition": {
                "service_name": "Amazon Rekognition",
                "resources": ["rekognition.collection", "rekognition.face"],
                "description": "Image and video analysis"
            },
            "polly": {
                "service_name": "Amazon Polly",
                "resources": ["polly.voice", "polly.lexicon"],
                "description": "Text-to-speech service"
            },
            "transcribe": {
                "service_name": "Amazon Transcribe",
                "resources": ["transcribe.job", "transcribe.vocabulary"],
                "description": "Speech-to-text service"
            }
        },
        
        # Developer Tools
        "developer_tools": {
            "codecommit": {
                "service_name": "AWS CodeCommit",
                "resources": ["codecommit.repository", "codecommit.branch"],
                "description": "Source control service"
            },
            "codebuild": {
                "service_name": "AWS CodeBuild",
                "resources": ["codebuild.project", "codebuild.build"],
                "description": "Build service"
            },
            "codedeploy": {
                "service_name": "AWS CodeDeploy",
                "resources": ["codedeploy.application", "codedeploy.deployment_group", "codedeploy.deployment"],
                "description": "Deployment service"
            },
            "codepipeline": {
                "service_name": "AWS CodePipeline",
                "resources": ["codepipeline.pipeline", "codepipeline.stage", "codepipeline.action"],
                "description": "CI/CD pipeline service"
            },
            "ecr": {
                "service_name": "Amazon Elastic Container Registry",
                "resources": ["ecr.repository", "ecr.image", "ecr.lifecycle_policy"],
                "description": "Container image registry"
            }
        },
        
        # Management & Governance
        "management": {
            "organizations": {
                "service_name": "AWS Organizations",
                "resources": ["organizations.org", "organizations.account", "organizations.policy", "organizations.ou"],
                "description": "Multi-account management"
            },
            "cloudformation": {
                "service_name": "AWS CloudFormation",
                "resources": ["cloudformation.stack", "cloudformation.stack_set", "cloudformation.template"],
                "description": "Infrastructure as code"
            },
            "cloudformation_stack_sets": {
                "service_name": "AWS CloudFormation Stack Sets",
                "resources": ["cloudformation_stack_sets.stack_set", "cloudformation_stack_sets.stack_instance"],
                "description": "Multi-region stack management"
            },
            "service_catalog": {
                "service_name": "AWS Service Catalog",
                "resources": ["servicecatalog.portfolio", "servicecatalog.product", "servicecatalog.provisioned_product"],
                "description": "IT service management"
            },
            "trusted_advisor": {
                "service_name": "AWS Trusted Advisor",
                "resources": ["trustedadvisor.check", "trustedadvisor.recommendation"],
                "description": "Best practice recommendations"
            },
            "wellarchitected": {
                "service_name": "AWS Well-Architected Tool",
                "resources": ["wellarchitected.workload", "wellarchitected.review", "wellarchitected.improvement"],
                "description": "Architecture review tool"
            }
        },
        
        # Backup & Disaster Recovery
        "backup_recovery": {
            "backup": {
                "service_name": "AWS Backup",
                "resources": ["backup.plan", "backup.vault", "backup.job", "backup.recovery_point"],
                "description": "Centralized backup service"
            },
            "drs": {
                "service_name": "AWS Elastic Disaster Recovery",
                "resources": ["drs.replication_configuration", "drs.source_server", "drs.replication_job"],
                "description": "Disaster recovery service"
            },
            "cloudendure": {
                "service_name": "AWS CloudEndure",
                "resources": ["cloudendure.machine", "cloudendure.replication_job"],
                "description": "Migration and disaster recovery"
            }
        },
        
        # Cost Management
        "cost_management": {
            "budgets": {
                "service_name": "AWS Budgets",
                "resources": ["budgets.budget", "budgets.budget_action"],
                "description": "Cost and usage budgets"
            },
            "costexplorer": {
                "service_name": "AWS Cost Explorer",
                "resources": ["costexplorer.report", "costexplorer.anomaly_detector"],
                "description": "Cost analysis and reporting"
            },
            "cur": {
                "service_name": "AWS Cost and Usage Report",
                "resources": ["cur.report", "cur.report_definition"],
                "description": "Detailed billing reports"
            }
        },
        
        # Migration & Transfer
        "migration": {
            "dms": {
                "service_name": "AWS Database Migration Service",
                "resources": ["dms.replication_instance", "dms.replication_task", "dms.endpoint"],
                "description": "Database migration service"
            },
            "snowball": {
                "service_name": "AWS Snowball",
                "resources": ["snowball.job", "snowball.cluster"],
                "description": "Data transfer service"
            },
            "datasync": {
                "service_name": "AWS DataSync",
                "resources": ["datasync.task", "datasync.location", "datasync.agent"],
                "description": "Data transfer service"
            },
            "mgn": {
                "service_name": "AWS Application Migration Service",
                "resources": ["mgn.source_server", "mgn.replication_job", "mgn.launch_configuration"],
                "description": "Application migration service"
            }
        },
        
        # Mobile & IoT
        "mobile_iot": {
            "iot": {
                "service_name": "AWS IoT Core",
                "resources": ["iot.thing", "iot.thing_type", "iot.thing_group", "iot.policy", "iot.certificate"],
                "description": "Internet of Things platform"
            },
            "iot_device_defender": {
                "service_name": "AWS IoT Device Defender",
                "resources": ["iot_device_defender.audit", "iot_device_defender.mitigation_action"],
                "description": "IoT security monitoring"
            },
            "iot_analytics": {
                "service_name": "AWS IoT Analytics",
                "resources": ["iot_analytics.dataset", "iot_analytics.pipeline", "iot_analytics.channel"],
                "description": "IoT data analytics"
            },
            "mobile": {
                "service_name": "AWS Mobile",
                "resources": ["mobile.project", "mobile.app"],
                "description": "Mobile app development"
            }
        },
        
        # Game Development
        "gaming": {
            "gamelift": {
                "service_name": "Amazon GameLift",
                "resources": ["gamelift.fleet", "gamelift.game_session", "gamelift.build"],
                "description": "Game server hosting"
            },
            "lumberyard": {
                "service_name": "Amazon Lumberyard",
                "resources": ["lumberyard.project", "lumberyard.resource"],
                "description": "Game engine and tools"
            }
        },
        
        # Media Services
        "media": {
            "mediaconvert": {
                "service_name": "AWS Elemental MediaConvert",
                "resources": ["mediaconvert.job", "mediaconvert.job_template", "mediaconvert.preset"],
                "description": "Video transcoding service"
            },
            "medialive": {
                "service_name": "AWS Elemental MediaLive",
                "resources": ["medialive.channel", "medialive.input", "medialive.multiplex"],
                "description": "Live video processing"
            },
            "mediapackage": {
                "service_name": "AWS Elemental MediaPackage",
                "resources": ["mediapackage.channel", "mediapackage.endpoint"],
                "description": "Video packaging service"
            },
            "mediastore": {
                "service_name": "AWS Elemental MediaStore",
                "resources": ["mediastore.container", "mediastore.object"],
                "description": "Media storage service"
            }
        },
        
        # Blockchain
        "blockchain": {
            "managed_blockchain": {
                "service_name": "Amazon Managed Blockchain",
                "resources": ["managed_blockchain.network", "managed_blockchain.member", "managed_blockchain.node"],
                "description": "Blockchain network management"
            },
            "qldb": {
                "service_name": "Amazon Quantum Ledger Database",
                "resources": ["qldb.ledger", "qldb.stream"],
                "description": "Immutable ledger database"
            }
        },
        
        # Quantum Computing
        "quantum": {
            "braket": {
                "service_name": "Amazon Braket",
                "resources": ["braket.task", "braket.device"],
                "description": "Quantum computing service"
            }
        },
        
        # Satellite
        "satellite": {
            "ground_station": {
                "service_name": "AWS Ground Station",
                "resources": ["ground_station.contact", "ground_station.mission_profile"],
                "description": "Satellite ground station service"
            }
        }
    }
    
    return aws_services


def create_coverage_verification_matrix(domains: Dict[str, Any], aws_services: Dict[str, Any]) -> Dict[str, Any]:
    """Create a verification matrix to ensure complete coverage"""
    
    verification_matrix = {
        "summary": {
            "total_domains": len(domains),
            "total_aws_service_categories": len(aws_services),
            "total_aws_services": sum(len(category) for category in aws_services.values()),
            "generated_at": datetime.utcnow().isoformat() + "Z"
        },
        "domains": domains,
        "aws_services": aws_services,
        "coverage_checklist": {
            "domain_subcat_combinations": [],
            "aws_service_coverage": {},
            "missing_services": [],
            "recommendations": []
        }
    }
    
    # Generate domain+subcat combinations for verification
    for domain_key, domain_info in domains.items():
        for subcat in domain_info["subcategories"]:
            verification_matrix["coverage_checklist"]["domain_subcat_combinations"].append({
                "domain_key": domain_key,
                "domain_name": domain_info["domain_name"],
                "subcat_id": subcat["subcat_id"],
                "subcat_title": subcat["title"],
                "combination_key": f"{domain_key}.{subcat['subcat_id']}"
            })
    
    # Create AWS service coverage checklist
    for category, services in aws_services.items():
        verification_matrix["coverage_checklist"]["aws_service_coverage"][category] = {
            "category_name": category,
            "services": list(services.keys()),
            "total_services": len(services),
            "covered": False  # To be updated during actual coverage verification
        }
    
    return verification_matrix


def main() -> None:
    """Main function"""
    print("Creating AWS Domain and Services Coverage Verification...")
    
    # Load input files
    taxonomy = load_json(TAXONOMY_PATH)
    assertions = load_json(ASSERTIONS_PATH)
    
    # Extract domains and subcategories
    domains = get_all_domains_and_subcategories(taxonomy)
    print(f"Found {len(domains)} domains with subcategories")
    
    # Get comprehensive AWS services
    aws_services = get_comprehensive_aws_services()
    total_services = sum(len(category) for category in aws_services.values())
    print(f"Found {len(aws_services)} AWS service categories with {total_services} total services")
    
    # Create domain and services list
    domain_services_data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_taxonomy": os.path.basename(TAXONOMY_PATH),
        "source_assertions": os.path.basename(ASSERTIONS_PATH),
        "domains": domains,
        "aws_services": aws_services,
        "summary": {
            "total_domains": len(domains),
            "total_aws_service_categories": len(aws_services),
            "total_aws_services": total_services
        }
    }
    
    # Create coverage verification matrix
    coverage_matrix = create_coverage_verification_matrix(domains, aws_services)
    
    # Save outputs
    save_json(DOMAIN_SERVICES_OUTPUT, domain_services_data)
    save_json(COVERAGE_MATRIX_OUTPUT, coverage_matrix)
    
    print(f"Saved domain and services list to {DOMAIN_SERVICES_OUTPUT}")
    print(f"Saved coverage verification matrix to {COVERAGE_MATRIX_OUTPUT}")
    print(f"Total domain+subcat combinations: {len(coverage_matrix['coverage_checklist']['domain_subcat_combinations'])}")
    print(f"Total AWS services to verify: {total_services}")


if __name__ == "__main__":
    main()
