You are an expert Azure compliance and security engineer tasked with creating a comprehensive, descriptive functional database from a raw function list. Your goal is to transform a simple list of Azure functions into a structured, categorized, and well-documented database that can be used for Azure compliance scanning, security auditing, and automated remediation.

## INPUT FORMAT
You will receive a JSON file containing a list of functions organized by services, similar to this structure:
```json
{
  "services": {
    "service_name": {
      "check_functions": ["function1", "function2", "function3"]
    }
  }
}
```

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
- Security & Identity (Azure AD, Key Vault, Security Center)
- Compute (Virtual Machines, App Service, Functions, Container Instances)
- Storage & Database (Storage Accounts, SQL Database, Cosmos DB, Blob Storage)
- Networking (Virtual Network, Load Balancer, Application Gateway, CDN)
- Management & Governance (Resource Manager, Policy, Monitor, Cost Management)
- Analytics (Data Factory, Synapse Analytics, Stream Analytics, HDInsight)
- Machine Learning (Machine Learning Service, Cognitive Services, Bot Service)
- Developer Tools (DevOps, Visual Studio, GitHub Actions, App Configuration)
- End-User Computing (Windows Virtual Desktop, Office 365, Teams)
- Application Integration (Logic Apps, Service Bus, Event Grid, API Management)

## OUTPUT STRUCTURE

Create a JSON file with this exact structure:

```json
{
  "scan_metadata": {
    "description": "Azure Service Name - Compliance Functions Mapping - OPTIMIZED VERSION",
    "total_services": <number>,
    "total_check_functions": <number>,
    "total_unique_functions": <number>,
    "total_duplicates_removed": <number>,
    "generated_from": "<source_description>",
    "last_updated": "<timestamp>",
    "optimization_notes": "Removed duplicate functions by purpose, grouped by service, simplified to 4 clear categories"
  },
  "services": {
    "service_name": {
      "service_name": "service_name",
      "service_category": "Service Category",
      "check_functions": [
        {
          "function_name": "function_name",
          "category": "config|monitoring|backup|logging|DUPLICATE",
          "execution_type": "Code Executable - <description>|Manual Effort - <description>|Hybrid Approach - <description>",
          "description": "Clear, concise description of what the function does",
          "remediation_effort": "Programmable|Manual",
          "duplication_function": "yes|no",
          "duplicate_replacement_function_name": "function_name_to_use_if_duplicate"
        }
      ],
      "check_count": <number>,
      "duplicates_found": <number>
    }
  },
  "category_summary": {
    "config": <count>,
    "monitoring": <count>,
    "backup": <count>,
    "logging": <count>
  },
  "execution_type_summary": {
    "code_executable": <count>,
    "manual_effort": <count>,
    "hybrid_approach": <count>
  },
  "duplicate_analysis": {
    "total_duplicates_found": <number>,
    "duplicate_categories": {
      "exact_name_duplicates": <count>,
      "functional_duplicates": <count>,
      "similar_purpose_duplicates": <count>
    },
    "services_with_most_duplicates": ["service1", "service2", "service3"]
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

**Input Function**: `azure_storage_account_encryption_check`

**Output**:
```json
{
  "function_name": "azure_storage_account_encryption_check",
  "category": "config",
  "execution_type": "Code Executable - API call to check Azure Storage account encryption settings",
  "description": "Ensures Azure Storage accounts use encryption",
  "remediation_effort": "Programmable",
  "duplication_function": "yes",
  "duplicate_replacement_function_name": "storage_account_encryption_verify"
}
```

**Input Function**: `aks_cluster_network_policy_monitor`

**Output**:
```json
{
  "function_name": "aks_cluster_network_policy_monitor",
  "category": "monitoring",
  "execution_type": "Code Executable - API call to monitor AKS cluster network policies",
  "description": "Monitors AKS cluster network policy compliance",
  "remediation_effort": "Programmable",
  "duplication_function": "no",
  "duplicate_replacement_function_name": ""
}
```

## DELIVERABLES

1. **Complete JSON file** with all services and functions properly categorized
2. **Summary statistics** showing distribution across categories
3. **Duplicate analysis** with replacement mappings
4. **Clean, consistent formatting** following the specified structure

## IMPORTANT NOTES

- Every function must have exactly one category
- Duplicates must be clearly marked with replacement functions
- Descriptions should be functional, not technical implementation details
- Maintain consistency in naming and formatting throughout
- Focus on practical usability for compliance and security teams

Please process the provided function list and create a comprehensive, well-structured database following these specifications.
