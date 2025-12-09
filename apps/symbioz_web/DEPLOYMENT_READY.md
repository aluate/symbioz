# ✅ Deployment Ready - Make Game Playable Online

**Status**: All code is ready! Just need to deploy and connect the pieces.

---

## 🎯 What's Already Done

### Backend (FastAPI)
- ✅ CORS configured to read from `ALLOWED_ORIGINS` environment variable
- ✅ Automatically allows localhost for local dev
- ✅ Port uses `$PORT` from environment (defaults to 8002 locally)
- ✅ Health check endpoint at `/api/health`
- ✅ `render.yaml` deployment config exists

### Frontend (Next.js)
- ✅ API client uses `NEXT_PUBLIC_API_URL` environment variable
- ✅ Falls back to `http://localhost:8002` for local dev
- ✅ All game components connected and working

### Local Development
- ✅ `LAUNCH_SYMBIOZ.bat` still works perfectly
- ✅ Frontend calls localhost:8002 automatically
- ✅ No changes needed for local play

---

## 🚀 What You Need to Do (30-45 minutes)

### Step 1: Deploy Backend to Render (~15 min)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign in or create account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub account if not already connected
   - Select repository: `aluate/symbioz` (or your repo name)

3. **Configure Service**
   - **Name**: `symbioz-api` (or `mellivox-api`)
   - **Root Directory**: `apps/symbioz_cli`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or paid)

   **OR** use the `render.yaml` file:
   - Render can auto-detect `render.yaml` in the repo
   - You may need to point it to `apps/symbioz_cli/render.yaml`
   - Or manually configure using the values above

4. **Set Environment Variables** (in Render Dashboard → Environment)
   ```
   PYTHON_VERSION=3.11.11
   ALLOWED_ORIGINS=https://*.vercel.app
   ```
   
   **Note**: We'll update `ALLOWED_ORIGINS` after frontend is deployed to include the actual Vercel URL.

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-5 minutes)
   - **Save the backend URL**: `https://symbioz-api.onrender.com` (or similar)

6. **Verify Backend**
   - Visit: `https://your-backend-url.onrender.com/api/health`
   - Should return: `{"status": "ok", "message": "Symbioz Game API"}`
   - API docs: `https://your-backend-url.onrender.com/docs`

---

### Step 2: Deploy Frontend to Vercel (~10 min)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Sign in or create account

2. **Import Project**
   - Click "Add New" → "Project"
   - Connect GitHub account if not already connected
   - Select repository: `aluate/symbioz` (or your repo name)
   - Click "Import"

3. **Configure Project**
   - **Project Name**: `symbioz` or `mellivox`
   - **Root Directory**: `apps/symbioz_web`
   - **Framework Preset**: Next.js (auto-detected)
   - **Build Command**: `npm install && npm run build` (auto-filled)
   - **Output Directory**: `.next` (auto-filled)
   - Click "Deploy"

4. **Wait for Deployment**
   - First deployment takes 2-5 minutes
   - **Save the Vercel URL**: `https://symbioz-xyz.vercel.app` (or similar)

---

### Step 3: Connect Frontend to Backend (~5 min)

1. **Update Backend CORS** (in Render)
   - Go to Render Dashboard → Your service → Environment
   - Update `ALLOWED_ORIGINS` to:
     ```
     https://your-actual-vercel-url.vercel.app,https://*.vercel.app
     ```
   - Replace `your-actual-vercel-url` with your actual Vercel URL
   - Save (Render will auto-redeploy)

2. **Set Frontend Environment Variable** (in Vercel)
   - Go to Vercel Dashboard → Your project → Settings → Environment Variables
   - Click "Add New"
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-backend-url.onrender.com` (from Step 1)
   - **Environment**: Select all (Production, Preview, Development)
   - Click "Save"

3. **Redeploy Frontend**
   - Go to Deployments tab
   - Click "⋯" on latest deployment → "Redeploy"
   - **Important**: Vercel doesn't auto-redeploy when you add env vars

---

### Step 4: Test the Game (~5 min)

1. **Visit your Vercel site**
   - Should load the landing page
   - Click "Enter the Hive"

2. **Test Game Flow**
   - Create a character
   - Start a mission
   - Test combat
   - Check browser console (F12) for any errors

3. **Verify API Connection**
   - Open browser console (F12)
   - Look for network requests to your Render backend
   - Should see successful API calls (status 200)

---

## 🔧 Configuration Summary

### Environment Variables

**Render (Backend)**:
```
PYTHON_VERSION=3.11.11
ALLOWED_ORIGINS=https://your-vercel-url.vercel.app,https://*.vercel.app
```

**Vercel (Frontend)**:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
```

### URLs to Save

- **Backend**: `https://symbioz-api.onrender.com` (or your Render URL)
- **Frontend**: `https://symbioz-xyz.vercel.app` (or your Vercel URL)

---

## ✅ Verification Checklist

- [ ] Backend deployed to Render
- [ ] Backend health check works (`/api/health`)
- [ ] Frontend deployed to Vercel
- [ ] `ALLOWED_ORIGINS` set in Render (includes Vercel URL)
- [ ] `NEXT_PUBLIC_API_URL` set in Vercel
- [ ] Frontend redeployed after env var change
- [ ] Game loads on Vercel URL
- [ ] Character creation works
- [ ] Missions load
- [ ] Combat works
- [ ] No CORS errors in browser console

---

## 🐛 Troubleshooting

### CORS Errors
- **Symptom**: Browser console shows CORS errors
- **Fix**: Check `ALLOWED_ORIGINS` in Render includes your exact Vercel URL
- **Fix**: Make sure URL format is correct: `https://your-site.vercel.app` (no trailing slash)

### API Not Working
- **Symptom**: "Failed to fetch" or network errors
- **Fix**: Check `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- **Fix**: Verify backend is running (check Render dashboard)
- **Fix**: Redeploy frontend after adding env var

### Backend Won't Start
- **Symptom**: Render deployment fails
- **Fix**: Check build logs for errors
- **Fix**: Verify `requirements.txt` has all dependencies
- **Fix**: Check start command uses `$PORT` not hardcoded port

---

## 📝 Files Modified/Created

### Already Configured (No Changes Needed)
- ✅ `apps/symbioz_cli/api_server.py` - CORS and port already configured
- ✅ `apps/symbioz_cli/render.yaml` - Deployment config exists
- ✅ `apps/symbioz_web/src/lib/api.ts` - Uses `NEXT_PUBLIC_API_URL` correctly
- ✅ `LAUNCH_SYMBIOZ.bat` - Still works for local dev

### Documentation Created
- ✅ `apps/symbioz_web/DEPLOYMENT_READY.md` - This file
- ✅ `apps/symbioz_web/DEPLOYMENT_STATUS.md` - Detailed deployment guide
- ✅ `apps/symbioz_web/ENV_SETUP.md` - Environment variable reference

---

## 🎉 Next Steps After Deployment

Once the game is playable online:

1. **Test thoroughly** - Play through a full game session
2. **Monitor logs** - Check Render and Vercel logs for any issues
3. **Add custom domain** (optional) - See `MELLIVOX_DEPLOYMENT_GUIDE.md` for domain setup
4. **Set up monitoring** (optional) - Add error tracking if desired

---

**Status**: ✅ Ready to deploy - all code is production-ready!

**Time to Live**: ~30-45 minutes of active work (deploy + connect + test)
