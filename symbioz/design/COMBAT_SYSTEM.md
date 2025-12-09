# Combat System: Symbioz MVP

**Version**: MVP (CLI Prototype)  
**Style**: D20-inspired, turn-based, KOTOR-like  
**Complexity**: Simple but tactical

---

## Overview

Combat is **turn-based** with initiative order. Each character (player party + enemies) takes one turn per round. Combat continues until one side is defeated or flees.

---

## Party & Enemy Composition

- **Player Party**: Up to 3 characters (player character + 2 companions in future; MVP may start with just player)
- **Enemies**: 1-4 enemies per encounter
- **Turn Order**: Determined by initiative roll

---

## Turn Order (Initiative)

**Formula**: `d20 + DEX Modifier + Initiative Bonus`

- Roll initiative at start of combat
- Higher initiative acts first
- Ties broken by DEX modifier, then random
- Turn order remains fixed for the encounter

**Example**:
- Player: d20 (12) + DEX mod (+3) = 15
- Enemy: d20 (8) + DEX mod (+1) = 9
- Player acts first

---

## Action Economy

Each character gets **1 Main Action** per turn:

### Main Actions:

1. **Attack**
   - Make a weapon attack against an enemy
   - Uses attack roll (see below)

2. **Use Ability** (Class Talent)
   - Use a class-specific ability (e.g., "Power Strike", "Hack", "First Aid")
   - May have cooldowns or resource costs
   - Defined by class

3. **Use Item**
   - Consume a Honey strain or other consumable
   - Instant effect (healing, buff, etc.)

4. **Defend / Brace**
   - Gain defensive bonus until next turn
   - Reduces incoming damage or increases Defense

5. **Flee** (Player Only)
   - Attempt to escape combat
   - May require a skill check or have consequences

---

## Attack Roll

**Formula**: `d20 + Attack Bonus vs Defense`

### Attack Bonus Components:
- **Base Attack Bonus** (from level/class)
- **Attribute Modifier**:
  - Melee weapons: STR modifier
  - Ranged weapons: DEX modifier
- **Weapon Bonus** (from weapon stats)
- **Feat/Skill Bonuses** (if applicable)

### Defense:
- **Base Defense** (from level/class)
- **DEX Modifier** (dodge/evasion)
- **Armor Bonus** (from equipped armor)
- **Shield Bonus** (if applicable)

### Hit/Miss/Graze:
- **Attack Roll ≥ Defense**: Hit! Roll full damage
- **Attack Roll within 2-3 points below Defense**: Graze! Deal half damage (rounded up), no status effects
- **Attack Roll < Defense - 3**: Miss! No damage

**Critical Hit**: Natural 20 on attack roll = automatic hit + double damage

**Graze Mechanic** (Round 2 addition):
- If attack roll is within 2-3 points below target's Defense, it's a "Graze"
- Graze deals half the normal damage (rounded up)
- Graze does NOT apply status effects (no bleed, no ability bonuses)
- This reduces "whiff fatigue" and makes combat feel more dynamic

---

## Damage Calculation

**Formula**: `Weapon Base Damage + Attribute Modifier - Armor Reduction`

### Components:

- **Weapon Base Damage**: From weapon stats (e.g., Pistol: 1d6, Sword: 1d8)
- **Attribute Modifier**:
  - Melee: STR modifier
  - Ranged: DEX modifier
- **Armor Reduction**: Flat reduction from enemy's armor (e.g., Light Armor: -1, Medium Armor: -2)
- **Minimum Damage**: Always at least 1 damage on a hit

**Example**:
- Player attacks with Sword (1d8 base) + STR mod (+3) = 1d8+3
- Roll: 5 + 3 = 8 damage
- Enemy has Medium Armor (-2 reduction)
- Final damage: 8 - 2 = **6 damage**

---

## Status Effects (MVP Set)

Simple status effects that modify combat:

### Staggered
- **Effect**: -2 to Attack and Defense
- **Duration**: 1 turn
- **Cause**: Certain abilities, critical hits, heavy damage

### Guarded
- **Effect**: +2 Defense, -1 Attack (defensive stance)
- **Duration**: Until next turn
- **Cause**: Defend/Brace action

### Bleeding
- **Effect**: Take 1 damage at start of each turn
- **Duration**: 3 turns (or until healed)
- **Cause**: Certain weapons, critical hits

### Stunned
- **Effect**: Skip next turn
- **Duration**: 1 turn
- **Cause**: Certain abilities, environmental hazards

---

## Health & Death

