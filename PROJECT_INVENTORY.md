# Project Inventory — My Drive Repository

**Last Updated:** January 2025  
**Purpose:** Comprehensive inventory of completed work, in-progress items, and planned initiatives across all projects in this repository.

---

## 📋 Overview

This repository contains multiple active projects across different domains:
1. **Catered By Me** - Meal planning web application
2. **Residential Repo** - Construction automation systems
3. **Pole Barn Calculator** - Construction estimating tool
4. **Valhalla Legacy Group (VLG)** - Business documentation & planning
5. **Dark CDA World** - Creative writing project
6. **System Built/Book** - Non-fiction book project
7. **Infra** (Empty) - Infrastructure/automation framework (planned)

---

## 🎯 CATERED BY ME

**Status:** Phase 5 Complete (Billing Prep), Ready for Stripe Integration  
**Repository:** `catered_by_me/`

### ✅ COMPLETED

#### Phase 0: MVP
- ✅ Backend API with recipe parsing
- ✅ Schedule generation with station-based task allocation
- ✅ Basic frontend with form + schedule view
- ✅ Deployed to Render (backend) and Vercel (frontend)

#### Phase 1: Visual Refresh
- ✅ Design system with brand colors
- ✅ Updated hero section with new taglines
- ✅ "How It Works" section
- ✅ Footer redesign

#### Phase 2: UI Modernization
- ✅ Professional Header component with navigation
- ✅ Footer component with organized links
- ✅ Button component system
- ✅ Redesigned landing page
- ✅ "Built for Hosts Like You" persona section
- ✅ Responsive mobile design

#### Phase 3: User Accounts & Recipe Bank
- ✅ **Phase 3A:** Supabase auth + foundation (auth provider, sign in/up pages, profile auto-creation)
- ✅ **Phase 3B:** "My Recipes" with real data (CRUD operations)
- ✅ **Phase 3C:** "My Events" with real data (Upcoming/Past tabs, attach recipes, generate plans)
- ✅ **Phase 3D:** Dashboard + Profile + Kitchen Capacity (fully implemented)
- ✅ **Phase 3E:** Capacity Coaching & Warnings (backend checks, frontend warnings)
- ✅ **Phase 3F:** Polish & Monetization Prep (grocery list enhancements, print layout, pricing page)

#### Phase 3.5: UX Polish & Microcopy
- ✅ Toast notification system
- ✅ Expanded microcopy system (messages.ts)
- ✅ Empty states with personality
- ✅ First-time user explainer on dashboard
- ✅ Recipe color coding helper
- ✅ Shareable read-only links for events
- ✅ Share page for public event viewing

#### Phase 4: Launch Readiness
- ✅ Central error handler with user-friendly messages
- ✅ Retry logic in API calls (exponential backoff)
- ✅ Backend logging (structured logging)
- ✅ Rate limiting middleware
- ✅ Email capture on landing page (waitlist API + form)
- ✅ Pricing page improvements (feature comparison table)

#### Phase 5: Billing Prep
- ✅ UpgradePrompt component for soft paywall
- ✅ Limit checking in event/recipe creation pages
- ✅ PDF export gating based on user tier
- ✅ Share feature gating (ready for Stripe)

#### Phase 6: Launch Hardening
- ✅ ErrorBoundary component for React error handling
- ✅ All critical error paths handled gracefully

#### Infrastructure
- ✅ GitHub repository: `aluate/catered_by_me`
- ✅ Render backend deployment
- ✅ Vercel frontend deployment
- ✅ Environment variables configured
- ✅ CORS properly set up
- ✅ Domain purchased: `cateredby.me`
- ✅ Brand guide and logo system (clock logo with fork/knife hands)

### 🚧 IN PROGRESS

**Nothing actively in progress** - Project is in maintenance/polish mode

### 📝 PLANNED / NEXT STEPS

#### Immediate Priority:
1. **Stripe Integration** - See `control/STRIPE_INTEGRATION.md` and `PROMPT_STRIPE_IMPLEMENTATION.md`
   - Payment processing
   - Subscription management
   - Tier upgrades

#### Future Enhancements:
- Recipe input upgrades (image OCR, URL parsing, PDF parsing)
- Recipe color coding in schedule view
- First-run walkthrough
- Starter pack / sample events
- Week view calendar
- Shareable game plan links with task assignment
- Task assignment to guests/co-hosts
- Print-friendly kitchen poster layout
- Recipe templates marketplace

