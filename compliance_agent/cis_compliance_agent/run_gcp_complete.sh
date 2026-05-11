#!/bin/bash
# Complete GCP processing - Steps 2, 3, 4, and merge
# Step 1 already completed: output_step1_20251031_225654

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

cd gcp_agent

# Activate virtual environment
if [ -d "../../ai_env" ]; then
    source ../../ai_env/bin/activate
    echo "✓ Activated virtual environment"
fi

TIMESTAMP="20251031_225654"
ORIGINAL_CSV="gcp_controls_FINAL_20251031_201244.csv"
INCOMPLETE_CSV="gcp_incomplete_${TIMESTAMP}.csv"
OUTPUT_STEP1="output_step1_${TIMESTAMP}"
OUTPUT_STEP2="output_step2_${TIMESTAMP}"
OUTPUT_STEP3="output_step3_${TIMESTAMP}"
OUTPUT_FINAL="output_final_${TIMESTAMP}"

echo "========================================"
echo "GCP Agent - Continuing from Step 2"
echo "========================================"
echo "Step 1 output: $OUTPUT_STEP1 (✓ Complete)"
echo ""

# Step 2: Review
echo "========================================"
echo "Step 2: Review (gpt-4o)"
echo "========================================"
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
echo "✓ GCP agent complete!"
echo "========================================"
echo "Updated: $ORIGINAL_CSV"
echo ""

# Verify results
echo "Verifying completion..."
python3 << 'PYEOF'
import csv

with open('gcp_controls_FINAL_20251031_201244.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    total = len(rows)
    complete = sum(1 for r in rows if r.get('final_approach') and r.get('program_name'))
    incomplete = total - complete
    pct = (complete/total)*100
    
    print(f"\n{'='*60}")
    print(f"GCP FINAL STATUS")
    print(f"{'='*60}")
    print(f"Total rows:      {total}")
    print(f"Complete:        {complete} ({pct:.1f}%)")
    print(f"Incomplete:      {incomplete}")
    print(f"{'='*60}\n")
PYEOF

