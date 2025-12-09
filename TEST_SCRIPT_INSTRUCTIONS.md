# Comprehensive Test Script Instructions

## Overview

The `test_otto_comprehensive.py` script tests all Phase 2 + Safety + Phase 3 features:
- Service health checks
- Otto Shell (manual prompts)
- Worker task processing
- Life OS actions (create task)
- Bills actions (create bill)
- Calendar actions (create event)
- Safety tier enforcement
- Retry logic
- Otto Runs API
- Life OS APIs (Tasks, Bills, Calendar)

## Prerequisites

**You MUST start these services before running the test:**

1. **Start all services:**
   ```bash
   START_OTTO_WINDOWS.bat
   ```
   Or manually:
   - Otto API: `cd apps\otto && python -m otto.cli server` (port 8001)
   - Life OS Backend: `cd apps\life_os\backend && python -m uvicorn main:app --reload --port 8000` (port 8000)
   - Life OS Frontend: `cd apps\life_os\frontend && npm run dev` (port 3000)

2. **Start the worker (in a separate terminal):**
   ```bash
   cd apps\life_os\backend
   python -m worker.otto_worker
   ```

## Running the Test

```bash
python test_otto_comprehensive.py
```

The test will:
- Wait up to 30 seconds for services to start
- Run all test suites
- Report pass/fail for each test
- Provide a summary at the end

## What Gets Tested

### Test 1: Service Health
- Checks if Life OS Backend is running (port 8000)
- Checks if Otto API is running (port 8001)

### Test 2: Otto Shell
- Creates a manual prompt via `/otto/runs`
- Verifies Otto responds

### Test 3: Worker Task Processing
- Creates an `otto.log` task
- Waits for worker to process it
- Verifies task status changes to "success"
- Checks that an OttoRun was created

### Test 4: Life OS Create Task Action
- Creates a task that should trigger `life_os.create_task` action
- Waits for worker to process
- Verifies a Life OS task was created

### Test 5: Bills Create Action
- Creates a task that should trigger `bills.create` action
- Waits for worker to process
- Verifies a bill was created

### Test 6: Calendar Create Event Action
- Creates a task that should trigger `calendar.create_event` action
- Waits for worker to process
- Verifies a calendar event was created

### Test 7: Safety Tier Enforcement
- Tests that safety tier registry works correctly
- Verifies TIER_0_SAFE and TIER_1_LIMITED are registered

### Test 8: Retry Logic
- Creates a task with invalid action type
- Verifies retry count increments
- Checks backoff logic

### Test 9: Otto Runs API
- Tests `/otto/runs` list endpoint
- Tests `/otto/runs/{id}` detail endpoint

### Test 10: Life OS APIs
- Tests `/life_os/tasks` endpoint
- Tests `/bills` endpoint
- Tests `/calendar` endpoint

## Expected Results

When all services are running and worker is active:
- ✅ All tests should pass
- ✅ Tasks should be processed within 60 seconds
- ✅ Actions should execute successfully
- ✅ Database records should be created

## Troubleshooting

**Services not starting:**
- Check if ports 8000, 8001, 3000 are available
- Check Python/Node dependencies are installed
- Run `setup_otto_windows.bat` first

**Worker not processing tasks:**
- Check worker console for errors
- Verify `OTTO_API_URL` environment variable
- Check database connection

**Tasks staying "pending":**
- Worker may not be running
- Worker may not be able to reach Otto API
- Check worker console logs

**Actions not executing:**
- Check action executor logs in run output
- Verify action handlers are registered
- Check database for created records

## Next Steps After Testing

Once tests pass:
1. Check http://localhost:3000/otto for run history
2. Check http://localhost:3000/tasks for created tasks
3. Check http://localhost:3000/bills for created bills
4. Check http://localhost:3000/calendar for created events

