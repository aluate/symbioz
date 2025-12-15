# Fix: Render "Could not open requirements file" Error

## 🚨 Error

```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

## 🔍 Root Cause

Render is using **Python runtime** instead of **Docker runtime**, and the **Root Directory** is not set to `apps/otto`.

## ✅ Fix (Choose One)

### Option 1: Use Docker Runtime (RECOMMENDED)

**Why:** We have a Dockerfile that handles everything correctly.

**Steps:**
1. Go to Render Dashboard → Your Otto Service → Settings
2. Scroll to **"Runtime"** section
3. Change from **"Python"** to **"Docker"**
4. **Root Directory:** Should be `apps/otto` (verify this is set)
5. Save changes
6. Render will automatically redeploy

**Result:** Render will use `apps/otto/Dockerfile` and everything will work.

---

### Option 2: Fix Python Runtime (If you prefer Python)

**Steps:**
1. Go to Render Dashboard → Your Otto Service → Settings
2. Scroll to **"Root Directory"** section
3. Set **Root Directory:** `apps/otto` (CRITICAL!)
4. Verify **Runtime** is set to **"Python"**
5. Verify **Build Command** is: `pip install -r requirements.txt`
6. Verify **Start Command** is: `python -m uvicorn otto.api:app --host 0.0.0.0 --port $PORT`
7. Save changes
8. Render will automatically redeploy

**Result:** Render will look for `requirements.txt` in `apps/otto/` directory.

---

## 🎯 Quick Check

**In Render Dashboard → Settings, verify:**

✅ **Root Directory:** `apps/otto`  
✅ **Runtime:** `Docker` (preferred) OR `Python` (if using Option 2)  
✅ **Auto-Deploy:** `ON`

---

## 📋 Why This Happened

Render defaults to **Python runtime** when it detects a Python project. For monorepos, you MUST set:
- **Root Directory** to `apps/otto` (so it knows where to look)
- **OR** use **Docker runtime** (which uses the Dockerfile)

Since we have a Dockerfile, **Option 1 (Docker)** is the easiest fix.

---

## ✅ After Fix

Once you change to Docker runtime (or set Root Directory correctly), the build should succeed and you'll see:

```
==> Building Docker image...
==> Build succeeded
==> Service is live at https://otto-xxxxx.onrender.com
```

Test with:
```bash
curl https://your-otto-url.onrender.com/health
```