**Key Documentation:**
- `PROJECT_STATUS.md` - Complete status tracking
- `IMMEDIATE_NEXT_STEPS.md` - Pre-deployment checklist
- `DEPLOYMENT_STATUS.md` - Deployment tracking
- `control/STRIPE_INTEGRATION.md` - Stripe implementation guide

---

## 🔨 RESIDENTIAL REPO

**Status:** Active Development — Multiple Automation Systems  
**Repository:** `residential_repo/`

### ✅ COMPLETED

#### Core Systems (Implemented):
- ✅ **Trim Calculator** - FastAPI web app (`apps/web/trim_api.py`)
  - Deployed to Render
  - Mobile-friendly interface
  - Trim takeoff and pricing calculations
  
#### Infrastructure:
- ✅ Project structure established
- ✅ Automation roadmap documented (`control/automation-roadmap.md`)
- ✅ Status tracking system (`control/automation-status.csv`)
- ✅ Playbooks structure (`control/playbooks/`)
- ✅ Configuration system (`config/` with YAML/CSV files)

#### Documentation:
- ✅ Master README
- ✅ SOP index (`docs/SOP_INDEX.md`)
- ✅ Residential SOP notes (`docs/RESIDENTIAL_SOP_NOTES.md`)
- ✅ Automation templates (`new automation/project-overview.md`, `data-schema.md`, `cursor-build-prompt.md`)

### 🚧 IN PROGRESS

**Trim Calculator Enhancements:**
- Active development on trim takeoff features
- Mobile interface improvements

**Automation Framework:**
- Standardized automation build process
- Template system for new automations

### 📝 PLANNED (Per Roadmap)

#### High Priority (P1 - First Wave):
1. **AUTO-TRIM-01, AUTO-TRIM-02, AUTO-TRIM-03** - Trim takeoff + mobile-friendly app
2. **AUTO-DEC-01, AUTO-SPEC-01** - Intake → Decisions → Spec bridge
3. **AUTO-CV-01** - CV room auto-redraw proof of concept

#### Medium Priority (P2 - Second Wave):
- **AUTO-CONTRACT-01, AUTO-BILL-01** - Contract generation & billing calculator
- **AUTO-EMAIL-01, AUTO-EMAIL-02** - Email template renderer & stage-based wizard
- **AUTO-SCHED-01** - Back-plan engine for scheduling

#### Full Automation List (67 total):
See `control/automation-roadmap.md` for complete list organized by:
- Lead & Intake / CRM (AUTO-INT-01 through AUTO-INT-04)
- Decisions & Room Matrix (AUTO-DEC-01 through AUTO-DEC-03)
- Spec Sheet & CV Bridge (AUTO-SPEC-01 through AUTO-SPEC-03)
- CV Geometry & Redraw (AUTO-CV-01 through AUTO-CV-04)
- Estimating & Contracts (AUTO-EST-01, AUTO-CONTRACT-01, AUTO-BILL-01)
- Scheduling & Capacity (AUTO-SCHED-01 through AUTO-SCHED-03)
- Email & Communication (AUTO-EMAIL-01 through AUTO-EMAIL-03)
- Install & Field Tools (AUTO-INSTALL-01 through AUTO-INSTALL-03)
- Warranty / Service (AUTO-WARR-01 through AUTO-WARR-03)
- Reporting & Dashboards (AUTO-REP-01 through AUTO-REP-03)
- Trim Takeoff & Finish Pricing (AUTO-TRIM-01 through AUTO-TRIM-04)
- Meta / Repo Maintenance (AUTO-META-01 through AUTO-META-03)

**Key Documentation:**
- `control/automation-roadmap.md` - Master automation tracking
- `control/automation-status.csv` - Status tracking (currently empty)
- `new automation/` - Templates for building new automations
- `README.md` - Project overview

---

## 🏗️ POLE BARN CALCULATOR

**Status:** Core Complete (~85%), Ready for BOM Validation & Feature Completion  
**Repository:** `poled burn/pole_barn_calc/`

### ✅ COMPLETED

#### Phase 1: Structure and Data Models
- ✅ Project structure and organization
- ✅ All data model definitions (dataclasses)
- ✅ CLI interface for accepting inputs
- ✅ GUI interface (tkinter)

