# Forge Site — Module Registry Control

## What Is a Module?

A module is a self-contained, reusable page component or content block. Modules have:

- A clear purpose (showcase work, capture leads, display services)
- Defined data requirements
- A layout component file
- Intent tags that guide template assembly

Modules are the building blocks. Templates are curated stacks of modules.

## Module Schema

Every module in the registry must define:

### Required Fields

- **`id`** (string): Unique identifier, lowercase with underscores (e.g., `hero_basic`)
- **`name`** (string): Human-readable name (e.g., "Hero Basic")
- **`category`** (string): Grouping (hero, content, gallery, form, commerce, etc.)
- **`intentTags`** (array of strings): What this module does
  - `INFORM` - Provides information
  - `CONVERT` - Drives action
  - `SHOWCASE` - Displays work/products
  - `QUALIFY_LEAD` - Filters or qualifies visitors
  - `CAPTURE_LEAD` - Collects contact info
  - `SELL` - Facilitates purchase
  - `TRUST` - Builds credibility
- **`requiredFields`** (array of strings): Data keys needed from business.json
- **`optionalFields`** (array of strings): Nice-to-have data
- **`layoutComponentPath`** (string): Path to the React component file
- **`recommendedUseCases`** (array of strings): When to use this module

### Optional Fields

- **`dependencies`** (array of module IDs): Other modules that should come before/after
- **`variants`** (array): Different visual treatments of the same module
- **`notes`** (string): Implementation or design notes

## Example Module Definitions

### Hero Basic

- **id:** `hero_basic`
- **name:** Hero Basic
- **category:** hero
- **intentTags:** `INFORM`, `CONVERT`
- **requiredFields:** `headline`, `subheadline`, `primaryCTA.label`, `primaryCTA.href`
- **optionalFields:** `heroImage`, `secondaryCTA`
- **layoutComponentPath:** `modules/page_modules/HeroBasic.tsx`
- **recommendedUseCases:** 
  - Landing pages
  - Home pages
  - Campaign pages

### Services Grid

- **id:** `services_grid`
- **name:** Services Grid
- **category:** content
- **intentTags:** `INFORM`, `SHOWCASE`
- **requiredFields:** `services[]` (array with name, shortDescription)
- **optionalFields:** `serviceIcons`, `serviceImages`
- **layoutComponentPath:** `modules/page_modules/ServicesGrid.tsx`
- **recommendedUseCases:**
  - Service business home pages
  - Dedicated services pages
  - Multi-service showcases

### Project Gallery Grid

- **id:** `project_gallery_grid`
- **name:** Project Gallery Grid
- **category:** gallery
- **intentTags:** `SHOWCASE`, `TRUST`
- **requiredFields:** `projects[]` (array with title, images, location, type)
- **optionalFields:** `projectDescriptions`, `projectLinks`
- **layoutComponentPath:** `modules/page_modules/ProjectGalleryGrid.tsx`
- **recommendedUseCases:**
  - Builder portfolios
  - Designer showcases
  - Contractor work galleries

## Rules for Adding Modules

1. **One Purpose:** Each module should do one thing well
2. **Data-Driven:** All content comes from business.json or generated copy
3. **Reusable:** Should work across multiple templates
4. **Documented:** Clear required/optional fields
5. **Tested:** Should render correctly with sample data

## Module-to-Template Relationship

Templates define which modules to use and in what order. A template is essentially:

```json
{
  "id": "simple-builder-landing",
  "pages": {
    "home": ["hero_basic", "services_grid", "project_gallery_grid", "testimonial_strip", "lead_capture_form"],
    "services": ["hero_basic", "services_grid", "cta_basic"],
    "projects": ["hero_basic", "project_gallery_grid"],
    "about": ["hero_basic", "content_two_column", "testimonial_strip"],
    "contact": ["hero_basic", "contact_form_simple", "map_embed"]
  }
}
```

The build system assembles pages by instantiating each module in order with data from business.json.

