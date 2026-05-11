# CIS Unmapped Controls — CSPM Rule-Writing Backlog

**Total unmapped CIS controls**: 351

These controls are already in the CSV and tagged as automatable, but have no rule mapped in any of your CSPM providers (aws/azure/gcp/oracle/ibm/alicloud/k8s).

**Action**: write CSPM rules for these. Each row in `cis_unmapped_controls.csv` contains the control ID, title, description, and source benchmark file.

## Breakdown by cloud/platform

| Framework | Count | Versions |
|---|---|---|
| CIS_ALICLOUD | 98 | (unknown), 2.0.0 |
| CIS_AWS | 28 | (unknown), 4.0.1 |
| CIS_AZURE | 29 | 1.0.0, 1.7.0, 2.0.0, 5.0.0 |
| CIS_GCP | 24 | (unknown), 1.8.0, 4.0.0 |
| CIS_IBM | 55 | (unknown), 1.3.0 |
| CIS_K8S | 78 | (unknown) |
| CIS_OCI | 39 | 1.2.0, 1.5.0, 3.0.0 |

## Sample entries per cloud (first 5 each)

### CIS_ALICLOUD

| control_id | version | title |
|---|---|---|
| 1.1.10 | — | Ensure that the Container Network Interface file ownership is set to root:root |
| 1.1.11 | — | Ensure that the etcd data directory permissions are set to 700 or more restricti |
| 1.1.12 | — | Ensure that the etcd data directory ownership is set to etcd:etcd |
| 1.1.13 | — | Ensure that the admin.conf file permissions are set to 644 or more restrictive |
| 1.1.14 | — | Ensure that the admin.conf file ownership is set to root:root |

### CIS_AWS

| control_id | version | title |
|---|---|---|
| 1.1 | — | Maintain current contact details |
| 1.3 | 4.0.1 | Ensure security questions are registered in the AWS account |
| 10.3 | — | Ensure Encryption in Transit is Configured |
| 10.7 | — | Ensure Regular Updates and Patches are Installed |
| 11.4 | — | Ensure Data in Transit is Encrypted |

### CIS_AZURE

| control_id | version | title |
|---|---|---|
| 11.2 | 1.0.0 | Ensure that shared access signature (SAS) tokens expire  within an hour |
| 11.4 | 1.0.0 | Ensure stored access policies (SAP) are used when  generating shared access sign |
| 12.1 | 1.0.0 | Ensure double encryption is used for Azure Data Box in  high-security environmen |
| 17.1.4 | 1.0.0 | Ensure that shared access signature (SAS) tokens expire  within an hour |
| 18.2 | 1.0.0 | Ensure stored access policies (SAP) are used when  generating shared access sign |

### CIS_GCP

| control_id | version | title |
|---|---|---|
| 1.3 | 4.0.0 | Ensure that Security Key Enforcement is Enabled for All  Admin Accounts |
| 2.14 | 4.0.0 | Ensure 'Access Transparency' is 'Enabled' |
| 3.1.1 | 1.8.0 | Ensure that the kubeconfig file permissions are set to 644 or  more restrictive |
| 3.1.2 | 1.8.0 | Ensure that the kubelet kubeconfig file ownership is set to  root:root |
| 3.1.3 | 1.8.0 | Ensure that the kubelet configuration file has permissions  set to 644 |

### CIS_IBM

| control_id | version | title |
|---|---|---|
| 1.1 | — | Restrict GPU and USB pass through to approved devices |
| 1.1.1 | — | Ensure that the API server pod specification file permissions are set to 600 or  |
| 1.1.12 | — | Ensure that the etcd data directory ownership is set to etcd:etcd |
| 1.1.13 | — | Ensure that the kubeconfig file permissions are set to 600 or more restrictive |
| 1.1.14 | — | Ensure that the kubeconfig file ownership is set to root:root |

### CIS_K8S

| control_id | version | title |
|---|---|---|
| 1.1.1 | — | Ensure that the API server pod specification file permissions are set to 600 or  |
| 1.1.10 | — | Ensure that the Container Network Interface file ownership is set to root:root |
| 1.1.11 | — | Ensure that the etcd data directory permissions are set to 700 or more restricti |
| 1.1.12 | — | Ensure that the etcd data directory ownership is set to etcd:etcd |
| 1.1.13 | — | Ensure that the admin.conf file permissions are set to 600 |

### CIS_OCI

| control_id | version | title |
|---|---|---|
| 1.10 | 3.0.0 | Ensure user auth tokens rotate within 90 days or less |
| 1.11 | 3.0.0 | Ensure user IAM Database Passwords rotate within 90 days |
| 1.12 | 3.0.0 | Ensure API keys are not created for tenancy administrator  users |
| 1.13 | 3.0.0 | Ensure all OCI IAM user accounts have a valid and current  email address |
| 1.14 | 3.0.0 | Ensure Instance Principal authentication is used for OCI  instances, OCI Cloud D |
