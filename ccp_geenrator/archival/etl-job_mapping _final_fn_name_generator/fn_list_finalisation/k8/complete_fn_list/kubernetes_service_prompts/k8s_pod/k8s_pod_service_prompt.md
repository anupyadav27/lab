# Kubernetes K8S_POD Service Compliance Prompt

## Service Information
- **Service Name**: K8S_POD
- **Total Functions**: 38
- **Service Type**: Kubernetes Component

## Function List
The following 38 functions are available for Kubernetes K8S_POD compliance checks:

1. `k8s_pod_security_parameters_enforcement`
2. `k8s_pod_prevent_key_substitution`
3. `k8s_pod_verify_no_live_pan`
4. `k8s_pod_remove_test_data`
5. `k8s_pod_script_integrity_check`
6. `k8s_pod_sensitive_data_debugging_control`
7. `k8s_pod_sensitive_data_retention_configuration`
8. `k8s_pod_transient_data_secure_deletion`
9. `k8s_pod_transient_data_immutability_check`
10. `k8s_pod_transient_data_debugging_control`
11. `k8s_pod_user_input_guidance_check`
12. `k8s_pod_secure_data_deletion`
13. `k8s_pod_forensic_data_residue_check`
14. `k8s_pod_transient_data_secure_deletion`
15. `k8s_pod_transient_data_erasure`
16. `k8s_pod_sensitive_data_residue_check`
17. `k8s_pod_side_channel_protection`
18. `k8s_pod_cryptographic_protection`
19. `k8s_pod_user_interaction_protection`
20. `k8s_pod_verify_update_integrity`
21. `k8s_pod_user_input_validation`
22. `k8s_pod_mask_pan_display`
23. `k8s_pod_mask_pan_display`
24. `k8s_pod_default_pan_masking`
25. `k8s_pod_enforce_rng_usage`
26. `k8s_pod_prevent_cleartext_data_sharing`
27. `k8s_pod_secure_shared_resource_integration`
28. `k8s_pod_prevent_application_segregation_bypass`
29. `k8s_pod_cryptographic_signature_verification`
30. `k8s_pod_integrity_verification`
31. `k8s_pod_input_validation`
32. `k8s_pod_error_handling`
33. `k8s_pod_race_condition_prevention`
34. `k8s_pod_vulnerability_testing`
35. `k8s_pod_generate_sbom`
36. `k8s_pod_dependency_mapping`
37. `k8s_pod_parser_restriction`
38. `k8s_pod_resource_starvation_protection`


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
3. Follow the naming convention: `k8s_pod_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def k8s_pod_example_function_check():
    """
    Example compliance check for Kubernetes K8S_POD service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific k8s_pod configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in k8s_pod check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: K8S_POD
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **K8S_POD**: Kubernetes k8s_pod component
- **Configuration**: k8s_pod specific configurations
- **Security**: k8s_pod security settings
- **Monitoring**: k8s_pod monitoring and logging
- **Compliance**: k8s_pod compliance requirements


## Implementation Guidelines
- All functions are based on Kubernetes K8S_POD API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
