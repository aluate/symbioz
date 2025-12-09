# Phase 3A Implementation Summary: Core Task Management

## Overview
Phase 3A implements the foundational task management system for Life OS, allowing Otto to create, update, and list household tasks.

## What Was Built

### 1. Database Model: `LifeOSTask`
**File:** `apps/life_os/backend/models.py`

Added a new model for household tasks with fields:
- `id`, `created_at`, `updated_at`, `completed_at`
- `title`, `description`
- `status` (todo, in_progress, done, blocked)
- `assignee`, `due_date`, `priority`, `category`

### 2. Life OS Tasks API
**File:** `apps/life_os/backend/life_os_tasks.py`

RESTful API endpoints:
- `POST /life_os/tasks` - Create a new task
- `GET /life_os/tasks` - List tasks (with filters: status, assignee, category)
- `GET /life_os/tasks/{id}` - Get task details
- `PATCH /life_os/tasks/{id}` - Update task
- `DELETE /life_os/tasks/{id}` - Delete task

### 3. Enhanced Otto Actions
**File:** `apps/life_os/backend/otto/actions.py`

Updated action handlers:
- **`life_os.create_task`**: Now creates `LifeOSTask` records (not `OttoTask`)
  - Required: `title`
  - Optional: `description`, `assignee`, `due_date`, `priority`, `category`
- **`life_os.update_task_status`**: Updates `LifeOSTask` records
  - Can update status and other fields
  - Automatically sets `completed_at` when status becomes "done"
- **`life_os.list_tasks`**: New action to query tasks
  - Supports filters: `status`, `assignee`, `category`
  - Returns task count and summary

### 4. Tasks Kanban UI
**File:** `apps/life_os/frontend/app/tasks/page.tsx`

Features:
- **Kanban board** with 3 columns: To Do, In Progress, Done
- **Create task form** with all fields
- **Click to change status** - click any task card to cycle through statuses
- **Visual indicators**: Priority dots, assignee, due date, category
- **Responsive design** for mobile and desktop
- **Quick links** to Otto Console and Life OS home

### 5. Navigation Updates
**File:** `apps/life_os/frontend/app/page.tsx`

Added "Tasks" link to the main Life OS navigation.

## Safety & Integration

### Safety Tiers
- `life_os.create_task`: **TIER_1_LIMITED** (requires basic safety checks)
- `life_os.update_task_status`: **TIER_1_LIMITED**
- `life_os.list_tasks`: **TIER_0_SAFE** (read-only)

### Action Severity
- `life_os.create_task`: **MEDIUM** (failure logged, execution continues)
- `life_os.update_task_status`: **MEDIUM**
- `life_os.list_tasks`: **LOW** (read-only, failure doesn't affect other actions)

## How to Use

### Via UI
1. Navigate to `/tasks` in Life OS frontend
2. Click "+ New Task" to create a task
3. Click any task card to change its status
4. Use filters (if added to UI) or API directly

### Via Otto
Ask Otto in the Otto Console (`/otto`):
- "Create a task: Pay electric bill, due next Friday, high priority"
- "List all my tasks"
- "Mark task #5 as done"
- "What tasks are due this week?"

Otto will use the `life_os.*` actions to interact with tasks.

### Via API
```bash
# Create a task
curl -X POST http://localhost:8000/life_os/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pay electric bill",
    "due_date": "2025-01-15T00:00:00",
    "priority": "high",
    "category": "bills"
  }'

# List tasks
curl http://localhost:8000/life_os/tasks?status=todo

# Update task status
curl -X PATCH http://localhost:8000/life_os/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

## Testing

### Manual Testing
1. Start all services:
   ```bash
   # Windows
   START_OTTO_WINDOWS.bat
   
   # In another terminal
   cd apps\life_os\backend
   python -m worker.otto_worker
   ```

2. Open `http://localhost:3000/tasks`
3. Create a few test tasks
4. Click tasks to change status
5. Test via Otto Console:
   - Go to `http://localhost:3000/otto`
   - Ask: "Create a task: Test task from Otto"
   - Verify it appears in `/tasks`

### Automated Testing
Run the Phase 2 test script (it should still work):
```bash
python test_otto_phase2.py
```

## Next Steps (Phase 3B & 3C)

- **Phase 3B**: Bills management (Bill model, API, UI, BillReminderSkill)
- **Phase 3C**: Calendar integration (CalendarEvent model, API, UI, calendar actions)

## Files Changed

### Backend
- `apps/life_os/backend/models.py` - Added `LifeOSTask` model
- `apps/life_os/backend/life_os_tasks.py` - New API router
- `apps/life_os/backend/main.py` - Registered new router
- `apps/life_os/backend/otto/actions.py` - Enhanced action handlers
- `apps/life_os/backend/otto/safety.py` - Added safety tier for `list_tasks`

### Frontend
- `apps/life_os/frontend/app/tasks/page.tsx` - New Tasks page
- `apps/life_os/frontend/app/page.tsx` - Added Tasks link

## Notes

- Tasks are stored in SQLite database (`life_os.db`)
- The kanban UI is a simple v1 - can be enhanced with drag-and-drop later
- Otto can now create, update, and query tasks via structured actions
- All task operations go through the same safety and action executor pipeline

