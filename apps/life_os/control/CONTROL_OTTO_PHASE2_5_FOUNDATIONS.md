# CONTROL_OTTO_PHASE2_5_FOUNDATIONS.md  

## Otto Phase 2.5 — Foundations Before More Skills

**Goal:**  

Before Otto gets more skills (or starts touching real-world money, taxes, and calendar flows at scale), we need to fix the foundations:

1. Global household/user context

2. Action schema registry & validator

3. Category/taxonomy governance

4. Schema migrations strategy

5. Decision memory (reasoning logs)

6. Trigger/event engine

This document is authoritative for **Phase 2.5** and is subordinate only to:

- `OTTO_ARCHITECTURE_OVERVIEW.md`

- `apps/otto/CONTROL_OTTO_META_RULES.md`

- `CONTROL_OTTO_LONG_TERM_MEMORY.md` (for memory-specific rules)

No new skills or major features should be added to Otto until Phase 2.5 is complete and DAC'd.

---

## Part A — Global Household/User Context

### A1. Problem

Right now, Otto's skills and actions assume a default user/household (e.g. hardcoded `user_id=1` in TaxBrain) and do not use a canonical context object. That will break:

- multi-user / multi-household support

- preference handling

- tax configuration

- consistent use of timezone/currency

### A2. Design: Household + User Context Models

Add two models in the Life OS backend (`models.py`):

1. **Household**

   - `id` (PK, int)

   - `name` (string)

   - `timezone` (string, e.g. `"America/Los_Angeles"`)

   - `currency` (string, e.g. `"USD"`)

   - `locale` (string, e.g. `"en-US"`)

   - `tax_filing_status` (string; e.g. `"single"`, `"married_joint"`)

   - `tax_year_start` (date; default Jan 1)

   - `primary_user_id` (FK to UserProfile, nullable)

   - `created_at`, `updated_at`

2. **UserProfile**

   - `id` (PK, int)

   - `household_id` (FK → Household.id)

   - `name` (string)

   - `email` (string)

   - `role` (string; e.g. `"primary"`, `"spouse"`, `"dependent"`)

   - `is_active` (bool)

   - `created_at`, `updated_at`

For now, you can default to a single `Household` and single `UserProfile`, but the schema must support more.

### A3. Context Propagation

Introduce a **Context object** used everywhere Otto runs:

```python

class OttoContext(BaseModel):

    household_id: int

    user_id: int

    timezone: str

    currency: str

    locale: str

    tax_year_start: date

    tax_filing_status: str

```

* The **worker**, **API layer**, and **skills** should all receive an `OttoContext` instance.

* When creating `OttoTask`, `OttoRun`, and domain entities (bills, income, transactions, tasks, events), store `household_id` (and `user_id` where appropriate).

**Rule:**

No skill may assume a default `user_id` or `household_id` without going through the context loader.

---

## Part B — Action Schema Registry & Validator

### B1. Problem

Currently, `otto/actions.py` contains hardcoded `if/elif` dispatch for action types and silently treats unknown types as generic "unknown action". There is no global registry of:

* which action types exist

* which handler owns them

* safety tier

* expected payload schema

This makes Otto fragile and hard to extend.

### B2. Design: ACTION_REGISTRY

Create a registry in `apps/life_os/backend/otto/action_registry.py`:

```python

from typing import Callable, Dict, Any, Optional

from pydantic import BaseModel

class ActionSchema(BaseModel):

    type: str

    description: str

    safety_tier: int  # 0–3, as defined in META_RULES

    handler: Callable[[Any, Dict[str, Any], Dict[str, Any]], Any]

    payload_model: Optional[type[BaseModel]] = None

    allow_in_worker: bool = True

```

Define:

```python

ACTION_REGISTRY: Dict[str, ActionSchema] = {

    "life_os.create_task": ActionSchema(

        type="life_os.create_task",

        description="Create a Life OS task",

        safety_tier=1,

        handler=_handle_life_os_create_task,

        payload_model=CreateTaskPayload,

        allow_in_worker=True,

    ),

    "calendar.create_event": ActionSchema(

        type="calendar.create_event",

        description="Create calendar event",

        safety_tier=2,

        handler=_handle_calendar_create_event,

        payload_model=CreateEventPayload,

        allow_in_worker=True,

    ),

    "transactions.categorize_transaction": ActionSchema(

        type="transactions.categorize_transaction",

        description="Categorize a transaction for tax/reporting",

        safety_tier=2,

        handler=_handle_transactions_categorize_transaction,

        payload_model=CategorizeTransactionPayload,

        allow_in_worker=True,

    ),

    # etc...

}

```

