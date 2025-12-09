# CONTROL_OTTO_LONG_TERM_MEMORY.md — Phase 3 Extension

**Purpose:** Give Otto a structured long-term memory system that is transparent, interpretable, queryable, and versioned.

**Status:** Phase 3 Extension

**⚠️ CRITICAL: Read `CONTROL_OTTO_META_RULES.md` FIRST — it is primary governance.**

---

## Goal

Give Otto a structured long-term memory system, **NOT** vector embeddings or a generic ML approach. Memory must be:
- **Transparent** — You can see exactly what Otto remembers
- **Interpretable** — Human-readable, not black-box embeddings
- **Queryable** — Structured queries, not similarity searches
- **Versioned** — Track changes over time
- **Auditable** — Full history of what was remembered and when

---

## Design Philosophy

Otto already stores:
- `OttoTask` — Operational tasks
- `OttoRun` — Execution history

These ARE memory — but they're **operational memory**.

Long-term memory should be:
**Knowledge that extends Otto's skills, accuracy, preferences, and interpretations over time.**

**Not a blob of random embeddings. Not "LLM-repack the entire repo and pray."**

---

## 1. Memory Model

### Database Schema

Create a new model/table in the Life OS backend: `OttoMemory`

**Fields:**
- `id` (int, PK)
- `category` (string) — e.g., `"preference"`, `"rule"`, `"domain_fact"`, `"interpretation_hint"`, `"workflow_cue"`, `"safety_policy"`
- `content` (text) — The memory itself (human-readable)
- `tags` (JSON, nullable) — Optional metadata for filtering (e.g., `["calendar", "reminders"]`)
- `source` (string) — `"user"`, `"otto_inference"`, `"task"`, or `"system"`
- `created_at` (datetime)
- `updated_at` (datetime)
- `last_used_at` (datetime, nullable)
- `usage_count` (int, default=0)
- `confidence_score` (float, 0.0–1.0) — How certain Otto is about this memory
- `version` (int, default=1)

### SQLAlchemy Model Example

```python
class OttoMemory(Base):
    __tablename__ = "otto_memory"
    
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    tags = Column(JSON, nullable=True)
    source = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0)
    confidence_score = Column(Float, default=1.0)
    version = Column(Integer, default=1)
```

**Migration:** Add `otto_memory` table to Life OS backend migrations.

---

## 2. APIs for Memory

Add routes under `/otto/memory` in Life OS backend:

### POST `/otto/memory`
**Create new memory entry**

**Request:**
```json
{
  "category": "preference",
  "content": "Karl rounds door height up before casing calc",
  "tags": ["construction", "calculations"],
  "source": "user",
  "confidence_score": 1.0
}
```

**Response:** Created memory entry

**Safety:** Tier 2 (requires approval if source is "otto_inference")

### GET `/otto/memory`
**List memories with filters**

**Query params:**
- `category` (optional) — Filter by category
- `tags` (optional, comma-separated) — Filter by tags
- `source` (optional) — Filter by source
- `limit` (optional, default=50) — Max results
- `offset` (optional, default=0) — Pagination

**Response:** Array of memory entries

### GET `/otto/memory/{id}`
**Get single memory entry by ID**

**Response:** Memory entry

### PATCH `/otto/memory/{id}`
**Update an entry**

**Request:**
```json
{
  "content": "Updated content",
  "tags": ["new", "tags"],
  "confidence_score": 0.9
}
```

**Behavior:**
- Increments `version`
- Updates `updated_at`
- Optionally archives previous version (Phase 4)

**Safety:** Tier 2 (requires approval)

### POST `/otto/memory/use`
**Mark memory as "used"**

**Request:**
```json
{
  "id": 123
}
```

**Or query-based:**
```json
{
  "category": "preference",
  "tags": ["calendar"]
}
```

**Behavior:**
- Increments `usage_count`
- Sets `last_used_at` to now
- Updates all matching entries if query-based

**Safety:** Tier 1 (read-only operation, just tracking)

### DELETE `/otto/memory/{id}`
**Delete memory entry**

**Safety:** Tier 2 (requires approval)

---

## 3. Skill: OttoMemorySkill

Add a new skill: `apps/otto/otto/skills/memory.py`

### Task Types Handled

