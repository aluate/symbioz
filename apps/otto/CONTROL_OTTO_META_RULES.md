# CONTROL_OTTO_META_RULES.md — Meta-Governance for Otto

**Purpose:** Hard rules that prevent architectural drift, feature bloat, and incoherent behavior as Otto scales.

**Status:** 🔒 LOCKED — These rules override all other guidance when conflicts arise.

**Last Updated:** January 2025

---

## ⚠️ CRITICAL: This Document is Primary Governance

**Order of Authority:**
1. This document (`CONTROL_OTTO_META_RULES.md`)
2. Top-level architecture docs (`OTTO_ARCHITECTURE_OVERVIEW.md`)
3. Control documents under `/control/`
4. App-specific control and context files
5. Code comments
6. Inference (lowest priority)

**If something conflicts, higher-order doc wins. Outdated code is the error, not the doc.**

---

## 1. Single Source of Truth Hierarchy

### ORDER OF AUTHORITY (Explicit Table)

| Priority | Document Type | Example | Authority Level |
|----------|---------------|---------|-----------------|
| 1 | Meta-rules (this doc) | `CONTROL_OTTO_META_RULES.md` | **Highest** |
| 2 | Architecture overview | `OTTO_ARCHITECTURE_OVERVIEW.md` | High |
| 3 | Control docs | `apps/otto/CONTROL_OTTO.md` | High |
| 4 | Phase control docs | `apps/life_os/control/CONTROL_OTTO_PHASE2.md` | Medium-High |
| 5 | App-specific control | `apps/life_os/control/CONTROL.md` | Medium |
| 6 | Code comments | Inline documentation | Low |
| 7 | Inference | Patterns in code | **Lowest** |

**Rule:** If something conflicts, **higher-order doc wins**. Cursor must treat outdated code as the error, not the doc.

---

## 2. No Cross-Project Osmosis

**CRITICAL:** Cursor must treat every project as isolated unless explicitly told otherwise.

### Isolation Rules

**Projects are isolated unless:**
- A control doc explicitly says to share logic, OR
- Frat tags a pattern as "shared architecture"

**Shared modules:**
- Live in `/shared/` or `/lib/`
- Everything else stays siloed

### Examples of What NOT to Do

❌ **Otto's auth logic does NOT bleed into SMB**  
❌ **Wedding site's kanban does NOT bleed into Life OS**  
❌ **Cabinet spec sheet flows do NOT bleed into meal planning logic**  
❌ **Life OS task management does NOT automatically apply to CateredByMe**

**Unless explicitly authorized in a control doc.**

---

## 3. Control Docs Must Stay 1:1 With Live Code

**Any deviation between doc and code is treated as a defect and must be reconciled before continuing a phase.**

### Rules

- If Cursor implements something not in control docs → **Must request doc update or fix implementation**
- If Cursor misses something in control docs → **Must fix implementation**
- Before phase completion → **Verify doc/code alignment**

**No exceptions.**

---

## 4. Every Phase Must End in Four Things

**When Cursor says "Phase X is complete," it must include:**

1. **Implementation Summary**
   - What was built
   - What files changed
   - What APIs were added/modified

2. **DAC Report**
   - Frat's review completed
   - All DAC fixes applied
   - Documented what was fixed and why

3. **Testing Validation**
   - Checklist showing PASS/FAIL
   - Test coverage documented
   - Edge cases tested

4. **Control Doc Updates**
   - New architecture reflected
   - New behavior documented
   - Phase status updated

**No "Phase Complete" until these four things exist.**

---

## 5. Skill Additions Require Explicit Definition

**Do NOT create skills because:**
- "it looked useful"
- "we used something similar over there"
- "it would be nice to have"

### Required Before Any New Skill

1. **Control doc update** — Document the skill's purpose and scope
2. **Action schema definition** — Explicit input/output schemas
3. **Safety tier assignment** — Must declare tier (see Safety Tiers below)
4. **Explicit recording:**
   - Input schema
   - Expected output
   - Failure behavior
   - Risks

**Skills with no safety tier are automatically rejected.**

---

## 6. Safety Tiers (Formal Table)

**Default Tier is 1. If no tier is declared, Otto rejects the action.**

| Tier | Capability                                      | Approval Required                           | Examples                                    |
| ---- | ----------------------------------------------- | ------------------------------------------- | ------------------------------------------- |
| 0    | Logging only, read-only operations              | No                                          | `otto.log`, `life_os.list_tasks`           |
| 1    | Internal DB writes (tasks, runs, notes)        | No                                          | `life_os.create_task`, `life_os.update_task_status` |
| 2    | Financial state, calendar, scheduling, tax data | Visible runs + clear logging (auto-execute) | `income.create_income`, `transactions.create_transaction`, `bills.mark_paid`, `calendar.create_event` |
| 3    | Code changes, infrastructure, critical financial | Human confirmation + signed control confirm | `infra.deploy_project`, `schema.migrate` |

