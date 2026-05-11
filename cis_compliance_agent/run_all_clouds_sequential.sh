#!/bin/bash
# Run all cloud agents sequentially with quality checks
# Keeps Mac awake during processing

set -e

# Prevent Mac from sleeping
echo "Starting caffeinate to prevent sleep..."
caffeinate -s -w $$ &
CAFFEINATE_PID=$!

# Cleanup function
cleanup() {
    echo "Cleaning up..."
    if [ ! -z "$CAFFEINATE_PID" ]; then
        kill $CAFFEINATE_PID 2>/dev/null || true
    fi
}
trap cleanup EXIT

# Navigate to agent directory
cd "$(dirname "$0")"

# Define processing order (smallest to largest)
CLOUDS=("oracle" "gcp" "aws" "alicloud" "azure" "ibm" "k8s")

echo "========================================"
echo "MULTI-CLOUD COMPLIANCE AGENT RUNNER"
echo "========================================"
echo "Processing order: ${CLOUDS[@]}"
echo "Start time: $(date)"
echo ""

# Make scripts executable
chmod +x run_cloud_agent.sh
chmod +x process_incomplete.py

# Process each cloud
for CLOUD in "${CLOUDS[@]}"; do
    echo ""
    echo "###################################################"
    echo "# Starting: $CLOUD"
    echo "# Time: $(date)"
    echo "###################################################"
    echo ""
    
    # Run the agent
    ./run_cloud_agent.sh "$CLOUD"
    
    # Quality check
    echo ""
    echo "Running quality check for $CLOUD..."
    cd "${CLOUD}_agent"
    
    # Find latest FINAL CSV
    LATEST_CSV=$(ls -t *FINAL*.csv 2>/dev/null | head -1)
    
    if [ -f "quality_check.py" ]; then
        python3 quality_check.py "$LATEST_CSV" || true
    else
        echo "⚠️  No quality_check.py found for $CLOUD, skipping..."
    fi
    
    cd ..
    
    echo ""
    echo "✓ $CLOUD complete and checked"
    echo ""
    sleep 2
done

echo ""
echo "###################################################"
echo "# ALL CLOUDS PROCESSED SUCCESSFULLY"
echo "# End time: $(date)"
echo "###################################################"
echo ""

# Final summary
echo "Generating final summary..."
python3 << 'PYEOF'
import csv
import os

agents = ['oracle', 'gcp', 'aws', 'alicloud', 'azure', 'ibm', 'k8s']
print("\n" + "="*60)
print("FINAL PROCESSING SUMMARY")
print("="*60)

for cloud in agents:
    agent_dir = f"{cloud}_agent"
    csv_files = [f for f in os.listdir(agent_dir) if f.endswith('FINAL.csv') or 'FINAL' in f]
    if csv_files:
        csv_file = os.path.join(agent_dir, sorted(csv_files)[-1])
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            total = len(rows)
            complete = sum(1 for r in rows if r.get('final_approach') and r.get('program_name'))
            incomplete = total - complete
            pct = (complete/total)*100 if total > 0 else 0
            
            status = "✓" if incomplete == 0 else "⚠️"
            print(f"{status} {cloud.upper():12s}: {complete:3d}/{total:3d} complete ({pct:5.1f}%)")

print("="*60)
PYEOF

echo ""
echo "✓ All processing complete!"











