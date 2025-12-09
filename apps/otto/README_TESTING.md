# Otto Memory System - Testing Guide

## Quick Start

1. **Start Services:**
   ```bash
   # From repo root
   START_OTTO_WINDOWS.bat
   
   # Or manually:
   # Terminal 1: Life OS Backend
   cd apps/life_os/backend
   python -m uvicorn main:app --reload --port 8000
   
   # Terminal 2: Otto API
   cd apps/otto
   python -m otto.cli server
   ```

2. **Run Tests:**
   ```bash
   cd apps/otto
   python run_tests_and_report.py
   ```

3. **Review Reports:**
   - `TEST_REPORT.json` - Full test results
   - `CLEANUP_PLAN.json` - Suggested fixes (if any failures)

## Test Suites

### Phase 3 Tests (`test_otto_phase3.py`)
- Memory API operations (create, retrieve, list, update, delete)
- Usage tracking
- Memory skill operations (remember, recall, lookup, update, delete)

### Phase 4 Tests (`test_otto_phase4.py`)
- Memory history (version tracking)
- Expiration and stale marking
- Memory links (relationships)
- Search functionality
- Search action via Otto API

## Test Report Structure

The comprehensive test report includes:
- Overall summary (total, passed, failed, pass rate)
- Phase breakdown (Phase 3 vs Phase 4)
- Category breakdown (API Operations, Skills, History, etc.)
- Failed tests with details
- Passed tests summary

## Cleanup Plan

If tests fail, `CLEANUP_PLAN.json` is generated with:
- List of failed tests
- Issue descriptions
- Suggested fixes based on error patterns

## Manual Testing

After automated tests pass, manually test:
- Memory Console UI at `/otto/memory`
- Edit memory and verify history
- Mark stale and set expiration
- Create links and view relationships
- Search functionality in UI

## Troubleshooting

**Services not reachable:**
- Check that services are running
- Verify ports 8000 (Life OS) and 8001 (Otto API) are not in use
- Check firewall settings

**404 errors:**
- Verify database migrations are applied
- Check that models exist in database

**500 errors:**
- Check server logs
- Verify database schema matches models
- Check for missing dependencies

