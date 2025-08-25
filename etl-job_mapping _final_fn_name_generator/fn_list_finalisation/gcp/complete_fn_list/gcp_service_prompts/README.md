# GCP Services Summary

This directory contains organized service prompts for GCP compliance checks.

## Available Services

### COMPUTE Services

- **compute** (422 functions)
  - Description: GCP COMPUTE Service
  - SDK Client: compute_client
  - Folder: `compute/`

- **functions** (12 functions)
  - Description: GCP FUNCTIONS Service
  - SDK Client: cloudfunctions_client
  - Folder: `functions/`

- **gke** (111 functions)
  - Description: GCP GKE Service
  - SDK Client: container_client
  - Folder: `gke/`

- **appengine** (8 functions)
  - Description: GCP APPENGINE Service
  - SDK Client: appengine_client
  - Folder: `appengine/`

- **run** (8 functions)
  - Description: GCP RUN Service
  - SDK Client: run_client
  - Folder: `run/`

### NETWORKING Services

- **vpc** (324 functions)
  - Description: GCP VPC Service
  - SDK Client: compute_client
  - Folder: `vpc/`

- **dns** (30 functions)
  - Description: GCP DNS Service
  - SDK Client: dns_client
  - Folder: `dns/`

- **loadbalancer** (1 functions)
  - Description: GCP LOADBALANCER Service
  - SDK Client: compute_client
  - Folder: `loadbalancer/`

### SECURITY Services

- **iam** (513 functions)
  - Description: GCP IAM Service
  - SDK Client: iam_client
  - Folder: `iam/`

- **kms** (38 functions)
  - Description: GCP KMS Service
  - SDK Client: kms_client
  - Folder: `kms/`

- **securitycenter** (76 functions)
  - Description: GCP SECURITYCENTER Service
  - SDK Client: securitycenter_client
  - Folder: `securitycenter/`

- **apikey** (38 functions)
  - Description: GCP APIKEY Service
  - SDK Client: apikeys_client
  - Folder: `apikey/`

- **certificatemanager** (2 functions)
  - Description: GCP CERTIFICATEMANAGER Service
  - SDK Client: certificatemanager_client
  - Folder: `certificatemanager/`

- **secretmanager** (11 functions)
  - Description: GCP SECRETMANAGER Service
  - SDK Client: secretmanager_client
  - Folder: `secretmanager/`

### STORAGE Services

- **storage** (152 functions)
  - Description: GCP STORAGE Service
  - SDK Client: storage_client
  - Folder: `storage/`

- **filestore** (7 functions)
  - Description: GCP FILESTORE Service
  - SDK Client: filestore_client
  - Folder: `filestore/`

### DATA Services

- **sql** (63 functions)
  - Description: GCP SQL Service
  - SDK Client: sqladmin_client
  - Folder: `sql/`

- **firestore** (16 functions)
  - Description: GCP FIRESTORE Service
  - SDK Client: firestore_client
  - Folder: `firestore/`

- **spanner** (1 functions)
  - Description: GCP SPANNER Service
  - SDK Client: spanner_client
  - Folder: `spanner/`

- **bigquery** (72 functions)
  - Description: GCP BIGQUERY Service
  - SDK Client: bigquery_client
  - Folder: `bigquery/`

- **datatransfer** (7 functions)
  - Description: GCP DATATRANSFER Service
  - SDK Client: datatransfer_client
  - Folder: `datatransfer/`

- **datastream** (4 functions)
  - Description: GCP DATASTREAM Service
  - SDK Client: datastream_client
  - Folder: `datastream/`

- **datastore** (6 functions)
  - Description: GCP DATASTORE Service
  - SDK Client: datastore_client
  - Folder: `datastore/`

- **dataproc** (4 functions)
  - Description: GCP DATAPROC Service
  - SDK Client: dataproc_client
  - Folder: `dataproc/`

- **datamigration** (2 functions)
  - Description: GCP DATAMIGRATION Service
  - SDK Client: datamigration_client
  - Folder: `datamigration/`

### OTHER Services

- **redis** (3 functions)
  - Description: GCP REDIS Service
  - SDK Client: redis_client
  - Folder: `redis/`

- **identitytoolkit** (10 functions)
  - Description: GCP IDENTITYTOOLKIT Service
  - SDK Client: identitytoolkit_client
  - Folder: `identitytoolkit/`

- **cloudbuild** (1 functions)
  - Description: GCP CLOUDBUILD Service
  - SDK Client: cloudbuild_client
  - Folder: `cloudbuild/`

- **pubsub** (13 functions)
  - Description: GCP PUBSUB Service
  - SDK Client: pubsub_client
  - Folder: `pubsub/`

- **sourcerepo** (2 functions)
  - Description: GCP SOURCEREPO Service
  - SDK Client: sourcerepo_client
  - Folder: `sourcerepo/`

- **apigateway** (28 functions)
  - Description: GCP APIGATEWAY Service
  - SDK Client: apigateway_client
  - Folder: `apigateway/`

- **final_misc** (23 functions)
  - Description: GCP FINAL_MISC - Truly Uncategorized Functions
  - SDK Client: unknown
  - Folder: `final_misc/`

### MANAGEMENT Services

