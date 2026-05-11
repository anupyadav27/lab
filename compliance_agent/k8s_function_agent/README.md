# K8s Function Generator for Non-CIS Compliance Frameworks

This tool generates Kubernetes-equivalent security check functions for non-CIS compliance frameworks using a two-AI verification approach.

## Overview

For compliance frameworks like NIST 800-171, HIPAA, GDPR, PCI, SOC2, etc., this tool:
1. Analyzes existing CSP (AWS/Azure/GCP/Oracle/IBM/Alicloud) security checks
2. Generates equivalent K8s security function names
3. Reviews and validates the mappings with a second AI
4. Updates the compliance CSV with a new `K8s_Checks` column

## Architecture

### Three-Step Process

**Step 1: Generate K8s Functions** (`agent_step1_generate_k8s.py`)
- First AI analyzes compliance controls and CSP checks
- Generates K8s-equivalent function names
- Maps cloud security concepts to K8s security domains
- Output: JSON files with proposed K8s functions

**Step 2: Review & Validate** (`agent_step2_review_k8s.py`)
- Second AI critically reviews Step 1 results
- Validates technical accuracy and naming conventions
- Approves, suggests changes, or rejects functions
- Output: JSON files with validated functions

**Step 3: Update CSV** (`agent_step3_update_csv.py`)
- Consolidates Step 2 results
- Adds `K8s_Checks` column to compliance CSV
- Updates `Total_Checks` count
- Generates summary report

## K8s Security Mapping

### Cloud → Kubernetes Equivalents

| Cloud Concept | K8s Equivalent | Function Pattern |
|--------------|----------------|------------------|
| IAM Roles/Policies | RBAC (Roles, RoleBindings) | `k8s_rbac_*` |
| Security Groups | NetworkPolicies | `k8s_networkpolicy_*` |
| KMS/Secrets | Secrets, etcd encryption | `k8s_secret_*`, `k8s_etcd_*` |
| CloudTrail/Audit | K8s Audit Logs | `k8s_audit_*` |
| VM Security | PodSecurityPolicy/Standards | `k8s_pod_*` |
| API Gateway | API Server Config | `k8s_apiserver_*` |
| Container Registry | Image Admission | `k8s_image_*` |
| Config Management | Admission Controllers | `k8s_admission_*` |

### Function Naming Convention

Pattern: `k8s_<resource>_<check_description>`

Examples:
- `k8s_rbac_no_cluster_admin_binding`
- `k8s_networkpolicy_default_deny_ingress`
- `k8s_pod_security_context_non_root`
- `k8s_secret_encryption_at_rest_enabled`
- `k8s_audit_logging_enabled`
- `k8s_image_scan_on_admission`

## Usage

### Process a Single Framework

```bash
cd /Users/apple/Desktop/compliance_Database/compliance_agent/k8s_function_agent

# Make script executable
chmod +x run_framework.sh

# Run for a specific framework
./run_framework.sh FRAMEWORK_NAME path/to/csv

# Examples:
./run_framework.sh GDPR ../gdpr/GDPR_controls_with_checks.csv
./run_framework.sh NIST_800_171 ../nist_800_171/NIST_800-171_R2_controls_with_checks.csv
./run_framework.sh HIPAA ../hipaa/HIPAA_controls_with_checks.csv
```

### Environment Setup

```bash
# Ensure OpenAI API key is set
export OPENAI_API_KEY="your-api-key-here"

# Activate virtual environment (done automatically by script)
source ../ai_env/bin/activate
```

### Output Structure

```
output_FRAMEWORK_TIMESTAMP/
├── step1_generate/           # Step 1 JSON results
│   ├── control_1.json
│   ├── control_2.json
│   └── ...
├── step2_review/            # Step 2 review results
│   ├── control_1.json
│   ├── control_2.json
│   └── ...
└── step3_final/             # Final outputs
    ├── FRAMEWORK_controls_with_k8s.csv    # Updated CSV
    └── FRAMEWORK_K8S_SUMMARY.md           # Summary report
```

## Supported Frameworks

