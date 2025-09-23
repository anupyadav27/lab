#!/usr/bin/env ts-node

import { program } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import { z } from 'zod';
import { AssertionsPackSchema, type Assertion } from '../schemas/assertions.schema';
import { RulesPackSchema, type Rule, type AdapterSpec } from '../schemas/rules.schema';
import { MatrixSchema, type Matrix } from '../schemas/matrix.schema';
import { GenerationProfileSchema, type GenerationProfile } from '../schemas/profile.schema';

// Enhanced pass condition templates with adapter specs
const PASS_CONDITION_TEMPLATES: Record<string, { condition: string; adapter_spec: AdapterSpec }> = {
  // IAM & Authentication
  'aws.iam.root_mfa_status': {
    condition: 'root_mfa_enabled == true',
    adapter_spec: {
      returns: {
        'root_mfa_enabled': 'boolean - whether root user has MFA enabled',
        'root_user_used': 'boolean - whether root user has been used recently'
      }
    }
  },
  'aws.iam.root_account_status': {
    condition: 'resource.root_mfa_enabled == true',
    adapter_spec: {
      returns: {
        'root_mfa_enabled': 'boolean - whether root user has MFA enabled'
      }
    }
  },
  'aws.iam.user_mfa_status': {
    condition: 'len(resource.mfa_devices) >= max(1, params.min_authn_factors_required - 1)',
    adapter_spec: {
      returns: {
        'mfa_devices': 'array of MFA device objects',
        'min_authn_factors_required': 'number - minimum authentication factors required'
      }
    }
  },
  'aws.identity_center.mfa_settings': {
    condition: 'mfa_required == true && instance_has_account_assignments == true',
    adapter_spec: {
      returns: {
        'mfa_required': 'boolean - whether MFA is required',
        'instance_has_account_assignments': 'boolean - whether instance has account assignments',
        'instance_status': 'string - status of the identity center instance'
      }
    }
  },
  
  // S3 & Storage
  'aws.s3.default_encryption': {
    condition: 'bucket_encryption.enabled == true',
    adapter_spec: {
      returns: {
        'bucket_encryption.enabled': 'boolean - whether default encryption is enabled',
        'bucket_encryption.algorithm': 'string - encryption algorithm used',
        'bucket_count': 'number - total number of buckets'
      }
    }
  },
  'aws.s3.public_access_blocked': {
    condition: 'block_public_access.enabled == true && policy_allows_public == false',
    adapter_spec: {
      returns: {
        'block_public_access.enabled': 'boolean - whether public access is blocked',
        'policy_allows_public': 'boolean - whether bucket policy allows public access',
        'acl_public': 'boolean - whether bucket ACL is public'
      }
    }
  },
  
  // RDS & Databases
  'aws.rds.storage_encrypted': {
    condition: 'storage_encrypted == true',
    adapter_spec: {
      returns: {
        'storage_encrypted': 'boolean - whether storage is encrypted',
        'encryption_key': 'string - KMS key used for encryption',
        'instance_count': 'number - total number of RDS instances'
      }
    }
  },
  'aws.rds.instance_encryption': {
    condition: 'resource.storage_encrypted == true',
    adapter_spec: {
      returns: {
        'storage_encrypted': 'boolean - whether storage is encrypted'
      }
    }
  },
  'aws.ebs.volume_encryption': {
    condition: 'resource.encrypted == true',
    adapter_spec: {
      returns: {
        'encrypted': 'boolean - whether volume is encrypted'
      }
    }
  },
  'aws.dynamodb.kms_cmk': {
    condition: 'resource.kms_key_id != null && resource.kms_key_id != "alias/aws/dynamodb"',
    adapter_spec: {
      returns: {
        'kms_key_id': 'string - KMS key ID used for encryption'
      }
    }
  },
  'aws.s3.bucket_kms': {
    condition: 'resource.default_encryption.enabled == true && resource.default_encryption.key_type == "CMK"',
    adapter_spec: {
      returns: {
        'default_encryption.enabled': 'boolean - whether default encryption is enabled',
        'default_encryption.key_type': 'string - type of encryption key (CMK, AES256)'
      }
    }
  },
  
  // Network Security
  'aws.ec2.security_groups_deny_all_default': {
    condition: 'has_ingress_open_to_world == false && has_egress_any_any == false',
    adapter_spec: {
      returns: {
        'has_ingress_open_to_world': 'boolean - whether any SG allows ingress from 0.0.0.0/0',
        'has_egress_any_any': 'boolean - whether any SG allows egress to 0.0.0.0/0',
        'security_group_count': 'number - total number of security groups'
      }
    }
  },
  'aws.wafv2.web_acl': {
    condition: 'len(resource.managed_rule_groups) > 0 && len(resource.associated_resources) > 0',
    adapter_spec: {
      returns: {
        'managed_rule_groups': 'array of managed rule groups',
        'associated_resources': 'array of associated resources'
      }
    }
  },
  'aws.cloudfront.waf_enabled': {
    condition: 'resource.waf_web_acl_id != null',
    adapter_spec: {
      returns: {
        'waf_web_acl_id': 'string with WAF Web ACL ID'
      }
    }
  },
  'aws.ec2.ssh_rdp_restricted': {
    condition: 'ssh_restricted == true && rdp_restricted == true',
    adapter_spec: {
      returns: {
        'ssh_restricted': 'boolean - whether SSH (port 22) is restricted',
        'rdp_restricted': 'boolean - whether RDP (port 3389) is restricted',
        'allowed_cidrs': 'array - list of allowed CIDR blocks'
      }
    }
  },
  
  // Monitoring & Logging
  'aws.cloudtrail.log_collection_enabled': {
    condition: 'logging_enabled == true && multi_region == true',
    adapter_spec: {
      returns: {
        'logging_enabled': 'boolean - whether CloudTrail logging is enabled',
        'multi_region': 'boolean - whether trail covers all regions',
        'log_file_validation': 'boolean - whether log file validation is enabled'
      }
    }
  },
  
  // Backup & Recovery
  'aws.backup.backup_plans_configured': {
    condition: 'backup_plans.length > 0 && vault_encryption_enabled == true',
    adapter_spec: {
      returns: {
        'backup_plans.length': 'number - number of backup plans configured',
        'vault_encryption_enabled': 'boolean - whether backup vault is encrypted',
        'backup_vault_count': 'number - total number of backup vaults'
      }
    }
  }
};

