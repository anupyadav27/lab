# Monitoring & System Sleep Prevention Instructions

## Quick Start - Keep System Awake & Monitor

### Option 1: Automated Monitor (Recommended)

Open a **new terminal window** and run:

```bash
cd /Users/apple/Desktop/compliance_Database/compliance_agent/k8s_function_agent
./monitor_and_keep_awake.sh
```

This will:
- ✅ Prevent system sleep automatically
- ✅ Show live progress updates every 10 seconds
- ✅ Display completed frameworks
- ✅ Show recent log activity
- ✅ Monitor process health

**To stop monitoring**: Press `Ctrl+C` (the main process will continue running)

---

### Option 2: Simple Tail with Sleep Prevention

Open **TWO terminal windows**:

**Terminal 1 - Prevent Sleep:**
```bash
caffeinate -d -i -m -s
```
Keep this running! (Press `Ctrl+C` only when done)

**Terminal 2 - Monitor Progress:**
```bash
cd /Users/apple/Desktop/compliance_Database/compliance_agent/k8s_function_agent
tail -f run_all_frameworks_*.log
```

---

### Option 3: Manual Checks

**Prevent Sleep First:**
```bash
caffeinate -d -i -m -s &
```

**Then check progress periodically:**
```bash
cd /Users/apple/Desktop/compliance_Database/compliance_agent/k8s_function_agent
./check_progress.sh
```

---

## What Each Command Does

### `caffeinate -d -i -m -s`
- `-d`: Prevent display sleep
- `-i`: Prevent system idle sleep
- `-m`: Prevent disk sleep
- `-s`: Prevent system sleep
- Keeps system awake until you press Ctrl+C

### `monitor_and_keep_awake.sh`
- Runs `caffeinate` automatically
- Updates every 10 seconds with:
  - Completed count (X/12)
  - Current framework being processed
  - Recent log activity
  - Process health status
- Press Ctrl+C to stop (main process continues)

### `tail -f run_all_frameworks_*.log`
- Shows live log updates as they happen
- Press Ctrl+C to stop viewing (process continues)

### `check_progress.sh`
- One-time snapshot of current status
- Shows completed frameworks
- Shows last 20 log lines
- Good for quick checks

---

## Recommended Setup

### For Overnight Processing:

1. **Start the monitor in a dedicated terminal:**
   ```bash
   cd /Users/apple/Desktop/compliance_Database/compliance_agent/k8s_function_agent
   ./monitor_and_keep_awake.sh
   ```

2. **Leave terminal window open overnight**

3. **In the morning, check results:**
   ```bash
   ./check_progress.sh
   ls -lh output_*/step3/*.csv
   ```

---

## Current Process Info

**Main Process:**
- PID: 42955
- Started: Nov 12, 2025 22:01:41
- Log: `run_all_frameworks_20251112_220141.log`

**Check if running:**
```bash
ps -p 42955
# or
ps aux | grep run_all_frameworks
```

**Kill if needed (emergency only):**
```bash
kill 42955
```

---

## Monitoring Commands Summary

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `./monitor_and_keep_awake.sh` | Auto monitor + prevent sleep | Overnight processing |
| `caffeinate -d -i -m -s` | Prevent sleep only | If monitor is too verbose |
| `tail -f run_all_*.log` | Live log viewing | Watch detailed progress |
| `./check_progress.sh` | Quick status check | Periodic manual checks |
| `ps aux \| grep run_all` | Check process | Verify still running |

---

## What to Look For

### Good Signs ✅
- Log file size growing
- New "Processing:" lines appearing
- "✅ complete!" messages for frameworks
- HTTP 200 OK responses from OpenAI
- Process PID shows in `ps` output

### Warning Signs ⚠️
- Log stopped growing for >5 minutes
- Many retry attempts
- API errors
- Process not found in `ps`

### If Process Stops
1. Check last error in log: `tail -50 run_all_*.log`
2. Check which framework failed
3. Can resume manually from that framework

---

## Example Monitor Output

```
================================================================
K8s Function Generation - Live Progress
Time: 2025-11-12 22:30:15
================================================================

Progress:
  Completed: 3/12
  Failed: 0
  Current: SOC2

Completed Frameworks:
  ✅ GDPR complete!
  ✅ RBI_BANK complete!
  ✅ RBI_NBFC complete!

Recent Activity:
────────────────────────────────────────────────────────────
  2025-11-12 22:30:10 - INFO - [5/25] Processing: cc_2_1
  2025-11-12 22:30:14 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
────────────────────────────────────────────────────────────

✓ Process is active (log growing)
✓ Main process (PID 42955) is running
✓ System sleep prevention: ACTIVE

Estimated completion: ~6:00 AM (Nov 13)
Press Ctrl+C to exit monitor (process continues)
```

---

## Emergency Commands

**If system starts to sleep:**
```bash
# Wake it up and restart sleep prevention
caffeinate -d -i -m -s &
```

**If process dies, resume from where it stopped:**
```bash
# Check which framework was last completed
grep "✅" run_all_frameworks_*.log | tail -1

# Run remaining frameworks manually
./run_framework.sh NEXT_FRAMEWORK ../path/to/csv
```

**Check system power settings:**
```bash
pmset -g
```

---

## Tips

1. **Best Practice**: Use `monitor_and_keep_awake.sh` - it handles everything
2. **Don't close the terminal** running caffeinate/monitor
3. **Check periodically** if unattended for long periods
4. **Battery**: Ensure laptop is plugged in for overnight processing
5. **Network**: Stable internet required (OpenAI API calls)

---

**Current Status Check:**
```bash
cd /Users/apple/Desktop/compliance_Database/compliance_agent/k8s_function_agent
./check_progress.sh
```

