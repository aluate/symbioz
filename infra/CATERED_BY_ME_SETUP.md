# Otto - Catered By Me Configuration Summary

**Date:** January 2025  
**Status:** ✅ Configured and Ready for Testing

---

## Overview

Otto has been configured specifically for the **catered-by-me** project. This document summarizes what was configured and what needs to be filled in before running real diagnostics/provisioning.

---

## Project Architecture

**Catered By Me** is a meal planning application with:

- **Frontend:** Next.js 14 app deployed on Vercel
- **Backend:** FastAPI app deployed on Render
- **Database:** Supabase (PostgreSQL + Auth)
- **Payments:** Stripe (TEST mode)
- **Repository:** GitHub (`aluate/catered_by_me`)

---

## Configuration Files Updated

### ✅ Project Spec
- **File:** `infra/project-specs/catered-by-me.yaml`
- **Status:** Updated with real repo path (`aluate/catered_by_me`)
- **Health Checks:** Configured for actual URLs

### ✅ Provider Configs
- **Render:** Template ready, needs service ID
- **Supabase:** Template ready, needs project ref and schema path
- **Stripe:** Template ready, needs webhook ID (TEST mode)
- **GitHub:** Configured with `aluate/catered_by_me`

---

## TODO: Fill In These Values

Before running real diagnostics or provisioning, you need to fill in these placeholders:

### 1. Render Service ID

**File:** `infra/providers/render.yaml`

```yaml
render_service_id: "TODO_FILL_RENDER_SERVICE_ID"
```

**How to get it:**
1. Go to Render dashboard → Your `catered-by-me-api` service
2. Go to Settings
3. Look for "Service ID" or check the URL: `https://dashboard.render.com/web/[SERVICE_ID]`
4. Replace `TODO_FILL_RENDER_SERVICE_ID` with the actual ID (format: `srv-xxxxx`)

### 2. Supabase Project Reference

**File:** `infra/providers/supabase.yaml`

```yaml
project_ref: "TODO_FILL_SUPABASE_PROJECT_REF"
```

**How to get it:**
1. Go to Supabase dashboard → Your project
2. Go to Settings → General
3. Look for "Reference ID" (format: `abcdefghijklmnop`)
4. Replace `TODO_FILL_SUPABASE_PROJECT_REF` with the actual ref

**Note:** Schema file path is already configured: `supabase/schema.sql`

### 3. Stripe Webhook Endpoint ID (TEST Mode)

**File:** `infra/providers/stripe.yaml`

```yaml
webhook_endpoint_id: "TODO_FILL_STRIPE_WEBHOOK_ID"
```

**How to get it:**
1. Go to Stripe dashboard → Developers → Webhooks
2. Make sure you're in **TEST mode** (toggle in top right)
3. Find your webhook endpoint for catered-by-me
4. Copy the endpoint ID (format: `we_xxxxxxxxxxxxx`)
5. Replace `TODO_FILL_STRIPE_WEBHOOK_ID` with the actual ID

**Important:** Otto defaults to Stripe TEST mode for safety. Only use test mode webhook IDs.

---

## Required Environment Variables

Set these in your `.env` file or shell:

### Required for Diagnostics
- `RENDER_API_KEY` - From Render dashboard → Account Settings → API Keys
- `GITHUB_TOKEN` - From GitHub → Settings → Developer Settings → Personal Access Tokens
- `STRIPE_SECRET_KEY` - From Stripe dashboard → Developers → API keys (use **TEST** key!)

### Required for Supabase Checks
- `SUPABASE_URL` - Your Supabase project URL (format: `https://xxxxx.supabase.co`)
- `SUPABASE_SERVICE_KEY` - From Supabase dashboard → Settings → API → service_role key

### Optional (Alternative to above)
- `SUPABASE_ACCESS_TOKEN` - Can use this instead of URL + SERVICE_KEY

### Required for Provisioning/Deployment
- `SUPABASE_JWT_SECRET` - From Supabase dashboard → Settings → API → JWT Secret
- `NEXT_PUBLIC_API_BASE_URL` - Your Render API URL (e.g., `https://catered-by-me.onrender.com`)
- `STRIPE_PUBLISHABLE_KEY` - Stripe publishable key (TEST mode)

---

## Testing Steps (Dry-Run First!)

### Step 1: Verify Configuration

Check that all config files are valid:

```bash
python infra/test_basic.py
```

Should show all ✅ green checks.

### Step 2: Dry-Run Diagnostics

**Safe to run - no API calls:**

```bash
python tools/infra.py diag --env=prod --dry-run
```

This will:
- Validate all configs
- Show what would be checked
- Not make any real API calls
- Generate example reports in `diagnostics/`

**Check the output:**
- Should see `[DRY RUN]` messages
- `diagnostics/latest.md` should be generated
- No errors about missing configs

### Step 3: Fill In Real IDs

After dry-run looks good, fill in the TODO placeholders:
- Render service ID
- Supabase project ref
- Stripe webhook ID

### Step 4: Real Diagnostics (Safe)

Once IDs are filled in:

```bash
python tools/infra.py diag --env=prod
```

This will:
- Check real service status
- Generate actual diagnostic reports
- Show health of all services

### Step 5: Dry-Run Provisioning

**Safe to run - shows what would be created:**

```bash
python tools/infra.py provision-project \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod \
  --dry-run
```

Review the output to ensure it would:
- Create/update the right services
- Set the correct environment variables
- Apply the Supabase schema correctly

### Step 6: Dry-Run Deployment

**Safe to run - shows what would be deployed:**

```bash
python tools/infra.py deploy \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod \
  --dry-run
```

---

## Real Run (Only After Dry-Run Looks Good!)

Once all dry-run commands succeed and output looks correct:

### Real Diagnostics
```bash
python tools/infra.py diag --env=prod
```

### Real Provisioning (Creates/Updates Services)
```bash
python tools/infra.py provision-project \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod
```

### Real Deployment (Triggers Deployments)
```bash
python tools/infra.py deploy \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod
```

---

## Current Configuration Status

### ✅ Complete
- Project spec configured with real repo path
- GitHub config with correct repo
- Provider config templates ready
- Environment variable mappings correct
- Health check URLs configured

### ⏳ Needs Real Values
- Render service ID (placeholder in config)
- Supabase project ref (placeholder in config)
- Stripe webhook ID (placeholder in config)

### ⏳ Needs Environment Variables
- API keys and tokens (set in `.env` or shell)

---

## Safety Features

Otto has built-in safety features:

- ✅ **Dry-run mode** - Test everything without changes
- ✅ **Secret redaction** - No secrets in logs or reports
- ✅ **Test mode default** - Stripe defaults to test mode
- ✅ **Non-destructive** - Won't delete databases or services
- ✅ **Idempotent** - Safe to run multiple times

---

## Next Steps

1. ✅ Configuration files updated
2. ⏳ Fill in TODO placeholders (Render ID, Supabase ref, Stripe webhook)
3. ⏳ Set environment variables
4. ⏳ Run dry-run tests
5. ⏳ Review dry-run output
6. ⏳ Run real diagnostics
7. ⏳ (Optional) Run real provisioning/deployment

---

**Ready to test! Start with dry-run mode to verify everything works.**

