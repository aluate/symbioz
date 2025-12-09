# Fix Wedding Site DNS Issue

## 🔍 Problem Identified

From the screenshots, I can see:

### Issue 1: Vercel Domain Configuration
- ❌ `britandkarl.com` shows **"Invalid Configuration"**
- ✅ `www.britandkarl.com` shows **"Valid Configuration"** and is in Production
- There's a 307 redirect from root to www

### Issue 2: Cloudflare DNS Missing Root Record
- ✅ `www.britandkarl.com` has CNAME pointing to Vercel
- ✅ `a.britandkarl.com` has A record
- ❌ **Missing root domain (`@`) record** for `britandkarl.com`

## 🛠️ Fix Steps

### Step 1: Fix Cloudflare DNS

You need to add a DNS record for the root domain:

1. **In Cloudflare DNS page:**
   - Click **"Add record"**
   - **Type:** `CNAME` (or `A` if Vercel provides an IP)
   - **Name:** `@` (this means root domain)
   - **Content:** Use the same Vercel domain as `www` record
     - From your screenshot, `www` points to: `c624a7d614776412.vercel-...`
     - **OR** check Vercel dashboard for the correct CNAME target
   - **Proxy status:** `DNS only` (same as your www record)
   - **TTL:** `Auto`
   - Click **"Save"**

2. **Alternative (if CNAME doesn't work for root):**
   - Vercel may provide an A record IP address
   - Check Vercel dashboard → Domains → `britandkarl.com` → DNS records
   - Use that IP for an A record instead

### Step 2: Fix Vercel Domain Configuration

1. **In Vercel dashboard:**
   - Go to: https://vercel.com/aluates-projects/wedding/settings/domains
   - Click on `britandkarl.com` (the one showing "Invalid Configuration")
   - Click **"Learn more"** to see what's wrong
   - Follow Vercel's instructions to fix the configuration

2. **Common fixes:**
   - Verify DNS records match what Vercel expects
   - Wait for DNS propagation (can take 10-30 minutes)
   - Remove and re-add the domain if needed

### Step 3: Verify Fix

After making changes:

1. **Wait 10-30 minutes** for DNS propagation
2. **Check Vercel dashboard** - `britandkarl.com` should show "Valid Configuration"
3. **Test the site:**
   ```bash
   python check_site_now.py
   ```

## 📋 Quick Reference

### Cloudflare DNS Records Needed:

```
Type    Name    Content                          Proxy
CNAME   @       c624a7d614776412.vercel-...     DNS only
CNAME   www     c624a7d614776412.vercel-...     DNS only
```

**OR** if Vercel provides an A record:

```
Type    Name    Content          Proxy
A       @       76.76.21.21      DNS only
CNAME   www     c624a7d614776412.vercel-...     DNS only
```

### Vercel Domain Status:
- `britandkarl.com` - Should show "Valid Configuration" ✅
- `www.britandkarl.com` - Already shows "Valid Configuration" ✅

## 🎯 Expected Result

After fixing:
- ✅ Root domain `britandkarl.com` works
- ✅ `www.britandkarl.com` continues to work
- ✅ Both point to your Vercel deployment
- ✅ Site is live and accessible
