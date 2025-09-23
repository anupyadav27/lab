# Kubernetes K8S_STORAGE Service Compliance Prompt

## Service Information
- **Service Name**: K8S_STORAGE
- **Total Functions**: 1
- **Service Type**: Kubernetes Component

## Function List
The following 1 functions are available for Kubernetes K8S_STORAGE compliance checks:

1. `k8s_storage_secure_deletion`


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
3. Follow the naming convention: `k8s_storage_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def k8s_storage_example_function_check():
    """
    Example compliance check for Kubernetes K8S_STORAGE service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific k8s_storage configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in k8s_storage check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: K8S_STORAGE
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **K8S_STORAGE**: Kubernetes k8s_storage component
- **Configuration**: k8s_storage specific configurations
- **Security**: k8s_storage security settings
- **Monitoring**: k8s_storage monitoring and logging
- **Compliance**: k8s_storage compliance requirements


## Implementation Guidelines
- All functions are based on Kubernetes K8S_STORAGE API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
