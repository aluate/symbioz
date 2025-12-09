# Cursor Control: Otto + Life OS + Apps

You are Cursor, helping me build and maintain a multi-app repo that powers my personal "Life OS," Otto automations, and a few side products.

## Your job

- You may work across **the entire repo**, not just a single folder.

- You must:

  - Respect any `CONTROL*.md` files in subfolders.

  - Keep context usage efficient (do NOT load the whole repo at once).

  - Make small, targeted, reversible changes.

When in doubt, **opt for smaller diffs and more comments**, not giant refactors.

---

## Repo navigation rules

1. **Repo-wide search first, then open files**

   - Use project search to locate:

     - File names

     - Symbols (functions, classes, components)

     - API endpoints and routes

   - Only open the files that are clearly relevant to the current change.

2. **Sub-controls override this file**

   - If you find:

     - `apps/otto/CONTROL*.md`

     - `apps/life_os/CONTROL*.md`

     - `apps/catered_by_me/CONTROL*.md`

     - `apps/corporate_crashout/CONTROL*.md`

   - Read those and follow their specific rules for that app.

3. **Know the main apps (names may vary slightly)**

   - `apps/otto` → core automation / "agent" logic.

   - `apps/life_os` → Life OS backend + frontend (web UI, task & calendar brain).

   - `apps/catered_by_me` → recipe/meal app.

   - `apps/corporate_crashout` or `apps/justin_*` → Justin's trading/subscription app.

   - If paths differ, infer from context but keep the same intent.

---

## Context management (VERY IMPORTANT)

Context is limited. Follow these rules:

1. **Never load huge files in full unless absolutely necessary.**

   - If you only need one function/class, include just that chunk in the prompt.

2. **Avoid replaying long histories.**

   - Do not re-include previous full responses unless critical.

   - If you need past info, summarize it in a few bullet points instead.

3. **Keep working set small.**

   - For any single task, try to stay within:

     - A handful of files

     - The minimal code snippets needed to understand/modify behavior.

4. **Summarize state instead of stuffing it into the prompt.**

   - If you must carry state forward (like a multi-step refactor plan), rewrite it as:

     - A short checklist

     - A brief "Current status" section

     - 5–10 lines, not full transcripts.

---

## How to work across multiple apps

I often refer to **several apps at once** (Otto, Life OS, CateredByMe, Justin's thing). When this happens:

1. **Identify the boundaries.**

   - Understand which app owns:

     - Backend API

     - Frontend UI

     - Background jobs / workers

     - Payments (Stripe) if applicable

2. **Document the relationships.**

   - If you discover important flows (e.g., "Life OS frontend → Life OS backend → Otto API"), add or update a small markdown doc in `control/` or `docs/` describing it.

3. **Keep each change localized.**

   - Even if a feature spans multiple apps, structure your work as:

     1. Backend/API step

     2. Otto/automation step

     3. Frontend/UI step

   - Make sure each step is testable on its own.

---

## Safety rules for changes

1. **Do not hardcode secrets.**

   - Never commit real API keys, Stripe keys, DB passwords, or tokens.

   - Use environment variables (e.g. `STRIPE_SECRET_KEY`) and `.env` patterns.

2. **Prefer incremental diffs.**

   - Small commits with clear intent > giant sweeping refactors.

   - When refactoring, keep behavior identical unless explicitly told otherwise.

3. **Keep migrations explicit.**

   - If a DB schema change is needed:

     - Update the migration system (Alembic, Prisma, etc.).

     - Add notes to the relevant `CONTROL` or `README` with any manual steps.

4. **Log what you changed.**

   - When you complete work, add/update a summary doc (e.g. in `control/` or `docs/`) describing:

     - What was added/changed

     - Where the main entrypoints are

     - Any TODOs or limitations

---

## Stripe and external plugins

- Treat Stripe and similar integrations as **optional modules**.

- If something is broken or blocking:

  - You may disable or stub Stripe flows if instructed.

  - Keep the rest of the app functional without Stripe.

- When disabling an integration:

  - Remove or guard plugin registration.

  - Guard any routes/endpoints so the app still runs.

  - Update docs to note that payments are currently disabled.

---

## How to ask for clarification

If user instructions are ambiguous:

- Briefly state your assumption.

- Proceed with the safest, smallest change that matches that assumption.

- Leave TODO comments if needed, e.g.:

  - `# TODO: Confirm if Stripe should be fully removed or just disabled in dev`

---

## Output style

When finishing a task:

- List:

  - Files touched

  - High-level summary of changes

  - Any manual steps to run (migrations, npm install, env vars)

Keep explanations short but precise. This control is always in effect when working in this repo.

