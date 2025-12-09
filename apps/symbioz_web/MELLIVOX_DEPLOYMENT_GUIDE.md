# 🚀 Mellivox.com Deployment Guide

**Domain:** mellivox.com  
**Project:** Symbioz Web Game  
**Status:** Ready to deploy!

---

## 📋 Overview

The Mellivox/Symbioz website consists of:
1. **Frontend** (Next.js) → Deploy to **Vercel**
2. **Backend** (FastAPI) → Deploy to **Render**
3. **Domain** (mellivox.com) → Configure DNS

**Estimated Time:** ~30-45 minutes active work

---

## ✅ Prerequisites

- [ ] GitHub account (for code repository)
- [ ] Vercel account (free tier works)
- [ ] Render account (free tier works)
- [ ] Domain registrar access (where you bought mellivox.com)
- [ ] Code is in a GitHub repository (or ready to push)

---

## 🎯 Step 1: Deploy Frontend to Vercel

### Option A: Via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Sign in or create account

2. **Import Project**
   - Click "Add New" → "Project"
   - Connect your GitHub account if not already connected
   - Select repository: `aluate/symbioz` (or your repo name)
   - Click "Import"

3. **Configure Project**
   - **Project Name**: `mellivox` or `symbioz`
   - **Root Directory**: `apps/symbioz_web`
   - **Framework Preset**: Next.js (auto-detected)
   - **Build Command**: `npm install && npm run build` (auto-filled)
   - **Output Directory**: `.next` (auto-filled)
   - Click "Deploy"

4. **Wait for Deployment**
   - First deployment takes 2-5 minutes
   - You'll get a URL like: `https://symbioz-xyz.vercel.app`
   - **Save this URL** - you'll need it for backend configuration

### Option B: Via Command Line

```bash
cd apps/symbioz_web
npm install -g vercel
vercel
```

Follow the prompts to deploy.

---

## 🎯 Step 2: Deploy Backend to Render

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign in or create account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account if not already connected
   - Select repository: `aluate/symbioz` (or your repo name)

3. **Configure Service**
   - **Name**: `mellivox-api` or `symbioz-api`
   - **Root Directory**: `apps/symbioz_cli`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or paid if you prefer)
   - Click "Create Web Service"

4. **Set Environment Variables**
   In Render Dashboard → Environment tab, add:
   ```
   PYTHON_VERSION=3.11.11
   ALLOWED_ORIGINS=https://symbioz-xyz.vercel.app,https://*.vercel.app,https://mellivox.com,https://www.mellivox.com
   ```
   
   **Important**: Replace `symbioz-xyz.vercel.app` with your actual Vercel URL from Step 1.

5. **Deploy**
   - Render will automatically build and deploy
   - Wait for deployment (2-5 minutes)
   - Note the service URL (e.g., `https://mellivox-api.onrender.com`)
   - **Save this URL** - you'll need it for frontend configuration

6. **Verify Backend**
   - Health check: Visit `https://your-api-url.onrender.com/api/health`
   - Should return: `{"status": "ok", "message": "Symbioz Game API"}`
   - API docs: Visit `https://your-api-url.onrender.com/docs`

---

## 🎯 Step 3: Connect Frontend to Backend

1. **Go to Vercel Dashboard**
   - Select your `mellivox` or `symbioz` project
   - Go to **Settings** → **Environment Variables**

2. **Add Environment Variable**
   - Click "Add New"
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-api-url.onrender.com` (from Step 2)
   - **Environment**: Select all (Production, Preview, Development)
   - Click "Save"

3. **Redeploy**
   - Go to **Deployments** tab
   - Click "⋯" on latest deployment → "Redeploy"
   - **Important**: Vercel doesn't auto-redeploy when you add env vars

---

## 🎯 Step 4: Configure Domain (mellivox.com)

### Step 4a: Add Domain to Vercel

1. **Go to Vercel Dashboard**
   - Select your project
   - Go to **Settings** → **Domains**
   - Click "Add Domain"

2. **Add Domain**
   - Enter: `mellivox.com`
   - Click "Add"
   - Vercel will show you DNS records needed

3. **Copy DNS Records**
   Vercel will show something like:
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```
   **📋 Copy these exact values!**

### Step 4b: Configure DNS at Your Registrar

**Where you bought mellivox.com** (GoDaddy, Namecheap, Cloudflare, etc.):

1. **Log into your domain registrar**
   - Find DNS management section
   - Look for "DNS Records", "DNS Settings", or "Name Servers"