- **resourcemanager** (7 functions)
  - Description: GCP RESOURCEMANAGER Service
  - SDK Client: resourcemanager_client
  - Folder: `resourcemanager/`

- **serviceusage** (1 functions)
  - Description: GCP SERVICEUSAGE Service
  - SDK Client: serviceusage_client
  - Folder: `serviceusage/`

### MONITORING Services

- **monitoring** (35 functions)
  - Description: GCP MONITORING Service
  - SDK Client: monitoring_client
  - Folder: `monitoring/`

- **logging** (127 functions)
  - Description: GCP LOGGING Service
  - SDK Client: logging_client
  - Folder: `logging/`

### WORKSPACE Services

- **workspace** (16 functions)
  - Description: GCP WORKSPACE Service
  - SDK Client: admin_client
  - Folder: `workspace/`

## Statistics
- **Total Services**: 37
- **Total Functions**: 2194
- **Service Types**: 9

## Directory Structure
```
gcp_service_prompts/
├── apigateway/
│   ├── apigateway_service_prompt.md
│   └── apigateway_functions.json
├── apikey/
│   ├── apikey_service_prompt.md
│   └── apikey_functions.json
├── appengine/
│   ├── appengine_service_prompt.md
│   └── appengine_functions.json
├── bigquery/
│   ├── bigquery_service_prompt.md
│   └── bigquery_functions.json
├── certificatemanager/
│   ├── certificatemanager_service_prompt.md
│   └── certificatemanager_functions.json
├── cloudbuild/
│   ├── cloudbuild_service_prompt.md
│   └── cloudbuild_functions.json
├── compute/
│   ├── compute_service_prompt.md
│   └── compute_functions.json
├── datamigration/
│   ├── datamigration_service_prompt.md
│   └── datamigration_functions.json
├── dataproc/
│   ├── dataproc_service_prompt.md
│   └── dataproc_functions.json
├── datastore/
│   ├── datastore_service_prompt.md
│   └── datastore_functions.json
├── datastream/
│   ├── datastream_service_prompt.md
│   └── datastream_functions.json
├── datatransfer/
│   ├── datatransfer_service_prompt.md
│   └── datatransfer_functions.json
├── dns/
│   ├── dns_service_prompt.md
│   └── dns_functions.json
├── filestore/
│   ├── filestore_service_prompt.md
│   └── filestore_functions.json
├── final_misc/
│   ├── final_misc_service_prompt.md
│   └── final_misc_functions.json
├── firestore/
│   ├── firestore_service_prompt.md
│   └── firestore_functions.json
├── functions/
│   ├── functions_service_prompt.md
│   └── functions_functions.json
├── gke/
│   ├── gke_service_prompt.md
│   └── gke_functions.json
├── iam/
│   ├── iam_service_prompt.md
│   └── iam_functions.json
├── identitytoolkit/
│   ├── identitytoolkit_service_prompt.md
│   └── identitytoolkit_functions.json
├── kms/
│   ├── kms_service_prompt.md
│   └── kms_functions.json
├── loadbalancer/
│   ├── loadbalancer_service_prompt.md
│   └── loadbalancer_functions.json
├── logging/
│   ├── logging_service_prompt.md
│   └── logging_functions.json
├── monitoring/
│   ├── monitoring_service_prompt.md
│   └── monitoring_functions.json
├── pubsub/
│   ├── pubsub_service_prompt.md
│   └── pubsub_functions.json
├── redis/
│   ├── redis_service_prompt.md
│   └── redis_functions.json
├── resourcemanager/
│   ├── resourcemanager_service_prompt.md
│   └── resourcemanager_functions.json
├── run/
│   ├── run_service_prompt.md
│   └── run_functions.json
├── secretmanager/
│   ├── secretmanager_service_prompt.md
│   └── secretmanager_functions.json
├── securitycenter/
│   ├── securitycenter_service_prompt.md
│   └── securitycenter_functions.json
├── serviceusage/
│   ├── serviceusage_service_prompt.md
│   └── serviceusage_functions.json
├── sourcerepo/
│   ├── sourcerepo_service_prompt.md
│   └── sourcerepo_functions.json
├── spanner/
│   ├── spanner_service_prompt.md
│   └── spanner_functions.json
├── sql/
│   ├── sql_service_prompt.md
│   └── sql_functions.json
├── storage/
│   ├── storage_service_prompt.md
│   └── storage_functions.json
├── vpc/
│   ├── vpc_service_prompt.md
│   └── vpc_functions.json
├── workspace/
│   ├── workspace_service_prompt.md
│   └── workspace_functions.json
└── README.md (this file)


## Usage
1. Navigate to the specific service folder
2. Read the service prompt for implementation guidance
3. Use the functions JSON file for function lists
4. Implement compliance checks based on the provided templates

## Service Types
- **Compute**: Virtual machines, containers, serverless
- **Data**: Databases, analytics, data processing
- **Storage**: Object storage, file systems
- **Networking**: VPC, DNS, load balancing
- **Security**: IAM, encryption, security monitoring
- **Monitoring**: Logging, metrics, alerts
- **Management**: Resource management, billing
- **AI/ML**: Machine learning, AI services
- **Workspace**: Google Workspace services
- **Other**: Miscellaneous services
