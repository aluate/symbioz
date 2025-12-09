# Skills Library - Reusable Utilities Catalog

**Purpose:** Catalog of all reusable skills, utilities, and tools to prevent code duplication  
**Last Updated:** January 2025

---

## 📋 How to Use This Library

**Before creating new code:**
1. Check this library for existing solutions
2. Check `PROBLEM_SOLUTION_REGISTRY.md` for solved problems
3. Extend existing skills rather than creating new ones
4. Document new skills here when created

---

## 🔧 Infrastructure Skills

### Infrastructure Automation CLI (`tools/infra.py`)

**Category:** Infrastructure | Deployment | Diagnostics  
**Location:** `tools/infra.py`  
**Dependencies:** `infra/` directory, provider configs, environment variables

**Purpose:** Zero-click infrastructure management and diagnostics

**Usage:**
```bash
# Run diagnostics
python tools/infra.py diag --env=prod

# Check specific providers
python tools/infra.py diag --provider vercel --provider render

# Dry-run (safe testing)
python tools/infra.py diag --dry-run

# Provision infrastructure
python tools/infra.py provision-project --spec infra/project-specs/PROJECT.yaml

# Auto-fix Vercel issues
python tools/infra.py fix-vercel --project PROJECT_NAME

# List project templates
python tools/infra.py list-templates

# Generate project from template
python tools/infra.py generate-project --template TEMPLATE --name PROJECT
```

**When to Use:**
- Checking service health across providers
- Provisioning new projects
- Auto-fixing deployment issues
- Managing infrastructure via API

**Examples:**
- Check all services: `python tools/infra.py diag`
- Fix Vercel deployment: `python tools/infra.py fix-vercel --project catered-by-me`
- Create new project: `python tools/infra.py generate-project --template saas-starter --name my-project`

**Documentation:** `infra/README.md`

**Related Skills:** Vercel Client, Render Client, Provider Clients

---

### Vercel Build Log Checker (`tools/check_vercel_logs.py`)

**Category:** Monitoring | Deployment | Debugging  
**Location:** `tools/check_vercel_logs.py`  
**Dependencies:** `infra.providers.vercel_client`, Vercel API token

**Purpose:** Check Vercel deployment logs and build status

**Usage:**
```bash
python tools/check_vercel_logs.py
```

**When to Use:**
- Debugging failed builds
- Checking deployment status
- Reviewing build logs
- **Use this instead of digging for logs!**

**What It Does:**
- Fetches latest deployment
- Shows deployment status
- Displays build logs (last 50 lines)
- Detects errors

**Example Output:**
```
Checking Vercel deployment for: achillies
============================================================
[1/3] Fetching latest deployment for project: achillies
   Deployment ID: dpl_xxx
   URL: https://project.vercel.app
   State: READY
   Ready State: READY

[2/3] Fetching build logs...
Build Logs (last 50 lines):
============================================================
[logs shown here]

[3/3] Checking for errors...
SUCCESS: Deployment successful!
```

**Related Skills:** `infra.py fix-vercel`, Vercel Client, `watch_vercel.py`

---

### Vercel Real-Time Monitor (`watch_vercel.py`)

**Category:** Monitoring | Real-Time  
**Location:** `watch_vercel.py` (root)  
**Dependencies:** Vercel API

**Purpose:** Watch Vercel deployments in real-time

**Usage:**
```bash
python watch_vercel.py
```

**When to Use:**
- Monitoring active deployment
- Waiting for build to complete
- Real-time status updates

**Features:**
- Updates every 5 seconds
- Shows live status
- Stops when deployment completes

**Related Skills:** `check_vercel_logs.py`, `check_deployment.py`

---

### Deployment Status Checker (`check_deployment.py`)

**Category:** Monitoring | Quick Check  
**Location:** `check_deployment.py` (root)  
**Dependencies:** Deployment platform APIs

**Purpose:** Quick terminal check of deployment status

**Usage:**
```bash
python check_deployment.py
```

**When to Use:**
- Quick status check
- See last 5 deployments
- Check without opening browser

**Shows:**
- Last 5 deployments
- Status (✅ READY, 🔨 BUILDING, ❌ ERROR)
- Commit messages
- Timestamps

**Related Skills:** `check_vercel_logs.py`, `watch_vercel.py`

---

### Vercel Settings Checker (`tools/check_vercel_settings.py`)

**Category:** Configuration | Validation  
**Location:** `tools/check_vercel_settings.py`  
**Dependencies:** Vercel API

**Purpose:** Check Vercel project configuration

**Usage:**
```bash
python tools/check_vercel_settings.py
```

**When to Use:**
- Verify project settings
- Check environment variables
- Validate configuration

**Related Skills:** Vercel Client, `infra.py`

---

### Multi-Project Deployment Check (`tools/check_both_deployments.py`)

