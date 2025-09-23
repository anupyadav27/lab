# Kubernetes SCHEDULER Service Compliance Prompt

## Service Information
- **Service Name**: SCHEDULER
- **Total Functions**: 8
- **Service Type**: Kubernetes Component

## Function List
The following 8 functions are available for Kubernetes SCHEDULER compliance checks:

1. `scheduler_bind_address`
2. `scheduler_profiling`
3. `scheduler_pod_spec_file_permissions`
4. `scheduler_pod_spec_file_ownership`
5. `scheduler_conf_file_permissions`
6. `scheduler_conf_file_ownership`
7. `scheduler_bind_address_check`
8. `scheduler_bind_address_localhost_check`


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
3. Follow the naming convention: `scheduler_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def scheduler_example_function_check():
    """
    Example compliance check for Kubernetes SCHEDULER service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific scheduler configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in scheduler check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: SCHEDULER
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **Scheduler**: Kubernetes scheduler component
- **Scheduling Policies**: Pod scheduling policies
- **Resource Management**: Resource allocation and limits
- **Node Affinity**: Node affinity and anti-affinity rules
- **Pod Priority**: Pod priority and preemption


## Implementation Guidelines
- All functions are based on Kubernetes SCHEDULER API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
