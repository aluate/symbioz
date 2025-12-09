# Repository Inventory - Complete Repository Map

**Last Updated:** January 2025  
**Purpose:** Comprehensive inventory of repository structure, projects, tools, and documentation

---

## 📋 Table of Contents

1. [Repository Overview](#repository-overview)
2. [Directory Structure](#directory-structure)
3. [Active Projects](#active-projects)
4. [Infrastructure & Tools](#infrastructure--tools)
5. [Technology Stack](#technology-stack)
6. [Documentation Files](#documentation-files)
7. [Utility Scripts & Skills](#utility-scripts--skills)
8. [Dependencies & Relationships](#dependencies--relationships)

---

## Repository Overview

**Location:** `E:\My Drive\` (Google Drive synced repository)  
**Total Projects:** 10+ active projects  
**Documentation Files:** 744+ markdown files  
**Languages:** Python, TypeScript/JavaScript, Markdown

### Repository Stats
- **Active Projects:** 7+ major projects
- **Deployed Projects:** 2 (Catered By Me, Trim Calculator)
- **Utility Scripts:** 8+ in `tools/`
- **Infrastructure Systems:** Otto (SRE bot), Infra automation framework
- **Documentation:** Extensive control docs, status files, summaries

---

## Directory Structure

### Root Level Directories

```
E:\My Drive\
├── apps/                          # Application projects
│   ├── corporate-crashout/       # Trading/stock app (Next.js)
│   ├── life_os/                  # Life OS system (backend + frontend)
│   ├── otto/                     # Otto SRE bot system
│   ├── symbioz_cli/              # CLI game/app
│   ├── symbioz_web/              # Web version
│   └── wedding/                  # Wedding site (Next.js)
├── catered_by_me/                # Meal planning app (FastAPI + Next.js)
├── residential_repo/              # Construction automation systems
├── poled burn/pole_barn_calc/    # Construction calculator (Python/Tkinter)
├── vlg/                          # Valhalla Legacy Group business docs
├── dark_cda_world/               # Creative writing project
├── system built/book/            # Non-fiction book project
├── infra/                        # Infrastructure automation framework
├── tools/                        # Utility scripts and CLI tools
├── diagnostics/                  # Auto-generated diagnostic reports
├── symbioz/                      # Game project documentation
└── temp_*_clone/                 # Temporary/clone directories
```

### Key Files at Root

**Control Documents:**
- `AUTO_CONTROL_DOCUMENT.md` - Master behavior guide for AI assistants
- `PROJECT_INVENTORY.md` - Project status inventory (needs enhancement)
- `OTTO_REPO_INVENTORY_PROMPT.md` - Inventory prompt (just created)

**Setup/Reference:**
- `SETUP_INSTRUCTIONS.md`
- `ONE_CLICK_START_GUIDE.md`
- `QUICK_START_*.md` files

**Status/Summary Files (many - see Documentation section):**
- `*_SUMMARY.md` files
- `*_STATUS.md` files
- `COMPLETE_*.md` files

---

## Active Projects

### 1. **Catered By Me** (`catered_by_me/`)

**Status:** Phase 5 Complete - Ready for Stripe Integration  
**Type:** Meal planning web application  
**Stack:** FastAPI (backend), Next.js 14 (frontend), Supabase (database/auth)

**Deployment:**
- Backend: Render (`https://catered-by-me.onrender.com`)
- Frontend: Vercel
- Domain: `cateredby.me`

**Key Features:**
- Recipe parsing and schedule generation
- User accounts with Supabase auth
- Recipe bank and event management
- Capacity coaching and warnings
- Billing prep (ready for Stripe)

**Control Docs:**
- `control/CONTROL.md`
- `control/STRIPE_INTEGRATION.md`
- `PROJECT_STATUS.md`

---

### 2. **Residential Repo** (`residential_repo/`)

**Status:** Active Development  
**Type:** Construction automation systems  
**Stack:** FastAPI, Python, CSV/YAML configs

**Components:**
- **Trim Calculator** - FastAPI web app (deployed to Render)
- Automation roadmap (67 automation ideas tracked)
- Template system for new automations

**Key Files:**
- `control/automation-roadmap.md` - 67 automation ideas
- `control/automation-status.csv` - Status tracking
- `apps/web/trim_api.py` - Trim calculator API

---

### 3. **Pole Barn Calculator** (`poled burn/pole_barn_calc/`)

**Status:** Core Complete (~85%) - BOM Validation Phase  
**Type:** Construction estimating tool  
**Stack:** Python, Tkinter GUI, Excel export

**Key Features:**
- Geometry and material calculations
- BOM (Bill of Materials) system
- Excel export with category tabs
- Pricing and costing engine

**Documentation:**
- `ARCHITECTURE_OVERVIEW.md` - System architecture
- `DEVELOPMENT_LOG.md` - Development history
- `NEXT_STEPS_AND_GAPS.md` - Roadmap

---

### 4. **Wedding Site** (`apps/wedding/`)

**Status:** Ready to Deploy  
**Type:** Wedding website  
**Stack:** Next.js, TypeScript

**Status:** Fully prepared, needs GitHub repo creation and deployment

**Key Files:**
- `START_HERE.md` - Deployment guide
- `WEDDING_SITE_STATUS.md`
- `DEPLOY_WITH_OTTO.md`

---

### 5. **Corporate Crashout** (`apps/corporate-crashout/`)

**Status:** Active  
**Type:** Trading/stock application  
**Stack:** Next.js, TypeScript, Prisma

**Features:**
- Trading interface
- Account management
- Admin panel
- Discord integration

---

### 6. **Valhalla Legacy Group (VLG)** (`vlg/`)

**Status:** Documentation Complete - Framework Ready  
**Type:** Business documentation & planning  
**Format:** Markdown documentation

**Contains:**
- 4 brand guidelines (SMB, Grid, Stax, VLG)
- Business plans and roadmaps
- Website content
- Legal templates
- Operational playbooks

**Structure:**
- `control/CONTROL.md` - Master control doc
- `docs/` - Business plans, roadmaps
- `brands/` - Brand guidelines
- `apps/smb_site/` - SMB website (in progress)

---

### 7. **Otto (SRE Bot)** (`apps/otto/`)

**Status:** Phase 1 Complete - Core Skeleton  
**Type:** Infrastructure automation bot  
**Stack:** Python, YAML config

**Capabilities:**
- Repo listing and auditing
- Health checks
- Command execution
- Self-testing

**Files:**
- `CONTROL_OTTO.md` - Vision and architecture
- `otto/` - Python package
- `otto_config.yaml` - Configuration

---

### 8. **Life OS** (`apps/life_os/`)

**Status:** Active  
**Type:** Personal OS system  
**Stack:** Python backend, TypeScript frontend

**Components:**
- Backend API
- Frontend interface
- Control system

---

### 9. **Symbioz** (`symbioz/`, `apps/symbioz_*`)

**Status:** Active Development  
**Type:** Game/Interactive Story  
**Stack:** Python (CLI), Next.js (web)

**Components:**
- CLI version (`apps/symbioz_cli/`)
- Web version (`apps/symbioz_web/`)
- Character stories and world building

---

### 10. **Creative Projects**

**Dark CDA World** (`dark_cda_world/`):
- World Bible and origin stories
- 192 story files (174 markdown, 18 docx)

**System Built/Book** (`system built/book/`):
- 17 chapters + intro + outro
- Control documents and reference materials
- Story bank and examples

---

## Infrastructure & Tools

### Infrastructure Automation (`infra/`)

**Purpose:** Zero-click infrastructure management and diagnostics

**Structure:**
```
infra/
├── providers/              # Provider clients (Vercel, Render, Supabase, etc.)
│   ├── vercel_client.py
│   ├── render_client.py
│   ├── supabase_client.py
│   ├── stripe_client.py
│   ├── github_client.py
│   └── *.yaml             # Provider configs
├── utils/                 # Utility modules
│   ├── yaml_loader.py
│   ├── logging.py
│   ├── health_check.py
│   ├── secrets.py
│   └── template_generator.py
├── project-specs/         # Project specifications
│   ├── catered-by-me.yaml
│   └── wedding.yaml
├── templates/             # Project templates
│   ├── saas-starter/
│   ├── portfolio-site/
│   └── booking-leadgen/
└── config.yaml            # Main configuration
```

**Main Tool:** `tools/infra.py` - CLI interface

**Capabilities:**
- ✅ Diagnostics across all providers
- ✅ Project provisioning
- ✅ Deployment management
- ✅ Auto-fixing (Vercel, Render)
- ✅ Template generation
- ✅ Health checks

**Key Commands:**
- `python tools/infra.py diag` - Run diagnostics
- `python tools/infra.py provision-project` - Provision infrastructure
- `python tools/infra.py fix-vercel` - Auto-fix Vercel issues
- `python tools/infra.py list-templates` - List project templates

---

### Utility Scripts (`tools/`)

**Location:** `tools/` directory

1. **`infra.py`** - Main infrastructure CLI tool
   - Diagnostics, provisioning, deployment
   - Vercel/Render auto-fixing
   - Template generation

2. **`check_vercel_logs.py`** - Check Vercel build logs
   - Fetches deployment logs
   - Shows build status
   - Error detection

3. **`check_deployment.py`** - Deployment status check
   - Shows last 5 deployments
   - Status indicators
   - Quick terminal check

4. **`check_vercel_settings.py`** - Vercel settings check
   - Project configuration
   - Environment variables

5. **`check_both_deployments.py`** - Multi-project check
   - Check multiple deployments at once

6. **`check_catered_by_me.py`** - Catered By Me specific checks

7. **`push_to_my_github.py`** - Git operations helper
   - Push to GitHub
   - Commit automation

8. **`push_corporate_crashout.py`** - Project-specific push script

---

## Technology Stack

### Backend Technologies
- **Python:**
  - FastAPI (Catered By Me, Residential Repo)
  - Tkinter (Pole Barn Calculator GUI)
  - CLI tools and automation scripts

- **Node.js:**
  - Next.js 14 (multiple frontends)
  - TypeScript

### Frontend Technologies
- **React/Next.js:** Catered By Me, Wedding, Corporate Crashout, Symbioz Web
- **Tailwind CSS:** Multiple projects
- **TypeScript:** Type-safe frontends

### Databases & Services
- **Supabase:** Database and auth (Catered By Me)
- **Prisma:** ORM (Corporate Crashout)

### Deployment Platforms
- **Vercel:** Frontend deployments (multiple projects)
- **Render:** Backend deployments (Catered By Me, Trim Calculator)

### APIs & Integrations
- **Stripe:** Payment processing (configured, not yet integrated)
- **GitHub:** Repository management and CI/CD
- **Vercel API:** Deployment management
- **Render API:** Service management

### Configuration & Data
- **YAML:** Configuration files (infra, project specs)
- **CSV:** Data exports and configs (Residential Repo)
- **JSON:** Data storage and configs
- **Markdown:** Extensive documentation

---

## Documentation Files

### Documentation Categories

**1. Control Documents** (Single source of truth)
- `AUTO_CONTROL_DOCUMENT.md` - Master behavior guide
- `PROJECT_INVENTORY.md` - Project status (needs enhancement)
- Project-specific `CONTROL.md` files

**2. Status Files** (Current state tracking)
- `*PROJECT_STATUS.md` - Per-project status
- `*DEPLOYMENT_STATUS.md` - Deployment tracking
- `*TODO*.md` - Task lists

**3. Summary Files** (Completion summaries - many duplicates)
- `*SUMMARY.md` - 54+ summary files
- `COMPLETE_*.md` - Completion summaries
- `FINAL_*.md` - Final summaries

**4. Setup/Guide Files**
- `*SETUP*.md` - Setup instructions
- `*GUIDE*.md` - How-to guides
- `*QUICK_START*.md` - Quick start guides

**5. Development Logs**
- `*DEVELOPMENT_LOG.md`
- `*CHANGELOG.md`
- Project-specific logs

**6. Deployment Documentation**
- Multiple deployment guides (can be consolidated)
- Vercel-specific guides
- Render-specific guides

### Documentation Issues Identified

**Problems:**
1. **744+ markdown files** - Too many to navigate
2. **Multiple deployment guides** - Should be consolidated
3. **Redundant summary files** - Same information in multiple files
4. **Hard to find** - Common tasks require digging

**Recommendations:**
- Archive old summary files
- Consolidate deployment guides
- Create documentation index
- Establish naming standards

---

## Utility Scripts & Skills

### Infrastructure Skills (via `tools/infra.py`)

**Diagnostics:**
- `diag` - Check all services health
- Provider-specific checks (Vercel, Render, Supabase, Stripe, GitHub)

**Project Management:**
- `provision-project` - Create/update infrastructure
- `deploy` - Deploy and health check
- `list-templates` - Show available templates
- `generate-project` - Create from template

**Auto-Fixing:**
- `fix-vercel` - Auto-fix Vercel deployment errors
- `fix-render` - Auto-fix Render service issues

**Configuration:**
- `setup-vercel-project` - Configure Vercel project
- `configure-domain` - Set up custom domains
- `update-env-vars` - Manage environment variables

### Standalone Utilities

**Vercel Management:**
- `check_vercel_logs.py` - Fetch build logs
- `check_vercel_settings.py` - Check configuration
- `watch_vercel.py` - Real-time monitoring

**Deployment Checks:**
- `check_deployment.py` - Status check
- `check_both_deployments.py` - Multi-project check

**Git Operations:**
- `push_to_my_github.py` - Push automation
- Project-specific push scripts

### Otto Skills (`apps/otto/`)

**Current Skills:**
- `RepoListerSkill` - List repo structure
- `RepoAuditSkill` - Audit Otto repo
- Health checks and self-testing

**Planned Skills:**
- Google Drive integration
- Life OS integration
- LLM abstraction layer

---

## Dependencies & Relationships

### Cross-Project Dependencies

**Shared Infrastructure:**
- `tools/infra.py` used by multiple projects
- Otto system available to all projects
- Diagnostic system (`diagnostics/`) shared

**Technology Dependencies:**
- Multiple projects use Next.js
- FastAPI pattern shared (Catered By Me, Residential)
- Supabase auth pattern (Catered By Me)

**Documentation Dependencies:**
- `AUTO_CONTROL_DOCUMENT.md` governs all AI assistant behavior
- `PROJECT_INVENTORY.md` references all projects
- Control documents per project

### Project → Tool Mapping

| Project | Tools Used | Infrastructure |
|---------|-----------|----------------|
| Catered By Me | `tools/infra.py`, Vercel/Render clients | Otto configured |
| Wedding | `tools/infra.py`, deployment scripts | Otto configured |
| Residential Repo | FastAPI pattern | Templates available |
| Corporate Crashout | Git push scripts | Standard deployment |
| Pole Barn Calc | None (standalone) | None |

### Tool Dependencies

**`tools/infra.py` requires:**
- `infra/` directory structure
- Provider configs (`infra/providers/*.yaml`)
- Project specs (`infra/project-specs/*.yaml`)
- Environment variables (`.env` file)

**Vercel utilities require:**
- `infra/providers/vercel_client.py`
- Vercel API token
- Project configurations

---

## Key Findings & Recommendations

### Strengths
✅ Comprehensive infrastructure automation (Otto/Infra)  
✅ Clear project separation  
✅ Extensive documentation  
✅ Reusable patterns (FastAPI, Next.js)

### Issues Identified
⚠️ **Documentation sprawl** - 744+ MD files  
⚠️ **Hard to find common tasks** - No quick reference  
⚠️ **Redundant summaries** - Same info in multiple files  
⚠️ **Skills not catalogued** - Utilities exist but not documented together

### Immediate Actions Needed
1. Create Skills Library (catalog all utilities)
2. Create Problem-Solution Registry (document solved problems)
3. Consolidate documentation (archive, merge, index)
4. Create Quick Reference (common tasks cheat sheet)

---

## Next Steps

See `SKILLS_LIBRARY.md`, `PROBLEM_SOLUTION_REGISTRY.md`, and `QUICK_REFERENCE.md` for organized access to utilities and solutions.

---

**Last Updated:** January 2025  
**Next Review:** After major changes or new project additions


