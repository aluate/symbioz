# Phase 3 Implementation Plan

**Status:** Ready to implement  
**Prerequisites:** Phase 2 + Safety complete ✅

---

## Quick Start: Test First

Before implementing Phase 3, verify Phase 2 works:

1. **Run quick test:** See `QUICK_TEST_PHASE2_SAFETY.md`
2. **Or ask Otto:** "Run a self-test" in Otto Console
3. **Verify:** All systems operational

---

## Phase 3 Implementation Order

### Week 1: Core Task Management

**Goal:** Otto can create and manage Life OS tasks

1. **LifeOSTask Model** (`apps/life_os/backend/models.py`)
   - Add `LifeOSTask` class with all fields
   - Migration for `life_os_tasks` table

2. **Life OS Tasks API** (`apps/life_os/backend/life_os_tasks.py`)
   - Full CRUD endpoints
   - Filtering by status, assignee, category, due_date

3. **Enhance Actions** (`apps/life_os/backend/otto/actions.py`)
   - Update `life_os.create_task` to create `LifeOSTask`
   - Update `life_os.update_task_status` to update `LifeOSTask`
   - Add `life_os.list_tasks` action

4. **Tasks UI** (`apps/life_os/frontend/app/tasks/page.tsx`)
   - Kanban board (todo / in_progress / done)
   - Create task form
   - Task cards with drag-and-drop (future)

5. **Test:**
   - Create task via Otto → See in UI
   - Update task status → UI updates

---

### Week 2: Bill Reminders

**Goal:** Otto automatically creates reminder tasks for bills

1. **Bill Model** (`apps/life_os/backend/models.py`)
   - Add `Bill` class
   - Migration for `bills` table

2. **Bills API** (`apps/life_os/backend/bills.py`)
   - Full CRUD endpoints
   - Query by due_date, paid status

3. **BillReminderSkill** (`apps/otto/otto/skills/bill_reminder.py`)
   - Task type: `life_os.bill_reminder`
   - Queries bills due in next 7 days
   - Creates `life_os.create_task` actions

4. **Bills UI** (`apps/life_os/frontend/app/bills/page.tsx`)
   - List of bills
   - Upcoming/overdue highlighted
   - Mark paid button
   - Create bill form

5. **Scheduled Task** (optional)
   - Create recurring `OttoTask` that runs daily
   - Calls `life_os.bill_reminder` skill

6. **Test:**
   - Create bill with due date 5 days out
   - Otto creates reminder task
   - Task appears in kanban board

---

### Week 3: Calendar Integration

**Goal:** Otto can create calendar events

1. **CalendarEvent Model** (`apps/life_os/backend/models.py`)
   - Add `CalendarEvent` class
   - Migration for `calendar_events` table

2. **Calendar API** (`apps/life_os/backend/calendar.py`)
   - Full CRUD endpoints
   - Query by date range

3. **Calendar Action** (`apps/life_os/backend/otto/actions.py`)
   - Add `calendar.create_event` handler
   - Safety: Tier 2

4. **Calendar UI** (`apps/life_os/frontend/app/calendar/page.tsx`)
   - Calendar view (month/week/day)
   - Create event form
   - Event details

5. **Test:**
   - Create event via Otto → See in calendar
   - Create event via UI → Otto can query it

---

### Week 4: Integration & Polish

**Goal:** Everything works together smoothly

1. **Quick Actions in Otto Console**
   - "Create task" button
   - "Check bills" button
   - "What's due?" query

2. **Scheduled Bill Checks**
   - Daily `OttoTask` for bill reminders
   - Runs automatically via worker

3. **End-to-End Testing**
   - Full workflow: Bill → Reminder → Task → Done
   - Calendar event → Task → Done
   - Multiple users/assignees

4. **Documentation**
   - Update `OTTO_CONTEXT.md` with new skills
   - User guide for Life OS features

---

## Files to Create/Update

### Backend

- `apps/life_os/backend/models.py` - Add LifeOSTask, Bill, CalendarEvent
- `apps/life_os/backend/life_os_tasks.py` (NEW)
- `apps/life_os/backend/bills.py` (NEW)
- `apps/life_os/backend/calendar.py` (NEW)
- `apps/life_os/backend/otto/actions.py` - Enhance existing, add calendar
- `apps/life_os/backend/main.py` - Add new routers

### Otto

- `apps/otto/otto/skills/bill_reminder.py` (NEW)
- `apps/otto/otto/skills/task_management.py` (NEW)
- `apps/otto/otto/skills/__init__.py` - Register new skills

### Frontend

- `apps/life_os/frontend/app/tasks/page.tsx` (NEW)
- `apps/life_os/frontend/app/bills/page.tsx` (NEW)
- `apps/life_os/frontend/app/calendar/page.tsx` (NEW)
- `apps/life_os/frontend/app/otto/page.tsx` - Add quick actions

---

## Safety Reminders

- ✅ All task types registered in safety tier registry
- ✅ Bill reminders: Tier 1 (safe)
- ✅ Calendar events: Tier 2 (sensitive)
- ✅ No financial transactions (Tier 3+ requires approval)
- ✅ Test artifacts tagged and filtered

---

**Ready to start? Begin with Phase 3A: Core Task Management!**

