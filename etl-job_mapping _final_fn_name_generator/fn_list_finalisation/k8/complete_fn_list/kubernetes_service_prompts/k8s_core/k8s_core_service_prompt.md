# Kubernetes K8S_CORE Service Compliance Prompt

## Service Information
- **Service Name**: K8S_CORE
- **Total Functions**: 5
- **Service Type**: Kubernetes Component

## Function List
The following 5 functions are available for Kubernetes K8S_CORE compliance checks:

1. `k8s_pod_removable_media_scan`
2. `k8s_data_inventory_tracking`
3. `k8s_storage_location_tracking`
4. `k8s_sensitive_data_protection_controls`
5. `k8s_transaction_type_identification`


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
3. Follow the naming convention: `k8s_core_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def k8s_core_example_function_check():
    """
    Example compliance check for Kubernetes K8S_CORE service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific k8s_core configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in k8s_core check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: K8S_CORE
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **K8S_CORE**: Kubernetes k8s_core component
- **Configuration**: k8s_core specific configurations
- **Security**: k8s_core security settings
- **Monitoring**: k8s_core monitoring and logging
- **Compliance**: k8s_core compliance requirements


## Implementation Guidelines
- All functions are based on Kubernetes K8S_CORE API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
