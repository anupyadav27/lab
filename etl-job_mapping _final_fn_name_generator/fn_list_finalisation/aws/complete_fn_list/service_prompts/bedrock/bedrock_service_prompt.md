# AWS Service Compliance Prompt Template

## SERVICE: bedrock
**Functions Count**: 5

---

## INPUT DATA FOR THIS SERVICE

```json
{
  "services": {
    "bedrock": {
      "check_functions": [
        "bedrock_agent_guardrail_enabled",
        "bedrock_guardrail_prompt_attack_filter_enabled",
        "bedrock_guardrail_sensitive_information_filter_enabled",
        "bedrock_model_invocation_logging_enabled",
        "bedrock_model_invocation_logs_encryption_enabled",
      ]
    }
  }
}
```

---

## COMPLIANCE TRANSFORMATION PROMPT

You are an expert compliance and security engineer tasked with creating a comprehensive, descriptive functional database from a raw function list. Your goal is to transform a simple list of functions into a structured, categorized, and well-documented database that can be used for compliance scanning, security auditing, and automated remediation.

## TASK REQUIREMENTS

### 1. FUNCTION CATEGORIZATION
Categorize each function into exactly ONE of these 4 categories:
- **`config`** - Configuration settings, policies, rules, security controls, encryption settings, access controls, compliance requirements
- **`monitoring`** - Monitoring, alerting, notifications, health checks, performance monitoring
- **`backup`** - Backup, recovery, disaster recovery, snapshot management
- **`logging`** - Logging, audit trails, access logs, activity recording

### 2. EXECUTION TYPE CLASSIFICATION
Classify each function's execution type:
- **`Code Executable`** - Can be automated via API calls, scripts, or programmatic means
- **`Manual Effort`** - Requires human intervention, review, or manual configuration
- **`Hybrid Approach`** - Combination of automated detection and manual review

### 3. REMEDIATION EFFORT CLASSIFICATION
Classify remediation effort as:
- **`Programmable`** - Can be automated or scripted
- **`Manual`** - Requires manual intervention

### 4. DUPLICATE FUNCTION HANDLING
For duplicate functions (same purpose, different names):
- Set `"category": "DUPLICATE"`
- Add `"replacement_function": "function_name_to_use_instead"`
- Keep `description` clean and functional (no duplicate info)
- Count in `duplicates_found` for the service

### 5. SERVICE CATEGORIZATION
Group services into logical categories like:
- Security & Identity
- Compute
- Storage & Database
- Networking & Content Delivery
- Management & Governance
- Analytics
- Machine Learning
- Developer Tools
- End-User Computing
- Application Integration

## OUTPUT STRUCTURE

Create a JSON file with this exact structure:

```json
{
  "scan_metadata": {
    "description": "bedrock - Compliance Functions Mapping - OPTIMIZED VERSION",
    "total_services": 1,
    "total_check_functions": 5,
    "total_unique_functions": 5,
    "total_duplicates_removed": 0,
    "generated_from": "bedrock compliance functions",
    "last_updated": "[TIMESTAMP]",
    "optimization_notes": "Intelligently categorized functions by cloud security expert analysis, grouped by service, simplified to 4 clear categories with execution types and remediation effort classification"
  },
  "services": {
    "bedrock": {
      "service_name": "bedrock",
      "service_category": "[SERVICE_CATEGORY]",
      "check_functions": [
        {
          "function_name": "function_name",
          "category": "config|monitoring|backup|logging|DUPLICATE",
          "execution_type": "Code Executable - <description>|Manual Effort - <description>|Hybrid Approach - <description>",
          "description": "Clear, concise description of what the function does",
          "remediation_effort": "Programmable|Manual",
          "replacement_function": "function_name_to_use" // ONLY for duplicates
        }
      ],
      "check_count": 5,
      "duplicates_found": 0
    }
  },
  "category_summary": {
    "config": 0,
    "monitoring": 0,
    "backup": 0,
    "logging": 0
  },
  "execution_type_summary": {
    "code_executable": 0,
    "manual_effort": 0,
    "hybrid_approach": 0
  },
  "duplicate_analysis": {
    "total_duplicates_found": 0,
    "duplicate_categories": {
      "exact_name_duplicates": 0,
      "functional_duplicates": 0,
      "similar_purpose_duplicates": 0
    },
    "services_with_most_duplicates": []
  }
}
```

## QUALITY REQUIREMENTS

### 1. DESCRIPTIONS
- Write clear, actionable descriptions
- Focus on what the function checks/validates
- Use consistent language and terminology
- Keep descriptions under 100 characters when possible

### 2. CATEGORIZATION ACCURACY
- **config**: Any setting, policy, rule, or configuration that needs to be set
- **monitoring**: Any check that involves watching, alerting, or continuous observation
- **backup**: Any function related to data protection, recovery, or preservation
- **logging**: Any function that records, tracks, or audits activities

### 3. DUPLICATE DETECTION
- Identify functions with the same purpose but different names
- Choose the most descriptive/clear function name as the replacement
- Mark duplicates clearly with category "DUPLICATE"
- Provide exact replacement function name

### 4. EXECUTION TYPE ACCURACY
- **Code Executable**: Functions that can be checked via API, CLI, or automated tools
- **Manual Effort**: Functions requiring human review, policy analysis, or manual verification
- **Hybrid Approach**: Functions that combine automated detection with manual review

## EXAMPLE TRANSFORMATION

**Input Function**: `s3_bucket_public_access_block`

**Output**:
```json
{
  "function_name": "s3_bucket_public_access_block",
  "category": "config",
  "execution_type": "Code Executable - API call to check S3 bucket public access settings",
  "description": "Ensures S3 buckets have public access blocked",
  "remediation_effort": "Programmable"
}
```

## IMPORTANT NOTES

- Every function must have exactly one category
- Duplicates must be clearly marked with replacement functions
- Descriptions should be functional, not technical implementation details
- Maintain consistency in naming and formatting throughout
- Focus on practical usability for compliance and security teams
- Process ALL functions in the input data. Do not skip any.
- Keep the EXACT original function names from the input

Please process the provided function list and create a comprehensive, well-structured database following these specifications.