- `memory.remember` — Add new memory
- `memory.recall` — Retrieve memory
- `memory.lookup` — Query memory with filters
- `memory.update` — Update existing memory
- `memory.propose` — Propose new memory (requires approval)

### Behavior

**When processing `memory.recall` or `memory.lookup`:**
1. Query Life OS backend `/otto/memory` API
2. Filter by category, tags, or content
3. Return relevant memories in response
4. Update `usage_count` and `last_used_at` for retrieved entries

**When processing `memory.remember`:**
1. Create action:
   ```json
   {
     "type": "memory.create",
     "tier": 2,
     "payload": {
       "category": "preference",
       "content": "...",
       "tags": [...],
       "source": "user"
     }
   }
   ```
2. Worker executes action (with approval if needed)

**When processing `memory.propose`:**
1. Create `OttoTask` with `status="pending"` and `requires_approval=true`
2. Worker blocks and waits for human approval
3. On approval, creates memory entry

### Integration with Other Skills

Other skills can:
- Call `memory.lookup` to fetch relevant memories
- Include memory evidence in reasoning
- Propose new memories via `memory.propose`

**Example:** `BillReminderSkill` might recall preference: "Notify 1 week, 1 day, and day-of for calendar events"

---

## 4. Usage Rules

### CRITICAL: Never Write Memory Silently

**Otto must never write new memory silently.**

Memory additions must come from:
- **User instruction** — "remember that..." (explicit command)
- **Explicit skill output** — Otto proposes the memory change and waits for approval

### Worker Integration

When Otto proposes memory:
1. Worker creates `OttoTask` with:
   - `type="memory.propose"`
   - `status="pending"`
   - `requires_approval=true`
2. Worker sets `OttoTask.status="blocked"`
3. Worker logs in `OttoRun`:
   - Why memory is proposed
   - What it will remember
   - Source of the proposal
4. UI displays proposal with:
   - Approve button
   - Reject button
   - Edit button (to modify before approval)
5. On approval, worker creates memory entry via API

**Safety Tier:** 2 (requires human confirmation)

---

## 5. Integration Into Skills

When processing tasks, Otto may:

1. **Fetch relevant memory entries** — Before processing, query memory for relevant context
2. **Reflect memory in proposed action plans** — Use remembered preferences/rules
3. **Include memory evidence in reasoning** — Show which memories influenced decisions

**Otto should NOT "hallucinate" memory beyond the structured records.**

If Otto needs information not in memory, it should:
- Propose adding it (if inferred)
- Ask user (if uncertain)
- Not assume

---

## 6. Memory Drift Detection

**If older memory contradicts new user direction:**

1. Otto must emit a `memory.update_proposal` action
2. Worker blocks and requires human approval
3. On approval, memory is updated (version incremented)
4. Previous version optionally archived

**Example:**
- Old memory: "Bills are due on the 5th"
- User says: "Actually, bills are due on the 10th now"
- Otto detects conflict → Proposes update → User approves → Memory updated

---

## 7. Versioning

**When a memory entry is updated:**
- Increment `version` field
- Update `updated_at` timestamp
- Optionally archive previous version (Phase 4: add `otto_memory_history` table)

**Version history enables:**
- Rollback if wrong update
- Audit trail
- Understanding how memory evolved

---

## 8. Transparency

**All memory changes must be visible in the Otto Console:**

- **New memory proposals** — Show pending proposals
- **Accepted memory writes** — Show what was remembered
- **Updated versions** — Show what changed
- **Memory usage** — Show which memories are being used

**UI Additions:**
- Memory browser page (`/otto/memory`)
- List all memories with filters
- Show usage stats (`usage_count`, `last_used_at`)
- Edit/delete buttons (with approval)
- Version history view (Phase 4)

---

## 9. Standard Memory Categories (Phase 3B)

**Currently Used Categories:**

1. **`preference`** — User preferences
   - Example: `"Default reminder pattern is 7 days before, 1 day before, and day-of."`
   - Tags: `["reminder_pattern", "scheduling"]`
   - Used by: SchedulingSkill, ReminderSkill, BillReminderSkill

2. **`tax_hint`** — Vendor/category mapping hints
   - Example: `"Vendor 'TKS' usually maps to category TOOLS_HAND"`
   - Tags: `["tax", "vendor_hint", "vendor:TKS"]`
   - Used by: TaxBrainSkill

