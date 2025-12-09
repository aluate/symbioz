# CONTROL_OTTO_SAFETY.md — Safety Tiers, Permissions, and Guard Rails

**Purpose:** Define safety patterns for Otto before he gains more autonomy and access to sensitive operations.

This document establishes the safety infrastructure that will protect against:
- Unauthorized actions
- Test data pollution
- Runaway loops
- Financial/legal mistakes
- Uncontrolled autonomy

---

## 1. Task Privilege Tiers

All task types must be assigned a privilege tier that determines what permissions are required.

### Tier Definitions

**Tier 0: Safe/Read-Only**
- Examples: `otto.log`, `env_status`, `otto_runs.list`
- No side effects
- No data modification
- Can run automatically

**Tier 1: Limited Writes**
- Examples: `life_os.create_task`, `life_os.log_note`
- Creates non-sensitive records
- No financial/legal implications
- Can run automatically (with logging)

**Tier 2: Sensitive Actions**
- Examples: `life_os.update_task_status`, `calendar.create_event`
- Modifies existing data
- May affect scheduling or workflows
- Requires explicit approval OR trusted source

**Tier 3: Financial/Legal**
- Examples: `bills.mark_paid`, `tax.categorize_transaction`
- Affects financial records
- May have tax/legal implications
- **Requires human approval**

**Tier 4: System/Critical**
- Examples: `infra.deploy`, `schema.migrate`, `config.update`
- Affects system infrastructure
- Irreversible or high-impact
- **Requires explicit human signature**

### Implementation

- Task types must declare their tier in a registry
- Worker checks tier before processing
- Actions above Tier 1 require approval workflow
- Tier 3+ actions pause and notify user

---

## 2. Test Artifact Tagging

All test-created tasks and runs must be clearly tagged to prevent pollution of real data.

### Tagging Format

```json
{
  "meta": {
    "source": "otto_self_test" | "test_script" | "manual_test",
    "discard_after": "2025-12-31",
    "test_id": "optional-test-identifier"
  }
}
```

### Rules

- Test tasks must include `[OTTO_SELF_TEST]` or `[TEST]` in description
- Test tasks cannot trigger reminders or scheduling
- Test tasks are auto-hidden from production UI views
- Test runs are excluded from analytics/reporting
- Optional: Auto-cleanup of test artifacts after expiration

---

## 3. Retry and Backoff Logic

Tasks must have retry limits to prevent infinite loops.

### Retry Metadata

Add to `OttoTask` model:
- `retries` (int, default 0)
- `max_retries` (int, default 3)
- `last_error` (text, nullable)
- `next_retry_at` (datetime, nullable)

### Backoff Strategy

- First retry: immediate
- Second retry: 1 minute delay
- Third retry: 5 minute delay
- After max retries: `status="blocked"`, notify user

### Loop Prevention

- Worker checks `retries < max_retries` before processing
- Failed tasks with `retries >= max_retries` are blocked
- Blocked tasks require manual intervention

---

## 4. Action Executor Severity Model

Actions must declare severity levels that determine execution behavior.

### Severity Levels

**Low:**
- Action failure doesn't affect other actions
- Continue with remaining actions
- Example: `otto.log`

**Medium:**
- Action failure should be logged but execution continues
- May affect dependent actions
- Example: `life_os.create_task`

**High:**
- Action failure should halt execution
- Remaining actions are skipped
- Example: `schema.migrate`, `config.update`

**Critical:**
- Action failure is catastrophic
- Rollback if possible
- Alert immediately
- Example: `financial.transfer`, `legal.sign_document`

### Implementation

- Each action type declares its severity
- Executor respects severity when handling errors
- High/Critical actions are logged prominently

---

## 5. Development vs Production Mode

Otto must distinguish between development/testing and production operations.

### Mode Detection

- Environment variable: `OTTO_MODE=dev|prod`
- Default: `dev` for safety
- Production mode requires explicit configuration

### Development Mode Behavior

- Test artifacts are clearly marked
- Actions use sandbox/test data when possible
- More verbose logging
- Lower retry limits
- Can be more permissive with tiers

### Production Mode Behavior

- Stricter tier enforcement
- All actions logged with full context
- Test artifacts rejected
- Higher scrutiny on financial/legal actions

