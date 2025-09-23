# GCP APIGATEWAY Service Compliance Prompt

## Service Information
- **Service Name**: APIGATEWAY
- **Description**: GCP APIGATEWAY Service
- **Total Functions**: 28
- **SDK Client**: apigateway_client
- **Service Type**: other

## Function List
The following 28 functions are available for APIGATEWAY compliance checks:

1. `workspace_user_outbound_gateway_disabled`
2. `workspace_api_access_enabled_for_internal_apps`
3. `endpoints_api_type_compliance`
4. `endpoints_service_ssl_certificate_required`
5. `dms_redis_endpoints_tls_ssl_enabled`
6. `gcdms_redis_endpoints_tls_ssl_enabled`
7. `endpoints_cloud_trace_tracing_enabled`
8. `endpoints_methods_cache_encrypted`
9. `dms_endpoints_ssl_configured`
10. `endpoints_trace_enabled`
11. `endpoints_cloud_trace_enabled`
12. `dlp_api_enabled`
13. `apigateway_api_config_use_cloud_armor`
14. `endpoints_api_endpoint_configuration_type_compliant`
15. `apigateway_stage_ssl_certificate_required`
16. `endpoints_api_ssl_certificate_enabled`
17. `endpoints_api_ssl_certificate_associated`
18. `apigateway_methods_cache_encrypted`
19. `endpoints_api_ssl_certificate_required`
20. `apigateway_api_config_uses_cloud_armor`
21. `endpoints_api_endpoint_type_compliant`
22. `api_gateway_trace_tracing_enabled`
23. `apigateway_service_trace_enabled`
24. `endpoints_apis_trace_enabled`
25. `apigateway_tracing_enabled`
26. `endpoints_api_trace_enabled`
27. `datamigration_endpoints_ssl_configured`
28. `datamigration_redis_endpoints_tls_enabled`


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
3. Follow the naming convention: `apigateway_<function_name>`
4. Include appropriate error handling and logging
5. Ensure proper authentication and authorization

## Example Implementation
```python
def apigateway_example_function_check():
    """
    Example compliance check for APIGATEWAY service
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error in apigateway check: {e}")
        return False
```

## Notes
- All functions are based on GCP APIGATEWAY API
- Ensure proper IAM permissions are configured
- Consider regional vs global service differences
- Implement appropriate retry logic for API calls
