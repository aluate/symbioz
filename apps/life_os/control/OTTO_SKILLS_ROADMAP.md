# Otto Skills Roadmap for Life OS

**Purpose:** Comprehensive list of skills Otto needs to fulfill the Life OS vision

**Last Updated:** January 2025

---

## Current Skills (Already Implemented)

✅ **bill_reminder** - Monitors bills and creates reminder tasks  
✅ **env_status** - Diagnoses environment and dependency status  
✅ **self_test** - Tests Otto's own functionality  
✅ **otto_runs** - Manages Otto run history  
✅ **repo_audit** - Audits repository structure  
✅ **repo_lister** - Lists repository contents  
✅ **symbioz** - Game-related skill (not Life OS specific)

---

## Required Skills for Life OS Vision

### Phase 1: Core Task Management (Priority: HIGH)

#### 1. **TaskManagementSkill** ⚠️ NEEDED
**Purpose:** Manage Life OS tasks (create, update, list, filter, summarize)

**Task Types:**
- `life_os.create_task`
- `life_os.list_tasks`
- `life_os.update_task`
- `life_os.delete_task`
- `life_os.summarize_tasks`
- `life_os.find_overdue`
- `life_os.find_by_category`
- `life_os.find_by_assignee`

**Actions:**
- `life_os.create_task` (already exists, enhance)
- `life_os.update_task_status` (already exists, enhance)
- `life_os.update_task` (new - update any field)
- `life_os.delete_task` (new)

**Safety Tier:** Tier 1 (limited writes, non-sensitive)

**Status:** Partially implemented (actions exist, skill missing)

---

### Phase 2: Calendar Integration (Priority: HIGH)

#### 2. **CalendarSkill** ⚠️ NEEDED
**Purpose:** Manage calendar events and reminders

**Task Types:**
- `calendar.create_event`
- `calendar.list_events`
- `calendar.update_event`
- `calendar.delete_event`
- `calendar.find_upcoming`
- `calendar.find_conflicts`
- `calendar.create_reminder`

**Actions:**
- `calendar.create_event` (needs implementation)
- `calendar.update_event` (needs implementation)
- `calendar.delete_event` (needs implementation)

**Safety Tier:** Tier 2 (sensitive - affects scheduling)

**Future:** Google Calendar sync

---

### Phase 3: Financial Tracking (Priority: MEDIUM)

#### 3. **BillManagementSkill** ⚠️ NEEDED
**Purpose:** Manage bills (create, update, mark paid, track history)

**Task Types:**
- `bills.create_bill`
- `bills.list_bills`
- `bills.update_bill`
- `bills.mark_paid`
- `bills.find_upcoming`
- `bills.find_overdue`
- `bills.summarize_bills`

**Actions:**
- `bills.create_bill` (needs implementation)
- `bills.update_bill` (needs implementation)
- `bills.mark_paid` (needs implementation)

**Safety Tier:** Tier 1 (tracking only, no payments)

**Note:** `BillReminderSkill` exists but only creates reminders. This skill manages bills themselves.

---

#### 4. **IncomeTrackingSkill** ⚠️ NEEDED
**Purpose:** Track income sources and amounts

**Task Types:**
- `income.create_income`
- `income.list_income`
- `income.update_income`
- `income.summarize_income`
- `income.by_period` (monthly, quarterly, yearly)

**Actions:**
- `income.create_income` (needs implementation)
- `income.update_income` (needs implementation)

**Safety Tier:** Tier 1 (tracking only)

---

#### 5. **TransactionSkill** ⚠️ NEEDED
**Purpose:** Track and categorize transactions (future: import from bank)

**Task Types:**
- `transactions.create_transaction`
- `transactions.list_transactions`
- `transactions.categorize_transaction`
- `transactions.summarize_by_category`
- `transactions.import_from_bank` (future)

**Actions:**
- `transactions.create_transaction` (needs implementation)
- `transactions.update_transaction` (needs implementation)
- `transactions.categorize_transaction` (needs implementation)

**Safety Tier:** Tier 1 (tracking only)

**Future:** Bank import integration

---

### Phase 4: Tax Brain Integration (Priority: MEDIUM)

#### 6. **TaxBrainSkill** ⚠️ NEEDED
**Purpose:** Integrate with Tax Brain module for tax categorization and reporting

**Task Types:**
- `tax.categorize_transaction`
- `tax.generate_report`
- `tax.find_deductions`
- `tax.summarize_by_category`
- `tax.export_for_accountant`

**Actions:**
- `tax.categorize_transaction` (needs implementation)
- `tax.update_category` (needs implementation)

**Safety Tier:** Tier 1 (read-only categorization, no filing)

**Note:** Tax Brain module exists in `apps/life_os/backend/tax/` - this skill should use it

---

### Phase 5: Communication & Scanning (Priority: LOW - Future)

#### 7. **EmailScanSkill** ⚠️ NEEDED (Future)
**Purpose:** Scan emails for todos, bills, appointments

**Task Types:**
- `email.scan_inbox`
- `email.extract_todos`
- `email.extract_bills`
- `email.extract_appointments`

**Actions:**
- `life_os.create_task` (from email todos)
- `bills.create_bill` (from email bills)
- `calendar.create_event` (from email appointments)

**Safety Tier:** Tier 2 (reads personal email)

**Future:** Gmail API integration

---

#### 8. **TextScanSkill** ⚠️ NEEDED (Future)
**Purpose:** Scan text messages for todos and reminders

**Task Types:**
- `text.scan_messages`
- `text.extract_todos`
- `text.extract_reminders`

