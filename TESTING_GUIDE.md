# Testing Guide - Phase 2

This guide shows you how to test Otto Phase 2, and how Otto can test himself!

---

## Option 1: Manual Testing (You Test It)

### Quick Test Script

Run the automated test script:

```bash
python test_otto_phase2.py
```

This script will:
1. ✅ Check if services are running
2. ✅ Create a test task
3. ✅ Wait for worker to process it
4. ✅ Verify a run was created
5. ✅ Report results

**Prerequisites:**
- All services running (`START_OTTO_WINDOWS.bat`)
- Worker running (`python -m worker.otto_worker`)

### Manual Testing Steps

1. **Start everything:**
   ```batch
   START_OTTO_WINDOWS.bat
   ```

2. **Start worker (separate terminal):**
   ```batch
   cd apps\life_os\backend
   python -m worker.otto_worker
   ```

3. **Create a test task:**
   ```bash
   curl -X POST http://localhost:8000/otto/tasks ^
     -H "Content-Type: application/json" ^
     -d "{\"type\": \"otto.log\", \"description\": \"Test task\", \"payload\": {\"message\": \"Hello from worker!\"}}"
   ```

4. **Watch it process:**
   - Worker console should show: `Processed 1 task(s)`
   - Open http://localhost:3000/otto
   - You should see a new run with `source="worker"`

5. **Verify task status:**
   ```bash
   curl http://localhost:8000/otto/tasks
   ```
   The task should show `status="success"`

---

## Option 2: Otto Tests Himself (Meta!)

Otto can now test his own functionality using the `SelfTestSkill`!

### Quick Test (Default - No DB Spam)

**Via Otto Console:**
1. Open http://localhost:3000/otto
2. Send this prompt:
   ```
   Run a self-test
   ```
   or
   ```
   Are you okay?
   ```

**What it does:**
- ✅ Checks if worker is processing tasks
- ✅ Tests all API endpoints (Otto API, Life OS API, Tasks API)
- ✅ Verifies action executor exists
- ✅ **Does NOT create test tasks** (cheap, fast)

### Full Test (Creates Test Task)

**Via Otto Console:**
1. Send this prompt:
   ```
   Run a full self-test
   ```
   or
   ```
   Test yourself completely
   ```

**What it does:**
- ✅ All quick test checks
- ✅ Creates a test task (tagged with `[OTTO_SELF_TEST]`)
- ✅ Waits for worker to process it
- ✅ Verifies full loop works

**Note:** Full tests create database records. Use sparingly!

### Via API

```bash
curl -X POST http://localhost:8001/prompt ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\": \"test yourself\", \"source\": \"test\"}"
```

### Create Test Task via Otto

You can even ask Otto to create a test task for himself:

```bash
curl -X POST http://localhost:8001/task ^
  -H "Content-Type: application/json" ^
  -d "{\"type\": \"self_test\", \"payload\": {\"test_type\": \"full\", \"create_test_task\": true}, \"source\": \"test\"}"
```

This will:
1. Run self-tests
2. Create a test task (if `create_test_task: true`)
3. The worker will process it
4. You can see the results in Otto Console

---

## What to Look For

### ✅ Success Indicators

- Worker console shows: `Processed 1 task(s)`
- Task status changes: `pending` → `running` → `success`
- OttoRun created with `source="worker"`
- Run has `output_text` and `output_payload`
- Actions executed (check `output_payload.action_results`)

### ⚠️ Common Issues

**Task stays "pending":**
- Worker not running
- Worker can't reach Otto API
- Check worker console for errors

**Task goes to "error":**
- Otto API returned error
- Action execution failed
- Check `last_error` field in task
- Check `logs` field in run

**No run created:**
- Worker crashed before creating run
- Database connection issue
- Check worker console

---

## Next Steps After Testing

Once basic testing works:

1. **Try different action types:**
   - `life_os.create_task` - Create a new task
   - `life_os.update_task_status` - Update task status

2. **Test recurring tasks:**
   - Create task with `next_run_at` set
   - Worker should process it at the scheduled time

3. **Test error handling:**
   - Create task with invalid type
   - See how worker handles it

4. **Use Otto Console:**
   - Create tasks via UI
   - View all runs (manual + worker)
   - See action execution results

---

**Happy Testing!** 🦉

