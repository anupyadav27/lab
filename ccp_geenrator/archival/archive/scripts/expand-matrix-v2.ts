#!/usr/bin/env ts-node

import * as fs from 'fs';

// Load current matrix
const currentMatrix = JSON.parse(fs.readFileSync('matrices/aws_fixed.json', 'utf8'));

// Load missing services
const missingServices = fs.readFileSync('missing_services.txt', 'utf8').trim().split('\n');

// New service mappings for missing services
const newServiceMappings = {
  // Security & Compliance Services
  'accessanalyzer': {
    'identity_access.least_privilege': {
      'core': [
        {
          'service': 'accessanalyzer',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.accessanalyzer.findings',
          'not_applicable_when': 'no_iam_resources'
        }
      ],
      'extended': [
        {
          'service': 'accessanalyzer',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.accessanalyzer.analyzer_configuration',
          'not_applicable_when': 'no_iam_resources'
        }
      ]
    },
    'network_perimeter.firewall_rules': {
      'extended': [
        {
          'service': 'accessanalyzer',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.accessanalyzer.network_findings',
          'not_applicable_when': 'no_public_resources'
        }
      ]
    }
  },

  'detective': {
    'monitoring_security.incident_response': {
      'core': [
        {
          'service': 'detective',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.detective.graph_enabled',
          'not_applicable_when': 'no_cloudtrail_logs'
        }
      ],
      'extended': [
        {
          'service': 'detective',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.detective.findings',
          'not_applicable_when': 'no_cloudtrail_logs'
        }
      ]
    },
    'monitoring_security.threat_detection': {
      'core': [
        {
          'service': 'detective',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.detective.threat_detection',
          'not_applicable_when': 'no_cloudtrail_logs'
        }
      ]
    }
  },

  'inspector2': {
    'host_security.vulnerability_management': {
      'core': [
        {
          'service': 'inspector2',
          'resource_type': 'compute.vm',
          'adapter': 'aws.inspector2.vulnerability_scanning',
          'not_applicable_when': 'no_ec2_instances'
        }
      ],
      'extended': [
        {
          'service': 'inspector2',
          'resource_type': 'compute.vm',
          'adapter': 'aws.inspector2.findings',
          'not_applicable_when': 'no_ec2_instances'
        }
      ]
    },
    'containers_kubernetes.image_security': {
      'core': [
        {
          'service': 'inspector2',
          'resource_type': 'registry.repo',
          'adapter': 'aws.inspector2.container_scanning',
          'not_applicable_when': 'no_container_images'
        }
      ]
    }
  },

  'securityhub': {
    'monitoring_security.incident_response': {
      'core': [
        {
          'service': 'securityhub',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.securityhub.findings',
          'not_applicable_when': 'no_security_services'
        }
      ],
      'extended': [
        {
          'service': 'securityhub',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.securityhub.standards',
          'not_applicable_when': 'no_security_services'
        }
      ]
    },
    'monitoring_security.threat_detection': {
      'core': [
        {
          'service': 'securityhub',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.securityhub.threat_intel',
          'not_applicable_when': 'no_security_services'
        }
      ]
    }
  },

  'shield': {
    'network_perimeter.ddos_protection': {
      'core': [
        {
          'service': 'shield',
          'resource_type': 'edge.waf',
          'adapter': 'aws.shield.protection_enabled',
          'not_applicable_when': 'no_public_resources'
        }
      ],
      'extended': [
        {
          'service': 'shield',
          'resource_type': 'edge.waf',
          'adapter': 'aws.shield.advanced_protection',
          'not_applicable_when': 'no_public_resources'
        }
      ]
    }
  },

  'networkfirewall': {
    'network_perimeter.firewall_rules': {
      'core': [
        {
          'service': 'networkfirewall',
          'resource_type': 'network.firewall',
          'adapter': 'aws.networkfirewall.firewall_policy',
          'not_applicable_when': 'no_vpc_networks'
        }
      ],
      'extended': [
        {
          'service': 'networkfirewall',
          'resource_type': 'network.firewall',
          'adapter': 'aws.networkfirewall.rule_groups',
          'not_applicable_when': 'no_vpc_networks'
        }
      ]
    }
  },

  // Compute & Containers
  'ecs': {
    'containers_kubernetes.workload_security': {
      'core': [
        {
          'service': 'ecs',
          'resource_type': 'k8s.workload',
          'adapter': 'aws.ecs.task_definition',
          'not_applicable_when': 'no_ecs_tasks'
        }
      ],
      'extended': [
        {
          'service': 'ecs',
          'resource_type': 'k8s.workload',
          'adapter': 'aws.ecs.service_configuration',
          'not_applicable_when': 'no_ecs_tasks'
        }
      ]
    },
    'host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'ecs',
          'resource_type': 'k8s.workload',
          'adapter': 'aws.ecs.vulnerability_scanning',
          'not_applicable_when': 'no_ecs_tasks'
        }
      ]
    }
  },

  'elbv2': {
    'network_perimeter.firewall_rules': {
      'core': [
        {
          'service': 'elbv2',
          'resource_type': 'network.load_balancer',
          'adapter': 'aws.elbv2.security_groups',
          'not_applicable_when': 'no_load_balancers'
        }
      ],
      'extended': [
        {
          'service': 'elbv2',
          'resource_type': 'network.load_balancer',
          'adapter': 'aws.elbv2.waf_integration',
          'not_applicable_when': 'no_load_balancers'
        }
      ]
    },
    'crypto_data_protection.encryption_in_transit': {
      'core': [
        {
          'service': 'elbv2',
          'resource_type': 'network.load_balancer',
          'adapter': 'aws.elbv2.ssl_certificates',
          'not_applicable_when': 'no_load_balancers'
        }
      ]
    }
  },

  // Data & Analytics
  'emr': {
    'data_protection.data_classification': {
      'extended': [
        {
          'service': 'emr',
          'resource_type': 'compute.vm',
          'adapter': 'aws.emr.data_encryption',
          'not_applicable_when': 'no_emr_clusters'
        }
      ]
    },
    'host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'emr',
          'resource_type': 'compute.vm',
          'adapter': 'aws.emr.security_configuration',
          'not_applicable_when': 'no_emr_clusters'
        }
      ]
    }
  },

  'glue': {
    'data_protection.data_classification': {
      'extended': [
        {
          'service': 'glue',
          'resource_type': 'paas.app',
          'adapter': 'aws.glue.data_catalog_encryption',
          'not_applicable_when': 'no_glue_jobs'
        }
      ]
    },
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'glue',
          'resource_type': 'paas.app',
          'adapter': 'aws.glue.connection_encryption',
          'not_applicable_when': 'no_glue_jobs'
        }
      ]
    }
  },

  'kinesis': {
    'crypto_data_protection.encryption_at_rest': {
      'core': [
        {
          'service': 'kinesis',
          'resource_type': 'storage.queue',
          'adapter': 'aws.kinesis.stream_encryption',
          'not_applicable_when': 'no_kinesis_streams'
        }
      ]
    },
    'monitoring_security.logging': {
      'core': [
        {
          'service': 'kinesis',
          'resource_type': 'storage.queue',
          'adapter': 'aws.kinesis.stream_monitoring',
          'not_applicable_when': 'no_kinesis_streams'
        }
      ]
    }
  },

  'firehose': {
    'crypto_data_protection.encryption_at_rest': {
      'core': [
        {
          'service': 'firehose',
          'resource_type': 'storage.queue',
          'adapter': 'aws.firehose.delivery_stream_encryption',
          'not_applicable_when': 'no_firehose_streams'
        }
      ]
    }
  },

  'sagemaker': {
    'data_protection.data_classification': {
      'extended': [
        {
          'service': 'sagemaker',
          'resource_type': 'paas.app',
          'adapter': 'aws.sagemaker.data_encryption',
          'not_applicable_when': 'no_sagemaker_endpoints'
        }
      ]
    },
    'host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'sagemaker',
          'resource_type': 'paas.app',
          'adapter': 'aws.sagemaker.model_security',
          'not_applicable_when': 'no_sagemaker_endpoints'
        }
      ]
    }
  },

  'neptune': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'neptune',
          'resource_type': 'db.cluster',
          'adapter': 'aws.neptune.cluster_encryption',
          'not_applicable_when': 'no_neptune_clusters'
        }
      ]
    }
  },

  'timestream': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'timestream',
          'resource_type': 'db.instance',
          'adapter': 'aws.timestream.database_encryption',
          'not_applicable_when': 'no_timestream_databases'
        }
      ]
    }
  },

  // Management & Orchestration
  'cloudformation': {
    'governance_compliance.infrastructure_as_code': {
      'core': [
        {
          'service': 'cloudformation',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.cloudformation.stack_drift',
          'not_applicable_when': 'no_cloudformation_stacks'
        }
      ],
      'extended': [
        {
          'service': 'cloudformation',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.cloudformation.template_validation',
          'not_applicable_when': 'no_cloudformation_stacks'
        }
      ]
    }
  },

  'stepfunctions': {
    'governance_compliance.infrastructure_as_code': {
      'extended': [
        {
          'service': 'stepfunctions',
          'resource_type': 'paas.app',
          'adapter': 'aws.stepfunctions.state_machine_security',
          'not_applicable_when': 'no_step_functions'
        }
      ]
    }
  },

  'directconnect': {
    'network_perimeter.network_segmentation': {
      'extended': [
        {
          'service': 'directconnect',
          'resource_type': 'network.gateway',
          'adapter': 'aws.directconnect.connection_encryption',
          'not_applicable_when': 'no_direct_connect'
        }
      ]
    }
  },

  // Additional services for comprehensive coverage
  'appsync': {
    'crypto_data_protection.encryption_in_transit': {
      'extended': [
        {
          'service': 'appsync',
          'resource_type': 'platform.api_endpoint',
          'adapter': 'aws.appsync.api_encryption',
          'not_applicable_when': 'no_appsync_apis'
        }
      ]
    }
  },

  'batch': {
    'host_security.vulnerability_management': {
      'extended': [
        {
          'service': 'batch',
          'resource_type': 'compute.vm',
          'adapter': 'aws.batch.job_definition_security',
          'not_applicable_when': 'no_batch_jobs'
        }
      ]
    }
  },

  'bedrock': {
    'data_protection.data_classification': {
      'exhaustive': [
        {
          'service': 'bedrock',
          'resource_type': 'paas.app',
          'adapter': 'aws.bedrock.model_access_control',
          'not_applicable_when': 'no_bedrock_usage'
        }
      ]
    }
  },

  'dms': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'dms',
          'resource_type': 'db.instance',
          'adapter': 'aws.dms.replication_encryption',
          'not_applicable_when': 'no_dms_tasks'
        }
      ]
    }
  },

  'memorydb': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'memorydb',
          'resource_type': 'db.cluster',
          'adapter': 'aws.memorydb.cluster_encryption',
          'not_applicable_when': 'no_memorydb_clusters'
        }
      ]
    }
  },

  'mq': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'mq',
          'resource_type': 'storage.queue',
          'adapter': 'aws.mq.broker_encryption',
          'not_applicable_when': 'no_mq_brokers'
        }
      ]
    }
  },

  'qldb': {
    'crypto_data_protection.encryption_at_rest': {
      'extended': [
        {
          'service': 'qldb',
          'resource_type': 'db.instance',
          'adapter': 'aws.qldb.ledger_encryption',
          'not_applicable_when': 'no_qldb_ledgers'
        }
      ]
    }
  },

  'ses': {
    'crypto_data_protection.encryption_in_transit': {
      'extended': [
        {
          'service': 'ses',
          'resource_type': 'platform.api_endpoint',
          'adapter': 'aws.ses.dkim_verification',
          'not_applicable_when': 'no_ses_usage'
        }
      ]
    }
  },

  'transfer': {
    'crypto_data_protection.encryption_in_transit': {
      'extended': [
        {
          'service': 'transfer',
          'resource_type': 'platform.api_endpoint',
          'adapter': 'aws.transfer.server_encryption',
          'not_applicable_when': 'no_transfer_servers'
        }
      ]
    }
  },

  'wellarchitected': {
    'governance_compliance.risk_management': {
      'extended': [
        {
          'service': 'wellarchitected',
          'resource_type': 'platform.control_plane',
          'adapter': 'aws.wellarchitected.workload_review',
          'not_applicable_when': 'no_wellarchitected_workloads'
        }
      ]
    }
  }
};

