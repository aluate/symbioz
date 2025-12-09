# 🚀 Deploy Mellivox with Otto

**Status:** ✅ Ready to use!

---

## Quick Start

Just run:

```bash
python deploy_symbioz.py
```

Otto will:
1. ✅ Push any uncommitted changes to GitHub
2. ✅ Monitor Render build (backend API)
3. ✅ Monitor Vercel build (frontend)
4. ✅ Auto-fix common errors
5. ✅ Commit and push fixes automatically
6. ✅ Repeat until successful (up to 5 iterations)

---

## Prerequisites

### 1. Render Service ID

**If you already have the Render service set up:**

1. Go to your Render dashboard
2. Click on your `symbioz-api` or `mellivox-api` service
3. Copy the service ID from the URL (looks like `srv-xxxxx`)
4. Update `infra/providers/render.yaml`:
   ```yaml
   symbioz-api:
     render_service_id: "srv-YOUR_ACTUAL_SERVICE_ID"  # Replace this
   ```

**If you don't have the Render service yet:**

Otto can't create it automatically, but you can:
1. Create it manually via Render dashboard (one-time setup)
2. Or use `python tools/infra.py provision-project --spec infra/project-specs/symbioz.yaml`

### 2. Vercel Project

**If you already have the Vercel project:**

The config in `infra/providers/vercel.yaml` should work. If your project is named differently (e.g., "mellivox" instead of "symbioz"), update the `project_id` in the config.

**If you don't have the Vercel project yet:**

Otto can create it! But first, make sure:
- Your code is in GitHub repo: `aluate/symbioz`
- You have `VERCEL_TOKEN` in your `.env` file

Then Otto's deployment automation will handle the rest.

### 3. Environment Variables

**Vercel needs:**
- `NEXT_PUBLIC_API_URL` - Your Render API URL (e.g., `https://symbioz-api.onrender.com`)

**Render needs:**
- `ALLOWED_ORIGINS` - Your Vercel URL + domain (e.g., `https://symbioz-xyz.vercel.app,https://*.vercel.app,https://mellivox.com,https://www.mellivox.com`)

Otto will try to set these automatically, but you may need to set them manually the first time.

---

## What Otto Does

### Step 1: Git Operations
- Checks for uncommitted changes
- Commits any changes
- Pushes to `origin/main`
- Handles secrets in commit history (auto-cleans if needed)

### Step 2: Monitor Deployments
- Triggers Render deployment (if service exists)
- Monitors Render build status (polls every 10s)
- Monitors Vercel build status (polls every 10s)
- Timeout: 10 minutes per service

### Step 3: Auto-Fix Issues
- **Render errors**: Detects and fixes common issues (env vars, config)
- **Vercel errors**: Detects and fixes build errors (missing env vars, TypeScript errors)
- **Code errors**: Auto-fixes common TypeScript issues (missing imports, type errors)

### Step 4: Commit & Retry
- Commits any fixes
- Pushes fixes to GitHub
- Triggers new deployments
- Repeats up to 5 times

---

## Example Output

```
🚀 Asking Otto to deploy Symbioz/Mellivox and fix any errors...

📋 Task: deployment.deploy_and_fix
   Project: symbioz
   Max iterations: 5

⏳ Running deployment automation...

============================================================
✅ SUCCESS: ✅ Vercel deployment successful after 2 iteration(s)!

   Completed in 2 iteration(s)

   Iteration Summary:
   - Iteration 1 - Git: pushed (Pushed 1 commit(s) to GitHub)
   - Iteration 1 - Render: live (Render deployment successful)
   - Iteration 1 - Vercel: failed (Vercel deployment error)
   - Iteration 1 - Fixes: Set environment variable: NEXT_PUBLIC_API_URL, Triggered Vercel redeploy
   - Iteration 2 - Git: pushed (Pushed 1 commit(s) to GitHub)
   - Iteration 2 - Render: live (Render deployment successful)
   - Iteration 2 - Vercel: ready (Vercel deployment successful)

   Render: live
   Vercel: ready
   URL: https://symbioz-xyz.vercel.app
============================================================
```

---

## Troubleshooting

### "Service not found in config"
- Make sure `symbioz-api` is in `infra/providers/render.yaml`
- Make sure `render_service_id` is set (not `REPLACE_WITH_ACTUAL_SERVICE_ID`)

### "Project not found in config"
- Make sure `symbioz` is in `infra/providers/vercel.yaml`
- Check that `project_id` matches your actual Vercel project name

### "Git push blocked by secrets"
- Otto will try to clean secrets automatically
- If it fails, you may need to manually clean git history
- See `clean_git_secrets.py` for help

### "Deployment failed after 5 iterations"
- Check the error messages in the output
- Some errors may require manual fixes
- Check Render/Vercel dashboards for detailed logs

---

## Manual Steps (If Needed)

If Otto can't auto-fix everything, you may need to:

1. **Set environment variables manually:**
   - Vercel: Settings → Environment Variables
   - Render: Environment tab

2. **Check deployment logs:**
   - Vercel: Deployments → Click deployment → View logs
   - Render: Deployments → Click deployment → View logs

3. **Fix code issues:**
   - Some TypeScript errors may need manual fixes
   - Check the error logs for specific issues

---

## Next Steps After Deployment

1. **Configure domain** (optional):
   - Add `mellivox.com` to Vercel
   - Update DNS records
   - Update Render `ALLOWED_ORIGINS` to include domain

2. **Test the game:**
   - Visit your Vercel URL
   - Test character creation
   - Test game flow
   - Check browser console for errors

---

**Ready to deploy?** Just run `python deploy_symbioz.py` and Otto will handle the rest! 🚀

