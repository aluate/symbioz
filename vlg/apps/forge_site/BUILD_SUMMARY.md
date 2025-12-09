# Forge Site — Build Summary

## Overview

Forge Site has been fully scaffolded as a standalone product. This document summarizes everything that was created.

## Brand Identity

**Name:** Forge Site  
**Abbreviation:** FS  
**Tagline:** "Get seen. Stay simple."

**Palette:**
- Steel Blue (#5D7586) - Primary accents
- Porcelain (#F4F2EC) - Background
- Graphite (#2F3136) - Text
- Lavender Gray (#D9DCE0) - Muted surfaces

**Voice:** Karl + Hemingway — direct, calm, professional, short sentences, plain words, strong verbs.

## Directory Structure

```
vlg/apps/forge_site/
├── control/                    # Control documentation
│   ├── CONTROL_FS_PRODUCT.md
│   ├── CONTROL_FS_MODULE_REGISTRY.md
│   ├── CONTROL_FS_TEMPLATES.md
│   └── CONTROL_FS_BUILD_FLOW.md
├── brand/                      # Brand tokens
│   ├── forge_site_brand.json
│   ├── forge_site_color_tokens.json
│   ├── forge_site_typography_tokens.json
│   └── forge_site_logo_notes.md
├── modules/                    # Module components (placeholders)
│   ├── page_modules/
│   └── ui_blocks/
├── templates/                  # Template definitions
│   ├── base_templates/
│   └── content_blocks/
├── scripts/                    # Build scripts
│   ├── build-site-from-config.ts
│   ├── generate-template.ts
│   └── list-templates.ts
├── data/                       # Registries and schemas
│   ├── module_registry.json
│   ├── template_index.json
│   └── prompts/
│       ├── business_intake_form.md
│       └── business_json_schema.json
├── docs/                       # Documentation
│   ├── README.md
│   ├── FS_PRICING_MODEL.md
│   ├── FS_SALES_PITCH.md
│   ├── FS_MARKETING_LANDING_COPY.md
│   └── LICENSE.md
├── app/                        # Marketing site (Next.js)
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── output/                     # Generated client sites
├── README.md
└── BUILD_SUMMARY.md
```

## Key Files Created

### Control Documentation (4 files)

1. **CONTROL_FS_PRODUCT.md** - Product overview, target audience, roadmap
2. **CONTROL_FS_MODULE_REGISTRY.md** - Module definition schema and rules
3. **CONTROL_FS_TEMPLATES.md** - Template definitions and selection logic
4. **CONTROL_FS_BUILD_FLOW.md** - Complete build pipeline documentation

### Brand Files (4 files)

1. **forge_site_brand.json** - Brand identity, tagline, voice notes
2. **forge_site_color_tokens.json** - Color palette with usage guidelines
3. **forge_site_typography_tokens.json** - Font system and typography scale
4. **forge_site_logo_notes.md** - Logo direction and symbol ideas

### Data Files

1. **module_registry.json** - 22 module definitions with full schemas
2. **template_index.json** - 3 base templates (simple-builder-landing, lead-capture, commerce-lite)
3. **business_intake_form.md** - Human-readable intake form
4. **business_json_schema.json** - JSON Schema for business config validation

### Build Scripts (3 files)

1. **build-site-from-config.ts** - Main build script that generates Next.js sites
2. **generate-template.ts** - Scaffolds new template folders
3. **list-templates.ts** - Lists available templates

### Documentation (5 files)

1. **README.md** - User guide and quick start
2. **FS_PRICING_MODEL.md** - Pricing structure and packages
3. **FS_SALES_PITCH.md** - Sales pitch for prospects
4. **FS_MARKETING_LANDING_COPY.md** - Full marketing page copy
5. **LICENSE.md** - MIT License

### Marketing Site

Complete Next.js app in `app/` with:
- Landing page using marketing copy
- Forge Site brand colors and typography
- Responsive design
- All sections from marketing copy

## Templates

Three base templates are defined:

1. **simple-builder-landing** - For builders, trades, local professionals
2. **lead-capture** - For lead-gen heavy services
3. **commerce-lite** - For small shops and product sellers

## Modules

22 modules defined in the registry, including:

- Hero sections (basic, image-right)
- Content modules (services grid, two-column, benefits)
- Gallery modules (project gallery, case study)
- Trust modules (testimonials, stats, FAQ)
- Form modules (lead capture, contact)
- Commerce modules (product grid, cart, checkout)
- Content modules (blog, map embed)

## How to Use

### Run Marketing Site

```bash
cd vlg/apps/forge_site/app
npm install
npm run dev
```

Open http://localhost:3000

### Build a Client Site

1. Create a `business.json` file (see `data/prompts/business_intake_form.md`)
2. Run the build script:

```bash
cd vlg/apps/forge_site
npx tsx scripts/build-site-from-config.ts path/to/business.json
```

3. Generated site will be in `output/<site-slug>/`
4. Run the generated site:

```bash
cd output/<site-slug>
npm install
npm run dev
```

### List Templates

```bash
npx tsx scripts/list-templates.ts
```

### Generate New Template

```bash
npx tsx scripts/generate-template.ts "template-name"
```

## Next Steps

1. **Implement Module Components** - Create React components for each module in `modules/page_modules/`
2. **Enhance Build Script** - Add actual module component generation and copy generation
3. **Add Content Blocks** - Create reusable copy blocks in `templates/content_blocks/`
4. **Test Build Flow** - Create sample business.json files and test the build
5. **Deploy Marketing Site** - Deploy the marketing site to Vercel
6. **Logo Design** - Create actual logo files based on `forge_site_logo_notes.md`

## Status

✅ **Complete:** All scaffolding, documentation, brand tokens, registries, scripts, and marketing site  
⏳ **Pending:** Module component implementation, enhanced build logic, logo design

## Notes

- The build script currently generates a basic Next.js structure. Module components need to be implemented.
- Copy generation is stubbed. In production, this would use AI or template libraries.
- The marketing site is fully functional and ready to deploy.
- All brand tokens are defined and ready to use.

---

**Get seen. Stay simple.**

