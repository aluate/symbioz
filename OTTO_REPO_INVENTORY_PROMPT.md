# Otto: Full Repository Inventory & Skill Management System

**Purpose:** This is a comprehensive prompt for Otto to conduct a full inventory of the Google Drive repository and establish systems to prevent code duplication, accumulate reusable skills, and manage documentation effectively.

**Priority:** HIGH - Repository is getting unwieldy, problems are being solved repeatedly, and documentation is becoming cumbersome.

---

## 🎯 Mission Overview

You are to:

1. **Conduct a full repository inventory** - Understand everything in the repo
2. **Establish a Skill Library System** - Create reusable, additive skills instead of rewriting code
3. **Create a Problem-Solution Registry** - Document solved problems so they don't need solving again
4. **Audit and consolidate documentation** - Reduce MD file sprawl while preserving valuable history
5. **Create a Quick Reference Guide** - Make common tasks easily discoverable

---

## 📋 Phase 1: Full Repository Inventory

### Task 1.1: Map Repository Structure

Create a comprehensive inventory document at `REPO_INVENTORY.md` that includes:

1. **Project Directory Structure**
   - Every major project directory (`apps/`, `infra/`, `tools/`, etc.)
   - Subdirectories and their purposes
   - File counts and types per directory

2. **Active Projects List**
   - Project name, status (Active/Archived/Planning), location
   - Primary technology stack
   - Deployment status (if applicable)
   - Reference to control documents

3. **Infrastructure Components**
   - Otto system (`apps/otto/`)
   - Infra automation (`infra/`, `tools/infra.py`)
   - Utility scripts (`tools/`)
   - Diagnostics system (`diagnostics/`)

4. **Documentation Inventory**
   - All `*.md` files organized by:
     - **Active/Current** - Still referenced and updated
     - **Historical/Archive** - Important history but not actively maintained
     - **Redundant/Consolidate** - Can be merged or removed
   - Summary files (`*SUMMARY*.md`, `*STATUS*.md`, etc.)
   - Control documents (`*CONTROL*.md`)

5. **Skill/Utility Inventory**
   - All Python scripts in `tools/` and their purposes
   - Infra skills/capabilities (`infra/` structure)
   - Otto skills (`apps/otto/` skills)
   - CLI commands available

### Task 1.2: Technology Stack Audit

Document all technologies used:
- Programming languages and versions
- Frameworks and libraries
- Deployment platforms (Vercel, Render, etc.)
- APIs and services integrated
- Configuration management systems

### Task 1.3: Dependency Map

Create a dependency graph:
- Which projects depend on shared utilities
- Which tools are used by which projects
- Cross-project dependencies

**Output:** `REPO_INVENTORY.md` (comprehensive, structured, searchable)

---

## 🛠️ Phase 2: Skill Library System

### Task 2.1: Identify Existing Skills

Catalog all existing reusable capabilities:

1. **Infrastructure Skills** (`tools/infra.py`, `infra/`)
   - Vercel deployment management
   - Render deployment management
   - Environment variable management
   - Domain configuration
   - Health checks and diagnostics

2. **Utility Scripts** (`tools/`)
   - `check_vercel_logs.py` - Check Vercel build logs
   - `check_deployment.py` - Deployment status checks
   - `watch_vercel.py` - Real-time Vercel monitoring
   - `check_stripe_setup.py` - Stripe configuration checks
   - `push_to_my_github.py` - Git operations
   - Others...

3. **Project-Specific Utilities**
   - Any reusable patterns from specific projects

### Task 2.2: Create Skill Library Structure

Create `SKILLS_LIBRARY.md` with standardized format for each skill:

```markdown
## Skill Name

**Category:** Infrastructure | Deployment | Monitoring | Utility
**Location:** `tools/script.py` or `infra/module.py`
**Dependencies:** List of requirements

**Purpose:** What problem does this solve?

**Usage:**
```bash
# Command example
python tools/script.py --args
```

**When to Use:** Specific use cases

**Examples:** Real examples from projects

**Related Skills:** Links to related skills
```

### Task 2.3: Create Quick Reference Card

