# CURSOR PROMPT: Symbioz Character Story Generation
## With Full Cross-Validation, Word Counts, and Dark CDA Tone

**SYSTEM DIRECTIVE:**

You are generating canonical character stories for the Symbioz universe. These 10 characters will become the foundation for quest lines, companions, NPCs, and narrative hooks throughout the game.

**CRITICAL REQUIREMENT:** All 10 stories must be internally consistent with each other. Characters who share worlds, factions, timelines, or events must acknowledge each other appropriately, even if their perspectives differ.

---

## MANDATORY FILES TO READ BEFORE STARTING

Before producing ANY content, read and understand:

1. `symbioz/design/LORE_BIBLE.md` (if exists - otherwise work from existing design docs)
2. `symbioz/design/MVP_SCOPE.md`
3. `symbioz/design/COMBAT_SYSTEM.md`
4. `symbioz/design/GAMEPLAY_LOOP.md`
5. `symbioz/design/VISUAL_STYLE_GUIDE.md`
6. `apps/symbioz_cli/data/races.json`
7. `apps/symbioz_cli/data/classes.json`
8. `apps/symbioz_cli/data/honey.json` (if exists)
9. `apps/symbioz_cli/data/weapons.json` (if exists)
10. `apps/symbioz_cli/data/missions.json` (if exists)

**Hold in memory:**
- All 10 races (use full vision, not just MVP 3)
- All 8 classes (+ NPC Channeler)
- Honey/Amber mechanics and rarity rules
- Faction tensions and relationships
- Race/class restrictions and synergies
- Implant availability and laws
- Weapon types and restrictions
- Timeline and political geography

---

## STEP 1: CREATE CHARACTER ROSTER

**Output File:** `symbioz/characters/CHARACTER_ROSTER.md`

**Requirements for 10 Characters:**

### Roster Composition Rules:

1. **Unique Race/Class Pairs:** No two characters share the same race + class combination
2. **Diversity Requirements:**
   - At least 4 characters must be non-humanoid races (Sylarin, Ærathi, Vazari, Ash-Khadd, Orm-Shun, Thalesari, Yntari)
   - At least 3 characters entangled with major political powers (Wardens, Combine, Cartel, or national blocs)
   - At least 2 characters with deep ties to Honey trade/smuggling networks
   - At least 1 Pioneer who uncovered ancient biosphere/Honey secrets
   - At least 1 character permanently altered by Honey mutation (physical, psychological, or both)
   - At least 1 character who witnessed (but cannot explain) an Amber Channeling event
   - At least 1 character scarred by Amber exposure (near-miss, radiation, etc.)

3. **Stereotype Subversion:** Every character must challenge at least one stereotype of their race or class

### Roster Table Format:

For each character, record:

| Field | Description |
|-------|-------------|
| **Name** | Full name + any aliases |
| **Race** | One of 10 playable races |
| **Class** | One of 8 playable classes |
| **Homeworld** | Planet/system name (must align with lore geography) |
| **Native Honey Strain** | Honey type from their world (check lore for planet assignments) |
| **Current Faction** | Primary affiliation(s) - can be multiple |
| **Age Range** | Approximate age (relative to race lifespan) |
| **Key Stereotype Subverted** | How they break expected norms |
| **Mechanical Hooks** | Gameplay-relevant traits (weapons, restrictions, perks, penalties) |
| **Present Situation** | 1 sentence: where they are now, what they're doing |
| **Shared History** | Names of other characters in roster who share timeline/faction/location events |

**Stop after creating roster. Wait for user approval before proceeding.**

---

## STEP 2: CREATE BIOGRAPHICAL SUMMARIES

**Output File:** `symbioz/characters/BIO_SUMMARIES.md`

**Format:** 2-3 paragraphs per character, 200-300 words each

**Each summary must establish:**

