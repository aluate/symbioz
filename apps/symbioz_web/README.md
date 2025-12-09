# Symbioz Web UI - Phase 3 Prototype

A Next.js web interface for Symbioz combat visualization.

## Mellivox Brand Canon (Summary)

**Mellivox** is the overarching brand and doctrine for the Symbioz universe. The core theme is that **symbiosis produces consequence** — every connection changes reality, sometimes beautifully, sometimes catastrophically.

The bee sigil represents the sacred archivist and mediator of the "Pact of Nectar" — an ancient agreement that nothing thrives alone. Mellivox influences the aesthetic, mood, and lore flavor of the universe, but does not directly affect gameplay mechanics.

**Full brand documentation:** See `brand/MELLIVOX_BRAND_BIBLE.md` for complete brand identity, color system, voice guidelines, and design specifications.

### Mellivox DAC (Devil's Advocate Check)

Mellivox intentionally flirts with:
- Environmental symbolism (bees)
- Cult-like doctrine aesthetics
- Luxury-coded black+gold palette

We are **NOT** trying to be:
- An eco-activist brand
- A real-world cult
- A flashy luxury label

We keep these edges because they give the brand gravity and mood. Contributors should lean into mythic biotech mysticism and consequence, keep designs austere and solemn, avoid real-world political/religious references, and reference the full DAC section in `brand/MELLIVOX_BRAND_BIBLE.md` when in doubt.

## Status

**Phase 3**: Static mock combat screen with portraits, stats, combat log, and action buttons.

This is a **visual prototype** - not yet connected to the CLI backend.

## Getting Started

1. Install dependencies:
   ```bash
   cd apps/symbioz_web
   npm install
   ```

2. Run development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000)

## Features

- Player and enemy portrait placeholders
- HP bars and stats display
- Combat log panel
- Action buttons (Attack, Ability, Item, Defend)

## Next Steps

- Wire to CLI backend API
- Add real character/enemy images
- Implement actual combat flow
- Add ability/item selection menus

## Image Placeholders

Images should be placed in:
- `public/symbioz/characters/` - Character portraits
- `public/symbioz/enemies/` - Enemy portraits

Use prompts from `symbioz/design/VISUAL_STYLE_GUIDE.md` to generate images.