**Actions:**
- `life_os.create_task` (from text todos)

**Safety Tier:** Tier 2 (reads personal messages)

**Future:** SMS/WhatsApp integration

---

### Phase 6: Reporting & Analytics (Priority: LOW)

#### 9. **ReportingSkill** ⚠️ NEEDED
**Purpose:** Generate reports and summaries across Life OS data

**Task Types:**
- `report.daily_summary`
- `report.weekly_summary`
- `report.monthly_summary`
- `report.financial_summary`
- `report.task_summary`
- `report.calendar_summary`

**Actions:**
- None (read-only reporting)

**Safety Tier:** Tier 0 (read-only)

---

#### 10. **AnalyticsSkill** ⚠️ NEEDED (Future)
**Purpose:** Analyze patterns and provide insights

**Task Types:**
- `analytics.spending_patterns`
- `analytics.task_completion_rate`
- `analytics.bill_payment_history`
- `analytics.calendar_insights`

**Actions:**
- None (read-only analysis)

**Safety Tier:** Tier 0 (read-only)

---

### Phase 7: Automation & Scheduling (Priority: MEDIUM)

#### 11. **SchedulingSkill** ⚠️ NEEDED
**Purpose:** Automatically schedule recurring tasks and reminders

**Task Types:**
- `schedule.create_recurring_task`
- `schedule.create_recurring_bill_reminder`
- `schedule.create_recurring_event`
- `schedule.list_recurring_items`
- `schedule.update_recurring_item`

**Actions:**
- `life_os.create_task` (for recurring tasks)
- `calendar.create_event` (for recurring events)
- `otto.create_recurring_task` (for OttoTask scheduling)

**Safety Tier:** Tier 1 (creates tasks/events, doesn't execute them)

---

#### 12. **ReminderSkill** ⚠️ NEEDED
**Purpose:** Send reminders for tasks, bills, events

**Task Types:**
- `reminder.create_reminder`
- `reminder.send_reminders`
- `reminder.list_upcoming_reminders`

**Actions:**
- `reminder.send_notification` (future: email, SMS, push)

**Safety Tier:** Tier 1 (notifications only)

**Future:** Email, SMS, push notification integration

---

### Phase 8: Integration Skills (Priority: LOW - Future)

#### 13. **GoogleCalendarSyncSkill** ⚠️ NEEDED (Future)
**Purpose:** Sync with Google Calendar

**Task Types:**
- `google_calendar.sync`
- `google_calendar.import_events`
- `google_calendar.export_events`

**Actions:**
- `calendar.create_event` (from Google Calendar)
- `calendar.update_event` (sync to Google Calendar)

**Safety Tier:** Tier 2 (external API access)

---

#### 14. **BankImportSkill** ⚠️ NEEDED (Future)
**Purpose:** Import transactions from bank accounts

**Task Types:**
- `bank.import_transactions`
- `bank.list_accounts`
- `bank.sync_account`

**Actions:**
- `transactions.create_transaction` (from bank import)

**Safety Tier:** Tier 3 (financial data access - requires approval)

---

## Skill Implementation Priority

### Immediate (Phase 1-2)
1. ✅ **TaskManagementSkill** - Core functionality
2. ✅ **CalendarSkill** - Essential for scheduling

### Short-term (Phase 3)
3. ✅ **BillManagementSkill** - Enhance bill tracking
4. ✅ **IncomeTrackingSkill** - Complete financial picture
5. ✅ **TransactionSkill** - Transaction tracking

### Medium-term (Phase 4-5)
6. ✅ **TaxBrainSkill** - Tax integration
7. ✅ **SchedulingSkill** - Automation
8. ✅ **ReminderSkill** - Notifications

### Long-term (Phase 6-8)
9. ✅ **ReportingSkill** - Analytics
10. ✅ **EmailScanSkill** - Communication
11. ✅ **TextScanSkill** - Communication
12. ✅ **GoogleCalendarSyncSkill** - External integration
13. ✅ **BankImportSkill** - External integration
14. ✅ **AnalyticsSkill** - Advanced insights

---

## Action Types Needed

### Already Implemented
- ✅ `life_os.create_task`
- ✅ `life_os.update_task_status`
- ✅ `otto.log`

### Need Implementation
- ⚠️ `life_os.update_task` (update any field)
- ⚠️ `life_os.delete_task`
- ⚠️ `calendar.create_event`
- ⚠️ `calendar.update_event`
- ⚠️ `calendar.delete_event`
- ⚠️ `bills.create_bill`
- ⚠️ `bills.update_bill`
- ⚠️ `bills.mark_paid`
- ⚠️ `income.create_income`
- ⚠️ `income.update_income`
- ⚠️ `transactions.create_transaction`
- ⚠️ `transactions.update_transaction`
- ⚠️ `transactions.categorize_transaction`
- ⚠️ `tax.categorize_transaction`
- ⚠️ `reminder.send_notification` (future)

---

## Summary

**Total Skills Needed:** 14 skills  
**Currently Implemented:** 1 (bill_reminder - partial)  
**High Priority:** 2 skills (TaskManagement, Calendar)  
**Medium Priority:** 5 skills (Bills, Income, Transactions, Tax, Scheduling, Reminders)  
**Low Priority:** 6 skills (Reporting, Email, Text, Google Calendar, Bank, Analytics)

**Next Steps:**
1. Implement `TaskManagementSkill` (highest priority)
2. Implement `CalendarSkill` (high priority)
3. Enhance existing `BillReminderSkill` with full bill management
4. Implement remaining action handlers in `apps/life_os/backend/otto/actions.py`