**Category:** Monitoring | Multi-Project  
**Location:** `tools/check_both_deployments.py`  
**Dependencies:** Multiple deployment platforms

**Purpose:** Check deployments for multiple projects at once

**Usage:**
```bash
python tools/check_both_deployments.py
```

**When to Use:**
- Checking multiple projects
- Quick health check across projects
- Comparing deployment status

**Related Skills:** `check_deployment.py`

---

## 🚀 Deployment Skills

### Auto-Fix Vercel (`tools/infra.py fix-vercel`)

**Category:** Auto-Fix | Deployment  
**Location:** Via `tools/infra.py`  
**Dependencies:** Vercel Client, Fixer system

**Purpose:** Automatically fix Vercel deployment errors

**Usage:**
```bash
python tools/infra.py fix-vercel --project PROJECT_NAME
```

**When to Use:**
- Deployment failed
- Build errors detected
- Configuration issues
- **Instead of manually fixing!**

**What It Does:**
- Detects issues from logs
- Applies fixes automatically
- Redeploys
- Retries until success (with limits)

**Examples:**
- Fix missing env vars
- Fix build configuration
- Retry failed deployments

**Documentation:** `infra/CAN_OTTO_FIX_VERCEL.md`

**Related Skills:** Vercel Client, Vercel Fixer, `check_vercel_logs.py`

---

### Auto-Fix Render (`tools/infra.py fix-render`)

**Category:** Auto-Fix | Deployment  
**Location:** Via `tools/infra.py`  
**Dependencies:** Render Client, Fixer system

**Purpose:** Automatically fix Render service issues

**Usage:**
```bash
python tools/infra.py fix-render --service SERVICE_NAME
```

**When to Use:**
- Service down
- Build failures
- Configuration issues

**Related Skills:** Render Client, Render Fixer

---

## 📦 Git & Repository Skills

### GitHub Push Helper (`tools/push_to_my_github.py`)

**Category:** Git | Automation  
**Location:** `tools/push_to_my_github.py`  
**Dependencies:** Git, GitHub API

**Purpose:** Automate Git push operations

**Usage:**
```bash
python tools/push_to_my_github.py
```

**When to Use:**
- Quick push to GitHub
- Automated commits
- Batch operations

**Related Skills:** Project-specific push scripts

---

### Project-Specific Push Scripts

**Category:** Git | Project-Specific  
**Location:** Various (e.g., `tools/push_corporate_crashout.py`)  
**Dependencies:** Git, project structure

**Purpose:** Push specific projects to GitHub

**Usage:**
```bash
python tools/push_corporate_crashout.py
```

**When to Use:**
- Project-specific workflows
- Custom commit messages
- Project structure requirements

---

## 🔍 Diagnostic Skills

### Full Diagnostics (`tools/infra.py diag`)

**Category:** Diagnostics | Health Check  
**Location:** Via `tools/infra.py`  
**Dependencies:** All provider clients

**Purpose:** Comprehensive health check across all services

**Usage:**
```bash
# All providers
python tools/infra.py diag --env=prod

# Specific providers
python tools/infra.py diag --provider vercel --provider render

# Dry-run
python tools/infra.py diag --dry-run
```

**When to Use:**
- Regular health checks
- Troubleshooting
- Before deployments
- After changes

**Output:**
- Console summary
- `diagnostics/latest.md` - Human-readable report
- `diagnostics/latest.json` - Machine-readable data
- `diagnostics/raw/` - Raw responses (secrets redacted)

**Checks:**
- Render service health
- Vercel deployment status
- Supabase connectivity
- Stripe webhook status
- GitHub CI/CD status

**Documentation:** `infra/README.md`, `infra/MONITORING_GUIDE.md`

**Related Skills:** All provider clients

---

## 🏗️ Project Provisioning Skills

### Provision Infrastructure (`tools/infra.py provision-project`)

**Category:** Provisioning | Infrastructure  
**Location:** Via `tools/infra.py`  
**Dependencies:** Provider clients, project specs

**Purpose:** Automatically provision infrastructure for a project

**Usage:**
```bash
python tools/infra.py provision-project \
  --spec infra/project-specs/PROJECT.yaml \
  --env=prod
```

**When to Use:**
- Setting up new projects
- Updating infrastructure
- Environment setup

**What It Does:**
- Creates/updates Render services
- Sets environment variables
- Configures Supabase
- Creates Stripe resources
- Sets up GitHub

**Examples:**
- New project setup
- Environment provisioning
- Infrastructure updates

**Documentation:** `infra/README.md`

**Related Skills:** Template Generator, Project Specs

---

### Generate Project from Template (`tools/infra.py generate-project`)

**Category:** Scaffolding | Templates  
**Location:** Via `tools/infra.py`  
**Dependencies:** Template generator, templates

**Purpose:** Create new projects from templates

