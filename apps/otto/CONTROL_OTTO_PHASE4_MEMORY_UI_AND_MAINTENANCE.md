# CONTROL_OTTO_PHASE4_MEMORY_UI_AND_MAINTENANCE.md  

## Otto Phase 4 — Memory UI, History, and Maintenance

Authoritative docs (in order of precedence):

1. `apps/otto/CONTROL_OTTO_META_RULES.md`
2. `OTTO_ARCHITECTURE_OVERVIEW.md`
3. `apps/life_os/control/CONTROL_OTTO_PHASE2_5_FOUNDATIONS.md`
4. `CONTROL_OTTO_LONG_TERM_MEMORY.md`
5. `SKILLS_IMPLEMENTATION_SUMMARY.md`
6. `PHASE2_5_IMPLEMENTATION_SUMMARY.md`
7. `PHASE3_IMPLEMENTATION_SUMMARY.md`
8. `PHASE3B_SUMMARY.md`
9. `PHASE3_SCENARIO_TESTS.md`

**Do NOT add new feature areas or skills beyond what's described here.**  
This phase is about:
- making memory manageable (UI),
- preserving history,
- handling expiration,
- adding simple search,
- and tightening reasoning/evidence around memory changes.

If code and docs conflict, follow the docs and note it in the summary.

---

## GOAL

Otto's long-term memory is now in place and used by reminders and TaxBrain.  
Phase 4 should make that memory:

1. **Visible and editable** through a UI in Life OS.  
2. **Auditable** via version history.  
3. **Maintainable** via expiration and simple maintenance tools.  
4. **Searchable** with simple, structured search (no embeddings/vector search).

---

## Part 0 — Sanity check (Tests & Health)

Before changing anything, do a health check.

### 0.1 Run the Phase 3 test suite

- Run `test_otto_phase3.py`:
  - Fix any failures.
  - If you need to adjust tests because behavior legitimately changed, update both the tests *and* the relevant control docs.

### 0.2 Env/health check

Use the env/self-test skill to ensure:
- Migrations are up to date.
- All core services (Otto API, Life OS backend, Life OS frontend) are reachable.

Document test results and any fixes in `PHASE4_IMPLEMENTATION_SUMMARY.md` under "Pre-flight checks".

---

## Part 1 — Memory History (Version Archive)

We already increment versions and update fields on OttoMemory. Now we need **history**.

### 1.1 Model: OttoMemoryHistory

Add a new model in the Life OS backend, e.g. `OttoMemoryHistory`:

Fields:
- `id` (PK)
- `memory_id` (FK → OttoMemory.id)
- `household_id` (FK)
- `version` (int)
- `category` (string)
- `content` (text)
- `tags` (JSON or text)
- `source` (string; as in OttoMemory)
- `created_at` (timestamp — when this historical record was created)
- `updated_at` (timestamp — last update to this history record; optional)
- `changed_by` (string or nullable; later can be user ID / "Otto" / API)

### 1.2 History creation

Whenever OttoMemory is **updated** (not created):
- Before applying the update:
  - insert a row into `OttoMemoryHistory` capturing the *previous* state (version, content, tags, etc.).

- When deleting OttoMemory:
  - either:
    - keep history and mark memory as deleted (`is_deleted` flag), OR
    - record a final history entry with a `deleted_at` in OttoMemory.

Choose whichever is simpler, but document the choice.

### 1.3 API endpoints

Add endpoints under `/otto/memory`:
- `GET /otto/memory/{id}/history`
  - Returns a list of historical versions (including metadata).
- Optional: `GET /otto/memory/{id}/history/{version}`
  - Returns a specific historical version.

No restore/rollback yet; just viewing.

### 1.4 Reasoning/evidence

- When memory is updated or deleted via an Otto action:
  - include the history operation in `OttoRun.reasoning`.
  - include the old version + memory ID in `OttoRun.evidence.memory_ids` and/or `evidence.memory_history`.

