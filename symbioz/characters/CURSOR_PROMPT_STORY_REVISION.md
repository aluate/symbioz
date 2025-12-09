# Cursor Prompt: Story Revision & Master File Creation

**Purpose:** Revise all 10 character stories based on Devil's Advocate reviews, apply standardization, create canonical master documents, and combine into a single master file for audio narration.

**Process:** Revise stories one-by-one. Only proceed to next story after current story passes all checks. After all 10 are revised, create master documents and combine into single file.

---

## Phase 1: Individual Story Revision (Stories 01-10)

### For Each Story (01 through 10):

#### Step 1: Read the Story and Its DAC Review
- Read: `symbioz/characters/stories/STORY_XX_[Character]_[Name].md`
- Read: `symbioz/characters/stories/STORY_XX_[Character]_[Name]_DEVILS_ADVOCATE.md`
- Understand all suggested fixes and improvements

#### Step 2: Apply All DAC Suggested Fixes AUTOMATICALLY
**This is critical - apply EVERY fix listed in the DAC review:**

**Common Fix Categories:**

1. **Pronoun/Wording Clarifications**
   - Apply all pronoun fixes
   - Fix accidental word choices
   - Standardize terminology

2. **Bio Summary vs Story Mismatch**
   - If story changes, UPDATE bio summary to match
   - Stories are FIRST TRUTH - bios must align
   - Update `BIO_SUMMARIES.md` immediately

3. **Timeline Years**
   - Highlight all timeline years explicitly
   - Ensure consistency with shared events
   - Verify birth years, event years, current age

4. **Honey Phrasing Standardization**
   - ❌ WRONG: "honey running through his system" (years later)
   - ✅ CORRECT: "the strength that Ironflower honey had given him" (permanent enhancement from childhood)
   - ✅ CORRECT: "felt the Ironflower-enhanced strength in his muscles—the permanent gift from his father's smuggled honey"
   
   **Honey Rules:**
   - **Can enhance development during growth years** → permanent stat effects
   - **Can temporarily buff performance** when consumed in adulthood
   - **CANNOT be felt later as physical presence** years after ingestion
   - **CANNOT grant magical-style powers**
   - **Cannot "run through" people years after ingestion**

5. **Amber Terminology Standardization**
   - ❌ WRONG: "resistance to Amber"
   - ✅ CORRECT: "survived Amber exposure" or "knew its dangers"
   - ❌ WRONG: "biological adaptation to Amber"
   - ✅ CORRECT: "psychological scars" or "enhanced perception" or "risk of mutation"
   
   **Amber Rules:**
   - **Amber exposure grants:**
     - Psychological scars
     - Enhanced perception
     - Risk of mutation or instability
     - Specialized knowledge or intuition
   - **Amber DOES NOT grant:**
     - Resistance
     - Immunity
     - Smooth acceptance
   - **Amber should always feel:**
     - Dangerous
     - Reality-distorting
     - Capable of killing even prepared experts

