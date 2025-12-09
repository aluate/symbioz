# 🚀 Deploy Corporate Crashout - Instructions

## Quick Deploy (Choose One Method)

### Method 1: Run PowerShell Script (Easiest)
```powershell
cd "g:\My Drive"
.\DEPLOY_CORPORATE_CRASHOUT_NOW.ps1
```

### Method 2: Run Python Script Directly
```powershell
cd "g:\My Drive"
python tools/deploy_corporate_crashout.py
```

### Method 3: Use Otto's Fix Command
```powershell
cd "g:\My Drive"
python tools/infra.py fix-vercel --project achillies --env prod
```

### Method 4: Test First (Recommended)
```powershell
cd "g:\My Drive"
python tools/test_deploy.py
```

## What the Script Does

1. ✅ Checks if VERCEL_TOKEN is set
2. ✅ Loads project configuration
3. ✅ Connects to Vercel API
4. ✅ Checks current root directory
5. ✅ **Fixes root directory if wrong** (sets to `apps/corporate-crashout`)
6. ✅ Checks latest deployment status
7. ✅ Reports what needs to be done

## Prerequisites

Make sure you have:
- ✅ `VERCEL_TOKEN` in your `.env` file
  - Get it from: https://vercel.com/account/tokens
- ✅ Project `achillies` exists in Vercel
  - If not, create it at: https://vercel.com/new
  - Import repo: `elikjwilliams/CorporateCrashoutTrading`

## Expected Output

You should see:
```
============================================================
🔧 Loading configuration...
============================================================
✅ achillies project found in config
   Root directory: apps/corporate-crashout

============================================================
🔧 Step 1: Verifying root directory configuration...
============================================================
   Current root directory: (not set)
   Expected root directory: apps/corporate-crashout
⚠️  Root directory is incorrect - fixing now...
✅ Root directory updated to: apps/corporate-crashout
```

## After Running

1. **Check Vercel Dashboard:**
   - Go to: https://vercel.com/dashboard
   - Project: `achillies`
   - Settings → General → Verify root directory is `apps/corporate-crashout`

2. **Check Site:**
   - Visit: https://achillies.vercel.app
   - Should see Corporate Crashout homepage (not 404)

3. **If Still 404:**
   - Wait 5-10 minutes for changes to propagate
   - Or trigger a new deployment in Vercel dashboard
   - Or push a small change to GitHub to trigger auto-deploy

## Troubleshooting

### "VERCEL_TOKEN not set"
- Add `VERCEL_TOKEN=your_token_here` to `.env` file
- Get token from: https://vercel.com/account/tokens

### "Project not found"
- Create project in Vercel dashboard
- Or the project name might be different - check `infra/providers/vercel.yaml`

### "Permission denied"
- Make sure you have write access to the Vercel project
- Check your Vercel token has the right permissions

---

**Ready?** Run one of the methods above! 🚀
