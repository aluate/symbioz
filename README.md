# 🚀 FRAT DEV MACHINE SETUP

**Turn this Windows box into a weapon-grade development workstation.**

This setup configures your Windows PC for modern web development with React, Next.js, FastAPI, Supabase, Docker, and cloud deployments—all on a budget with open-source tools.

---

## 📋 What This Setup Includes

### Core Stack
- **WSL2** (Ubuntu) for Linux development environment
- **Node.js** (LTS) via nvm
- **Python 3.11+** with Poetry
- **Docker Desktop** for containerization
- **Git & GitHub CLI** for version control
- **VS Code** with essential extensions

### Package Managers
- npm, yarn, pnpm
- pip, Poetry
- Bun (optional)
- apt (WSL)

### CLI Tools
- Supabase CLI
- Vercel CLI
- Render CLI
- GitHub CLI (gh)

### Development Tools
- Build essentials (gcc, make, etc.)
- Git configuration
- SSH key setup
- Dev folder structure

---

## 🎯 Quick Start

### Step 1: Run Windows Setup

Open PowerShell **as Administrator** and run:

```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run setup
.\setup.ps1
```

**Options:**
```powershell
# Skip WSL installation (if already installed)
.\setup.ps1 -SkipWSL

# Skip Chocolatey
.\setup.ps1 -SkipChoco

# Set Git identity during setup
.\setup.ps1 -GitName "Your Name" -GitEmail "your.email@example.com"
```

### Step 2: Restart (if WSL was installed)

If WSL was installed, **restart your computer**. After restart, WSL will continue setup automatically.

### Step 3: Run WSL Setup

Open WSL (Ubuntu) and run:

```bash
# Make script executable
chmod +x setup_wsl.sh

# Run setup
bash setup_wsl.sh
```

The script will:
- Update system packages
- Install Node.js, Python, Docker client
- Install package managers (yarn, pnpm, Poetry)
- Install CLI tools (Supabase, Vercel, Render)
- Configure Git and SSH
- Set up dev directories

### Step 4: Verify Installation

Run the verification checklist:

```bash
# In WSL
cat verification_checklist.md
```

Follow the tests in `verification_checklist.md` to ensure everything works.

### Step 5: Load Aliases

Add aliases to your shell:

```bash
# Add to ~/.bashrc
echo "source ~/aliases.sh" >> ~/.bashrc
source ~/.bashrc
```

---

## 📁 Folder Structure

After setup, you'll have:

```
C:\dev\
├── _projects\     # Your active projects
├── _templates\    # Project templates
└── _repos\        # Cloned repositories
```

In WSL, these are accessible at:
```
/mnt/c/dev/_projects
/mnt/c/dev/_templates
/mnt/c/dev/_repos
```

---

## 🔧 Configuration

### Git Identity

If not set during setup:

```bash
# In WSL or Windows
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### SSH Keys

SSH keys are generated automatically. Add your public key to GitHub:

```bash
# In WSL
cat ~/.ssh/id_ed25519.pub
```

Copy the output and add it to: GitHub Settings > SSH and GPG keys > New SSH key

### GitHub CLI Authentication

```bash
gh auth login
```

Follow the prompts to authenticate.

---

## 🐳 Docker Setup

Docker Desktop must be running on Windows for WSL to access Docker.

1. Open Docker Desktop
2. Settings > Resources > WSL Integration
3. Enable integration with your Ubuntu distribution
4. Restart WSL: `wsl --shutdown` then reopen

Test Docker:
```bash
docker run hello-world
```

---

## 🎨 VS Code Extensions

The setup installs these extensions automatically:
- Prettier
- ESLint
- Python
- Docker
- Remote-WSL
- Astro
- Prisma
- Tailwind CSS IntelliSense

To install manually:
```bash
code --install-extension <extension-id>
```

---

## 🚀 Quick Commands

### Navigation
```bash
dev        # Go to repos folder
projects   # Go to projects folder
templates  # Go to templates folder
```

### Docker
```bash
docker_clean  # Clean up Docker system
docker_stop   # Stop all containers
```

### Supabase
```bash
supabase_up    # Start Supabase locally
supabase_down  # Stop Supabase
```

### Git
```bash
gs    # git status
ga    # git add
gc    # git commit
gp    # git push
```

See `aliases.sh` for the full list.

---

## 🔍 Troubleshooting

### WSL Not Starting

```powershell
# Check WSL status
wsl --status

