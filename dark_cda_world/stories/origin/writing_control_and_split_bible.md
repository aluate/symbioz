# Dark CDA Writing Control Document (Cursor Version)

This control document governs **all writing, rewriting, outlining, worldbuilding, and narrative operations** performed inside Cursor for ANY story set in the **Dark CDA Universe**.

It is entirely separate from the development/automation control doc.
Cursor must never mix the two modes.

---
# 1. PURPOSE OF THIS DOCUMENT
This file defines how Cursor should behave when assisting with narrative work. Cursor must:
- Load the world bible and universe-level character/timeline docs BEFORE generating prose.
- Never contradict universal rules.
- Add new lore to the append-only sections.
- Keep story files consistent.
- Maintain tone, pacing, and voice.
- NEVER treat writing tasks as coding tasks.

This control doc is ONLY for writing.

---
# 2. REQUIRED BEHAVIOR FOR CURSOR
Whenever Cursor is given ANY writing-related instruction:
```
You are in WRITING MODE.
Load and reference the following ALWAYS:
/world/world_bible.md
/world/universe_characters.md
/world/universe_timeline.md

If the active story folder exists, also reference:
/stories/<story_name>/outline.md
/stories/<story_name>/characters.md
/stories/<story_name>/timeline.md
```

Cursor must:
- Track characters across scenes
- Track metaphysical rules
- Prevent contradictions
- Maintain POV consistency
- Flag unclear chronology
- When a new magic effect or lore detail appears, propose an addition to /world/world_bible.md
- When a new character detail appears, propose an addition to the story-level characters file

Cursor must NOT:
- Use coding patterns
- Generate functions, imports, modules, etc.
- Modify dev repos
- Suggest algorithms or code fixes

---
# 3. WRITING STYLE RULES
Cursor must follow these stylistic constraints:
- Voice: grounded, clean, Western clarity with mythic undertone
- Avoid purple prose
- Favor clear imagery and character-driven beats
- Maintain emotional truth
- Preserve tone hierarchy: weight > spectacle
- Dialogue must be concise

For expansions:
- Atmospheric but efficient
- Strong paragraph hooks
- Every scene must change something in: character, relationship, or world

---
# 4. WORLD BIBLE ENFORCEMENT
Cursor must enforce:
- **Weight mechanics** (choices alter metaphysical mass)
- **Balance & Scales** logic
- **Names have weight**
- **Coin vs Pouch dynamics**
- **Coyote’s rules** (no forced choice; probability bending)
- **Graybreaker’s rules** (truth + consequence)
- **Hawk’s role** (witness)
- **Mountain Olayah’s pressure logic**

Cursor must NEVER violate these.
If a user’s request contradicts established rules:
- Cursor must rewrite the scene to fit the rules, OR
- Ask the user if the universal rule should be updated

---
# 5. FILE HANDLING IN CURSOR
Cursor must:
- Modify only the files explicitly requested
- Never overwrite universal files
- Append lore to world files
- Keep story-level files inside the story folder

Cursor must NEVER:
- Merge story lore into the universal bible
- Replace universal rules with story-specific ones

---
# 6. GENERATION BEHAVIOR
When generating:
- Scene → write it cleanly
- Chapter → follow beats & outline
- Rewrite → keep intent, improve clarity
- Summaries → respect structure

When asked to create new magic:
- Propose rule
- If approved → append to world bible

---
# 7. TIMELINE & CHARACTER CONSISTENCY
Cursor must:
- Track all character ages
- Track relationship changes
- Track all timeline beats
- Warn if chronology breaks
- Update story-level timeline when needed

---
# 8. WHEN IN DOUBT
If ANY ambiguity exists:
- Cursor must default to the WORLD BIBLE
- Then to the STORY OUTLINE
- Then ask the user

---
# END OF WRITING CONTROL DOCUMENT


---

# SPLIT WORLD BIBLE (UNIVERSAL VERSION)
The original "World Bible" has now been split into:
- **Universal Bible (below)**
- **Origin-Specific Outline (separate)**

This ensures cross-story cleanliness.

---
# /world/world_bible.md (UNIVERSAL)

## 1. Metaphysics of Dark CDA
- Weight governs all things
- Scales react to choices, not intent
- Names carry metaphysical mass
- Balance is the world's equilibrium engine

## 2. Universal Entities
### Coyote
- Embodies choice
- Cannot force outcomes
- Nudges probability
- Appears at crossroads

### Graybreaker
- Enforces truth
- Stationed at sacred springs
- Appears when imbalance threatens catastrophe

### Hawk
- Witness only
- Marks turning points
- Responds to Weight shifts

### Mountain Olayah
- Pressure valve for cosmic imbalance
- Erupts when Weight peaks

## 3. Magic Rules (Universal)
### Weight
- All choices create Weight
- Imbalance → tremors, ash, sickness

### Names
- Spoken names alter Weight
- Naming something binds it

### Balance
- No action is free
- Scales require settlement

## 4. Objects of Power (Universal)
### Coin
- Amplifies intent
- Enhances persuasion
- Dangerous when imbalanced

### Pouch
- Holds Weight
- Used by "the keeper"

> Specific owners exist per era but are NOT defined here.

## 5. Universal Timeline (Cosmological)
- Seven Fires event (universal myth)
- Early tribes + settler interactions
- Springs as ancient sites
- Olayah eruptions throughout history

## 6. Universe-Level Characters
(None specific, aside from mythic entities)

More characters become universal only if they appear across multiple eras.

## 7. Append-Only Lore Section
(Add new universal rules here)

