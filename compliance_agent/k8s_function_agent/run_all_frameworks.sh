#!/bin/bash
###############################################################################
# Run K8s Function Generation for ALL Non-CIS Compliance Frameworks
# Processes each framework sequentially with proper logging
###############################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPLIANCE_DIR="$(dirname "$SCRIPT_DIR")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$SCRIPT_DIR/run_all_frameworks_${TIMESTAMP}.log"

# Check OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable not set"
    exit 1
fi

# Frameworks to process
declare -a FRAMEWORKS=(
    "GDPR:gdpr/GDPR_controls_with_checks.csv"
    "RBI_BANK:rbi_bank/RBI_BANK_controls_with_checks.csv"
    "RBI_NBFC:rbi_nbfc/RBI_NBFC_controls_with_checks.csv"
    "CISA_CE:cisa_ce/CISA_CE_controls_with_checks.csv"
    "SOC2:soc2/SOC2_controls_with_checks.csv"
    "HIPAA:hipaa/HIPAA_controls_with_checks.csv"
    "ISO27001:iso27001-2022/ISO27001_2022_controls_with_checks.csv"
    "NIST_800_171:nist_800_171/NIST_800-171_R2_controls_with_checks.csv"
    "CANADA_PBMM:canada_pbmm/CANADA_PBMM_controls_with_checks.csv"
    "PCI_DSS:pci_compliance_agent/PCI_controls_with_checks.csv"
    "FedRAMP:FedRamp/FedRAMP_controls_with_checks.csv"
    "NIST_800_53:nist_complaince_agent/NIST_controls_with_checks.csv"
)

echo "==========================================================================" | tee -a "$LOG_FILE"
echo "K8s Function Generation - ALL FRAMEWORKS" | tee -a "$LOG_FILE"
echo "Start Time: $(date)" | tee -a "$LOG_FILE"
echo "Log File: $LOG_FILE" | tee -a "$LOG_FILE"
echo "==========================================================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Activate virtual environment
source "$COMPLIANCE_DIR/ai_env/bin/activate"

TOTAL=${#FRAMEWORKS[@]}
SUCCESS_COUNT=0
FAIL_COUNT=0

for i in "${!FRAMEWORKS[@]}"; do
    IFS=':' read -r FRAMEWORK_NAME CSV_PATH <<< "${FRAMEWORKS[$i]}"
    CURRENT=$((i + 1))
    FULL_CSV_PATH="$COMPLIANCE_DIR/$CSV_PATH"
    
    echo "========================================================================" | tee -a "$LOG_FILE"
    echo "[$CURRENT/$TOTAL] Processing: $FRAMEWORK_NAME" | tee -a "$LOG_FILE"
    echo "CSV: $CSV_PATH" | tee -a "$LOG_FILE"
    echo "Start: $(date)" | tee -a "$LOG_FILE"
    echo "------------------------------------------------------------------------" | tee -a "$LOG_FILE"
    
    # Check if CSV exists
    if [ ! -f "$FULL_CSV_PATH" ]; then
        echo "❌ ERROR: CSV file not found: $FULL_CSV_PATH" | tee -a "$LOG_FILE"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        continue
    fi
    
    # Create output directory
    OUTPUT_DIR="$SCRIPT_DIR/output_${FRAMEWORK_NAME}_${TIMESTAMP}"
    mkdir -p "$OUTPUT_DIR/step1" "$OUTPUT_DIR/step2" "$OUTPUT_DIR/step3"
    
    # Step 1: Generate
    echo "Step 1: Generating K8s functions..." | tee -a "$LOG_FILE"
    if python "$SCRIPT_DIR/agent_step1_generate_k8s.py" \
        --input "$FULL_CSV_PATH" \
        --output-dir "$OUTPUT_DIR/step1" \
        --framework "$FRAMEWORK_NAME" >> "$LOG_FILE" 2>&1; then
        echo "✓ Step 1 complete" | tee -a "$LOG_FILE"
    else
        echo "❌ Step 1 failed" | tee -a "$LOG_FILE"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        continue
    fi
    
    # Step 2: Review
    echo "Step 2: Reviewing K8s functions..." | tee -a "$LOG_FILE"
    if python "$SCRIPT_DIR/agent_step2_review_k8s.py" \
        --step1-dir "$OUTPUT_DIR/step1" \
        --output-dir "$OUTPUT_DIR/step2" \
        --framework "$FRAMEWORK_NAME" >> "$LOG_FILE" 2>&1; then
        echo "✓ Step 2 complete" | tee -a "$LOG_FILE"
    else
        echo "❌ Step 2 failed" | tee -a "$LOG_FILE"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        continue
    fi
    
    # Step 3: Update CSV
    echo "Step 3: Updating CSV..." | tee -a "$LOG_FILE"
    OUTPUT_CSV="$OUTPUT_DIR/step3/${FRAMEWORK_NAME}_controls_with_k8s.csv"
    SUMMARY_REPORT="$OUTPUT_DIR/step3/${FRAMEWORK_NAME}_K8S_SUMMARY.md"
    
    if python "$SCRIPT_DIR/agent_step3_update_csv.py" \
        --input-csv "$FULL_CSV_PATH" \
        --step2-dir "$OUTPUT_DIR/step2" \
        --output-csv "$OUTPUT_CSV" \
        --framework "$FRAMEWORK_NAME" \
        --summary-report "$SUMMARY_REPORT" >> "$LOG_FILE" 2>&1; then
        echo "✓ Step 3 complete" | tee -a "$LOG_FILE"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo "❌ Step 3 failed" | tee -a "$LOG_FILE"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        continue
    fi
    
    echo "✅ $FRAMEWORK_NAME complete!" | tee -a "$LOG_FILE"
    echo "   Output: $OUTPUT_CSV" | tee -a "$LOG_FILE"
    echo "   Summary: $SUMMARY_REPORT" | tee -a "$LOG_FILE"
    echo "   End: $(date)" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
done

echo "==========================================================================" | tee -a "$LOG_FILE"
echo "ALL FRAMEWORKS PROCESSING COMPLETE" | tee -a "$LOG_FILE"
echo "End Time: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Summary:" | tee -a "$LOG_FILE"
echo "  Total frameworks: $TOTAL" | tee -a "$LOG_FILE"
echo "  Successful: $SUCCESS_COUNT" | tee -a "$LOG_FILE"
echo "  Failed: $FAIL_COUNT" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Log file: $LOG_FILE" | tee -a "$LOG_FILE"
echo "==========================================================================" | tee -a "$LOG_FILE"

