# OTTO_CONTEXT.md

## 1. What "Otto" means in this repo

**Otto is a single AI agent that lives with this repo.**

- Otto is not just an SRE bot.

- Otto is not tied to a single project.

- Otto is a *general agent* that can perform different skills depending on context.

You can think of it like this:

- **Otto (core)** — agent brain and protocol, lives in `apps/otto/`

- **Skills** — specific capabilities Otto can use:

  - `infra_sre` — infrastructure + deployment automation (Render, Vercel, Supabase, Stripe, GitHub, etc.)

  - `life_os` — personal Life OS tasks (calendar, tasks, bills, taxes, etc.)

  - `wedding_site` — deploy/manage the wedding site

  - Future skills — any new areas we add

Other docs may casually say "Otto will deploy this" or "let Otto handle that".  

**Always interpret that as: "Otto, using the relevant skill for this project."**

---

## 2. Where Otto lives

- Core agent: `apps/otto/`

- Infra/SRE helpers: `infra/`, `tools/infra.py`, and any infra-specific scripts

- Life OS app: `apps/life_os/`

- Other apps:

  - Wedding site

  - CateredByMe

  - Justin's subscription/trading app

  - (etc.)

These apps *consume* Otto's skills; they do **not** define separate Ottos.

---

## 3. Otto vs. the SRE skill

Originally, "Otto" started as:

- A **CLI / automation tool** to:

  - deploy apps

  - manage infra

  - run diagnostics

  - set up Stripe/Supabase/Vercel/Render/github, etc.

This shows up in docs under `infra/` and in some project notes.

That SRE functionality is now considered:

> **Otto's `infra_sre` skill**  

> (the first skill we gave Otto)

So when you see "Use Otto to deploy this project" in a doc, read it as:

> "Use Otto's `infra_sre` skill to deploy this project."

---

## 4. How Cursor should reason about Otto

If you are Cursor working in this repo:

1. **Otto is a single agent system**

   - Code and configuration for Otto's core behavior live in `apps/otto/`.

   - Otto should be extended with new skills; do *not* duplicate or fork Otto for each project.

2. **Projects integrate with Otto**

   - The wedding site, Life OS, CateredByMe, Justin's app, etc. are **clients** of Otto.

   - They might:

     - call Otto via HTTP

     - write tasks/commands into shared storage

     - be targets for `infra_sre` deployment workflows

3. **Skills are modular**

   - Infra/SRE is one skill.

   - Life OS is another domain where Otto acts.

   - If a new project needs automation, prefer:

     - "Add a new skill to Otto"

     - over "build a new bot from scratch".

4. **Document new skills**

   - When adding a new Otto skill:

     - Add a short description to this file under "Skills".

     - Create/update a control doc in `apps/otto/` describing how that skill works.

     - Add a short project-local doc in that app explaining how it talks to Otto.

---

## 5. Project-specific references to Otto

When you see "Otto" mentioned in project docs:

- **Wedding site docs**  

  "Deploy with Otto" → means "Use Otto's `infra_sre` skill to deploy this Next.js wedding site."

- **Life OS docs**  

  "Otto handles tasks from the Life OS" → means "Life OS sends tasks/commands to Otto. Otto acts as a background agent and writes results back."

- **Other app docs**  

  Similar pattern: Otto is always **one agent**, using the relevant skill for that app.

If you (Cursor) are confused:

- Check this file (`OTTO_CONTEXT.md`).

- Check `apps/otto/CONTROL_OTTO.md`.

- Then check the local project's control doc (e.g. `apps/<project>/CONTROL_*.md`) for specific integration details.

---