**Household Scoping:**
- All memories are scoped to `household_id`
- Memories are queried within household context
- Global memories (household_id=NULL) are not yet supported

**Active Usage:**
- Memory is now actively used by:
  - **Scheduling/Reminders:** Default reminder pattern lookup
  - **TaxBrainSkill:** Vendor hint lookup for categorization

---

## 9A. Examples of Memory Categories (Original)

### Preference Rules
- "Karl rounds door height up before casing calc"
- "Use Tiffany blue and black for brand palette"
- "Notify 1 week, 1 day, and day-of for calendar events"

### Domain Facts
- "Pocket door count is always cell C13"
- "Bills are due on the 5th and 20th"
- "Jobsite docs templates live in /control/templates"

### Workflow Cues
- "When 'RFQ' appears in inbox, create a task"
- "Email subject 'schedule' means calendar"
- "Tasks with 'urgent' tag get high priority"

### Interpretation Hints
- "When user says 'remind me', they mean calendar reminder"
- "'Fix it' means run diagnostics first, then propose solution"

### Safety Policies
- "Finance actions require approval"
- "Never modify production code without explicit instruction"

---

## 10. What We Do NOT Want

❌ **Embeddings** — No vector stores or similarity searches  
❌ **Recall based on similarity scoring** — Use structured queries instead  
❌ **Memory that changes without audit trail** — All changes must be logged  
❌ **Otto inventing personal facts** — Only remember what's explicitly told or approved  
❌ **Otto rewriting memory on its own** — Always requires approval  

**These are dangerous in an autonomous agent.**

Structured DB rules keep Otto predictable and trustworthy.

---

## 11. Testing

Add to `test_otto_phase3.py`:

### Test Cases

1. **Add memory**
   - Create memory via API
   - Verify DB fields correct
   - Verify `created_at` set

2. **Retrieve memory**
   - Query by category
   - Query by tags
   - Verify `usage_count` increments
   - Verify `last_used_at` updates

3. **Update memory**
   - Update content
   - Verify `version` increments
   - Verify `updated_at` changes

4. **Memory proposal flow**
   - Skill proposes memory
   - Task created with `blocked` status
   - Approve → Memory created
   - Reject → Memory not created

5. **Memory drift detection**
   - Create conflicting memory
   - Verify update proposal created
   - Approve → Memory updated

---

## 12. Deliverables for Phase 3 Extension

- ✅ `OttoMemory` model + DB migrations
- ✅ Memory APIs (`/otto/memory/*`)
- ✅ `OttoMemorySkill` in `apps/otto/otto/skills/memory.py`
- ✅ Worker integration for proposed memory writes
- ✅ Console UI addition for memory browsing (`/otto/memory`)
- ✅ `test_otto_phase3.py` script with memory tests
- ✅ `PHASE3_IMPLEMENTATION_SUMMARY.md` documenting memory system

---

## 13. Implementation Notes

### Phase Naming
All code must include:
```python
# Phase 3 Extension — CONTROL_OTTO_LONG_TERM_MEMORY.md
# Implements:
# - OttoMemory model
# - Memory APIs
# - MemorySkill
# - Worker integration for memory proposals
```

### Safety Tiers
- **Memory read** — Tier 0 (safe)
- **Memory create (user)** — Tier 2 (requires approval)
- **Memory create (otto_inference)** — Tier 2 (requires approval)
- **Memory update** — Tier 2 (requires approval)
- **Memory delete** — Tier 2 (requires approval)

### Control Doc Alignment
- Follows `CONTROL_OTTO_META_RULES.md` (primary governance)
- No cross-project contamination
- Control docs must stay 1:1 with code
- Phase completion requires DAC

---

## 14. Memory History (Phase 4)

**Status:** ✅ Implemented

OttoMemoryHistory table archives all previous versions of memory entries.

### Behavior
- **On Update:** Before updating OttoMemory, a history entry is created with the previous state (version, content, tags, etc.)
- **On Delete:** Before deleting OttoMemory, a final history entry is created
- **History Preserved:** History entries remain even after memory deletion

### API Endpoints
- `GET /otto/memory/{id}/history` — List all versions
- `GET /otto/memory/{id}/history/{version}` — Get specific version

### Fields
- `id`, `memory_id`, `household_id`, `version`, `category`, `content`, `tags`, `source`, `created_at`, `updated_at`, `changed_by`

