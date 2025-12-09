# Phase 3B Implementation Summary: Bills Management

## Overview
Phase 3B implements a complete bills management system for Life OS, allowing users to track bills, set up recurring bills, and have Otto automatically create reminder tasks for upcoming or overdue bills.

## What Was Built

### 1. Database Model: `Bill`
**File:** `apps/life_os/backend/models.py`

Added a new model for household bills with fields:
- `id`, `created_at`, `updated_at`, `paid_at`
- `name`, `amount`, `due_date`, `paid` (yes, no, partial)
- `category`, `payee`, `account_number`, `notes`
- `is_recurring`, `recurrence_frequency`, `next_due_date` (for recurring bills)

### 2. Bills API
**File:** `apps/life_os/backend/bills.py`

RESTful API endpoints:
- `POST /bills` - Create a new bill
- `GET /bills` - List bills (with filters: paid, category, upcoming, overdue)
- `GET /bills/{id}` - Get bill details
- `PATCH /bills/{id}` - Update bill (including marking as paid)
- `DELETE /bills/{id}` - Delete bill
- `GET /bills/upcoming/summary` - Get summary of upcoming bills (count, total amount, overdue count)

**Special Features:**
- When marking a recurring bill as paid, automatically creates the next occurrence
- Calculates `next_due_date` based on `recurrence_frequency` (monthly, quarterly, yearly)

### 3. BillReminderSkill
**File:** `apps/otto/otto/skills/bill_reminder.py`

New Otto skill that:
- Monitors bills from Life OS API
- Analyzes bills to determine if reminders are needed:
  - **Overdue**: Always creates high-priority reminder
  - **Due in 3 days**: High-priority reminder
  - **Due in 7 days**: Medium-priority reminder
  - **Due in 14 days**: Medium-priority reminder
  - **Due in 30 days**: Low-priority reminder
- Creates `life_os.create_task` actions for bills needing reminders
- Can be triggered via task types: `bill_reminder`, `check_bills`, `create_bill_reminders`, `scan_bills`, `upcoming_bills`

### 4. Otto Actions for Bills
**File:** `apps/life_os/backend/otto/actions.py`

New action handlers:
- **`bills.create`**: Creates a new bill
  - Required: `name`, `amount`, `due_date`
  - Optional: `category`, `payee`, `account_number`, `notes`, `is_recurring`, `recurrence_frequency`
- **`bills.update`**: Updates a bill (including marking as paid)
- **`bills.list`**: Lists bills with optional filters

### 5. Bills UI
**File:** `apps/life_os/frontend/app/bills/page.tsx`

Features:
- **Summary cards**: Shows upcoming count, total amount, overdue count
- **Filter buttons**: All Unpaid, Upcoming, Overdue, Paid
- **Create bill form**: Full form with all fields including recurring bill setup
- **Bill cards**: Visual display with:
  - Color-coded left border (red=overdue, orange=upcoming, green=paid)
  - Amount, due date, payee, category
  - Recurring bill indicator
  - Overdue/Paid badges
  - "Mark as Paid" button
- **Responsive design** for mobile and desktop

### 6. Navigation Updates
**File:** `apps/life_os/frontend/app/page.tsx`

Added "Bills" link to the main Life OS navigation.

## Safety & Integration

### Safety Tiers
- `bills.create`: **TIER_1_LIMITED** (requires basic safety checks)
- `bills.update`: **TIER_1_LIMITED**
- `bills.list`: **TIER_0_SAFE** (read-only)

### Action Severity
- `bills.create`: **MEDIUM** (failure logged, execution continues)
- `bills.update`: **MEDIUM**
- `bills.list`: **LOW** (read-only, failure doesn't affect other actions)

## How to Use

### Via UI
1. Navigate to `/bills` in Life OS frontend
2. Click "+ New Bill" to create a bill
3. Use filters to view upcoming, overdue, or paid bills
4. Click "Mark as Paid" to mark a bill as paid
5. View summary cards for quick overview

### Via Otto
Ask Otto in the Otto Console (`/otto`):
- "Check my bills" - Scans bills and creates reminder tasks
- "Create a bill: Electric bill, $150, due next Friday"
- "What bills are due this month?"
- "Mark bill #3 as paid"

Otto will use the `bill_reminder` skill and `bills.*` actions to interact with bills.

### Via API
```bash
# Create a bill
curl -X POST http://localhost:8000/bills \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electric Bill",
    "amount": "$150.00",
    "due_date": "2025-01-15T00:00:00",
    "category": "utilities",
    "payee": "Electric Company",
    "is_recurring": "yes",
    "recurrence_frequency": "monthly"
  }'

# Get upcoming bills summary
curl http://localhost:8000/bills/upcoming/summary?days=30

# Mark bill as paid
curl -X PATCH http://localhost:8000/bills/1 \
  -H "Content-Type: application/json" \
  -d '{"paid": "yes"}'
```

### Automated Bill Reminders
Create an OttoTask to run bill reminders:
```bash
curl -X POST http://localhost:8000/otto/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "type": "bill_reminder",
    "description": "Check bills and create reminders",
    "payload": {}
  }'
```

The worker will process this task, and Otto's `BillReminderSkill` will:
1. Fetch all unpaid bills
2. Analyze which ones need reminders
3. Create `life_os.create_task` actions for each bill needing a reminder
4. The action executor will create the reminder tasks

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

2. Open `http://localhost:3000/bills`
3. Create a few test bills (including a recurring one)
4. Test filters (upcoming, overdue, paid)
5. Mark a bill as paid and verify recurring bill creates next occurrence
6. Test via Otto Console:
   - Go to `http://localhost:3000/otto`
   - Ask: "Check my bills"
   - Verify reminder tasks are created in `/tasks`

### Automated Testing
You can create an OttoTask to test bill reminders:
```bash
curl -X POST http://localhost:8000/otto/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "type": "bill_reminder",
    "description": "Test bill reminder",
    "payload": {}
  }'
```

Watch the worker logs to see Otto process the task and create reminder actions.

## Next Steps (Phase 3C)

- **Phase 3C**: Calendar integration (CalendarEvent model, API, UI, calendar actions)

## Files Changed

### Backend
- `apps/life_os/backend/models.py` - Added `Bill` model
- `apps/life_os/backend/bills.py` - New API router
- `apps/life_os/backend/main.py` - Registered bills router
- `apps/life_os/backend/otto/actions.py` - Added bill action handlers
- `apps/life_os/backend/otto/safety.py` - Added safety tiers for bill actions

### Otto
- `apps/otto/otto/skills/bill_reminder.py` - New BillReminderSkill
- `apps/otto/otto/skills/__init__.py` - Registered BillReminderSkill

### Frontend
- `apps/life_os/frontend/app/bills/page.tsx` - New Bills page
- `apps/life_os/frontend/app/page.tsx` - Added Bills link

## Notes

- Bills are stored in SQLite database (`life_os.db`)
- Recurring bills automatically create the next occurrence when marked as paid
- BillReminderSkill can be scheduled to run periodically (e.g., daily) to check for bills needing reminders
- Otto creates reminder tasks automatically, which appear in the Tasks kanban board
- All bill operations go through the same safety and action executor pipeline

