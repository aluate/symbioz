# Symbioz CLI - MVP Prototype

A text-based, KOTOR-inspired sci-fi RPG prototype built to test the core gameplay loop and combat system.

## What This Is

This is a **Minimum Viable Product (MVP)** prototype designed to prove the core concepts before building the full game. It includes:

- 3 playable races (Human, Stonelock, Aeshura)
- 4 playable classes (Vanguard, Operative, Tech Specialist, Pioneer)
- Turn-based D20-style combat
- Simple skill checks for narrative choices
- Basic progression (XP, leveling)
- Hub → Mission → Encounter → Reward loop

## What This Is NOT

- A complete game (it's a prototype)
- A polished experience
- The full vision (10 races, 8 classes, full Honey system, Amber magic, etc.)
- A web app or API (it's a CLI game)

See `symbioz/design/MVP_SCOPE.md` for full details on what's included and what's deferred.

## Requirements

- Python 3.7+ (uses only standard library, no external dependencies)

## How to Run

From the `apps/symbioz_cli/` directory:

```bash
python main.py
```

Or from the project root:

```bash
python apps/symbioz_cli/main.py
```

## Gameplay

1. **Character Creation**: Choose a race and class
2. **Hub Menu**: Select missions, rest, view character sheet
3. **Missions**: Complete combat or skill-check missions
4. **Combat**: Turn-based combat with initiative, attacks, abilities
5. **Progression**: Gain XP, level up, improve stats

## Project Structure

```
apps/symbioz_cli/
├── main.py              # Entry point, game loop
├── data_loader.py       # Loads JSON game data
├── models/              # Data models
│   ├── character.py
│   ├── race.py
│   ├── clazz.py
│   ├── weapon.py
│   ├── armor.py
│   └── enemy.py
├── systems/             # Game systems
│   ├── combat.py
│   ├── skill_checks.py
│   ├── progression.py
│   └── hub.py
└── data/                # JSON game data
    ├── races.json
    ├── classes.json
    ├── weapons.json
    ├── armor.json
    ├── honey.json
    └── missions.json
```

## Design Documents

See `symbioz/design/` for:
- `GAMEPLAY_LOOP.md` - Core loop and mission structure
- `COMBAT_SYSTEM.md` - Combat rules and mechanics
- `MVP_SCOPE.md` - What's in MVP vs Phase 2+

## Next Steps

After testing the MVP:

1. Play through all missions
2. Test different race/class combinations
3. Evaluate if combat is fun
4. Check if progression feels rewarding
5. Review `symbioz/DEVILS_ADVOCATE_SUMMARY.md` for concerns

If MVP is fun, proceed to Phase 2:
- More content (missions, enemies)
- Expanded systems (more races, classes)
- First glimpse of deferred systems (Honey combinations, basic implants)

## Notes

- This is intentionally simple and unpolished
- Focus is on proving the core loop is fun
- Many systems are simplified or deferred
- Balance is rough (expected for MVP)
- Bugs may exist (report them!)

---

**Remember**: The full vision (10 races, 8 classes, full Honey system, Amber magic, etc.) is **canon** and will be built in Phase 2+. But we can't build Phase 2+ until we prove Phase 1 (MVP) is fun.