### Action Schema Must Include Tier

```json
{
  "type": "calendar.create_event",
  "tier": 2,
  "payload": {
    "title": "Meeting",
    "start_time": "2025-01-15T10:00:00Z"
  }
}
```

**If `tier` is missing, action is rejected.**

---

## 7. Human Approval Protocol

**When skill emits `approval_required`, worker MUST:**

1. Set `OttoTask.status = "blocked"`
2. Add text in `OttoRun`:
   - Why blocked
   - What action needs approval
   - What will happen if approved
3. Display in console with:
   - Approve button
   - Reject button
   - Snooze option (future)

**Worker does NOT proceed until approval is given.**

---

## 8. Test Tagging

**All automated tests or self-tests must include:**

```json
{
  "meta": {
    "source": "otto_self_test",
    "is_test": true
  }
}
```

### Worker Rules for Test Tasks

- **Never reschedule them**
- **Never treat them as real events**
- **Never create reminders for them**
- **Auto-delete after X days** (configurable, default 7 days)

**Test tasks must be clearly marked to prevent pollution of real data.**

---

## 9. Rate Limits & Runaway Prevention

**Cursor will not invent these himself unless told explicitly.**

### Required Limits

- **Max N OttoTasks runnable per sweep** (default: 2)
- **Max tasks created per hour by worker** (default: 10)
- **Max time worker can spend per loop** (default: 30 seconds)
- **Max actions per OttoRun execution** (default: 5)

### If Limits Breached

Worker must:
1. **Halt immediately**
2. **Log the breach**
3. **Mark system as "danger_mode"**
4. **Send notification to UI**
5. **Require manual reset**

**Even a 2-per-loop cap is enough for now. Safety over speed.**

---

## 10. Phase Naming Convention

**Force Cursor to put the Phase name, doc reference, and deliverables IN the code he implements.**

### Required Format

```python
# Phase 2 — CONTROL_OTTO_PHASE2.md
# Implements:
# - OttoTask model
# - task worker
# - action executor
```

**Same in PR messages or change summaries.**

**Every file/change must reference:**
- Phase number
- Control doc name
- What it implements

---

## 11. "Cursor, Don't Hallucinate the Ask"

**If Cursor wants to extend requirements, he must output a "Proposal Block" instead of implementing it.**

### Proposal Block Format

```markdown
## Proposal From Cursor

**Reasoning:** [Why this change is suggested]

**Suggested change:** [What would be added/modified]

**Risk:** [What could go wrong]

**Requires approval from:** [Karl or Frat]

**Files affected:** [List of files]

**Estimated impact:** [Low/Medium/High]
```

**Cursor waits for approval. ZERO self-initiated architecture changes.**

---

## 12. Rule A: Otto Never Modifies Repo Code

**🔥 CRITICAL RULE**

**Otto never modifies repo code without explicit human instruction.**

Even if Otto thinks it's a "fix."

### Only Allowed

- Structured proposals (see Proposal Block above)
- Control doc edits (with approval)
- Recommendations (read-only suggestions)

**Execution only with explicit signature/approval.**

---

## 13. Rule B: Control Doc > Cursor's Interpretation

**🔥 CRITICAL RULE**

**If conflict between control doc and code patterns:**

- Cursor must align implementation to the docs
- NOT the code patterns he sees elsewhere
- Outdated code is the error, not the doc

**Control docs are the source of truth. Always.**

---

## 14. Skill Registry Requirements

**Every skill must be registered with:**

1. **Name** — Unique identifier
2. **Description** — What it does
3. **Task types** — What task types it handles
4. **Actions emitted** — What actions it can create
5. **Safety tier** — Default tier for actions
6. **Dependencies** — What it needs to run
7. **Health check** — How to verify it's working

**Skills not in registry are not discoverable and cannot be used.**

---

## 15. Action Schema Validation

**All actions must validate against schema before execution.**

### Required Schema Fields

```json
{
  "type": "string (required, namespaced)",
  "tier": "number (required, 0-3)",
  "payload": "object (required)",
  "requires_approval": "boolean (optional, default: false if tier < 2)",
  "idempotent": "boolean (optional, default: false)"
}
```

**Invalid actions are rejected before execution.**

---

## 16. Documentation Requirements

**Every phase completion must update:**

1. **Control docs** — Architecture and behavior
2. **Status files** — Phase status
3. **Changelog** — What changed
4. **API docs** — New endpoints/schemas
5. **Testing docs** — Test coverage and results

**Incomplete documentation = incomplete phase.**

---

## 17. Error Handling Standards

**All errors must:**

1. **Log with context** — What was attempted, what failed, why
2. **Set appropriate status** — `error`, `blocked`, `retry`
3. **Provide actionable message** — What user can do
4. **Never expose secrets** — Redact in all logs
5. **Include error code** — For programmatic handling