**Usage:**
```bash
python tools/infra.py generate-project \
  --template saas-starter \
  --name my-project \
  --github-repo username/repo \
  --display-name "My Project"
```

**When to Use:**
- Starting new projects
- Consistent project structure
- Quick setup

**Available Templates:**
- `saas-starter` - Full-stack SaaS with payments
- `portfolio-site` - Simple portfolio/landing page
- `booking-leadgen` - Forms + database

**Documentation:** `infra/TEMPLATE_SYSTEM_COMPLETE.md`

**Related Skills:** Template Generator, Project Provisioning

---

### List Templates (`tools/infra.py list-templates`)

**Category:** Discovery | Templates  
**Location:** Via `tools/infra.py`  
**Dependencies:** Template system

**Purpose:** See available project templates

**Usage:**
```bash
python tools/infra.py list-templates
```

**When to Use:**
- Choosing a template
- Discovering options
- Understanding templates

---

## 🛠️ Provider Clients

### Vercel Client

**Category:** Provider | Infrastructure  
**Location:** `infra/providers/vercel_client.py`  
**Dependencies:** Vercel API, httpx

**Purpose:** Vercel API client for deployments and configuration

**Capabilities:**
- List deployments
- Get deployment logs
- Trigger redeployments
- Get project details
- Update settings
- Environment variable management

**Used By:**
- `tools/infra.py`
- `tools/check_vercel_logs.py`
- Vercel Fixer

**Documentation:** `infra/providers/vercel_client.py`

---

### Render Client

**Category:** Provider | Infrastructure  
**Location:** `infra/providers/render_client.py`  
**Dependencies:** Render API, httpx

**Purpose:** Render API client for service management

**Capabilities:**
- Service health checks
- Deployment management
- Environment variables
- Service configuration

**Used By:**
- `tools/infra.py`
- Render Fixer
- Diagnostics

---

### Supabase Client

**Category:** Provider | Database  
**Location:** `infra/providers/supabase_client.py`  
**Dependencies:** Supabase API

**Purpose:** Supabase API client for database operations

**Capabilities:**
- Health checks
- Schema management
- Connection testing

**Used By:**
- Diagnostics
- Project provisioning

---

### Stripe Client

**Category:** Provider | Payments  
**Location:** `infra/providers/stripe_client.py`  
**Dependencies:** Stripe API

**Purpose:** Stripe API client for payment configuration

**Capabilities:**
- Webhook management
- Product creation
- Health checks

**Used By:**
- Diagnostics
- Project provisioning

---

### GitHub Client

**Category:** Provider | Version Control  
**Location:** `infra/providers/github_client.py`  
**Dependencies:** GitHub API, PyGithub

**Purpose:** GitHub API client for repository operations

**Capabilities:**
- Repository checks
- CI/CD status
- Branch management

**Used By:**
- Diagnostics
- Project provisioning

---

## 📝 Otto Skills (`apps/otto/`)

### Repo Lister Skill

**Category:** Analysis | Repository  
**Location:** `apps/otto/otto/skills/repo_lister.py`  
**Dependencies:** Python, file system

**Purpose:** List repository structure and write to Markdown

**Usage:**
```bash
otto run-sample
```

**When to Use:**
- Understanding repo structure
- Documentation
- Auditing

---

### Repo Audit Skill

**Category:** Analysis | Quality  
**Location:** `apps/otto/otto/skills/repo_audit.py`  
**Dependencies:** Python, file system

**Purpose:** Audit Otto repository for issues

**Usage:**
```bash
otto audit
```

**When to Use:**
- Health checks
- Quality assurance
- Finding issues

**Checks:**
- Dead/empty directories
- Very large files
- Missing `__init__.py`
- Skills without self_test

---

## 🔄 Skill Development Process

**Before creating new skills:**

1. **Check this library** - Does something similar exist?
2. **Check Problem-Solution Registry** - Has this been solved?
3. **Consider extending** - Can existing skill be extended?
4. **Standardize** - Follow existing patterns

**When creating new skills:**

1. Document in this library
2. Add to Quick Reference if commonly used
3. Add examples
4. Link related skills
5. Update Problem-Solution Registry if solving a problem

**Skill structure template:**

```markdown
### Skill Name

**Category:** Category | Subcategory
**Location:** `path/to/skill.py`
**Dependencies:** List dependencies

**Purpose:** What problem does this solve?

**Usage:**
```bash
command examples
```

**When to Use:** Specific use cases

**Examples:** Real examples

**Related Skills:** Links to related skills
```

---

## 📚 Related Documentation

- `QUICK_REFERENCE.md` - Common tasks cheat sheet
- `PROBLEM_SOLUTION_REGISTRY.md` - Solved problems
- `infra/README.md` - Infrastructure system docs
- `apps/otto/CONTROL_OTTO.md` - Otto system docs

---

**Last Updated:** January 2025  
**Maintainer:** Add new skills here when created, update when modified


