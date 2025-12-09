# Forge Site

**Get seen. Stay simple.**

Forge Site is a calm, professional, modular website system. It takes a simple business profile, selects proven templates and page modules, and generates a clean, modern, high-converting website ready to deploy.

## Quick Start

### Run the Marketing Site

The Forge Site marketing site is in `app/`:

```bash
cd app
npm install
npm run dev
```

Open http://localhost:3000 to see the marketing landing page.

### Build a Client Site

Create a `business.json` file (see `data/prompts/business_intake_form.md` for guidance), then:

```bash
npx tsx scripts/build-site-from-config.ts path/to/business.json
```

The generated site will be in `output/<site-slug>/`.

## Project Structure

```
forge_site/
  control/          # Control documentation
  brand/            # Brand tokens and guidelines
  modules/          # Module components (to be implemented)
  templates/        # Template definitions
  scripts/          # Build scripts
  data/             # Registries and schemas
  docs/             # Documentation
  app/              # Marketing site (this product)
  output/           # Generated client sites
```

## Documentation

- **Product Overview:** `control/CONTROL_FS_PRODUCT.md`
- **Module Registry:** `control/CONTROL_FS_MODULE_REGISTRY.md`
- **Templates:** `control/CONTROL_FS_TEMPLATES.md`
- **Build Flow:** `control/CONTROL_FS_BUILD_FLOW.md`
- **User Guide:** `docs/README.md`
- **Pricing:** `docs/FS_PRICING_MODEL.md`
- **Sales Pitch:** `docs/FS_SALES_PITCH.md`
- **Marketing Copy:** `docs/FS_MARKETING_LANDING_COPY.md`

## Brand

Forge Site uses a calm, professional palette:

- **Steel Blue** (#5D7586) - Primary accents
- **Porcelain** (#F4F2EC) - Background
- **Graphite** (#2F3136) - Text
- **Lavender Gray** (#D9DCE0) - Muted surfaces

See `brand/` for full brand tokens and guidelines.

## License

MIT License. See `docs/LICENSE.md`.

---

**Get seen. Stay simple.**

