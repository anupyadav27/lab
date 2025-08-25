# Kubernetes FLANNELD Service Compliance Prompt

## Service Information
- **Service Name**: FLANNELD
- **Total Functions**: 1
- **Service Type**: Kubernetes Component

## Function List
The following 1 functions are available for Kubernetes FLANNELD compliance checks:

1. `flanneld_file_ownership_check`


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
3. Follow the naming convention: `flanneld_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def flanneld_example_function_check():
    """
    Example compliance check for Kubernetes FLANNELD service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific flanneld configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in flanneld check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: FLANNELD
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **Flannel**: Container networking interface
- **Network Configuration**: CNI configuration
- **Security**: Network security policies
- **Performance**: Network performance optimization
- **Monitoring**: Network monitoring and logging


## Implementation Guidelines
- All functions are based on Kubernetes FLANNELD API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
