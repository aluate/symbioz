# CONTROL_OTTO_SHELL.md — Build the Otto Shell

Goal:

Create a simple Otto Shell so Karl can:

- Talk directly to Otto from a web UI (like ChatGPT/Cursor).

- See what Otto is doing (inputs, outputs, errors).

- Use the same mechanism for both manual runs and future background runs.

This work should integrate with the existing Life OS + Otto setup described in:

- `OTTO_CONTEXT.md` (repo root)

- `FRAT_CONTEXT.md` (repo root)

- `apps/otto/CONTROL_OTTO.md`

## 1. Data model — otto_runs

In the Life OS backend (or wherever app-level models live), add a model/table:

Name: `OttoRun` (SQLAlchemy / ORM equivalent)

Fields:

- `id` (PK)

- `created_at` (datetime, default now)

- `updated_at` (datetime, auto-update)

- `status` (string or enum) — `pending` | `running` | `success` | `error`

- `source` (string) — e.g. `shell`, `worker`, `webhook`

- `input_text` (text) — human-readable input prompt

- `input_payload` (JSON, nullable) — structured input if needed

- `output_text` (text, nullable) — main text output from Otto

- `output_payload` (JSON, nullable) — structured actions, if any

- `logs` (text or JSON, nullable) — debug info, intermediate steps, error messages

Implement migrations if needed, consistent with the existing backend.

## 2. Backend API — Otto Runs

Under the Life OS backend API (FastAPI or equivalent), add a router:

Base path: `/otto/runs`

Endpoints:

1. `POST /otto/runs`

   - Body: `{ "input_text": string, "input_payload"?: json }`

   - Creates an `OttoRun` with:

     - `status = "pending"`

     - `source = "shell"`

     - saves `input_text` and `input_payload`

   - Immediately triggers a function that:

     - marks status → `running`

     - calls the existing Otto HTTP API (`apps/otto` service) at `/prompt` with:

       - the input text and payload

       - any necessary context

     - captures:

       - main response text → `output_text`

       - any structured actions (if already implemented) → `output_payload`

     - sets `status` → `success` or `error`

     - writes logs if there is an exception

   - Returns the created `OttoRun` record.

   **Important:** implement the Otto call as a Python function using the existing configuration for Otto's base URL (do not hardcode localhost in the logic, use a config/env setting).

2. `GET /otto/runs`

   - Query params:

     - optional `limit` (default ~20)

   - Returns a list of recent `OttoRun` objects, ordered by `created_at` DESC.

3. `GET /otto/runs/{id}`

   - Returns full details of a single run, including logs.

The implementation can be synchronous for now (no async worker needed yet), as long as the endpoint stays responsive. If needed, keep the Otto call in a separate function so it's easy to move into a background worker later.

## 3. Frontend — Otto Console page

In the Life OS frontend app:

1. Add a route/page:

   - Path: `/otto` or `/agent-console` (choose one and keep it consistent with nav)

   - Add a simple nav link or button in the existing UI so Karl can get there easily.

2. Page layout (desktop + mobile friendly):

   - Left column (or top section on mobile):

     - List of recent `OttoRun` items:

       - Show: status badge, source, timestamp, and first line of `input_text`

       - Clicking an item sets it as the "active" run.

   - Right column (or bottom section on mobile):

     - If an active run is selected:

       - Show:

         - Status, timestamps

         - `input_text`

         - `output_text`

         - `logs` (collapsible if long)

     - At the bottom:

       - A textarea or input box to create a new run:

         - Placeholder: "Talk to Otto…"

         - Enter or a "Send" button triggers `POST /otto/runs` with `input_text`

         - On success, prepend the new run to the list and set it active.

3. Behavior details:

   - Polling:

     - For now, simple polling is fine (e.g. refetch run details every few seconds while status is `pending` or `running`).

   - Error handling:

     - If the backend marks a run as `error`, show that clearly with a red badge and display the `logs` or error message.

   - No need for streaming yet; a simple "submit → wait → show result" flow is OK for v1.

4. Styling:

   - Keep consistent with existing Life OS frontend styling.

   - Make sure the console works nicely on mobile (since Karl uses Otto from his phone).

## 4. Integration with existing Otto API

When calling the Otto backend:

- Use the already-existing `/prompt` endpoint from `apps/otto`, if available.

- Wrap the response so that we store:

  - The main human-readable answer in `output_text`.

  - Any structured data (if present) in `output_payload`.

If `/prompt` doesn't exist or has changed:

- Inspect `apps/otto` for the current HTTP interface and adapt accordingly.

- Update any relevant docs (`OTTO_CONTEXT.md`, `apps/otto/CONTROL_OTTO.md`) with the final chosen API shape.

## 5. Deliverables

When you are done, you should have:

- A new `OttoRun` model + migrations.

- A working `/otto/runs` API in the Life OS backend.

- A new Otto Console page in the Life OS frontend that:

  - Lists runs

  - Shows details

  - Lets Karl send new prompts

Keep changes small, focused, and documented.

