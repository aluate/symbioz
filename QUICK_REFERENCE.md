# Quick Reference - Common Tasks Cheat Sheet

**Purpose:** Instant answers for common tasks - no more digging!  
**Last Updated:** January 2025

---

## 🚨 Most Common Tasks

### Check Vercel Build Logs

**Problem:** Need to see why a build failed or check deployment status

**Solution:**
```bash
# Option 1: Use the dedicated script
python tools/check_vercel_logs.py

# Option 2: Use infra.py (more comprehensive)
python tools/infra.py fix-vercel --project PROJECT_NAME

# Option 3: Dashboard (visual)
# Open: https://vercel.com/aluates-projects/PROJECT_NAME
```

**See Also:** `SKILLS_LIBRARY.md` → Vercel Build Log Checker

---

### Monitor Vercel Deployment in Real-Time

**Problem:** Want to watch a deployment as it happens

**Solution:**
```bash
# Real-time monitoring script
python watch_vercel.py

# Or use dashboard
# Open: https://vercel.com/aluates-projects/PROJECT_NAME
```

**See Also:** `SKILLS_LIBRARY.md` → Vercel Real-Time Monitor

---

### Quick Deployment Status Check

**Problem:** Just need a quick status check

**Solution:**
```bash
# Quick terminal check
python check_deployment.py

# Or check specific project
python tools/infra.py diag --provider vercel
```

**See Also:** `SKILLS_LIBRARY.md` → Deployment Status Checker

---

### Fix Vercel Deployment Automatically

**Problem:** Deployment failed and you want Otto to fix it

**Solution:**
```bash
python tools/infra.py fix-vercel --project PROJECT_NAME
```

**What it does:**
- Detects issues from logs
- Applies fixes automatically
- Redeploys
- Retries until success

**See Also:** `SKILLS_LIBRARY.md` → Auto-Fix Vercel, `PROBLEM_SOLUTION_REGISTRY.md`

---

### Run Full Diagnostics

**Problem:** Check health of all services

**Solution:**
```bash
# All providers
python tools/infra.py diag --env=prod

# Specific providers
python tools/infra.py diag --provider vercel --provider render

# Dry-run (safe testing)
python tools/infra.py diag --dry-run
```

**Output:** `diagnostics/latest.md`

**See Also:** `SKILLS_LIBRARY.md` → Full Diagnostics

---

## 🚀 Deployment Tasks

### Deploy to Vercel

**Problem:** Need to deploy or redeploy a project

**Solution:**
```bash
# Push to GitHub (triggers auto-deploy)
git push origin main

# Or manually trigger via infra.py
python tools/infra.py deploy --spec infra/project-specs/PROJECT.yaml
```

**See Also:** Project-specific deployment guides

---

### Configure Vercel Project

**Problem:** Set up a new Vercel project

**Solution:**
```bash
python tools/infra.py setup-vercel-project \
  --project PROJECT_NAME \
  --repo USERNAME/REPO \
  --root-dir apps/PROJECT \
  --framework nextjs
```

**See Also:** `infra/README.md`

---

### Set Up Custom Domain

**Problem:** Configure custom domain on Vercel

**Solution:**
```bash
python tools/infra.py configure-domain \
  --project PROJECT_NAME \
  --domain example.com
```

Then update DNS at your registrar.

**See Also:** `infra/README.md`

---

## 🔧 Infrastructure Tasks

### Provision New Project

**Problem:** Set up infrastructure for a new project

**Solution:**
```bash
# From project spec
python tools/infra.py provision-project \
  --spec infra/project-specs/PROJECT.yaml \
  --env=prod

# Dry-run first!
python tools/infra.py provision-project \
  --spec infra/project-specs/PROJECT.yaml \
  --dry-run
```

**See Also:** `SKILLS_LIBRARY.md` → Provision Infrastructure

---

### Generate Project from Template

**Problem:** Start a new project quickly

**Solution:**
```bash
# List available templates
python tools/infra.py list-templates

# Generate from template
python tools/infra.py generate-project \
  --template saas-starter \
  --name my-project \
  --github-repo username/repo \
  --display-name "My Project"
```

**Available Templates:**
- `saas-starter` - Full-stack SaaS
- `portfolio-site` - Portfolio/landing page
- `booking-leadgen` - Forms + database

