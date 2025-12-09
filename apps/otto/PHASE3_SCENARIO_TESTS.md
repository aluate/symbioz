# Phase 3 Scenario Tests

**Purpose:** Realistic end-to-end test scenarios to verify Otto's skills work together correctly

**Status:** Test scenarios defined - ready for implementation

---

## Scenario A: Simple Bill & Reminder Loop

**Goal:** Verify bill creation, recurring setup, and reminder generation work together

### Steps

1. **Create a bill**
   - Name: "Power bill"
   - Amount: "$150"
   - Due date: 15th of current month
   - Category: "utilities"
   - Payee: "Power Company"

2. **BillManagementSkill creates it**
   - Verify bill exists in database
   - Verify all fields are correct

3. **SchedulingSkill sets recurring monthly**
   - Mark bill as recurring
   - Set recurrence_frequency to "monthly"
   - Calculate next_due_date

4. **ReminderSkill triggers reminders**
   - 7 days before due date
   - 1 day before due date
   - Day-of reminder

5. **Verify**
   - Bill exists with correct data
   - Recurring flag is set
   - Reminders are scheduled correctly
   - Worker processes reminders without creating duplicate tasks

### Expected Results

- Bill created successfully
- Recurring bill has next_due_date set
- Three reminder tasks created (7 days, 1 day, day-of)
- Reminders appear in Otto console/logs
- No duplicate bills or reminders

---

## Scenario B: Income + Transactions + TaxBrainSkill

**Goal:** Verify financial tracking and tax categorization work together

### Steps

1. **Create income entries**
   - Paycheck: $3000, monthly, category "wages"
   - Side gig: $500, one-time, category "self_employment"
   - Investment: $200, quarterly, category "investment"

2. **Create transactions**
   - Groceries: -$150, vendor "Grocery Store", no category
   - Truck fuel: -$80, vendor "Gas Station", no category
   - Business tools: -$250, vendor "Home Depot", no category
   - Restaurant meal: -$45, vendor "Restaurant", no category

3. **Run TaxBrainSkill to categorize**
   - Categorize "Grocery Store" → "personal" (not deductible)
   - Categorize "Gas Station" → "business_expense" (deductible)
   - Categorize "Home Depot" → "business: tools" (deductible)
   - Categorize "Restaurant" → "personal" (not deductible)

4. **Generate tax summary**
   - Run TaxBrainSkill.generate_report for current year
   - Get summary by category
   - Find deductions

5. **Verify**
   - No overwriting of original transaction text
   - Categories look sane (business vs personal)
   - Tax summary shows correct totals
   - Deductions are identified correctly
   - No Tier 3 magic (no "file your taxes now" behavior)

### Expected Results

- All income entries created
- All transactions created
- TaxBrainSkill categorizes transactions correctly
- Tax summary shows:
  - Total income: $3000 (or $3700 if including side gig)
  - Business deductions: $330 (fuel + tools)
  - Personal expenses: $195 (groceries + restaurant)
- No unauthorized tax filing actions

---

## Scenario C: Task → Calendar → Reminders Chain

**Goal:** Verify task creation, calendar event creation, and reminder scheduling work together

### Steps

1. **Create a Life OS task**
   - Title: "Go to Audrey's concert"
   - Description: "Audrey's school concert at 7pm"
   - Due date: Tomorrow at 7:00 PM
   - Priority: "high"
   - Category: "family"

2. **CalendarSkill creates event**
   - Extract date/time from task
   - Create calendar event with:
     - Title: "Go to Audrey's concert"
     - Start time: Tomorrow 7:00 PM
     - End time: Tomorrow 9:00 PM (estimated)
     - Category: "family"
     - Location: "School auditorium" (if provided)

3. **SchedulingSkill generates reminders**
   - Week before (if applicable)
   - Day before
   - Day-of (morning reminder)

4. **ReminderSkill handles them**
   - Check for upcoming reminders
   - Send/log reminders at appropriate times

5. **Verify**
   - Task created successfully
   - Calendar event created and linked to task
   - Reminders scheduled correctly
   - Worker processes reminders
   - No duplicate events or reminders

### Expected Results

- Task created with all fields
- Calendar event created with correct date/time
- Three reminders scheduled (week, day, day-of)
- Reminders appear in logs/console
- Task and event are linked (via description or notes)

---

## Test Execution Notes

### Prerequisites

- Life OS backend running on port 8000
- Otto API running on port 8001
- Otto worker running
- Database initialized with all models

### Running Tests

These are **manual scenario tests** to verify end-to-end behavior. They should be run:

1. **Before Phase 3 completion** - Verify skills work together
2. **After any skill changes** - Ensure no regressions
3. **Before adding new features** - Baseline verification

### Test Data Cleanup

After running tests, clean up test data:
- Delete test bills
- Delete test income entries
- Delete test transactions
- Delete test tasks
- Delete test calendar events

Or use test tags/metadata to identify and auto-delete test data.

---

## Success Criteria

All scenarios pass if:

✅ **No errors** in Otto worker logs  
✅ **No duplicate** records created  
✅ **No unauthorized** Tier 3 actions  
✅ **Data integrity** maintained (no overwrites)  
✅ **Reminders** appear in expected places  
✅ **Tax categorization** is accurate  
✅ **Calendar events** match task dates/times  

---

**Next Steps:** Implement these scenarios as automated tests or manual test scripts.

