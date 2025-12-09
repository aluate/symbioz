# Prompt: Build OTTO Activity Reporting Tool

**Purpose:** Create a tool/skill that allows OTTO to track and report on all activity and changes within specified time periods, with automatic daily reports showing progress from one day to the next.

**Date:** January 2025  
**Target:** OTTO Skills System

---

## Overview

Build a new OTTO skill called `ActivityReportingSkill` that:

1. **Tracks Activity Across All Systems** - Monitors changes in:
   - OTTO tasks (created, executed, completed, failed)
   - Actions executed (all action types from the action registry)
   - Life OS entities (tasks created/updated, bills, calendar events, income, transactions)
   - Memory entries (created, updated, used)
   - Any other tracked entities with `created_at`/`updated_at` timestamps

2. **Generates Activity Reports** - Creates comprehensive reports for any time period:
   - User-specified start and end dates/times
   - Summary statistics (counts by type, success rates, etc.)
   - Detailed change log (what changed, when, by what)
   - Categorized by entity type and action type

3. **Automatic Daily Reports** - Runs daily to generate "last 24 hours" reports:
   - Executes automatically each day (configurable time, default: midnight)
   - Compares current day's activity to previous day
   - Shows progress metrics (more/less activity, trends)
   - Stores reports for historical comparison
   - Can be retrieved via API or stored in a reports table

---

## Technical Requirements

### 1. Database Schema

Add a new table `activity_reports` to track generated reports:

```sql
CREATE TABLE activity_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    report_type VARCHAR(50) NOT NULL,  -- 'daily', 'custom', 'period'
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    report_data JSON NOT NULL,  -- Full report data
    summary TEXT,  -- Human-readable summary
    comparison_data JSON,  -- For daily reports: comparison to previous period
    metadata JSON  -- Additional metadata (generation time, etc.)
);
```

### 2. Skill Implementation

**File:** `apps/otto/otto/skills/activity_reporting.py`

**Task Types Handled:**
- `activity.report` - Generate report for a custom time period
- `activity.daily_report` - Generate or retrieve today's daily report
- `activity.compare_periods` - Compare activity between two periods
- `activity.list_reports` - List available reports
- `activity.get_report` - Get a specific report by ID

**Key Methods:**

1. **`generate_period_report(start_time, end_time)`**
   - Query all relevant tables for changes in the period
   - Aggregate by entity type, action type, status
   - Calculate statistics (totals, success rates, trends)
   - Return structured report data

2. **`generate_daily_report(target_date=None)`**
   - If target_date is None, use yesterday (last 24 hours)
   - Generate report for the period
   - If previous day's report exists, compare and include delta metrics
   - Store report in `activity_reports` table
   - Return report with comparison data

3. **`compare_reports(report1_id, report2_id)`**
   - Load two reports
   - Calculate differences (more/less activity, new types, etc.)
   - Return comparison summary

**Data Sources to Query:**

- `otto_tasks` - All tasks (created_at, updated_at, status changes)
- `otto_runs` - All runs (created_at, status, actions executed)
- `life_os_tasks` - Life OS tasks (created_at, updated_at, completed_at)
- `bills` - Bills (created_at, updated_at, paid_at)
- `calendar_events` - Events (created_at, updated_at)
- `income` - Income entries (created_at, updated_at)
- `transactions` - Transactions (created_at, updated_at)
- `otto_memory` - Memory entries (created_at, updated_at, last_used_at)
- Action execution logs (if stored separately)

**Report Structure:**

```json
{
  "period": {
    "start": "2025-01-15T00:00:00Z",
    "end": "2025-01-16T00:00:00Z",
    "duration_hours": 24
  },
  "summary": {
    "total_changes": 45,
    "tasks_created": 12,
    "tasks_completed": 8,
    "actions_executed": 23,
    "entities_created": 15,
    "entities_updated": 30
  },
  "by_category": {
    "tasks": {
      "created": 12,
      "completed": 8,
      "failed": 1,
      "pending": 3
    },
    "actions": {
      "life_os.create_task": 5,
      "bills.create": 2,
      "calendar.create_event": 3,
      "memory.remember": 4
    },
    "entities": {
      "life_os_tasks": {"created": 5, "updated": 3},
      "bills": {"created": 2, "updated": 1},
      "calendar_events": {"created": 3, "updated": 2}
    }
  },
  "timeline": [
    {
      "timestamp": "2025-01-15T10:30:00Z",
      "type": "task_created",
      "entity": "life_os_tasks",
      "id": 123,
      "title": "Pay electric bill"
    }
  ],
  "comparison": {
    "previous_period": {
      "start": "2025-01-14T00:00:00Z",
      "end": "2025-01-15T00:00:00Z"
    },
    "deltas": {
      "total_changes": "+12",
      "tasks_created": "+3",
      "tasks_completed": "+2"
    },
    "trends": {
      "activity_increased": true,
      "completion_rate_improved": true
    }
  }
}
```