| Framework | CSV Path |
|-----------|----------|
| NIST 800-171 | `nist_800_171/NIST_800-171_R2_controls_with_checks.csv` |
| HIPAA | `hipaa/HIPAA_controls_with_checks.csv` |
| GDPR | `gdpr/GDPR_controls_with_checks.csv` |
| PCI DSS | `pci_compliance_agent/PCI_controls_with_checks.csv` |
| SOC2 | `soc2/SOC2_controls_with_checks.csv` |
| ISO27001-2022 | `iso27001-2022/ISO27001_2022_controls_with_checks.csv` |
| FedRAMP | `FedRamp/FedRAMP_controls_with_checks.csv` |
| NIST 800-53 | `nist_complaince_agent/NIST_controls_with_checks.csv` |
| RBI Bank | `rbi_bank/RBI_BANK_controls_with_checks.csv` |
| RBI NBFC | `rbi_nbfc/RBI_NBFC_controls_with_checks.csv` |
| CISA CE | `cisa_ce/CISA_CE_controls_with_checks.csv` |
| Canada PBMM | `canada_pbmm/CANADA_PBMM_controls_with_checks.csv` |

## Processing All Frameworks

To process all frameworks sequentially:

```bash
# Process GDPR (smallest, good for testing)
./run_framework.sh GDPR ../gdpr/GDPR_controls_with_checks.csv

# Process NIST 800-171
./run_framework.sh NIST_800_171 ../nist_800_171/NIST_800-171_R2_controls_with_checks.csv

# Process HIPAA
./run_framework.sh HIPAA ../hipaa/HIPAA_controls_with_checks.csv

# ... continue with others
```

## Quality Assurance

The two-AI approach ensures:

1. **First AI (Generator)**
   - Analyzes context deeply
   - Maps CSP concepts to K8s
   - Proposes function names

2. **Second AI (Reviewer)**
   - Validates technical accuracy
   - Checks naming consistency
   - Catches errors and suggests improvements

3. **Review Statuses**
   - `APPROVE`: Functions validated as-is
   - `APPROVE_WITH_CHANGES`: Improvements made
   - `REJECT`: Needs major revision
   - `NOT_APPLICABLE`: Control doesn't apply to K8s

## Example Workflow

### Running GDPR (Quick Test)

```bash
# GDPR has only 3 controls - perfect for testing
./run_framework.sh GDPR ../gdpr/GDPR_controls_with_checks.csv

# Check results
cat output_GDPR_*/step3_final/GDPR_K8S_SUMMARY.md
head output_GDPR_*/step3_final/GDPR_controls_with_k8s.csv
```

### Running NIST 800-171 (Full Framework)

```bash
# NIST 800-171 has ~50 controls
./run_framework.sh NIST_800_171 ../nist_800_171/NIST_800-171_R2_controls_with_checks.csv

# Monitor progress (in another terminal)
tail -f output_NIST_800_171_*/step1_generate/*.json
```

## Troubleshooting

### API Key Issues
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Set if missing
export OPENAI_API_KEY="sk-..."
```

### Network Issues
- The script includes retry logic with exponential backoff
- Rate limiting: 0.5s delay between API calls
- Max 4 retries per API call

### Resume from Failure
If a step fails:
```bash
# Step 1 failed - rerun from beginning
./run_framework.sh FRAMEWORK_NAME path/to/csv

# Step 2 failed - run Step 2 manually
python agent_step2_review_k8s.py \
    --step1-dir output_FRAMEWORK_*/step1_generate \
    --output-dir output_FRAMEWORK_*/step2_review \
    --framework FRAMEWORK_NAME

# Step 3 failed - run Step 3 manually
python agent_step3_update_csv.py \
    --input-csv path/to/original.csv \
    --step2-dir output_FRAMEWORK_*/step2_review \
    --output-csv output.csv \
    --framework FRAMEWORK_NAME \
    --summary-report summary.md
```

## Output Validation

After processing, verify:

1. **CSV has K8s_Checks column**
   ```bash
   head -1 output_*/step3_final/*_with_k8s.csv | grep K8s_Checks
   ```

2. **K8s functions follow naming convention**
   ```bash
   grep "^k8s_" output_*/step3_final/*_with_k8s.csv
   ```

3. **Summary report looks reasonable**
   ```bash
   cat output_*/step3_final/*_SUMMARY.md
   ```

## Next Steps

After generating K8s functions for all frameworks:

1. Review generated functions for accuracy
2. Merge approved CSV files back to main framework directories
3. Update audit results JSON files with K8s check information
4. Implement actual K8s check functions in the compliance engine

## Notes

- **One framework at a time**: Process sequentially for better context and clearer logs
- **Review outputs**: Each framework's results should be reviewed before moving to the next
- **Customize as needed**: Function names can be manually adjusted in Step 3 CSV if needed
- **Not all controls apply**: Many cloud-specific controls won't have K8s equivalents (e.g., cloud billing)

## Contact

For questions or issues with the K8s function generation process, refer to the main compliance database documentation.

