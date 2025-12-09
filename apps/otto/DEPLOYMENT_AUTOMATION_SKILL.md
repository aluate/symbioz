# Deployment Automation Skill for Otto

**Created:** January 2025  
**Status:** ✅ Complete

## Overview

Otto now has a **DeploymentAutomationSkill** that fully automates the deployment workflow for Catered By Me (or any project):

1. ✅ **Push commits** to GitHub automatically
2. ✅ **Monitor Render build** status until completion
3. ✅ **Monitor Vercel build** status until completion
4. ✅ **Auto-fix errors** (environment variables, config issues)
5. ✅ **Commit and push fixes** automatically
6. ✅ **Repeat until successful** (up to 5 iterations by default)

## What It Does

The skill orchestrates the entire deployment process:

```
1. Check git status → Push any unpushed commits
2. Wait for deployments to start
3. Monitor Render build (poll every 10s, timeout 10min)
4. Monitor Vercel build (poll every 10s, timeout 10min)
5. If both succeed → ✅ Done!
6. If either fails → Auto-fix issues → Commit fixes → Push → Loop back to step 1
```

## Usage

### Via Otto Task

When Otto is running, you can ask:

- **"Deploy catered by me and fix any errors"**
- **"Sync catered by me to live"**
- **"Push and monitor deployment for catered by me"**

Otto will handle task types:
- `deployment.deploy_and_fix`
- `deployment.sync_to_live`
- `deployment.push_and_monitor`
- `catered_by_me.deploy`

### Task Payload Options

```python
{
    "project_path": "catered_by_me",  # Path to project (default: "catered_by_me")
    "project_name": "catered-by-me",   # Project name in configs (default: "catered-by-me")
    "max_iterations": 5                # Max retry attempts (default: 5)
}
```

## How It Works

### Step 1: Push Commits

- Checks if local repo is ahead of GitHub
- Commits any uncommitted changes
- Pushes to `origin/main`
- Waits for deployments to trigger

### Step 2: Monitor Render Build

- Polls Render API every 10 seconds
- Checks deployment status:
  - ✅ `live` = Success
  - ❌ `build_failed` = Failure (gets error logs)
  - ⏳ Other statuses = Still building
- Timeout: 10 minutes

### Step 3: Monitor Vercel Build

- Polls Vercel API every 10 seconds
- Checks deployment state:
  - ✅ `READY` = Success
  - ❌ `ERROR` or `CANCELED` = Failure (gets error logs)
  - ⏳ Other states = Still building
- Timeout: 10 minutes

### Step 4: Auto-Fix Issues

**Render Fixes:**
- Detects failed deployments
- Uses `RenderFixer` to identify issues
- Applies fixes (env vars, config)
- Triggers redeploy

**Vercel Fixes:**
- Detects build errors from logs
- Uses `VercelFixer` to identify issues
- Applies fixes (missing env vars)
- Triggers redeploy

**Code Fixes:**
- If fixes require code changes, commits them
- Pushes fixes and loops back

### Step 5: Success or Failure

**Success:** Both Render and Vercel deployments succeed
- Returns success with deployment details

**Failure:** After max iterations or unfixable errors
- Returns failure with detailed error information
- Reports what needs manual attention

## Example Output

```
✅ Deployment successful after 2 iteration(s)!

Results:
- Iteration 1 - Git: pushed (Pushed 2 commit(s) to GitHub)
- Iteration 1 - Render: live (Render deployment successful)
- Iteration 1 - Vercel: failed (Vercel deployment error)
- Iteration 1 - Fixes: Set environment variable: NEXT_PUBLIC_API_BASE_URL, Triggered Vercel redeploy
- Iteration 2 - Git: pushed (Pushed 1 commit(s) to GitHub)
- Iteration 2 - Render: live (Render deployment successful)
- Iteration 2 - Vercel: ready (Vercel deployment successful)
```

## Requirements

### API Keys (Already Configured ✅)

All required keys are in your `.env` file:
- ✅ `VERCEL_TOKEN` - For Vercel API
- ✅ `RENDER_API_KEY` - For Render API
- ✅ `GITHUB_TOKEN` - For git operations (optional, uses local git)

### Project Configuration

The skill uses existing configs:
- `infra/providers/vercel.yaml` - Vercel project configs
- `infra/providers/render.yaml` - Render service configs

For `catered-by-me`:
- Vercel project: `catered-by-me`
- Render service: `catered-by-me-api`

## What Can Be Auto-Fixed

### ✅ Automatically Fixable

- **Missing environment variables** - Sets them via API
- **Configuration issues** - Updates via API
- **Failed deployments** - Triggers redeploy
- **Uncommitted changes** - Commits and pushes
- **TypeScript/build errors** - **NEW!** Auto-fixes common TypeScript errors:
  - Missing imports (adds import statements)
  - Type errors in API calls (fixes return types)
  - Missing 'use client' directives (adds to client components)
  - Dynamic rendering issues (adds `export const dynamic = 'force-dynamic'`)

### ⚠️ Partially Auto-Fixable

- **Parameter order issues** - Complex, may require manual fix
- **Complex type errors** - Some can be fixed, others need context

### ❌ Requires Manual Fix

- **Missing dependencies** - Need package.json updates
- **Code logic errors** - Need developer understanding
- **Complex refactoring** - Beyond simple pattern matching

See `TYPESCRIPT_AUTO_FIX.md` for full details on TypeScript error fixing.

## Limitations

1. **Code-level errors** - Cannot automatically fix TypeScript errors, missing imports, etc.
2. **Max iterations** - Default 5, can be configured
3. **Timeout** - 10 minutes per build monitoring (configurable)
4. **Git operations** - Requires git to be configured and accessible

## Integration with Existing Tools

This skill uses:
- ✅ `VercelClient` - For Vercel API operations
- ✅ `RenderClient` - For Render API operations
- ✅ `VercelFixer` - For Vercel auto-fixing
- ✅ `RenderFixer` - For Render auto-fixing

**No duplicate code!** It leverages existing infrastructure.

## Next Steps

1. **Test the skill** by asking Otto to deploy catered by me
2. **Monitor the output** to see what it detects and fixes
3. **Extend if needed** - Add more auto-fix capabilities for code-level errors

---

**Ready to use!** Just ask Otto to deploy and it will handle the entire workflow automatically! 🚀

