# Azure Azure Compute Service Compliance Prompt

## Service Information
- **Service Name**: COMPUTE
- **Display Name**: Azure Compute
- **Total Functions**: 76
- **Original Categories**: Compute, Unknown, Compute|Storage|Database
- **Categorization Methods**: sdk_example, function_name

## Function List
The following 76 functions are available for Azure Compute compliance checks:

1. `compute_virtualmachine_has_managed_disks`
2. `compute_extension_approved_only`
3. `compute_virtualmachine_endpoint_protection_installed`
4. `compute_virtual_machine_trusted_launch_enabled`
5. `compute_virtualmachine_instances_in_vnet`
6. `compute_virtualmachine_in_vnet_names_match`
7. `compute_virtualmachine_in_virtualnetwork`
8. `compute_manageddisks_attached_to_vms_on_termination`
9. `compute_virtual_machine_installed_applications_version_platform`
10. `compute_manageddisks_attached_on_termination`
11. `compute_virtual_machine_installed_apps_version_platform`
12. `compute_virtualmachine_ssh_public_key_launched`
13. `compute_virtualmachine_ssh_public_key_required`
14. `compute_virtualmachine_azure_ssh_public_key_required`
15. `compute_virtualmachine_ssh_public_key_usage`
16. `compute_imds_v2_only_enabled`
17. `compute_azure_images_no_backdoor`
18. `compute_service_infrastructure_modification_monitoring`
19. `azure_compute_instance_creation_in_unused_regions_prevented`
20. `compute_storage_database_resources_protected`
21. `compute_operational_systems_secure_software_installation`
22. `compute_system_capacity_forecast_management`
23. `compute_system_transition_controlled_execution`
24. `compute_java_version_supported`
25. `compute_runtime_python_version_supported`
26. `compute_php_version_supported`
27. `compute_remote_debugging_disabled`
28. `azure_compute_virtualmachine_device_lock`
29. `azure_compute_reference_monitor_implementation`
30. `azure_compute_hardening_standards_enforcement`
31. `azure_compute_function_isolation`
32. `azure_compute_service_protocol_management`
33. `azure_compute_console_lock_enforcement`
34. `azure_compute_identify_sensitive_data`
35. `azure_compute_identify_sensitive_configuration`
36. `azure_compute_check_builtin_account_credentials`
37. `azure_compute_check_builtin_account_key_usage`
38. `azure_compute_default_ssh_key_replacement`
39. `azure_compute_instance_default_credentials_check`
40. `azure_compute_software_required_privileges_validation`
41. `azure_compute_software_access_permissions_check`
42. `azure_compute_software_legacy_features_check`
43. `azure_compute_limit_resource_access`
44. `azure_compute_verify_legacy_feature_usage`
45. `azure_compute_software_privilege_limitation`
46. `azure_compute_software_resource_access_limitation`
47. `azure_compute_software_legacy_feature_usage_detection`
48. `azure_compute_software_privilege_and_resource_limit_check`
49. `azure_compute_software_access_permission_check`
50. `azure_compute_disk_encryption_verification`
51. `azure_compute_data_encryption_check`
52. `azure_compute_memory_data_cleanup`
53. `azure_compute_memory_data_residue_check`
54. `azure_compute_memory_dump_encryption`
55. `azure_compute_error_log_encryption`
56. `azure_compute_keyboard_input_encryption`
57. `azure_compute_camera_input_encryption`
58. `azure_compute_nfc_input_encryption`
59. `azure_compute_memory_dump_protection`
60. `azure_compute_disk_encryption`
61. `azure_compute_vm_disk_encryption`
62. `azure_compute_data_transmission_encryption_check`
63. `azure_compute_software_update_integrity_check`
64. `azure_compute_software_update_notification`
65. `azure_compute_software_update_coverage_check`
66. `azure_compute_application_segregation_verification`
67. `azure_compute_software_files_signature_verification`
68. `azure_compute_input_validation`
69. `azure_compute_string_input_validation`
70. `azure_compute_buffer_size_validation`
71. `azure_compute_return_value_check`
72. `azure_compute_race_condition_mitigation`
73. `azure_compute_generate_sbom`
74. `azure_compute_get_sbom`
75. `azure_compute_verify_third_party_components`
76. `azure_compute_parser_interpreter_restrictive_config`


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
3. Follow the naming convention: `compute_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization using Azure SDK

## Example Implementation
```python
def compute_example_function_check():
    """
    Example compliance check for Azure Compute service
    """
    try:
        # Implementation using Azure SDK
        # from azure.identity import DefaultAzureCredential
        # from azure.mgmt.compute import ComputeManagementClient
        
        # credential = DefaultAzureCredential()
        # client = ComputeManagementClient(credential, subscription_id)
        
        pass
    except Exception as e:
        logger.error(f"Error in compute check: {e}")
        return False
```

## Azure SDK Integration
- **Service**: Azure Compute
- **SDK Namespace**: azure.mgmt.compute
- **Client Class**: ComputeManagementClient
- **Authentication**: DefaultAzureCredential or ServicePrincipalCredential

## Notes
- All functions are based on Azure Azure Compute API
- Ensure proper Azure RBAC permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
- Use Azure Resource Graph for efficient resource queries
