# Forge Site

**Get seen. Stay simple.**

Forge Site is a calm, professional, modular website system. It takes a simple business profile, selects proven templates and page modules, and generates a clean, modern, high-converting website ready to deploy.

## What It Is

Forge Site builds websites from JSON configs. You provide business information, we generate a complete Next.js site with:

- Clean, professional design
- Proven page layouts
- SEO-ready structure
- Brand-consistent styling
- Ready for Vercel deployment

No chaos. No guesswork. Just a clear path from business data to a live site.

## Quick Start

### 1. Create a Business Config

Create a `business.json` file with your business information. See `data/prompts/business_intake_form.md` for guidance, or use `data/prompts/business_json_schema.json` as a reference.

Example:

```json
{
  "businessName": "Acme Builders",
  "industry": "builder",
  "primaryGoal": "GET_LEADS",
  "description": "Quality custom home construction",
  "serviceAreas": ["Portland", "Beaverton"],
  "services": [
    { "name": "Custom Homes", "flagship": true },
    { "name": "Remodels" },
    { "name": "Additions" }
  ],
  "contact": {
    "phone": "503-555-0123",
    "email": "info@acmebuilders.com"
  }
}
```

### 2. Build the Site

Run the build script:

```bash
# From forge_site directory
npx tsx scripts/build-site-from-config.ts path/to/business.json
```

The script will:

- Validate your config
- Select the right template
- Assemble modules
- Generate copy
- Create a Next.js site in `output/<site-slug>/`

### 3. Run the Site

```bash
cd output/<site-slug>
npm install
npm run dev
```

Open http://localhost:3000 to see your site.

### 4. Deploy

The generated site is ready for Vercel:

```bash
cd output/<site-slug>
vercel
```

Or push to GitHub and connect to Vercel.

## How It Works

1. **Template Selection:** Forge Site picks a template based on your business type and goals
2. **Module Assembly:** Pages are built from reusable modules (hero, services, gallery, forms, etc.)
3. **Copy Generation:** Missing content is generated in the Forge Site voice (calm, direct, professional)
4. **Brand Application:** Colors, typography, and spacing are applied automatically
5. **Site Output:** A complete Next.js site is generated in the output directory

## Templates

Forge Site includes three base templates:

- **simple-builder-landing:** For builders, trades, local professionals
- **lead-capture:** For lead-gen heavy services
- **commerce-lite:** For small shops and product sellers

See `data/template_index.json` for details.

## Modules

Modules are reusable page components. See `data/module_registry.json` for the full list.

Common modules:

- Hero sections
- Service grids
- Project galleries
- Testimonials
- Contact forms
- Product catalogs
- Checkout flows

## Customization

### Brand Colors

Override default colors in `business.json`:

```json
{
  "brandColors": {
    "primary": "#5D7586",
    "secondary": "#F4F2EC"
  }
}
```

### Custom Pages

Add pages beyond the template defaults:

```json
{
  "pages": ["home", "services", "custom-page"]
}
```

### Explicit Template

Force a specific template:

```json
{
  "templateId": "simple-builder-landing"
}
```

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

## Future Directions

- **v2:** Web-based config editor and CMS
- **v3:** Multi-tenant hosting and white-label agency tooling
- **Module Library:** Expandable component library
- **Content Blocks:** Reusable copy blocks per industry

## License

See `LICENSE.md` for details.

## Support

For questions or issues, refer to the control docs in `control/` or check the build flow documentation.

---

**Get seen. Stay simple.**

