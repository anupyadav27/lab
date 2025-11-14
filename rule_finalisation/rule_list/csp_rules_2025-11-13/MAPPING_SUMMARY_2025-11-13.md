# Function ↔ Compliance Mapping Summary

**Generated**: 2025-11-13
**Source**: consolidated_compliance_rules_FINAL.csv

## Overview

Mapping between compliance functions and compliance requirement IDs for traceability.

## Statistics

| CSP | Unique Functions | Compliance IDs | Total Mappings | Avg Compliance/Function |
|-----|-----------------|----------------|----------------|-------------------------|
| **ALICLOUD** | 904 | 905 | 5232 | 5.8 |
| **AWS** | 716 | 960 | 4387 | 6.1 |
| **AZURE** | 888 | 1093 | 4216 | 4.7 |
| **GCP** | 654 | 913 | 3704 | 5.7 |
| **IBM** | 959 | 934 | 5230 | 5.5 |
| **K8S** | 526 | 747 | 2380 | 4.5 |
| **ORACLE** | 1175 | 874 | 5176 | 4.4 |

## Files Per CSP

Each CSP directory contains 3 mapping files:

### 1. `<csp>_function_to_compliance_mapping_<date>.json`
**Format**: Function → List of Compliance IDs

```json
{
  "aws.iam.user.accesskey_unused": [
    "canada_pbmm_moderate_multi_cloud_CCCS_AC-2_0002",
    "fedramp_moderate_multi_cloud_AC-2_0002",
    "hipaa_multi_cloud_164_308_a_3_ii_b_0006",
    ...
  ]
}
```

**Use**: Find all compliance requirements that use a specific function

### 2. `<csp>_compliance_to_function_mapping_<date>.json`
**Format**: Compliance ID → List of Functions

```json
{
  "hipaa_multi_cloud_164_308_a_3_i_0004": [
    "aws.iam.user.accesskey_unused",
    "aws.iam.user.mfa_enabled",
    ...
  ]
}
```

**Use**: Find all functions needed for a specific compliance requirement

### 3. `<csp>_function_compliance_detailed_<date>.json`
**Format**: Function → Detailed compliance metadata

```json
{
  "aws.iam.user.accesskey_unused": {
    "function": "aws.iam.user.accesskey_unused",
    "total_compliance_mappings": 15,
    "compliance_items": [
      {
        "compliance_id": "hipaa_multi_cloud_164_308_a_3_i_0004",
        "framework": "HIPAA",
        "requirement_id": "164_308_a_3_i",
        "requirement_name": "Workforce security",
        "automation_type": "automated"
      }
    ]
  }
}
```

**Use**: Get complete context for each function's compliance usage

## Usage Examples

### Find compliance IDs for a function
```python
# Load function→compliance mapping
with open('aws/aws_function_to_compliance_mapping_2025-11-13.json') as f:
    mapping = json.load(f)

# Get all compliance IDs using this function
compliance_ids = mapping['aws.iam.user.accesskey_unused']
print(f'Used in {len(compliance_ids)} compliance requirements')
```

### Find functions for a compliance requirement
```python
# Load compliance→function mapping
with open('aws/aws_compliance_to_function_mapping_2025-11-13.json') as f:
    mapping = json.load(f)

# Get all functions for HIPAA requirement
functions = mapping['hipaa_multi_cloud_164_308_a_3_i_0004']
print(f'{len(functions)} functions needed')
```

### Get detailed context
```python
# Load detailed mapping
with open('aws/aws_function_compliance_detailed_2025-11-13.json') as f:
    mapping = json.load(f)

# Get all compliance context for a function
details = mapping['aws.iam.user.accesskey_unused']
print(f"Function: {details['function']}")  
print(f"Used in {details['total_compliance_mappings']} requirements")
for item in details['compliance_items']:
    print(f"  - {item['framework']}: {item['requirement_name']}")
```

## Benefits

1. **Traceability**: Know which compliance requirements use each function
2. **Impact Analysis**: Understand impact of changes to functions
3. **Coverage**: See which functions are most widely used
4. **Planning**: Prioritize function implementation by compliance coverage
5. **Reporting**: Generate compliance coverage reports

---

**Generated**: 2025-11-13  
**Total CSPs**: 7  