# Restart WSL
wsl --shutdown
wsl
```

### Docker Not Working in WSL

1. Ensure Docker Desktop is running
2. Enable WSL integration in Docker Desktop settings
3. Restart WSL

### Node Version Not Persisting

Add to `~/.bashrc`:
```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

### Poetry Not Found

Add to `~/.bashrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### VS Code Can't Open WSL Folders

Install "Remote - WSL" extension, then:
```bash
code --remote wsl+Ubuntu
```

---

## 📊 System Requirements

- **Windows 10/11** (64-bit)
- **8GB RAM** minimum (16GB recommended)
- **20GB free disk space** minimum
- **Virtualization enabled** in BIOS (for WSL2)

---

## 🎓 Next Steps

1. **Clone a test repository:**
   ```bash
   cd /mnt/c/dev/_repos
   git clone https://github.com/vercel/next.js.git
   ```

2. **Create a new Next.js project:**
   ```bash
   cd /mnt/c/dev/_projects
   npx create-next-app@latest my-app
   ```

3. **Create a FastAPI project:**
   ```bash
   cd /mnt/c/dev/_projects
   poetry new my-api
   cd my-api
   poetry add fastapi uvicorn
   ```

4. **Start Supabase locally:**
   ```bash
   supabase init
   supabase start
   ```

---

## 🔐 Security Notes

- SSH keys are generated with no passphrase by default (for convenience)
- Consider adding a passphrase for production use: `ssh-keygen -p -f ~/.ssh/id_ed25519`
- Windows Defender exceptions are added for `C:\dev` (development only)
- Keep your system updated: `sudo apt update && sudo apt upgrade` (in WSL)

---

## 🛠️ Advanced Configuration

### Performance Tuning

See `OPTIMIZATION.md` (if created) for:
- Pagefile configuration
- Memory compression settings
- Windows Defender exclusions
- Power mode optimization

### CUDA Support (GPU)

If you have an NVIDIA GPU and want CUDA support:
1. Install NVIDIA drivers on Windows
2. Install CUDA toolkit in WSL
3. Configure Docker for GPU support

### Custom Project Templates

Add templates to `C:\dev\_templates\`:
- Next.js starter
- FastAPI starter
- Full-stack template

---

## 📝 Maintenance

### Update All Tools

**Windows:**
```powershell
winget upgrade --all
```

**WSL:**
```bash
sudo apt update && sudo apt upgrade
nvm install --lts
npm update -g
poetry self update
```

### Clean Up

```bash
# Docker cleanup
docker_clean

# npm cache
npm cache clean --force

# Poetry cache
poetry cache clear pypi --all
```

---

## 🐛 Known Issues

- **WSL2 slow file access:** Use WSL filesystem (`~/dev`) instead of `/mnt/c` for active development
- **Docker Desktop memory usage:** Adjust in Settings > Resources
- **Git line endings:** Configured for cross-platform (CRLF on Windows, LF in WSL)

---

## 📚 Resources

- [WSL Documentation](https://docs.microsoft.com/windows/wsl/)
- [Docker Desktop WSL Integration](https://docs.docker.com/desktop/wsl/)
- [Node Version Manager](https://github.com/nvm-sh/nvm)
- [Poetry Documentation](https://python-poetry.org/docs/)

---

## 🎉 Success!

If you've completed all steps and verification tests pass, **your dev machine is ready for FRAT OPS!**

**Welcome to the team. Let's build something awesome.** 🚀

---

## 📞 Support

For issues or questions:
1. Check `verification_checklist.md` for common problems
2. Review troubleshooting section above
3. Check tool-specific documentation

---

**Setup Version:** 1.0  
**Last Updated:** 2024  
**Maintained by:** FRAT OPS

