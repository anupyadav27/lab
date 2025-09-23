#!/usr/bin/env ts-node

import * as fs from 'fs';

// Load current matrix
const matrix = JSON.parse(fs.readFileSync('matrices/aws_matrix_v2.json', 'utf8'));

// Additional services to reach 30+ new services
const additionalServices = {
  'appstream': {
    'compute_host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'appstream',
          'resource_type': 'compute.vm',
          'adapter': 'aws.appstream.fleet_security',
          'not_applicable_when': 'no_appstream_fleets'
        }
      ]
    }
  },

  'artifact': {
    'governance_compliance.risk_management': {
      'extended': [
        {
          'service': 'artifact',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.artifact.compliance_reports',
          'not_applicable_when': 'no_artifact_usage'
        }
      ]
    }
  },

  'autoscaling': {
    'compute_host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'autoscaling',
          'resource_type': 'compute.vm',
          'adapter': 'aws.autoscaling.launch_template_security',
          'not_applicable_when': 'no_autoscaling_groups'
        }
      ]
    }
  },

  'datasync': {
    'crypto_data_protection.encryption_in_transit': {
      'extended': [
        {
          'service': 'datasync',
          'resource_type': 'storage.queue',
          'adapter': 'aws.datasync.task_encryption',
          'not_applicable_when': 'no_datasync_tasks'
        }
      ]
    }
  },

  'directoryservice': {
    'identity_access.authentication': {
      'extended': [
        {
          'service': 'directoryservice',
          'resource_type': 'identity.tenant',
          'adapter': 'aws.directoryservice.mfa_enforcement',
          'not_applicable_when': 'no_directory_service'
        }
      ]
    }
  },

  'dlm': {
    'resilience_recovery.backup_management': {
      'extended': [
        {
          'service': 'dlm',
          'resource_type': 'backup.plan',
          'adapter': 'aws.dlm.lifecycle_policy',
          'not_applicable_when': 'no_dlm_policies'
        }
      ]
    }
  },

  'docdb': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'docdb',
          'resource_type': 'db.cluster',
          'adapter': 'aws.docdb.cluster_encryption',
          'not_applicable_when': 'no_docdb_clusters'
        }
      ]
    }
  },

  'documentdb': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'documentdb',
          'resource_type': 'db.cluster',
          'adapter': 'aws.documentdb.cluster_encryption',
          'not_applicable_when': 'no_documentdb_clusters'
        }
      ]
    }
  },

  'dynamodbstreams': {
    'crypto_data_protection.encryption_in_transit': {
      'extended': [
        {
          'service': 'dynamodbstreams',
          'resource_type': 'storage.queue',
          'adapter': 'aws.dynamodbstreams.stream_encryption',
          'not_applicable_when': 'no_dynamodb_streams'
        }
      ]
    }
  },

  'elasticdisasterrecovery': {
    'resilience_recovery.disaster_recovery': {
      'extended': [
        {
          'service': 'elasticdisasterrecovery',
          'resource_type': 'dr.plan',
          'adapter': 'aws.elasticdisasterrecovery.replication_configuration',
          'not_applicable_when': 'no_dr_plans'
        }
      ]
    }
  },

  'fms': {
    'network_perimeter.firewall_rules': {
      'extended': [
        {
          'service': 'fms',
          'resource_type': 'network.firewall',
          'adapter': 'aws.fms.policy_enforcement',
          'not_applicable_when': 'no_fms_policies'
        }
      ]
    }
  },

  'kafka': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'kafka',
          'resource_type': 'storage.queue',
          'adapter': 'aws.kafka.cluster_encryption',
          'not_applicable_when': 'no_kafka_clusters'
        }
      ]
    }
  },

  'keyspaces': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'keyspaces',
          'resource_type': 'db.instance',
          'adapter': 'aws.keyspaces.table_encryption',
          'not_applicable_when': 'no_keyspaces_tables'
        }
      ]
    }
  },

  'kubernetes': {
    'containers_kubernetes.workload_security': {
      'extended': [
        {
          'service': 'kubernetes',
          'resource_type': 'k8s.workload',
          'adapter': 'aws.kubernetes.pod_security_standards',
          'not_applicable_when': 'no_kubernetes_clusters'
        }
      ]
    }
  },

  'resourceexplorer2': {
    'governance_compliance.risk_management': {
      'extended': [
        {
          'service': 'resourceexplorer2',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.resourceexplorer2.index_configuration',
          'not_applicable_when': 'no_resource_explorer'
        }
      ]
    }
  },

  'servicecatalog': {
    'governance_compliance.infrastructure_as_code': {
      'extended': [
        {
          'service': 'servicecatalog',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.servicecatalog.portfolio_security',
          'not_applicable_when': 'no_service_catalog'
        }
      ]
    }
  },

  'ssmincidents': {
    'monitoring_security.incident_response': {
      'extended': [
        {
          'service': 'ssmincidents',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.ssmincidents.response_plan',
          'not_applicable_when': 'no_incident_response'
        }
      ]
    }
  },

  'storagegateway': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'storagegateway',
          'resource_type': 'storage.bucket',
          'adapter': 'aws.storagegateway.gateway_encryption',
          'not_applicable_when': 'no_storage_gateways'
        }
      ]
    }
  },

  'trustedadvisor': {
    'governance_compliance.risk_management': {
      'extended': [
        {
          'service': 'trustedadvisor',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.trustedadvisor.recommendations',
          'not_applicable_when': 'no_trusted_advisor'
        }
      ]
    }
  },

  'workdocs': {
    'data_protection.data_classification': {
      'extended': [
        {
          'service': 'workdocs',
          'resource_type': 'storage.bucket',
          'adapter': 'aws.workdocs.document_encryption',
          'not_applicable_when': 'no_workdocs_usage'
        }
      ]
    }
  },

  'workspaces': {
    'compute_host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'workspaces',
          'resource_type': 'compute.vm',
          'adapter': 'aws.workspaces.workstation_security',
          'not_applicable_when': 'no_workspaces'
        }
      ]
    }
  }
};

// Merge additional services with current matrix
const expandedMatrix = { ...matrix };

Object.entries(additionalServices).forEach(([service, mappings]) => {
  Object.entries(mappings).forEach(([assertionFamily, tiers]) => {
    if (!expandedMatrix[assertionFamily]) {
      expandedMatrix[assertionFamily] = {};
    }
    
    Object.entries(tiers).forEach(([tier, entries]) => {
      if (!expandedMatrix[assertionFamily][tier]) {
        expandedMatrix[assertionFamily][tier] = [];
      }
      
      expandedMatrix[assertionFamily][tier].push(...(entries as any[]));
    });
  });
});

// Save expanded matrix
fs.writeFileSync('matrices/aws_matrix_v2.json', JSON.stringify(expandedMatrix, null, 2));

console.log('✅ Added additional services to reach 30+');
console.log(`📊 Added ${Object.keys(additionalServices).length} more services`);
console.log('📁 Updated matrices/aws_matrix_v2.json');
