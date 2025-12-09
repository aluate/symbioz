# Phase 5 Roadmap - MVP Polish & Completion

**Status**: Planning  
**Goal**: Complete the MVP experience with polish and missing features

---

## 🚨 Priority 0: Lore/Data Binding Layer (FOUNDATIONAL - DO FIRST)

**Status**: Critical foundation before other work  
**Why**: Makes lore first-class game data, prevents story/mechanic drift, enables systemic gameplay

### 0.1. Core Lore Data Structure
**Tasks**:
- [ ] Create `symbioz/data/lore/` directory structure
- [ ] Design JSON schemas for all lore entities
- [ ] Migrate existing race/class data to include lore metadata
- [ ] Create unified data loader that reads from lore files

**Files to Create**:
```
symbioz/data/lore/
  races.json          (enhanced with cultural traits, honey affinity, etc.)
  classes.json        (enhanced with faction alignment, amber risk, etc.)
  honey.json          (all honey types with mechanical + lore data)
  amber.json          (amber effects, psychology risks, channeling rules)
  factions.json       (faction attitudes, rules of engagement)
  planets.json        (world data, honey sources, faction control)
  shared_events.json  (Gamma-7, timeline events, consequences)
```

**Estimated Time**: 4-5 hours

---

### 0.2. Faction Reputation System
**Tasks**:
- [ ] Create `faction_reputation_rules.json` with attitude modifiers
- [ ] Implement faction calculation based on race/class/story flags
- [ ] Wire faction reputation to vendor prices/availability
- [ ] Add faction display to character sheet

**Estimated Time**: 3-4 hours

---

### 0.3. Gamma-7 Event Codification
**Tasks**:
- [ ] Create `shared_events/gamma7.json` with complete event data
- [ ] Link event to character stories
- [ ] Create quest foundation hooks
- [ ] Add event flags to character creation/background

**Estimated Time**: 2-3 hours

---

### 0.4. Canon Ledger as JSON
**Tasks**:
- [ ] Convert `STORY_CANON_LEDGER.md` to `canon_ledger.json`
- [ ] Structure character data with mechanical implications
- [ ] Link to faction reputation, honey affinity, amber exposure
- [ ] Create lookup system for NPCs/quests

**Estimated Time**: 3-4 hours

---

### 0.5. Character Relationship Atlas
**Tasks**:
- [ ] Create `connections/characters_graph.json`
- [ ] Map all character relationships from stories
- [ ] Include trust levels, knowledge depth
- [ ] Create system for NPC dialogue hooks

**Estimated Time**: 2-3 hours

---

### 0.6. Portrait Metadata System
**Tasks**:
- [ ] Create `data/portraits/` structure with JSON metadata
- [ ] Link portraits to race/class/canon data
- [ ] Include generation prompts, style hashes
- [ ] Enable automatic portrait selection

**Estimated Time**: 1-2 hours

---

**Total Priority 0 Time**: ~15-21 hours

**Why This Matters**: 
- Lore becomes game data, not just documentation
- Mechanics derive from lore automatically
- UI displays canonical information
- Systems reference same source of truth
- Story and gameplay stay in sync
- Enables faction-based gameplay, honey compatibility, amber risks, etc.

**This transforms Symbioz from "a cool text RPG" into "a narratively integrated simulation universe."**

---

## Priority 1: Complete Existing Systems

### 1. Vendor System UI ✅ Backend Ready
**Status**: Backend complete, UI needs wiring

**Tasks**:
- [ ] Wire vendor purchase flow in HubScreen
- [ ] Show purchased items in inventory
- [ ] Display item stats/descriptions
- [ ] Handle insufficient credits gracefully
- [ ] Show equipped vs available items

**Estimated Time**: 2-3 hours

---

### 2. Skill Mission UI
**Status**: Backend ready, UI not implemented

**Tasks**:
- [ ] Create SkillMissionScreen component
- [ ] Display skill check descriptions
- [ ] Show roll results with animations
- [ ] Handle success/failure outcomes
- [ ] Return to hub with appropriate rewards

**Estimated Time**: 3-4 hours

---

### 3. Character Images
**Status**: Placeholders only

**Tasks**:
- [ ] Generate character portraits using `VISUAL_STYLE_GUIDE.md`
- [ ] Generate enemy portraits
- [ ] Add images to `public/symbioz/characters/`
- [ ] Add images to `public/symbioz/enemies/`
- [ ] Update CombatScreen to display images
- [ ] Update CharacterCreation to show race/class previews

**Estimated Time**: 2-3 hours (image generation) + 1 hour (integration)

---

## Priority 2: UX Improvements

### 4. Better Error Handling
**Status**: Basic error handling exists

