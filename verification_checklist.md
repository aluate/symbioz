# 🔍 DEV MACHINE VERIFICATION CHECKLIST

Run these tests after completing both Windows and WSL setup to verify everything is working correctly.

## ✅ Prerequisites Check

### Windows Verification

```powershell
# 1. Check WSL
wsl --version
wsl --list --verbose

# 2. Check Git
git --version
git config --global --list

# 3. Check GitHub CLI
gh --version
gh auth status

# 4. Check Docker Desktop
docker --version
docker info

# 5. Check VS Code
code --version
```

### WSL Verification

```bash
# Enter WSL
wsl

# 1. Check Node.js
node --version
npm --version
nvm --version

# 2. Check Python
python3 --version
pip3 --version
poetry --version

# 3. Check Package Managers
yarn --version
pnpm --version
# bun --version (if installed)

# 4. Check Git
git --version
git config --global --list

# 5. Check Docker
docker --version
docker info

# 6. Check CLIs
supabase --version
vercel --version
render --version
gh --version
```

---

## 🧪 Functional Tests

### Test 1: Node.js Environment

```bash
# In WSL
node -e "console.log('Node.js works!')"
npm --version
nvm list
```

**Expected:** Node LTS version installed, npm working, nvm shows installed versions.

---

### Test 2: Python Environment

```bash
# In WSL
python3 -c "import sys; print(f'Python {sys.version}')"
pip3 --version
poetry --version
```

**Expected:** Python 3.11+, pip working, Poetry installed.

---

### Test 3: Docker Integration

```bash
# In WSL
docker run hello-world
```

**Expected:** Docker pulls and runs hello-world container successfully.

**Troubleshooting:**
- If Docker daemon not found, ensure Docker Desktop is running on Windows
- Check Docker Desktop settings: Settings > Resources > WSL Integration > Enable integration with Ubuntu

---

### Test 4: GitHub SSH Authentication

```bash
# In WSL
ssh -T git@github.com
```

**Expected:** "Hi [username]! You've successfully authenticated..."

**Troubleshooting:**
- If "Permission denied", check SSH key exists: `ls -la ~/.ssh/id_ed25519`
- Add SSH key to GitHub: `cat ~/.ssh/id_ed25519.pub` and add to GitHub Settings > SSH Keys
- Test SSH agent: `eval "$(ssh-agent -s)"` then `ssh-add ~/.ssh/id_ed25519`

---

### Test 5: GitHub CLI Authentication

```bash
# In WSL or Windows
gh auth status
```

**Expected:** Logged in as [username]

**If not logged in:**
```bash
gh auth login
```

---

### Test 6: Build Next.js App

```bash
# In WSL
cd /mnt/c/dev/_projects
npx create-next-app@latest test-nextjs --typescript --tailwind --app --no-src-dir --import-alias "@/*"
cd test-nextjs
npm run build
```

**Expected:** Next.js app builds successfully without errors.

**Cleanup:**
```bash
cd /mnt/c/dev/_projects
rm -rf test-nextjs
```

---

### Test 7: Build FastAPI App

```bash
# In WSL
cd /mnt/c/dev/_projects
poetry new test-fastapi
cd test-fastapi
poetry add fastapi uvicorn
poetry run python -c "import fastapi; print('FastAPI works!')"
```

**Expected:** FastAPI installs and imports successfully.

**Cleanup:**
```bash
cd /mnt/c/dev/_projects
rm -rf test-fastapi
```

---

### Test 8: Vercel Deployment Test

```bash
# In WSL
cd /mnt/c/dev/_projects
npx create-next-app@latest test-vercel --typescript --tailwind --app
cd test-vercel
vercel login
vercel --prod
```

**Expected:** Vercel CLI authenticates and deploys (or prompts for setup).

**Note:** This creates a real deployment. Cancel if you don't want it.

---

### Test 9: Supabase Local Development

```bash
# In WSL
cd /mnt/c/dev/_projects
mkdir test-supabase && cd test-supabase
supabase init
supabase start
```

**Expected:** Supabase initializes and starts local services.

**Cleanup:**
```bash
supabase stop
cd /mnt/c/dev/_projects
rm -rf test-supabase
```

---

### Test 10: Git Repository Clone

```bash
# In WSL
cd /mnt/c/dev/_repos
git clone https://github.com/vercel/next.js.git test-clone
cd test-clone
git status
```

**Expected:** Repository clones successfully, git status shows clean working tree.

**Cleanup:**
```bash
cd /mnt/c/dev/_repos
rm -rf test-clone
```

---

## 🔧 System Health Checks

### WSL Kernel Version

```bash
# In WSL
uname -r
```

**Expected:** Kernel version 5.10+ (WSL2)

---

### Disk Space

```bash
# In WSL
df -h
```

**Expected:** Sufficient space on /mnt/c (Windows drive)

---

### Memory

```bash
# In WSL
free -h
```

**Expected:** Adequate memory available

---

### Network Connectivity

```bash
# In WSL
ping -c 3 google.com
curl -I https://github.com
```

**Expected:** Both commands succeed

---

## 📊 Performance Benchmarks (Optional)

### Node.js Performance

```bash
# In WSL
time node -e "console.log('test')"
```

### Docker Performance

```bash
# In WSL
time docker run hello-world
```

---

## 🚨 Common Issues & Solutions

### Issue: Docker daemon not found in WSL

**Solution:**
1. Open Docker Desktop on Windows
2. Settings > Resources > WSL Integration
3. Enable integration with your Ubuntu distribution
4. Restart WSL: `wsl --shutdown` then reopen

---

### Issue: Node version not persisting in WSL

**Solution:**
Add to `~/.bashrc`:
```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

---

### Issue: Poetry not found after installation

**Solution:**
Add to `~/.bashrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then: `source ~/.bashrc`

---

### Issue: VS Code Remote-WSL not working

**Solution:**
1. Install "Remote - WSL" extension in VS Code
2. Open WSL terminal: `code .`
3. Or use: `code --remote wsl+Ubuntu`

---

### Issue: Git credentials not working in WSL

**Solution:**
Use SSH keys instead of HTTPS, or configure Git Credential Manager:
```bash
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
```

---

## ✅ Final Checklist

- [ ] All version checks pass
- [ ] Docker hello-world runs
- [ ] GitHub SSH authentication works
- [ ] GitHub CLI authenticated
- [ ] Next.js app builds successfully
- [ ] FastAPI imports work
- [ ] Vercel CLI responds
- [ ] Supabase CLI works
- [ ] Git clone works
- [ ] Dev folders exist and are accessible
- [ ] Aliases loaded in shell
- [ ] VS Code can open WSL folders

---

## 🎉 Success Criteria

If all tests pass, your dev machine is **READY FOR FRAT OPS**! 🚀

---

## 📝 Notes

- Keep this checklist for future reference
- Re-run tests after major system updates
- Document any custom configurations you make
- Share issues with the team for troubleshooting

---

**Last Updated:** $(date)
**Setup Version:** 1.0

