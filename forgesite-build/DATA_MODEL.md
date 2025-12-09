# Data Model Documentation

## Schema Structure

### BusinessIntakeSchema

The core intake schema that captures all business information needed to build a site.

**Required Fields:**
- `businessName` (string) - Name of the business
- `tradeType` (enum) - Type of trade: builder, remodeler, cabinet_shop, steel_buildings, hvac, electrical, plumbing, other
- `serviceArea` (string) - Geographic service area
- `services` (string[]) - Array of services offered
- `mainGoal` (enum) - Primary goal: get_leads, look_legit, recruit_staff, showcase_projects
- `contact` (object) - Contact information
  - `phone` (string) - Required
  - `email` (string) - Required, must be valid email
  - `address` (string) - Optional

**Optional Fields:**
- `ownerName` (string)
- `typicalJobSize` (string)
- `idealClientDescription` (string)
- `differentiators` (string[])
- `testimonials` (array) - Array of testimonial objects with name, quote, projectType
- `logoUrl` (string) - Must be valid URL
- `brandColors` (object) - primary, secondary, accent colors
- `brandVoice` (enum) - straightforward, premium, friendly, no_bullshit (default: straightforward)
- `packageLevel` (enum) - basic, pro, premium (default: basic)

### SiteConfigSchema

Extends BusinessIntakeSchema with site structure.

**Fields:**
- `business` (BusinessIntakeSchema) - All business intake data
- `pages` (array) - Array of page configurations
  - `route` (string) - URL route for the page
  - `title` (string) - Page title
  - `modules` (array) - Array of module configurations
    - `type` (string) - Module type identifier
    - `props` (object) - Props to pass to the module
- `seo` (object) - SEO metadata
  - `title` (string) - SEO title
  - `description` (string) - Meta description
  - `keywords` (string[]) - Optional keywords array

## Factory Modules

All client sites are constructed by composing these factory modules according to the intake and package selected. These modules are part of the **Website Factory Library** - proven, tested components optimized for builders, trades, and shops.

### Available Factory Modules

1. **hero** - Hero section with headline, subheadline, CTA
   - Props: `headline`, `subheadline`, `primaryCta`, `secondaryCta?`, `backgroundImage?`, `brandColors?`

2. **services-grid** - Grid of services with icons
   - Props: `services` (array), `columns?` (number, default: 3)

3. **project-gallery** - Image gallery with project showcases
   - Props: `projects` (array of {title, image, description?}), `columns?` (number)

4. **testimonial-strip** - Testimonials carousel/section
   - Props: `testimonials` (array from intake), `layout?` (carousel | grid)

5. **process-steps** - "How we work" step-by-step
   - Props: `steps` (array of {title, description, icon?})

6. **lead-capture** - Contact form with validation
   - Props: `title?`, `fields?` (custom field config)

7. **contact-block** - Contact info display
   - Props: `contact` (from intake), `layout?` (vertical | horizontal)

8. **faq-section** - Expandable FAQ items
   - Props: `faqs` (array of {question, answer})

9. **trust-bar** - Licenses, associations, years in business
   - Props: `badges` (array of {label, icon?}), `layout?` (horizontal | grid)

10. **split-feature** - Image + text split layout
    - Props: `image`, `title`, `content`, `reverse?` (boolean), `cta?`

## Factory Workflow

1. **Intake** - Client fills form or chats with Factory Assistant bot
2. **Validation** - BusinessIntakeSchema validates the data
3. **Config Generation** - System generates SiteConfig from intake
4. **Module Selection** - Appropriate factory modules selected based on package level and goals
5. **Page Assembly** - Layout compositor builds pages from config using factory modules
6. **Preview** - Preview site generated and deployed
7. **Review** - Client reviews and requests small config changes if needed
8. **Launch** - Site goes live

## Example Config Flow

```
Intake JSON → BusinessIntakeSchema.validate() → SiteConfigSchema.generate() → 
Module Mapping → Page Assembly → Preview Site
```