### B3. Validation Layer

Replace ad-hoc type checks in `execute_actions()` with:

1. Lookup in `ACTION_REGISTRY`.

2. Validate `action["payload"]` against `payload_model` (if provided).

3. Enforce safety tier vs. context (e.g. worker config, human approval).

4. If not found:

   * Log clearly as **unknown action**.

   * Mark action as failed.

   * Do **not** attempt to execute.

Pseudo:

```python

def execute_actions(db, actions: list[dict], context: OttoContext) -> ExecutionResult:

    for action in actions:

        schema = ACTION_REGISTRY.get(action["type"])

        if not schema:

            # log unknown; continue

            continue

        if schema.payload_model:

            payload = schema.payload_model(**action.get("payload", {}))

        else:

            payload = action.get("payload", {})

        # safety tier checks here

        # call handler(schema.handler)

```

### B4. Single Source of Truth

* All action types must be registered in `ACTION_REGISTRY`.

* Skills must not invent new action types without:

  * control doc update

  * registry entry

  * DAC review

---

## Part C — Category & Taxonomy Governance

### C1. Problem

Transactions and TaxBrainSkill can assign categories, but there is no:

* central category list

* versioning

* alias mapping

* clear tax-line mapping

This leads to category drift and inconsistent tax summaries.

### C2. Design: Category & CategoryVersion

Add models:

**Category**

* `id` (PK)

* `household_id` (FK) or `NULL` for global

* `code` (string; stable identifier, e.g. `"TOOLS_HAND"`)

* `label` (string; display name, e.g. `"Hand Tools"`)

* `type` (string; `"income"`, `"expense"`, `"transfer"`, `"other"`)

* `tax_line` (string; optional IRS line reference)

* `created_at`, `updated_at`

* `is_active` (bool)

**CategoryVersion**

* `id` (PK)

* `category_id` (FK)

* `version` (int)

* `effective_from` (date)

* `effective_to` (date|NULL)

* `notes` (text)

* `created_at`

**Transaction**

* Must reference `category_id` (FK).

* Optionally also store `category_version` used at time of classification.

### C3. Category Changes

* Changes to category **meaning** must create a new CategoryVersion.

* Transactions keep their original category+version for auditability.

* TaxBrainSkill must:

  * only assign categories that exist in the category table

  * not invent new codes

  * propose new categories via a `tax.propose_category` action that goes through human approval.

### C4. Control

Create or update a doc (or section in this one) describing:

* List of default categories

* Mapping to tax lines

* Rules for adding new categories

---

## Part D — Schema Migrations Strategy

### D1. Problem

New models (Income, Transactions, etc.) have been added without a clear migration framework. That will cause breakage on schema changes.

### D2. Design

* Use **Alembic** or a minimal migration runner.

* Create `apps/life_os/backend/migrations/` with:

  * `env.py`

  * `versions/` directory

* Every schema change must:

  * add a migration script

  * be recorded in `MIGRATIONS.md`

  * be applied before worker / backend start (or at least blocked with a clear error).

### D3. Otto + Migrations

Add a health check in Otto's env/self-test skill:

* Check for pending migrations (e.g. Alembic head vs current).

* If pending:

  * mark env as `needs_migration`

  * instruct user to run a migration command

  * do NOT let worker start until migrations applied.

---

## Part E — Decision Memory & Run Reasoning

*(This is separate from long-term memory; it is about capturing **why** a given run did what it did.)*

### E1. Problem

Otto currently records:

* input_text

* output_text

* logs

But not structured reasoning, evidence, or decision chain. This blocks:

* learning from mistakes

* explaining decisions

* future optimization

### E2. Design: Reasoning Fields in OttoRun

Extend `OttoRun` model with:

* `reasoning` (JSON, nullable)

  * Structured list of steps; example shape:

    ```json

    {

      "steps": [

        {

          "id": "step1",

          "type": "analysis",

          "summary": "Identified upcoming power bill",

          "evidence": [

            {"kind": "bill", "id": 42}

          ]

        }

      ]

    }

    ```

