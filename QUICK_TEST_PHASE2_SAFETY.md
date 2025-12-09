# Quick Test - Phase 2 + Safety Features

**Time:** ~5 minutes  
**Goal:** Verify Otto works and safety features are active

---

## Step 1: Start Everything

```batch
# Terminal 1: Start all services
START_OTTO_WINDOWS.bat

# Terminal 2: Start worker
cd apps\life_os\backend
python -m worker.otto_worker
```

**Expected output from worker:**
```
Starting Otto Worker...
Otto API URL: http://localhost:8001
Poll interval: 30 seconds
Otto Enabled: True
Max actions per run: 10
Press Ctrl+C to stop
```

---

## Step 2: Test Otto's Self-Test (Option B)

**Via Otto Console:**
1. Open http://localhost:3000/otto
2. Type: `"run a self-test"`
3. Click "Send to Otto"

**Expected:** Otto reports on:
- ✓ Worker status
- ✓ API health
- ✓ Actions available

---

## Step 3: Test Safety Features

### Test 1: Kill Switch

```batch
# In worker terminal, press Ctrl+C to stop
# Set environment variable
set OTTO_ENABLED=false

# Restart worker
python -m worker.otto_worker
```

**Expected:** Worker shows "⚠️  Otto is DISABLED" and doesn't process tasks

### Test 2: Retry Logic

```bash
# Create a task that will fail (invalid type)
curl -X POST http://localhost:8000/otto/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"type\": \"invalid.type\", \"description\": \"This will fail\"}"
```

**Expected:**
- Task processes → fails → retries (1min delay)
- After 3 failures → status = "blocked"

### Test 3: Tier Checking

```bash
# Create Tier 3 task (requires approval)
curl -X POST http://localhost:8000/otto/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"type\": \"bills.mark_paid\", \"description\": \"Test bill payment\"}"
```

**Expected:**
- Task created with `status="pending_approval"`
- Worker skips it (requires approval)

### Test 4: Test Artifact Tagging

```bash
# Create test task
curl -X POST http://localhost:8000/otto/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"type\": \"otto.log\", \"description\": \"[OTTO_SELF_TEST] Test task\", \"payload\": {\"message\": \"test\"}}"
```

**Expected:**
- Task created normally
- In `OTTO_MODE=prod`, worker would skip it
- Can be filtered from UI

---

## Step 4: Full End-to-End Test

```bash
# Create a simple task that should work
curl -X POST http://localhost:8000/otto/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"type\": \"otto.log\", \"description\": \"Test task\", \"payload\": {\"message\": \"Hello from test!\"}}"
```

**Watch:**
1. Worker console: `Processed 1 task(s)`
2. Otto Console: New run with `source="worker"`
3. Task status: `pending` → `running` → `success`

---

## Success Criteria

✅ Worker starts and shows safety config  
✅ Self-test reports all systems OK  
✅ Kill switch disables worker  
✅ Failed tasks retry with backoff  
✅ Tier 3 tasks require approval  
✅ Test artifacts are detected  
✅ End-to-end task processing works  

---

**If all tests pass → Ready for Phase 3!** 🚀