#### Phase 2: Core Calculations
- ✅ Geometry calculations (all derived dimensions)
- ✅ Material quantity calculations (assemblies)
- ✅ Pricing & costing engine
- ✅ Granular markup controls (material, labor, subcontractor, overhead)

#### Phase 3: BOM System
- ✅ BOM expansion system (assemblies → parts)
- ✅ Excel export with category tabs
- ✅ JSON project export
- ✅ CSV flat export (with sheet_name column)
- ✅ Panel length breakdown (gable panels)
- ✅ Lumber stock length packing (8, 10, 12, 14, 16 ft)
- ✅ J-channel trim with stick packing algorithm
- ✅ Sheathing assemblies (OSB/plywood as sheets)
- ✅ Concrete slab assemblies (cubic yards + reinforcement)
- ✅ Overhead door assemblies

#### Phase 4: BOM Accuracy Fixes
- ✅ Panel quantity engine (whole integers, no fractions)
- ✅ Material takeoff override (matches BOM exactly)
- ✅ Full lumber stock-length packing (all framing items)
- ✅ Sheathing as sheets (not sqft)
- ✅ Consistency cleanup (all length-based items properly tracked)

#### Testing:
- ✅ Test building generator (4 test buildings)
- ✅ Test exports (Excel, CSV, JSON)
- ✅ All test buildings regenerate successfully

#### Configuration:
- ✅ Parts catalog with coverage dimensions
- ✅ Pricing library
- ✅ Assembly mappings
- ✅ Waste factors and labor per unit

### 🚧 IN PROGRESS

**BOM Validation Phase:**
- ⏳ **READY FOR REVIEW** - 4 test building BOMs generated
- Need user validation of quantities against real-world expectations

### 📝 PLANNED / NEXT STEPS

#### Tier 1 - Must-Happen First (Foundational):
1. **Validate BOM Accuracy** ⚠️ **CRITICAL - DO THIS NOW**
   - Review 4 test building BOMs
   - Verify panel counts, lumber lengths, J-channel sticks, sheathing sheets
   - Fix any discrepancies before new features

2. **Complete Trim System** (HIGH PRIORITY)
   - J-channel done ✅
   - Still needed: Rake trim, Eave trim, Ridge cap, Base trim, Corner trim
   - Implement packing algorithms similar to J-channel

#### Tier 2 - Costing Logic + Markups:
3. **Finalize Costing Engine** (HIGH PRIORITY)
   - Validate markup calculations
   - Test edge cases
   - Ensure markups applied correctly

#### Tier 3 - MEP Allowances:
4. **Derived MEP Defaults** (MEDIUM-HIGH PRIORITY)
   - Auto-calculation based on building size/doors
   - Electrical: outlet count, switches, lights, wire LF, subpanel
   - Plumbing: hose bibs, bathroom rough-in, floor drain
   - Mechanical: ventilation fans, heater rough-in

#### Tier 4 - UI/UX Refinements:
5. **GUI Cleanup & Workflow** (MEDIUM PRIORITY)
   - Organize inputs into logical tabs/sections
   - Add validation and error messages
   - Improve results display
   - Add "Save Project" / "Load Project" functionality

#### Tier 5 - Advanced Features:
6. **Interior Framing Modules** (MEDIUM PRIORITY)
   - Office framing (2×4 walls, drywall, insulation)
   - Bathroom framing
   - Mezzanine framing

7. **Pricing Override UI** (LOW-MEDIUM PRIORITY)
   - Per-project price adjustments without editing CSVs

8. **Vendor Integration** (LOW - Future)
   - API integrations with vendors
   - Auto-update pricing from vendor feeds

#### Known Gaps:
- Fastener quantities not yet calculated per SF/LF
- Post hole concrete may need refinement
- Ridge offset input not fully used
- Shed roof logic may need separate calculation path
- Multiple door/window sizes (currently assumes all same size)
- Lap siding/Stucco exterior finishes not fully implemented
- Regional pricing adjustments
- Volume discounts
- Subcontractor line items

**Key Documentation:**
- `ARCHITECTURE_OVERVIEW.md` - Complete system architecture
- `DEVELOPMENT_LOG.md` - Full development history
- `NEXT_STEPS_AND_GAPS.md` - Detailed roadmap
- `PROJECT_EXPORT_FULL.md` - Codebase snapshot
- `README.md` - Project overview

---

## 🏛️ VALHALLA LEGACY GROUP (VLG)