2. **Add DNS Records**

   **Record 1 - Root Domain:**
   - **Type**: `A`
   - **Name**: `@` (or leave blank for root domain)
   - **Value/IP**: `76.76.21.21` (use the IP from Vercel)
   - **TTL**: `3600` or Auto

   **Record 2 - WWW Subdomain:**
   - **Type**: `CNAME`
   - **Name**: `www`
   - **Value/Target**: `cname.vercel-dns.com` (use the value from Vercel)
   - **TTL**: `3600` or Auto

3. **Save Changes**

### Step 4c: Update Backend CORS

1. **Go to Render Dashboard**
   - Select your `mellivox-api` service
   - Go to **Environment** tab
   - Update `ALLOWED_ORIGINS` to include your domain:
   ```
   ALLOWED_ORIGINS=https://symbioz-xyz.vercel.app,https://*.vercel.app,https://mellivox.com,https://www.mellivox.com
   ```
   - Save (Render will auto-redeploy)

### Step 4d: Wait for DNS Propagation

- **Typical**: 5-30 minutes
- **Maximum**: 24-48 hours
- Vercel will show green checkmark when domain is configured correctly
- You can check status in Vercel Dashboard → Settings → Domains

---

## ✅ Step 5: Test Everything

1. **Test Frontend**
   - Visit: `https://mellivox.com`
   - Should load the landing page
   - Click "Enter the Hive"

2. **Test Backend Connection**
   - Open browser console (F12)
   - Try creating a character
   - Check for any API errors

3. **Test Game Flow**
   - Create character
   - Start a mission
   - Test combat
   - Verify save/load works

---

## 🔧 Troubleshooting

### Frontend Issues

**Problem**: Site shows "Failed to fetch" or API errors
- **Fix**: Check `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- **Fix**: Verify backend is running (check Render dashboard)
- **Fix**: Redeploy frontend after adding env var

**Problem**: Domain shows "Invalid Configuration"
- **Fix**: Check DNS records match exactly what Vercel shows
- **Fix**: Wait for DNS propagation (can take up to 48 hours)
- **Fix**: Verify DNS records are saved at your registrar

### Backend Issues

**Problem**: CORS errors in browser
- **Fix**: Check `ALLOWED_ORIGINS` includes your Vercel URL and domain
- **Fix**: Format: `https://mellivox.com,https://www.mellivox.com,https://*.vercel.app`
- **Fix**: Save changes in Render (auto-redeploys)

**Problem**: Backend won't start
- **Fix**: Check Render build logs for errors
- **Fix**: Verify `requirements.txt` has all dependencies
- **Fix**: Check start command uses `$PORT` not hardcoded port

### DNS Issues

**Problem**: Domain doesn't resolve
- **Fix**: Verify DNS records are correct at registrar
- **Fix**: Wait for DNS propagation (up to 48 hours)
- **Fix**: Use DNS checker: https://dnschecker.org

**Problem**: www works but root domain doesn't
- **Fix**: Make sure you have BOTH A record (@) and CNAME (www)
- **Fix**: Some registrars require different setup for root domain

---

## 📚 Quick Reference

### Environment Variables Summary

| Variable | Where | Value | Required |
|----------|-------|-------|----------|
| `NEXT_PUBLIC_API_URL` | Vercel | `https://your-api.onrender.com` | ✅ Yes |
| `ALLOWED_ORIGINS` | Render | `https://mellivox.com,https://www.mellivox.com,https://*.vercel.app` | ✅ Yes |
| `PYTHON_VERSION` | Render | `3.11.11` | ⚠️ Optional |
| `PORT` | Render | Auto-set | ❌ No |

### URLs to Save

- **Frontend (Vercel)**: `https://symbioz-xyz.vercel.app`
- **Backend (Render)**: `https://mellivox-api.onrender.com`
- **Domain**: `https://mellivox.com`

### Important Files

- **Frontend**: `apps/symbioz_web/`
- **Backend**: `apps/symbioz_cli/api_server.py`
- **Backend Config**: `apps/symbioz_cli/render.yaml`
- **Dependencies**: 
  - Frontend: `apps/symbioz_web/package.json`
  - Backend: `apps/symbioz_cli/requirements.txt`

---

## 🎉 You're Done!

Once DNS propagates, your site will be live at:
- ✅ `https://mellivox.com`
- ✅ `https://www.mellivox.com`

**Next Steps:**
- Monitor deployment logs for any issues
- Test all game features
- Set up monitoring/alerts if desired
- Consider adding analytics

---

## 📞 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **DNS Help**: Check your domain registrar's documentation
- **Project Docs**: See `apps/symbioz_web/DEPLOYMENT_STATUS.md` for more details

---

**Last Updated**: Based on current codebase structure  
**Status**: ✅ Ready to deploy
