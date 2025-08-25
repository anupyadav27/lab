# GCP APIKEY Service Compliance Prompt

## Service Information
- **Service Name**: APIKEY
- **Description**: GCP APIKEY Service
- **Total Functions**: 38
- **SDK Client**: apikeys_client
- **Service Type**: security

## Function List
The following 38 functions are available for APIKEY compliance checks:

1. `kms_keys_management_organization_defined`
2. `kms_keys_management_compliance`
3. `logging_log_sinks_encrypted_with_kms_key`
4. `kms_keys_sensitive_data_encrypted`
5. `ai_platform_endpoint_kms_key_configured`
6. `kms_keys_blocked_actions_restricted`
7. `kms_keys_not_scheduled_for_deletion`
8. `kms_keys_no_scheduled_destruction`
9. `kms_key_automatic_rotation_enabled`
10. `kms_keys_no_deletion_scheduled`
11. `kms_keys_disallowed_actions_restricted`
12. `secretmanager_secret_encryption_customer_managed_key`
13. `kms_keys_not_scheduled_for_destruction`
14. `kms_keys_intellectual_property_protection`
15. `kms_keys_cryptography_management`
16. `kms_keys_certificate_management`
17. `kms_keys_protection`
18. `kms_keys_use_authorized_algorithms`
19. `kms_keys_confidentiality_protection`
20. `kms_keys_encryption_enabled`
21. `kms_keys_sensitive_information_encryption`
22. `kms_keys_integrity_authenticity_protection`
23. `kms_keys_authorized_algorithms`
24. `kms_keys_certificados_cualificados`
25. `kms_keys_signature_verification`
26. `kms_keys_encryption_enforced`
27. `kms_key_rotation_schedule_format`
28. `kms_cryptokeys_restrict_public_access`
29. `kms_cryptokeys_no_public_access`
30. `kms_keys_rotation_within_90_days`
31. `kms_cryptokeys_restrict_anonymous_public_access`
32. `kms_keys_secure_management_procedures`
33. `kms_keys_encrypt_decrypt_ephi`
34. `kms_keys_encrypt_ephi`
35. `kms_keys_fips_validated_cryptography`
36. `kms_key_exchange_algorithm_strong`
37. `ai_platform_notebook_kms_key_configured`
38. `certificate_manager_rsa_key_minimum_length_2048_bits`


## Compliance Framework Coverage
This service supports compliance checks for:
- **NIST Cybersecurity Framework**
- **PCI DSS v4.0**
- **ISO 27001**
- **SOC 2**
- **GDPR**
- **HIPAA** (where applicable)

## Usage Instructions
1. Use the function names above to create compliance checks
2. Each function should be implemented as a separate compliance rule
3. Follow the naming convention: `apikey_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def apikey_example_function_check():
    """
    Example compliance check for APIKEY service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in apikey check: {e}")
        return False
```

## Notes
- All functions are based on GCP APIKEY API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
