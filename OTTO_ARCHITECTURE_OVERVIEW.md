# OTTO_ARCHITECTURE_OVERVIEW.md

**Purpose:** Central hub for understanding how Otto works and how all the pieces fit together.

This document links to all the key control documents and context files that define Otto's architecture and behavior.

---

## ⚠️ CRITICAL: Meta-Rules Document

### 0. `apps/otto/CONTROL_OTTO_META_RULES.md`
**What it is:** Hard rules that prevent architectural drift, feature bloat, and incoherent behavior.

**Key points:**
- Primary governance document — overrides all other guidance
- Defines safety tiers, approval protocols, rate limits
- Prevents cross-project contamination
- Enforces control doc/code alignment
- Requires explicit skill definitions

**Read this FIRST before any Otto work.**

---

## Core Context Documents

### 1. `OTTO_CONTEXT.md` (repo root)
**What it is:** Master context explaining what "Otto" means in this repo.

**Key points:**
- Otto is a **single AI agent** with multiple skills
- SRE/infra is the **first skill**, not a separate bot
- Projects integrate with Otto; they don't define separate Ottos

**Read this when:** You're confused about what "Otto" refers to, or how projects relate to Otto.

---

### 2. `FRAT_CONTEXT.md` (repo root)
**What it is:** Explains who Frat is and how Frat, Cursor, and Otto relate.

**Key points:**
- Frat = External ChatGPT persona (strategy/planning) - **not in the repo**
- Cursor = Code implementer - reads docs and builds
- Otto = In-repo agent being built - executes tasks/skills

**Read this when:** You see references to "Frat" and wonder if it's a service to build.

---

### 3. `apps/otto/CONTROL_OTTO.md`
**What it is:** Control document for working on Otto's core agent system.

**Key points:**
- Otto is a provider-agnostic agent with skills architecture
- Skills are modular and loosely coupled
- How other projects talk to Otto (HTTP API, shared storage, etc.)

**Read this when:** You're editing code in `apps/otto/` or adding new skills.

**Note:** This document is subject to `CONTROL_OTTO_META_RULES.md` which takes precedence.

---

## Implementation Control Documents

### 4. `apps/otto/CONTROL_OTTO_LONG_TERM_MEMORY.md`
**What it is:** Phase 3 Extension - Structured long-term memory system for Otto.

**Key points:**
- Transparent, interpretable, queryable memory (NOT embeddings)
- Structured DB model with categories, tags, versioning
- Memory proposals require approval (Tier 2)
- Full audit trail of what Otto remembers

**Read this when:** Implementing or extending Otto's memory capabilities.

---

### 5. `apps/life_os/control/CONTROL_OTTO_SHELL.md`
**What it is:** Spec for Phase 1 - the Otto Shell (visible console interface).

**Key points:**
- `OttoRun` model tracks execution history
- `/otto/runs` API for creating and viewing runs
- Otto Console frontend page for manual interaction

**Status:** ✅ **COMPLETE** (Phase 1)

**Read this when:** You need to understand how the Otto Shell works or extend it.

---

### 5. `apps/life_os/control/CONTROL_OTTO_PHASE2.md`
**What it is:** Spec for Phase 2 - Worker, Actions, and Easy Setup.

**Key points:**
- `OttoTask` model for scheduled/recurring tasks
- Worker loop that processes tasks autonomously
- Action executor for structured side effects
- "Grandma mode" setup scripts and environment diagnostics

**Status:** ⏳ **PLANNED** (Phase 2)

**Read this when:** You're implementing autonomous task processing or action execution.

---

## Mental Model Summary

```
┌─────────────────────────────────────────────────────────┐
│                    OTTO ARCHITECTURE                     │
└─────────────────────────────────────────────────────────┘

Frat (ChatGPT) ──┐
                │ writes control docs
                ▼
         [Control Docs in Repo]
                │
                ├──► OTTO_CONTEXT.md (what is Otto?)
                ├──► FRAT_CONTEXT.md (who is Frat?)
                ├──► CONTROL_OTTO.md (Otto core)
                ├──► CONTROL_OTTO_SHELL.md (Phase 1)
                └──► CONTROL_OTTO_PHASE2.md (Phase 2)
                │
                │ Cursor reads these
                ▼
         [Implementation]
                │
                ├──► apps/otto/ (Otto agent core)
                │    ├── skills/ (modular capabilities)
                │    └── api.py (HTTP interface)
                │
                └──► apps/life_os/ (Life OS app)
                     ├── backend/ (FastAPI)
                     │   ├── models.py (OttoRun, OttoTask)
                     │   ├── otto_runs.py (Phase 1 API)
                     │   ├── otto_tasks.py (Phase 2 API)
                     │   └── worker/ (Phase 2 worker loop)
                     └── frontend/ (Next.js)
                         └── app/otto/ (Otto Console)
```

---

## Key Concepts

### Otto = One Agent, Many Skills

- **Core:** `apps/otto/` - routing, memory, context handling
- **Skills:** Discrete modules (infra_sre, life_os, otto_runs, env_status, etc.)
- **Projects:** Clients of Otto (wedding site, Life OS, CateredByMe, etc.)

### Task vs Run

- **OttoTask:** What should happen (scheduled/recurring tasks)
- **OttoRun:** What actually happened (execution record)
- **Worker:** Turns Tasks → Runs by calling Otto and executing actions

### Actions

- Otto proposes structured actions (e.g., `life_os.create_task`)
- Action executor safely applies them
- All actions are logged and reversible where possible

---

## How to Extend Otto

1. **Adding a new skill:**
   - Create skill module in `apps/otto/otto/skills/`
   - Register in `apps/otto/otto/skills/__init__.py`
   - Update `OTTO_CONTEXT.md` with skill description

2. **Adding a new action type:**
   - Add handler in Life OS backend `otto/actions.py`
   - Document in `CONTROL_OTTO_PHASE2.md`
   - Update Otto skills to emit the new action type

3. **Adding a new project integration:**
   - Create project-local doc explaining which Otto skill(s) it uses
   - Add integration section (like in `apps/wedding/START_HERE.md`)

---

## Context Preservation Strategy

**The Problem:** Frat (external AI) loses context over time.

**The Solution:** All important decisions and architecture live in this repo:

- ✅ Control docs define behavior (not just code comments)
- ✅ Database models persist state (`OttoTask`, `OttoRun`)
- ✅ Code implements the docs (docs are source of truth)
- ✅ This overview links everything together

**Result:** If Frat forgets something, the repo remembers. Otto and Cursor read the same docs and stay consistent.

---

## Quick Reference

**"What is Otto?"** → `OTTO_CONTEXT.md`

**"Who is Frat?"** → `FRAT_CONTEXT.md`

**"How do I work on Otto core?"** → `apps/otto/CONTROL_OTTO.md`

**"How does the Shell work?"** → `apps/life_os/control/CONTROL_OTTO_SHELL.md`

**"How do I implement the worker?"** → `apps/life_os/control/CONTROL_OTTO_PHASE2.md`

---

**Last Updated:** January 2025  
**Status:** Living document - update when architecture changes