---

## 15. Memory Expiration & Stale Marking (Phase 4)

**Status:** ✅ Implemented

Memories can be marked as stale or given expiration dates without deletion.

### Fields on OttoMemory
- `expires_at` (datetime, nullable) — When memory should be considered expired
- `is_stale` (bool, default False) — Whether memory is marked as stale
- `stale_reason` (text, nullable) — Reason for marking stale

### Actions
- `memory.mark_stale` (Tier 1) — Marks memory as stale with reason
- `memory.set_expiration` (Tier 1) — Sets expiration date

### Maintenance Worker
- Periodically scans for `expires_at < now` and `is_stale = False`
- Automatically marks expired memories as stale
- Non-destructive: Only sets flags, never deletes

### Skill Behavior
- Skills **prefer** non-stale memories when looking up patterns/hints
- If only stale memories exist, skills can:
  - Use them with a warning in reasoning, OR
  - Ignore them and fall back to defaults
- Skills do NOT auto-delete stale memories

---

## 16. Memory Relationships (Phase 4)

**Status:** ✅ Implemented

OttoMemoryLink table enables relationships between memories and domain objects.

### Model
- `from_memory_id` — Source memory
- `to_memory_id` — Target memory (nullable if linking to non-memory object)
- `target_type` — "task", "bill", "transaction", "event", "memory"
- `target_id` — ID in relevant table
- `relationship_type` — "supports", "contradicts", "refines", "applies_to", etc.

### API Endpoints
- `POST /otto/memory/{id}/links` — Create link
- `GET /otto/memory/{id}/links` — List links
- `DELETE /otto/memory/links/{link_id}` — Delete link

### Action
- `memory.link` (Tier 1) — Creates memory links

### Usage
- BillReminderSkill creates `applies_to` links when reminder patterns are applied
- TaxBrainSkill creates `applies_to` links when vendor hints are applied to transactions
- Links included in `OttoRun.evidence`

---

## 17. Memory Search (Phase 4)

**Status:** ✅ Implemented

Simple SQL-based search (no embeddings/vector search).

### Endpoint
- `GET /otto/memory/search`

### Query Parameters
- `q` (optional) — Text search in content (SQL LIKE)
- `category` (optional)
- `tag` (optional, single tag)
- `source` (optional)
- `is_stale` (optional, bool)
- `limit`, `offset` — Pagination

### Implementation
- Uses SQL `LIKE '%q%'` for text search
- Simple tag filtering (JSON contains or LIKE)
- Fast and reliable, no fuzzy matching

### Skill Integration
- `OttoMemorySkill` handles `memory.search` action
- Query parameters and matched IDs included in reasoning/evidence

---

## 18. Memory Console UI (Phase 4)

**Status:** ✅ Implemented

Complete browser interface for viewing and managing memories.

### Location
- `/otto/memory` in Life OS frontend

### Features
1. **List View:** Content preview, category, tags, usage stats, stale status
2. **Filters:** Search, category, tag, source, stale status
3. **Detail View:** Full content, metadata, version history, links
4. **Actions:** Edit (creates new version), mark stale, set expiration

### Safety
- All writes go through existing APIs/action handlers
- Respects household scoping
- No actions bypass safety tiers

---

## 19. Future Enhancements (Post-Phase 4)

- **Memory history restore** — Ability to restore previous versions
- **Memory confidence decay** — Reduce confidence if unused
- **Bulk operations** — Mark multiple memories stale, set expiration in bulk
- **Memory analytics** — Dashboard showing memory usage trends
- **Advanced search** — Full-text search index, fuzzy matching
- **Memory templates** — Pre-defined memory structures for common patterns
- **Memory import/export** — Backup and restore memory data

---

## Summary

This design provides:
- ✅ **Low fragility** — No unpredictable LLM hallucinations
- ✅ **Total transparency** — Memory is literal DB rows you can inspect
- ✅ **Finite + controllable** — Only added when you command or approve
- ✅ **Safety against bias drift** — Wrong interpretations are visible and reversible
- ✅ **Otto gets smarter over time** — Accumulates habits, preferences, workflow patterns explicitly

**Memory must be semantic, explicit, auditable, and versioned.**

**Do NOT implement embeddings, vector stores, RAG, or external ML frameworks.**

---

**End of Long-Term Memory Control Document**