**Status:** Documentation Complete — Framework Ready for Implementation  
**Repository:** `vlg/`

### ✅ COMPLETED

#### Documentation Framework:
- ✅ Master control document (`control/CONTROL.md`)
- ✅ Complete brand guidelines for all 4 brands:
  - Sugar Mountain Builders (SMB)
  - Grid Cabinet Systems
  - Stax Modular
  - Valhalla Legacy Group
- ✅ Business plan (`docs/business_plan.md`)
- ✅ Development roadmap (Phase 0-7) (`docs/roadmap.md`)
- ✅ Website content for all 4 brands (`web/`)
- ✅ Product catalogs:
  - Grid SKU catalog
  - QuickBuild™ program
  - Strategic Stock Reserve
  - Stax module catalog
  - Options packages (Quartz/Garnet/Sapphire)
- ✅ Financial models:
  - Startup costs
  - Unit economics (Grid & Stax)
  - Cashflow model outline
- ✅ Legal templates:
  - Builder letter of intent
  - Joint venture spec home template
  - Modular purchase agreement
  - Cabinet purchase terms
  - Facility lease
- ✅ Operational playbooks:
  - Grid operations playbook
  - Stax operations playbook
  - SMB operations playbook
- ✅ Strategic documents:
  - Sales strategies
  - Supply chain strategy
  - Organizational chart
  - Repository summary

#### Web Assets:
- ✅ SMB website content
- ✅ Brand color palettes and guidelines
- ✅ Complete brand briefs with taglines, typography, visual direction

### 🚧 IN PROGRESS

**Website Development:**
- ⏳ `apps/smb_site/` - SMB website in progress (34 files, Next.js/React)

### 📝 PLANNED

#### Implementation Phases:
- **Phase 0:** Current (Grid launch, SMB expansion)
- **Phase 1:** Grid launch + SMB expansion
- **Phase 2:** Land acquisition
- **Phase 3:** Grid facility
- **Phase 4:** Stax prototype yard
- **Phase 5:** Full factory
- **Phase 6:** Prototype village
- **Phase 7:** 200-unit builder partnership

#### Website Development:
- Complete SMB website
- Grid website
- Stax website
- Valhalla website

#### Operations:
- Implement operational playbooks
- Set up Grid production SOPs
- Set up Stax production SOPs
- Set up SMB project SOPs

**Key Documentation:**
- `control/CONTROL.md` - Master control document
- `docs/business_plan.md` - Complete business plan
- `docs/roadmap.md` - Phased development roadmap
- `README.md` - Repository overview

---

## 📚 SYSTEM BUILT / BOOK PROJECT

**Status:** Active Writing Project  
**Repository:** `system built/book/`

### ✅ COMPLETED

#### Book Structure:
- ✅ Core control documents:
  - `core/control-document.md` - Master control doc
  - `core/voice-guide.md` - Tone and voice guidelines
  - `core/metaphor-guide.md` - Key metaphors
  - `core/outline.md` - Book outline
  - `core/system-four-moves.md` - AI partner control document
- ✅ Complete chapter drafts (17 chapters + intro + outro):
  - ch01.md through ch17.md
  - intro.md
  - outro.md
- ✅ Reference materials:
  - `reference/loops-examples.md`
  - `reference/parts-examples.md`
  - `reference/questions-examples.md`
  - `reference/universal-applications.md`
- ✅ Story bank (`core/story-bank.md`)

### 🚧 IN PROGRESS

**Content Development:**
- ⏳ Chapter revisions and polish
- ⏳ Draft consolidation

### 📝 PLANNED

#### Completion Tasks:
- Final chapter revisions (see `todo/revisions.md`)
- Punchlist items (see `todo/punchlist.md`)
- Additional drafts in `drafts/` folder:
  - alt-openings.md
  - jokes-and-asides.md
  - scraps.md

**Key Documentation:**
- `core/control-document.md` - Master book control doc
- `core/system-four-moves.md` - AI collaboration framework
- `todo/revisions.md` - Revision tracking
- `todo/punchlist.md` - Completion checklist

---

## ✍️ DARK CDA WORLD

**Status:** Creative Writing Project  
**Repository:** `dark_cda_world/`

### ✅ COMPLETED

#### Content:
- ✅ World Bible (`bible_md/world_bible.md`)
- ✅ Origin Story Bible (`stories/origin_story_bible.md`)
- ✅ Origin Stories (`stories/origin/` - 192 files: 174 markdown, 18 docx)

