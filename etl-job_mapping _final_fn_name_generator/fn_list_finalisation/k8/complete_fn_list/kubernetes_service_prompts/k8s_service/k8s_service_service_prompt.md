# Kubernetes K8S_SERVICE Service Compliance Prompt

## Service Information
- **Service Name**: K8S_SERVICE
- **Total Functions**: 19
- **Service Type**: Kubernetes Component

## Function List
The following 19 functions are available for Kubernetes K8S_SERVICE compliance checks:

1. `k8s_service_key_management_guidance_distribution`
2. `k8s_service_scope_validation`
3. `k8s_service_org_change_monitor`
4. `k8s_service_enable_security_controls_on_init`
5. `k8s_service_third_party_feature_configuration_check`
6. `k8s_service_enforce_secure_protocols`
7. `k8s_service_enforce_strong_cryptography`
8. `k8s_service_cryptography_compliance_check`
9. `k8s_service_third_party_crypto_configuration_check`
10. `k8s_service_third_party_tool_configuration`
11. `k8s_service_attack_method_identification`
12. `k8s_service_attack_validation`
13. `k8s_service_mitigation_validation`
14. `k8s_service_chain_of_trust_verification`
15. `k8s_service_update_notification`
16. `k8s_service_vulnerability_notification`
17. `k8s_service_sbom_integration`
18. `k8s_service_malicious_file_detection`
19. `k8s_service_object_creation_protection`


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
3. Follow the naming convention: `k8s_service_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def k8s_service_example_function_check():
    """
    Example compliance check for Kubernetes K8S_SERVICE service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific k8s_service configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in k8s_service check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: K8S_SERVICE
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **K8S_SERVICE**: Kubernetes k8s_service component
- **Configuration**: k8s_service specific configurations
- **Security**: k8s_service security settings
- **Monitoring**: k8s_service monitoring and logging
- **Compliance**: k8s_service compliance requirements


## Implementation Guidelines
- All functions are based on Kubernetes K8S_SERVICE API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