Update the memory skill and action handlers to populate reasoning/evidence for write operations.

---

## Part 2 — Memory Expiration & Maintenance

We want a way to mark memories as stale without silently deleting them.

### 2.1 Fields on OttoMemory

Add fields to OttoMemory:
- `expires_at` (datetime, nullable)
- `is_stale` (bool, default False)
- `stale_reason` (text, nullable)

### 2.2 Maintenance actions

Add new action types (and register them in `ACTION_REGISTRY`):
- `memory.mark_stale`
  - payload: `{ "memory_id": int, "reason": str }`
  - Tier: 1 or 2 (depending on how destructive you consider it; Tier 1 is fine if it's non-destructive)
- `memory.set_expiration`
  - payload: `{ "memory_id": int, "expires_at": ISO8601 datetime }`
  - Tier: 1 or 2
- Optional: `memory.clear_expiration`

These should:
- not delete memory
- just adjust these fields.

### 2.3 Worker clean-up (non-destructive)

Add a simple maintenance worker function (could be part of an existing worker or a new one):
- Periodically (e.g. daily / on demand), scan for:
  - `expires_at < now` and `is_stale = False`
- Set `is_stale=True` and `stale_reason="expired"`.

Log actions as OttoRuns with appropriate reasoning.

### 2.4 Behavior in skills

- When Scheduling or TaxBrain skills lookup memory:
  - they SHOULD prefer non-stale memories.
  - If only stale memories exist, they can:
    - use them with a warning in reasoning, OR
    - ignore them and fall back to defaults.
- Do NOT silently auto-delete stale memories.

Document this behavior in `CONTROL_OTTO_LONG_TERM_MEMORY.md`.

---

## Part 3 — Memory Relationships

We want memories to be able to reference each other and domain objects (tasks, bills, transactions, events), without magical graph complexity.

### 3.1 Model: OttoMemoryLink

Add `OttoMemoryLink` model:

Fields:
- `id` (PK)
- `from_memory_id` (FK → OttoMemory.id)
- `to_memory_id` (FK → OttoMemory.id, nullable)
- `target_type` (string; e.g. `"task"`, `"bill"`, `"transaction"`, `"event"`, `"memory"`)
- `target_id` (int; ID in the relevant table, or same as `to_memory_id` if target_type=`"memory"`)
- `relationship_type` (string; e.g. `"supports"`, `"contradicts"`, `"refines"`, `"applies_to"`)
- `created_at`
- `notes` (text, nullable)

### 3.2 API

Add routes:
- `POST /otto/memory/{id}/links`
- `GET /otto/memory/{id}/links`
- Optional: `DELETE /otto/memory/links/{link_id}`

Action types:
- `memory.link`
  - payload: `{ "from_memory_id": ..., "target_type": ..., "target_id": ..., "relationship_type": ..., "notes": ... }`
  - Tier 1 or 2.

### 3.3 Usage in reasoning

- When a skill uses a memory that is linked to a domain object:
  - add those links to `OttoRun.evidence` (e.g. `evidence.links` array).
- Example:
  - When a reminder pattern memory is used for a specific bill:
    - create a link `memory.applies_to` that bill.
  - When a tax vendor hint is created based on a set of transactions:
    - link it to those transactions.

We don't need advanced graph traversal yet; just simple links and recording them.

---

## Part 4 — Memory Search (Simple, Non-Vector)

We want a **simple search** system for memory that is:
- SQL-friendly,
- filterable,
- no embeddings/vector search.

### 4.1 Search endpoint

Add:
- `GET /otto/memory/search`

Query parameters:
- `q` (optional, text search on `content`)
- `category` (optional)
- `tag` (optional, single tag)
- `source` (optional)
- `is_stale` (optional, bool)
- pagination (`limit`, `offset`)

Implementation:
- Use basic SQL:
  - `content LIKE '%q%'` or equivalent.
- For tags, if stored as JSON/text, you can:
  - use simple `LIKE` filtering (acceptable for now),
  - or small JSON contains checks depending on DB.

### 4.2 Integration with OttoMemorySkill

Add a new type:
- `memory.search`
  - payload: same parameters as the search API.
  - Returns a summary of matches plus IDs.

This gives Otto an internal way to search memory for you.

### 4.3 Reasoning

- When a skill uses `memory.search` to find something before acting:
  - record the query parameters in `OttoRun.reasoning`.
  - record the matched memory IDs in `evidence.memory_ids`.

---

## Part 5 — Memory Console UI (Life OS Frontend)

Now we give you a way to **see and manage** memory in the Life OS web UI.

### 5.1 New route: `/otto/memory` (or `/memory` within Life OS)

Create a page in the Life OS frontend:
- Basic layout:
  - Left: filters (category, tag, source, stale/active, search box).
  - Right: memory list + details panel.

### 5.2 Features

Minimum features:

1. **List view**
   - Show:
     - content preview (first line)
     - category
     - tags
     - source
     - usage_count
     - last_used_at
     - is_stale / expires_at status

2. **Filters**
   - Filter by:
     - category
     - tag
     - source
     - is_stale (yes/no)
   - Text search (passes `q` to `/otto/memory/search`).

3. **Detail view**
   - On selecting a memory:
     - show full content
     - full tags
     - source
     - creation time
     - version
     - usage stats
     - expires_at / is_stale / stale_reason
   - Show:
     - history (via `/history` endpoint)
     - any links (relationships).

4. **Actions (scoped, non-destructive)**
   - Edit content/tags (which will:
     - create a new version,
     - insert into `OttoMemoryHistory`).
   - Mark stale / set expiration.
   - Delete memory (if allowed by meta-rules; if not, just mark stale).

All writes must go through existing memory APIs/action handlers; the UI should not directly manipulate DB.

### 5.3 Navigation

- Add a link from the main Life OS or Otto Console to:
  - "Memory Browser" or "Memory Console".

### 5.4 Safety

- Respect household scoping: only show memories for the active household.
- No actions that bypass existing safety tiers or approval protocols.

---

## Part 6 — Docs & Summary

### 6.1 New summary doc

Create `apps/otto/PHASE4_IMPLEMENTATION_SUMMARY.md` with:
- Pre-flight checks (test results from Part 0).
- What was implemented:
  - Memory history
  - Expiration/stale handling
  - Relationships
  - Search
  - Memory Console UI
- Usage examples:
  - How to open the Memory Console
  - How to view history for a memory
  - How to mark a memory stale or set expiration

### 6.2 Update control docs

- Update `CONTROL_OTTO_LONG_TERM_MEMORY.md` with:
  - history behavior,
  - expiration/stale rules,
  - relationship types,
  - search capabilities.
- If needed, update:
  - `SKILLS_IMPLEMENTATION_SUMMARY.md`
  - `OTTO_ARCHITECTURE_OVERVIEW.md`

---

## DONE Criteria

Phase 4 is complete when:

1. `test_otto_phase3.py` passes (and any updated tests also pass).
2. OttoMemoryHistory exists, is populated on updates, and is viewable via API.
3. OttoMemory expiration/stale fields exist and are used by:
   - maintenance worker
   - lookup behavior in skills (prefer non-stale).
4. OttoMemoryLink exists with basic create/list behavior and is used in at least:
   - reminder pattern → bill/event linking
   - tax hint → transaction linking.
5. Memory search endpoint works and is used by `memory.search`.
6. Memory Console UI exists in Life OS:
   - lists memories with filters
   - shows details + history + links
   - supports safe edit/mark-stale/expiration.
7. `PHASE4_IMPLEMENTATION_SUMMARY.md` summarizes all of the above.

As usual, do not add unrelated features or skills in this phase. Keep changes small, well-documented, and consistent with the meta-rules.

