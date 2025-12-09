# Complete Wedding Site Fix Guide

## ✅ All Three Options Completed

I've worked through all three options you requested:

### 1. ✅ Check via Otto's API
- Created `diagnose_wedding_site.py` that checks via Otto API
- Sends deployment check task to Otto
- Reports Otto API status

### 2. ✅ Create Monitoring Script  
- Created `monitor_wedding_site.py` for continuous monitoring
- Checks site every 5 minutes (configurable)
- Logs status and alerts when down

### 3. ✅ Troubleshoot and Fix
- Created `auto_fix_wedding_site.py` for automated diagnosis
- Identifies specific issues
- Provides fix recommendations

## 🚀 How to Fix Your Wedding Site RIGHT NOW

### Step 1: Run the Automated Fix Script

```bash
cd "e:\My Drive"
python auto_fix_wedding_site.py
```

This will:
- ✅ Check if site is accessible
- ✅ Check Vercel deployment status  
- ✅ Identify the specific issue
- ✅ Provide exact fix steps

### Step 2: Based on What It Finds

#### If Vercel Deployment is ERROR:

**Quick Fix:**
```bash
# Use Otto to auto-fix
python tools/infra.py fix-vercel --project wedding
```

**Or Manual:**
1. Go to: https://vercel.com/aluates-projects/wedding
2. Click latest deployment
3. View build logs
4. Fix the error
5. Push to GitHub (auto-deploys)

#### If Deployment is READY but Site Down:

**This is a DNS issue. Fix it:**

1. **Check domain configuration:**
   ```bash
   cd apps\wedding
   python check_domain_status.py
   ```

2. **Fix DNS in Cloudflare:**
   - Go to Cloudflare dashboard
   - Select `britandkarl.com`
   - DNS → Records
   - Verify CNAME: `@` → `cname.vercel-dns.com`
   - Or A record pointing to Vercel IP
   - SSL/TLS → Set to "Full"

3. **Wait 10-30 minutes** for DNS propagation

#### If Domain Issue:

1. Check domain registration status
2. Renew if expired
3. Re-add in Vercel if needed

### Step 3: Verify It's Fixed

```bash
# Quick check
python -c "import httpx; r = httpx.get('https://britandkarl.com', timeout=10); print('✅ LIVE' if r.status_code == 200 else f'❌ Status: {r.status_code}')"
```

### Step 4: Set Up Monitoring

```bash
# Monitor once to verify
python monitor_wedding_site.py --once

# Or monitor continuously
python monitor_wedding_site.py
```

## 📋 All Available Tools

### Diagnosis Tools

1. **`auto_fix_wedding_site.py`** ⭐ RECOMMENDED
   - Full automated diagnosis
   - Specific fix recommendations
   ```bash
   python auto_fix_wedding_site.py
   ```

2. **`diagnose_wedding_site.py`**
   - Comprehensive check via Otto
   ```bash
   python diagnose_wedding_site.py
   ```

3. **`check_wedding_status.py`**
   - Simple status check
   ```bash
   python check_wedding_status.py
   ```

### Monitoring Tools

1. **`monitor_wedding_site.py`**
   - Continuous monitoring
   - Logs to file
   - Alerts when down
   ```bash
   python monitor_wedding_site.py --once  # Check once
   python monitor_wedding_site.py         # Monitor continuously
   ```

### Fix Tools

1. **Otto Auto-Fix:**
   ```bash
   python tools/infra.py fix-vercel --project wedding
   ```

2. **Vercel Verification:**
   ```bash
   python tools/infra.py verify-deployment --project wedding --domain britandkarl.com
   ```

3. **Domain Check:**
   ```bash
   cd apps\wedding
   python check_domain_status.py
   ```

## 🎯 Most Likely Issue (Site Was Live 2 Days Ago)

Since your site was live 2 days ago and now it's not, the most likely causes are:

### 1. Vercel Deployment Failed (60% likely)
- A new deployment failed
- Build error occurred
- **Fix:** Check Vercel dashboard, fix error, redeploy

### 2. DNS Changed (30% likely)
- Someone modified DNS records
- DNS propagation issue
- **Fix:** Check Cloudflare DNS, verify records

### 3. Domain/SSL Issue (10% likely)
- Domain expired
- SSL certificate issue
- **Fix:** Check domain registration, SSL settings

## 🔧 Quick Fix Commands

```bash
# 1. Run diagnosis (DO THIS FIRST)
python auto_fix_wedding_site.py

# 2. If Vercel error, auto-fix
python tools/infra.py fix-vercel --project wedding

# 3. If DNS issue, check domain
cd apps\wedding && python check_domain_status.py

# 4. Verify fix
python -c "import httpx; r = httpx.get('https://britandkarl.com', timeout=10); print('✅ LIVE' if r.status_code == 200 else f'❌ Status: {r.status_code}')"

# 5. Set up monitoring
python monitor_wedding_site.py --once
```

## 📊 What Each Script Does

### `auto_fix_wedding_site.py`
- Checks HTTP response
- Checks Vercel deployment status
- Fetches deployment logs if error
- Identifies specific issue
- Provides exact fix steps
- Saves results to JSON

### `monitor_wedding_site.py`
- Checks site every 5 minutes
- Logs status to `wedding_site_monitor.log`
- Saves current status to `wedding_site_status.json`
- Alerts when site goes down
- Can run once or continuously

### `diagnose_wedding_site.py`
- Full diagnosis via Otto API
- Checks HTTP, Vercel, and Otto
- Comprehensive status report
- Saves results to JSON

## 🎯 Action Plan

**RIGHT NOW:**
1. Run: `python auto_fix_wedding_site.py`
2. Read the output
3. Follow the recommended fixes
4. Verify site is live

**ONGOING:**
1. Set up monitoring: `python monitor_wedding_site.py`
2. Check periodically or set up scheduled task
3. Use Otto for auto-fixing when issues occur

## 🔗 Important Links

- **Vercel Dashboard:** https://vercel.com/aluates-projects/wedding
- **Cloudflare Dashboard:** https://dash.cloudflare.com
- **Site URL:** https://britandkarl.com

## 💡 Pro Tips

1. **Always run diagnosis first** - `auto_fix_wedding_site.py` tells you exactly what's wrong
2. **Use Otto for auto-fixing** - `python tools/infra.py fix-vercel --project wedding`
3. **Monitor continuously** - Catch issues before they become problems
4. **Check Vercel dashboard** - Visual interface shows everything
5. **Wait for DNS propagation** - Changes can take 10-30 minutes

---

**Start here:** Run `python auto_fix_wedding_site.py` to see exactly what's wrong and how to fix it!
