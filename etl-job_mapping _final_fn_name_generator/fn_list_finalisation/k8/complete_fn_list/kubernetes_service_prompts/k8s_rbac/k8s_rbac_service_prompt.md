# Kubernetes K8S_RBAC Service Compliance Prompt

## Service Information
- **Service Name**: K8S_RBAC
- **Total Functions**: 49
- **Service Type**: Kubernetes Component

## Function List
The following 49 functions are available for Kubernetes K8S_RBAC compliance checks:

1. `k8s_rbac_account_monitoring`
2. `k8s_rbac_account_lifecycle_management`
3. `k8s_rbac_access_enforcement`
4. `k8s_rbac_separation_of_duties`
5. `k8s_rbac_split_knowledge_enforcement`
6. `k8s_rbac_dual_control_enforcement`
7. `k8s_rbac_key_custodian_acknowledgement`
8. `k8s_rbac_define_access_control_model`
9. `k8s_rbac_least_privilege_enforcement`
10. `k8s_rbac_privilege_approval_tracking`
11. `k8s_rbac_periodic_access_review`
12. `k8s_rbac_least_privilege_system_accounts`
13. `k8s_rbac_system_account_access_review`
14. `k8s_rbac_audit_shared_id_usage`
15. `k8s_rbac_unique_authentication_per_customer`
16. `k8s_rbac_authorization_enforcement`
17. `k8s_rbac_terminate_user_access`
18. `k8s_rbac_disable_inactive_accounts`
19. `k8s_rbac_account_lockout_policy`
20. `k8s_rbac_password_reset_policy`
21. `k8s_rbac_password_complexity_policy`
22. `k8s_rbac_password_history_policy`
23. `k8s_rbac_password_expiration_policy`
24. `k8s_rbac_dynamic_access_analysis`
25. `k8s_rbac_customer_password_guidance`
26. `k8s_rbac_password_expiration_policy`
27. `k8s_rbac_dynamic_access_analysis`
28. `k8s_rbac_unique_authentication_factor`
29. `k8s_rbac_mfa_enforcement`
30. `k8s_rbac_remote_mfa_enforcement`
31. `k8s_rbac_mfa_configuration_check`
32. `k8s_rbac_interactive_login_prevention`
33. `k8s_rbac_prevent_hardcoded_passwords`
34. `k8s_service_account_password_policy_enforcement`
35. `k8s_rbac_tpsp_engagement_tracking`
36. `k8s_rbac_tpsp_compliance_monitoring`
37. `k8s_rbac_tpsp_responsibility_matrix`
38. `k8s_rbac_tpsp_acknowledgment_tracking`
39. `k8s_rbac_tpsp_information_provision`
40. `k8s_rbac_check_default_credentials`
41. `k8s_rbac_verify_default_credentials_removal`
42. `k8s_rbac_user_input_for_credential_change`
43. `k8s_rbac_enforce_non_default_credentials`
44. `k8s_rbac_access_control_audit`
45. `k8s_rbac_access_attempt_logging`
46. `k8s_rbac_input_rate_limiting`
47. `k8s_rbac_authentication_mechanism_check`
48. `k8s_rbac_authentication_credentials_strength_check`
49. `k8s_rbac_authentication_decision_enforcement_check`


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
3. Follow the naming convention: `k8s_rbac_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Kubernetes API

## Example Implementation
```python
def k8s_rbac_example_function_check():
    """
    Example compliance check for Kubernetes K8S_RBAC service
    """
    try:
        # Implementation using Kubernetes API
        # from kubernetes import client, config
        # config.load_kube_config()
        # v1 = client.CoreV1Api()
        
        # Check specific k8s_rbac configuration
        # result = v1.read_namespaced_config_map(...)
        
        pass
    except Exception as e:
        logger.error(f"Error in k8s_rbac check: {e}")
        return False
```

## Kubernetes API Integration
- **Service**: K8S_RBAC
- **API Group**: Core API or Custom Resource Definitions
- **Authentication**: Service Account, kubeconfig, or token-based
- **Namespace**: Cluster-wide or namespace-specific

## Service-Specific Notes
- **K8S_RBAC**: Kubernetes k8s_rbac component
- **Configuration**: k8s_rbac specific configurations
- **Security**: k8s_rbac security settings
- **Monitoring**: k8s_rbac monitoring and logging
- **Compliance**: k8s_rbac compliance requirements


## Implementation Guidelines
- All functions are based on Kubernetes K8S_RBAC API
- Ensure proper RBAC permissions are configured
- Consider cluster-wide vs namespace-specific checks
- Implement appropriate retry logic for API calls
- Use Kubernetes client libraries for API interactions
- Follow Kubernetes security best practices
- Consider multi-cluster environments
