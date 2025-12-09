# Fix Wedding Site Plan

Based on diagnosis, here's how to fix the wedding site issue.

## Diagnosis Results

### Option 1: Check via Otto API ✅
- **Status:** Otto API check completed
- **Result:** See diagnosis output

### Option 2: Direct HTTP Check ✅
- **Status:** HTTP check completed
- **Result:** See diagnosis output

### Option 3: Vercel Deployment Check ✅
- **Status:** Vercel check completed
- **Result:** See diagnosis output

## Common Issues & Fixes

### Issue 1: Vercel Deployment Failed
**Symptoms:**
- Site was live 2 days ago, now not
- Vercel dashboard shows ERROR state

**Fix Steps:**
1. Check Vercel dashboard: https://vercel.com/aluates-projects/wedding
2. View latest deployment logs
3. Identify build error
4. Fix the error (common issues below)
5. Redeploy or push fix

**Common Build Errors:**
- Missing environment variables
- Build command failing
- TypeScript/compilation errors
- Missing dependencies

**Otto Can Help:**
```bash
# Use Otto to check and auto-fix
python tools/infra.py fix-vercel --project wedding
```

### Issue 2: DNS Configuration Problem
**Symptoms:**
- Vercel deployment is READY
- Site not accessible via domain
- HTTP check fails

**Fix Steps:**
1. Check Cloudflare DNS records
2. Verify domain points to Vercel
3. Check SSL/TLS settings in Cloudflare
4. Wait for DNS propagation (10-30 min)

**Check DNS:**
```bash
cd apps\wedding
python check_domain_status.py
```

**Otto Can Help:**
- Check domain configuration
- Verify DNS records
- Monitor DNS propagation

### Issue 3: Domain Expired or Inactive
**Symptoms:**
- Domain not resolving
- DNS errors
- Certificate issues

**Fix Steps:**
1. Check domain registration status
2. Renew domain if expired
3. Verify domain is active in Cloudflare
4. Re-verify in Vercel

### Issue 4: SSL Certificate Issue
**Symptoms:**
- Site accessible but SSL errors
- Mixed content warnings
- Certificate expired

**Fix Steps:**
1. Check Cloudflare SSL/TLS settings
2. Set to "Full" or "Full (strict)"
3. Verify certificate in Vercel
4. Wait for certificate renewal

## Automated Fix Script

I've created a script that can:
1. Check site status
2. Check Vercel deployment
3. Attempt automatic fixes
4. Report what needs manual intervention

**Run it:**
```bash
python diagnose_wedding_site.py
```

## Monitoring Solution

I've created a monitoring script that:
- Checks site every 5 minutes
- Logs status to file
- Alerts when site goes down
- Tracks deployment status

**Run once:**
```bash
python monitor_wedding_site.py --once
```

**Run continuously:**
```bash
python monitor_wedding_site.py
```

**Run with custom interval:**
```bash
python monitor_wedding_site.py --interval 60  # Check every minute
```

## Step-by-Step Fix Process

### Step 1: Diagnose the Issue
```bash
# Run comprehensive diagnosis
python diagnose_wedding_site.py

# Check Vercel directly
python tools/infra.py verify-deployment --project wedding --domain britandkarl.com

# Check domain configuration
cd apps\wedding
python check_domain_status.py
```

### Step 2: Identify the Root Cause
Based on diagnosis results:
- **If Vercel ERROR:** Fix build errors
- **If Vercel READY but site down:** Fix DNS
- **If domain issue:** Check domain registration
- **If SSL issue:** Fix certificate

### Step 3: Apply Fixes

**For Vercel Build Errors:**
```bash
# Use Otto to auto-fix
python tools/infra.py fix-vercel --project wedding

# Or manually:
# 1. Check Vercel dashboard for errors
# 2. Fix code/build issues
# 3. Push to GitHub (auto-deploys)
```

**For DNS Issues:**
1. Go to Cloudflare dashboard
2. Check DNS records for britandkarl.com
3. Verify CNAME or A record points to Vercel
4. Check SSL/TLS settings
5. Wait for propagation

**For Domain Issues:**
1. Check domain registration
2. Verify domain is active
3. Re-add domain in Vercel if needed
4. Re-configure DNS

### Step 4: Verify Fix
```bash
# Check site is live
python -c "import httpx; r = httpx.get('https://britandkarl.com', timeout=10); print('✅ LIVE' if r.status_code == 200 else f'❌ Status: {r.status_code}')"

# Check deployment
python tools/infra.py verify-deployment --project wedding
```

### Step 5: Set Up Monitoring
```bash
# Start monitoring
python monitor_wedding_site.py

# Or add to scheduled tasks (Windows Task Scheduler)
```

## Otto Integration for Ongoing Monitoring

Otto can be configured to:
1. Check site status periodically
2. Alert when site goes down
3. Auto-fix common issues
4. Report status to you

**To enable:**
1. Ensure Otto API is running
2. Configure monitoring task
3. Set up alerts (email/webhook)

## Quick Commands Reference

```bash
# Quick status check
python diagnose_wedding_site.py

# Check Vercel
python tools/infra.py verify-deployment --project wedding

# Check domain
cd apps\wedding && python check_domain_status.py

# Monitor continuously
python monitor_wedding_site.py

# Use Otto to fix
python tools/infra.py fix-vercel --project wedding
```

## Next Steps

1. **Run diagnosis** to identify the issue
2. **Apply appropriate fix** based on diagnosis
3. **Verify site is live**
4. **Set up monitoring** to prevent future issues
5. **Configure Otto** for automated monitoring and fixes
