# Otto Auto-Repair Engine - Next Steps

## Current Status ✅

Otto monitor/repair/redeploy skill is implemented and pushed (commit `a9ed42a`).

**What works:**
- ✅ `GET /capabilities` - Check API token availability
- ✅ `POST /skills/monitor_repair_redeploy` - Full control endpoint
- ✅ `POST /actions/run_deploy_monitor` - Quick start endpoint
- ✅ Provider clients for Vercel, Render, GitHub
- ✅ Monitor loop - checks deployments, fetches logs
- ✅ Commit/push functionality

**What's stubbed:**
- ⚠️ Repair step - Currently writes failure summary to `docs/deploy_failures_latest.md` instead of applying code fixes

## Deploy Otto on Render

### Step 1: Create Render Web Service

1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect GitHub → select repository: `aluate/symbioz`
5. Select branch: `main`

### Step 2: Configure Service

1. **Root Directory:** `apps/otto` (CRITICAL for monorepos!)
2. **Runtime:** Docker (uses `apps/otto/Dockerfile`)
3. **Auto-Deploy:** ON

### Step 3: Set Environment Variables

**Minimum required:**
- `GITHUB_TOKEN` - GitHub personal access token (repo write permissions)
- `VERCEL_TOKEN` - Vercel API token (read deployments + events/logs)
- `RENDER_API_KEY` - Render API key (read deploys + logs)

**Service identifiers (so Otto knows what to watch):**
- `VERCEL_PROJECT_ID` or `VERCEL_PROJECT_NAME` - Which Vercel project to monitor
- `RENDER_SERVICE_ID_OTTO` - Otto's own service ID (for self-monitoring)
- `RENDER_SERVICE_ID_SYMBIOZ` - Other Render services to monitor

### Step 4: Verify Access

```bash
curl https://<otto>.onrender.com/capabilities
```

Expected response:
```json
{
  "github_token": true,
  "vercel_token": true,
  "render_api_key": true
}
```

### Step 5: Trigger Monitor Loop (Safe Mode)

```bash
curl -X POST https://<otto>.onrender.com/actions/run_deploy_monitor \
  -H "Content-Type: application/json" \
  -d '{"mode":"pr","maxIterations":5}'
```

**Current behavior:**
- Monitors Vercel and Render deployments
- Fetches build/deploy logs
- Writes failure summary to `docs/deploy_failures_latest.md`
- Commits and pushes (creates PR in PR mode)
- Loops until both green or max iterations

---

## Next: Implement Real Auto-Repair Engine

### Cursor Prompt for Auto-Repair Implementation

```text
GOAL:

Replace the "stub fix" in apps/otto/otto/skills/monitor_repair_redeploy.py with a real minimal repair engine.

SCOPE:

- Only implement fixes for common, deterministic failure classes:

  1) Vercel root directory / missing package.json / wrong build command

  2) TypeScript compile errors (surface file+line; propose patch only for null/undefined mismatch patterns)

  3) Render Docker build errors: missing files in COPY, wrong workdir, PORT binding, module import error

- Do NOT attempt large refactors or speculative changes.

- Default mode stays PR (never force-push main).

REQUIREMENTS:

1) Log collection must store raw log excerpt + parsed "key error lines"

2) Classification must output: {target, category, confidence, recommended_fix}

3) Implement fix handlers for the categories above that:

   - apply the smallest patch possible

   - explain what changed in the PR body/commit message

4) Safety:

   - If confidence < 0.8, do not patch; instead open PR with the log excerpt + recommended human action

DELIVERABLES:

- Update monitor_repair_redeploy skill to:

  - fetch logs

  - classify

  - if fixable with high confidence: patch + commit/PR + loop

  - else: PR with log excerpt and stop

- Add unit-ish tests for classifiers (lightweight)

- Update docs to explain supported auto-fix classes

COMMIT:

"Otto: implement minimal auto-repair engine for Vercel/Render failures"
```

### Supported Auto-Fix Classes (To Implement)

1. **Vercel Root Directory Issues**
   - Error: "Couldn't find any `pages` or `app` directory"
   - Fix: Verify/update Root Directory setting in Vercel project config

2. **Missing package.json / Build Command**
   - Error: "package.json not found" or "build script not found"
   - Fix: Verify package.json exists, check build command

3. **TypeScript Compile Errors**
   - Error: Type mismatches (null/undefined)
   - Fix: Add null checks or type guards (only for simple patterns)

4. **Render Docker Build Errors**
   - Error: "COPY failed: file not found"
   - Fix: Verify Dockerfile COPY paths relative to build context
   - Error: "Module not found"
   - Fix: Check Python import paths, verify requirements.txt

5. **PORT Binding Issues**
   - Error: "Port already in use" or "Cannot bind to port"
   - Fix: Ensure Dockerfile uses `$PORT` env var

### Safety Rules

- **Confidence threshold:** Only auto-fix if confidence ≥ 0.8
- **PR mode default:** Always create PR for fixes (never force-push main)
- **Minimal patches:** Only change what's necessary to fix the error
- **No refactors:** Do not attempt large code changes or optimizations
- **Human review:** Low-confidence fixes should create PR with log excerpt and recommended action

---

## Current Value (Even with Stub)

Even with the stub repair, Otto provides:

1. **Automated log collection** - No need to manually check Vercel/Render dashboards
2. **Centralized failure tracking** - All failures logged to `docs/deploy_failures_latest.md`
3. **Automated commit/push** - Failures are documented and committed automatically
4. **Loop until green** - Keeps checking until deployments succeed

This gets you **80% of the value** immediately. The remaining 20% is implementing the actual code fixes.

---

## Testing the Current Implementation

After deploying Otto on Render:

1. **Check capabilities:**
   ```bash
   curl https://<otto>.onrender.com/capabilities
   ```

2. **Trigger monitor (will create PR with failure summary):**
   ```bash
   curl -X POST https://<otto>.onrender.com/actions/run_deploy_monitor \
     -H "Content-Type: application/json" \
     -d '{"mode":"pr","maxIterations":2}'
   ```

3. **Check the PR** - Should contain failure summary in `docs/deploy_failures_latest.md`

4. **Review logs** - The summary will include extracted error lines from build logs

---

## Future Enhancements

Once the auto-repair engine is implemented:

- [ ] Support for more failure classes
- [ ] Confidence scoring improvements
- [ ] Local build verification before committing
- [ ] Rollback capability if fix makes things worse
- [ ] Integration with GitHub Actions for CI checks

