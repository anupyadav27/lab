#!/usr/bin/env ts-node

import { program } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import { z } from 'zod';
import { AssertionsPackSchema, type Assertion } from '../schemas/assertions.schema';
import { RulesPackSchema, type Rule } from '../schemas/rules.schema';
import { MatrixSchema, type Matrix } from '../schemas/matrix.schema';
import { GenerationProfileSchema, type GenerationProfile } from '../schemas/profile.schema';

// Pass condition templates - Specific templates for common services
const PASS_CONDITION_TEMPLATES: Record<string, string> = {
  // S3 & Storage
  'aws.s3.encryption': 'bucket_encryption.enabled == true',
  'aws.s3.public_access_block': 'bucket.block_public_access.enabled == true',
  'aws.s3.access_logging': 'bucket.logging.enabled == true',
  'aws.s3.versioning': 'bucket.versioning.enabled == true',
  'aws.s3.lifecycle_policies': 'bucket.lifecycle_rules.length > 0',
  'aws.s3.object_locking': 'bucket.object_lock_configuration.enabled == true',
  'aws.s3.data_classification': 'bucket.tags.classification != null',
  'aws.s3.retention_policies_enforced': 'bucket.lifecycle_rules.length > 0',
  'aws.s3.secure_deletion_enabled': 'bucket.lifecycle_rules.secure_deletion == true',
  
  // EBS & Compute Storage
  'aws.ebs.default_encryption': 'ebs.default_encryption == true',
  'aws.ebs.snapshots': 'snapshot.status == "available"',
  'aws.efs.encrypted': 'filesystem.encrypted == true',
  'aws.efs.access_points': 'access_point.status == "available"',
  'aws.fsx.access_control': 'filesystem.administrative_actions.length > 0',
  
  // RDS & Databases
  'aws.rds.storage_encrypted': 'rds.storage_encrypted == true',
  'aws.rds.snapshots': 'snapshot.status == "available"',
  'aws.rds.multi_az': 'instance.multi_az == true',
  'aws.rds.ssl_enforcement': 'instance.ssl_enforcement == true',
  'aws.rds.data_masking': 'instance.masking_policy != null',
  'aws.rds.master_key_rotation': 'instance.master_key_rotation == true',
  'aws.redshift.encrypted': 'cluster.encrypted == true',
  'aws.redshift.ssl_enforcement': 'cluster.ssl_enforcement == true',
  'aws.redshift.data_masking': 'cluster.masking_policy != null',
  'aws.dynamodb.sse': 'table.sse.enabled == true',
  'aws.dynamodb.point_in_time_recovery': 'table.point_in_time_recovery.enabled == true',
  'aws.dynamodb.data_masking': 'table.masking_policy != null',
  'aws.elasticache.at_rest_encryption': 'cluster.at_rest_encryption_enabled == true',
  'aws.elasticache.in_transit_encryption': 'cluster.transit_encryption_enabled == true',
  'aws.elasticache.cluster_mode': 'cluster.cluster_mode == "enabled"',
  'aws.opensearch.encryption_at_rest': 'domain.encryption_at_rest.enabled == true',
  'aws.opensearch.log_analysis': 'domain.log_publishing_options.enabled == true',
  'aws.neptune.encryption_at_rest': 'cluster.encryption_at_rest == true',
  
  // IAM & Access Management
  'aws.iam.account_password_policy': 'password_policy.min_length >= 14',
  'aws.iam.mfa': 'user.mfa_devices.length > 0',
  'aws.iam.role_policies': 'role.managed_policies.length > 0 || role.inline_policies.length > 0',
  'aws.iam.managed_policies': 'role.managed_policies.length > 0',
  'aws.iam.inline_policies': 'role.inline_policies.length > 0',
  'aws.iam.permission_boundaries': 'role.permission_boundary != null',
  'aws.iam.saml_providers': 'saml_provider.status == "ACTIVE"',
  'aws.iam.oidc_providers': 'oidc_provider.status == "ACTIVE"',
  'aws.iam.role_definitions': 'role.assume_role_policy_document != null',
  'aws.iam.role_assignments': 'role.attached_policies.length > 0',
  'aws.iam.least_privilege_analysis': 'access_analyzer.findings.length == 0',
  'aws.iam.entitlement_policies': 'policy.policy_document != null',
  'aws.iam.role_permissions': 'role.attached_policies.length > 0',
  'aws.iam.organization_policies': 'policy.type == "SERVICE_CONTROL_POLICY"',
  'aws.iam.resource_based_policies': 'policy.resource_based == true',
  'aws.iam.crypto_policies': 'policy.crypto_requirements != null',
  'aws.iam.session_duration': 'role.max_session_duration <= 3600',
  'aws.iam.cross_account_access_controlled': 'role.external_id != null',
  'aws.iam.external_idp_configured': 'identity_provider.status == "ACTIVE"',
  'aws.iam.permission_boundaries_enforced': 'role.permission_boundary != null',
  'aws.iam.resource_policies_configured': 'policy.resource_based == true',
  'aws.iam.trust_relationships_managed': 'role.trust_policy != null',
  'aws.iam.conditional_access_enabled': 'policy.conditions != null',
  'aws.iam.least_privilege_analysis': 'access_analyzer.findings.length == 0',
  'aws.iam.entitlement_management': 'policy.entitlements != null',
  
  // Cognito & Identity Services
  'aws.cognito.user_pool_policies': 'user_pool.policies != null',
  'aws.cognito.identity_pools': 'identity_pool.status == "ENABLED"',
  'aws.cognito.mfa_settings': 'user_pool.mfa_configuration.enabled == true',
  'aws.cognito.session_settings': 'user_pool.session_timeout > 0',
  'aws.sso.instance_settings': 'instance.status == "ACTIVE"',
  'aws.sso.mfa': 'instance.mfa_configuration.enabled == true',
  'aws.sso.session_settings': 'instance.session_timeout > 0',
  'aws.sso.external_identity_providers': 'identity_provider.status == "ACTIVE"',
  'aws.ds.directory_settings': 'directory.status == "ACTIVE"',
  'aws.ds.trust_relationships': 'trust.status == "ACTIVE"',
  
  // VPC & Networking
  'aws.ec2.security_groups': 'sg.has_ingress_open_to_world == false && sg.has_egress_any_any == false',
  'aws.ec2.network_acls': 'nacl.entries.length > 0',
  'aws.ec2.vpc_segmentation': 'vpc.is_default == false',
  'aws.ec2.subnet_segmentation': 'subnet.availability_zone != null',
  'aws.ec2.route_tables': 'route_table.routes.length > 0',
  'aws.ec2.vpc_endpoints': 'endpoint.policy_document != null',
  'aws.ec2.vpc_endpoints_policy_enforcement': 'endpoint.policy_enforcement == true',
  'aws.ec2.vpc_peering': 'peering.status == "active"',
  'aws.network_firewall.policy': 'firewall_policy.state == "ACTIVE"',
  'aws.r53r.df.rule_groups': 'rule_group.status == "ACTIVE"',
  'aws.route53.dns_security': 'hosted_zone.private_zone == true',
  'aws.route53.resolver_rules': 'resolver_rule.status == "COMPLETE"',
  'aws.route53.health_checks': 'health_check.status == "HEALTHY"',
  'aws.route53.resolver_dns_firewall': 'dns_firewall.status == "ACTIVE"',
  
  // Load Balancing
  'aws.elb.load_balancer_security': 'load_balancer.scheme == "internal"',
  'aws.elb.ssl_termination': 'listener.ssl_policy != null',
  'aws.elb.high_availability': 'load_balancer.availability_zones.length > 1',
  'aws.alb.load_balancer_security': 'load_balancer.scheme == "internal"',
  'aws.nlb.load_balancer_security': 'load_balancer.scheme == "internal"',
  'aws.cloudfront.https_enforcement': 'distribution.viewer_certificate.ssl_support_method == "sni-only"',
  'aws.cloudfront.distribution_security': 'distribution.origins.origin_protocol_policy == "https-only"',
  
  // VPN & Connectivity
  'aws.ec2.vpn_connections': 'vpn_connection.state == "available"',
  'aws.directconnect.connections': 'connection.connection_state == "up"',
  'aws.ec2.transit_gateway': 'transit_gateway.state == "available"',
  
  // Compute & Host Security
  'aws.ec2.os_hardening': 'instance.platform == "linux"',
  'aws.ec2.launch_template_hardening': 'launch_template.latest_version > 1',
  'aws.ec2.ami_hardening': 'ami.state == "available"',
  'aws.ec2.endpoint_protection': 'instance.security_groups.length > 0',
  'aws.ec2.instance_security': 'instance.security_groups.length > 0',
  'aws.ssm.patch_management': 'patch_baseline.operating_system != null',
  'aws.ssm.patch_groups': 'patch_group.patch_baseline_id != null',
  'aws.ssm.maintenance_windows': 'maintenance_window.schedule != null',
  'aws.ssm.patch_deployment': 'patch_group.patch_baseline_id != null',
  'aws.ssm.automated_patching': 'maintenance_window.schedule != null',
  'aws.ssm.security_updates': 'patch_baseline.operating_system != null',
  'aws.inspector.assessments': 'assessment.state == "COMPLETED"',
  'aws.inspector.vulnerability_assessments': 'assessment.findings.length > 0',
  'aws.inspector.vulnerability_scanning': 'assessment.state == "COMPLETED"',
  'aws.guardduty.threat_detection': 'detector.status == "ENABLED"',
  'aws.guardduty.detector': 'detector.status == "ENABLED"',
  'aws.security_hub.findings': 'hub.findings.length > 0',
  'aws.security_hub.compliance_frameworks': 'hub.standards.length > 0',
  'aws.security_hub.compliance_standards': 'hub.standards.length > 0',
  'aws.security_hub.vulnerability_findings': 'hub.findings.length > 0',
  'aws.macie.data_classification': 'job.status == "COMPLETED"',
  'aws.macie.sensitive_data_discovery': 'job.findings.length > 0',
  'aws.config.compliance_rules': 'config_rule.state == "ACTIVE"',
  'aws.config.audit_rules': 'config_rule.source.source_identifier != null',
  'aws.config.compliance_framework': 'config_rule.compliance_type != null',
  'aws.audit_manager.assessments': 'assessment.status == "ACTIVE"',
  'aws.audit_manager.compliance_assessments': 'assessment.framework_id != null',
  'aws.audit_manager.compliance_assessments': 'assessment.framework_id != null',
  
  // Containers & Kubernetes
  'aws.ecr.image_scanning': 'repository.image_scanning_configuration.scan_on_push == true',
  'aws.ecr.registry_security': 'repository.encryption_configuration.encryption_type != "NONE"',
  'aws.ecr.repository_policies': 'repository.policy_text != null',
  'aws.ecr.lifecycle_policies': 'repository.lifecycle_policy_text != null',
  'aws.ecr.dependency_scanning': 'repository.image_scanning_configuration.scan_on_push == true',
  'aws.ecr.vulnerability_scanning': 'repository.image_scanning_configuration.scan_on_push == true',
  'aws.ecr.software_bill_of_materials': 'repository.sbom_configuration.enabled == true',
  'aws.ecr.image_signing': 'repository.image_signing_configuration.enabled == true',
  'aws.eks.runtime_security': 'cluster.logging.enabled == true',
  'aws.eks.cluster_logging': 'cluster.logging.enabled == true',
  'aws.eks.network_policies': 'cluster.network_config.service_ipv4_cidr != null',
  'aws.eks.rbac_configuration': 'cluster.identity.oidc.issuer != null',
  'aws.eks.node_security': 'node_group.status == "ACTIVE"',
  'aws.eks.fargate_security': 'fargate_profile.status == "ACTIVE"',
  'aws.eks.cni_addon': 'addon.status == "ACTIVE"',
  'aws.eks.service_mesh': 'addon.service_mesh.enabled == true',
  'aws.eks.oidc_identity_provider': 'cluster.identity.oidc.issuer != null',
  'aws.eks.admission_controllers': 'cluster.admission_controllers.enabled == true',
  'aws.eks.opa_gatekeeper': 'addon.gatekeeper.enabled == true',
  'aws.eks.kyverno_policies': 'addon.kyverno.enabled == true',
  'aws.eks.service_roles': 'cluster.service_role_arn != null',
  'aws.eks.version_management': 'cluster.version != null',
  
  // Serverless & PaaS
  'aws.lambda.function_security': 'function.runtime != null',
  'aws.lambda.layer_security': 'layer.version != null',
  'aws.lambda.code_signing': 'function.code_signing_config != null',
  'aws.lambda.resource_limits': 'function.timeout <= 300',
  'aws.lambda.deprecation_management': 'function.runtime != "deprecated"',
  'aws.apigateway.api_security': 'api.protocol_type == "HTTP"',
  'aws.apigateway.ssl_enforcement': 'api.protocol_type == "HTTP"',
  'aws.apigateway.rate_limiting': 'api.throttle.burst_limit > 0',
  'aws.apigateway.api_keys': 'api_key.enabled == true',
  'aws.apigateway.api_management': 'api.name != null',
  'aws.apigateway.api_versioning': 'api.version != null',
  'aws.apigateway.api_documentation': 'api.documentation != null',
  'aws.apigateway.resource_limits': 'api.throttle.burst_limit > 0',
  'aws.elasticbeanstalk.application_security': 'application.version_label != null',
  'aws.elasticbeanstalk.resource_limits': 'application.max_count <= 10',
  'aws.apprunner.service_security': 'service.status == "RUNNING"',
  'aws.lightsail.instance_security': 'instance.state.name == "running"',
  'aws.lightsail.resource_limits': 'instance.bundle_id != null',
  
  // Event & Messaging
  'aws.eventbridge.rule_security': 'rule.state == "ENABLED"',
  'aws.eventbridge.rule_security': 'rule.state == "ENABLED"',
  'aws.sqs.queue_security': 'queue.visibility_timeout_seconds > 0',
  'aws.sns.topic_security': 'topic.subscriptions.length > 0',
  'aws.sns.alerting_topics': 'topic.subscriptions.length > 0',
  
  // Monitoring & Logging
  'aws.cloudtrail.log_collection': 'trail.logging_enabled == true',
  'aws.cloudtrail.audit_logging': 'trail.logging_enabled == true',
  'aws.cloudtrail.log_retention': 'trail.log_retention_days >= 90',
  'aws.cloudtrail.insights': 'trail.insights_enabled == true',
  'aws.cloudwatch.alarms': 'alarm.state_value == "OK"',
  'aws.cloudwatch.dashboards': 'dashboard.body != null',
  'aws.cloudwatch.log_retention': 'log_group.retention_in_days >= 30',
  'aws.cloudwatch.insights_queries': 'insights_query.status == "COMPLETED"',
  'aws.cloudwatch.log_collection': 'log_group.log_streams.length > 0',
  'aws.cloudwatch.platform_monitoring': 'alarm.metric_name != null',
  'aws.cloudwatch.platform_dashboards': 'dashboard.name != null',
  'aws.vpc-flow-logs.vpc_flow_logs': 'flow_logs.status == "ACTIVE"',
  'aws.athena.log_analysis': 'query.status == "SUCCEEDED"',
  'aws.opensearch.log_analysis': 'domain.log_publishing_options.enabled == true',
  'aws.xray.platform_tracing': 'trace.id != null',
  
  // Backup & Recovery
  'aws.backup.backup_strategy': 'vault.backup_plans.length > 0',
  'aws.backup.backup_plans': 'backup_plan.backup_plan_rules.length > 0',
  'aws.backup.backup_selections': 'backup_selection.iam_role_arn != null',
  'aws.backup.disaster_recovery': 'backup_vault.encryption_key_arn != null',
  'aws.backup.recovery_testing': 'backup_vault.test_mode == true',
  'aws.drs.replication': 'replication_configuration.state == "ACTIVE"',
  'aws.drs.recovery_testing': 'replication_configuration.test_mode == true',
  'aws.fis.chaos_engineering': 'experiment.state == "RUNNING"',
  
  // Governance & Compliance
  'aws.organizations.policy_management': 'policy.content != null',
  'aws.organizations.resource_governance': 'policy.type == "SERVICE_CONTROL_POLICY"',
  'aws.tag.resource_tagging': 'tags.length > 0',
  'aws.resource_groups.governance': 'group.resource_query != null',
  'aws.budgets.cost_governance': 'budget.budget_limit.amount > 0',
  'aws.cost_explorer.cost_analysis': 'cost_explorer.report_definition != null',
  'aws.budgets.cost_anomaly_detection': 'budget.anomaly_detection.enabled == true',
  'aws.access_analyzer.findings': 'analyzer.status == "ACTIVE"',
  'aws.access_analyzer.policy_analysis': 'analyzer.findings.length > 0',
  
  // Platform & Versioning
  'aws.ec2.version_management': 'instance.platform_version != null',
  'aws.rds.version_management': 'instance.engine_version != null',
  'aws.eks.version_management': 'cluster.version != null',
  'aws.ec2.deprecation_management': 'instance.platform_version != "deprecated"',
  'aws.rds.deprecation_management': 'instance.engine_version != "deprecated"',
  'aws.lambda.deprecation_management': 'function.runtime != "deprecated"',
  
  // Supply Chain & Registries
  'aws.codebuild.build_security': 'project.encryption_key != null',
  'aws.codebuild.artifact_signing': 'project.artifacts.encryption_disabled == false',
  'aws.codepipeline.pipeline_security': 'pipeline.encryption_key != null',
  'aws.codecommit.repository_security': 'repository.encryption_configuration.encryption_type != "NONE"',
  'aws.signer.code_signing': 'signing_profile.status == "ACTIVE"',
  'aws.codeartifact.dependency_management': 'repository.external_connections.length > 0',
  
  // WAF & Security Services
  'aws.wafv2.cloudfront_web_acl': 'distribution.associated_web_acl == true',
  'aws.wafv2.web_acl': 'web_acl.rules.length > 0',
  'aws.wafv2.managed_rules': 'web_acl.managed_rule_groups.length > 0',
  
  // KMS & Encryption
  'aws.kms.key_rotation': 'key.rotation_enabled == true',
  'aws.kms.key_management': 'key.key_usage == "ENCRYPT_DECRYPT"',
  'aws.kms.customer_managed_keys': 'key.origin == "AWS_KMS"',
  'aws.kms.key_policies': 'key.policy != null',
  'aws.kms.hsm_protection': 'key.origin == "EXTERNAL"',
  'aws.kms.key_storage': 'key.state == "Enabled"',
  'aws.kms.key_usage': 'key.key_usage != null',
  'aws.kms.import_key_material': 'key.origin == "EXTERNAL"',
  'aws.kms.crypto_policies': 'key.policy.crypto_requirements != null',
  
  // ACM & Certificates
  'aws.acm.certificate_management': 'certificate.status == "ISSUED"',
  'aws.acm.private_ca': 'certificate_authority.status == "ACTIVE"',
  'aws.acm.certificate_authority': 'certificate_authority.status == "ACTIVE"',
  
  // Secrets Management
  'aws.secrets_manager.secret_storage': 'secret.status == "Active"',
  'aws.secrets_manager.rotation': 'secret.rotation_enabled == true',
  'aws.secrets_manager.retrieval': 'secret.retrieval_enabled == true',
  'aws.ssm.parameter_storage': 'parameter.type == "SecureString"',
  'aws.ssm.parameter_retrieval': 'parameter.tier == "Advanced"',
  
  // Directory Services
  'aws.ds.directory_settings': 'directory.status == "ACTIVE"',
  'aws.ds.trust_relationships': 'trust.status == "ACTIVE"',
  
  // Cost Management
  'aws.budgets.cost_governance': 'budget.budget_limit.amount > 0',
  'aws.cost_explorer.cost_analysis': 'cost_explorer.report_definition != null',
  'aws.budgets.cost_anomaly_detection': 'budget.anomaly_detection.enabled == true'
};

