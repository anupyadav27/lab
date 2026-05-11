#!/bin/bash
###############################################################################
# Check progress of K8s function generation
###############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE=$(ls -t "$SCRIPT_DIR"/run_all_frameworks_*.log 2>/dev/null | head -1)

if [ -z "$LOG_FILE" ]; then
    echo "No log file found"
    exit 1
fi

echo "==================================================================="
echo "K8s Function Generation - Progress Check"
echo "==================================================================="
echo ""
echo "Log file: $LOG_FILE"
echo "Last updated: $(date -r "$LOG_FILE" '+%Y-%m-%d %H:%M:%S')"
echo ""

# Show current progress
echo "--- Last 20 lines of log ---"
tail -20 "$LOG_FILE"
echo ""

# Count completed frameworks
COMPLETED=$(grep -c "✅.*complete!" "$LOG_FILE" 2>/dev/null || echo "0")
FAILED=$(grep -c "❌.*failed" "$LOG_FILE" 2>/dev/null || echo "0")

echo "==================================================================="
echo "Status:"
echo "  Completed: $COMPLETED/12"
echo "  Failed: $FAILED"
echo "==================================================================="
echo ""

# Show output directories
echo "Output directories:"
ls -d "$SCRIPT_DIR"/output_*_202* 2>/dev/null | tail -5

echo ""
echo "To monitor live:"
echo "  tail -f $LOG_FILE"

