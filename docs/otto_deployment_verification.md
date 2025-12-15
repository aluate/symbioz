# Otto Deployment Verification Checklist

## ✅ Pre-Deployment Verification (Done)

**Commits verified:**
- `449fb70` - Build context fix + dry-run mode
  - Changed: `apps/otto/otto/api.py`
  - Changed: `apps/otto/otto/skills/monitor_repair_redeploy.py`
  - Changed: `apps/otto/otto/skills/repair_applicators.py`
- `a681455` - Validation report
- `cd531fb` - One-button monitor script

**Dockerfile validated:**
```dockerfile
COPY requirements.txt .        ✅ Correct for Root Directory = apps/otto
COPY otto/ ./otto/            ✅ Correct
COPY otto_config.yaml .       ✅ Correct
CMD uses $PORT                ✅ Correct
```

**Safety features:**
- ✅ Build context awareness (respects `RENDER_ROOT_DIR`)
- ✅ Dry-run mode
- ✅ PR mode default
- ✅ Confidence threshold (≥85%)

---

## 🚀 Post-Deployment Verification (Do This After Deploying Otto)

### Step 1: Deploy Otto on Render

**Render Service Settings:**
- Repo: `aluate/symbioz`
- **Root Directory:** `apps/otto` ⚠️ CRITICAL
- Runtime: **Docker**
- Auto deploy: **ON**

### Step 2: Set Environment Variables

In Render dashboard → Environment tab:

**Required:**
- `RENDER_ROOT_DIR=apps/otto`
- `GITHUB_TOKEN=your_github_token`
- `VERCEL_TOKEN=your_vercel_token`
- `RENDER_API_KEY=your_render_api_key`

**Optional (for testing):**
- `DRY_RUN=true` (set to `false` for live mode)

**Service Identifiers:**
- `VERCEL_PROJECT_ID` or `VERCEL_PROJECT_NAME` (e.g., "symbioz-web")
- `RENDER_SERVICE_ID_OTTO` (Otto's own service ID)
- `RENDER_SERVICE_ID_SYMBIOZ` (if monitoring other services)

### Step 3: Get Your Otto URL

After deployment, Render will provide a URL like:
- `https://otto-xxxxx.onrender.com`

**Save this URL** - you'll need it for the next steps.

### Step 4: Check Capabilities

**Command:**
```bash
curl https://<your-otto-url>.onrender.com/capabilities
```

**Expected Response:**
```json
{
  "github_token": true,
  "vercel_token": true,
  "render_api_key": true
}
```

**What to check:**
- ✅ All three should be `true`
- ❌ If any are `false`, that token is missing in Render env vars

### Step 5: Test with Dry-Run

**Command:**
```bash
curl -X POST https://<your-otto-url>.onrender.com/actions/run_deploy_monitor \
  -H "Content-Type: application/json" \
  -d '{"mode":"pr","maxIterations":2,"dryRun":true}'
```

**What success looks like:**
- Returns status and message
- Shows proposed changes in `data.diff` (if fixes detected)
- Does NOT commit anything
- Shows which files would be changed

### Step 6: Run Live (One-Touch)

**Command:**
```bash
curl -X POST https://<your-otto-url>.onrender.com/actions/run_deploy_monitor \
  -H "Content-Type: application/json" \
  -d '{"mode":"pr","maxIterations":5}'
```

**What success looks like:**
- Creates PR with fixes
- Shows commit message
- Lists files changed
- New deployment triggered automatically

---

## 📋 What Frat Wants to See

**After deploying Otto, provide:**

1. **Otto Render URL:**
   ```
   https://____.onrender.com
   ```

2. **Capabilities Output:**
   ```json
   {
     "github_token": true/false,
     "vercel_token": true/false,
     "render_api_key": true/false
   }
   ```

**Frat will tell you:**
- ✅ Whether tokens are set correctly
- ✅ Whether it's safe to run non-dry mode
- ✅ Whether Render emails will stop after the next loop

---

## 🎯 One-Button Command (Local)

After Otto is deployed, use the helper script:

**From repo root:**
```powershell
.\scripts\run_otto_monitor.ps1
```

**What it does:**
1. Checks Otto capabilities
2. Asks if you want dry-run mode
3. Triggers monitor loop
4. Shows results and PR link

**Prerequisites:**
- Set `$env:OTTO_BASE_URL` or configure `config/otto.json`
- Otto must be deployed and accessible

---

## ⚠️ Important Notes

1. **Root Directory MUST be `apps/otto`** in Render settings
2. **Dockerfile is correct** for this setup (no `apps/otto/` prefix in COPY)
3. **Auto-fix respects `RENDER_ROOT_DIR`** - won't break your setup
4. **Always test with dry-run first** before running live
5. **PR mode is default** - fixes go to branches, not main

---

## 🐛 Troubleshooting

**If capabilities shows `false`:**
- Check Render dashboard → Environment tab
- Verify tokens are set (no typos)
- Redeploy service after adding env vars

**If monitor loop fails:**
- Check Otto service logs in Render dashboard
- Verify service identifiers are set (`VERCEL_PROJECT_ID`, etc.)
- Try dry-run mode first to see what it would do

**If fixes don't work:**
- Check the PR diff to see what changed
- Verify `RENDER_ROOT_DIR=apps/otto` is set
- Check Render build logs for new errors

