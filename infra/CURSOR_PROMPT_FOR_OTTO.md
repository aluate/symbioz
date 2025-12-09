# 🎯 Cursor Prompt: Finish & Polish Otto for Real-World Use

**Purpose:** This prompt guides Cursor to finish Otto, validate it works, and prepare it for building real projects (not just catered-by-me).

---

## CONTEXT

You're working on **Otto**, an automation engine that:
- Provisions infrastructure (Render, Vercel, Supabase, Stripe)
- Deploys applications automatically
- Handles environment variables
- Fixes deployment errors
- Validates everything is working

Otto lives in `tools/infra.py` with configs in `infra/`.

**Current Status:**
- ✅ Core automation working for catered-by-me
- ✅ Stripe integration complete
- ✅ Deployment automation working
- ⚠️ Need to make it more robust for multiple projects
- ⚠️ Need better error handling and user feedback
- ⚠️ Need to document template patterns

---

## YOUR GOALS

### Goal 1: Make Otto Bulletproof for Catered-By-Me

1. **Verify all commands work end-to-end:**
   ```bash
   python tools/infra.py diag --env prod
   python tools/infra.py setup-stripe --project catered-by-me
   python tools/infra.py validate-launch --project catered-by-me
   python tools/infra.py finish-site --project catered-by-me
   ```

2. **Fix any remaining issues:**
   - Render API response handling (already fixed)
   - Stripe webhook config validation
   - Error messages clarity
   - Documentation completeness

3. **Test the full flow:**
   - New project from scratch
   - Existing project updates
   - Error recovery
   - Multi-provider scenarios

---

### Goal 2: Make Otto Reusable for Multiple Projects

1. **Template System:**
   - Document template structure in `infra/templates/README.md`
   - Create at least 2 template examples:
     - `templates/saas-starter/` — Next.js + FastAPI + Supabase + Stripe
     - `templates/portfolio/` — Simple Next.js site
   - Each template should have:
     - `template.yaml` — Template metadata
     - `project-spec.yaml` — Default project spec
     - `README.md` — What it includes
     - Optional: starter code snippets

2. **Project Spec Generation:**
   - Add command: `python tools/infra.py generate-spec --template saas-starter --name my-project`
   - This creates a new `infra/project-specs/my-project.yaml` from template
   - User can then customize it
   - Then run: `python tools/infra.py provision-project --spec infra/project-specs/my-project.yaml`

3. **Better Error Messages:**
   - When something fails, tell user EXACTLY what to do
   - Include links to dashboards if needed
   - Suggest alternative approaches
   - Make it actionable, not just "error occurred"

---

### Goal 3: Documentation & Maintainability

1. **Update `infra/README.md`:**
   - Quick start guide
   - Common workflows
   - Troubleshooting section
   - Examples for each command

2. **Create `infra/TEMPLATES.md`:**
   - How to create a template
   - Template structure
   - How to use templates
   - Examples

3. **Create `infra/TROUBLESHOOTING.md`:**
   - Common errors and fixes
   - How to debug provider issues
   - How to reset/clean up
   - When to use dry-run mode

4. **Update `infra/CONTROL.md`:**
   - Reflect current state
   - Add lessons learned
   - Document any changes to original plan

---

### Goal 4: Add Safety & Validation

1. **Pre-flight Checks:**
   - Before provisioning, validate:
     - All required env vars are set
     - Provider credentials work
     - Project spec is valid
     - No conflicts with existing resources
   - Fail fast with clear messages

2. **Dry-Run by Default:**
   - Make `--dry-run` the default for destructive operations
   - Require explicit `--yes` flag to make real changes
   - Show exactly what will happen

3. **Rollback Capability:**
   - For deployments, keep track of previous version
   - Add command: `python tools/infra.py rollback --project X --deployment Y`
   - Document how to manually rollback if needed

---

## WORKFLOW

1. **Read First:**
   - `infra/CONTROL.md`
   - `infra/README.md`
   - `WHAT_NEEDS_TO_BE_DONE.md`
   - `AUTOMATION_PLAN.md`

2. **Test Current State:**
   - Run diagnostics
   - Test each command
   - Document what works and what doesn't

3. **Fix Issues:**
   - Prioritize: crashes > unclear errors > missing features
   - Make changes incrementally
   - Test after each change

4. **Document:**
   - Update docs as you go
   - Add examples
   - Explain why, not just what

---

## CONSTRAINTS

- **Never break existing functionality** — Test before changing
- **Never expose secrets** — Always redact in logs
- **Never make destructive changes without confirmation** — Use dry-run
- **Always update docs** — If you change something, document it
- **Keep commands backwards compatible** — Add flags, don't remove options

---

## SUCCESS CRITERIA

After your work, a user should be able to:

1. ✅ Run `python tools/infra.py diag --env prod` and get clear status
2. ✅ Run `python tools/infra.py setup-stripe --project X` and have Stripe configured
3. ✅ Run `python tools/infra.py finish-site --project X` and have site ready
4. ✅ Use Otto on a NEW project with minimal config changes
5. ✅ Understand what went wrong if something fails
6. ✅ Find documentation for common tasks

---

## PRIORITY ORDER

1. **Fix any bugs** in existing commands (catered-by-me)
2. **Add template system** so Otto can handle multiple projects
3. **Improve error messages** so failures are actionable
4. **Document everything** so future work is easier
5. **Add safety features** so mistakes are recoverable

---

**Remember:** You're making Otto ready for REAL projects, not just catered-by-me. Focus on robustness, clarity, and reusability.

