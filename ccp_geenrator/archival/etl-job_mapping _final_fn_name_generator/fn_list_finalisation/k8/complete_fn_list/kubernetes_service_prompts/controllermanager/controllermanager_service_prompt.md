# Kubernetes CONTROLLERMANAGER Service Compliance Prompt

## Service Information
- **Service Name**: CONTROLLERMANAGER
- **Total Functions**: 12
- **Service Type**: Kubernetes Component

## Function List
The following 12 functions are available for Kubernetes CONTROLLERMANAGER compliance checks:

1. `controllermanager_bind_address`
2. `controllermanager_disable_profiling`
3. `controllermanager_garbage_collection`
4. `controllermanager_root_ca_file_set`
5. `controllermanager_rotate_kubelet_server_cert`
6. `controllermanager_service_account_credentials`
7. `controllermanager_service_account_private_key_file`
8. `controllermanager_pod_spec_file_permissions`
9. `controllermanager_pod_spec_file_ownership`
10. `controllermanager_conf_file_permissions`
11. `controllermanager_conf_file_ownership`
12. `controllermanager_terminated_pod_gc_threshold_set`


## Compliance Framework Coverage
This service supports compliance checks for:
- **NIST Cybersecurity Framework**
- **PCI DSS v4.0**
- **ISO 27001**
- **SOC 2**
- **GDPR**
- **HIPAA** (where applicable)
- **CIS Kubernetes Benchmark**
- **PCI Secure Software Standard v1.2.1**

## Usage Instructions
1. Use the function names above to create compliance checks
2. Each function should be implemented as a separate compliance rule
3. Follow the naming convention: `controllermanager_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def controllermanager_example_function_check():
    """
    Example compliance check for Kubernetes CONTROLLERMANAGER service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific controllermanager configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in controllermanager check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: CONTROLLERMANAGER
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **Controller Manager**: Kubernetes controller components
- **Controllers**: Various controller configurations
- **Leader Election**: High availability configuration
- **Service Accounts**: Service account management
- **Node Management**: Node lifecycle management


## Implementation Guidelines
- All functions are based on Kubernetes CONTROLLERMANAGER API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