- **HP (Hit Points)**: Current health
- **Max HP**: Maximum health (from level, class, CON modifier)
- **0 HP**: Character is **Incapacitated** (unconscious, can't act)
- **Negative HP**: Character is **Defeated** (out of combat)
- **Healing**: Restore HP via items (Honey), abilities, or rest

---

## Positioning (Simplified for Text)

Since this is text-based, positioning is abstract:

- **Front Rank**: Melee fighters, tanks
- **Back Rank**: Ranged fighters, support
- **Effects**:
  - Melee weapons can only target Front Rank enemies
  - Ranged weapons can target any rank
  - Some abilities affect "all enemies in Front Rank"

**MVP Simplification**: For MVP, we may ignore ranks entirely and just allow targeting any enemy. Ranks can be added in Phase 2.

---

## Honey in Combat (MVP)

Honey strains are consumable items usable in combat:

- **Vital Honey**: Restore 2d4+2 HP
- **Stim Honey**: +2 to next attack roll (1 turn)
- **Toxin Honey**: Deal 1d4 damage to target enemy (ranged item)
- **Shield Honey**: +2 Defense for 3 turns
- **Focus Honey**: +1 to all skill checks for 1 encounter

**Usage**: "Use Item" action, select Honey from inventory, apply effect immediately.

---

## Example Combat Flow

```
=== COMBAT START ===
Initiative Roll:
- Player (DEX +3): 15
- Thug (DEX +1): 9

Round 1:
[Player Turn]
> 1) Attack  2) Use Ability  3) Use Item  4) Defend
Player chooses: 1) Attack
Target: Thug
Attack Roll: d20 (14) + Attack Bonus (+5) = 19
Thug Defense: 12
Hit! Damage: 1d8 (6) + STR (+3) = 9 damage
Thug HP: 15 → 6

[Thug Turn]
Thug attacks Player
Attack Roll: d20 (10) + Attack Bonus (+2) = 12
Player Defense: 15
Miss!

Round 2:
[Player Turn]
> 1) Attack  2) Use Ability  3) Use Item  4) Defend
Player chooses: 1) Attack
Attack Roll: d20 (18) + Attack Bonus (+5) = 23
Hit! Damage: 1d8 (7) + STR (+3) = 10 damage
Thug HP: 6 → 0
Thug Defeated!

=== COMBAT END ===
XP Gained: 50
Loot: 25 Credits, Vital Honey x1
```

---

## Class Abilities (Phase 3)

Each class has 2-3 abilities available:

### Vanguard (Tank/Fighter)
- **Power Strike**: +2 to hit AND +2 damage on next attack
- **Brace**: +4 Defense for 1 turn

### Operative (Rogue/Stealth)
- **Sneak Attack**: +3 damage if enemy hasn't acted yet this round
- **Dodge**: +4 Defense for 1 turn

### Tech Specialist (Hacker/Support)
- **Hack**: Disable enemy for 1 turn (INT check vs enemy Defense)
- **Repair**: Self-only heal, restores 1d4 + INT modifier HP (minimum 1 HP)
- **Overload Systems**: Attack roll (d20 + INT mod + 2) vs enemy Defense. On hit: deals 1d6 + INT mod energy damage and applies -2 Defense debuff for 2 turns

### Pioneer (Survival/Utility)
- **First Aid**: Self-only heal, restores 2d4+2 HP
- **Survival Instinct**: +2 Attack and +1 to skill checks for 3 turns

---

## Explicit Simplifications for MVP

The following are **intentionally simplified** for MVP:

- **No Movement**: Positioning is abstract (no grid, no movement actions)
- **No Opportunity Attacks**: No attacks of opportunity
- **No Reactions**: No reaction abilities
- **Simple Status Effects**: Only 4 status effects (Staggered, Guarded, Bleeding, Stunned)
- **No Environmental Hazards**: No traps, fire, etc. in combat (deferred to Phase 2)
- **No Cover**: No cover mechanics
- **No Flanking**: No positional bonuses
- **No Resource Management**: Abilities have simple cooldowns or no limits (MVP)

---

## Future Enhancements (Phase 2+)

- More complex status effects
- Environmental hazards in combat
- Movement and positioning mechanics
- Reaction abilities
- More class abilities and feats
- Implant abilities
- Cross-race synergy bonuses in combat
- Multi-target abilities (AoE)

---

## Success Metrics

After implementing combat, we should verify:

1. ✅ Combat feels tactical (choices matter)
2. ✅ Combat is fast (2-5 minutes per encounter)
3. ✅ Different classes feel distinct
4. ✅ Status effects add depth without complexity
5. ✅ Honey usage feels meaningful
6. ✅ Difficulty feels balanced (challenging but fair)

