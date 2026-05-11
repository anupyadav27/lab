#!/bin/bash
###############################################################################
# Monitor K8s Function Generation & Keep System Awake
# This script prevents system sleep and shows live progress updates
###############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE=$(ls -t "$SCRIPT_DIR"/run_all_frameworks_*.log 2>/dev/null | head -1)
PID_FILE="$SCRIPT_DIR/.monitor.pid"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Stopping monitor...${NC}"
    if [ -f "$PID_FILE" ]; then
        CAFFEINATE_PID=$(cat "$PID_FILE")
        kill "$CAFFEINATE_PID" 2>/dev/null
        rm "$PID_FILE"
    fi
    exit 0
}

trap cleanup INT TERM

if [ -z "$LOG_FILE" ]; then
    echo -e "${RED}No log file found!${NC}"
    exit 1
fi

# Start caffeinate to prevent sleep
caffeinate -d -i -m -s &
CAFFEINATE_PID=$!
echo $CAFFEINATE_PID > "$PID_FILE"

echo -e "${GREEN}================================================================${NC}"
echo -e "${GREEN}K8s Function Generation - Live Monitor${NC}"
echo -e "${GREEN}System Sleep Prevention: ACTIVE (PID: $CAFFEINATE_PID)${NC}"
echo -e "${GREEN}================================================================${NC}"
echo ""
echo -e "${BLUE}Log file: $LOG_FILE${NC}"
echo -e "${BLUE}Press Ctrl+C to stop monitoring (process will continue)${NC}"
echo ""
echo -e "${GREEN}================================================================${NC}"
echo ""

# Monitor loop
LAST_SIZE=0
while true; do
    clear
    echo -e "${GREEN}================================================================${NC}"
    echo -e "${GREEN}K8s Function Generation - Live Progress${NC}"
    echo -e "${GREEN}Time: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo -e "${GREEN}================================================================${NC}"
    echo ""
    
    # Count completed and failed
    COMPLETED=$(grep -c "✅.*complete!" "$LOG_FILE" 2>/dev/null || echo "0")
    FAILED=$(grep -c "❌.*failed" "$LOG_FILE" 2>/dev/null || echo "0")
    
    # Get current framework
    CURRENT_FW=$(grep -o "\[.*\] Processing: [A-Z_]*" "$LOG_FILE" | tail -1 | sed 's/.*Processing: //')
    
    echo -e "${BLUE}Progress:${NC}"
    echo -e "  Completed: ${GREEN}$COMPLETED/12${NC}"
    echo -e "  Failed: ${RED}$FAILED${NC}"
    echo -e "  Current: ${YELLOW}$CURRENT_FW${NC}"
    echo ""
    
    # Show which frameworks are done
    echo -e "${BLUE}Completed Frameworks:${NC}"
    grep "✅.*complete!" "$LOG_FILE" 2>/dev/null | sed 's/.*✅ /  ✅ /' | tail -5
    echo ""
    
    # Show last 15 lines
    echo -e "${BLUE}Recent Activity:${NC}"
    echo -e "${YELLOW}────────────────────────────────────────────────────────────${NC}"
    tail -15 "$LOG_FILE" | sed 's/^/  /'
    echo -e "${YELLOW}────────────────────────────────────────────────────────────${NC}"
    echo ""
    
    # File size monitoring
    CURRENT_SIZE=$(wc -c < "$LOG_FILE")
    if [ "$CURRENT_SIZE" -gt "$LAST_SIZE" ]; then
        echo -e "${GREEN}✓ Process is active (log growing)${NC}"
    else
        echo -e "${YELLOW}⚠ Process may be idle (log not growing)${NC}"
    fi
    LAST_SIZE=$CURRENT_SIZE
    
    # Check if process is still running
    if ps -p 42955 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Main process (PID 42955) is running${NC}"
    else
        echo -e "${RED}✗ Main process not found!${NC}"
        # Check for any run_all_frameworks process
        NEW_PID=$(ps aux | grep "[r]un_all_frameworks.sh" | awk '{print $2}')
        if [ -n "$NEW_PID" ]; then
            echo -e "${YELLOW}Found process with PID: $NEW_PID${NC}"
        fi
    fi
    
    echo -e "${GREEN}✓ System sleep prevention: ACTIVE${NC}"
    echo ""
    echo -e "${BLUE}Estimated completion: ~6:00 AM (Nov 13)${NC}"
    echo -e "${YELLOW}Press Ctrl+C to exit monitor (process continues)${NC}"
    
    sleep 10
done

