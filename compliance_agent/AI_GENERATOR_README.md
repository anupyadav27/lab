# AI-Powered GCP & Azure Function Generator

## 🎯 Purpose

Intelligently generates GCP and Azure compliance function equivalents for NIST 800-171, GDPR, and HIPAA frameworks using OpenAI GPT-4.

## ✨ Key Features

- **AI-Powered Mapping**: Uses GPT-4 for intelligent, context-aware function generation (NOT simple string replacement)
- **Manual Requirement Handling**: Automatically skips manual requirements and validates data consistency
- **Service Mapping Guide**: Includes comprehensive AWS → GCP → Azure service equivalents
- **Data Validation**: Detects inconsistencies (e.g., manual requirements with automated functions)
- **Semantic Equivalence**: Generates functions that match compliance intent, not just naming patterns

## 📋 Prerequisites

```bash
# 1. Python 3.8+
python3 --version

# 2. OpenAI Python library
pip3 install openai

# 3. OpenAI API Key
export OPENAI_API_KEY='your-api-key-here'
```

## 🚀 Usage

```bash
# Navigate to compliance_agent directory
cd /Users/apple/Desktop/compliance_Database/compliance_agent

# Run the generator
python3 ai_function_generator.py
```

## 📂 Input Files

| Framework | CSV | JSON |
|-----------|-----|------|
| NIST 800-171 | `nist_800_171/NIST_800-171_R2_controls_with_checks.csv` | `nist_800_171/NIST_800-171_R2_audit_results.json` |
| GDPR | `gdpr/GDPR_controls_with_checks.csv` | `gdpr/GDPR_audit_results.json` |
| HIPAA | `hipaa/HIPAA_controls_with_checks.csv` | `hipaa/HIPAA_audit_results.json` |

## 📂 Output Files

Enhanced versions with GCP and Azure functions:

- `nist_800_171/NIST_800-171_R2_controls_with_checks_ENHANCED.csv`
- `gdpr/GDPR_controls_with_checks_ENHANCED.csv`
- `hipaa/HIPAA_controls_with_checks_ENHANCED.csv`

## 🎨 How It Works

### For Automated Requirements:

1. **Read** AWS/IBM/Alicloud/Oracle functions for each requirement
2. **Extract Context** from requirement title and description
3. **Send to AI** with service mapping guide and context
4. **Generate** GCP and Azure equivalent functions
5. **Validate** function naming follows `<csp>_<service>_<check>` convention
6. **Update** CSV with new functions in `GCP_Checks` and `Azure_Checks` columns

### For Manual Requirements:

1. **Detect** automation_type = "manual"
2. **Skip** AI generation entirely
3. **Validate** that AWS also has no functions (data consistency check)
4. **Ensure** GCP_Checks and Azure_Checks remain empty
5. **Report** any inconsistencies found

## 📊 Example Output

```
================================================================================
Processing: NIST 800-171
================================================================================

[1/50] Processing: 3_13_16
  ✅ Generated 11 GCP + 11 Azure functions
  📝 Note: GCP uses Cloud KMS, Azure uses Key Vault for encryption

[2/50] Processing: 3_13_4
  📋 MANUAL requirement - no automated checks should exist
  ✅ Data consistent - no functions found

[3/50] Processing: 3_13_1
  ⚠️  WARNING: Manual requirement has AWS functions - DATA INCONSISTENCY!
      AWS functions found: aws_cloudtrail_enabled, aws_guardduty_enabled...
  ✅ Generated 20 GCP + 20 Azure functions

...

================================================================================
📊 ENHANCEMENT SUMMARY
================================================================================
Total Requirements:       85
  └─ Manual:              1 (no functions generated)
  └─ Automated:           84
     └─ Enhanced:         84 (GCP/Azure added)

⚠️  Data Inconsistencies:   1
    Manual requirements with AWS functions - needs review!

================================================================================
✅ ENHANCEMENT COMPLETE!
================================================================================
```

## 🗺️ Service Mapping Guide

The AI uses this comprehensive mapping guide:

| AWS Service | GCP Service | Azure Service |
|-------------|-------------|---------------|
| CloudTrail | Cloud Logging | Azure Monitor |
| CloudWatch | Cloud Monitoring | Azure Monitor |
| S3 | Cloud Storage | Azure Storage |
| IAM | IAM | Microsoft Entra / IAM |
| EC2 | Compute Engine | Virtual Machines |
| RDS | Cloud SQL | Azure SQL Database |
| KMS | Cloud KMS | Key Vault |
| VPC | VPC | Virtual Network |
| ELB/ELBv2 | Cloud Load Balancing | Load Balancer |
| Lambda | Cloud Functions | Azure Functions |
| GuardDuty | Security Command Center | Microsoft Defender |
| SecurityHub | Security Command Center | Microsoft Defender |
| ... | ... | ... |

Full list included in the script.

## ⚠️ Important Rules

### Manual Requirements:
- ❌ NO functions should be generated
- ❌ AWS should NOT have functions either
- ✅ Script will detect and report inconsistencies

### Automated Requirements:
- ✅ Generate GCP and Azure equivalents
- ✅ Maintain semantic equivalence (not just naming)
- ✅ Follow `<csp>_<service>_<check>` naming convention

## 🔍 Data Validation

The script performs these validations:

1. **Manual Requirement Check**: Ensures no functions exist for manual requirements
2. **AWS Consistency Check**: Flags manual requirements that have AWS functions
3. **Function Format**: Validates generated functions follow naming conventions
4. **Context Awareness**: Uses requirement context to generate appropriate checks

## 📝 Example Function Generation

**Input:**
```
Requirement: "Protect the confidentiality of CUI at rest"
Automation: automated
AWS Functions:
  - aws_cloudtrail_kms_encryption_enabled
  - aws_s3_bucket_default_encryption
  - aws_rds_instance_storage_encrypted
```

**AI Output:**
```json
{
  "gcp_functions": [
    "gcp_logging_kms_encryption_enabled",
    "gcp_storage_bucket_default_encryption",
    "gcp_sql_instance_disk_encryption_enabled"
  ],
  "azure_functions": [
    "azure_monitor_kms_encryption_enabled",
    "azure_storage_account_encryption_enabled",
    "azure_sql_server_tde_enabled"
  ],
  "notes": "Azure uses TDE (Transparent Data Encryption) for SQL encryption"
}
```

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY environment variable not set"
```bash
export OPENAI_API_KEY='your-key-here'
```

### Error: "No module named 'openai'"
```bash
pip3 install openai
```

### Warning: "Manual requirement has AWS functions"
This indicates a data inconsistency. Review the requirement and either:
1. Change automation_type to "automated" if checks exist
2. Remove AWS functions if truly manual

## 📈 Next Steps

After generation:

1. **Review** enhanced CSV files
2. **Validate** function names match your naming conventions
3. **Update** `consolidated_compliance_rules_FINAL.csv` with new GCP/Azure functions
4. **Test** generated functions against actual cloud environments

## 🔗 Related Files

- `GCP_AZURE_ENHANCEMENT_PLAN.md` - Detailed enhancement plan
- `comprehensive_service_mapping.json` - Service mapping reference

## 📞 Support

For issues or questions:
1. Check the enhancement plan
2. Review service mapping JSON
3. Validate input CSV format
4. Check OpenAI API quota

---

**Last Updated:** 2025-11-11
**Version:** 1.0