**Tasks**:
- [ ] User-friendly error messages
- [ ] Loading states for all async operations
- [ ] Retry mechanisms for failed API calls
- [ ] Connection status indicator
- [ ] Graceful degradation if API unavailable

**Estimated Time**: 2-3 hours

---

### 5. Multiple Enemies UI
**Status**: Works but could be better

**Tasks**:
- [ ] Better layout for 2+ enemies
- [ ] Enemy selection highlighting
- [ ] Clearer enemy health bars
- [ ] Enemy status effects display
- [ ] Turn order indicator

**Estimated Time**: 2-3 hours

---

### 6. Combat Polish
**Status**: Functional but basic

**Tasks**:
- [ ] Combat animations/transitions
- [ ] Damage number popups
- [ ] Status effect indicators
- [ ] Turn indicator improvements
- [ ] Victory/defeat screens
- [ ] Sound effects (optional)

**Estimated Time**: 4-5 hours

---

## Priority 3: Content Expansion

### 7. More Missions
**Status**: 3 missions currently

**Tasks**:
- [ ] Add 2-3 more combat missions
- [ ] Add 1-2 more skill missions
- [ ] Vary difficulty levels
- [ ] Add mission descriptions/flavor text
- [ ] Better mission rewards variety

**Estimated Time**: 3-4 hours

---

### 8. More Enemies
**Status**: Limited enemy variety

**Tasks**:
- [ ] Add 2-3 new enemy types
- [ ] Vary enemy stats/abilities
- [ ] Add enemy descriptions
- [ ] Create enemy images

**Estimated Time**: 2-3 hours

---

## Priority 4: Technical Improvements

### 9. Session Persistence
**Status**: In-memory only

**Tasks**:
- [ ] Add save/load functionality
- [ ] Store sessions in file or database
- [ ] Character save slots
- [ ] Resume game after restart

**Estimated Time**: 4-5 hours

---

### 10. Performance & Optimization
**Status**: Not optimized

**Tasks**:
- [ ] Optimize API calls (batching, caching)
- [ ] Reduce re-renders in React
- [ ] Lazy load images
- [ ] Code splitting for web UI
- [ ] API response optimization

**Estimated Time**: 3-4 hours

---

## Phase 5 Success Criteria

Phase 5 is complete when:

1. ✅ Vendor system fully functional in UI
2. ✅ Skill missions playable through web UI
3. ✅ Character/enemy images displayed
4. ✅ Error handling is user-friendly
5. ✅ Multiple enemies display clearly
6. ✅ Combat feels polished and responsive
7. ✅ At least 5-6 total missions available
8. ✅ Game can be saved and resumed

---

## Recommended Phase 5 Order

**Week 0: Foundation (CRITICAL - DO FIRST)**
1. Core Lore Data Structure (Priority 0.1)
2. Faction Reputation System (Priority 0.2)
3. Gamma-7 Event Codification (Priority 0.3)
4. Canon Ledger as JSON (Priority 0.4)
5. Character Relationship Atlas (Priority 0.5)
6. Portrait Metadata System (Priority 0.6)

**Week 1: Complete Systems**
1. Vendor System UI (Priority 1) - Now uses faction reputation!
2. Skill Mission UI (Priority 1)
3. Character Images (Priority 1) - Now uses portrait metadata!

**Week 2: Polish**
4. Error Handling (Priority 2)
5. Multiple Enemies UI (Priority 2)
6. Combat Polish (Priority 2)

**Week 3: Content**
7. More Missions (Priority 3) - Now lore-anchored with factions/events!
8. More Enemies (Priority 3)

**Week 4: Technical**
9. Session Persistence (Priority 4)
10. Performance (Priority 4)

---

## After Phase 5

Once Phase 5 is complete, the MVP will be **feature-complete and polished**. Next steps:

- **Playtesting**: Get real player feedback
- **Balance Tuning**: Adjust combat difficulty, XP curves, etc.
- **Phase 6 Planning**: Decide on expansion (more races/classes, Amber magic, etc.)

---

**Total Estimated Time**: ~45-61 hours (including Priority 0)

**Recommendation**: 
1. **CRITICAL**: Complete Priority 0 first (foundational data layer) - ~15-21 hours
2. Then Priority 1 (complete existing systems) - ~8-11 hours
3. Then Priority 2 (polish) - ~8-11 hours
4. Then Priority 3 (content) - ~5-7 hours
5. Finally Priority 4 (technical) - ~7-9 hours

**Why Priority 0 First**: 
- Makes all subsequent work easier (systems can reference lore data)
- Prevents story/mechanic drift
- Enables faction-based gameplay, honey compatibility, amber risks
- Transforms Symbioz into a narratively integrated simulation universe