**See Also:** `SKILLS_LIBRARY.md` → Generate Project

---

## 📦 Git Tasks

### Push to GitHub

**Problem:** Push code to GitHub

**Solution:**
```bash
# Generic helper
python tools/push_to_my_github.py

# Project-specific
python tools/push_corporate_crashout.py

# Manual
git add .
git commit -m "Message"
git push origin main
```

**See Also:** `SKILLS_LIBRARY.md` → GitHub Push Helper

---

## 🔍 Debugging Tasks

### Check Vercel Settings

**Problem:** Verify Vercel project configuration

**Solution:**
```bash
python tools/check_vercel_settings.py

# Or via infra.py
python tools/infra.py diag --provider vercel
```

**See Also:** `SKILLS_LIBRARY.md` → Vercel Settings Checker

---

### Check Multiple Deployments

**Problem:** Check status of multiple projects

**Solution:**
```bash
python tools/check_both_deployments.py

# Or check specific projects
python tools/infra.py diag --provider vercel
```

**See Also:** `SKILLS_LIBRARY.md` → Multi-Project Check

---

## 📊 Monitoring Tasks

### Vercel Dashboard URLs

**Quick access to projects:**

- Catered By Me: https://vercel.com/aluates-projects/catered-by-me
- Corporate Crashout: https://vercel.com/aluates-projects/corporate-crashout
- Wedding: (check Vercel dashboard)

**What you can do:**
- View real-time build logs
- See deployment history
- Check environment variables
- View preview URLs

---

## 🆘 Common Problems → Quick Fixes

### "Build Failed" on Vercel

1. **Check logs:**
   ```bash
   python tools/check_vercel_logs.py
   ```

2. **Auto-fix:**
   ```bash
   python tools/infra.py fix-vercel --project PROJECT_NAME
   ```

3. **Common fixes:**
   - Missing environment variables
   - Build configuration issues
   - Dependency problems

**See Also:** `PROBLEM_SOLUTION_REGISTRY.md` → Build Failures

---

### "Can't Find Deployment Logs"

**Use:**
```bash
python tools/check_vercel_logs.py
```

**Or dashboard:**
- Open: https://vercel.com/aluates-projects/PROJECT_NAME
- Click on deployment
- View logs tab

**See Also:** This was the original problem! Now solved.

---

### "Service Down" or "Health Check Failed"

1. **Run diagnostics:**
   ```bash
   python tools/infra.py diag
   ```

2. **Check specific provider:**
   ```bash
   python tools/infra.py diag --provider render
   ```

3. **Auto-fix (if supported):**
   ```bash
   python tools/infra.py fix-render --service SERVICE_NAME
   ```

**See Also:** `PROBLEM_SOLUTION_REGISTRY.md`

---

## 📚 Where to Find More

### By Category

**Infrastructure:**
- `SKILLS_LIBRARY.md` → Infrastructure Skills
- `infra/README.md` - Full infrastructure docs

**Deployment:**
- `SKILLS_LIBRARY.md` → Deployment Skills
- Project-specific deployment guides

**Monitoring:**
- `SKILLS_LIBRARY.md` → Diagnostic Skills
- `infra/MONITORING_GUIDE.md`

**Problems:**
- `PROBLEM_SOLUTION_REGISTRY.md` - All solved problems
- This file - Common issues

---

## 🔗 Quick Links

**Documentation:**
- `REPO_INVENTORY.md` - Full repository structure
- `SKILLS_LIBRARY.md` - All utilities catalog
- `PROBLEM_SOLUTION_REGISTRY.md` - Solved problems
- `AUTO_CONTROL_DOCUMENT.md` - AI assistant behavior

**Tools:**
- `tools/infra.py` - Main infrastructure CLI
- `infra/README.md` - Infrastructure system
- `apps/otto/` - Otto SRE bot

**Projects:**
- `PROJECT_INVENTORY.md` - All projects status
- Individual project `CONTROL.md` files

---

## 💡 Tips

1. **Always check this first** - Common tasks are here
2. **Use dry-run** - Test commands with `--dry-run` flag
3. **Check diagnostics** - Run `diag` before making changes
4. **Auto-fix first** - Try `fix-vercel` before manual fixes
5. **Document new problems** - Add to Problem-Solution Registry

---

**Last Updated:** January 2025  
**Add new common tasks here as they're discovered!**


