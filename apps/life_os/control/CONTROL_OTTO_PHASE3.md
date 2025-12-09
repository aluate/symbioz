# CONTROL_OTTO_PHASE3.md — Real-Life Integrations

**⚠️ CRITICAL: Read `apps/otto/CONTROL_OTTO_META_RULES.md` FIRST — it is primary governance.**

**Goal:** Wire Otto into your actual daily life with real, useful automations.

This builds on:
- `apps/otto/CONTROL_OTTO_META_RULES.md` (PRIMARY GOVERNANCE - READ FIRST)
- `CONTROL_OTTO_SHELL.md` (Phase 1)
- `CONTROL_OTTO_PHASE2.md` (Phase 2 - Worker + Actions)
- `CONTROL_OTTO_SAFETY.md` (Safety infrastructure)

**Status:** Phase 2 + Safety complete ✅

---

## Phase 3 Overview

Phase 3 adds **real-life task types** and **daily-use integrations** so Otto becomes actually useful, not just a demo.

**Key Principle:** Start small, one integration at a time. Each integration should:
- Solve a real problem
- Be testable end-to-end
- Respect safety tiers
- Be reversible/auditable

---

## Part 1 — Real Life OS Task Types

### 1.1 Life OS Task Model

First, we need a proper `LifeOSTask` model (separate from `OttoTask`).

**Model:** `LifeOSTask`

Fields:
- `id` (PK)
- `title` (string)
- `description` (text, nullable)
- `status` (enum: `todo`, `in_progress`, `done`, `blocked`)
- `assignee` (string, nullable) - e.g., "Karl", "Brit", "Household"
- `due_date` (datetime, nullable)
- `priority` (enum: `low`, `medium`, `high`, nullable)
- `category` (string, nullable) - e.g., "bills", "household", "work"
- `created_at`, `updated_at`
- `completed_at` (datetime, nullable)

**Migration:** Add `life_os_tasks` table

### 1.2 Life OS Tasks API

Add router: `/life_os/tasks`

Endpoints:
- `POST /life_os/tasks` - Create task
- `GET /life_os/tasks` - List tasks (with filters)
- `GET /life_os/tasks/{id}` - Get task details
- `PATCH /life_os/tasks/{id}` - Update task
- `DELETE /life_os/tasks/{id}` - Delete task

### 1.3 Action Handlers

Update `otto/actions.py` to add:

**`life_os.create_task`** (already exists, enhance it):
- Creates `LifeOSTask` record
- Returns task ID
- Can set assignee, due_date, priority, category

**`life_os.update_task_status`** (already exists, enhance it):
- Updates `LifeOSTask.status`
- Sets `completed_at` if status = "done"
- Can update other fields too

**New: `life_os.list_tasks`**:
- Queries `LifeOSTask` records
- Returns filtered list
- Used by Otto to see what tasks exist

---

## Part 2 — First Real Integration: Bill Reminders

### 2.1 Bill Model

**Model:** `Bill`

Fields:
- `id` (PK)
- `name` (string) - e.g., "Electric Bill"
- `amount` (decimal, nullable)
- `due_date` (date)
- `frequency` (enum: `monthly`, `quarterly`, `yearly`, `one_time`)
- `paid` (boolean, default false)
- `paid_date` (date, nullable)
- `category` (string, nullable) - for tax purposes
- `notes` (text, nullable)
- `created_at`, `updated_at`

### 2.2 Bill Reminder Task Type

**Task Type:** `life_os.bill_reminder`

**Behavior:**
- Otto scans `Bill` records
- Finds bills with `due_date` approaching (e.g., 7 days out)
- Creates `LifeOSTask` with:
  - Title: "Pay [Bill Name]"
  - Due date: Bill's due date
  - Category: "bills"
  - Priority: "high" if overdue, "medium" if due soon

**Safety:** Tier 1 (limited writes, non-sensitive)

**Implementation:**
- New Otto skill: `BillReminderSkill`
- Runs on schedule (e.g., daily)
- Creates `OttoTask` with type `life_os.bill_reminder`
- Worker processes it
- Skill creates `LifeOSTask` records via action

### 2.3 Bill API

Add router: `/life_os/bills`

Endpoints:
- `POST /life_os/bills` - Create bill
- `GET /life_os/bills` - List bills
- `PATCH /life_os/bills/{id}` - Update bill (e.g., mark paid)
- `DELETE /life_os/bills/{id}` - Delete bill

---

## Part 3 — Calendar Integration (Basic)

### 3.1 Calendar Event Model

**Model:** `CalendarEvent`

Fields:
- `id` (PK)
- `title` (string)
- `description` (text, nullable)
- `start_time` (datetime)
- `end_time` (datetime, nullable)
- `location` (string, nullable)
- `all_day` (boolean, default false)
- `reminder_minutes` (int, nullable) - e.g., 60 for 1 hour before
- `created_at`, `updated_at`