// Severity escalation keywords
const HIGH_SEVERITY_KEYWORDS = ['MFA', 'encryption', 'deny-all', 'critical', 'admin', 'root', 'privilege'];

function getPassCondition(adapter: string): string {
  return PASS_CONDITION_TEMPLATES[adapter] || 'TBD-by-adapter';
}

function determineSeverity(assertion: Assertion): 'low' | 'medium' | 'high' {
  const title = assertion.title.toLowerCase();
  
  // Check for high severity keywords
  if (HIGH_SEVERITY_KEYWORDS.some(keyword => title.includes(keyword.toLowerCase()))) {
    return 'high';
  }
  
  // Use assertion severity if available
  if (assertion.severity) {
    switch (assertion.severity) {
      case 'critical':
      case 'high':
        return 'high';
      case 'medium':
        return 'medium';
      case 'low':
        return 'low';
    }
  }
  
  return 'medium';
}

function getCoverageTier(selectedTier: 'core' | 'extended' | 'exhaustive'): string[] {
  const tiers = ['core'];
  if (selectedTier === 'extended' || selectedTier === 'exhaustive') {
    tiers.push('extended');
  }
  if (selectedTier === 'exhaustive') {
    tiers.push('exhaustive');
  }
  return tiers;
}

function generateRuleId(service: string, assertionId: string): string {
  const assertionTail = assertionId.split('.').slice(2).join('.');
  return `aws.${service}.${assertionTail}`;
}

