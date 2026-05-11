#!/bin/bash
# Run compliance agent for a specific cloud on incomplete rows only
# Usage: ./run_cloud_agent.sh <cloud_name>
# Example: ./run_cloud_agent.sh oracle

set -e

# Start caffeinate to prevent Mac from sleeping
echo "Starting caffeinate to keep Mac awake..."
caffeinate -d -i -m -s -w $$ &
CAFFEINATE_PID=$!
echo "✓ Caffeinate started (PID: $CAFFEINATE_PID)"

# Cleanup function
cleanup() {
    echo ""
    echo "Cleaning up caffeinate..."
    if [ ! -z "$CAFFEINATE_PID" ]; then
        kill $CAFFEINATE_PID 2>/dev/null || true
        echo "✓ Caffeinate stopped"
    fi
}
trap cleanup EXIT

CLOUD=$1
if [ -z "$CLOUD" ]; then
    echo "Usage: $0 <cloud_name>"
    echo "Available: oracle, gcp, aws, alicloud, azure, ibm, k8s"
    exit 1
fi

AGENT_DIR="${CLOUD}_agent"
if [ ! -d "$AGENT_DIR" ]; then
    echo "Error: Agent directory $AGENT_DIR not found"
    exit 1
fi

cd "$AGENT_DIR"

# Activate virtual environment if available
if [ -d "../../ai_env" ]; then
    source ../../ai_env/bin/activate
    echo "✓ Activated virtual environment"
fi

# Find the latest FINAL CSV
ORIGINAL_CSV=$(ls -t *FINAL*.csv 2>/dev/null | head -1)
if [ -z "$ORIGINAL_CSV" ]; then
    echo "Error: No FINAL CSV found in $AGENT_DIR"
    exit 1
fi

echo "========================================"
echo "Processing $CLOUD compliance agent"
echo "========================================"
echo "Original CSV: $ORIGINAL_CSV"
echo ""

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Step 0: Filter incomplete rows
echo "Step 0: Filtering incomplete rows..."
INCOMPLETE_CSV="${CLOUD}_incomplete_${TIMESTAMP}.csv"
python3 ../process_incomplete.py \
    --action filter \
    --input-csv "$ORIGINAL_CSV" \
    --output-csv "$INCOMPLETE_CSV"

# Count incomplete rows
INCOMPLETE_COUNT=$(awk 'END {print NR-1}' "$INCOMPLETE_CSV")
echo ""
echo "Found $INCOMPLETE_COUNT incomplete rows to process"
echo ""

if [ "$INCOMPLETE_COUNT" -eq 0 ]; then
    echo "✓ No incomplete rows. All done!"
    exit 0
fi

# Step 1: Initial assessment
echo "========================================"
echo "Step 1: Initial Assessment (gpt-4o-mini)"
echo "========================================"
OUTPUT_STEP1="output_step1_${TIMESTAMP}"
python3 agent_step1_initial.py \
    --csv "$INCOMPLETE_CSV" \
    --output-dir "$OUTPUT_STEP1" \
    --model "gpt-4o-mini"

echo ""
echo "✓ Step 1 complete"
echo ""

# Step 2: Review
echo "========================================"
echo "Step 2: Review (gpt-4o)"
echo "========================================"
OUTPUT_STEP2="output_step2_${TIMESTAMP}"
python3 agent_step2_review.py \
    --input-dir "$OUTPUT_STEP1" \
    --output-dir "$OUTPUT_STEP2" \
    --review-model "gpt-4o"

echo ""
echo "✓ Step 2 complete"
echo ""

# Step 3: Final decision
echo "========================================"
echo "Step 3: Final Decision (gpt-4o)"
echo "========================================"
OUTPUT_STEP3="output_step3_${TIMESTAMP}"
python3 agent_step3_final.py \
    --input-dir "$OUTPUT_STEP2" \
    --output-dir "$OUTPUT_STEP3" \
    --decision-model "gpt-4o"

echo ""
echo "✓ Step 3 complete"
echo ""

# Step 4: Generate CSV
echo "========================================"
echo "Step 4: Generate Final CSV"
echo "========================================"
OUTPUT_FINAL="output_final_${TIMESTAMP}"
mkdir -p "$OUTPUT_FINAL"
python3 agent_step4_csv.py \
    --input-dir "$OUTPUT_STEP3" \
    --original-csv "$INCOMPLETE_CSV" \
    --output-dir "$OUTPUT_FINAL"

echo ""
echo "✓ Step 4 complete"
echo ""

# Step 5: Merge back into original CSV
echo "========================================"
echo "Step 5: Merging results back"
echo "========================================"
STEP4_CSV=$(ls -t ${OUTPUT_FINAL}/*FINAL*.csv 2>/dev/null | head -1)
if [ -z "$STEP4_CSV" ]; then
    echo "Error: No FINAL CSV found in $OUTPUT_FINAL"
    exit 1
fi

python3 ../process_incomplete.py \
    --action merge \
    --input-csv "$ORIGINAL_CSV" \
    --step4-csv "$STEP4_CSV"

echo ""
echo "✓ Merge complete"
echo ""

# Cleanup incomplete CSV
rm -f "$INCOMPLETE_CSV"

echo "========================================"
echo "✓ $CLOUD agent complete!"
echo "========================================"
echo "Updated: $ORIGINAL_CSV"
echo ""

