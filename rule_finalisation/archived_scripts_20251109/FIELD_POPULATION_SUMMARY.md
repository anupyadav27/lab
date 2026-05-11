# CSV Field Population Summary

## Overview
The consolidated CSV has been updated with improved field mapping. Different cloud providers have different fields populated based on their source JSON structures.

## Field Population by Cloud Provider

### AWS (19/20 fields populated)
✅ All relevant fields populated:
- `rule_id`, `scope`, `program`, `assertion_key`, `category`
- `provider_service`, `service`, `resource`, `template_id`
- `assertion_bindings`, `implementation_status`, `mapping_status`
- `mapped`, `version`, `generated_at`

❌ Empty fields:
- `alt_id` (not present in AWS source data)

### Azure, GCP, IBM (14/20 fields populated)
✅ Populated fields:
- `rule_id`, `scope`, `program`, `assertion_key`, `assertion_id`
- `category`, `provider_service`, `provider_category`, `resource_class`
- `mapping_status`, `mapped`, `version`, `generated_at`

❌ Empty fields (not in source structure):
- `service`, `resource`, `template_id`, `assertion_bindings`, `implementation_status`, `alt_id`

### OCI, Alicloud (14/20 fields populated)
✅ Populated fields:
- `rule_id`, `scope`, `program`, `assertion_key`, `assertion_id`
- `category`, `provider_service`, `provider_category`
- `mapping_status`, `mapped`, `alt_id`, `version`, `generated_at`

❌ Empty fields (not in source structure):
- `resource_class`, `service`, `resource`, `template_id`, `assertion_bindings`, `implementation_status`

### K8s (13/20 fields populated)
✅ Populated fields:
- `rule_id`, `scope`, `program`, `assertion_key`, `assertion_id`
- `category`, `provider_service`, `provider_category`, `service`
- `assertion_bindings`, `mapping_status`, `mapped`, `version`, `generated_at`

❌ Empty fields (not in source structure):
- `resource_class`, `resource`, `template_id`, `implementation_status`, `alt_id`

## Key Improvements Made

1. **AWS Rules**: 
   - Now extracts `program` from `template_id`
   - Derives `category` from `template_id`
   - Populates `assertion_key` from first assertion binding
   - Adds version and generation timestamp

2. **All Providers**:
   - Consistent `mapping_status` field
   - Boolean `mapped` field converted to string
   - Version and timestamp from metadata

## Why Some Fields Are Empty

The empty fields are intentional and reflect the actual structure of each cloud provider's source JSON:
- **AWS** doesn't have `alt_id` in its schema
- **Azure/GCP/IBM** use different naming conventions (no `template_id`)
- **OCI/Alicloud** don't include `resource_class` explicitly
- **K8s** has a completely different structure focused on programs and services

This is a **normalized schema** that accommodates all providers while preserving their unique data.




