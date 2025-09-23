# Kubernetes RBAC Service Compliance Prompt

## Service Information
- **Service Name**: RBAC
- **Total Functions**: 15
- **Service Type**: Kubernetes Component

## Function List
The following 15 functions are available for Kubernetes RBAC compliance checks:

1. `rbac_cluster_admin_usage`
2. `rbac_minimize_csr_approval_access`
3. `rbac_minimize_node_proxy_subresource_access`
4. `rbac_minimize_pod_creation_access`
5. `rbac_minimize_pv_creation_access`
6. `rbac_minimize_secret_access`
7. `rbac_minimize_service_account_token_creation`
8. `rbac_minimize_webhook_config_access`
9. `rbac_minimize_wildcard_use_roles`
10. `rbac_limit_bind_permission`
11. `rbac_limit_impersonate_permission`
12. `rbac_limit_escalate_permission`
13. `rbac_limit_secrets_access`
14. `namespace_boundaries_enforcement_check`
15. `rbac_limit_service_account_token_creation`


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
3. Follow the naming convention: `rbac_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def rbac_example_function_check():
    """
    Example compliance check for Kubernetes RBAC service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific rbac configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in rbac check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: RBAC
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **RBAC**: Role-Based Access Control
- **Roles**: Cluster and namespace roles
- **RoleBindings**: Role binding configurations
- **Service Accounts**: Service account permissions
- **Privilege Escalation**: Privilege escalation prevention


## Implementation Guidelines
- All functions are based on Kubernetes RBAC API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
