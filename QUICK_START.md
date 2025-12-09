# ⚡ QUICK START GUIDE

**Get your dev machine running in 5 minutes.**

## 🚀 Fast Track Setup

### 1. Run Windows Setup (2 minutes)

```powershell
# Open PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1 -GitName "Your Name" -GitEmail "your@email.com"
```

**If WSL was installed:** Restart your computer.

### 2. Run WSL Setup (3 minutes)

```bash
# Open WSL (Ubuntu)
chmod +x setup_wsl.sh
bash setup_wsl.sh
```

Answer prompts:
- Install Bun? (optional, type `n` to skip)
- Set Git name/email (if not set in Windows)

### 3. Verify (30 seconds)

```bash
# Quick test
node --version
python3 --version
docker run hello-world
```

If all three work, **you're done!** 🎉

---

## 📋 What Just Happened?

✅ Created `C:\dev\_projects`, `_templates`, `_repos`  
✅ Installed WSL2 Ubuntu  
✅ Installed Git, GitHub CLI, VS Code, Docker Desktop  
✅ Configured Node.js, Python, Docker, Supabase, Vercel CLIs  
✅ Set up SSH keys  
✅ Created dev folder structure  

---

## 🎯 Next Steps

1. **Load aliases:**
   ```bash
   echo "source ~/aliases.sh" >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Test GitHub SSH:**
   ```bash
   ssh -T git@github.com
   ```

3. **Authenticate GitHub CLI:**
   ```bash
   gh auth login
   ```

4. **Start coding:**
   ```bash
   dev  # Go to repos folder
   ```

---

## 🆘 Something Broke?

See `verification_checklist.md` for troubleshooting.

---

**That's it! Welcome to FRAT OPS.** 🚀

