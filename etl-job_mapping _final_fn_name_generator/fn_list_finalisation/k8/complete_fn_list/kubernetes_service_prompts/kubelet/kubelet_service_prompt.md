# Kubernetes KUBELET Service Compliance Prompt

## Service Information
- **Service Name**: KUBELET
- **Total Functions**: 26
- **Service Type**: Kubernetes Component

## Function List
The following 26 functions are available for Kubernetes KUBELET compliance checks:

1. `kubelet_authorization_mode`
2. `kubelet_client_ca_file_set`
3. `kubelet_conf_file_ownership`
4. `kubelet_conf_file_permissions`
5. `kubelet_config_yaml_ownership`
6. `kubelet_config_yaml_permissions`
7. `kubelet_disable_anonymous_auth`
8. `kubelet_disable_read_only_port`
9. `kubelet_event_record_qps`
10. `kubelet_manage_iptables`
11. `kubelet_rotate_certificates`
12. `kubelet_service_file_ownership_root`
13. `kubelet_service_file_permissions`
14. `kubelet_streaming_connection_timeout`
15. `kubelet_tls_cert_and_key`
16. `kubelet_strong_ciphers_only`
17. `kubelet_ca_file_permissions_check`
18. `kubelet_no_hostname_override`
19. `kubelet_set_pod_pid_limit`
20. `kubelet_client_certificate_and_key_check`
21. `kubelet_certificate_authority_check`
22. `kubelet_seccomp_default_check`
23. `kubelet_ip_address_deny_check`
24. `kubelet_https_argument_check`
25. `kubelet_insecure_experimental_approve_all_csrs_check`
26. `kubelet_protect_kernel_defaults_check`


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
3. Follow the naming convention: `kubelet_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def kubelet_example_function_check():
    """
    Example compliance check for Kubernetes KUBELET service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific kubelet configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in kubelet check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: KUBELET
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **Kubelet**: Node agent component
- **Authentication**: Kubelet authentication configuration
- **Authorization**: Kubelet authorization settings
- **TLS**: Kubelet TLS configuration
- **Pod Security**: Pod security context enforcement


## Implementation Guidelines
- All functions are based on Kubernetes KUBELET API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
