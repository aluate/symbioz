# Symbioz Lore Data Layer

**Purpose**: First-class game data that binds lore, mechanics, and systems together.

**Philosophy**: Lore should be data, not just documentation. This ensures zero drift between story and mechanics.

---

## Directory Structure

```
symbioz/data/lore/
├── races.json              # Race data with cultural traits, honey affinity
├── classes.json            # Class data with faction alignment, amber risk
├── honey.json             # All honey types with mechanical + lore data
├── amber.json              # Amber effects, psychology risks, channeling rules
├── factions.json           # Faction attitudes, rules of engagement
├── planets.json            # World data, honey sources, faction control
├── shared_events/          # Major world events (Gamma-7, etc.)
│   └── gamma7.json
├── canon_ledger.json      # Character canon with mechanical implications
├── connections/            # Relationship graphs
│   └── characters_graph.json
└── portraits/              # Portrait metadata
    └── [character_name].json
```

---

## Data Schema Principles

1. **Unified Fields**: All entities share common metadata fields
2. **Mechanical Implications**: Lore data includes gameplay hooks
3. **Cross-References**: Entities link to each other (honey → planets, characters → factions)
4. **Version Control**: JSON is source of truth, markdown docs reference it

---

## Usage

Game systems read from these files:
- Character creation uses `races.json` and `classes.json`
- Combat modifiers check `honey.json` and `amber.json`
- Vendor prices use `factions.json` reputation rules
- Missions reference `planets.json` and `shared_events/`
- NPCs pull from `canon_ledger.json` and `connections/`

---

## Migration Path

1. Extract data from existing markdown docs
2. Structure as JSON with schemas
3. Update game code to read from JSON
4. Markdown docs become "human-readable views" of JSON data

