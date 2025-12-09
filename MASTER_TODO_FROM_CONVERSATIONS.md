# Master TODO List - From Conversations Since 6PM Dec 1, 2025

**Created:** December 2, 2025  
**Source:** All conversation threads from ~6PM Dec 1 onward  
**Status:** Active - Working through items

---

## 🎯 Priority 1: Critical Infrastructure

### 1. Otto - Persistent AI Agent (NEW)
**Status:** Not Started  
**Priority:** CRITICAL - Foundation for everything else

**Requirements:**
- Build Otto as a persistent AI agent that lives with all your files
- Must run locally or in infra you control (not dependent on ChatGPT/Cursor)
- Self-checking and auditing abilities
- Standing task to audit repo, look for inefficiencies, propose changes
- Should NOT auto-apply changes initially - proposal-based only
- Wire into Life OS for task intake and reporting

**Tasks:**
- [ ] Create `apps/otto/` structure (separate from infra/otto which is SRE bot)
- [ ] Implement core skeleton with skills, health checks, repo auditing
- [ ] Build LLM abstraction layer (provider-agnostic)
- [ ] Create RepoListerSkill and RepoAuditSkill
- [ ] Implement CLI commands: `otto run-sample`, `otto health`, `otto audit`
- [ ] Wire into Life OS for task management

**Reference:** See conversation thread starting around line 975 in source document

---

### 2. Life OS - Household Management App
**Status:** Not Started  
**Priority:** CRITICAL - Central hub for all personal automation

**Requirements:**
- Kanban-style task management (like CateredByMe swim lanes but for life tasks)
- Integration with Otto for automation
- Personal calendar integration
- Email/text scanning for todos
- Bill tracking and income tracking
- Tax preparation support

**Tasks:**
- [ ] Create `apps/life_os/` structure
- [ ] Build kanban board for household tasks
- [ ] Integrate Otto for task automation
- [ ] Add calendar integration
- [ ] Build email/text scanning for todos
- [ ] Implement bill and income tracking
- [ ] Build Tax Brain module (see below)

---

## 🎯 Priority 2: Wedding Website

### 3. Wedding Website - GitHub Repo & Deployment
**Status:** Not Started  
**Priority:** HIGH

**Requirements:**
- GitHub repo named `wedding` (public)
- Deploy to Vercel (prefer Vercel over Render for this)
- Admin logins with kanban-style project management
- Similar to CateredByMe swim lanes but for wedding tasks
- Consider moving kanban to general Life OS app, wedding site as showcase

**Tasks:**
- [ ] Create GitHub repo `wedding`
- [ ] Set up Next.js project structure
- [ ] Configure Vercel deployment
- [ ] Build admin kanban board for wedding tasks
- [ ] Create public-facing wedding site pages
- [ ] Add RSVP system
- [ ] Add T-Rex style game (`/game` route)
- [ ] Mobile dashboard for real-time RSVP tracking

**Reference:** See conversation starting around line 12 in source document  
**Config:** See `wedding_config.json` structure around line 5502

---

## 🎯 Priority 3: Audiobook System

### 4. Audiobook Studio - Multi-Actor Voice System
**Status:** Not Started  
**Priority:** MEDIUM

**Requirements:**
- Build inside Life OS app
- Convert manuscripts to role-tagged scripts with stage directions
- Map roles (NARRATOR, DAD, BAD_GUY, MOM, LITTLE_GIRL) to voice models
- Call external TTS/voice cloning API (e.g., ElevenLabs)
- Listen while editing, drop notes, re-render sections
- Integration with Otto for automation

**Tasks:**
- [ ] Create `control/CONTROL_AUDIO.md` in residential_repo
- [ ] Create folder structure: `content/books/example_book/`
- [ ] Create `audio_control.yaml` template
- [ ] Create `script_tagged.md` example
- [ ] Build Life OS backend endpoints for audio
- [ ] Implement audio engine module
- [ ] Build frontend UI in Life OS
- [ ] Integrate with Otto for script tagging automation

**Reference:** See conversation starting around line 56, detailed spec around line 271

---

## 🎯 Priority 4: Tax Brain

### 5. Tax Brain - Life OS Module
**Status:** Not Started  
**Priority:** MEDIUM

**Requirements:**
- Module inside Life OS app
- Track bills, income, transactions
- Auto-categorize transactions for tax purposes
- Generate year-end tax summaries
- Fill tax forms based on data
- Rule engine for categorization

**Tasks:**
- [ ] Create `apps/life_os/tax/` module structure
- [ ] Build data models (TaxProfile, TaxCategory, TaxRule, Transaction, TaxYearSummary)
- [ ] Implement rule engine for auto-categorization
- [ ] Build year-end package generator
- [ ] Create TaxBrain service layer
- [ ] Build FastAPI endpoints
- [ ] Create frontend UI in Life OS
- [ ] Integrate with bill/income tracking

**Reference:** See conversation starting around line 1639, detailed spec around line 1644

---

## 🎯 Priority 5: Project Management

### 6. Master Project List
**Status:** Not Started  
**Priority:** HIGH

**Requirements:**
- Updated list of everything we're working on
- Priority ranking for each item
- Next steps on each item
- All steps needed to complete each item
- Integration with Life OS kanban

**Tasks:**
- [ ] Audit all active projects
- [ ] Create master project list document
- [ ] Assign priority rankings
- [ ] Break down each project into steps
- [ ] Integrate with Life OS kanban board
- [ ] Set up Otto to track and update projects

**Reference:** See conversation around line 98

---

## 🎯 Priority 6: Symbioz Character Stories

### 7. Symbioz Canon Characters
**Status:** Not Started  
**Priority:** LOW (Creative project)

**Requirements:**
- Generate 10 canonical character stories
- Cross-validate against lore bible
- 1,800-2,600 words per story
- Dark CDA tone
- Mechanical anchoring to game systems

**Tasks:**
- [ ] Read all Symbioz design docs
- [ ] Create CHARACTER_ROSTER.md (10 characters)
- [ ] Create BIO_SUMMARIES.md
- [ ] Write first full story (wait for approval)
- [ ] Run devil's advocate pass
- [ ] Rewrite in Dark CDA tone
- [ ] Repeat for remaining 9 characters

**Reference:** See conversation starting around line 18000, detailed prompt around line 18319

---

## 📋 Notes & Decisions

### Key Decisions Made:
1. **Otto** - Must be persistent, local, provider-agnostic AI agent
2. **Life OS** - Central hub for household management, kanban-style
3. **Wedding Site** - Vercel deployment, public repo, kanban admin
4. **Audiobook** - Multi-actor system, Life OS integration
5. **Tax Brain** - Life OS module, rule-based categorization

### Blockers:
- Life OS doesn't exist yet - need to create structure first
- Otto (new version) needs to be built from scratch (different from infra/otto)
- Wedding site needs domain and design decisions

### Next Immediate Steps:
1. Create Life OS app structure
2. Build Otto core skeleton
3. Create wedding repo and basic structure
4. Set up master project list

---

**Last Updated:** December 2, 2025