// Severity escalation keywords with impact levels
const SEVERITY_KEYWORDS = {
  critical: ['root', 'admin', 'public', 'unencrypted', 'open', 'disabled'],
  high: ['mfa', 'encryption', 'deny-all', 'privilege', 'authentication', 'authorization'],
  medium: ['logging', 'monitoring', 'backup', 'rotation', 'compliance'],
  low: ['tagging', 'versioning', 'documentation', 'naming']
};

function getPassCondition(adapter: string): { condition: string; adapter_spec?: AdapterSpec } {
  const template = PASS_CONDITION_TEMPLATES[adapter];
  if (template) {
    return template;
  }
  
  // Generic patterns for common service types
  const servicePatterns = {
    'encryption': 'resource.encryption.enabled == true',
    'logging': 'resource.logging.enabled == true',
    'monitoring': 'resource.monitoring.enabled == true',
    'backup': 'resource.backup.enabled == true',
    'security': 'resource.security.enabled == true',
    'compliance': 'resource.compliance.enabled == true',
    'policy': 'resource.policy != null',
    'access': 'resource.access_control.enabled == true',
    'authentication': 'resource.authentication.enabled == true',
    'authorization': 'resource.authorization.enabled == true',
    'audit': 'resource.audit.enabled == true',
    'scanning': 'resource.scanning.enabled == true',
    'assessment': 'resource.assessment.status == "COMPLETED"',
    'vulnerability': 'resource.vulnerability_scanning.enabled == true',
    'threat': 'resource.threat_detection.enabled == true',
    'firewall': 'resource.firewall.enabled == true',
    'network': 'resource.network.enabled == true',
    'load_balancer': 'resource.load_balancer.status == "ACTIVE"',
    'ssl': 'resource.ssl.enabled == true',
    'https': 'resource.https.enabled == true',
    'certificate': 'resource.certificate.status == "ISSUED"',
    'rotation': 'resource.rotation.enabled == true',
    'retention': 'resource.retention.days >= 30',
    'lifecycle': 'resource.lifecycle.enabled == true',
    'versioning': 'resource.versioning.enabled == true',
    'snapshot': 'resource.snapshot.status == "available"',
    'replication': 'resource.replication.enabled == true',
    'disaster_recovery': 'resource.disaster_recovery.enabled == true',
    'high_availability': 'resource.high_availability.enabled == true',
    'multi_az': 'resource.multi_az == true',
    'segmentation': 'resource.segmentation.enabled == true',
    'isolation': 'resource.isolation.enabled == true',
    'hardening': 'resource.hardening.enabled == true',
    'patching': 'resource.patching.enabled == true',
    'updates': 'resource.updates.enabled == true',
    'governance': 'resource.governance.enabled == true',
    'tagging': 'resource.tags.length > 0',
    'cost': 'resource.cost_control.enabled == true',
    'budget': 'resource.budget.limit > 0',
    'anomaly': 'resource.anomaly_detection.enabled == true',
    'analysis': 'resource.analysis.enabled == true',
    'reporting': 'resource.reporting.enabled == true',
    'dashboard': 'resource.dashboard.enabled == true',
    'alerting': 'resource.alerting.enabled == true',
    'notification': 'resource.notification.enabled == true',
    'integration': 'resource.integration.enabled == true',
    'api': 'resource.api.enabled == true',
    'endpoint': 'resource.endpoint.enabled == true',
    'gateway': 'resource.gateway.enabled == true',
    'proxy': 'resource.proxy.enabled == true',
    'cache': 'resource.cache.enabled == true',
    'queue': 'resource.queue.enabled == true',
    'topic': 'resource.topic.enabled == true',
    'stream': 'resource.stream.enabled == true',
    'function': 'resource.function.enabled == true',
    'container': 'resource.container.enabled == true',
    'image': 'resource.image.enabled == true',
    'registry': 'resource.registry.enabled == true',
    'repository': 'resource.repository.enabled == true',
    'pipeline': 'resource.pipeline.enabled == true',
    'build': 'resource.build.enabled == true',
    'deploy': 'resource.deploy.enabled == true',
    'test': 'resource.test.enabled == true',
    'quality': 'resource.quality.enabled == true',
    'signing': 'resource.signing.enabled == true',
    'verification': 'resource.verification.enabled == true',
    'validation': 'resource.validation.enabled == true',
    'checksum': 'resource.checksum.enabled == true',
    'integrity': 'resource.integrity.enabled == true',
    'authenticity': 'resource.authenticity.enabled == true',
    'non_repudiation': 'resource.non_repudiation.enabled == true',
    'confidentiality': 'resource.confidentiality.enabled == true',
    'availability': 'resource.availability.enabled == true',
    'reliability': 'resource.reliability.enabled == true',
    'scalability': 'resource.scalability.enabled == true',
    'performance': 'resource.performance.enabled == true',
    'efficiency': 'resource.efficiency.enabled == true',
    'optimization': 'resource.optimization.enabled == true',
    'tuning': 'resource.tuning.enabled == true',
    'configuration': 'resource.configuration.enabled == true',
    'settings': 'resource.settings.enabled == true',
    'parameters': 'resource.parameters.enabled == true',
    'variables': 'resource.variables.enabled == true',
    'environment': 'resource.environment.enabled == true',
    'deployment': 'resource.deployment.enabled == true',
    'provisioning': 'resource.provisioning.enabled == true',
    'orchestration': 'resource.orchestration.enabled == true',
    'automation': 'resource.automation.enabled == true',
    'workflow': 'resource.workflow.enabled == true',
    'process': 'resource.process.enabled == true',
    'procedure': 'resource.procedure.enabled == true',
    'methodology': 'resource.methodology.enabled == true',
    'framework': 'resource.framework.enabled == true',
    'standard': 'resource.standard.enabled == true',
    'guideline': 'resource.guideline.enabled == true',
    'best_practice': 'resource.best_practice.enabled == true',
    'recommendation': 'resource.recommendation.enabled == true',
    'requirement': 'resource.requirement.enabled == true',
    'specification': 'resource.specification.enabled == true',
    'criteria': 'resource.criteria.enabled == true',
    'threshold': 'resource.threshold.enabled == true',
    'limit': 'resource.limit.enabled == true',
    'quota': 'resource.quota.enabled == true',
    'capacity': 'resource.capacity.enabled == true',
    'allocation': 'resource.allocation.enabled == true',
    'reservation': 'resource.reservation.enabled == true',
    'dedication': 'resource.dedication.enabled == true',
    'separation': 'resource.separation.enabled == true',
    'compartmentalization': 'resource.compartmentalization.enabled == true',
    'boundary': 'resource.boundary.enabled == true',
    'perimeter': 'resource.perimeter.enabled == true',
    'zone': 'resource.zone.enabled == true',
    'region': 'resource.region.enabled == true',
    'availability_zone': 'resource.availability_zone.enabled == true',
    'data_center': 'resource.data_center.enabled == true',
    'facility': 'resource.facility.enabled == true',
    'infrastructure': 'resource.infrastructure.enabled == true',
    'platform': 'resource.platform.enabled == true',
    'service': 'resource.service.enabled == true',
    'component': 'resource.component.enabled == true',
    'module': 'resource.module.enabled == true',
    'feature': 'resource.feature.enabled == true',
    'capability': 'resource.capability.enabled == true',
    'functionality': 'resource.functionality.enabled == true',
    'behavior': 'resource.behavior.enabled == true',
    'characteristic': 'resource.characteristic.enabled == true',
    'attribute': 'resource.attribute.enabled == true',
    'property': 'resource.property.enabled == true',
    'parameter': 'resource.parameter.enabled == true',
    'argument': 'resource.argument.enabled == true',
    'input': 'resource.input.enabled == true',
    'output': 'resource.output.enabled == true',
    'result': 'resource.result.enabled == true',
    'outcome': 'resource.outcome.enabled == true',
    'consequence': 'resource.consequence.enabled == true',
    'effect': 'resource.effect.enabled == true',
    'impact': 'resource.impact.enabled == true',
    'influence': 'resource.influence.enabled == true',
    'change': 'resource.change.enabled == true',
    'modification': 'resource.modification.enabled == true',
    'update': 'resource.update.enabled == true',
    'upgrade': 'resource.upgrade.enabled == true',
    'migration': 'resource.migration.enabled == true',
    'transition': 'resource.transition.enabled == true',
    'transformation': 'resource.transformation.enabled == true',
    'conversion': 'resource.conversion.enabled == true',
    'translation': 'resource.translation.enabled == true',
    'mapping': 'resource.mapping.enabled == true',
    'correlation': 'resource.correlation.enabled == true',
    'association': 'resource.association.enabled == true',
    'relationship': 'resource.relationship.enabled == true',
    'connection': 'resource.connection.enabled == true',
    'link': 'resource.link.enabled == true',
    'bond': 'resource.bond.enabled == true',
    'tie': 'resource.tie.enabled == true',
    'attachment': 'resource.attachment.enabled == true',
    'binding': 'resource.binding.enabled == true',
    'coupling': 'resource.coupling.enabled == true',
    'interconnection': 'resource.interconnection.enabled == true',
    'interdependency': 'resource.interdependency.enabled == true',
    'dependence': 'resource.dependence.enabled == true',
    'reliance': 'resource.reliance.enabled == true',
    'trust': 'resource.trust.enabled == true',
    'confidence': 'resource.confidence.enabled == true',
    'assurance': 'resource.assurance.enabled == true',
    'guarantee': 'resource.guarantee.enabled == true',
    'warranty': 'resource.warranty.enabled == true',
    'promise': 'resource.promise.enabled == true',
    'commitment': 'resource.commitment.enabled == true',
    'obligation': 'resource.obligation.enabled == true',
    'responsibility': 'resource.responsibility.enabled == true',
    'accountability': 'resource.accountability.enabled == true',
    'liability': 'resource.liability.enabled == true',
    'duty': 'resource.duty.enabled == true',
    'role': 'resource.role.enabled == true',
    'purpose': 'resource.purpose.enabled == true',
    'objective': 'resource.objective.enabled == true',
    'goal': 'resource.goal.enabled == true',
    'target': 'resource.target.enabled == true',
    'aim': 'resource.aim.enabled == true',
    'intention': 'resource.intention.enabled == true',
    'plan': 'resource.plan.enabled == true',
    'strategy': 'resource.strategy.enabled == true',
    'approach': 'resource.approach.enabled == true',
    'method': 'resource.method.enabled == true',
    'technique': 'resource.technique.enabled == true',
    'tool': 'resource.tool.enabled == true',
    'instrument': 'resource.instrument.enabled == true',
    'device': 'resource.device.enabled == true',
    'equipment': 'resource.equipment.enabled == true',
    'apparatus': 'resource.apparatus.enabled == true',
    'machinery': 'resource.machinery.enabled == true',
    'system': 'resource.system.enabled == true',
    'mechanism': 'resource.mechanism.enabled == true',
    'activity': 'resource.activity.enabled == true',
    'task': 'resource.task.enabled == true',
    'job': 'resource.job.enabled == true',
    'work': 'resource.work.enabled == true',
    'effort': 'resource.effort.enabled == true',
    'endeavor': 'resource.endeavor.enabled == true',
    'undertaking': 'resource.undertaking.enabled == true',
    'project': 'resource.project.enabled == true',
    'initiative': 'resource.initiative.enabled == true',
    'program': 'resource.program.enabled == true',
    'campaign': 'resource.campaign.enabled == true',
    'mission': 'resource.mission.enabled == true',
    'assignment': 'resource.assignment.enabled == true',
    'charge': 'resource.charge.enabled == true'
  };
  
  // Check for generic patterns
  for (const [pattern, condition] of Object.entries(servicePatterns)) {
    if (adapter.includes(pattern)) {
      return { condition };
    }
  }
  
  // Fallback for truly unique cases
  return { condition: 'TBD-by-adapter' };
}