### 🚧 IN PROGRESS

**Writing:**
- ⏳ Story development and expansion

### 📝 PLANNED

- Continue story development
- Organize and structure story collection
- Production/publishing preparation

---

## 🔧 INFRASTRUCTURE / "LONGER ARM" PROJECT

**Status:** PLANNED — Not Yet Started  
**Repository:** `infra/` (currently empty)

### 📝 CONCEPT

Based on templates and control documents found in the repository, the "longer arm" project appears to be about building:

#### Proposed Framework:
1. **AI Project Co-Pilot System**
   - Standardized project templates
   - Control document framework
   - Cross-project knowledge management
   - Automation generation templates

2. **Standardized Automation Builder**
   - Template system (see `residential_repo/new automation/`)
   - Data schema templates
   - Build prompts for consistent automation creation
   - Project structure standardization

3. **Cross-Project Intelligence**
   - Knowledge base system
   - Pattern recognition across projects
   - Shared utilities and components
   - Documentation standards

#### Key Templates Found:
- `residential_repo/new automation/cursor-build-prompt.md` - Automation build template
- `residential_repo/new automation/data-schema.md` - Data schema template
- `residential_repo/new automation/project-overview.md` - Project overview template
- `system built/book/core/system-four-moves.md` - AI partner control document

#### Potential Features:
- Standardized project scaffolding
- Cross-project code sharing
- Automated documentation generation
- Project status dashboard
- Knowledge graph of all projects
- Shared component library
- Automation template library

**Next Steps:**
1. Define scope and requirements for "longer arm" system
2. Design architecture for cross-project framework
3. Create initial templates and structure
4. Build core utilities and shared components
5. Integrate with existing projects

---

## 📊 SUMMARY STATISTICS

### Projects by Status:

**Production/Deployed:**
- ✅ Catered By Me (deployed to Render + Vercel)
- ✅ Trim Calculator (deployed to Render)

**Active Development:**
- 🔨 Residential Repo (multiple automations in progress)
- 🔨 Pole Barn Calculator (85% complete, validation phase)
- 🔨 SMB Website (in progress)

**Documentation/Planning:**
- 📚 Valhalla Legacy Group (framework complete, ready for implementation)
- 📚 System Built/Book (writing in progress)
- 📚 Dark CDA World (creative writing)

**Planned:**
- 📝 Infrastructure/"Longer Arm" Project (not started)

### Total Automation Ideas Tracked:
- **Residential Repo:** 67 automation ideas (AUTO-INT-01 through AUTO-META-03)
- **Status:** Mostly in "Idea" phase, few in "Prototyping" or "In Use"

### Lines of Code (Estimated):
- **Catered By Me:** ~10,000+ lines (backend + frontend)
- **Pole Barn Calculator:** ~8,000+ lines
- **Residential Repo:** ~5,000+ lines (growing)
- **Total:** ~25,000+ lines across all projects

---

## 🎯 IMMEDIATE PRIORITIES (Cross-Project)

### Critical Path Items:
1. **Catered By Me** - Stripe integration (blocking monetization)
2. **Pole Barn Calculator** - BOM validation (blocking production release)
3. **Residential Repo** - Trim calculator enhancements (P1 automation)

### High-Value Next Steps:
1. **Infrastructure Project** - Define and begin "longer arm" framework
2. **Residential Repo** - Implement P1 automations from roadmap
3. **Pole Barn Calculator** - Complete trim system after BOM validation

---

## 📝 NOTES FOR FUTURE SESSIONS

### Patterns Identified:
- Heavy use of control documents for project management
- Template-driven automation building approach
- Focus on mobile-friendly, field-usable tools
- Construction/estimation domain expertise throughout
- Multi-project knowledge sharing opportunities

### Common Technologies:
- FastAPI (Python) for backends
- Next.js/React for web frontends
- Supabase for database/auth
- Render for backend hosting
- Vercel for frontend hosting
- CSV/JSON for configuration
- Excel export for BOMs/reports

### Documentation Standards:
- Control documents as single source of truth
- Status tracking files (PROJECT_STATUS.md, automation-status.csv)
- Development logs for history
- Architecture overviews for complex systems
- Next steps/gaps documents for roadmaps

---

**Last Inventory Update:** January 2025  
**Next Review:** After major milestones or new project additions

