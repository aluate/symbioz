# Forge Site — Next Steps

## Immediate Priorities (v1 MVP)

### 1. Implement Core Module Components ⚡ HIGH PRIORITY

**Status:** Module registry exists, but no React components yet

**Tasks:**
- Create React components for top 10 most-used modules:
  - `HeroBasic.tsx` - Hero section with headline, subheadline, CTA
  - `ServicesGrid.tsx` - Grid of service cards
  - `ProjectGalleryGrid.tsx` - Project showcase grid
  - `TestimonialStrip.tsx` - Testimonial carousel/strip
  - `ContactFormSimple.tsx` - Basic contact form
  - `LeadCaptureForm.tsx` - Lead generation form
  - `FAQAccordion.tsx` - FAQ accordion component
  - `CTABasic.tsx` - Call-to-action section
  - `MapEmbed.tsx` - Map embed component
  - `ContentTwoColumn.tsx` - Two-column content layout

**Location:** `modules/page_modules/`

**Requirements:**
- Use Forge Site brand tokens (colors, typography)
- Accept props from business.json
- Be responsive and accessible
- Follow Forge Site design principles (calm, clean, professional)

### 2. Enhance Build Script to Use Modules ⚡ HIGH PRIORITY

**Status:** Build script generates basic pages, but doesn't use module components

**Tasks:**
- Update `build-site-from-config.ts` to:
  - Copy module components to generated site
  - Import and use modules in page generation
  - Pass correct props from business.json to modules
  - Generate pages with actual module composition

**Current:** Pages are basic placeholders
**Target:** Pages use real module components with business data

### 3. Create Example Business Configs 📋 MEDIUM PRIORITY

**Status:** No examples yet

**Tasks:**
- Create `examples/` directory with:
  - `example-builder.json` - Builder/contractor example
  - `example-lead-capture.json` - Service business example
  - `example-commerce.json` - Small shop example
  - `example-with-brand.json` - Example with brand input

**Purpose:** Help users understand the format and test the system

### 4. Implement Copy Generation 🎨 MEDIUM PRIORITY

**Status:** Copy generation is stubbed

**Tasks:**
- Enhance `generateCopy()` function in build script
- Create content block library in `templates/content_blocks/`
- Generate copy in Forge Site voice (Karl + Hemingway)
- Use brand voice guidelines when available
- Generate:
  - Headlines and subheadlines
  - Service descriptions
  - About page content
  - CTA text
  - Meta descriptions

**Future:** Could integrate AI/LLM for sophisticated generation

### 5. Test End-to-End Build Flow 🧪 MEDIUM PRIORITY

**Status:** Not tested yet

**Tasks:**
- Create test business.json files
- Run build script
- Verify generated sites:
  - TypeScript compiles
  - Pages render correctly
  - Modules work
  - Brand tokens applied
  - Can run `npm run dev` successfully
- Fix any issues found

### 6. Enhance Brand Generation with AI/LLM 🤖 LOW PRIORITY (Future)

**Status:** Uses rule-based generation

**Tasks:**
- Integrate AI/LLM (OpenAI, Anthropic, etc.) for:
  - Parsing conversation transcripts
  - Generating sophisticated color palettes
  - Extracting brand elements from natural language
  - Creating more nuanced voice guidelines
- Keep rule-based fallback for when AI unavailable

**Note:** Current rule-based system works, but AI would improve quality

## Secondary Features (v2)

### 7. Content Block Library

**Status:** Mentioned but not implemented

**Tasks:**
- Create reusable copy blocks in `templates/content_blocks/`
- Organize by industry (builder, service, shop, etc.)
- Include:
  - Hero headlines
  - CTA variations
  - Service descriptions
  - SEO snippets
- Use in copy generation

### 8. Logo Generation

**Status:** Mentioned in brand generation docs

**Tasks:**
- Generate logo concepts from brand system
- Create SVG logo files
- Apply to generated sites
- Multiple format outputs (SVG, PNG, favicon)

### 9. Image Placeholder System

**Status:** No image handling yet

**Tasks:**
- Generate placeholder images
- Handle image paths from business.json
- Create image optimization pipeline
- Support multiple image formats

### 10. Deployment Automation

**Status:** Manual deployment

**Tasks:**
- Add Vercel deployment script
- Auto-deploy generated sites
- Domain configuration helper
- Environment variable setup

## Documentation & Polish

### 11. User Guide

**Tasks:**
- Step-by-step guide for creating business.json
- How to customize templates
- How to add custom modules
- Troubleshooting guide

### 12. Developer Guide

**Tasks:**
- How to create new modules
- How to create new templates
- Module component patterns
- Brand token usage guide

### 13. Marketing Site Enhancements

**Tasks:**
- Add example sites showcase
- Add pricing page
- Add contact/intake form
- Add blog/docs section

## Testing & Quality

### 14. Unit Tests

**Tasks:**
- Test brand generation functions
- Test template selection logic
- Test module prop mapping
- Test copy generation

### 15. Integration Tests

**Tasks:**
- Test full build flow
- Test with various business.json configs
- Test brand generation integration
- Test error handling

## Recommended Order

**Week 1: Core Functionality**
1. Implement top 5 module components (Hero, Services, Gallery, Testimonials, Contact)
2. Update build script to use modules
3. Create example business configs
4. Test end-to-end build

**Week 2: Polish & Enhancement**
5. Implement remaining module components
6. Enhance copy generation
7. Add content block library
8. Improve error handling

**Week 3: Documentation & Launch Prep**
9. Write user guide
10. Enhance marketing site
11. Create deployment scripts
12. Final testing

**Future: Advanced Features**
- AI/LLM integration
- Logo generation
- Advanced image handling
- Multi-tenant hosting

## Quick Wins (Can Do Now)

1. **Create example business.json files** (15 minutes)
2. **Add basic error handling to build script** (30 minutes)
3. **Create simple HeroBasic component** (1 hour)
4. **Add build script validation** (30 minutes)
5. **Create README examples** (30 minutes)

## Questions to Answer

1. **Module Implementation:** Should modules be simple React components or more sophisticated with animations/transitions?
2. **Copy Generation:** Use templates, AI, or both?
3. **Brand Generation:** Keep rule-based or prioritize AI integration?
4. **Deployment:** Auto-deploy to Vercel or manual?
5. **Pricing:** When to launch pricing page and payment integration?

## Current State Summary

✅ **Complete:**
- Product scaffold and structure
- Control documentation
- Brand generation system (rule-based)
- Build script (basic)
- Marketing site
- Schema and registries

⏳ **In Progress:**
- Module components (0/22)
- Copy generation (stubbed)
- End-to-end testing (not started)

🎯 **Next Focus:**
Implement core module components and integrate into build script to get a working end-to-end flow.

---

**Get seen. Stay simple.**

