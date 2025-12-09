# Complete Deployment Guide - Get SMB Site Live

**Status: ~95% ready! Just need git setup and push.**

---

## 🎯 **Quick Answer**

**Can I push?** Not directly (not a git repo yet), but I can help set it up!  
**How close?** ~95% - Just need git/GitHub setup, then Otto deploys it.

**Time to live:** ~20 minutes of active work!

---

## 🚀 **Complete Deployment Steps**

### **Step 1: Initialize Git** (~2 minutes)

**Option A: Use Script** (I'll create this)
```powershell
.\vlg\apps\smb_site\INIT_GIT_AND_DEPLOY.ps1
```

**Option B: Manual**
```powershell
cd "C:\Users\small\My Drive"
git init
git add .
git commit -m "Initial commit: SMB website complete"
```

---

### **Step 2: Create GitHub Repository** (~3 minutes)

**Option A: Via Otto (Automated!)**
```bash
python tools/infra.py create-github-repo \
  --name smb \
  --description "Sugar Mountain Builders website"
```

**Option B: Via Web**
1. Go to https://github.com/new
2. Repository name: `smb`
3. Click "Create repository"

---

### **Step 3: Push to GitHub** (~2 minutes)

```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/smb.git
git push -u origin main
```

---

### **Step 4: Deploy to Vercel** (~5 minutes, Automated!)

```bash
python tools/infra.py setup-vercel-project \
  --project smb \
  --repo YOUR_USERNAME/smb \
  --root-dir vlg/apps/smb_site
```

**What this does:**
- Creates Vercel project
- Connects GitHub repo
- Triggers deployment
- **Site goes live immediately on Vercel URL!**

---

### **Step 5: Configure Domain** (~5 minutes, Mostly Automated)

```bash
python tools/infra.py configure-domain \
  --project smb \
  --domain sugarmountainbuilders.com
```

**What this does:**
- Adds domain to Vercel
- Gets DNS records
- Shows you what to add in Wix

**Then you:**
- Log into Wix
- Add DNS records (~5 minutes)

**Wait:** DNS propagation (24-48 hours, passive)

---

## ⏱️ **Time Breakdown**

**Active work:** ~20 minutes
- Git setup: ~5 min
- Push to GitHub: ~5 min
- Otto deploy: ~5 min (automated)
- Domain DNS: ~5 min

**Passive wait:** 24-48 hours (DNS propagation)

**Site works immediately** on Vercel URL after Step 4!

---

## ✅ **What's Ready**

- ✅ Complete website code
- ✅ Automation commands
- ✅ Otto deployment ready
- ✅ All components working

---

## 📋 **Commands Ready to Run**

I've added to Otto:
1. ✅ `create-github-repo` - Create GitHub repository
2. ✅ `setup-vercel-project` - Deploy to Vercel
3. ✅ `configure-domain` - Configure custom domain
4. ✅ `verify-deployment` - Check everything works

---

**Ready to go live in ~20 minutes!** 🚀

