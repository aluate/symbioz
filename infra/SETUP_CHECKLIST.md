# Otto Setup Checklist - Catered By Me

**Follow this checklist step-by-step to get Otto working for catered-by-me.**

---

## Step 1: Install Dependencies ✅ (I can guide you)

**Action Required:** Install Python packages

```bash
pip install -r infra/requirements.txt
```

**What this installs:**
- CLI framework (click)
- YAML parser (pyyaml)
- HTTP client (httpx)
- Provider SDKs (stripe, supabase, PyGithub, etc.)

**I can help with:** Troubleshooting installation issues

---

## Step 2: Set Environment Variables ⚠️ (You must do this)

**Action Required:** Create `.env` file with your API keys

**I can help with:**
- ✅ Creating `.env.example` template (done!)
- ✅ Showing you exactly which variables are needed
- ❌ I cannot access your dashboards to get the actual keys

**What you need to do:**

1. Copy `infra/.env.example` to `.env` in repo root:
   ```bash
   cp infra/.env.example .env
   ```

2. Fill in your actual values in `.env`:
   - `RENDER_API_KEY` - From Render dashboard
   - `GITHUB_TOKEN` - From GitHub settings
   - `STRIPE_SECRET_KEY` - From Stripe dashboard (TEST mode!)
   - `SUPABASE_URL` - From Supabase dashboard
   - `SUPABASE_SERVICE_KEY` - From Supabase dashboard

3. Verify `.env` is in `.gitignore` (it should be)

**I can help you find:** Instructions on where to get each key (see below)

---

## Step 3: Fill In TODO Placeholders ⚠️ (You must do this)

**Action Required:** Edit YAML config files and replace TODO placeholders with real IDs

**I can help with:**
- ✅ Showing you exactly which files to edit
- ✅ Creating templates with clear placeholders
- ✅ Validating the config format after you fill them in
- ❌ I cannot access your dashboards to get the actual IDs

### 3.1 Render Service ID

**File:** `infra/providers/render.yaml`

**What you need:**
- Render service ID (format: `srv-xxxxx`)

**I can help:**
- ✅ Show you the exact line to edit
- ✅ Validate the format once you fill it in
- ❌ Cannot access Render dashboard to get the ID

**How to get it (from Frat's guide):**
1. Go to Render dashboard → Your `catered-by-me-api` service
2. Check the URL or Settings page
3. Look for "Service ID" (format: `srv-xxxxx`)

### 3.2 Supabase Project Reference

**File:** `infra/providers/supabase.yaml`

**What you need:**
- Supabase project ref (short ID from your Supabase URL)

**I can help:**
- ✅ Show you the exact line to edit
- ✅ Validate the format once you fill it in
- ❌ Cannot access Supabase dashboard to get the ref

**How to get it:**
- It's in your Supabase project URL: `https://xxxxx.supabase.co` (the `xxxxx` part)

### 3.3 Stripe Webhook ID

**File:** `infra/providers/stripe.yaml`

**What you need:**
- Stripe webhook endpoint ID (format: `we_xxxxx`) - TEST mode only!

**I can help:**
- ✅ Show you the exact line to edit
- ✅ Validate the format once you fill it in
- ❌ Cannot access Stripe dashboard to get the ID

**How to get it:**
- Stripe dashboard → Developers → Webhooks → Endpoint ID (TEST mode)

---

## Step 4: Dry-Run Tests ✅ (I can run these!)

**Action Required:** Run dry-run commands to test Otto

**I can do:**
- ✅ Run the CLI help command
- ✅ Run dry-run diagnostics (if dependencies installed)
- ✅ Run dry-run provisioning
- ✅ Run dry-run deployment
- ✅ Validate configuration files
- ✅ Check for syntax errors in configs

**Commands I can test:**

```bash
# CLI help
python tools/infra.py --help

# Dry-run diagnostics
python tools/infra.py diag --env=prod --dry-run

# Dry-run provisioning
python tools/infra.py provision-project --spec infra/project-specs/catered-by-me.yaml --env=prod --dry-run

# Dry-run deployment
python tools/infra.py deploy --spec infra/project-specs/catered-by-me.yaml --env=prod --dry-run
```

**What I'll check:**
- ✅ Commands execute without errors
- ✅ Reports are generated
- ✅ No secrets are exposed
- ✅ Config validation works

---

## Step 5: Real Diagnostics ⚠️ (Needs your API keys)

**Action Required:** Run real diagnostics (read-only, safe)

**I can do:**
- ✅ Run the command for you (if you provide API keys)
- ✅ Review the generated reports
- ✅ Help interpret results
- ❌ I cannot provide your API keys

**This is safe to run** - it only reads status, doesn't make changes.

---

## Step 6: Real Provisioning/Deployment ⚠️ (Needs your approval)

**Action Required:** Let Otto actually create/update infrastructure

**I can:**
- ✅ Run the commands when you're ready
- ✅ Monitor the output
- ✅ Help troubleshoot issues
- ❌ I will NOT run these without your explicit approval

**These commands make real changes:**
- Create/update Render services
- Set environment variables
- Apply database schemas
- Trigger deployments

---

## What I Can Do Right Now

### ✅ Immediate Actions (No Secrets Needed)

1. **Validate configuration files**
   - Check YAML syntax
   - Validate structure
   - Check for missing required fields

2. **Create helper templates**
   - `.env.example` file (done!)
   - Setup checklist (this file!)
   - Configuration guides

3. **Test dry-run mode** (if dependencies installed)
   - CLI structure
   - Config loading
   - Dry-run execution

4. **Create detailed guides**
   - Where to find each API key
   - Where to find each ID
   - Step-by-step instructions

### ⚠️ Requires Your Action

1. **Install dependencies** - You need to run `pip install`
2. **Set environment variables** - You need to add your actual keys
3. **Fill in TODO placeholders** - You need to get IDs from dashboards
4. **Approve real operations** - You need to confirm before provisioning/deploying

---

## Let's Start!

I can help you right now with:

1. ✅ Creating detailed guides for finding each API key/ID
2. ✅ Validating configuration files
3. ✅ Testing dry-run mode (if you install dependencies first)
4. ✅ Creating helper scripts/checklists

**What would you like me to do first?**

- Create detailed guides for finding each key/ID?
- Test the configuration files for errors?
- Create a PowerShell script to set env vars?
- Something else?

