# CONTROL_OTTO.md — Otto Agent Core

**⚠️ CRITICAL: Read `CONTROL_OTTO_META_RULES.md` FIRST — it is primary governance for all Otto work.**

You are editing **Otto**, a single AI agent that lives in this repo.

## 1. Purpose

Otto is a provider-agnostic agent that:

- Reads tasks and prompts from various inputs (Life OS, CLI, docs, etc.).

- Chooses which **skill** to apply (infra_sre, life_os, etc.).

- Emits actions (code changes, deployments, calendar events, DB updates, etc.).

- Runs in the background as a long-lived helper for this repo and related apps.

Otto is NOT:

- A one-off script.

- Separate per-project bots.

Otto is ONE system with MANY skills.

---

## 2. Skills architecture

Treat Otto as:

- **Core:** routing, memory, context handling, action protocol.

- **Skills:** discrete modules, each responsible for a domain.

Examples:

- `infra_sre` skill:

  - Manages Render/Vercel/Supabase/Stripe/etc.

  - Deploys apps from this repo.

  - Performs health checks / diagnostics.

- `life_os` skill:

  - Works with the Life OS app (tasks, calendar, bills, taxes).

  - Executes household / personal automations.

- `wedding_site` skill:

  - Handles deployment / maintenance for the wedding site.

When extending Otto:

- Prefer adding or improving a **skill module** over mixing everything into one giant file.

- Keep skills loosely coupled and discoverable.

---

## 3. How other projects talk to Otto

Other apps (Life OS, wedding site, CateredByMe, Justin's app) should:

- Treat Otto as an external *agent service*.

- Communicate via:

  - HTTP API (e.g., `/prompt`, `/task`)

  - Shared task queues / DB tables

  - File-based command docs (if applicable)

Do NOT:

- Rebuild Otto logic inside each project.

- Fork Otto's agent core per app.

- Hardcode project-specific behavior directly into Otto's core without putting it behind a skill boundary.

---

## 4. Cursor rules when working in `apps/otto/`

1. **Respect the skill boundaries**

   - If you need infra-related behavior → update/extend the `infra_sre` skill.

   - If you need Life OS automation → add a life_os skill, don't inject into infra_sre.

   - Keep each skill focused and testable.

2. **Keep context tight**

   - When editing Otto:

     - Open only the core files and the specific skill module you are touching.

     - Avoid loading the entire repo into context.

   - Summarize Otto's state and plans instead of copying huge logs into prompts.

3. **Document changes**

   - Update `OTTO_CONTEXT.md` if new skills or integration patterns are added.

   - Leave brief notes in this file (or a dedicated `CHANGELOG_OTTO.md`) when you:

     - Add a new skill

     - Change how tasks are routed

     - Change the action protocol

4. **Maintain stable APIs**

   - Otto's external interface (HTTP routes, task schema, action schema) should remain stable or be versioned.

   - If you change APIs, document the expected callers:

     - Life OS frontend/backend

     - CLI tools

     - Other apps (wedding, CateredByMe, Justin's app)

---

## 5. Safety and testing

- Keep Otto's actions **reversible** where possible (e.g. Git commits, backups).

- For destructive operations (e.g. infra changes, DB migrations):

  - Add a "dry run" mode.

  - Make sure it's documented and easy to enable.

- Prefer:

  - Small, incremental changes.

  - Clear logging / summaries of what Otto did.

---

## 6. Mental model reminder

Whenever this repo or docs say "Otto will handle X":

- Interpret it as:

  > "The Otto agent (apps/otto) will use one of its skills to perform that work."

There is only **one Otto**.  

Skills and projects are layered on top of that single agent.

---

## Original Vision (for reference)

Otto is a provider-agnostic AI agent that lives with my files (repos, Google Drive, local storage), not inside any one UI (ChatGPT, Cursor, etc.).

If any external AI tool becomes unavailable or too expensive, Otto still:
- Reads tasks from documents
- Executes scripts and skills
- Organizes outputs
- Proposes refactors and improvements to its own codebase

All logic, prompts, and configuration live in my repos where I own them.

See `OTTO_CONTEXT.md` in the repo root for the complete context of how Otto fits into the broader system.
