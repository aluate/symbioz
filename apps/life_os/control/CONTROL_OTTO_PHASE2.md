# CONTROL_OTTO_PHASE2.md — Worker, Actions, and Easy Setup

Goal for Phase 2:

1. Give Otto an **autonomous worker** that runs tasks without me manually poking the Shell.

2. Give Otto a **structured action executor** so it can actually change things (DB, calendar, files, etc.) in a safe, logged way.

3. Add **"grandma mode" setup**: one-command scripts + an Otto env skill to detect/install missing dependencies and report status.

**⚠️ CRITICAL: Read `apps/otto/CONTROL_OTTO_META_RULES.md` FIRST — it is primary governance.**

This builds on:

- `apps/otto/CONTROL_OTTO_META_RULES.md` (PRIMARY GOVERNANCE - READ FIRST)
- `OTTO_CONTEXT.md` (repo root)
- `FRAT_CONTEXT.md` (repo root)
- `apps/otto/CONTROL_OTTO.md`
- `control/CONTROL_OTTO_SHELL.md`

Otto Shell (Phase 1) is already done:

- `OttoRun` model and `/otto/runs` API in Life OS backend

- Otto Console page in Life OS frontend

- `OttoRunsSkill` in Otto

---

## Part 1 — Otto Task Worker (Autonomous Agent)

### 1. Data model: OttoTask

Add a **new table in the Life OS backend** for tasks Otto should process.

Model: `OttoTask`

Fields:

- `id` (PK)

- `created_at` (datetime, default now)

- `updated_at` (datetime, auto)

- `status` (enum/string):

  - `"pending"` | `"running"` | `"success"` | `"error"` | `"blocked"`

- `type` (string):

  - e.g. `"life_os.reminder"`, `"infra.deploy"`, `"debug.env"`, `"custom.prompt"`

- `description` (text):

  - Human-readable description of the task

- `payload` (JSON, nullable):

  - Structured input data for the task

- `next_run_at` (datetime, nullable):

  - When this task is due to run next (for scheduled/recurring tasks)

- `last_run_at` (datetime, nullable)

- `last_error` (text, nullable)

Migration:

- Add DB migration for `OttoTask` consistent with existing backend migration strategy.

### 2. Task API

Add a router to Life OS backend: `/otto/tasks`

Endpoints:

1. `POST /otto/tasks`

   - Creates a new `OttoTask` with:

     - `status="pending"`

     - `type`, `description`, `payload`, optional `next_run_at`

   - Returns the task.

2. `GET /otto/tasks`

   - Query params:

     - optional `status`

     - optional `limit` (default ~50)

   - Returns recent tasks.

3. `GET /otto/tasks/{id}`

   - Returns details for a single task.

These APIs are mainly for:

- The Otto Shell UI

- Future scripting

- Debugging

### 3. Worker loop service

Create a **worker module** in Life OS backend, e.g.:

- `worker/otto_worker.py` (or similar)

Responsibilities:

- Periodically poll for tasks that are ready to run:

  - `status="pending"` and (no `next_run_at` or `next_run_at <= now`)

- For each task:

  1. Create a corresponding `OttoRun` with:

     - `source="worker"`

     - `input_text` summarizing the task

     - `input_payload` containing the full task payload

     - `status="pending"` → `"running"` → final state

  2. Call a shared helper function that:

     - Calls Otto's `/task` or `/prompt` API with a **structured payload**:

       - `task_type` = `task.type`

       - `task_payload` = `task.payload`

       - Maybe also include `task_id` in the payload

     - Receives text and optional structured `actions` from Otto.

  3. Execute returned actions via the Action Executor (see Part 2).

  4. Update:

     - `OttoRun` with `output_text`, `output_payload`, `logs`, final status.

     - `OttoTask` with `status`, `last_run_at`, `next_run_at` (if recurring), `last_error` if any.

Implementation details:

- For Phase 2, a **simple polling loop** is fine:

  - For dev: a function `run_worker_forever()` that:

    - Sleeps for N seconds between scans (e.g. 10–30).

  - Provide a CLI entrypoint or script to start it:

    - e.g. `python -m worker.otto_worker` or `life_os_worker.bat`

- Use the same DB/session setup as the existing backend.

### 4. Shell integration

- Update the Otto Console to show tasks as well (Phase 2.5, optional):

  - Either a second tab for "Tasks" or a section that links from runs → tasks.

- At minimum, the worker should log enough into `OttoRun` that I can see:

  - Which tasks it handled

  - What Otto replied

  - Which actions were executed

  - Any errors

---

## Part 2 — Structured Actions & Action Executor

Otto should not just reply with text; it should **emit actions** that the worker can execute.

### 1. Action schema

Define a **standard JSON shape** for actions:

```json
{
  "actions": [
    {
      "type": "create_calendar_event",
      "payload": { /* ... */ }
    },
    {
      "type": "mark_task_complete",
      "payload": { "task_id": 123 }
    }
  ]
}
```

General rules:

* Root object may contain:

  * `message` (string) — Otto's human-readable summary.

  * `actions` (array) — list of action objects.

* Each action:

  * `type` (string) — namespaced where helpful, e.g. `"life_os.create_task"`.

  * `payload` (JSON object) — fields specific to that action.

For Phase 2, implement a **small starter set**:

* `life_os.create_task`

