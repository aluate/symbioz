# 🚀 START HERE - Get SMB Site Live

**You're ~95% ready! Follow these steps to go live in ~20 minutes.**

---

## ⚡ **Quick Start (5 Steps)**

### **1. Run Git Setup** (~2 min)
```powershell
.\vlg\apps\smb_site\DEPLOY_NOW.ps1
```

### **2. Create GitHub Repo** (~3 min)
```bash
python tools/infra.py create-github-repo --name smb
```

### **3. Push Code** (~2 min)
```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/smb.git
git push -u origin main
```

### **4. Deploy to Vercel** (~5 min, Automated!)
```bash
python tools/infra.py setup-vercel-project \
  --project smb \
  --repo YOUR_USERNAME/smb \
  --root-dir vlg/apps/smb_site
```

**🎉 Site goes live immediately on Vercel URL!**

### **5. Configure Domain** (~5 min, Mostly Automated!)
```bash
python tools/infra.py configure-domain \
  --project smb \
  --domain sugarmountainbuilders.com
```

Then add DNS records in Wix.

---

## 📋 **What You Need**

- ✅ Git configured (script checks this)
- ✅ GitHub account
- ✅ GitHub token in `.env` (for Otto)
- ✅ Vercel token in `.env` (for Otto)

---

## ⏱️ **Timeline**

**Active work:** ~20 minutes  
**Site live:** Immediately after Step 4  
**Domain works:** After DNS propagates (24-48 hours)

---

## 📖 **Detailed Guides**

- `STEP_BY_STEP_DEPLOY.md` - Complete step-by-step
- `COMPLETE_DEPLOYMENT_GUIDE.md` - Full reference
- `DEPLOY_NOW.ps1` - Git setup script

---

## ✅ **Ready to Start?**

**Run Step 1 now:**
```powershell
.\vlg\apps\smb_site\DEPLOY_NOW.ps1
```

**Then follow the steps above!** 🚀