function determineSeverity(assertion: Assertion): 'low' | 'medium' | 'high' | 'critical' {
  const title = assertion.title.toLowerCase();
  const assertionId = assertion.assertion_id.toLowerCase();
  
  // Check for critical keywords first
  for (const keyword of SEVERITY_KEYWORDS.critical) {
    if (title.includes(keyword) || assertionId.includes(keyword)) {
      return 'critical';
    }
  }
  
  // Check for high keywords
  for (const keyword of SEVERITY_KEYWORDS.high) {
    if (title.includes(keyword) || assertionId.includes(keyword)) {
      return 'high';
    }
  }
  
  // Check for medium keywords
  for (const keyword of SEVERITY_KEYWORDS.medium) {
    if (title.includes(keyword) || assertionId.includes(keyword)) {
      return 'medium';
    }
  }
  
  // Check for low keywords
  for (const keyword of SEVERITY_KEYWORDS.low) {
    if (title.includes(keyword) || assertionId.includes(keyword)) {
      return 'low';
    }
  }
  
  // Default to medium for unknown cases
  return 'medium';
}

function generateRuleId(service: string, assertionId: string, adapter: string, tier: string): string {
  // Use the full assertion ID to ensure uniqueness
  const assertionParts = assertionId.split('.');
  const domainSubcat = assertionParts.slice(0, 2).join('_');
  const assertionTail = assertionParts.slice(2).join('_');
  const tierSuffix = tier !== 'core' ? `_${tier}` : '';
  return `aws.${service}.${domainSubcat}_${assertionTail}${tierSuffix}`;
}

