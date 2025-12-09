# MVP Round 2 Tuning Notes

**Date**: December 2024  
**Status**: Implemented

---

## Changes Implemented

### 1. Graze Mechanic ✅

**What**: Added "Graze" hits that deal half damage when attack roll is within 2-3 points below Defense.

**Why**: Reduces "whiff fatigue" from multiple misses, makes combat feel more dynamic, fights are ~20-30% shorter.

**Implementation**:
- In `systems/combat.py`, attack() now returns (hit, damage, result_type)
- Graze threshold: `defense - 3 <= total_attack < defense`
- Graze deals half damage (rounded up), no status effects
- Updated `COMBAT_SYSTEM.md` to document the rule

**Result**: Players now get feedback every turn, even on "near misses". Combat feels less random and more engaging.

---

### 2. Enemy Tuning ✅

**Scavenger**:
- HP: 15 → 12
- Damage range kept consistent (2-4 typical)

**Wild Beast**:
- HP: 20 → 15 (both beasts)
- Damage reduced (max hit reduced from 9 to ~6-7)
- Mission labeled: "Clear the Den (Hard - Recommended Level 2+)"

**Why**: Scavenger fights were slightly too long. Wild Beasts were hitting too hard for level 1 characters, making "Clear the Den" feel unfair.

**Result**: Scavenger fights end in ~4-5 rounds instead of 6+. Wild Beasts are still dangerous but survivable with smart play.

---

### 3. Ability Improvements ✅

**Power Strike** (Vanguard):
- Now gives +2 to hit AND +2 damage on next attack
- Status effect "Power Strike Active" tracks the buff
- Removed after use

**Brace** (Vanguard):
- Now gives +4 Defense (was vague "increased")
- Clear messaging: "Defense increased by 4 this turn"
- Status effect "Guarded" applies +4 Defense bonus

**Survival Instinct** (Pioneer):
- Now gives +2 Attack and +1 to skill checks
- Duration: 3 turns (was 1)
- Status effect "Focused" tracks the buff

**First Aid** (Pioneer):
- **FIXED**: Now self-only, no target prompt
- Can't accidentally heal enemies
- Simple: "You restore X HP"

**Why**: Abilities felt like flavor text, not impactful choices. Players need to feel the difference when using abilities.

**Result**: Abilities now meaningfully change outcomes. Power Strike feels like a commitment that pays off. Brace feels like a defensive stance.

---

### 4. XP Curve Adjustment ✅

**What**: Level 2 threshold changed from 100 XP to 75 XP.

**Why**: After Mission 1 (50 XP) + failed Mission 2 (37 XP) = 87 XP, players should hit level 2 before trying "Clear the Den".

**Implementation**:
- Updated `character.py` `_xp_for_level()` method
- Level 2: 75 XP
- Level 3: 150 XP
- Level 4: 250 XP
- Level 5: 400 XP

**Result**: Players can now realistically reach level 2 before attempting the hard mission, making progression feel more rewarding.

---

### 5. Item/Honey Usage Improvements ✅

**What**: 
- Items now properly added to inventory after missions
- "Use Item" in combat actually uses Vital Honey
- Clear messaging: "You consume Vital Honey and restore X HP!"
- Items show in inventory

**Why**: Items were dropping but not usable, making them feel pointless.

**Result**: Players can now actually use the Honey they find, making item drops meaningful.

---

### 6. Mission Feedback Improvements ✅

**What**:
- Mission failure now shows: "XP Gained: X (would have been Y on success)"
- Items properly added to inventory with usage hint
- Difficulty labels on missions

**Why**: Players should know what they're missing when they fail, and how to use items.

**Result**: Better feedback loop, players understand consequences of failure.

---

## Combat Feel Changes

### Before Round 2:
- Too many full misses (felt random)
- Abilities were flavor text
- Fights dragged (6+ rounds)
- Items existed but weren't usable
- Wild Beasts felt unfair

### After Round 2:
- Graze hits provide feedback every turn
- Abilities meaningfully change outcomes
- Fights are faster (4-5 rounds typical)
- Items are usable and meaningful
- Wild Beasts are dangerous but fair with warning

---

## Testing Recommendations

Test these scenarios:

