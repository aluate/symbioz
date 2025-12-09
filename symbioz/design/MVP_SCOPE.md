# MVP Scope: Symbioz CLI Prototype

**Version**: MVP (Minimum Viable Product)  
**Purpose**: Prove the core loop and combat system are fun before building the full system  
**Target**: 20-40 minute playable prototype

---

## MVP Constraints (Ruthlessly Limited)

### Races: **Exactly 3**

1. **Human**
   - Balanced attributes
   - No special restrictions
   - Versatile, good for any class

2. **Stonelock** (Dwarf analog)
   - High CON, low DEX
   - Natural armor bonus
   - Bonus to crafting/tech skills

3. **Aeshura** (Elf analog)
   - High DEX, low CON
   - Bonus to precision/ranged attacks
   - Natural skill bonuses

**Deferred**: 7 additional races (10 total in full vision)

---

### Classes: **Exactly 4**

1. **Vanguard** (Tank/Fighter)
   - High STR, CON
   - Melee focus
   - Abilities: Power Strike, Brace

2. **Operative** (Rogue/Stealth)
   - High DEX, INT
   - Ranged/stealth focus
   - Abilities: Sneak Attack, Dodge

3. **Tech Specialist** (Hacker/Support)
   - High INT, moderate other stats
   - Support/utility focus
   - Abilities: Hack, Repair

4. **Pioneer** (Survival/Utility)
   - Balanced stats, WIS focus
   - Utility/survival focus
   - Abilities: First Aid, Survival Instinct

**Deferred**: 4 additional classes (8 total in full vision) + NPC Channeler class

---

### Honey: **Exactly 5 Base Strains**

1. **Vital Honey**: Restore 2d4+2 HP
2. **Stim Honey**: +2 to next attack roll (1 turn)
3. **Toxin Honey**: Deal 1d4 damage to target enemy
4. **Shield Honey**: +2 Defense for 3 turns
5. **Focus Honey**: +1 to all skill checks for 1 encounter

**Deferred**:
- Multi-strain combinations (brewing system)
- 15+ additional honey types
- Complex honey effects
- Honey as currency (credits only in MVP)
- Honey-based weapon upgrades

---

### Weapons: **Exactly 2 Shapes, Simplified Slots**

**Shapes**:
1. **Pistol** (Ranged)
   - Base damage: 1d6
   - Uses DEX for attack
   - 3 upgrade slots (not 6)

2. **Sword** (Melee)
   - Base damage: 1d8
   - Uses STR for attack
   - 3 upgrade slots (not 6)

**Upgrade Slots** (Simplified):
- **Slot 1**: Damage modifier (+1, +2, +3)
- **Slot 2**: Accuracy modifier (+1, +2, +3)
- **Slot 3**: Special effect (e.g., "Bleeding on crit", "Bonus vs armor")

**Deferred**:
- Additional weapon shapes (Rifle, Hammer, Explosive, etc.)
- Full 6-slot upgrade system
- Energy vs Ballistic damage types
- Weapon-specific upgrade components (lens, battery, etc.)
- Feat-locked upgrade slots

---

### Armor: **Only Light and Medium**

1. **Light Armor**
   - Defense: +1
   - Damage Reduction: -1
   - No class restrictions

