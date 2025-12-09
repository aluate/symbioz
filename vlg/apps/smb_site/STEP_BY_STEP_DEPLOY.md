# Step-by-Step: Get SMB Site Live in 20 Minutes

**Follow these steps in order. Most are automated!**

---

## ✅ **Step 1: Run Git Setup Script** (~2 minutes)

```powershell
.\vlg\apps\smb_site\DEPLOY_NOW.ps1
```

**What this does:**
- Checks git configuration
- Initializes git repository
- Creates .gitignore
- Shows what needs to be committed
- Offers to commit files

**If git isn't configured:**
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Then run the script again.

---

## ✅ **Step 2: Create GitHub Repository** (~3 minutes)

### **Option A: Via Otto (Automated!)** ⭐ Recommended

```bash
python tools/infra.py create-github-repo \
  --name smb \
  --description "Sugar Mountain Builders website"
```

**What this does:**
- Creates GitHub repository automatically
- Shows you the repo URL
- Ready to push!

### **Option B: Via Web (Manual)**

1. Go to: https://github.com/new
2. Repository name: `smb`
3. Description: "Sugar Mountain Builders website"
4. Choose Public or Private
5. **Don't** initialize with README
6. Click "Create repository"

---

## ✅ **Step 3: Push Code to GitHub** (~2 minutes)

**Replace `YOUR_USERNAME` with your GitHub username:**

```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/smb.git
git push -u origin main
```

**If you see authentication prompt:**
- Use your GitHub username
- Use a Personal Access Token (not password)
- Get token from: https://github.com/settings/tokens

**Verify it worked:**
- Go to: https://github.com/YOUR_USERNAME/smb
- You should see all your files!

---

## ✅ **Step 4: Deploy to Vercel** (~5 minutes, Automated!)

**Replace `YOUR_USERNAME` with your GitHub username:**

```bash
python tools/infra.py setup-vercel-project \
  --project smb \
  --repo YOUR_USERNAME/smb \
  --root-dir vlg/apps/smb_site
```

**What this does:**
- Creates Vercel project
- Connects GitHub repository
- Sets root directory
- Triggers deployment
- **Site goes live immediately!**

**You'll get:**
- Vercel deployment URL (e.g., `https://smb.vercel.app`)
- Site is live and working!

---

## ✅ **Step 5: Configure Domain** (~5 minutes, Mostly Automated!)

```bash
python tools/infra.py configure-domain \
  --project smb \
  --domain sugarmountainbuilders.com
```

**What this does:**
- Adds domain to Vercel
- Gets DNS configuration
- Shows DNS records you need

**Then you:**
1. Log into Wix domain management
2. Add the DNS records shown
3. Wait 24-48 hours for DNS propagation

**Site works on Vercel URL immediately!** Domain works after DNS propagates.

---

## ✅ **Step 6: Verify Everything** (Optional)

```bash
python tools/infra.py verify-deployment \
  --project smb \
  --domain sugarmountainbuilders.com
```

**What this does:**
- Checks deployment status
- Verifies domain configuration
- Tests website accessibility

---

## ⏱️ **Time Breakdown**

- **Step 1:** ~2 minutes (script)
- **Step 2:** ~3 minutes (Otto or web)
- **Step 3:** ~2 minutes (push)
- **Step 4:** ~5 minutes (Otto automates)
- **Step 5:** ~5 minutes (Otto automates mostly)
- **Step 6:** ~1 minute (optional)

**Total: ~20 minutes of active work!**

**Then:**
- ✅ Site works immediately on Vercel URL
- ✅ Domain works after DNS propagates (24-48 hours)

---

## 🎯 **Quick Reference**

**All commands in one place:**

```powershell
# 1. Git setup
.\vlg\apps\smb_site\DEPLOY_NOW.ps1

# 2. Create GitHub repo (automated)
python tools/infra.py create-github-repo --name smb

# 3. Push code
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/smb.git
git push -u origin main

# 4. Deploy to Vercel (automated)
python tools/infra.py setup-vercel-project --project smb --repo YOUR_USERNAME/smb --root-dir vlg/apps/smb_site

# 5. Configure domain (mostly automated)
python tools/infra.py configure-domain --project smb --domain sugarmountainbuilders.com

# 6. Verify (optional)
python tools/infra.py verify-deployment --project smb --domain sugarmountainbuilders.com
```

---

## 🚀 **You're Ready!**

**Follow the steps above and your site will be live in ~20 minutes!**

**Need help?** Check:
- `DEPLOY_NOW.ps1` - Git setup script
- `COMPLETE_DEPLOYMENT_GUIDE.md` - Detailed guide
- `HOW_CLOSE_TO_LIVE.md` - Status overview

---

**Let's get this site live!** 🎉