function shouldIncludeService(service: string, profile: GenerationProfile): boolean {
  const { include_services, exclude_services } = profile.generation_profile;
  
  // If include_services is specified and not empty, only include those services
  if (include_services && include_services.length > 0) {
    return include_services.includes(service);
  }
  
  // If exclude_services is specified, exclude those services
  if (exclude_services && exclude_services.length > 0) {
    return !exclude_services.includes(service);
  }
  
  return true;
}

function generateRules(
  assertions: Assertion[],
  matrix: Matrix,
  profile: GenerationProfile
): Rule[] {
  const rules: Rule[] = [];
  const selectedTier = profile.generation_profile.coverage;
  const coverageTiers = getCoverageTier(selectedTier);
  
  for (const assertion of assertions) {
    const assertionFamily = assertion.assertion_id.split('.').slice(0, 2).join('.');
    const matrixEntry = matrix[assertionFamily];
    
    if (!matrixEntry) {
      console.warn(`No matrix entry found for assertion family: ${assertionFamily}`);
      continue;
    }
    
    // Get all services for the selected coverage tiers
    const allServices: Array<{ service: string; resource: string; adapter: string; tier: string }> = [];
    
    for (const tier of coverageTiers) {
      const tierServices = matrixEntry[tier as keyof typeof matrixEntry] || [];
      for (const service of tierServices) {
        allServices.push({ ...service, tier });
      }
    }
    
    // Generate rules for each service
    for (const service of allServices) {
      if (!shouldIncludeService(service.service, profile)) {
        continue;
      }
      
      const rule: Rule = {
        rule_id: generateRuleId(service.service, assertion.assertion_id),
        assertion_id: assertion.assertion_id,
        provider: 'aws',
        service: service.service,
        resource_type: service.resource,
        adapter: service.adapter,
        pass_condition: getPassCondition(service.adapter),
        severity: determineSeverity(assertion),
        coverage_tier: service.tier as 'core' | 'extended' | 'exhaustive',
        evidence_type: assertion.evidence_type === 'log_query' ? 'log' : 
                      assertion.evidence_type === 'runtime_observe' ? 'metric' : 'config_read',
        notes: assertion.notes || undefined
      };
      
      rules.push(rule);
    }
  }
  
  return rules;
}

