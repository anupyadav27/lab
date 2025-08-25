# Kubernetes Services Summary

This directory contains organized service prompts for Kubernetes compliance checks.

## Available Services

### CORE COMPONENT Services

- **apiserver** (92 functions)
  - Folder: `apiserver/`

- **core** (44 functions)
  - Folder: `core/`

- **controllermanager** (12 functions)
  - Folder: `controllermanager/`

- **scheduler** (8 functions)
  - Folder: `scheduler/`

### DATA STORE Services

- **etcd** (18 functions)
  - Folder: `etcd/`

### NODE COMPONENT Services

- **kubelet** (26 functions)
  - Folder: `kubelet/`

- **kube-proxy** (3 functions)
  - Folder: `kube-proxy/`

### SECURITY Services

- **rbac** (15 functions)
  - Folder: `rbac/`

### NETWORKING Services

- **flanneld** (1 functions)
  - Folder: `flanneld/`

### OTHER Services

- **k8s_rbac** (49 functions)
  - Folder: `k8s_rbac/`

- **k8s_network** (18 functions)
  - Folder: `k8s_network/`

- **k8s_service_name** (258 functions)
  - Folder: `k8s_service_name/`

- **networking** (3 functions)
  - Folder: `networking/`

- **k8s_pod** (38 functions)
  - Folder: `k8s_pod/`

- **k8s_secret** (7 functions)
  - Folder: `k8s_secret/`

- **k8s_service** (19 functions)
  - Folder: `k8s_service/`

- **k8s_batch** (3 functions)
  - Folder: `k8s_batch/`

- **k8s_apps** (1 functions)
  - Folder: `k8s_apps/`

- **k8s_core** (5 functions)
  - Folder: `k8s_core/`

- **k8s_authentication** (1 functions)
  - Folder: `k8s_authentication/`

- **k8s_testing** (1 functions)
  - Folder: `k8s_testing/`

- **k8s_storage** (1 functions)
  - Folder: `k8s_storage/`

## Statistics
- **Total Services**: 22
- **Total Functions**: 623
- **Service Types**: 6

## Directory Structure
```
kubernetes_service_prompts/
├── apiserver/
│   ├── apiserver_service_prompt.md
│   └── apiserver_functions.json
├── controllermanager/
│   ├── controllermanager_service_prompt.md
│   └── controllermanager_functions.json
├── core/
│   ├── core_service_prompt.md
│   └── core_functions.json
├── etcd/
│   ├── etcd_service_prompt.md
│   └── etcd_functions.json
├── flanneld/
│   ├── flanneld_service_prompt.md
│   └── flanneld_functions.json
├── k8s_apps/
│   ├── k8s_apps_service_prompt.md
│   └── k8s_apps_functions.json
├── k8s_authentication/
│   ├── k8s_authentication_service_prompt.md
│   └── k8s_authentication_functions.json
├── k8s_batch/
│   ├── k8s_batch_service_prompt.md
│   └── k8s_batch_functions.json
├── k8s_core/
│   ├── k8s_core_service_prompt.md
│   └── k8s_core_functions.json
├── k8s_network/
│   ├── k8s_network_service_prompt.md
│   └── k8s_network_functions.json
├── k8s_pod/
│   ├── k8s_pod_service_prompt.md
│   └── k8s_pod_functions.json
├── k8s_rbac/
│   ├── k8s_rbac_service_prompt.md
│   └── k8s_rbac_functions.json
├── k8s_secret/
│   ├── k8s_secret_service_prompt.md
│   └── k8s_secret_functions.json
├── k8s_service/
│   ├── k8s_service_service_prompt.md
│   └── k8s_service_functions.json
├── k8s_service_name/
│   ├── k8s_service_name_service_prompt.md
│   └── k8s_service_name_functions.json
├── k8s_storage/
│   ├── k8s_storage_service_prompt.md
│   └── k8s_storage_functions.json
├── k8s_testing/
│   ├── k8s_testing_service_prompt.md
│   └── k8s_testing_functions.json
├── kube-proxy/
│   ├── kube-proxy_service_prompt.md
│   └── kube-proxy_functions.json
├── kubelet/
│   ├── kubelet_service_prompt.md
│   └── kubelet_functions.json
├── networking/
│   ├── networking_service_prompt.md
│   └── networking_functions.json
├── rbac/
│   ├── rbac_service_prompt.md
│   └── rbac_functions.json
├── scheduler/
│   ├── scheduler_service_prompt.md
│   └── scheduler_functions.json
└── README.md (this file)


## Usage
1. Navigate to the specific service folder
2. Read the service prompt for implementation guidance
3. Use the functions JSON file for function lists
4. Implement compliance checks based on the provided templates

## Service Types
- **Core Component**: API Server, Controller Manager, Scheduler, Core
- **Data Store**: etcd
- **Node Component**: Kubelet, Kube-proxy
- **Security**: RBAC
- **Networking**: Flannel, CNI components
- **Other**: Miscellaneous components

## Kubernetes Compliance Standards
- **CIS Kubernetes Benchmark**
- **PCI Secure Software Standard v1.2.1**
- **NIST Cybersecurity Framework**
- **ISO 27001**
- **SOC 2**
- **GDPR**
- **HIPAA** (where applicable)
