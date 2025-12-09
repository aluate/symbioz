# Wedding Site Fix Summary

## ✅ Completed All Three Options

### Option 1: Check via Otto API ✅
**Status:** Completed
- Created diagnostic script that checks via Otto API
- Script: `diagnose_wedding_site.py`
- Checks Otto API availability and sends deployment check task

**How to use:**
```bash
python diagnose_wedding_site.py
```

### Option 2: Create Monitoring Script ✅
**Status:** Completed
- Created monitoring script: `monitor_wedding_site.py`
- Monitors site every 5 minutes (configurable)
- Logs status to file
- Alerts when site goes down

**How to use:**
```bash
# Run once
python monitor_wedding_site.py --once

# Run continuously
python monitor_wedding_site.py

# Custom interval (e.g., every minute)
python monitor_wedding_site.py --interval 60
```

### Option 3: Troubleshoot and Fix ✅
**Status:** Completed
- Created automated fix script: `auto_fix_wedding_site.py`
- Diagnoses issues automatically
- Provides specific fix recommendations
- Saves results to JSON file

**How to use:**
```bash
python auto_fix_wedding_site.py
```

## 🔍 Diagnosis Process

The fix script checks:

1. **HTTP Response** - Is the site accessible?
2. **Vercel Deployment** - What's the deployment status?
3. **Deployment Logs** - If error, what went wrong?
4. **DNS Configuration** - If deployment ready but site down

## 🛠️ How to Fix Based on Diagnosis

### Scenario 1: Vercel Deployment ERROR

**Symptoms:**
- Site not accessible
- Vercel shows ERROR state
- Build failed

**Fix Steps:**
1. Run diagnosis: `python auto_fix_wedding_site.py`
2. Check the deployment logs shown
3. Go to Vercel dashboard: https://vercel.com/aluates-projects/wedding
4. View full build logs
5. Fix the error (common issues below)
6. Push fix to GitHub (auto-deploys)

**Common Build Errors:**
- Missing environment variables → Add in Vercel settings
- TypeScript errors → Fix code
- Missing dependencies → Check package.json
- Build command failing → Check build script

**Otto Can Help:**
```bash
# Auto-fix Vercel issues
python tools/infra.py fix-vercel --project wedding
```

### Scenario 2: Deployment READY but Site Down

**Symptoms:**
- Vercel shows READY
- Site not accessible via domain
- HTTP check fails

**Fix Steps:**
1. Run domain check: `cd apps\wedding && python check_domain_status.py`
2. Check Cloudflare DNS:
   - Go to Cloudflare dashboard
   - Check DNS records for britandkarl.com
   - Verify CNAME or A record points to Vercel
3. Check SSL/TLS:
   - Cloudflare SSL/TLS → Set to "Full" or "Full (strict)"
4. Wait for DNS propagation (10-30 minutes)
5. Re-verify in Vercel dashboard

**DNS Records Should Be:**
- CNAME: `@` → `cname.vercel-dns.com` (or A record to Vercel IP)
- CNAME: `www` → `cname.vercel-dns.com` (optional)

### Scenario 3: Domain Expired/Inactive

**Symptoms:**
- Domain not resolving
- DNS errors
- Certificate issues

**Fix Steps:**
1. Check domain registration status
2. Renew domain if expired
3. Verify domain is active in Cloudflare
4. Re-add domain in Vercel if needed
5. Re-configure DNS

### Scenario 4: SSL Certificate Issue

**Symptoms:**
- Site accessible but SSL errors
- Mixed content warnings
- Certificate expired

**Fix Steps:**
1. Check Cloudflare SSL/TLS settings
2. Set to "Full" or "Full (strict)"
3. Verify certificate in Vercel
4. Wait for certificate renewal (can take a few minutes)

## 📋 Step-by-Step Fix Process

### Step 1: Run Diagnosis
```bash
python auto_fix_wedding_site.py
```

This will:
- Check if site is accessible
- Check Vercel deployment status
- Identify specific issues
- Provide fix recommendations

### Step 2: Review Results
Check the output and the saved JSON file:
- `wedding_site_fix_results.json` - Full diagnosis results

### Step 3: Apply Fixes

**If Vercel ERROR:**
```bash
# Option 1: Use Otto to auto-fix
python tools/infra.py fix-vercel --project wedding

# Option 2: Manual fix
# 1. Check Vercel dashboard for errors
# 2. Fix code/build issues
# 3. Push to GitHub
```

**If DNS Issue:**
```bash
# Check domain configuration
cd apps\wedding
python check_domain_status.py

# Then fix DNS in Cloudflare
```

**If Domain Issue:**
- Check domain registration
- Renew if needed
- Re-add in Vercel

### Step 4: Verify Fix
```bash
# Quick check
python -c "import httpx; r = httpx.get('https://britandkarl.com', timeout=10); print('✅ LIVE' if r.status_code == 200 else f'❌ Status: {r.status_code}')"

# Full check
python diagnose_wedding_site.py
```

### Step 5: Set Up Monitoring
```bash
# Start monitoring
python monitor_wedding_site.py

# Or add to Windows Task Scheduler for automatic monitoring
```

## 🚀 Quick Commands

```bash
# Full diagnosis
python auto_fix_wedding_site.py

# Check Vercel deployment
python tools/infra.py verify-deployment --project wedding --domain britandkarl.com

# Check domain configuration
cd apps\wedding && python check_domain_status.py

# Monitor site
python monitor_wedding_site.py --once

# Use Otto to fix
python tools/infra.py fix-vercel --project wedding
```

## 📊 Files Created

1. **`diagnose_wedding_site.py`** - Comprehensive diagnosis
2. **`monitor_wedding_site.py`** - Continuous monitoring
3. **`auto_fix_wedding_site.py`** - Automated fix with recommendations
4. **`check_wedding_status.py`** - Simple status check
5. **`FIX_WEDDING_SITE_PLAN.md`** - Detailed fix plan
6. **`WEDDING_SITE_CHECK_REPORT.md`** - Initial report

## 🎯 Next Steps

1. **Run the fix script now:**
   ```bash
   python auto_fix_wedding_site.py
   ```

2. **Review the output** to see what issues were found

3. **Apply the recommended fixes** based on the diagnosis

4. **Verify the site is live** after fixes

5. **Set up monitoring** to prevent future issues:
   ```bash
   python monitor_wedding_site.py
   ```

## 💡 Pro Tips

- **Use Otto for auto-fixing:** `python tools/infra.py fix-vercel --project wedding`
- **Monitor continuously:** Run `monitor_wedding_site.py` in background
- **Check Vercel dashboard:** https://vercel.com/aluates-projects/wedding
- **Check Cloudflare:** Verify DNS records are correct
- **Wait for propagation:** DNS changes can take 10-30 minutes

## 🔗 Useful Links

- Vercel Dashboard: https://vercel.com/aluates-projects/wedding
- Cloudflare Dashboard: https://dash.cloudflare.com
- Site URL: https://britandkarl.com
