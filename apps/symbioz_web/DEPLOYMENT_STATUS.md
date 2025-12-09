# Symbioz Web Deployment Status

**Goal**: Make the game playable online (without custom domain yet)

## ✅ What's Ready

### Frontend (Next.js)
- ✅ Landing page with Mellivox branding
- ✅ Character creation screen
- ✅ Hub screen (mission selection)
- ✅ Combat screen
- ✅ Skill mission screen
- ✅ All game components connected
- ✅ Routing logic implemented
- ✅ API client configured to use `NEXT_PUBLIC_API_URL`
- ✅ Falls back to `localhost:8002` for local dev
- ✅ Security headers configured

### Backend (FastAPI)
- ✅ API server exists (`apps/symbioz_cli/api_server.py`)
- ✅ All game endpoints implemented
- ✅ Session management
- ✅ Save/load functionality
- ✅ CORS configured with environment variable support
- ✅ Automatically allows localhost for local dev
- ✅ Port configuration uses `$PORT` for production (defaults to 8002 locally)
- ✅ Health check endpoint at `/api/health`
- ✅ `render.yaml` deployment config created

### Local Development
- ✅ `LAUNCH_SYMBIOZ.bat` works perfectly
- ✅ Frontend automatically uses `localhost:8002` when `NEXT_PUBLIC_API_URL` not set
- ✅ Backend automatically allows localhost origins
- ✅ No changes needed for local play

## 🚀 Deployment Steps

### Step 1: Deploy Backend to Render

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign in or create account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account if not already connected
   - Select repository: `aluate/symbioz` (or your repo name)

3. **Configure Service**
   - **Name**: `symbioz-api`
   - **Root Directory**: `apps/symbioz_cli`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or paid if you prefer)

4. **Set Environment Variables**
   In Render Dashboard → Environment:
   ```
   PYTHON_VERSION=3.11.11
   ALLOWED_ORIGINS=https://symbioz.vercel.app,https://*.vercel.app
   ```
   
   **Note**: After you deploy the frontend, you'll get a Vercel URL. Update `ALLOWED_ORIGINS` to include:
   - Your actual Vercel URL (e.g., `https://symbioz-xyz.vercel.app`)
   - The wildcard pattern `https://*.vercel.app` for preview deployments

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy
   - Wait for deployment to complete (usually 2-5 minutes)
   - Note the service URL (e.g., `https://symbioz-api.onrender.com`)

6. **Verify Backend**
   - Health check: Visit `https://your-api-url.onrender.com/api/health`
   - Should return: `{"status": "ok", "message": "Symbioz Game API"}`
   - API docs: Visit `https://your-api-url.onrender.com/docs`

### Step 2: Update Frontend Environment Variable

1. **Go to Vercel Dashboard**
   - Visit [vercel.com/dashboard](https://vercel.com/dashboard)
   - Select your `symbioz` project

2. **Add Environment Variable**
   - Go to Settings → Environment Variables
   - Click "Add New"
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-api-url.onrender.com` (from Step 1)
   - **Environment**: Production, Preview, Development (select all)
   - Click "Save"

3. **Redeploy**
   - Go to Deployments tab
   - Click "⋯" on latest deployment → "Redeploy"
   - Or push a new commit to trigger auto-deploy
   - **Important**: Vercel doesn't auto-redeploy when you add env vars

### Step 3: Update Backend CORS (if needed)

If your Vercel URL is different from `symbioz.vercel.app`:

1. **Go to Render Dashboard**
   - Select your `symbioz-api` service
   - Go to Environment tab
   - Update `ALLOWED_ORIGINS`:
     ```
     https://your-actual-vercel-url.vercel.app,https://*.vercel.app
     ```
   - Save changes (Render will auto-redeploy)

### Step 4: Test the Game

1. Visit your Vercel site
2. Click "Enter the Hive" on landing page
3. Create a character
4. Try starting a mission
5. Check browser console (F12) for any errors

## 🔧 Configuration Details

### Backend Configuration

**File**: `apps/symbioz_cli/render.yaml`
- Defines Render service configuration
- Uses `$PORT` for port binding (required by Render)
- Health check at `/api/health`

**File**: `apps/symbioz_cli/api_server.py`
- CORS reads from `ALLOWED_ORIGINS` environment variable
- Defaults to localhost for local development
- Port uses `$PORT` or defaults to 8002 for local dev

### Frontend Configuration

**File**: `apps/symbioz_web/src/lib/api.ts`
- Uses `NEXT_PUBLIC_API_URL` environment variable
- Falls back to `http://localhost:8002` for local development

**Environment Variables**:
- **Local Dev**: No env var needed (uses `localhost:8002`)
- **Vercel Production**: Set `NEXT_PUBLIC_API_URL` to your Render API URL

## 🎮 Local Development

Everything still works locally:

1. **Start Backend**:
   ```bash
   cd apps/symbioz_cli
   python api_server.py
   ```
   Runs on `http://localhost:8002`

2. **Start Frontend**:
   ```bash
   cd apps/symbioz_web
   npm run dev
   ```
   Runs on `http://localhost:3000`

3. **Or use the launcher**:
   ```bash
   LAUNCH_SYMBIOZ.bat
   ```
   Starts both automatically

**Local CORS**: Automatically allows `localhost:3000` and `localhost:3001`

## 📋 Deployment Checklist

- [ ] Backend deployed to Render
- [ ] Backend health check works (`/api/health`)
- [ ] `ALLOWED_ORIGINS` set in Render (includes Vercel URL)
- [ ] `NEXT_PUBLIC_API_URL` set in Vercel
- [ ] Vercel site redeployed after env var change
- [ ] Test character creation
- [ ] Test mission selection
- [ ] Test combat
- [ ] Test skill missions
- [ ] Verify save/load works

## 🔍 Troubleshooting

### Backend Issues

**Issue**: "ModuleNotFoundError"
- **Fix**: Ensure `requirements.txt` includes all dependencies
- Check Render build logs

**Issue**: "Port already in use"
- **Fix**: Make sure start command uses `$PORT`, not hardcoded port

**Issue**: CORS errors in browser
- **Fix**: Check `ALLOWED_ORIGINS` includes your Vercel URL
- Verify format: `https://your-site.vercel.app,https://*.vercel.app`

### Frontend Issues

**Issue**: "Failed to fetch" or network errors
- **Fix**: Check `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Verify backend is running and accessible
- Check browser console for CORS errors

**Issue**: API calls go to localhost in production
- **Fix**: Ensure `NEXT_PUBLIC_API_URL` is set in Vercel
- Redeploy after adding env var

## 📚 Files Modified

### Backend
- `apps/symbioz_cli/render.yaml` - Created (Render deployment config)
- `apps/symbioz_cli/api_server.py` - Updated:
  - CORS now reads from `ALLOWED_ORIGINS` env var
  - Port uses `$PORT` or defaults to 8002
  - Added `/api/health` endpoint

### Frontend
- `apps/symbioz_web/src/lib/api.ts` - Already correct (uses `NEXT_PUBLIC_API_URL`)

### Documentation
- `apps/symbioz_web/DEPLOYMENT_STATUS.md` - This file (updated with deployment steps)

---

**Status**: ✅ Ready for deployment - all configuration files in place

**Next Steps**: 
1. Deploy backend to Render using `render.yaml`
2. Set `NEXT_PUBLIC_API_URL` in Vercel
3. Test the game online!