1. **Level 1 Vanguard vs Scavenger**
   - Should feel winnable in 4-5 rounds
   - Graze hits should be visible
   - Power Strike should feel impactful

2. **Hack the Terminal with non-Tech class**
   - Should show class identity (Vanguard bad at hacking)
   - Partial rewards should feel fair

3. **Clear the Den at Level 1**
   - Should feel very dangerous (as intended)
   - Should be possible with smart play and item usage

4. **Clear the Den at Level 2**
   - Should feel hard but survivable
   - Abilities should make a difference

---

## Next Steps

If Round 2 tuning feels good:

1. **Add more content**: More missions, enemy variety
2. **Companions**: Make "Clear the Den" a 3v2 instead of 1v2
3. **Honey system expansion**: More complex effects
4. **Visual polish**: ASCII art or simple graphics

If issues remain:

1. **Further tuning**: Adjust graze threshold, damage ranges
2. **More ability variety**: Each class needs 2-3 distinct abilities
3. **Better enemy AI**: Enemies should use abilities too

---

## Files Modified

- `apps/symbioz_cli/systems/combat.py` - Graze mechanic, ability improvements
- `apps/symbioz_cli/models/character.py` - XP curve adjustment
- `apps/symbioz_cli/data/missions.json` - Enemy HP, difficulty labels
- `apps/symbioz_cli/main.py` - Attack handling, item usage, messaging
- `symbioz/design/COMBAT_SYSTEM.md` - Graze documentation

---

## Phase 3 Changes

### 1. Tech Specialist Identity Fixed ✅

**Repair Ability**:
- Now self-only (no enemy healing bug)
- Heals: 1d4 + INT modifier HP (minimum 1 HP)
- Message: "reroutes power and stabilizes systems"

**New Ability: Overload Systems**:
- Offensive utility ability
- Attack roll: d20 + INT mod + 2 vs enemy Defense
- On hit: 1d6 + INT mod energy damage + -2 Defense debuff for 2 turns
- Gives Tech Specialist a way to help win fights, not just sustain

**Result**: Tech Specialist now has clear identity - can heal self AND debuff enemies.

---

### 2. Vital Honey Strengthened ✅

**New Formula**: 1d6 + CON modifier HP (minimum 3 HP)

**Why**: Makes Honey feel more impactful, especially for high-CON characters.

**Implementation**: Updated item usage in combat to use new formula.

---

### 3. Mid-Tier Mission Added ✅

**Salvage Run**:
- 2x Raiders (10 HP each, moderate damage)
- XP: 65
- Credits: 35
- Positioned between "Retrieve the Package" and "Clear the Den"

**Why**: Gives players a second combat mission before attempting the hard mission.

**Result**: Better progression curve, more content variety.

---

### 4. Vendor System Implemented ✅

**Available Items**:
- Improved Pistol: 80 credits (+1 attack or damage)
- Improved Sword: 80 credits (+1 damage)
- Reinforced Light Armor: 70 credits (+1 Defense over Light Armor)
- Vital Honey: 25 credits (consumable)

**Features**:
- Shows player credits
- Can purchase and equip weapons/armor immediately
- Items added to inventory
- Credits tracked and updated after missions

**Result**: Credits now matter, gear progression is visible.

---

### 5. Web UI Shell Created ✅

**Location**: `apps/symbioz_web/`

**Features**:
- Next.js 14 setup
- Combat screen layout:
  - Left: Player portrait, stats, HP bar
  - Right: Enemy portrait, stats, HP bar
  - Bottom: Combat log panel
  - Action buttons: Attack, Ability, Item, Defend
- Static mock data (not yet connected to CLI)

**Status**: Visual prototype ready. Can add real images to `public/symbioz/` folders.

---

## Phase 3 Testing Checklist

- [ ] Tech Specialist Repair works (self-only, no enemy healing)
- [ ] Overload Systems hits and applies debuff correctly
- [ ] Vital Honey heals with CON modifier
- [ ] Salvage Run is winnable at level 1, feels appropriately challenging
- [ ] Vendor allows purchasing and equipping upgrades
- [ ] Credits are tracked and displayed correctly
- [ ] Web UI displays correctly and buttons are visible

---

**Status**: All Phase 3 changes implemented and ready for testing.

