#!/bin/bash
# Continue GCP processing from Step 3 (Steps 1 & 2 already complete)

set -e

# Start caffeinate
echo "Starting caffeinate..."
caffeinate -d -i -m -s -w $$ &
CAFFEINATE_PID=$!
echo "✓ Caffeinate running (PID: $CAFFEINATE_PID)"

cleanup() {
    echo "Stopping caffeinate..."
    kill $CAFFEINATE_PID 2>/dev/null || true
}
trap cleanup EXIT

# Activate virtual environment
source ../../ai_env/bin/activate
echo "✓ Virtual environment activated"

TIMESTAMP="20251031_225654"
ORIGINAL_CSV="gcp_controls_FINAL_20251031_201244.csv"
INCOMPLETE_CSV="gcp_incomplete_${TIMESTAMP}.csv"
OUTPUT_STEP2="output_step2_${TIMESTAMP}"
OUTPUT_STEP3="output_step3_${TIMESTAMP}"
OUTPUT_FINAL="output_final_${TIMESTAMP}"

echo ""
echo "========================================"
echo "GCP Agent - Continuing from Step 3"
echo "========================================"
echo "Step 1: ✓ Complete (164 rows)"
echo "Step 2: ✓ Complete (164 rows)"
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

# Step 5: Merge back
echo "========================================"
echo "Step 5: Merging results back"
echo "========================================"
STEP4_CSV=$(ls -t ${OUTPUT_FINAL}/*FINAL*.csv 2>/dev/null | head -1)
if [ -z "$STEP4_CSV" ]; then
    echo "Error: No FINAL CSV found"
    exit 1
fi

python3 ../process_incomplete.py \
    --action merge \
    --input-csv "$ORIGINAL_CSV" \
    --step4-csv "$STEP4_CSV"

echo ""
echo "✓ Merge complete"
rm -f "$INCOMPLETE_CSV"
echo ""

# Verify
echo "========================================"
echo "Verification"
echo "========================================"
python3 << 'PYEOF'
import csv
with open('gcp_controls_FINAL_20251031_201244.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    total = len(rows)
    complete = sum(1 for r in rows if r.get('final_approach') and r.get('program_name'))
    incomplete = total - complete
    pct = (complete/total)*100
    
    print(f"Total rows:      {total}")
    print(f"Complete:        {complete} ({pct:.1f}%)")
    print(f"Incomplete:      {incomplete}")
    if incomplete == 0:
        print("\n✅ GCP AGENT 100% COMPLETE!")
    else:
        print(f"\n⚠️  Still {incomplete} rows to process")
PYEOF

echo "========================================"

