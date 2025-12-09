# ⚡ Mellivox.com Quick Start Checklist

**Domain:** mellivox.com  
**Time to Live:** ~30-45 minutes

---

## ✅ Deployment Checklist

### 1. Frontend (Vercel) - ~10 min
- [ ] Go to https://vercel.com/dashboard
- [ ] Import GitHub repo: `aluate/symbioz`
- [ ] Set root directory: `apps/symbioz_web`
- [ ] Deploy
- [ ] **Save Vercel URL**: `https://symbioz-xyz.vercel.app`

### 2. Backend (Render) - ~10 min
- [ ] Go to https://dashboard.render.com
- [ ] Create Web Service from GitHub repo
- [ ] Set root directory: `apps/symbioz_cli`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
- [ ] Add env var: `ALLOWED_ORIGINS=https://your-vercel-url.vercel.app,https://*.vercel.app,https://mellivox.com,https://www.mellivox.com`
- [ ] Deploy
- [ ] **Save Render URL**: `https://mellivox-api.onrender.com`

### 3. Connect Frontend to Backend - ~5 min
- [ ] Vercel → Settings → Environment Variables
- [ ] Add: `NEXT_PUBLIC_API_URL` = `https://your-render-url.onrender.com`
- [ ] Redeploy frontend

### 4. Domain Configuration - ~10 min
- [ ] Vercel → Settings → Domains → Add `mellivox.com`
- [ ] Copy DNS records from Vercel
- [ ] Go to domain registrar
- [ ] Add A record: `@` → `76.76.21.21` (use IP from Vercel)
- [ ] Add CNAME record: `www` → `cname.vercel-dns.com` (use value from Vercel)
- [ ] Update Render `ALLOWED_ORIGINS` to include `https://mellivox.com,https://www.mellivox.com`
- [ ] Wait for DNS propagation (5 min - 48 hours)

### 5. Test - ~5 min
- [ ] Visit `https://mellivox.com`
- [ ] Test character creation
- [ ] Test game flow
- [ ] Check browser console for errors

---

## 🔑 Key URLs to Save

- **Frontend**: `https://symbioz-xyz.vercel.app`
- **Backend**: `https://mellivox-api.onrender.com`
- **Domain**: `https://mellivox.com`

---

## 📝 Environment Variables

### Vercel (Frontend)
```
NEXT_PUBLIC_API_URL=https://mellivox-api.onrender.com
```

### Render (Backend)
```
ALLOWED_ORIGINS=https://symbioz-xyz.vercel.app,https://*.vercel.app,https://mellivox.com,https://www.mellivox.com
PYTHON_VERSION=3.11.11
```

---

## 🚨 Common Issues

**CORS errors?** → Update `ALLOWED_ORIGINS` in Render  
**API not working?** → Check `NEXT_PUBLIC_API_URL` in Vercel  
**Domain not working?** → Check DNS records match Vercel exactly  
**Still broken?** → See full guide: `MELLIVOX_DEPLOYMENT_GUIDE.md`

---

**Full Guide**: See `MELLIVOX_DEPLOYMENT_GUIDE.md` for detailed instructions
