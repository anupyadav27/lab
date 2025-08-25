# Azure Azure AD Service Compliance Prompt

## Service Information
- **Service Name**: ACTIVE_DIRECTORY
- **Display Name**: Azure AD
- **Total Functions**: 34
- **Original Categories**: Identity
- **Categorization Methods**: sdk_example

## Function List
The following 34 functions are available for Azure AD compliance checks:

1. `azuread_inlinepolicy_no_blockedactions_on_keyvaultkeys`
2. `azure_ad_authentication_reconfirm_days_not_zero`
3. `azure_ad_password_reset_notify_users_enabled`
4. `azure_ad_admin_password_reset_notification_enabled`
5. `azure_ad_group_membership_requests_owner_management_disabled`
6. `azure_ad_authentication_reconfirm_days_non_zero`
7. `azuread_keyvault_inline_policies_no_blocked_actions`
8. `azuread_inlinepolicy_disallow_blockedactions_keyvaultkeys`
9. `azuread_inline_policy_keyvault_key_blocked_actions`
10. `azuread_inlinepolicy_no_blockedactions_keyvaultkeys`
11. `azuread_inlinepolicy_keyvaultkey_blockedactions`
12. `azuread_inlinepolicy_no_blockedaction_keyvault_keys`
13. `azure_ad_group_has_member`
14. `azure_ad_user_inactive_credentials`
15. `azuread_keyvault_inline_policies_no_blocked_actions_on_keys`
16. `azure_ad_service_principal_credential_rotation`
17. `azure_ad_user_password_policy_compliance`
18. `azure_ad_user_mfa_enabled`
19. `azure_ad_service_principal_credentials_rotation`
20. `azure_ad_credentials_abuse_prevention`
21. `azure_ad_endpoint_manager_limit_script_execution`
22. `azure_ad_authentication_material_alternate_use_prevention`
23. `azure_ad_mfa_policy_enforced`
24. `azure_ad_user_access_secure_authentication_multi_factor`
25. `azuread_users_create_tenants_disabled`
26. `azuread_administration_portal_access_restriction`
27. `azuread_device_registration_require_mfa`
28. `azuread_inlinepolicy_no_blockedaction_keyvaultkeys`
29. `azuread_keyvaultkeys_inlinepolicies_no_blockedactions`
30. `azuread_inlinepolicy_no_blockedactions_keyvault_keys`
31. `azuread_keyvault_inline_policy_blocked_actions`
32. `azure_active_directory_users_application_registration_disabled`
33. `active_directory_security_defaults_enabled`
34. `azure_active_directory_gallery_apps_addition_disabled`


## Compliance Framework Coverage
This service supports compliance checks for:
- **NIST Cybersecurity Framework**
- **PCI DSS v4.0**
- **ISO 27001**
- **SOC 2**
- **GDPR**
- **HIPAA** (where applicable)
- **Azure Security Benchmark**

## Usage Instructions
1. Use the function names above to create compliance checks
2. Each function should be implemented as a separate compliance rule
3. Follow the naming convention: `active_directory_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def active_directory_example_function_check():
    """
    Example compliance check for Azure AD service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.active_directory import Active_DirectoryManagementClient
        
        # credential = DefaultAzureCredential()
        # client = Active_DirectoryManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in active_directory check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure AD
- **SDK Namespace**: azure.mgmt.active_directory
- **Client Class**: Active_DirectoryManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure AD API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