2. **Medium Armor**
   - Defense: +2
   - Damage Reduction: -2
   - Some class restrictions (Tech Specialist can't use)

**Deferred**:
- Heavy Armor
- Implant-based armor
- Armor upgrade slots
- Class-specific armor restrictions (beyond basic)

---

### Magic/Amber: **NOT in MVP**

- No Channeler class
- No Amber mechanics
- No magic spells
- No magic-based weapons
- Magic exists only as flavor text / future story hooks

**Deferred**: Full Amber magic system, Channeler class, magic weapons, spell system

---

### Mode: **Single-Player Only**

- No multiplayer
- No co-op
- No party management (player character only, or simple companion system)
- No networking
- No server infrastructure

**Deferred**: Co-op multiplayer, party system, networking, server architecture

---

### Content: **Minimal but Functional**

**Hub**:
- 1 hub location: "The Outpost"
- Basic vendor (buy/sell weapons, armor, honey)
- Rest area
- Mission board

**Missions**:
- 2-3 simple missions
- Linear narrative (no complex branching)
- 1 combat encounter per mission (or skill challenge)

**Enemies**:
- 3-5 enemy types (e.g., "Thug", "Security Drone", "Wild Beast")
- Simple AI (basic attack patterns)

**Deferred**:
- Multiple hubs/planets
- Complex narrative branching
- Procedural content
- Boss fights (may have 1 simple boss in MVP)
- Side quests
- Multiple endings

---

### Systems: **Simplified**

**Attributes**: STR, DEX, CON, INT, WIS, CHA (standard D&D 6-attribute system)

**Leveling**:
- Level cap: 5 (for MVP, full game is 30)
- XP from combat and mission completion
- Simple stat increases on level-up
- 1-2 new abilities per class

**Inventory**:
- Simple list (weapons, armor, consumables)
- No weight limits
- No item degradation

**Deferred**:
- Full level 30 progression
- Complex feat trees
- Implant system (beyond basic flavor)
- Cross-race synergies
- Complex inventory management
- Item crafting (beyond basic upgrades)

---

## Phase 2+ Systems (Explicitly Deferred)

These are part of the full vision but **intentionally not in MVP**:

### Races & Classes
- 7 additional races (10 total)
- 4 additional classes (8 total)
- NPC Channeler class

### Honey System
- Multi-strain brewing combinations
- 15+ additional honey types
- Honey as currency
- Honey-based weapon upgrades
- Complex honey effects

### Weapons & Armor
- Additional weapon shapes (Rifle, Hammer, Explosive, etc.)
- Full 6-slot upgrade system
- Energy vs Ballistic damage types
- Weapon-specific components
- Heavy Armor
- Implant-based armor
- Armor upgrade slots

### Magic & Amber
- Full Amber magic system
- Channeler class mechanics
- Magic spells
- Magic-based weapons
- Story-gated magic unlocks

### Gameplay Features
- Co-op multiplayer
- Party management system
- Multiple hubs/planets
- Ship combat
- Complex narrative branching
- Procedural content generation
- Boss fights
- Side quests
- Multiple endings

### Advanced Systems
- Full implant system with synergies
- Cross-race synergy bonuses
- Complex feat trees
- Full level 30 progression
- Item crafting system
- Environmental hazards
- Advanced status effects
- Movement and positioning mechanics

---

## MVP Success Criteria

The MVP is successful if:

1. ✅ **Core Loop Works**: Hub → Mission → Encounter → Reward feels engaging
2. ✅ **Combat is Fun**: Turn-based combat is tactical and satisfying
3. ✅ **Progression Feels Good**: Leveling up and upgrades are visible and rewarding
4. ✅ **Systems Are Clear**: New players can understand the game in 5 minutes
5. ✅ **Replayability Exists**: Players want to try different race/class combinations
6. ✅ **Foundation is Solid**: The MVP proves the concept before building the full system

---

## What MVP Is NOT

- A complete game
- A polished experience (it's a prototype)
- A showcase of all systems (most are deferred)
- A commercial product (it's a proof of concept)
- A web app or API (it's a CLI prototype)

---

## Next Steps After MVP

If MVP is successful:

1. **Expand Content**: Add more missions, enemies, hubs
2. **Add Systems**: Gradually add deferred systems (more races, classes, honey combinations)
3. **Polish**: Improve UI, add flavor text, balance combat
4. **Consider Platform**: Evaluate if CLI is sufficient or if web/desktop app is needed
5. **Test with Players**: Get feedback, iterate, expand scope

If MVP is not fun:

1. **Identify Problems**: What's not working? (combat? loop? progression?)
2. **Simplify Further**: Maybe even smaller scope
3. **Pivot**: Consider different approach or format
4. **Learn**: Document what didn't work and why

---

## Development Philosophy

**MVP First, Full Vision Later**

- Build the smallest thing that proves the concept
- Test if it's fun before adding complexity
- Defer everything that isn't essential to the core loop
- Use this document to resist scope creep

**Remember**: The full vision (10 races, 8 classes, full Honey system, Amber magic, etc.) is **canon** and will be built in Phase 2+. But we can't build Phase 2+ until we prove Phase 1 (MVP) is fun.

