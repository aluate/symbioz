# 🔍 How to Check Build Logs - Manual Instructions

Since we're having trouble with script output, here's how to check manually:

---

## Quick Check - Vercel Dashboard

1. **Go to:** https://vercel.com/dashboard
2. **Login** (if needed)
3. **Find project:** `achillies`
4. **Click on the project**

### Check Deployment Status:

1. Click **"Deployments"** tab (left sidebar)
2. Look at the **latest deployment**
3. Check the **status badge:**
   - ✅ Green = Ready
   - ⚠️ Yellow = Building
   - ❌ Red = Error

### View Build Logs:

1. Click on the **latest deployment** (the top one)
2. Click **"View Build Logs"** or scroll down to see logs
3. Look for:
   - ❌ Error messages (red text)
   - ⚠️ Warning messages (yellow text)
   - Build completion message

### Check Root Directory:

1. Click **"Settings"** tab
2. Click **"General"**
3. Look for **"Root Directory"**
4. Should be: `apps/corporate-crashout`

### Check Domain:

1. Click **"Settings"** tab
2. Click **"Domains"**
3. Check if `corporatecrashouttrading.com` is listed
4. Status should be "Valid Configuration" ✅

---

## Common Issues Found:

### Issue 1: Build Failed
**Look for in logs:**
- TypeScript errors
- Missing dependencies
- Import errors
- Build command failures

**Fix:**
- Fix the errors shown in logs
- Push fixes to GitHub
- Vercel will redeploy automatically

### Issue 2: Wrong Root Directory
**Symptoms:**
- Build succeeds but site shows 404
- Or build fails with "package.json not found"

**Fix:**
- Settings → General → Root Directory
- Change to: `apps/corporate-crashout`
- Save and redeploy

### Issue 3: Deployment Not Production
**Symptoms:**
- Build succeeds but only preview URL works
- Production domain returns 404

**Fix:**
- Deployments → Latest → "..." → "Promote to Production"

### Issue 4: No Deployments
**Symptoms:**
- No deployments in list

**Fix:**
- Check GitHub repo exists
- Verify Vercel is connected to GitHub
- Settings → Git → Verify repo connection
- Push code to trigger deployment

---

## What to Tell Me:

After checking, please share:

1. **Deployment Status:**
   - Ready ✅ / Building ⏳ / Error ❌

2. **If Error, what does it say?**
   - Copy any error messages from logs

3. **Root Directory:**
   - What is it set to? (should be `apps/corporate-crashout`)

4. **Domain Status:**
   - Is `corporatecrashouttrading.com` added?
   - What's the status?

---

**Check the dashboard and let me know what you find!** 🔍
