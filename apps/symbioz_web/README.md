# Symbioz Web UI - Phase 3 Prototype

A Next.js web interface for Symbioz combat visualization.

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