* `evidence` (JSON, nullable)

  * IDs of tasks, bills, income, transactions, events, memory entries consulted:

    ```json

    {

      "bills": [42],

      "transactions": [1001, 1002],

      "memory_ids": [3, 7]

    }

    ```

Skills don't need to fill this perfectly, but:

* When TaxBrainSkill runs, it should populate `reasoning` with:

  * summary of classification logic

  * references to categories and rules used.

### E3. Link With Long-Term Memory

* When a run depends on specific `OttoMemory` entries, store those IDs in `evidence.memory_ids`.

* Long-term memory doc (`CONTROL_OTTO_LONG_TERM_MEMORY.md`) governs how those memories are written and updated.

---

## Part F — Trigger / Event System

### F1. Problem

Current worker loop **polls** for pending tasks on a schedule. It does not react directly to events like:

* new bill created

* task completed

* income posted

* transaction imported

* calendar event created

This prevents Otto from being responsive and forces wasteful polling patterns.

### F2. Design: OttoEvent Model

Add:

**OttoEvent**

* `id` (PK)

* `household_id` (FK)

* `type` (string; e.g. `"bill.created"`, `"transaction.imported"`, `"task.completed"`)

* `source_model` (string; `"Bill"`, `"Transaction"`, `"Task"`, etc.)

* `source_id` (int)

* `payload` (JSON)

* `status` (string; `"pending"`, `"processing"`, `"done"`, `"error"`)

* `created_at`

* `processed_at` (nullable)

* `error` (text, nullable)

### F3. Emitting Events

Whenever key domain models change (via APIs):

* After successful DB commit, insert an `OttoEvent` row with:

  * relevant type

  * minimal payload (snapshot)

* Examples:

  * Bill created → `type="bill.created"`

  * Transaction created/imported → `type="transaction.created"`

  * Income entry created → `type="income.created"`

  * Task completed → `type="task.completed"`

  * Calendar event created → `type="calendar.created"`

### F4. Event Worker

Create a worker module:

* `worker/otto_event_worker.py`

Responsibilities:

1. Fetch `OttoEvent` rows with `status="pending"`.

2. For each, map event → OttoTask:

   * e.g. `bill.created` → create an `OttoTask` for scheduling + reminders.

   * `transaction.created` → create an `OttoTask` for classification (tax).

3. Set event status accordingly:

   * `processing` → `done` / `error`.

**Important:**

Events should be small and stateless; all real work happens via `OttoTask` + `OttoRun`.

### F5. Priority

For Phase 2.5, we only need **a minimal set**:

* `bill.created`

* `transaction.created`

* `income.created`

* `task.created`

* `calendar.created`

and a simple event→task mapping. More sophisticated routing can come later.

---

## Part G — Deliverables Checklist for Phase 2.5

Phase 2.5 is complete when ALL of the following exist and pass DAC:

1. **Global Context**

   * Household & UserProfile models

   * `OttoContext` object

   * Context wired through worker, actions, and core skills

2. **Action Registry**

   * `ACTION_REGISTRY` with all action types

   * Validator integrated into `execute_actions`

   * Unknown actions clearly reported

3. **Category Governance**

   * Category / CategoryVersion models

   * Transactions reference categories

   * TaxBrainSkill only uses known categories

   * Category change policy documented

4. **Schema Migrations**

   * Migration system in place (Alembic or equivalent)

   * Migrations for any new models

   * Otto env/self-test checks for pending migrations

5. **Decision Memory**

   * `reasoning` and `evidence` fields on `OttoRun`

   * At least TaxBrainSkill and one other skill populating basic reasoning

6. **Triggers & Events**

   * `OttoEvent` model

   * Minimal event emission on core model changes

   * Event worker that creates OttoTasks from events

7. **Docs & DAC**

   * This doc implemented

   * Changes summarized in `PHASE2_5_IMPLEMENTATION_SUMMARY.md`

   * DAC pass run and documented before starting Phase 3 skills

No new skills (beyond those already implemented) may be added until these boxes are checked and DAC-reviewed.

---

## Notes

* All rules here are subject to `CONTROL_OTTO_META_RULES.md`.

* Any conflicts must be resolved in favor of META_RULES first, then this document.

* After Phase 2.5, Phase 3 (memory + advanced skills) can proceed using:

  * `CONTROL_OTTO_LONG_TERM_MEMORY.md`

  * `SKILLS_IMPLEMENTATION_SUMMARY.md`

  * This doc as the underlying foundation.