async function main() {
  program
    .option('-p, --profile <path>', 'Path to generation profile JSON file', 'profiles/aws.core.json')
    .option('-a, --assertions <path>', 'Path to assertions pack JSON file', '../assertions_pack_2025-01-09.json')
    .option('-m, --matrix <path>', 'Path to AWS matrix JSON file', 'matrices/aws.json')
    .option('-o, --output <path>', 'Output path for generated rules', 'out/aws_rules.json')
    .parse();

  const options = program.opts();
  
  try {
    console.log('🚀 Starting AWS rule generation...');
    
    // Load and validate inputs
    console.log('📖 Loading assertions pack...');
    const assertionsData = JSON.parse(fs.readFileSync(options.assertions, 'utf8'));
    const assertionsPack = AssertionsPackSchema.parse(assertionsData);
    
    console.log('📖 Loading AWS matrix...');
    const matrixData = JSON.parse(fs.readFileSync(options.matrix, 'utf8'));
    const matrix = MatrixSchema.parse(matrixData);
    
    console.log('📖 Loading generation profile...');
    const profileData = JSON.parse(fs.readFileSync(options.profile, 'utf8'));
    const profile = GenerationProfileSchema.parse(profileData);
    
    console.log(`📊 Processing ${assertionsPack.assertions.length} assertions for ${profile.generation_profile.coverage} coverage`);
    
    // Generate rules
    const rules = generateRules(assertionsPack.assertions, matrix, profile);
    
    console.log(`✅ Generated ${rules.length} rules`);
    
    // Create output directory if it doesn't exist
    const outputDir = path.dirname(options.output);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    // Create rules pack
    const rulesPack = {
      version: '1.0',
      provider: 'aws' as const,
      coverage: profile.generation_profile.coverage,
      rule_count: rules.length,
      rules: rules
    };
    
    // Validate output
    const validatedRulesPack = RulesPackSchema.parse(rulesPack);
    
    // Write output
    fs.writeFileSync(options.output, JSON.stringify(validatedRulesPack, null, 2));
    
    console.log(`📝 Rules written to ${options.output}`);
    console.log('🎉 Rule generation complete!');
    
    // Print summary
    const tierCounts = rules.reduce((acc, rule) => {
      acc[rule.coverage_tier] = (acc[rule.coverage_tier] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    
    console.log('\n📈 Coverage Summary:');
    Object.entries(tierCounts).forEach(([tier, count]) => {
      console.log(`  ${tier}: ${count} rules`);
    });
    
  } catch (error) {
    console.error('❌ Error generating rules:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
