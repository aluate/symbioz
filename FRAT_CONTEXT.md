# FRAT_CONTEXT.md

## ⚠️ CRITICAL: Who Everyone Is

**The Team:**
- **Karl** - The human developer/owner of this repository
- **Frat** - External ChatGPT persona that Karl uses for strategy/planning (NOT in this repo)
- **Auto (Cursor)** - AI coding assistant that reads Frat's specs and implements them
- **Otto** - The in-repo agent being built that executes tasks

**The Workflow:**
1. Karl → Frat (ChatGPT) → Creates plans/specs/control docs
2. Frat's docs → Stored in this repo
3. Auto (me) → Reads docs → Implements code
4. Otto → Executes tasks using the code

---

## What "Frat" means

**Frat is NOT a service or agent in this repo.**

Frat is the name of an external AI assistant persona (ChatGPT) that **Karl** uses for:

- Strategy and architecture

- Master execution plans and roadmaps

- Control documents and specs

- Detailed implementation prompts for Cursor

Frat lives *outside* the codebase.  

You will not find a `frat` backend or a `frat` API here.

---

## How Frat, Cursor, and Otto relate

- **Frat (ChatGPT persona)**  

  - Designs systems and workflows  

  - Writes control docs, prompts, and specs stored in this repo



- **Auto (Cursor/me)**  

  - Reads those docs and prompts  

  - Edits the code, configs, and infra in this repo
  
  - **I am Auto, Karl's AI coding assistant in Cursor**



- **Otto (apps/otto)**  

  - The in-repo agent being built  

  - Executes tasks/skills using the code you implement



Whenever repo docs say things like:

- "Frat will create a plan"

- "Ask Frat for a control doc"

- "Frat will generate prompts for Cursor"



Interpret that as:

> "There will be a written spec or control document in this repo. You (Cursor) should follow that spec; do not try to implement a separate 'Frat' service."

---

## Rule for Cursor

If you encounter references to "Frat":

- Do **not** search for or build a "Frat" backend.

- Instead, look for:

  - `CONTROL_*.md`

  - `*_PLAN.md`

  - `*_PROMPT.md`

  - Other docs that look like strategy / instructions.

- Treat those docs as Frat's output and follow them.

