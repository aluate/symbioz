# Forge Site — Build Flow Control

## Overview

The Forge Site build pipeline takes a `business.json` file and generates a complete Next.js website. This document explains each step.

## Build Pipeline Steps

### 1. Ingest business.json

Read the business configuration file from the specified path.

Validate file exists and is valid JSON.

### 2. Validate Against Schema

Check `business.json` against `business_json_schema.json`:

- Required fields present
- Field types match (strings, arrays, booleans)
- Enums are valid values
- Arrays contain expected structures

If validation fails, log errors and stop.

### 3. Choose Base Template

Select template based on:

1. Explicit `templateId` in business.json (if present)
2. `primaryGoal` field:
   - `GET_LEADS` → `lead-capture` or `simple-builder-landing`
   - `SELL_PRODUCTS` → `commerce-lite`
   - `CREDIBILITY` / `CLARITY` → `simple-builder-landing`
3. `hasProducts` flag:
   - `true` → `commerce-lite` (unless overridden)
4. `industry` hints:
   - Builder/trades → `simple-builder-landing`
   - Service-heavy → `lead-capture`

Load template definition from `template_index.json`.

### 4. Build Page List

Extract list of pages from chosen template:

- `home` (always present)
- Additional pages per template definition
- Custom pages from `business.json.pages` (if specified)

### 5. Assemble Modules Per Page

For each page:

1. Get module IDs from template definition
2. Load module definitions from `module_registry.json`
3. Create module instances in order
4. For each module:
   - Extract required data from `business.json`
   - Generate missing copy using Forge Site voice
   - Apply brand tokens
   - Create props object

### 6. Generate Copy

For any missing text fields:

- Use Forge Site voice (Karl + Hemingway):
  - Short sentences
  - Plain words
  - Strong verbs
  - Concrete examples
  - Direct, calm tone
- Pull from content block library if available
- Generate based on business context

### 7. Apply Brand Tokens

**Check for client-specific branding:**

1. **If `business.json` includes `brandTokensPath`:**
   - Load client brand tokens from specified path
   - Use client-specific colors, typography, spacing
   - Apply client branding throughout site

2. **If client branding not present:**
   - Apply default Forge Site brand tokens:
     - Colors (Steel Blue, Porcelain, Graphite, Lavender Gray)
     - Typography (font stack, sizes, weights)
     - Spacing (8px grid)
     - Border radius
     - Component styling
   - Tokens come from `forge_site_brand.json` and related token files

**Brand Generation Integration:**
- If `business.json` includes raw brand input (conversation transcript, notes), generate brand system first using `CONTROL_FS_BRANDING_GENERATION.md`
- Generate brand tokens from brand system
- Apply generated tokens to site

**Token Priority:**
1. Client brand tokens (if specified)
2. Generated brand tokens (if brand generation was run)
3. Default Forge Site tokens (fallback)

### 8. Write Next.js Files

Generate site structure in `/output/<site-slug>/`:

**Directory Structure:**
```
output/<site-slug>/
  app/
    layout.tsx          # Root layout with brand tokens
    page.tsx            # Home page
    services/
      page.tsx          # Services page (if in template)
    projects/
      page.tsx          # Projects page (if in template)
    about/
      page.tsx          # About page (if in template)
    contact/
      page.tsx          # Contact page (if in template)
    products/
      page.tsx          # Products page (if commerce)
    product/[slug]/
      page.tsx          # Product detail (if commerce)
    cart/
      page.tsx          # Cart (if commerce)
    checkout/
      page.tsx          # Checkout (if commerce)
    globals.css         # Tailwind + brand tokens
  components/           # Module components
    HeroBasic.tsx
    ServicesGrid.tsx
    ...
  lib/
    brand.ts            # Brand token helpers
  public/               # Static assets
  package.json
  tsconfig.json
  next.config.js
  tailwind.config.js
```

**File Generation:**

- `app/layout.tsx`: Root layout with metadata, fonts, brand CSS
- `app/page.tsx`: Home page with assembled modules
- Additional route pages: One per template page
- Component files: Copy from module registry or generate
- Config files: Next.js, TypeScript, Tailwind setup
- `package.json`: Dependencies (Next.js, React, Tailwind, shadcn)

### 9. Verify Build

Run basic sanity checks:

- TypeScript compilation (`tsc --noEmit`)
- Check for missing imports
- Validate component props
- Ensure all required files exist

Log any warnings or errors.

### 10. Generate Build Report

Output a summary:

```
Build Report: <site-name>
─────────────────────────
Template: simple-builder-landing
Pages Created: 5
  - home
  - services
  - projects
  - about
  - contact

Modules Used: 12
  - hero_basic (5 instances)
  - services_grid (2 instances)
  - project_gallery_grid (2 instances)
  - testimonial_strip (2 instances)
  - lead_capture_form (1 instance)
  - contact_form_simple (1 instance)
  - map_embed (1 instance)

Assumptions:
  - Used default hero image placeholder
  - Generated service descriptions from industry keywords
  - Applied Forge Site brand palette

Output: output/<site-slug>/
Status: ✓ Ready for dev server
```

## Error Handling

- **Invalid JSON:** Stop, log error, return
- **Missing Required Fields:** List missing fields, stop
- **Template Not Found:** Fall back to `simple-builder-landing`, log warning
- **Module Not Found:** Skip module, log warning, continue
- **TypeScript Errors:** Log errors, continue (user can fix)
- **Missing Images:** Use placeholder, log note

## Build Script Usage

```bash
# From forge_site directory
npm run build-site -- --config path/to/business.json

# Or via TypeScript directly
npx tsx scripts/build-site-from-config.ts path/to/business.json
```

## Output Structure

Sites are generated into `output/<site-slug>/` where `site-slug` is derived from `businessName` (lowercase, hyphenated).

To run the generated site:

```bash
cd output/<site-slug>
npm install
npm run dev
```

The site should be fully functional and deployable to Vercel.