**Silent failures are not allowed.**

---

## 18. Idempotency Requirements

**Actions should be idempotent when possible.**

### Idempotent Actions

- Can be run multiple times safely
- Same input = same output
- No side effects from re-running

### Non-Idempotent Actions

- Must be marked as such
- Require explicit confirmation if re-run
- Log warnings if attempted multiple times

**Prefer idempotent designs.**

---

## 19. Secret Management (General)

**NEVER:**
- Log secrets in plain text
- Commit secrets to repo
- Expose secrets in error messages
- Store secrets in code

**ALWAYS:**
- Use environment variables
- Redact in all logs
- Use secret management tools when available
- Validate secret presence before use

**See Section 22 (Data & Secrets Management) for Otto-specific rules.**

---

## 20. Testing Requirements

**Before phase completion:**

1. **Unit tests** — Core logic covered
2. **Integration tests** — APIs work end-to-end
3. **Safety tests** — Tier enforcement works
4. **Error handling tests** — Failures handled gracefully
5. **Documentation** — Test coverage reported

**No phase is complete without passing tests.**

---

## 21. Memory Governance

**All long-term memory must follow `CONTROL_OTTO_LONG_TERM_MEMORY.md`.**

### Memory Tiers

Memory writes are categorized by impact:

| Tier | Description | Approval Required | Examples |
|------|-------------|-------------------|-----------|
| **M0** | Obvious recall facts (no future effect) | **No** | "Home zip code = X", "Karl prefers military time", "Tiffany blue is brand color" |
| **M1** | Preferences that influence task creation | **Yes** | "Notify 1 week, 1 day, and day-of for events", "Round door height up before calc" |
| **M2** | Memories that trigger autonomous actions | **Yes (Strong)** | "When 'RFQ' appears, create task", "Finance actions require approval" |

**Tier-0 (M0) memories:**
- Can be written automatically (no approval)
- Must be obvious facts with no external effect
- Only shape outputs, don't trigger actions
- Still logged in `OttoRun` for audit trail

**Tier-1 (M1) and Tier-2 (M2) memories:**
- Require `memory.update_proposal` + human approval
- Must go through approval workflow

### Memory Write Rules

**Otto cannot write Tier-1 or Tier-2 memory silently.**

Memory additions must come from:
- **User instruction** — Explicit "remember that..." command
- **Explicit `memory.update_proposal`** — With human approval (Tier 1 or Tier 2)
- **Automatic (Tier-0 only)** — Obvious facts with no external effect

### Memory Management

Memory entries can be:
- **Viewed** — Via UI or API
- **Edited** — With approval (Tier 2)
- **Deleted** — "Forget this" via UI or API (Tier 2)
- **Exported** — On explicit user command (not automated, not implicit)

### Memory Usage Restrictions

Memory is **never** used to:
- Train external models
- Leave the local environment without explicit export command
- Share with third parties
- Train other AI systems

**Memory stays local and private unless explicitly exported by user.**

### Confidence Score Rules

**Otto cannot increase or decrease `confidence_score` autonomously.**

- Any change to `confidence_score` requires a proposal block + human approval
- No auto-mutation of confidence logic
- No inference heuristics that modify confidence
- No re-scoring logic without approval

**The field exists for future use, but Otto cannot modify it on his own.**

---

## 22. Data & Secrets Management

**No raw secrets or credentials anywhere in code, tasks, runs, or memory.**

### Hard Rules

**NEVER:**
- Hardcode secrets in code
- Commit API keys, tokens, bank credentials, or personal IDs
- Store raw credentials in memory or tasks
- Log secrets in plain text
- Expose credentials in tracebacks or error messages

**ALWAYS:**
- Use environment variables for secrets
- Store only opaque references (e.g., `"gmail_account_1"`, `"gdrive_personal"`, `"tax_file_repo_auth"`)
- Redact in all logs and runs before storage
- Use secret store references (future: encrypted at rest, OS keychain, protected config)

### Secret Reference System

**Otto can reference secrets by name only:**
- `gmail_1`
- `gdrive_personal`
- `stripe_account_prod`
- `tax_file_repo_auth`

**Secrets live:**
- Encrypted at rest
- In a protected storage spot (config file, .env, OS keychain)
- Never appear in DB, logs, tasks, memory

**Key resolution occurs in a secure layer that Otto cannot introspect.**

**Note:** Cursor should NOT build the secret manager now, but ensure future Otto can integrate with one.

### Redaction Requirements

**Logs and runs must automatically redact BEFORE storage:**
- **API keys** — Any field containing "key", "secret", "token", "credential"
- **OAuth tokens** — Token patterns (long alphanumeric strings)
- **Passwords** — Any field named "password", "passwd", "pwd"
- **Banking details** — Account numbers, routing numbers
- **SSN-like patterns** — XXX-XX-XXXX format
- **Personal identifiers** — SSN, driver's license numbers

