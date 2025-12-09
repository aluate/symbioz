# Test Setup Complete ✅

## What's Ready

I've created a comprehensive test and reporting system for Otto's memory features:

### Test Files Created

1. **`run_tests_and_report.py`** - Master test runner
   - Runs Phase 3 tests (Memory API & Skills)
   - Runs Phase 4 tests (History, Expiration, Links, Search)
   - Generates comprehensive report
   - Creates cleanup plan if tests fail

2. **`test_otto_phase4.py`** - Phase 4 specific tests
   - Memory history creation and retrieval
   - Expiration and stale marking
   - Memory links
   - Search functionality
   - Search action via Otto API

3. **`README_TESTING.md`** - Testing guide
   - Quick start instructions
   - Troubleshooting tips
   - Manual testing checklist

## How to Run Tests

### Step 1: Start Services

**Option A: Use batch file (easiest)**
```bash
# From repo root
START_OTTO_WINDOWS.bat
```

**Option B: Manual start**
```bash
# Terminal 1: Life OS Backend
cd apps/life_os/backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2: Otto API
cd apps/otto
python -m otto.cli server
```

### Step 2: Run Tests

```bash
cd apps/otto
python run_tests_and_report.py
```

### Step 3: Review Reports

The test runner will generate:
- **`TEST_REPORT.json`** - Full test results with:
  - Overall summary (total, passed, failed, pass rate)
  - Phase breakdown (Phase 3 vs Phase 4)
  - Category breakdown (API, Skills, History, etc.)
  - All test results with details

- **`CLEANUP_PLAN.json`** - (Only if tests fail)
  - List of failed tests
  - Issue descriptions
  - Suggested fixes based on error patterns

## What the Report Will Show

### Overall Summary
- Total tests run
- Pass/fail counts
- Overall pass rate

### Phase Breakdown
- Phase 3 results (Memory API & Skills)
- Phase 4 results (History, Expiration, Links, Search)

### Category Breakdown
- API Operations
- Skill Integration
- Memory History
- Expiration & Maintenance
- Memory Links
- Search
- Usage Tracking

### Failed Tests (if any)
- Test name and phase
- Error message
- Suggested fixes

## Next Steps

1. **Start services** using `START_OTTO_WINDOWS.bat`
2. **Run tests** using `python run_tests_and_report.py`
3. **Review report** in `TEST_REPORT.json`
4. **Fix issues** based on `CLEANUP_PLAN.json` (if generated)
5. **Re-run tests** until all pass

## Expected Test Coverage

### Phase 3 Tests
- ✅ Memory API create
- ✅ Memory API retrieve
- ✅ Memory API list with filters
- ✅ Memory API update
- ✅ Memory API usage tracking
- ✅ Memory skill remember
- ✅ Memory skill recall
- ✅ Memory skill lookup
- ✅ Memory skill update
- ✅ Memory skill delete

### Phase 4 Tests
- ✅ Memory history creation on update
- ✅ Memory history creation on delete
- ✅ Memory history retrieval
- ✅ Memory history version lookup
- ✅ Memory expiration setting
- ✅ Memory stale marking
- ✅ Memory link creation
- ✅ Memory link retrieval
- ✅ Memory link deletion
- ✅ Memory search by text
- ✅ Memory search by filters
- ✅ Memory search action via Otto API

## Cleanup Process

When tests run, the system will:
1. ✅ Check if services are running
2. ✅ Run all Phase 3 tests
3. ✅ Run all Phase 4 tests
4. ✅ Generate comprehensive report
5. ✅ Create cleanup plan for failures
6. ✅ Save reports to JSON files

Then we can:
- Review the report
- Fix any issues identified
- Re-run tests
- Iterate until all pass

---

**Status:** Ready to test! Just start services and run `python run_tests_and_report.py`

