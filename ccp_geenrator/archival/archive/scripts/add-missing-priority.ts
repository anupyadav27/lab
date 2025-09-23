#!/usr/bin/env ts-node

import * as fs from 'fs';

// Load the current matrix
const matrix = JSON.parse(fs.readFileSync('matrices/aws_matrix_v2_complete.json', 'utf8'));

// Add missing priority services with correct assertion families
const missingPriorityServices = {
  'detective': {
    'compute_host_security.compliance_monitoring': {
      'extended': [
        {
          'service': 'detective',
          'resource': 'platform.control_plane',
          'adapter': 'aws.detective.graph_enabled',
          'not_applicable_when': 'no_cloudtrail_logs'
        }
      ]
    },
    'compute_host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'detective',
          'resource': 'platform.control_plane',
          'adapter': 'aws.detective.findings',
          'not_applicable_when': 'no_cloudtrail_logs'
        }
      ]
    }
  },

  'securityhub': {
    'compute_host_security.compliance_monitoring': {
      'core': [
        {
          'service': 'securityhub',
          'resource': 'platform.control_plane',
          'adapter': 'aws.securityhub.findings',
          'not_applicable_when': 'no_security_services'
        }
      ],
      'extended': [
        {
          'service': 'securityhub',
          'resource': 'platform.control_plane',
          'adapter': 'aws.securityhub.standards',
          'not_applicable_when': 'no_security_services'
        }
      ]
    },
    'compute_host_security.vulnerability_management': {
      'core': [
        {
          'service': 'securityhub',
          'resource': 'platform.control_plane',
          'adapter': 'aws.securityhub.threat_intel',
          'not_applicable_when': 'no_security_services'
        }
      ]
    }
  },

  'shield': {
    'network_perimeter.firewall_rules': {
      'core': [
        {
          'service': 'shield',
          'resource': 'edge.waf',
          'adapter': 'aws.shield.protection_enabled',
          'not_applicable_when': 'no_public_resources'
        }
      ],
      'extended': [
        {
          'service': 'shield',
          'resource': 'edge.waf',
          'adapter': 'aws.shield.advanced_protection',
          'not_applicable_when': 'no_public_resources'
        }
      ]
    }
  },

  'cloudformation': {
    'governance_compliance.policy_management': {
      'core': [
        {
          'service': 'cloudformation',
          'resource': 'platform.control_plane',
          'adapter': 'aws.cloudformation.stack_drift',
          'not_applicable_when': 'no_cloudformation_stacks'
        }
      ],
      'extended': [
        {
          'service': 'cloudformation',
          'resource': 'platform.control_plane',
          'adapter': 'aws.cloudformation.template_validation',
          'not_applicable_when': 'no_cloudformation_stacks'
        }
      ]
    }
  },

  'stepfunctions': {
    'governance_compliance.policy_management': {
      'extended': [
        {
          'service': 'stepfunctions',
          'resource': 'paas.app',
          'adapter': 'aws.stepfunctions.state_machine_security',
          'not_applicable_when': 'no_step_functions'
        }
      ]
    }
  },

  'ecs': {
    'containers_kubernetes.runtime_security': {
      'core': [
        {
          'service': 'ecs',
          'resource': 'k8s.workload',
          'adapter': 'aws.ecs.task_definition',
          'not_applicable_when': 'no_ecs_tasks'
        }
      ],
      'extended': [
        {
          'service': 'ecs',
          'resource': 'k8s.workload',
          'adapter': 'aws.ecs.service_configuration',
          'not_applicable_when': 'no_ecs_tasks'
        }
      ]
    },
    'compute_host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'ecs',
          'resource': 'k8s.workload',
          'adapter': 'aws.ecs.vulnerability_scanning',
          'not_applicable_when': 'no_ecs_tasks'
        }
      ]
    }
  },

  'emr': {
    'data_protection_storage.data_classification': {
      'extended': [
        {
          'service': 'emr',
          'resource': 'compute.vm',
          'adapter': 'aws.emr.data_encryption',
          'not_applicable_when': 'no_emr_clusters'
        }
      ]
    },
    'compute_host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'emr',
          'resource': 'compute.vm',
          'adapter': 'aws.emr.security_configuration',
          'not_applicable_when': 'no_emr_clusters'
        }
      ]
    }
  },

  'sagemaker': {
    'data_protection_storage.data_classification': {
      'extended': [
        {
          'service': 'sagemaker',
          'resource': 'paas.app',
          'adapter': 'aws.sagemaker.data_encryption',
          'not_applicable_when': 'no_sagemaker_endpoints'
        }
      ]
    },
    'compute_host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'sagemaker',
          'resource': 'paas.app',
          'adapter': 'aws.sagemaker.model_security',
          'not_applicable_when': 'no_sagemaker_endpoints'
        }
      ]
    }
  }
};

// Add missing services to matrix
Object.entries(missingPriorityServices).forEach(([service, mappings]) => {
  Object.entries(mappings).forEach(([assertionFamily, tiers]) => {
    if (!matrix[assertionFamily]) {
      matrix[assertionFamily] = {};
    }
    
    Object.entries(tiers).forEach(([tier, entries]) => {
      if (!matrix[assertionFamily][tier]) {
        matrix[assertionFamily][tier] = [];
      }
      
      // Add entries if they don't already exist
      (entries as any[]).forEach((newEntry: any) => {
        const exists = matrix[assertionFamily][tier].some((existingEntry: any) => 
          existingEntry.service === newEntry.service && 
          existingEntry.adapter === newEntry.adapter
        );
        
        if (!exists) {
          matrix[assertionFamily][tier].push(newEntry);
        }
      });
    });
  });
});

// Save updated matrix
fs.writeFileSync('matrices/aws_matrix_v2_complete.json', JSON.stringify(matrix, null, 2));

console.log('✅ Added missing priority services');
console.log(`📊 Added mappings for: ${Object.keys(missingPriorityServices).join(', ')}`);
console.log('📁 Updated matrices/aws_matrix_v2_complete.json');
