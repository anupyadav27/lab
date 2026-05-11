# Cloud Provider Functions - Complete Summary

**Generated:** 2025-11-08  
**Source:** consolidated_compliance_rules_2025-11-08.csv

---

## Overview

This directory contains compliance check functions organized by service category for **all major cloud providers**:
- AWS (Amazon Web Services)
- Azure (Microsoft Azure)
- GCP (Google Cloud Platform)
- Oracle Cloud Infrastructure (OCI)
- IBM Cloud
- Alicloud (Alibaba Cloud)
- Kubernetes

All function names have been properly categorized by service, with invalid entries (like "No checks defined") filtered out.

---

## Files

| File | Cloud Provider | Services | Functions | Mappings | Size |
|------|----------------|----------|-----------|----------|------|
| `aws_functions_by_service_2025-11-08.json` | AWS | 58 | 386 | 2,495 | 233 KB |
| `azure_functions_by_service_2025-11-08.json` | Azure | 37 | 351 | 1,968 | 183 KB |
| `gcp_functions_by_service_2025-11-08.json` | GCP | 36 | 245 | 1,644 | 146 KB |
| `oracle_functions_by_service_2025-11-08.json` | Oracle | 88 | 439 | 2,984 | 278 KB |
| `ibm_functions_by_service_2025-11-08.json` | IBM | 95 | 533 | 2,996 | 293 KB |
| `alicloud_functions_by_service_2025-11-08.json` | Alicloud | 93 | 492 | 2,926 | 286 KB |
| `kubernetes_functions_by_service_2025-11-08.json` | Kubernetes | 15 | 107 | 110 | 31 KB |

**Total:** 2,553 unique functions across 422 services with 14,123 compliance mappings

---

## JSON Structure

All files follow the same standardized structure:

```json
{
  "metadata": {
    "version": "1.0",
    "cloud_provider": "AWS",
    "generated_date": "2025-11-08",
    "description": "AWS compliance check functions organized by service category",
    "total_services": 58,
    "total_functions": 386,
    "total_compliance_mappings": 2495
  },
  "services": {
    "service_name": {
      "service_name": "iam",
      "function_count": 64,
      "total_compliance_mappings": 618,
      "functions": {
        "function_name": {
          "function_name": "aws_iam_console_mfa_enabled",
          "compliance_count": 2,
          "compliance_ids": ["id1", "id2"]
        }
      }
    }
  }
}
```

---

## Top Services by Cloud Provider

### AWS (58 services, 386 functions)
1. **ec2** - 80 functions, 465 mappings
2. **iam** - 64 functions, 618 mappings
3. **cloudtrail** - 22 functions, 30 mappings
4. **cloudwatch** - 21 functions, 238 mappings
5. **rds** - 20 functions, 214 mappings

### Azure (37 services, 351 functions)
1. **monitor** - 26 functions, 248 mappings
2. **entra** - 21 functions, 78 mappings
3. **defender** - 19 functions, 200 mappings
4. **active** - 14 functions, 381 mappings
5. **network** - 13 functions, 153 mappings

### GCP (36 services, 245 functions)
1. **compute** - 46 functions, 213 mappings
2. **iam** - 34 functions, 431 mappings
3. **sql** - 26 functions, 169 mappings
4. **gke** - 22 functions, 23 mappings
5. **bigquery** - 13 functions, 122 mappings

### Oracle (88 services, 439 functions)
1. **compute** - 80 functions, 468 mappings
2. **identity** - 33 functions, 583 mappings
3. **defender** - 18 functions, 198 mappings
4. **monitoring** - 18 functions, 226 mappings
5. **kms** - 16 functions, 122 mappings

### IBM (95 services, 533 functions)
1. **vsi** - 70 functions, 302 mappings
2. **openshift** - 67 functions, 68 mappings
3. **iam** - 45 functions, 615 mappings
4. **vpc** - 24 functions, 190 mappings
5. **defender** - 18 functions, 198 mappings

### Alicloud (93 services, 492 functions)
1. **ecs** - 80 functions, 464 mappings
2. **ram** - 46 functions, 596 mappings
3. **ack** - 22 functions, 22 mappings
4. **rds** - 22 functions, 215 mappings
5. **oss** - 20 functions, 267 mappings

### Kubernetes (15 services, 107 functions)
1. **api** - 42 functions, 44 mappings
2. **pod** - 13 functions, 14 mappings
3. **rbac** - 12 functions, 12 mappings
4. **etcd** - 10 functions, 10 mappings
5. **federation** - 7 functions, 7 mappings

---

## Usage Examples

### 1. Load AWS functions by service

```python
import json

with open('aws_functions_by_service_2025-11-08.json', 'r') as f:
    aws_data = json.load(f)

# Get all IAM functions
iam_functions = aws_data['services']['iam']['functions']
print(f"IAM has {len(iam_functions)} functions")

# Get specific function details
func = iam_functions['aws_iam_console_mfa_enabled']
print(f"Function: {func['function_name']}")
print(f"Compliance controls: {func['compliance_count']}")
print(f"IDs: {func['compliance_ids']}")
```

### 2. Compare services across cloud providers

```python
import json

csps = ['aws', 'azure', 'gcp', 'oracle', 'ibm', 'alicloud']

for csp in csps:
    with open(f'{csp}_functions_by_service_2025-11-08.json', 'r') as f:
        data = json.load(f)
    
    metadata = data['metadata']
    print(f"{metadata['cloud_provider']}: {metadata['total_functions']} functions")
```

### 3. Find all compliance controls for a GCP function

```python
import json

with open('gcp_functions_by_service_2025-11-08.json', 'r') as f:
    gcp_data = json.load(f)

# Find function in IAM service
function_name = 'gcp_iam_mfa_enabled'
if function_name in gcp_data['services']['iam']['functions']:
    func = gcp_data['services']['iam']['functions'][function_name]
    print(f"Compliance controls: {func['compliance_ids']}")
```

---

## Data Quality

✅ **No Invalid Entries**
- All "No checks defined" entries have been filtered out
- All functions properly categorized by service
- No NA or placeholder values

✅ **Proper Service Categorization**
- Services automatically extracted from function naming conventions
- 'unknown' category used only when service cannot be determined

✅ **Complete Metadata**
- Each file includes comprehensive metadata
- Service-level and function-level statistics
- Version and generation date tracking

---

## Cross-Reference

To look up details for any unique compliance ID mentioned in these files, refer to:
- `consolidated_compliance_rules_2025-11-08.csv` - Full compliance database

Each unique compliance ID in these JSON files maps back to a specific row in the consolidated CSV containing:
- Full compliance framework details
- Requirement descriptions
- All cloud provider checks
- References and source information

---

## Notes

- Functions are organized by the primary service they belong to
- Some functions may appear in 'unknown' service if the naming convention doesn't match expected patterns
- All JSON files use consistent structure for easy programmatic access
- Functions are deduplicated and normalized for consistency

---

**End of Summary**