function shouldIncludeService(service: string, profile: GenerationProfile): boolean {
  const { include_services, exclude_services } = profile.generation_profile;
  
  if (include_services && include_services.length > 0 && !include_services.includes(service)) {
    return false;
  }
  
  if (exclude_services && exclude_services.includes(service)) {
    return false;
  }
  
  return true;
}

function isServiceAppropriateForAssertion(assertion: Assertion, service: any): boolean {
  const assertionId = assertion.assertion_id;
  
  // Specific mappings for assertions that need particular services
  const assertionServiceMappings: Record<string, string[]> = {
    'network_perimeter.firewall_rules.waf_enabled': ['wafv2'],
    'network_perimeter.firewall_rules.waf_enabled_at_edge': ['cloudfront'],
    'network_perimeter.firewall_rules.deny_all_default': ['ec2'],
    'network_perimeter.firewall_rules.ssh_rdp_restricted': ['ec2'],
    'network_perimeter.firewall_rules.egress_filtering_enabled': ['ec2'],
    'crypto_data_protection.encryption_at_rest.database_encryption_enabled': ['rds'],
    'crypto_data_protection.encryption_at_rest.volume_encryption_enabled': ['ec2'],
    'crypto_data_protection.encryption_at_rest.customer_managed_keys_used': ['s3', 'kms'],
    'crypto_data_protection.key_management.customer_managed_keys_used': ['s3', 'kms'],
    'identity_access.authentication.strong_authn_enabled': ['iam', 'identity-center', 'cognito']
  };
  
  // Check if there's a specific mapping for this assertion
  const preferredServices = assertionServiceMappings[assertionId];
  if (preferredServices) {
    // Only allow services that are in the preferred list
    return preferredServices.includes(service.service);
  }
  
  // For assertions without specific mappings, allow all services
  return true;
}