**Redaction must happen on insert, not after.**

**Implementation:** Regex scrubber for logs (Phase 2.5 mini-task)

### Credential Storage

**Otto can only store:**
- Opaque references: `"gmail_account_1"`, `"stripe_account_prod"`
- Configuration keys: `"STRIPE_API_KEY"` (points to env var, not the value)

**Never the actual credential value.**

**Future:** Secret store integration for encrypted credential management.

---

## 23. No Silent Autonomous Changes

**Any autonomous change Otto makes to user-facing state must be logged, with visibility based on tier.**

### Visibility Requirements by Tier

**Tier 0 & Tier 1 (Silent Maintenance Allowed):**
- **Cosmetic corrections** — Date formatting, tag updates
- **Metadata enrichment** — Adding tags, updating status
- **Status updates** — Marking tasks complete, updating progress
- **Safe re-alignments** — Rescheduling reminders when due date moves (equal or smaller scope)

**These create `OttoRun` records but are marked as:**
```json
{
  "source": "worker",
  "kind": "silent_maintenance",
  "approved": true,
  "tier": 0,
  "actions": [ ... ]
}
```

**UI behavior:**
- Hidden by default (to prevent console noise)
- Visible via debug filter
- Still fully logged for audit trail

**Tier 2+ (Must Be Visible):**
- **Scheduling changes** — Calendar events, recurring tasks
- **Calendar edits** — Creating, updating, deleting events
- **Financial changes** — Bill payments, transaction updates
- **Memory changes** — Tier-1 and Tier-2 memory writes
- **Commit-affecting logic** — Code changes, file modifications

**These must:**
- Show in Otto Console by default
- Display what was done, when, and why
- Require approval for Tier 3

### Bulk Operations Rule

**No "hidden" background migrations, mass edits, or cleanups.**

If Otto wants to do something big, it must:
1. **Emit a proposal** — Describe what will happen
2. **Require approval** — Tier 2 or Tier 3 depending on scope
3. **Show in UI** — User must see what's proposed
4. **Wait for approval** — No execution until approved

### Silent Actions Allowed IF:

**Silent adjustments allowed only if:**
- Equal or smaller in scope (e.g., reschedule reminder when due date moves)
- Does not create NEW action types
- Does not affect finances
- Does not affect calendar dates beyond due_date itself
- Tier 0 or Tier 1 only

### Examples

❌ **Silently updating 100 tasks** → Must propose first  
❌ **Bulk calendar changes** → Must propose first  
❌ **Mass memory updates** → Must propose first  
❌ **Database migrations** → Must propose first  
❌ **Financial changes** → Must be visible + approved  

✅ **Single task creation (Tier 1)** → Silent OK, logged  
✅ **Reschedule reminder (Tier 1)** → Silent OK, logged  
✅ **Update task status (Tier 1)** → Silent OK, logged  
✅ **Tag enrichment (Tier 0)** → Silent OK, logged  
✅ **Logging (Tier 0)** → Silent OK, logged  
✅ **Reading data (Tier 0)** → Silent OK, logged  

**When in doubt, propose. Transparency over speed.**

### Logging Requirements

**Even silent changes must create an `OttoRun` record with:**
- `source="worker"`
- `kind="silent_maintenance"`
- `approved=true` (auto-approved for Tier 0/1)
- `tier` (0 or 1)
- `timestamp`
- `actions` (what was done)

**All changes are logged. Visibility is tier-based.**

---

## Summary: What This Prevents

These rules prevent:

✅ **Runaway feature creep** — No features without explicit definition  
✅ **Fragile architecture** — Control docs enforce structure  
✅ **Incoherent AI behavior** — Clear hierarchy and rules  
✅ **Cross-project contamination** — Explicit isolation  
✅ **Code/doc drift** — 1:1 requirement  
✅ **Unsafe actions** — Tier system enforced  
✅ **Hallucinated features** — Proposal blocks required  
✅ **Uncontrolled scaling** — Rate limits enforced  
✅ **Silent memory writes** — Memory governance enforced  
✅ **Secret exposure** — Data & secrets management enforced  
✅ **Hidden autonomous changes** — Visibility requirements enforced  

---

## How to Use This Document

1. **Cursor must read this first** before any Otto work
2. **Reference in all phase docs** — "See CONTROL_OTTO_META_RULES.md"
3. **Update when patterns emerge** — But changes require approval
4. **Enforce in code** — These aren't suggestions, they're requirements

---

**These rules form the spine for architectural integrity, safety, autonomy scaling, and future business logic.**

**They prevent Cursor from becoming a well-meaning gremlin.**

---

**End of Meta-Rules Document**

