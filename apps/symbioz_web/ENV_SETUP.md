# Environment Variables Setup

Quick reference for environment variables needed for Symbioz/Mellivox deployment.

## Frontend (Vercel)

### Production Environment

**Variable**: `NEXT_PUBLIC_API_URL`

**Value**: `https://your-backend-url.onrender.com` (or your backend host)

**Where to set**: Vercel Dashboard → Project → Settings → Environment Variables

**Important**:
- Must start with `NEXT_PUBLIC_` to be available in browser
- After adding, **redeploy** the site (Vercel won't auto-redeploy)
- Set for all environments: Production, Preview, Development

**Example**:
```
NEXT_PUBLIC_API_URL=https://symbioz-api.onrender.com
```

### Local Development

**No environment variable needed** - defaults to `http://localhost:8002`

If you want to override:
```bash
# .env.local (not committed to git)
NEXT_PUBLIC_API_URL=http://localhost:8002
```

## Backend (Render)

### Required Variables

**Variable**: `ALLOWED_ORIGINS`

**Value**: Comma-separated list of frontend URLs allowed by CORS

**Example**:
```
ALLOWED_ORIGINS=https://symbioz.vercel.app,https://*.vercel.app
```

**Where to set**: Render Dashboard → Service → Environment

**Notes**:
- Include your actual Vercel URL
- Include `https://*.vercel.app` for preview deployments
- Localhost is automatically allowed (no need to include)

**Variable**: `PYTHON_VERSION` (optional)

**Value**: `3.11.11` (or your preferred Python version)

**Where to set**: Render Dashboard → Service → Environment

### Port Configuration

**Variable**: `PORT`

**Value**: Automatically set by Render (don't set manually)

**Note**: The API server reads `$PORT` from environment and defaults to 8002 for local dev.

## Local Development

### Backend

No environment variables needed for local development. The API server:
- Uses port 8002 by default
- Allows `localhost:3000` and `localhost:3001` for CORS automatically

### Frontend

No environment variables needed. The API client:
- Defaults to `http://localhost:8002` if `NEXT_PUBLIC_API_URL` is not set

## Environment Variable Summary

| Variable | Frontend (Vercel) | Backend (Render) | Local Dev |
|----------|------------------|-----------------|-----------|
| `NEXT_PUBLIC_API_URL` | ✅ Required | ❌ | ❌ Optional |
| `ALLOWED_ORIGINS` | ❌ | ✅ Required | ❌ Auto |
| `PORT` | ❌ | ✅ Auto-set | ❌ Auto (8002) |
| `PYTHON_VERSION` | ❌ | ⚠️ Optional | ❌ |

## Quick Setup Commands

### Vercel (via Dashboard)
1. Go to Project → Settings → Environment Variables
2. Add `NEXT_PUBLIC_API_URL` = `https://your-api.onrender.com`
3. Redeploy

### Render (via Dashboard)
1. Go to Service → Environment
2. Add `ALLOWED_ORIGINS` = `https://your-site.vercel.app,https://*.vercel.app`
3. (Optional) Add `PYTHON_VERSION` = `3.11.11`
4. Save (auto-redeploys)

---

**See `DEPLOYMENT_STATUS.md` for full deployment instructions.**