1. **Upbringing:** Family, homeworld conditions, early political/cultural context
2. **Key Influences:** How Honey economy, faction tensions, or Amber events shaped them
3. **Early Conflicts:** First major challenge, betrayal, loss, or choice
4. **Path to Current Class:** How they became Vanguard/Operative/etc. (training, necessity, accident)
5. **Faction Entanglements:** Current and past affiliations, debts, enemies
6. **Amber/Honey Exposure:** Direct encounters, mutations, rumors witnessed
7. **Scars/Trauma:** Physical or psychological marks that affect gameplay
8. **Present Stakes:** What they're fighting for, running from, or seeking

**Cross-Reference Notes:**
- If two characters share a world/event/faction, note it: "Shared history with Character X"
- If timelines overlap, note temporal relationships: "Active during same period as Character Y"
- If they should know each other but don't, explain why: "Never met due to class divisions"

**Stop and wait for user approval.**

---

## STEP 3: WRITE FULL STORY #1 (ONE AT A TIME)

**Output File:** `symbioz/characters/stories/STORY_01_<CHARACTER_NAME>.md`

**Word Count:** 1,800 - 2,600 words (strict enforcement)

**Format:** Narrative prose, third-person limited or tight-zoom omniscient focused on the character

### Story Structure:

1. **Opening Scene (200-300 words):** A defining moment that shows who they are now
2. **Childhood/Early Years (400-500 words):** Homeworld, family, first conflicts
3. **Adolescence/Education (300-400 words):** Skills development, class training, first faction contact
4. **Young Adulthood/First Missions (400-500 words):** Early adventures, mistakes, relationships
5. **Crisis/Turning Point (400-500 words):** The event that defines their moral compass (must involve Honey or Amber pressure)
6. **Recent History (200-300 words):** How they got to their present situation
7. **Mechanical Notes Section (see below)**

### Tone Requirements:

**"Dark CDA" Style:**
- Gritty frontier sci-fi realism
- Industrial decay, harsh environments
- Moral ambiguity, no perfect heroes
- Practical violence, unromantic survival
- Philosophical undercurrent but grounded
- Quiet menace, subtle dread
- Economic anxiety, resource scarcity
- Hard choices with real consequences

**Writing Quality:**
- Show, don't tell
- Minimal dialogue (only when it matters)
- Sparse, precise prose
- No purple prose or exposition dumps
- Let worldbuilding emerge through details
- Violence has weight and aftermath
- Technology feels improvised, dangerous, lived-in

**Reference Tones:**
- KOTOR 2 (philosophical depth, moral ambiguity)
- The Expanse Season 1 (realism, economic pressure)
- Andor (grounded, political, character-driven)
- Taylor Sheridan frontier psychology (stubborn survivors, micro-politics)

### Content Requirements:

1. **Worldbuilding Integration:**
   - Reference specific planets, stations, factions from LORE_BIBLE
   - Show how political tensions affect daily life
   - Demonstrate Honey economy through practical details (costs, scarcity, effects)

2. **Mechanical Anchoring:**
   - Explain stat tendencies through life events
   - Justify class abilities through training/necessity
   - Show race traits as biological/cultural facts, not just numbers
   - Demonstrate faction reputation effects through narrative consequences
   - Establish access to implants/weapons through story context

