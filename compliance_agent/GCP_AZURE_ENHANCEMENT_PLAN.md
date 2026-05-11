# GCP & AZURE FUNCTION ENHANCEMENT PLAN
## For NIST 800-171, GDPR, and HIPAA

Generated: $(date)

---

## 📊 CURRENT STATE

### Files to Enhance:

#### 1. NIST 800-171 (50 requirements)
- \`nist_800_171/NIST_800-171_R2_controls_with_checks.csv\`
- \`nist_800_171/NIST_800-171_R2_audit_results.json\`
- **Status:** GCP_Checks and Azure_Checks columns EMPTY

#### 2. GDPR (3 requirements) 
- \`gdpr/GDPR_controls_with_checks.csv\`
- \`gdpr/GDPR_audit_results.json\`
- **Status:** GCP_Checks and Azure_Checks columns EMPTY

#### 3. HIPAA (32 requirements)
- \`hipaa/HIPAA_controls_with_checks.csv\`
- \`hipaa/HIPAA_audit_results.json\`
- **Status:** GCP_Checks and Azure_Checks columns EMPTY

**Total:** 85 requirements across 3 frameworks need GCP & Azure functions

---

## 🎯 ENHANCEMENT STRATEGY

### Step 1: Service Mapping (AWS → GCP/Azure)
Create translation rules for cloud service equivalents:

\`\`\`
AWS Service          → GCP Service            → Azure Service
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cloudtrail          → logging                → monitor
cloudwatch          → monitoring             → monitor
s3                  → storage                → storage
iam                 → iam                    → entra (or iam)
ec2                 → compute                → vm (or compute)
rds                 → sql                    → sql
kms                 → kms                    → keyvault
guardduty           → securitycommandcenter  → defender
securityhub         → securitycommandcenter  → defender
\`\`\`

### Step 2: Function Name Translation
Pattern-based function name generation:

**AWS Format:** \`aws_service_check_name\`
**GCP Format:** \`gcp_service_check_name\`  
**Azure Format:** \`azure_service_check_name\`

**Example:**
- AWS: \`aws_cloudtrail_kms_encryption_enabled\`
- GCP: \`gcp_logging_kms_encryption_enabled\`
- Azure: \`azure_monitor_kms_encryption_enabled\`

### Step 3: Batch Generation
Generate functions in batches by framework:

1. **NIST 800-171:** 50 requirements
2. **GDPR:** 3 requirements  
3. **HIPAA:** 32 requirements

For each requirement:
- Analyze AWS/IBM/Alicloud functions
- Identify service patterns
- Generate GCP equivalent
- Generate Azure equivalent
- Validate function names follow naming convention

### Step 4: File Updates

#### CSV Updates:
- Add functions to \`GCP_Checks\` column (semicolon-separated)
- Add functions to \`Azure_Checks\` column (semicolon-separated)
- Update \`Total_Checks\` count
- Preserve all existing data

#### JSON Updates:
- Add \`gcp\` section under \`cloud_implementations\`
- Add \`azure\` section under \`cloud_implementations\`
- Include detailed check metadata (service, check_name, severity, etc.)
- Preserve all existing structure

### Step 5: Compliance CSV Integration
Update \`consolidated_compliance_rules_FINAL.csv\` with new functions:
- Populate \`gcp_uniform_format\` column
- Populate \`azure_uniform_format\` column
- For NIST 800-171, GDPR, and HIPAA requirements only

---

## 📋 IMPLEMENTATION STEPS

### Phase 1: Service Mapping Generation (10 min)
\`\`\`python
# Create comprehensive service mapping dictionary
service_mapping = {
    'aws_to_gcp': {...},
    'aws_to_azure': {...}
}
\`\`\`

### Phase 2: Function Generation (30 min)
\`\`\`python
# For each framework (NIST, GDPR, HIPAA):
#   1. Read existing CSV
#   2. For each row with AWS_Checks:
#      - Parse AWS functions
#      - Generate GCP equivalents
#      - Generate Azure equivalents
#   3. Add to GCP_Checks and Azure_Checks columns
#   4. Update JSON file with detailed metadata
\`\`\`

### Phase 3: Validation (10 min)
- Verify function name conventions
- Check semicolon separation
- Validate Total_Checks count
- Ensure JSON structure integrity

### Phase 4: Backup & Save (5 min)
- Create backups of original files
- Save enhanced CSV and JSON files
- Generate summary report

### Phase 5: Compliance CSV Update (15 min)
- Map enhanced functions to compliance CSV
- Update gcp_uniform_format column
- Update azure_uniform_format column
- Verify data integrity

---

## 🎨 FUNCTION NAMING CONVENTIONS

### GCP Service Name Mapping:
\`\`\`
AWS              → GCP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cloudtrail       → logging
cloudwatch       → monitoring  
s3               → storage
iam              → iam
ec2              → compute
rds              → sql
kms              → kms
vpc              → vpc
elb/elbv2        → loadbalancing
lambda           → functions
guardduty        → securitycommandcenter
securityhub      → securitycommandcenter
config           → config
\`\`\`

### Azure Service Name Mapping:
\`\`\`
AWS              → Azure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cloudtrail       → monitor
cloudwatch       → monitor
s3               → storage
iam              → entra (or iam)
ec2              → vm (or compute)
rds              → sql
kms              → keyvault
vpc              → network
elb/elbv2        → loadbalancer
lambda           → function
guardduty        → defender
securityhub      → defender
config           → config
\`\`\`

---

## 📊 EXPECTED OUTPUT

### Before:
\`\`\`csv
Requirement_ID,AWS_Checks,Azure_Checks,GCP_Checks,Total_Checks
3_13_16,aws_cloudtrail_kms_encryption_enabled; aws_s3_bucket_default_encryption,,,11
\`\`\`

### After:
\`\`\`csv
Requirement_ID,AWS_Checks,Azure_Checks,GCP_Checks,Total_Checks
3_13_16,aws_cloudtrail_kms_encryption_enabled; aws_s3_bucket_default_encryption,azure_monitor_kms_encryption_enabled; azure_storage_bucket_default_encryption,gcp_logging_kms_encryption_enabled; gcp_storage_bucket_default_encryption,33
\`\`\`

---

## ✅ SUCCESS CRITERIA

1. **Coverage:** All 85 requirements have GCP and Azure functions
2. **Naming:** Functions follow \`<csp>_<service>_<check>\` convention
3. **Consistency:** Same checks exist across AWS/GCP/Azure where applicable
4. **Files Updated:** 6 files enhanced (3 CSV + 3 JSON)
5. **Compliance CSV:** Updated with new GCP/Azure functions
6. **No Data Loss:** All existing data preserved

---

## 🚀 READY TO PROCEED?

This plan will:
- ✅ Add GCP functions for 85 requirements
- ✅ Add Azure functions for 85 requirements
- ✅ Update 3 CSV files (NIST, GDPR, HIPAA)
- ✅ Update 3 JSON files (NIST, GDPR, HIPAA)
- ✅ Update consolidated compliance CSV
- ✅ Generate detailed enhancement report

**Estimated Time:** 70 minutes
**Total Functions to Generate:** ~1,700+ (85 requirements × ~10 functions each × 2 CSPs)

