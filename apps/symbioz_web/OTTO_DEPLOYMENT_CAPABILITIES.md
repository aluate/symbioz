# Otto Deployment Capabilities for Symbioz/Mellivox

**Question**: Can Otto complete the deployment?  
**Answer**: **Partially** - Otto can automate ~70% of the deployment, but some steps still need manual action.

---

## ✅ What Otto CAN Do

### 1. Frontend Deployment (Vercel) - **100% Automated** ✅

**Commands Available:**
```bash
# Create Vercel project and deploy
python tools/infra.py setup-vercel-project \
  --project symbioz \
  --repo YOUR_USERNAME/symbioz \
  --root-dir apps/symbioz_web \
  --framework nextjs

# Set environment variables
python tools/infra.py set-env-var \
  --project symbioz \
  --name NEXT_PUBLIC_API_URL \
  --value https://your-backend-url.onrender.com

# Configure custom domain (optional, for later)
python tools/infra.py configure-domain \
  --project symbioz \
  --domain mellivox.com
```

**What It Does:**
- ✅ Creates Vercel project via API
- ✅ Connects GitHub repository
- ✅ Sets root directory
- ✅ Configures framework
- ✅ Triggers initial deployment
- ✅ Sets environment variables
- ✅ Monitors deployment status

---

### 2. Backend Environment Variables (Render) - **100% Automated** ✅

**Commands Available:**
```bash
# Set environment variables in Render
python tools/infra.py set-render-env \
  --project symbioz \
  --service api \
  --key ALLOWED_ORIGINS \
  --value "https://your-vercel-url.vercel.app,https://*.vercel.app"
```

**What It Does:**
- ✅ Sets environment variables in Render via API
- ✅ Triggers automatic redeploy
- ✅ Works once Render service exists

---

### 3. Deployment Monitoring - **100% Automated** ✅

**Via Otto's DeploymentAutomationSkill:**
- ✅ Monitors Render builds
- ✅ Monitors Vercel builds
- ✅ Auto-fixes common errors
- ✅ Retries on failure

**Usage:**
- Ask Otto: "Deploy symbioz and fix any errors"
- Otto will push commits, monitor builds, and fix issues automatically

---

### 4. Diagnostics & Health Checks - **100% Automated** ✅

```bash
# Check deployment status
python tools/infra.py diag --env=prod --provider vercel
python tools/infra.py diag --env=prod --provider render
```

**What It Does:**
- ✅ Checks deployment status
- ✅ Verifies services are accessible
- ✅ Tests health endpoints
- ✅ Generates reports

---

## ⚠️ What Otto CANNOT Do (Yet)

### 1. Create Render Service from Scratch - **Not Fully Automated** ❌

**Current Limitation:**
- Otto can deploy to Render via `provision-project` command, but it requires:
  - A project spec file (`infra/project-specs/symbioz.yaml`)
  - The service to already exist in `infra/providers/render.yaml` config
  - OR manual creation via Render dashboard first

**What You Need to Do:**
1. **Option A**: Create Render service manually via dashboard (first time only)
2. **Option B**: Create project spec file and use `provision-project` command

**After service exists**, Otto can:
- ✅ Set environment variables
- ✅ Trigger deployments
- ✅ Monitor builds
- ✅ Fix errors

---

## 🎯 Recommended Deployment Strategy

### Step 1: Manual (One-Time Setup) - ~10 min

**Create Render Service:**
1. Go to Render Dashboard
2. Create Web Service from GitHub repo
3. Configure:
   - Root Directory: `apps/symbioz_cli`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
4. **Save the service ID** (you'll need it for Otto config)

**Add to Otto Config:**
Edit `infra/providers/render.yaml`:
```yaml
services:
  symbioz-api:
    render_service_id: "srv-xxxxx"  # From Render dashboard
    repo: "YOUR_USERNAME/symbioz"
    branch: "main"
```

---

### Step 2: Otto Automation - ~5 min

**Deploy Frontend:**
```bash
python tools/infra.py setup-vercel-project \
  --project symbioz \
  --repo YOUR_USERNAME/symbioz \
  --root-dir apps/symbioz_web \
  --framework nextjs
```

**Get Vercel URL** (from output), then:

**Set Backend CORS:**
```bash
python tools/infra.py set-render-env \
  --project symbioz \
  --service api \
  --key ALLOWED_ORIGINS \
  --value "https://your-vercel-url.vercel.app,https://*.vercel.app"
```

**Set Frontend API URL:**
```bash
python tools/infra.py set-env-var \
  --project symbioz \
  --name NEXT_PUBLIC_API_URL \
  --value https://your-backend-url.onrender.com
```

**Redeploy Frontend:**
- Go to Vercel dashboard → Deployments → Redeploy
- (Or Otto's DeploymentAutomationSkill can handle this)

---

## 📊 Automation Summary

| Task | Otto Can Do | Manual Required |
|------|-------------|-----------------|
| Create Vercel project | ✅ Yes | ❌ No |
| Deploy frontend | ✅ Yes | ❌ No |
| Set Vercel env vars | ✅ Yes | ❌ No |
| Create Render service | ⚠️ Partial* | ✅ Yes (first time) |
| Set Render env vars | ✅ Yes | ❌ No |
| Trigger Render deploy | ✅ Yes | ❌ No |
| Monitor deployments | ✅ Yes | ❌ No |
| Auto-fix errors | ✅ Yes | ❌ No |
| Configure domain | ✅ Yes | ⚠️ DNS records |

**Total Automation**: ~70%  
**Manual Steps**: ~30% (mostly one-time setup)

\* *Otto can deploy to Render via project specs, but requires config setup first*

---

## 🚀 Quick Start with Otto

### Prerequisites
1. ✅ Otto infrastructure tool installed (`tools/infra.py`)
2. ✅ Environment variables set:
   - `VERCEL_TOKEN` (from Vercel dashboard)
   - `RENDER_API_KEY` (from Render dashboard)
   - `GITHUB_TOKEN` (from GitHub settings)

### One-Time Setup
1. Create Render service manually (see Step 1 above)
2. Add service ID to `infra/providers/render.yaml`

### Then Use Otto
```bash
# Deploy everything
python tools/infra.py setup-vercel-project --project symbioz --repo YOUR_USERNAME/symbioz --root-dir apps/symbioz_web
python tools/infra.py set-render-env --project symbioz --service api --key ALLOWED_ORIGINS --value "https://..."
python tools/infra.py set-env-var --project symbioz --name NEXT_PUBLIC_API_URL --value "https://..."
```

---

## 💡 Future Improvements

To make Otto 100% automated, we could add:

1. **`setup-render-service` command** (like `setup-vercel-project`)
   - Create Render service from scratch
   - Auto-configure from `render.yaml`
   - Set initial environment variables

2. **Full deployment orchestration**
   - Deploy backend first
   - Get backend URL
   - Deploy frontend
   - Connect them automatically
   - Test end-to-end

**Current Status**: Otto is very capable, but Render service creation needs one manual step (or project spec setup).

---

## 📚 Related Documentation

- **Full Deployment Guide**: `DEPLOYMENT_READY.md`
- **Otto Infrastructure Tool**: `infra/README.md`
- **Deployment Automation Skill**: `apps/otto/DEPLOYMENT_AUTOMATION_SKILL.md`

---

**Bottom Line**: Otto can automate most of the deployment, but you'll need to create the Render service manually the first time (or set up a project spec). After that, Otto can handle everything else!