3. **Amber/Honey Rules Compliance:**
   - Honey strains match lore rarity and planet assignments
   - Amber exposure has real, lasting consequences
   - Channeling remains mysterious, never fully explained
   - Effects match game mechanics (don't contradict combat system)

4. **No Meta Commentary:**
   - Story is in-universe, not a game manual
   - Never mention "game mechanics," "stats," "levels"
   - Never break fourth wall

### Mechanical Notes Section:

At the end of each story, include:

```markdown
## MECHANICAL NOTES

- [Stat modifiers or tendencies from backstory]
- [Faction reputation effects]
- [Honey/Amber exposure consequences]
- [Weapon/armor/implant access and restrictions]
- [Skill specialties tied to backstory]
- [Mission types they're suited for]
- [Known non-combat proficiencies]
- [Any gameplay-relevant traits or penalties]
```

**After writing Story #1, STOP. Wait for user approval before proceeding.**

---

## STEP 4: DEVIL'S ADVOCATE REVIEW #1

**Output File:** `symbioz/characters/stories/STORY_01_<CHARACTER_NAME>_DEVILS_ADVOCATE.md`

**Review Categories:**

### A. Lore Consistency Check

- [ ] Does the story contradict LORE_BIBLE.md?
- [ ] Are faction motivations consistent with lore?
- [ ] Do Honey strains match planet assignments?
- [ ] Are Amber rules followed correctly?
- [ ] Does the timeline fit established history?

### B. Mechanical Consistency Check

- [ ] Do stat/ability claims match race/class rules?
- [ ] Are implant/weapon access justified by rules?
- [ ] Does Honey exposure match game mechanics?
- [ ] Are faction effects consistent with systems?
- [ ] Can the character actually do what the story claims?

### C. Cross-Story Consistency Check

**CRITICAL:** Compare against:
- All other characters in the roster (even unwritten ones)
- Any previously written stories

Check for:
- [ ] Timeline conflicts (two characters in same place/time without acknowledgment)
- [ ] Faction stance contradictions
- [ ] Honey strain duplication/violations
- [ ] Shared events that should be acknowledged
- [ ] Character relationships that should exist but don't
- [ ] Geographic/logical impossibilities
- [ ] Economic inconsistencies (prices, scarcity, trade routes)

### D. Story Quality Check

- [ ] Word count within range (1,800-2,600)?
- [ ] Tone matches Dark CDA style?
- [ ] No meta commentary or fourth-wall breaks?
- [ ] Mechanical notes complete and accurate?
- [ ] Stereotype subversion clear?
- [ ] Character is distinct from others?

### E. Conflict Resolution Priority:

If contradictions are found, resolve in this order:

1. **Game Mechanics First** (can't contradict combat/honey/amber rules)
2. **Lore Bible Second** (must align with established world)
3. **Story Viability Third** (narrative coherence)
4. **Style Last** (tone can be adjusted)

**Output Format:**

```markdown
# Devil's Advocate Review: [Character Name]

## Lore Consistency
- Issue: [description]
- Fix: [recommendation]

## Mechanical Consistency
- Issue: [description]
- Fix: [recommendation]

## Cross-Story Consistency
- Conflict with Character X: [description]
- Shared Event: [how to harmonize]
- Timeline Issue: [resolution]

## Story Quality
- Issue: [description]
- Fix: [recommendation]

## Required Changes
[List of specific edits needed]
```

**Stop after review. Wait for user approval.**

---

## STEP 5: CORRECT AND HARMONIZE STORY #1

**Action Items:**

1. Apply all fixes from Devil's Advocate review
2. Update cross-story notes for shared history
3. Revise Mechanical Notes if needed
4. Ensure tone matches Dark CDA style
5. Verify word count still within range

**Output:** Updated `STORY_01_<CHARACTER_NAME>.md`

**Then create:** `symbioz/characters/stories/FINAL/STORY_01_<CHARACTER_NAME>.md`

This final version is the approved, canonical story.

**Stop and wait for approval of final version.**

---

## STEP 6: REPEAT FOR STORIES #2-10

**Process for Each Remaining Story:**

1. Write full story (1,800-2,600 words)
2. **Run cross-validation against ALL previously written stories**
3. Run Devil's Advocate review
4. Apply corrections
5. Create final version in `/FINAL/` folder

**CRITICAL:** As you write each new story, you MUST:

- Check against all previous stories for conflicts
- Acknowledge shared events/characters/locations appropriately
- Update cross-story relationship notes
- Ensure timeline consistency across all stories
- Maintain faction consistency across all stories

**If Story #5 references an event that Story #2 also experienced:**
- Perspectives can differ (even contradict on details)
- But core facts must align
- Characters should acknowledge each other if they met
- Shared world events must have consistent consequences

---

## STEP 7: FINAL CROSS-VALIDATION REPORT

**Output File:** `symbioz/characters/CROSS_STORY_VALIDATION_REPORT.md`

**Content:**

### Timeline Consistency Map
- Chronological list of major events across all 10 stories
- Character presence at each event
- Conflicts or gaps identified

### Shared Character Relationships
- Characters who know each other (directly or through reputation)
- Characters who should know each other but don't (with explanation)
- Missing connections that should exist

### Faction Consistency Check
- How each faction behaves across all stories
- Contradictions resolved
- Established patterns

### Honey/Amber Event Registry
- All Honey exposures and their effects
- All Amber incidents and consequences
- Rarity compliance check

### Final Notes
- Any remaining ambiguities (intentional or not)
- Suggested follow-up questions for lore expansion
- Recommendations for future character stories

---

## ADDITIONAL WRITING RULES

### Dialogue:
- Minimal, only when it advances character or plot
- No expository speeches
- Regional/cultural speech patterns acceptable (light accents, not heavy dialect)

### Violence:
- Impactful, not gratuitous
- Shows consequences (pain, trauma, aftermath)
- No "action movie" choreography

### Technology:
- Feels improvised, patched, dangerous
- Not shiny utopian sci-fi
- Shows wear, damage, jury-rigging

### Honey/Amber:
- Treated with appropriate gravity/respect/fear
- Never casual power-ups
- Economic and social consequences always present

### Race/Class Identity:
- Biology and culture shape worldview
- But individuals subvert expectations
- No race is monolithic

---

## VALIDATION CHECKLIST (Before Finalizing Any Story)

- [ ] Word count: 1,800-2,600
- [ ] No lore contradictions
- [ ] No mechanical contradictions
- [ ] No cross-story conflicts (checked against all previous stories)
- [ ] Tone matches Dark CDA style
- [ ] No meta commentary
- [ ] Mechanical notes complete
- [ ] Stereotype subversion clear
- [ ] Character is distinct
- [ ] Honey/Amber rules followed
- [ ] Timeline consistent
- [ ] Faction behavior consistent
- [ ] Shared events acknowledged appropriately

---

## OUTPUT FILES SUMMARY

1. `symbioz/characters/CHARACTER_ROSTER.md` - Initial roster table
2. `symbioz/characters/BIO_SUMMARIES.md` - 2-3 paragraph summaries
3. `symbioz/characters/stories/STORY_01_<NAME>.md` - First draft of each story
4. `symbioz/characters/stories/STORY_01_<NAME>_DEVILS_ADVOCATE.md` - Review for each story
5. `symbioz/characters/stories/FINAL/STORY_01_<NAME>.md` - Approved final versions
6. `symbioz/characters/CROSS_STORY_VALIDATION_REPORT.md` - Final consistency check

---

## EXECUTION ORDER

**MANDATORY SEQUENCE:**

1. Read all design docs
2. Create CHARACTER_ROSTER.md → **WAIT FOR APPROVAL**
3. Create BIO_SUMMARIES.md → **WAIT FOR APPROVAL**
4. Write STORY_01 → **WAIT FOR APPROVAL**
5. Write DEVILS_ADVOCATE for STORY_01 → **WAIT FOR APPROVAL**
6. Correct STORY_01, create FINAL version → **WAIT FOR APPROVAL**
7. Repeat steps 4-6 for STORY_02 → **WAIT FOR APPROVAL**
8. Continue for STORIES #3-10, checking against all previous stories each time
9. Create CROSS_STORY_VALIDATION_REPORT.md

**DO NOT SKIP APPROVAL STEPS. DO NOT WRITE MULTIPLE STORIES SIMULTANEOUSLY.**

---

## BEGIN EXECUTION

Start with **STEP 1: CREATE CHARACTER ROSTER**

Read all required files first, then generate the roster table.

**STOP after roster is complete and wait for user approval before proceeding.**