* `life_os.update_task_status`

* `life_os.log_note`

* `otto.log` (for debug messages only)

Later we can add:

* `calendar.create_event`

* `infra.deploy_project`

* `bills.mark_paid`

  …etc.

### 2. Executor module

In Life OS backend, add an executor module, e.g.:

* `otto/actions.py`

Responsibilities:

* Function: `execute_actions(db, actions: list, context: dict) -> ExecutionResult`

  * Iterate over actions.

  * For each `action["type"]`, dispatch to a handler:

    * e.g. `_handle_life_os_create_task`, `_handle_life_os_update_task_status`, `_handle_otto_log`, etc.

  * Collect:

    * success/failure for each action

    * any error messages

  * Return a structured `ExecutionResult` object that can be serialized and stored in `OttoRun.output_payload` or `OttoRun.logs`.

Execution rules:

* Be **defensive**:

  * If an action is unknown, add a warning to logs and continue with others.

  * If an action fails (exception), catch it, log it, and mark that action as failed.

* Log everything important:

  * Action type

  * Payload

  * Result (ok/error)

  * Error messages if any

### 3. Otto's output contract

Update / extend Otto's skills so that when Otto is called for **task processing** (from the worker), it:

* Returns a JSON object with:

  * `message`: summary text

  * `actions`: list of action objects (may be empty)

* Otto should **not** execute side effects directly; it should only propose `actions`.

The worker + executor are responsible for actually performing those actions.

---

## Part 3 — "Grandma Mode" Setup & Dependency Management

We want Otto to be "grandma-usable": minimal friction to install and repair.

### 1. Root-level setup scripts

Add **simple, one-shot scripts** at the repo root:

* `setup_otto_windows.bat`

* `setup_otto_unix.sh`

Goal: one command (or double-click) to:

* Create / activate a virtualenv (optional but preferred on Unix).

* Install Python deps for:

  * `apps/otto/requirements.txt`

  * `apps/life_os/backend/requirements.txt`

* Install Node deps for:

  * `apps/life_os/frontend/package.json`

* Print **clear status** at the end.

Example high-level behavior (Windows batch):

* Check for `python` and `pip`.

* `python -m venv .venv` (if no venv).

* `call .venv\Scripts\activate.bat`

* `pip install -r apps\otto\requirements.txt`

* `pip install -r apps\life_os\backend\requirements.txt`

* `cd apps\life_os\frontend && npm install`

* Print "Setup complete. Use START_OTTO.bat to run everything."

Also add simple "start everything" scripts (if not already present):

* `START_OTTO_WINDOWS.bat`

* `start_otto_unix.sh`

They should:

* Start Otto API

* Start Life OS backend

* Start Life OS frontend

* Optionally start the worker loop

### 2. Environment skill in Otto

Add a new skill in `apps/otto/otto/skills/`, e.g. `env_status.py`:

Responsibilities:

* Provide **diagnostics**, not arbitrary shell access.

* When invoked with types like:

  * `env_status`, `otto_doctor`, `check_dependencies`

* It should:

  * Hit a small backend route in Life OS (or run local checks if appropriate) to see:

    * Are the main services up? (Otto, Life OS backend, Life OS frontend)

    * Are DB migrations up to date?

  * Optionally run **safe** commands like:

    * `pip list` (via subprocess) and compare against `requirements.txt`

    * `npm -v` / `node -v` (version checks)

  * Return a structured report:

    * What's OK

    * What's missing

    * Which script (e.g. `setup_otto_windows.bat`) the user should run to fix it

The point: Grandma doesn't need to understand `pip install`. Otto (and the Shell UI) can say:

> "Your backend dependencies are missing. Run `setup_otto_windows.bat` once, then click 'Retry'."

### 3. No unsupervised `pip install` in Otto

Important constraint:

* Otto's env skill can **suggest** or **trigger** pre-defined scripts,

* But do **not** give Otto full arbitrary shell command execution inside the running server.

Instead:

* Let scripts (`setup_otto_*.sh/.bat`) handle actual installs.

* Otto's role:

  * Detect what's missing.

  * Update `requirements.txt` / `package.json` when told to.

  * Tell the user which script to run.

If needed later, we can add a separate, explicit "maintenance mode" script that can be run manually to:

* Apply updated lockfiles

* Reinstall dependencies

---

## Part 4 — Deliverables Checklist

When Phase 2 is complete, we should have:

1. **OttoTask model** + migrations in Life OS backend.

2. `/otto/tasks` API (create/list/get).

3. Worker service:

   * Scans for due tasks.

   * Calls Otto with structured payloads.

   * Creates `OttoRun` records with `source="worker"`.

4. Action executor:

   * Standard JSON schema for actions.

   * Handlers for at least:

     * `life_os.create_task`

     * `life_os.update_task_status`

     * `otto.log`

5. Updates to Otto skills to emit:

   * `message` + `actions[]` for task processing calls.

6. Root-level setup scripts:

   * `setup_otto_windows.bat`

   * `setup_otto_unix.sh`

   * `START_OTTO_WINDOWS.bat` / `start_otto_unix.sh` (if not already present)

7. Environment/doctor skill in Otto:

   * Reports env/dependency status.

   * Points user at the right setup script to run.

Keep changes small, modular, and well-documented in the existing control/docs structure.

