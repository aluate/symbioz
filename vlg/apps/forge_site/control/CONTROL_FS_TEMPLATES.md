# Forge Site — Templates Control

## What Is a Template?

A template is a curated stack of modules organized into pages. Templates define:

- Which pages to create
- Which modules to use on each page
- The order of modules
- Default settings and styling

Templates are selected automatically based on business.json data, or can be specified explicitly.

## Template Selection Logic

The build system chooses a template based on:

1. **`primaryGoal`** from business.json:
   - `GET_LEADS` → `lead-capture` or `simple-builder-landing`
   - `SELL_PRODUCTS` → `commerce-lite`
   - `CREDIBILITY` → `simple-builder-landing`
   - `CLARITY` → `simple-builder-landing`

2. **`hasProducts`** flag:
   - `true` → `commerce-lite` (unless overridden)

3. **`industry`** hints:
   - Builder/trades → `simple-builder-landing`
   - Service-heavy → `lead-capture`
   - Retail/shop → `commerce-lite`

4. **Explicit `templateId`** in business.json (overrides auto-selection)

## Base Templates

### 1. simple-builder-landing

**Target:** Builders, trades, local professionals, service businesses

**Intent:** Showcase work, build trust, capture leads

**Pages:**

- **home:**
  - `hero_basic` - Main headline and CTA
  - `services_grid` - Top services
  - `project_gallery_grid` - Past work showcase
  - `testimonial_strip` - Social proof
  - `lead_capture_form` - Contact form

- **services:**
  - `hero_basic` - Page title
  - `services_grid` - Full service list
  - `cta_basic` - Call to action

- **projects:**
  - `hero_basic` - Page title
  - `project_gallery_grid` - Full project gallery

- **about:**
  - `hero_basic` - Page title
  - `content_two_column` - About story
  - `testimonial_strip` - Client feedback

- **contact:**
  - `hero_basic` - Page title
  - `contact_form_simple` - Contact form
  - `map_embed` - Location (if address provided)

**When to Use:**
- Builders, contractors, trades
- Local service professionals
- Designers, architects
- Any business that needs to show work and build trust

### 2. lead-capture

**Target:** Lead-gen heavy services (roofers, painters, HVAC, coaches, realtors)

**Intent:** Convert visitors into qualified leads quickly

**Pages:**

- **home (landing):**
  - `hero_basic` - Strong value proposition
  - `benefits_strip` - Key benefits
  - `lead_capture_form` - Short form (above fold)
  - `testimonial_strip` - Social proof
  - `faq_accordion` - Address objections

- **long-form:**
  - `hero_basic` - Detailed headline
  - `content_multi_section` - Extended sales copy
  - `lead_capture_form` - Long form with qualification fields
  - `testimonial_grid` - Multiple testimonials
  - `faq_accordion` - Comprehensive FAQ

- **contact/booking:**
  - `hero_basic` - Booking headline
  - `contact_form_simple` - Contact form
  - `map_embed` - Service area (if applicable)

**When to Use:**
- Services that rely on lead generation
- Ad-driven campaigns
- Funnel-focused businesses
- Quick conversion needs

### 3. commerce-lite

**Target:** Small shops, boutiques, product sellers (<50 products)

**Intent:** Simple product catalog with checkout

**Pages:**

- **home:**
  - `hero_basic` - Shop headline
  - `product_grid_simple` - Featured products
  - `testimonial_strip` - Reviews
  - `cta_basic` - Shop CTA

- **products:**
  - `hero_basic` - Products page title
  - `product_grid_simple` - Full product catalog

- **product/[slug]:**
  - `product_detail_basic` - Product info, images, add to cart

- **cart:**
  - `cart_page` - Cart items, totals

- **checkout:**
  - `checkout_page` - Stripe checkout integration

- **contact/support:**
  - `hero_basic` - Support headline
  - `contact_form_simple` - Support form
  - `faq_accordion` - Product/shipping FAQ

**When to Use:**
- Small product catalogs
- Boutique shops
- Handmade goods
- Simple e-commerce needs

## Template Composition Rules

1. **Every page starts with a hero** (usually `hero_basic`)
2. **Forms appear after trust signals** (testimonials, benefits)
3. **CTAs appear at natural break points**
4. **Gallery/showcase modules come after intro content**
5. **FAQ/trust modules appear before final CTAs**

## Customization

Templates can be extended by:

- Adding modules to existing pages
- Adding new pages
- Overriding module variants
- Custom styling via brand tokens

The build system applies these customizations from business.json when present.

