#!/bin/bash
###############################################################################
# Run K8s Function Generation for a Single Compliance Framework
# Usage: ./run_framework.sh <framework_name> <csv_path>
# Example: ./run_framework.sh GDPR gdpr/GDPR_controls_with_checks.csv
###############################################################################

set -e

# Check arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <framework_name> <csv_path_relative_to_compliance_agent>"
    echo "Example: $0 GDPR gdpr/GDPR_controls_with_checks.csv"
    exit 1
fi

FRAMEWORK_NAME="$1"
CSV_PATH="$2"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Set paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPLIANCE_DIR="$(dirname "$SCRIPT_DIR")"
FULL_CSV_PATH="$COMPLIANCE_DIR/$CSV_PATH"

# Create output directories
OUTPUT_BASE="$SCRIPT_DIR/output_${FRAMEWORK_NAME}_${TIMESTAMP}"
STEP1_DIR="$OUTPUT_BASE/step1_generate"
STEP2_DIR="$OUTPUT_BASE/step2_review"
STEP3_DIR="$OUTPUT_BASE/step3_final"

mkdir -p "$STEP1_DIR" "$STEP2_DIR" "$STEP3_DIR"

echo "=========================================================================="
echo "K8s Function Generation Pipeline"
echo "Framework: $FRAMEWORK_NAME"
echo "Input CSV: $FULL_CSV_PATH"
echo "Output: $OUTPUT_BASE"
echo "=========================================================================="
echo ""

# Check if CSV exists
if [ ! -f "$FULL_CSV_PATH" ]; then
    echo "❌ Error: CSV file not found: $FULL_CSV_PATH"
    exit 1
fi

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable not set"
    exit 1
fi

# Activate virtual environment
source "$COMPLIANCE_DIR/ai_env/bin/activate"

echo "Step 1: Generating K8s functions..."
echo "--------------------------------------------------------------------"
python "$SCRIPT_DIR/agent_step1_generate_k8s.py" \
    --input "$FULL_CSV_PATH" \
    --output-dir "$STEP1_DIR" \
    --framework "$FRAMEWORK_NAME"

if [ $? -ne 0 ]; then
    echo "❌ Step 1 failed"
    exit 1
fi

echo ""
echo "Step 2: Reviewing K8s functions..."
echo "--------------------------------------------------------------------"
python "$SCRIPT_DIR/agent_step2_review_k8s.py" \
    --step1-dir "$STEP1_DIR" \
    --output-dir "$STEP2_DIR" \
    --framework "$FRAMEWORK_NAME"

if [ $? -ne 0 ]; then
    echo "❌ Step 2 failed"
    exit 1
fi

echo ""
echo "Step 3: Updating CSV..."
echo "--------------------------------------------------------------------"
OUTPUT_CSV="$STEP3_DIR/${FRAMEWORK_NAME}_controls_with_k8s.csv"
SUMMARY_REPORT="$STEP3_DIR/${FRAMEWORK_NAME}_K8S_SUMMARY.md"

python "$SCRIPT_DIR/agent_step3_update_csv.py" \
    --input-csv "$FULL_CSV_PATH" \
    --step2-dir "$STEP2_DIR" \
    --output-csv "$OUTPUT_CSV" \
    --framework "$FRAMEWORK_NAME" \
    --summary-report "$SUMMARY_REPORT"

if [ $? -ne 0 ]; then
    echo "❌ Step 3 failed"
    exit 1
fi

echo ""
echo "=========================================================================="
echo "✅ Complete! K8s functions generated for $FRAMEWORK_NAME"
echo ""
echo "Results:"
echo "  - Step 1 JSON: $STEP1_DIR"
echo "  - Step 2 JSON: $STEP2_DIR"
echo "  - Updated CSV: $OUTPUT_CSV"
echo "  - Summary: $SUMMARY_REPORT"
echo "=========================================================================="