---

## 6. Control Doc Validation

Otto should validate his behavior against control documents to detect drift.

### Validation Points

- When loading a skill, check if control doc has changed
- Before executing high-tier actions, verify against current spec
- Log "implementation mismatch detected" if discrepancies found

### Implementation (Future)

- Store control doc hashes/timestamps
- Compare on skill load
- Report drift in self-test
- Alert if behavior doesn't match spec

---

## 7. Approval Workflow

High-tier actions require explicit approval before execution.

### Approval States

- `pending_approval` - Action created, waiting for approval
- `approved` - Human approved, ready to execute
- `rejected` - Human rejected, task marked as blocked
- `expired` - Approval timeout (e.g., 24 hours)

### Approval Mechanism

- Worker detects Tier 3+ actions
- Sets task `status="pending_approval"`
- Notifies user (via console, email, etc.)
- User approves/rejects via API or UI
- Worker only processes approved tasks

---

## 8. Rate Limiting and Panic Switch

Prevent runaway behavior with limits and kill switches.

### Rate Limits

- Max actions per run: 10 (configurable)
- Max runs per hour: 100 (configurable)
- Max tasks created per minute: 5 (configurable)

### Panic Detection

Worker monitors:
- Task creation rate
- Action execution rate
- Error rate
- If thresholds exceeded → auto-pause

### Kill Switch

- Environment variable: `OTTO_ENABLED=false`
- Worker checks on startup and each cycle
- If disabled, worker stops processing
- Can be toggled without restarting services

---

## 9. Pre-flight Checks

Setup scripts and Otto must verify prerequisites before proceeding.

### Required Checks

- Python installed and version >= 3.8
- pip installed
- Node.js installed (if frontend needed)
- npm installed (if frontend needed)
- Database accessible
- Required environment variables set

### Failure Handling

- Clear error messages
- Links to installers/documentation
- Otto doctor skill reports missing prerequisites
- Setup scripts fail fast with helpful messages

---

## 10. Financial/Legal Action Safeguards

Special rules for actions affecting financial or legal data.

### Required Safeguards

- **Summary only** - Otto can analyze and recommend
- **Human approval required** - No automatic execution
- **Confirmation required** - User must explicitly confirm
- **Audit trail** - All actions logged with full context
- **Reversibility** - Where possible, actions should be reversible

### Action Types Requiring Approval

- `bills.*` - Any bill-related action
- `tax.*` - Any tax-related action
- `financial.*` - Any financial transaction
- `legal.*` - Any legal document action
- `calendar.*` - Calendar modifications (may affect scheduling)

---

## Implementation Priority

### Phase 2.5 (Before Phase 3)

1. ✅ **Task privilege tiers** - Registry and tier checking
2. ✅ **Test artifact tagging** - Meta tags and filtering
3. ✅ **Retry/backoff logic** - Prevent infinite loops
4. ✅ **Rate limiting** - Basic limits on actions/runs
5. ✅ **Kill switch** - Environment variable toggle

### Phase 3 (With new features)

6. ⏳ **Approval workflow** - For Tier 3+ actions
7. ⏳ **Severity model** - Action executor enhancements
8. ⏳ **Control doc validation** - Drift detection
9. ⏳ **Dev/prod mode** - Environment separation

### Phase 4+ (As needed)

10. ⏳ **Financial safeguards** - Special handling for sensitive data
11. ⏳ **Panic detection** - Advanced runaway prevention
12. ⏳ **Sandbox mode** - Isolated test environment

---

## Files to Create/Update

1. `apps/life_os/backend/otto/safety.py` - Safety tier registry and checks
2. `apps/life_os/backend/models.py` - Add retry fields to OttoTask
3. `apps/life_os/backend/worker/otto_worker.py` - Add tier checking, retry logic, rate limits
4. `apps/life_os/backend/otto/actions.py` - Add severity model
5. `apps/life_os/backend/otto_tasks.py` - Add approval workflow endpoints

---

**This safety infrastructure must be in place before Otto gains access to:**
- Email/calendar integration
- Financial data
- Tax categorization
- Bill payment
- Legal document processing

**Better to build the guard rails now than retrofit them later.**