// Merge new mappings with current matrix
const expandedMatrix: any = { ...currentMatrix };

// Add new service mappings
Object.entries(newServiceMappings).forEach(([service, mappings]) => {
  Object.entries(mappings).forEach(([assertionFamily, tiers]) => {
    if (!expandedMatrix[assertionFamily]) {
      expandedMatrix[assertionFamily] = {};
    }
    
    Object.entries(tiers).forEach(([tier, entries]) => {
      if (!expandedMatrix[assertionFamily][tier]) {
        expandedMatrix[assertionFamily][tier] = [];
      }
      
      // Add new entries
      expandedMatrix[assertionFamily][tier].push(...(entries as any[]));
    });
  });
});

// Save expanded matrix
fs.writeFileSync('matrices/aws_matrix_v2.json', JSON.stringify(expandedMatrix, null, 2));

console.log('✅ Expanded AWS matrix with new services');
console.log(`📊 Added mappings for ${Object.keys(newServiceMappings).length} new services`);
console.log('📁 Saved to matrices/aws_matrix_v2.json');

// Count total assertion families
const totalFamilies = Object.keys(expandedMatrix).length;
console.log(`📈 Total assertion families: ${totalFamilies}`);

// Count services by tier
const coreServices = new Set();
const extendedServices = new Set();
const exhaustiveServices = new Set();

Object.values(expandedMatrix).forEach((family: any) => {
  Object.entries(family).forEach(([tier, entries]) => {
    (entries as any[]).forEach((entry: any) => {
      if (tier === 'core') coreServices.add(entry.service);
      if (tier === 'extended') extendedServices.add(entry.service);
      if (tier === 'exhaustive') exhaustiveServices.add(entry.service);
    });
  });
});

console.log(`📊 Services by tier:`);
console.log(`   Core: ${coreServices.size}`);
console.log(`   Extended: ${extendedServices.size}`);
console.log(`   Exhaustive: ${exhaustiveServices.size}`);