### 3.2 Calendar Action

**Action Type:** `calendar.create_event`

**Behavior:**
- Creates `CalendarEvent` record
- Can be triggered by Otto or manually
- Future: Sync with Google Calendar

**Safety:** Tier 2 (sensitive - affects scheduling)

### 3.3 Calendar API

Add router: `/life_os/calendar`

Endpoints:
- `POST /life_os/calendar/events` - Create event
- `GET /life_os/calendar/events` - List events (with date range)
- `PATCH /life_os/calendar/events/{id}` - Update event
- `DELETE /life_os/calendar/events/{id}` - Delete event

---

## Part 4 — Otto Skills for Real Life

### 4.1 BillReminderSkill

**Location:** `apps/otto/otto/skills/bill_reminder.py`

**Task Types:** `life_os.bill_reminder`, `check_bills`, `scan_bills`

**Behavior:**
1. Queries Life OS backend for bills
2. Finds bills due in next 7 days (or overdue)
3. For each bill, creates action:
   ```json
   {
     "type": "life_os.create_task",
     "payload": {
       "title": "Pay [Bill Name]",
       "due_date": "[bill due date]",
       "category": "bills",
       "priority": "high" or "medium"
     }
   }
   ```

**Safety:** Tier 1

### 4.2 TaskManagementSkill

**Location:** `apps/otto/otto/skills/task_management.py`

**Task Types:** `life_os.list_tasks`, `life_os.summarize_tasks`, `life_os.find_overdue`

**Behavior:**
- Queries Life OS tasks
- Can summarize, filter, report
- Read-only (Tier 0)

---

## Part 5 — UI Integration

### 5.1 Life OS Tasks Page

**Route:** `/life_os/tasks` or `/tasks`

**Features:**
- Kanban board view (todo / in_progress / done)
- Create task button
- Filter by assignee, category, due date
- Link to Otto Console for automation

### 5.2 Bills Page

**Route:** `/life_os/bills`

**Features:**
- List of bills
- Upcoming/overdue highlighted
- Mark paid button
- Create bill form
- Link to Otto for reminders

### 5.3 Quick Actions in Otto Console

Add buttons/shortcuts:
- "Create task" → Opens task creation form
- "Check bills" → Runs bill reminder check
- "What's due?" → Lists upcoming tasks/bills

---

## Implementation Order

### Phase 3A: Core Task Management (Week 1)

1. ✅ `LifeOSTask` model + API
2. ✅ Enhance `life_os.create_task` action
3. ✅ Enhance `life_os.update_task_status` action
4. ✅ Basic tasks UI (kanban board)
5. ✅ Test: Create task via Otto → See in UI

### Phase 3B: Bill Reminders (Week 2)

1. ✅ `Bill` model + API
2. ✅ `BillReminderSkill` in Otto
3. ✅ Bill reminder task type
4. ✅ Bills UI page
5. ✅ Test: Create bill → Otto creates reminder task → Task appears

### Phase 3C: Calendar (Week 3)

1. ✅ `CalendarEvent` model + API
2. ✅ `calendar.create_event` action
3. ✅ Calendar UI page
4. ✅ Test: Create event via Otto → See in calendar

### Phase 3D: Integration & Polish (Week 4)

1. ✅ Connect everything together
2. ✅ Add quick actions to Otto Console
3. ✅ Add scheduled bill checks
4. ✅ End-to-end testing

---

## Safety Considerations

All Phase 3 features respect safety tiers:

- **Task creation:** Tier 1 (limited writes)
- **Bill reminders:** Tier 1 (creates tasks, doesn't pay bills)
- **Calendar events:** Tier 2 (sensitive - affects scheduling)
- **Bill payment:** Tier 3 (requires approval - future)

**No financial transactions** in Phase 3 - only reminders and tracking.

---

## Deliverables

When Phase 3 is complete:

1. ✅ `LifeOSTask` model + full CRUD API
2. ✅ `Bill` model + API
3. ✅ `CalendarEvent` model + API
4. ✅ `BillReminderSkill` in Otto
5. ✅ `TaskManagementSkill` in Otto
6. ✅ Enhanced action handlers
7. ✅ Tasks kanban UI
8. ✅ Bills UI
9. ✅ Calendar UI
10. ✅ Quick actions in Otto Console

---

## Success Criteria

**Phase 3 is successful when:**

- ✅ You can create a bill in Life OS
- ✅ Otto automatically creates a reminder task 7 days before due date
- ✅ You can see the task in the kanban board
- ✅ You can mark the task done
- ✅ You can create calendar events via Otto
- ✅ Everything respects safety tiers
- ✅ Test artifacts don't pollute real data

---

**Phase 3 makes Otto actually useful for daily life management.**