function main() {
  program
    .option('-p, --profile <path>', 'Path to generation profile JSON file')
    .option('-o, --output <path>', 'Output path for generated rules', 'out/aws_rules_improved.json')
    .parse();

  const options = program.opts();
  
  if (!options.profile) {
    console.error('Error: --profile is required');
    process.exit(1);
  }

  try {
    // Load and validate inputs
    const assertionsPack = JSON.parse(fs.readFileSync('assertions_pack_2025-01-09.json', 'utf8'));
    const matrix = JSON.parse(fs.readFileSync('matrices/aws_fixed.json', 'utf8'));
    const profile = JSON.parse(fs.readFileSync(options.profile, 'utf8'));

    // Validate schemas
    const validatedAssertions = AssertionsPackSchema.parse(assertionsPack);
    const validatedMatrix = MatrixSchema.parse(matrix);
    const validatedProfile = GenerationProfileSchema.parse(profile);

    console.log(`Loaded ${validatedAssertions.assertions.length} assertions`);
    console.log(`Loaded matrix with ${Object.keys(validatedMatrix).length} assertion families`);
    console.log(`Using profile: ${validatedProfile.generation_profile.provider} ${validatedProfile.generation_profile.coverage}`);

    const rules: Rule[] = [];
    const coverageTier = validatedProfile.generation_profile.coverage;

    // Generate rules for each assertion
    for (const assertion of validatedAssertions.assertions) {
      const assertionFamily = assertion.assertion_id.split('.').slice(0, 2).join('.');
      const familyMatrix = validatedMatrix[assertionFamily];
      
      if (!familyMatrix) {
        console.warn(`No matrix entry for assertion family: ${assertionFamily}`);
        continue;
      }

      // Get services for the selected coverage tier and below
      const allServices = [];
      if (coverageTier === 'exhaustive') {
        allServices.push(...familyMatrix.core.map(s => ({ ...s, tier: 'core' })));
        allServices.push(...familyMatrix.extended.map(s => ({ ...s, tier: 'extended' })));
        allServices.push(...familyMatrix.exhaustive.map(s => ({ ...s, tier: 'exhaustive' })));
      } else if (coverageTier === 'extended') {
        allServices.push(...familyMatrix.core.map(s => ({ ...s, tier: 'core' })));
        allServices.push(...familyMatrix.extended.map(s => ({ ...s, tier: 'extended' })));
      } else {
        allServices.push(...familyMatrix.core.map(s => ({ ...s, tier: 'core' })));
      }

      // Generate rules for each coverage tier (core/extended/exhaustive)
      for (const service of allServices) {
        if (!shouldIncludeService(service.service, validatedProfile)) {
          continue;
        }
        
        // Skip if this service doesn't match the assertion's requirements
        if (!isServiceAppropriateForAssertion(assertion, service)) {
          continue;
        }
        
        const passConditionInfo = getPassCondition(service.adapter);
        
        const rule: Rule = {
          rule_id: generateRuleId(service.service, assertion.assertion_id, service.adapter, service.tier),
          assertion_id: assertion.assertion_id,
          provider: 'aws',
          service: service.service,
          resource_type: service.resource,
          adapter: service.adapter,
          params: assertion.params || undefined,
          pass_condition: passConditionInfo.condition,
          not_applicable_when: service.not_applicable_when || undefined,
          severity: determineSeverity(assertion),
          coverage_tier: service.tier as 'core' | 'extended' | 'exhaustive',
          evidence_type: assertion.evidence_type === 'log_query' ? 'event_log' : 
                        assertion.evidence_type === 'runtime_observe' ? 'runtime_check' : 'config_read',
          rationale: assertion.rationale || `Ensures ${assertion.title.toLowerCase()}`,
          adapter_spec: passConditionInfo.adapter_spec,
          notes: assertion.notes || undefined
        };
        
        rules.push(rule);
      }
    }

    // Create output directory if it doesn't exist
    const outputDir = path.dirname(options.output);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Write rules pack
    const rulesPack = {
      version: '1.0',
      provider: 'aws',
      coverage: coverageTier,
      rule_count: rules.length,
      rules: rules
    };

    fs.writeFileSync(options.output, JSON.stringify(rulesPack, null, 2));
    console.log(`Generated ${rules.length} rules to ${options.output}`);

    // Validate output
    const validatedRulesPack = RulesPackSchema.parse(rulesPack);
    console.log('✅ Output validation passed');

  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
