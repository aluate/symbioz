# 🚀 CORPORATE CRASH OUT TRADING - GET UNSTUCK GUIDE

**Created:** December 2024  
**Status:** Action plan to get live

---

## 🎯 CURRENT SITUATION

Based on the deployment status documents:

✅ **What's Working:**
- Build succeeds on Vercel
- Preview URLs work (`https://achillies-xxx.vercel.app`)
- Root directory is correctly set to `apps/corporate-crashout`

❌ **What's Blocking:**
- Production domain returns 404 (`https://achillies.vercel.app`)
- Code may not be fully synced to GitHub
- Production deployment may not be promoted

---

## 📋 STEP-BY-STEP ACTION PLAN

### STEP 1: Verify & Push Code to GitHub

**Check if code is on GitHub:**
1. Visit: https://github.com/elikjwilliams/CorporateCrashoutTrading
2. Do you see the `apps/corporate-crashout/` folder?
3. If YES → Skip to Step 2
4. If NO → Push code:

```powershell
cd "E:\My Drive"

# Use the push script (recommended)
python tools/push_corporate_crashout.py https://github.com/elikjwilliams/CorporateCrashoutTrading.git

# OR manually:
cd "E:\My Drive\apps\corporate-crashout"
git init
git remote add origin https://github.com/elikjwilliams/CorporateCrashoutTrading.git
git add .
git commit -m "Corporate Crashout Trading - ready for deployment"
git branch -M main
git push -u origin main
```

---

### STEP 2: Fix Vercel Production Domain 404

**The issue:** Builds succeed but production domain returns 404

**Solution:**

1. **Go to Vercel Dashboard:**
   - Visit: https://vercel.com/dashboard
   - Find project: `achillies`

2. **Check Latest Deployment:**
   - Go to **Deployments** tab
   - Find the latest deployment (should show green checkmark)
   - **IMPORTANT:** Check if it says "Production" or "Preview"
   - If it says "Preview", click the "..." menu → **Promote to Production**

3. **Verify Root Directory:**
   - Go to **Settings** → **General**
   - Check **Root Directory** is: `apps/corporate-crashout` (exactly, no trailing slash)
   - If wrong, click "Edit", set it, click "Save"

4. **Check Domain Assignment:**
   - Go to **Settings** → **Domains**
   - Verify `achillies.vercel.app` is listed
   - If not listed, Vercel should auto-assign it, but you can manually add it
   - Wait 5-10 minutes after any changes

5. **Trigger Fresh Deployment (if needed):**
   - Go to **Deployments** tab
   - Click "..." on latest deployment → **Redeploy**
   - OR if connected to GitHub, just push a commit (even a small one)

---

### STEP 3: Verify Environment Variables

**Go to:** Settings → Environment Variables

**Minimum Required:**
```
NEXTAUTH_SECRET=<random-32-char-string>
NEXTAUTH_URL=https://achillies.vercel.app
```

**For Full Functionality:**
```
DATABASE_URL=postgresql://...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
(etc.)
```

**Important:** Make sure env vars are set for **Production** environment, not just Preview!

---

### STEP 4: Test the Site

**Test Preview URL First:**
- Should work: `https://achillies-xxx-aluates-projects.vercel.app`
- Test: `/api/health` should return `{"status":"ok"}`

**Test Production URL:**
- After promoting deployment: `https://achillies.vercel.app`
- Wait 5-10 minutes after promoting
- Clear browser cache or use incognito mode
- Test: `/api/health` endpoint

---

## 🔍 QUICK DIAGNOSIS

**If preview works but production doesn't:**
→ Deployment not promoted to production (Step 2.2)

**If both return 404:**
→ Root directory wrong OR code not on GitHub (Step 1, Step 2.3)

**If build fails:**
→ Check build logs for errors (missing env vars, TypeScript errors, etc.)

**If site loads but features don't work:**
→ Missing environment variables (Step 3)

---

## ✅ SUCCESS CHECKLIST

- [ ] Code is on GitHub at `elikjwilliams/CorporateCrashoutTrading`
- [ ] Vercel project connected to GitHub repo
- [ ] Root directory set to `apps/corporate-crashout`
- [ ] Latest deployment marked as "Production"
- [ ] Environment variables set (at minimum: NEXTAUTH_SECRET, NEXTAUTH_URL)
- [ ] Preview URL works
- [ ] Production URL works
- [ ] `/api/health` returns `{"status":"ok"}`

---

## 🚀 FASTEST PATH (If You Want to Deploy Right Now)

**Do these in order:**

1. **Verify GitHub has code:**
   ```
   https://github.com/elikjwilliams/CorporateCrashoutTrading
   ```
   If empty, run:
   ```powershell
   cd "E:\My Drive"
   python tools/push_corporate_crashout.py https://github.com/elikjwilliams/CorporateCrashoutTrading.git
   ```

2. **Promote deployment to production:**
   - Vercel Dashboard → `achillies` project
   - Deployments → Latest → "..." → "Promote to Production"

3. **Wait 5 minutes, then test:**
   - Visit: `https://achillies.vercel.app`
   - Should work!

---

## 📞 IF STILL STUCK

**Check in this order:**

1. **Is code on GitHub?**
   - Go to: https://github.com/elikjwilliams/CorporateCrashoutTrading
   - Should see folders and files

2. **Is Vercel connected?**
   - Vercel Dashboard → Project → Settings → Git
   - Should show: `elikjwilliams/CorporateCrashoutTrading`

3. **Is deployment promoted?**
   - Deployments tab → Latest deployment
   - Should say "Production" not "Preview"

4. **Is root directory correct?**
   - Settings → General → Root Directory
   - Must be: `apps/corporate-crashout`

5. **Are env vars set?**
   - Settings → Environment Variables
   - Need at least: `NEXTAUTH_SECRET`, `NEXTAUTH_URL`

---

## 🎯 SUMMARY

**The main blocker is likely:**
- Production deployment not promoted (most common)
- OR code not on GitHub (if GitHub repo is empty)

**Quick fix:**
1. Push code to GitHub (if needed)
2. Promote latest deployment to production
3. Wait 5 minutes
4. Test site

**That's it!** 🚀

---

**Created by Auto + Otto to help you get unstuck!**
