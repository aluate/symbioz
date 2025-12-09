# Phase 4 Cleanup and Future Work

**Status:** Post-Phase 4 items for testing and refinement

---

## Immediate Cleanup Items

### 1. Run and Extend Tests

**Current Status:** `test_otto_phase3.py` exists but hasn't been run yet

**Action Items:**
- [ ] Start Life OS backend (port 8000) and Otto API (port 8001)
- [ ] Run `python apps/otto/test_otto_phase3.py`
- [ ] Fix any test failures
- [ ] Extend test suite to cover:
  - [ ] History creation on update/delete
  - [ ] Expiration marking (`memory.set_expiration`)
  - [ ] Stale marking (`memory.mark_stale`)
  - [ ] Memory links creation (`memory.link`)
  - [ ] Search functionality (`memory.search`)
  - [ ] Maintenance worker (expired → stale)

**Location:** `apps/otto/test_otto_phase3.py`

---

### 2. Finish Context Integration

**Current Status:** API endpoints use `get_default_context()` which works for single-household use

**Action Items:**
- [ ] Review all API endpoints that create domain models
- [ ] Ensure context is fully wired for multi-user scenarios
- [ ] Consider adding user authentication/session context
- [ ] Test with multiple households/users

**Files to Review:**
- `apps/life_os/backend/otto/context.py`
- All API endpoints in `apps/life_os/backend/`

---

### 3. Vendor and Pattern Parsing Improvements

**Current Status:** Simple parsing works but could be more robust

**Action Items:**

**Reminder Pattern Parsing:**
- [ ] Formalize pattern format (e.g., JSON structure or strict syntax)
- [ ] Add validation helper function
- [ ] Document pattern format in `CONTROL_OTTO_LONG_TERM_MEMORY.md`
- [ ] Consider examples:
  - `{"days": [7, 1, 0]}` (structured)
  - `"7/1/0"` (compact format)
  - `"week/day/day-of"` (named format)

**Vendor Name Normalization:**
- [ ] Add normalization helper function (strip punctuation, case-insensitive)
- [ ] Normalize vendor names when:
  - Creating vendor hint memories
  - Looking up vendor hints
- [ ] Handle edge cases:
  - "T.K.S" vs "TKS"
  - "Home Depot" vs "HOME DEPOT"
  - Whitespace variations

**Files to Update:**
- `apps/otto/otto/skills/memory_helpers.py`
- `apps/otto/otto/skills/tax_brain.py`

---

### 4. Review Memory Console UI

**Current Status:** UI implemented but needs manual testing

**Action Items:**
- [ ] Navigate to `/otto/memory` in Life OS
- [ ] Test filters (category, tag, source, stale status)
- [ ] Test search functionality
- [ ] Create/edit a memory and verify:
  - [ ] New version is created in history
  - [ ] Version number increments
  - [ ] History entry shows previous state
- [ ] Test mark stale functionality
- [ ] Test set expiration functionality
- [ ] Verify links are displayed correctly
- [ ] Check for any UI glitches or styling issues

**Location:** `apps/life_os/frontend/app/otto/memory/page.tsx`

---

## Future Enhancements (Post-Phase 4)

### High Priority

1. **Version Restore**
   - Add ability to restore previous versions from history
   - Action: `memory.restore_version`
   - UI button in Memory Console

2. **Bulk Operations**
   - Mark multiple memories stale at once
   - Set expiration for multiple memories
   - UI checkboxes + bulk action buttons

3. **Pattern Format Standardization**
   - Define formal pattern format
   - Migration helper for existing patterns
   - Validation on create/update

4. **Vendor Normalization**
   - Implement normalization helper
   - Update existing vendor hints
   - Document normalization rules

### Medium Priority

5. **Memory Analytics Dashboard**
   - Usage trends over time
   - Most-used memories
   - Stale memory cleanup suggestions
   - Category distribution

6. **Advanced Search**
   - Full-text search index (PostgreSQL `tsvector` or similar)
   - Fuzzy matching for typos
   - Search across history entries

7. **Memory Templates**
   - Pre-defined structures for common patterns
   - Template library (reminder patterns, tax hints, etc.)
   - Quick-create from template

### Lower Priority

8. **Memory Import/Export**
   - JSON export of memories
   - Import from backup
   - Household migration support

9. **Memory Confidence Decay**
   - Reduce confidence if unused for X days
   - Automatic decay rules
   - Manual confidence adjustment

10. **Memory Relationships UI**
    - Visual graph of memory links
    - Navigate between related memories
    - Relationship type filtering

---

## Testing Checklist

### Manual Testing

- [ ] **Memory CRUD**
  - [ ] Create memory via API
  - [ ] Update memory (verify history)
  - [ ] Delete memory (verify final history entry)
  - [ ] List memories with filters

- [ ] **History**
  - [ ] View history via API
  - [ ] View specific version
  - [ ] Verify history preserved after deletion

- [ ] **Expiration & Stale**
  - [ ] Mark memory as stale
  - [ ] Set expiration date
  - [ ] Run maintenance worker
  - [ ] Verify expired memories marked stale
  - [ ] Test skill behavior with stale memories

- [ ] **Links**
  - [ ] Create link via API
  - [ ] List links for memory
  - [ ] Delete link
  - [ ] Verify links created by skills

- [ ] **Search**
  - [ ] Search by text query
  - [ ] Filter by category/tag/source/stale
  - [ ] Test pagination
  - [ ] Test via `memory.search` action

- [ ] **UI**
  - [ ] Open Memory Console
  - [ ] Filter memories
  - [ ] Search memories
  - [ ] View memory details
  - [ ] Edit memory (verify version increment)
  - [ ] Mark stale from UI
  - [ ] Set expiration from UI
  - [ ] View history in UI
  - [ ] View links in UI

### Automated Testing

- [ ] Extend `test_otto_phase3.py` with Phase 4 features
- [ ] Add tests for maintenance worker
- [ ] Add tests for link creation by skills
- [ ] Add UI integration tests (if framework available)

---

## Notes

- All Phase 4 features are implemented and follow meta-rules
- Backward compatibility maintained
- Safety tiers respected
- Documentation updated

**Next Phase:** After cleanup and testing, consider Phase 5 based on priorities and user needs.

