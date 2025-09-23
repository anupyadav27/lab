# Kubernetes CORE Service Compliance Prompt

## Service Information
- **Service Name**: CORE
- **Total Functions**: 44
- **Service Type**: Kubernetes Component

## Function List
The following 44 functions are available for Kubernetes CORE compliance checks:

1. `core_minimize_admission_hostport_containers`
2. `core_minimize_admission_windows_hostprocess_containers`
3. `core_minimize_allowPrivilegeEscalation_containers`
4. `core_minimize_containers_added_capabilities`
5. `core_minimize_containers_capabilities_assigned`
6. `core_minimize_hostIPC_containers`
7. `core_minimize_hostNetwork_containers`
8. `core_minimize_hostPID_containers`
9. `core_minimize_net_raw_capability_admission`
10. `core_minimize_privileged_containers`
11. `core_minimize_root_containers_admission`
12. `core_no_secrets_envs`
13. `core_seccomp_profile_docker_default`
14. `container_network_interface_file_permissions`
15. `container_network_interface_file_ownership`
16. `kubernetes_pki_key_file_permissions_check`
17. `core_no_secrets_in_envs`
18. `core_default_service_account_usage_check`
19. `core_minimize_service_account_token_mount`
20. `core_minimize_hostpath_pv_creation`
21. `core_minimize_admission_hostpath_volumes`
22. `cni_network_policy_support_check`
23. `core_namespace_network_policy_check`
24. `core_secrets_as_files`
25. `external_secret_storage_check`
26. `external_secret_storage_authentication_check`
27. `external_secret_storage_audit_check`
28. `external_secret_storage_encryption_check`
29. `external_secret_storage_rotation_check`
30. `namespace_isolation_check`
31. `core_security_context_check`
32. `default_namespace_usage_check`
33. `namespace_resource_isolation_check`
34. `namespace_network_policy_enforcement_check`
35. `namespace_creation_and_usage_check`
36. `apply_security_context_to_pods`
37. `apply_security_context_to_containers`
38. `general_config_file_ownership_check`
39. `flanneld_file_permissions_check`
40. `network_policy_isolation_check`
41. `core_avoid_secrets_usage`
42. `config_file_permissions_check`
43. `general_config_file_ownership_check`
44. `rbac_minimize_hostpath_mount_in_pod_creation`


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
3. Follow the naming convention: `core_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def core_example_function_check():
    """
    Example compliance check for Kubernetes CORE service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific core configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in core check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: CORE
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **Core Components**: Essential Kubernetes core functionality
- **Pods**: Pod security policies and configurations
- **Namespaces**: Namespace isolation and security
- **Services**: Service networking and security
- **ConfigMaps/Secrets**: Configuration and secret management


## Implementation Guidelines
- All functions are based on Kubernetes CORE API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