### 3. Scheduled Daily Report Generation

**Option A: Cron-style scheduling in OTTO**
- Add a scheduled task system to OTTO core
- Register daily report generation as a recurring task
- Runs at configurable time (default: 00:00 UTC)

**Option B: External scheduler**
- Use system cron or task scheduler
- Call OTTO API endpoint to trigger daily report
- Endpoint: `POST /task` with `type: "activity.daily_report"`

**Option C: Life OS integration**
- Add to Life OS backend as a scheduled job
- Runs daily and calls OTTO API or directly uses the skill

### 4. API Integration

**Otto API Endpoints:**
- `POST /task` with `type: "activity.report"` and payload:
  ```json
  {
    "start_time": "2025-01-15T00:00:00Z",
    "end_time": "2025-01-16T00:00:00Z",
    "include_timeline": true,
    "include_comparison": false
  }
  ```

- `POST /task` with `type: "activity.daily_report"` and payload:
  ```json
  {
    "target_date": "2025-01-15",  // Optional, defaults to yesterday
    "store": true,  // Whether to store the report
    "compare_previous": true  // Whether to compare to previous day
  }
  ```

- `POST /task` with `type: "activity.get_report"` and payload:
  ```json
  {
    "report_id": 123
  }
  ```

- `POST /task` with `type: "activity.list_reports"` and payload:
  ```json
  {
    "report_type": "daily",  // Optional filter
    "limit": 30
  }
  ```

### 5. Life OS Backend Integration

**New Endpoints in Life OS Backend:**

- `GET /otto/activity/report?start=...&end=...` - Generate custom report
- `GET /otto/activity/daily` - Get today's daily report (generates if missing)
- `GET /otto/activity/reports` - List all reports
- `GET /otto/activity/reports/{id}` - Get specific report
- `GET /otto/activity/compare?report1_id=...&report2_id=...` - Compare reports

---

## Implementation Steps

1. **Create Database Migration**
   - Add `activity_reports` table
   - Add indexes on `created_at`, `report_type`, `period_start`, `period_end`

2. **Implement ActivityReportingSkill**
   - Create skill file with all task type handlers
   - Implement query logic for all data sources
   - Implement report generation and comparison logic
   - Register skill in `apps/otto/otto/skills/__init__.py`

3. **Add Database Models**
   - Create `ActivityReport` model in `apps/life_os/backend/models.py`
   - Add relationships if needed

4. **Create Life OS API Endpoints**
   - Add endpoints in `apps/life_os/backend/api/otto.py`
   - Handle authentication and authorization
   - Return formatted reports

5. **Add Scheduled Task (Optional)**
   - Implement daily report generation scheduler
   - Configure default schedule
   - Add ability to enable/disable via config

6. **Testing**
   - Test report generation for various time periods
   - Test daily report generation and comparison
   - Test API endpoints
   - Test with empty periods (no activity)
   - Test with high activity periods

---

## Usage Examples

### Generate Custom Period Report

```python
# Via OTTO API
POST /task
{
  "type": "activity.report",
  "payload": {
    "start_time": "2025-01-01T00:00:00Z",
    "end_time": "2025-01-31T23:59:59Z",
    "include_timeline": true
  }
}
```

### Get Daily Report

```python
# Via OTTO API
POST /task
{
  "type": "activity.daily_report",
  "payload": {
    "target_date": "2025-01-15",  # Optional
    "compare_previous": true,
    "store": true
  }
}
```

### Via Life OS API

```bash
# Get today's daily report
curl http://localhost:8000/otto/activity/daily

# Get custom period report
curl "http://localhost:8000/otto/activity/report?start=2025-01-01T00:00:00Z&end=2025-01-31T23:59:59Z"

# List all daily reports
curl http://localhost:8000/otto/activity/reports?report_type=daily&limit=30
```

---

## Success Criteria

✅ Skill can generate reports for any time period  
✅ Daily reports automatically generated and stored  
✅ Reports include comparison to previous period  
✅ All major entity types are tracked  
✅ API endpoints work correctly  
✅ Reports are stored and retrievable  
✅ Performance is acceptable (reports generate in < 5 seconds for 24-hour periods)  

---

## Future Enhancements

- **Visualization** - Generate charts/graphs for activity trends
- **Alerts** - Alert on unusual activity patterns
- **Export** - Export reports as PDF, CSV, or JSON
- **Filtering** - Filter reports by entity type, action type, user, etc.
- **Real-time** - WebSocket endpoint for real-time activity feed
- **Activity Dashboard** - Web UI showing activity in real-time

---

## Notes

- This skill should be **read-only** - it only queries and reports, never modifies data
- Consider caching frequently accessed reports
- For large time periods, consider pagination or summary-only mode
- Ensure queries are optimized with proper indexes
- Handle timezone considerations (store all times in UTC, convert for display)
