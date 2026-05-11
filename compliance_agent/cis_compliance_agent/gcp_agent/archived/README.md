# GCP Compliance Agent

Three-AI pipeline for GCP CIS compliance audit automation.

## Pipeline

```
CSV Input → Step 1 (gpt-4o-mini) → Step 2 (GPT-4o) → Step 3 (GPT-4o) → Step 4 (CSV) → Quality Check
```

## Files

1. **agent_step1_initial.py** - Initial assessment (Manual vs Automated)
2. **agent_step2_review.py** - GPT-4o review and validation
3. **agent_step3_final.py** - Final authoritative decision
4. **agent_step4_csv.py** - Generate final CSV with all decisions
5. **quality_check.py** - Validate quality of all decisions
6. **run_full_pipeline.sh** - Run all steps automatically

## Usage

### Run full pipeline:
```bash
./run_full_pipeline.sh
```

### Or run steps individually:
```bash
# Step 1: Initial Assessment
python agent_step1_initial.py --csv gcp_controls.csv

# Step 2: Review
python agent_step2_review.py --input-dir output_step1_YYYYMMDD_HHMMSS

# Step 3: Final Decision
python agent_step3_final.py --input-dir output_step2_YYYYMMDD_HHMMSS

# Step 4: CSV Generation
python agent_step4_csv.py --input-dir output_step3_YYYYMMDD_HHMMSS --original-csv gcp_controls.csv

# Quality Check
python quality_check.py --input-dir output_step3_YYYYMMDD_HHMMSS
```

## Program Naming Convention

Format: `gcp_<service>_<resource>_<security_intent>`

Examples:
- `gcp_storage_bucket_encryption_enabled`
- `gcp_compute_instance_public_ip_restricted`
- `gcp_iam_password_policy_compliant`

## Quality Targets

- ✅ 100% coverage
- ✅ >80% automation rate
- ✅ >90% HIGH confidence
- ✅ 0 errors
- ✅ All program names valid