6. **Shared Event Consistency (Especially Gamma-7)**
   - For stories involving Outpost Gamma-7 (Kaelen #1, Mara #5, Vex #6, Kresh #7):
     - Match canonical event details exactly
     - Use standardized terminology
     - Align timeline, participants, sequence
   - If DAC suggests clarification, apply it
   - **If DAC fix forces a choice (e.g., who touched Amber fragment), the story becomes canonical truth - lore bibles should NOT rewrite stories. Stories lead canon.**

#### Step 3: Apply Standardization Requirements

**A. Political Reputation Matrix**
At the end of each story, add:

```
---

## POLITICAL REPUTATION MATRIX

| Faction | Reputation | Notes |
|---------|------------|-------|
| Wardens of the Reach | [Status] | [Reason] |
| Horizon Combine | [Status] | [Reason] |
| Confluence Cartel | [Status] | [Reason] |
| Resistance Cells | [Status] | [Reason] |
| Independent Operators | [Status] | [Reason] |
| Outpost K-77 (The Spindle) | [Status] | [Reason] |

**Faction Relationship Details:**
- [Specific details about relationship with each faction]
- [Why this reputation exists]
- [How it affects character's operations]
```

**B. Canon Ledger Entry**
At the end of each story, add:

```
---

## CANON LEDGER ENTRY

### Planets Referenced:
- **[Planet Name]:** [Nature, faction control, key details]

### Honey Types Used:
- **[Honey Type]:** [Source planet, mechanical buffs, rarity]

### Factions Encountered:
- **[Faction Name]:** [Ideology, major conflicts, character's relationship]

### Shared Events:
- **[Event Name]:** [Date, who was there, mechanical consequences, character's role]

### Timeline Anchor Points:
- **Birth Year:** [Year]
- **Major Events:** [Year - Event]
- **Current Age/Status:** [Age or status]

### Mechanical Perks Tied to Backstory:
- **[Perk/Stat Bonus]:** [Reason from backstory]

### Character Relationships:
- **[Character Name]:** [Relationship type, awareness level, history]
```

**C. Shared Event Master Recap (If Applicable)**
For stories involving Outpost Gamma-7 Amber Channeling event:

At the end of the story, add:

```
---

## GAMMA-7 AMBER CHANNELING EVENT - CANONICAL RECAP

**Event Date:** 5 years ago  
**Location:** Outpost Gamma-7  
**Participants:** 
- Kaelen Voss (Human Vanguard)
- Tessa (Warden Vanguard)
- Mara Deep-Current (Ærathi Pioneer - Warden at time)
- Vex Three-Stance (Vazari Reclaimer)
- Kresh Four-Arm (Ash-Khadd Warden - arrived later)

**Sequence of Events:**
1. [Canonical sequence from master event - standardize across all 4 stories]
2. [Who discovered what]
3. [Who touched the artifact]
4. [What happened during channeling]
5. [Containment protocol]
6. [Casualties and consequences]

**Character's Role in Event:** [This character's specific perspective and actions]

**Character's Interpretation:** [How this character saw/interprets the event]

**Post-Event Consequences:**
- [Immediate effects]
- [Long-term consequences]
- [Character's path after event]

**Mechanical Implications:**
- [Amber exposure effects on character]
- [Permanent changes]
- [Specialized knowledge gained]
```

#### Step 4: Update Downstream Documents
After revising each story:

1. **Update BIO_SUMMARIES.md**
   - If story details changed, update bio summary to match
   - Stories are FIRST TRUTH

2. **Update CHARACTER_ROSTER.md** (if needed)
   - Update any details that changed in story
   - Stories are FIRST TRUTH

3. **Update Mechanical Notes**
   - Ensure mechanical notes align with revised story
   - Add any new mechanical implications

#### Step 5: Re-Run Devil's Advocate Check
After applying all fixes:

**Check:**
- [ ] All DAC suggested fixes applied
- [ ] Honey terminology standardized
- [ ] Amber terminology standardized
- [ ] Shared events match canonical details
- [ ] Timeline years explicit and consistent
- [ ] Political Reputation Matrix added
- [ ] Canon Ledger Entry added
- [ ] Shared Event Recap added (if applicable)
- [ ] Bio summaries updated
- [ ] No remaining inconsistencies

**If story passes all checks:** Mark as COMPLETE and proceed to next story.

**If story has remaining issues:** Fix issues, re-check, then proceed.

---

## Phase 2: Cross-Story Harmonization Pass

### After All 10 Stories Are Revised:

#### Step 1: Read All 10 Revised Stories Simultaneously
- Load all 10 story files
- Scan for contradictions across stories

#### Step 2: Harmonization Checklist

**A. Shared Events Validation:**
- [ ] Outpost Gamma-7 event details identical across all 4 stories (Kaelen #1, Mara #5, Vex #6, Kresh #7)
- [ ] Timeline years consistent
- [ ] Participants list matches
- [ ] Sequence of events matches
- [ ] Consequences align

**B. Character Relationship Validation:**
- [ ] If Story A mentions Character B, verify Story B's perspective aligns
- [ ] Relationship types consistent (ally, rival, neutral, etc.)
- [ ] Awareness levels match (do they know each other? How well?)
- [ ] Shared history aligns

**C. Faction Stance Validation:**
- [ ] Combine law structure consistent
- [ ] Warden procedure consistent
- [ ] Cartel operations consistent
- [ ] Faction ideology aligns across stories

**D. Honey & Amber Validation:**
- [ ] Honey mechanics consistent (permanent vs temporary)
- [ ] Amber effects consistent (danger, reality-distorting, etc.)
- [ ] Terminology standardized across all stories
- [ ] No "magical" Honey effects
- [ ] No "resistance" to Amber (only survival/knowledge)

**E. Timeline Validation:**
- [ ] Birth years don't conflict
- [ ] Event years align
- [ ] Age progression makes sense
- [ ] Shared events occur at same time

**F. Location Validation:**
- [ ] Planet descriptions consistent
- [ ] Station layouts consistent
- [ ] The Spindle details consistent

#### Step 3: Fix Any Contradictions Found
- If contradictions found, resolve using:
  - **Stories are FIRST TRUTH** - canonical events in stories override other sources
  - If two stories conflict, use the more detailed/central story as canonical
  - Update both stories to align if needed

#### Step 4: Create Harmonization Report
Generate: `symbioz/characters/HARMONIZATION_REPORT.md`

**Report Should Include:**
- Contradictions found and how resolved
- Alignment wins (things that work perfectly)
- Cross-story connections validated
- Areas of perfect consistency

---

## Phase 3: Master Document Creation

### Create the Following Documents:

#### 1. **GAMMA-7_MASTER_EVENT_RECAP.md**
**Location:** `symbioz/characters/GAMMA-7_MASTER_EVENT_RECAP.md`

**Contents:**
- Complete canonical sequence of events
- All participants and their roles
- Exact timeline
- Reality-warping effects
- Containment protocol details
- Casualties and consequences
- Post-event character paths
- This becomes the **keystone reference** for future content

#### 2. **STORY_CANON_LEDGER.md** (Global)
**Location:** `symbioz/characters/STORY_CANON_LEDGER.md`

**Format:**
```
# Story Canon Ledger - Global

## Planets
| Planet Name | Nature | Faction Control | Key Details |
|-------------|--------|-----------------|-------------|
| [Planet] | [Type] | [Faction] | [Details] |

## Honey Types
| Honey Type | Source Planet | Mechanical Buffs | Rarity |
|------------|---------------|------------------|--------|
| [Type] | [Planet] | [Effects] | [Rarity] |

## Factions
| Faction | Ideology | Major Conflicts | Territory |
|---------|----------|-----------------|-----------|
| [Faction] | [Ideology] | [Conflicts] | [Territory] |

## Shared Events
| Event Name | Date | Participants | Consequences |
|------------|------|--------------|--------------|
| [Event] | [Year] | [Who] | [Results] |

## Timelines
| Character | Birth Year | Major Events | Current Status |
|-----------|-----------|--------------|----------------|
| [Name] | [Year] | [Events] | [Status] |

## Mechanical Perks
| Character | Perk/Stat Bonus | Backstory Reason |
|-----------|-----------------|------------------|
| [Name] | [Bonus] | [Reason] |

## Relationships
| Character A | Character B | Relationship Type | Awareness | History |
|-------------|-------------|-------------------|-----------|---------|
| [Name] | [Name] | [Type] | [Level] | [Details] |
```

#### 3. **POLITICAL_REPUTATION_MATRIX.md**
**Location:** `symbioz/characters/POLITICAL_REPUTATION_MATRIX.md`

**Contents:**
- Matrix showing each character's reputation with each faction
- Allows for:
  - Pricing modifiers
  - NPC reactions
  - Escort request probability
  - Black market access
  - Mission availability

#### 4. **MECHANICAL_PERK_MATRIX.md**
**Location:** `symbioz/characters/MECHANICAL_PERK_MATRIX.md`

**Contents:**
- Each character's stat bonuses tied to backstory
- Honey/Amber effects on character
- Class/race trait justifications
- Equipment preferences
- Ability specializations

#### 5. **RELATIONSHIP_NETWORK_MAP.md**
**Location:** `symbioz/characters/RELATIONSHIP_NETWORK_MAP.md`

**Contents:**
- Visual/textual map of character relationships
- Alliances, tensions, debts, conflicts
- Cross-story connection points
- Questline opportunities

#### 6. **FACTION_PRESENCE_BY_WORLD.md**
**Location:** `symbioz/characters/FACTION_PRESENCE_BY_WORLD.md`

**Contents:**
- Which factions control/operate on which planets
- Territory claims
- Economic interests
- Conflict zones

#### 7. **HONEY_AMBER_RULES_SHEET.md**
**Location:** `symbioz/characters/HONEY_AMBER_RULES_SHEET.md`

**Contents:**
- Standardized Honey mechanics
- Standardized Amber mechanics
- Terminology glossary
- What Honey CAN/CANNOT do
- What Amber CAN/CANNOT do
- This becomes the **authoritative reference** for all future content

---

## Phase 4: Master File Creation

### After All Master Documents Created:

#### Step 1: Create Combined Master File
**File:** `symbioz/characters/ALL_CHARACTER_STORIES_MASTER.md`

**Structure:**
1. **Header/Metadata**
   - Project name
   - Total word count
   - Generation date
   - Status: Revised and Harmonized

2. **Table of Contents**
   - All 10 stories listed
   - Master documents referenced

3. **Introduction Section**
   - Universe overview
   - Story purpose
   - Usage guidelines

4. **All 10 Stories (In Order: 01-10)**
   - Complete revised text
   - Include Political Reputation Matrix
   - Include Canon Ledger Entry
   - Include Shared Event Recap (if applicable)

5. **Master Reference Section**
   - Gamma-7 Master Event Recap (full details)
   - Story Canon Ledger (summary/links)
   - Political Reputation Matrix (summary)
   - Mechanical Perk Matrix (summary)
   - Relationship Network Map (summary)
   - Faction Presence by World (summary)
   - Honey & Amber Rules Sheet (full)

6. **Appendices**
   - Timeline of major events
   - Character cross-reference
   - Faction overview

#### Step 2: Final Atmospheric Pass

**Apply to the entire master file:**

**Tone Refinement:**
- Tighten prose rhythm
- Amplify shadow and industrial texture
- Push moral ambiguity
- Dark CDA tone should hit like:
  - Andor
  - Metro
  - The Expanse
  - Raised by Wolves
- Borderline corporate-colonial gothic

**Language Consistency:**
- Standardize terminology throughout
- Ensure consistent voice
- Polish transitions between stories

**Formatting for Audio:**
- Mark section breaks clearly
- Ensure smooth narrative flow
- Prepare for stage direction insertion (later step - NOT in this pass)

#### Step 3: Final Validation

**Check:**
- [ ] All 10 stories included and revised
- [ ] All DAC fixes applied
- [ ] All standardization requirements met
- [ ] Cross-story harmonization complete
- [ ] All master documents referenced
- [ ] Tone consistent throughout
- [ ] No contradictions remain
- [ ] Ready for audio narration (stage directions to be added later)

---

## Success Criteria

### Individual Story Revision:
- ✅ All DAC suggested fixes applied
- ✅ Honey/Amber terminology standardized
- ✅ Political Reputation Matrix added
- ✅ Canon Ledger Entry added
- ✅ Shared Event Recap added (if applicable)
- ✅ Bio summaries updated
- ✅ Story passes all checks

### Cross-Story Harmonization:
- ✅ No contradictions between stories
- ✅ Shared events perfectly aligned
- ✅ Character relationships consistent
- ✅ Faction stances aligned
- ✅ Timeline consistent
- ✅ Harmonization report created

### Master Documents:
- ✅ Gamma-7 Master Event Recap created
- ✅ Story Canon Ledger created
- ✅ Political Reputation Matrix created
- ✅ Mechanical Perk Matrix created
- ✅ Relationship Network Map created
- ✅ Faction Presence by World created
- ✅ Honey & Amber Rules Sheet created

### Master File:
- ✅ All 10 revised stories combined
- ✅ All master documents integrated/referenced
- ✅ Final atmospheric pass applied
- ✅ Ready for audio narration
- ✅ Professional quality, AAA-tier material

---

## Files to Work With

### Input Files:
- `symbioz/characters/stories/STORY_01_Kaelen_Voss.md` + DAC
- `symbioz/characters/stories/STORY_02_Thorn_Ironhand.md` + DAC
- `symbioz/characters/stories/STORY_03_Lysara_Void-Touch.md` + DAC
- `symbioz/characters/stories/STORY_04_Dr_Zara_Mesh-Bond.md` + DAC
- `symbioz/characters/stories/STORY_05_Mara_Deep-Current.md` + DAC
- `symbioz/characters/stories/STORY_06_Vex_Three-Stance.md` + DAC
- `symbioz/characters/stories/STORY_07_Kresh_Four-Arm.md` + DAC
- `symbioz/characters/stories/STORY_08_Stalwart_Bone-Anchor.md` + DAC
- `symbioz/characters/stories/STORY_09_Prism_Light-Weaver.md` + DAC
- `symbioz/characters/stories/STORY_10_Dr_Reth_Hive-Mind.md` + DAC
- `symbioz/characters/BIO_SUMMARIES.md`
- `symbioz/characters/CHARACTER_ROSTER.md`

### Output Files:
- Revised versions of all 10 stories
- `symbioz/characters/GAMMA-7_MASTER_EVENT_RECAP.md`
- `symbioz/characters/STORY_CANON_LEDGER.md`
- `symbioz/characters/POLITICAL_REPUTATION_MATRIX.md`
- `symbioz/characters/MECHANICAL_PERK_MATRIX.md`
- `symbioz/characters/RELATIONSHIP_NETWORK_MAP.md`
- `symbioz/characters/FACTION_PRESENCE_BY_WORLD.md`
- `symbioz/characters/HONEY_AMBER_RULES_SHEET.md`
- `symbioz/characters/HARMONIZATION_REPORT.md`
- `symbioz/characters/ALL_CHARACTER_STORIES_MASTER.md` (Final Combined File)

### Reference Files:
- `symbioz/characters/STORY_REVIEW_EXPANSION.md`
- `symbioz/characters/STORY_UNIVERSE_INSIGHTS.md`
- `symbioz/characters/FRAT_REVIEW_RESPONSE.md`

---

## Important Principles

1. **Stories are FIRST TRUTH** - Stories lead canon. Lore bibles should update to match stories, not rewrite them.

2. **If DAC fix forces a choice** - The story becomes canonical truth.

3. **Apply ALL fixes** - Don't skip any DAC suggestions.

4. **One story at a time** - Only proceed after current story passes all checks.

5. **Standardization is key** - Honey/Amber terminology must be consistent across all stories.

6. **Cross-validation is critical** - After all revisions, harmonize across all 10 stories.

7. **Master documents enable future work** - These will support quest design, NPC creation, mission generation.

8. **Quality bar is high** - This should be AAA-tier, publication-ready material.

---

## Process Flow

```
Phase 1: Individual Revision (01-10)
├── Story 01: Read → Apply DAC Fixes → Standardize → Update Bios → Re-check → ✅
├── Story 02: Read → Apply DAC Fixes → Standardize → Update Bios → Re-check → ✅
├── Story 03: Read → Apply DAC Fixes → Standardize → Update Bios → Re-check → ✅
├── Story 04: Read → Apply DAC Fixes → Standardize → Update Bios → Re-check → ✅
├── Story 05: Read → Apply DAC Fixes → Standardize → Update Bios → Re-check → ✅
├── Story 06: Read → Apply DAC Fixes → Standardize → Update Bios → Re-check → ✅
├── Story 07: Read → Apply DAC Fixes → Standardize → Update Bios → Re-check → ✅
├── Story 08: Read → Apply DAC Fixes → Standardize → Update Bios → Re-check → ✅
├── Story 09: Read → Apply DAC Fixes → Standardize → Update Bios → Re-check → ✅
└── Story 10: Read → Apply DAC Fixes → Standardize → Update Bios → Re-check → ✅

Phase 2: Cross-Story Harmonization
├── Read all 10 stories simultaneously
├── Validate shared events
├── Validate relationships
├── Validate faction stances
├── Fix contradictions
└── Create harmonization report

Phase 3: Master Document Creation
├── Gamma-7 Master Event Recap
├── Story Canon Ledger
├── Political Reputation Matrix
├── Mechanical Perk Matrix
├── Relationship Network Map
├── Faction Presence by World
└── Honey & Amber Rules Sheet

Phase 4: Master File Creation
├── Combine all 10 revised stories
├── Integrate master documents
├── Apply final atmospheric pass
└── Create ALL_CHARACTER_STORIES_MASTER.md

✅ COMPLETE - Ready for audio narration (stage directions to be added later)
```

---

**This prompt ensures all 10 stories are revised, standardized, harmonized, and combined into a single master file of AAA-tier quality, ready for audio narration preparation.**

