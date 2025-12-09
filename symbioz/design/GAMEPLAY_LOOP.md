# Gameplay Loop: Symbioz MVP

**Version**: MVP (CLI Prototype)  
**Target Session Length**: 20-40 minutes for a 3-mission arc  
**Mode**: Single-player, text-based CLI

---

## Core Loop

```
Hub → Choose Mission → Narrative Node → Encounter (Skill Check or Combat) → Outcome → Loot/XP → Return to Hub → Upgrade
```

---

## Hub Structure

The **Hub** is the player's home base between missions. It's a menu-driven interface where players can:

### Hub Menu Options:

1. **View Missions** (Primary Action)
   - List available missions with brief descriptions
   - Show mission difficulty/recommended level
   - Select a mission to begin

2. **Visit Vendor** (Upgrade/Shop)
   - Buy/sell weapons and armor
   - Purchase Honey strains (5 types in MVP)
   - Upgrade weapon slots (if player has required feats/skills)
   - View inventory

3. **Rest/Recover**
   - Restore HP to full
   - Remove status effects
   - Advance time (may affect mission availability)

4. **Character Sheet**
   - View stats, level, XP
   - View equipped gear
   - View inventory
   - View available abilities/feats

5. **Talk** (Optional in MVP)
   - Simple flavor text from NPCs
   - May unlock missions or provide hints
   - Minimal implementation for MVP

6. **Exit Game** (Save and quit)

---

## Mission Flow

A **Mission** is a self-contained narrative sequence that takes 5-15 minutes to complete.

### Mission Structure:

1. **Mission Briefing** (Text Description)
   - Location description
   - Objective (e.g., "Retrieve the data core", "Eliminate the target")
   - Context and flavor

2. **Travel to Location** (Optional Narrative Node)
   - Brief text describing the journey
   - May include a simple skill check (e.g., "Navigate the asteroid field" → DEX check)

3. **Mission Area** (1-3 Narrative Nodes)
   - Each node presents:
     - Descriptive text about the environment
     - Choices (menu-driven: "1) Go left 2) Go right 3) Search area")
     - Skill checks based on choices (e.g., INT check to hack a door, STR check to force it)
     - Outcomes based on success/failure

4. **Encounter** (Combat or Skill Challenge)
   - **Combat Encounter**: Turn-based combat using `COMBAT_SYSTEM.md` rules
   - **Skill Challenge**: Series of skill checks (e.g., "Sneak past guards" → 3 DEX checks)
   - May include environmental hazards or traps

5. **Resolution**
   - Success: Loot, XP, return to hub
   - Failure: Reduced rewards, may retry or return to hub

6. **Return to Hub**
   - Mission complete
   - XP awarded
   - Loot added to inventory
   - Level-up check (if applicable)

---

## Runtime Goals

### 20-40 Minute Session Target:

- **Hub Time**: 2-5 minutes (choose mission, maybe shop/upgrade)
- **Mission Time**: 15-30 minutes (narrative + encounter)
- **Post-Mission**: 2-5 minutes (review loot, level up, plan next mission)

### Progression Feel:

- **Early Game** (Levels 1-5): Simple missions, basic combat, learning systems
- **Mid Game** (Levels 6-15): More complex encounters, weapon upgrades become meaningful
- **Late Game** (Levels 16-30): Challenging boss fights, full build optimization

### MVP Content:

- **1 Hub Location**: "The Outpost" (space station or planet-side base)
- **2-3 Simple Missions**: 
  - "Retrieve the Package" (intro mission, combat encounter)
  - "Hack the Terminal" (skill-check focused)
  - "Clear the Den" (combat-focused, multiple enemies)
- **Handful of Enemy Types**: 3-5 enemy archetypes (e.g., "Thug", "Security Drone", "Wild Beast")

---

## Skill Checks (Non-Combat)

Simple attribute-based checks for narrative choices:

- **Formula**: `d20 + Attribute Modifier + Skill Bonus vs Difficulty Class (DC)`
- **Common Checks**:
  - **STR**: Force doors, lift objects, break things
  - **DEX**: Sneak, dodge, pick locks, dodge traps
  - **INT**: Hack terminals, analyze data, solve puzzles
  - **WIS**: Detect traps, read people, survival checks
  - **CHA**: Persuade, intimidate, negotiate

- **Difficulty Examples**:
  - Easy (DC 10): Basic tasks
  - Medium (DC 15): Challenging tasks
  - Hard (DC 20): Expert-level tasks

---

## Honey in MVP

Honey is simplified for MVP:

- **5 Base Strains**: Each with a single, clear effect
  - Example: "Vital Honey" (restore HP), "Stim Honey" (temporary stat boost), "Toxin Honey" (damage over time for enemies)
- **Usage**: Consumable items in combat or out of combat
- **Acquisition**: Buy from vendor, find as loot
- **No Complex Combinations**: Multi-strain brewing deferred to Phase 2

---

## Explicitly Deferred to Future Phases

The following are **intentionally not in MVP** but are part of the full vision:

- **Co-op/Multiplayer**: Single-player only for MVP
- **Ship Combat**: No space battles yet
- **Full Amber Magic System**: No Channeler class, no Amber mechanics
- **Complex Honey Brewing**: No multi-strain combinations
- **Full 10 Races / 8 Classes**: MVP has 3 races, 4 classes
- **Implant Synergies**: Basic implants exist, but cross-race synergies deferred
- **Full Weapon Upgrade System**: Simplified to 3 slots per weapon (not 6)
- **Heavy Armor**: Only Light and Medium armor in MVP
- **Multiple Hubs/Planets**: Single hub location for MVP
- **Complex Narrative Branching**: Simple linear missions for MVP

---

## Success Metrics for MVP

After playing the MVP, we should be able to answer:

1. ✅ Is the hub → mission → encounter → reward loop engaging?
2. ✅ Do players want to do another mission immediately?
3. ✅ Does combat feel satisfying?
4. ✅ Do skill checks add meaningful choices?
5. ✅ Is progression (leveling, upgrades) visible and rewarding?
6. ✅ Can a new player understand the game in 5 minutes?

---

## Next Steps After MVP

If MVP is fun, Phase 2 would add:

- More missions and content
- Additional race/class options
- Expanded Honey system
- First glimpse of Amber/magic (as story element, not playable)
- More weapon/armor variety
- Basic implant system

