# Function-to-Compliance Mapping & Gap Analysis

## Context
You are a cloud security expert working with a CSPM tool. I have an existing function database (prowler.json) with 563 AWS security check functions in snake_case format. I need to map these to compliance frameworks and identify gaps.

## Your Tasks:

### 1. **Map Existing Functions**
- Review compliance items and match them to existing functions from prowler.json
- Multiple functions can map to one compliance item
- One function can satisfy multiple compliance items
- Search for semantic matches, not just exact name matches

### 2. **Identify Gaps** 
- For compliance items with no matching functions, suggest new function names
- Follow existing naming pattern: `{service}_{resource}_{check_description}`
- Only suggest functions that are boto3-implementable (not theoretical)
- Only suggest functions for "Automated" compliance items

### 3. **Update Function Database**
- Add new suggested functions to the database for future compliance mapping
- Ensure no duplicate function names
- Validate that new functions follow snake_case convention

## Input Format:
- **Function Database**: prowler.json (563 existing functions organized by AWS service)
- **Compliance Framework**: JSON with compliance items containing:
  - `id`: Compliance identifier  
  - `title`: Requirement title
  - `assessment`: "Automated" or "Manual" 
  - `description`: Detailed requirement
  - `function_names`: Current suggestions (may be empty/incorrect)

## Output Format:
```json
{
  "compliance_id": "1.1",
  "title": "Compliance requirement title",
  "existing_functions_mapped": [
    "account_maintain_current_contact_details",
    "account_security_contact_information_is_registered"
  ],
  "coverage_assessment": "complete|partial|none",
  "new_functions_needed": [
    {
      "name": "account_alternate_contacts_configured",
      "boto3_api": "account.get_alternate_contact()",
      "service": "account",
      "rationale": "Check if alternate contacts are properly configured"
    }
  ],
  "mapping_notes": "Brief explanation of mapping decisions and any conflicts resolved"
}
```

## Example Mapping:
**Compliance Item**: "1.3 - Ensure no 'root' user account access key exists"
- **Existing Functions Mapped**: `["account_root_access_key_not_exists"]`
- **Coverage**: "complete" 
- **New Functions**: None needed
- **Notes**: "Direct match found in prowler.json account service"

## Key Constraints:
- Only suggest functions for "Automated" compliance items (skip "Manual" ones)
- Function names must follow snake_case: `service_resource_check`
- Each function must be implementable via boto3 API calls (specify which API)
- Avoid suggesting functions that duplicate existing ones
- Process compliance items in batches of 10 for manageability

## Validation Rules for New Functions:
1. **Boto3 Implementability**: Must use real AWS API calls (describe_*, get_*, list_*)
2. **Naming Convention**: Follow existing pattern in prowler.json
3. **Service Categorization**: Correctly assign to appropriate AWS service
4. **Uniqueness**: Check against existing 563 functions to avoid duplicates

## Conflict Resolution:
- If compliance JSON suggests function names that conflict with prowler.json, prefer prowler.json names
- If compliance function names don't follow snake_case, convert them appropriately
- Document any name changes in mapping_notes

## Important Note:
Act as cloud security experts for a CSPM (Cloud Security Posture Management) tool. Focus on practical, implementable security checks that can be automated through AWS APIs.