Create `QUICK_REFERENCE.md` with common tasks:

- **Check Vercel Build Logs** → `tools/check_vercel_logs.py` or `python tools/infra.py fix-vercel --project PROJECT`
- **Monitor Deployment** → `python watch_vercel.py` or Vercel Dashboard URL
- **Run Diagnostics** → `python tools/infra.py diag`
- **Deploy Project** → (list commands per project)
- etc.

**Output:**
- `SKILLS_LIBRARY.md` - Complete catalog of reusable skills
- `QUICK_REFERENCE.md` - Common tasks cheat sheet

---

## 🔍 Phase 3: Problem-Solution Registry

### Task 3.1: Extract Solved Problems

Review all documentation and identify problems that were solved:

1. **Common Issues Solved:**
   - Vercel build failures → Solution: Check logs via `check_vercel_logs.py`, common fixes documented
   - Missing environment variables → Solution: Use `tools/infra.py` to set env vars
   - Deployment configuration → Solution: Use infra automation
   - etc.

2. **Pattern: Problem → Solution → Tool/Command**

### Task 3.2: Create Problem-Solution Registry

Create `PROBLEM_SOLUTION_REGISTRY.md`:

```markdown
## Problem: [Short Description]

**Symptoms:** How do you know you have this problem?

**Root Cause:** Why does it happen?

**Solution:** Step-by-step fix

**Command/Tool:** `python tools/fix.py --args`

**Prevention:** How to avoid this in the future

**Last Solved:** Date and context

**Related:** Links to relevant docs/skills
```

### Task 3.3: Index by Problem Type

Organize by categories:
- Deployment Issues (Vercel, Render)
- Configuration Issues (Env vars, domain setup)
- Build Errors
- API/Integration Issues
- etc.

**Output:** `PROBLEM_SOLUTION_REGISTRY.md` - Searchable, categorized problem solutions

---

## 📚 Phase 4: Documentation Consolidation

### Task 4.1: Audit Documentation Files

Analyze all `*.md` files and categorize:

1. **Keep Active (Root Level):**
   - `PROJECT_INVENTORY.md` - Master project list
   - `AUTO_CONTROL_DOCUMENT.md` - Master control doc
   - `REPO_INVENTORY.md` - (new, from Phase 1)
   - `SKILLS_LIBRARY.md` - (new, from Phase 2)
   - `PROBLEM_SOLUTION_REGISTRY.md` - (new, from Phase 3)
   - `QUICK_REFERENCE.md` - (new, from Phase 2)
   - Project-specific `CONTROL.md` files

2. **Archive (Move to `docs/archive/`):**
   - Old summary files (keep most recent, archive rest)
   - Historical status files
   - Completed implementation summaries

3. **Consolidate:**
   - Multiple deployment guides → Single `DEPLOYMENT_GUIDE.md`
   - Multiple status files → Update `PROJECT_INVENTORY.md`
   - Redundant setup docs → Merge into project READMEs

### Task 4.2: Create Documentation Standards

Define in `DOCUMENTATION_STANDARDS.md`:

- **What gets a new file:** Only when creating new knowledge that doesn't fit elsewhere
- **What updates existing files:** Status updates, new features, fixes
- **What gets archived:** Completed milestones, historical summaries
- **Naming conventions:** Consistent naming patterns
- **When to delete:** Truly redundant files (after archiving)

### Task 4.3: Create Master Index

Create `DOCUMENTATION_INDEX.md`:
- Links to all active documentation
- Explanation of what each doc contains
- When to reference each doc

**Output:**
- `docs/archive/` directory with archived files
- Consolidated deployment/setup guides
- `DOCUMENTATION_STANDARDS.md`
- `DOCUMENTATION_INDEX.md`

---

## 🔧 Phase 5: Skill Enhancement System

### Task 5.1: Identify Skill Gaps

From the inventory, identify:
- Problems solved manually that should have a skill
- Repeated workflows that need automation
- Missing utilities for common tasks

### Task 5.2: Create Skill Development Process

Document in `SKILL_DEVELOPMENT.md`:

1. **Before creating new code:**
   - Check `SKILLS_LIBRARY.md` for existing solutions
   - Check `PROBLEM_SOLUTION_REGISTRY.md` for solved problems
   - Consider if existing skill can be extended

2. **When creating new skills:**
   - Follow standardized skill structure
   - Document in `SKILLS_LIBRARY.md`
   - Add examples and usage
   - Link from `QUICK_REFERENCE.md` if commonly used

3. **Skill lifecycle:**
   - New skills go through review
   - Skills are versioned
   - Deprecated skills are marked and alternatives listed

### Task 5.3: Enhance Existing Skills

Based on inventory, improve:
- Make Vercel log checking more discoverable
- Add common tasks to quick reference
- Improve error messages and documentation

**Output:**
- `SKILL_DEVELOPMENT.md` - Process for adding/maintaining skills
- Enhanced existing skills with better docs/discoverability

---

## 📊 Phase 6: Ongoing Maintenance System

### Task 6.1: Create Maintenance Checklist

Create `REPO_MAINTENANCE.md` with regular tasks:

- Weekly: Review new docs, consolidate if needed
- Monthly: Update inventories, archive old summaries
- Quarterly: Full repo audit, skill library review

### Task 6.2: Create Update Process

When making changes:
1. Update relevant inventory/docs immediately
2. If solving a problem, add to Problem-Solution Registry
3. If creating a utility, add to Skills Library
4. Archive old summary files when creating new ones

**Output:** `REPO_MAINTENANCE.md` - Maintenance schedule and processes

---

## ✅ Deliverables Summary

After completing all phases, you should have created:

1. **`REPO_INVENTORY.md`** - Complete repository structure and contents
2. **`SKILLS_LIBRARY.md`** - Catalog of all reusable skills/utilities
3. **`PROBLEM_SOLUTION_REGISTRY.md`** - Solved problems and how to fix them
4. **`QUICK_REFERENCE.md`** - Common tasks cheat sheet
5. **`DOCUMENTATION_INDEX.md`** - Master index of all documentation
6. **`DOCUMENTATION_STANDARDS.md`** - Rules for creating/maintaining docs
7. **`SKILL_DEVELOPMENT.md`** - Process for adding new skills
8. **`REPO_MAINTENANCE.md`** - Ongoing maintenance procedures
9. **`docs/archive/`** - Directory with archived/redundant docs
10. **Consolidated guides** - Merged deployment/setup documentation

---

## 🎯 Success Criteria

The inventory and systems are successful when:

1. ✅ **Any problem solved once is easily found** - Problem-Solution Registry is searchable and complete
2. ✅ **Common tasks take seconds to find** - Quick Reference provides immediate answers
3. ✅ **Skills accumulate, don't duplicate** - New utilities check Skills Library first
4. ✅ **Documentation stays manageable** - Standards prevent sprawl, archive system handles history
5. ✅ **Repository structure is clear** - Inventory shows what exists and where

---

## 🚀 Execution Instructions

**For Otto:**

1. Start with Phase 1 - do a complete inventory before making changes
2. Work through phases sequentially
3. Create files incrementally - start with structure, fill in details
4. Use existing tools to discover capabilities (e.g., run `tools/infra.py --help`)
5. Review existing docs to extract problems/solutions
6. Ask for clarification if structure conflicts with existing patterns

**Timeline:**
- Phase 1: Comprehensive inventory (most important - do thoroughly)
- Phase 2-3: Create library systems (critical for preventing duplication)
- Phase 4: Consolidate docs (cleanup - can be incremental)
- Phase 5-6: Establish processes (for ongoing maintenance)

---

## 📝 Notes

- **Don't delete anything without explicit approval** - Archive instead
- **Respect existing patterns** - Build on what's there, don't reinvent
- **Make it searchable** - Use consistent keywords, clear titles
- **Keep it practical** - Focus on what you actually need, not theoretical organization
- **Update as you go** - When you find gaps or patterns, update the inventories

---

**End of Prompt**

*This prompt establishes the foundation for a maintainable, organized repository where problems are solved once, skills accumulate, and documentation stays manageable.*

