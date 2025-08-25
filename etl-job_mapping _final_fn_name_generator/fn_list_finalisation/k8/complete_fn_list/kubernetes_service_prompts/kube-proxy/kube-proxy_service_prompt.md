# Kubernetes KUBE-PROXY Service Compliance Prompt

## Service Information
- **Service Name**: KUBE-PROXY
- **Total Functions**: 3
- **Service Type**: Kubernetes Component

## Function List
The following 3 functions are available for Kubernetes KUBE-PROXY compliance checks:

1. `proxy_kubeconfig_file_permissions`
2. `kube_proxy_kubeconfig_file_ownership`
3. `kube_proxy_metrics_bind_to_localhost`


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
3. Follow the naming convention: `kube-proxy_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def kube-proxy_example_function_check():
    """
    Example compliance check for Kubernetes KUBE-PROXY service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific kube-proxy configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in kube-proxy check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: KUBE-PROXY
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **Kube-proxy**: Network proxy component
- **Network Policies**: Network policy enforcement
- **Service Networking**: Service networking configuration
- **Load Balancing**: Load balancer configuration
- **Security**: Network security settings


## Implementation Guidelines
- All functions are based on Kubernetes KUBE-PROXY API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
