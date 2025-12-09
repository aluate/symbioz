#!/bin/bash
# ============================================
# DEV MACHINE BOOTSTRAP - WSL Ubuntu
# ============================================
# Run this inside WSL after Windows setup completes
# Usage: bash setup_wsl.sh

set -e

echo "🚀 FRAT DEV MACHINE SETUP - WSL Ubuntu"
echo "======================================"

# ============================================
# 1. UPDATE SYSTEM
# ============================================
echo ""
echo "📦 Updating system packages..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

# ============================================
# 2. INSTALL ESSENTIAL BUILD TOOLS
# ============================================
echo ""
echo "🛠️  Installing build essentials..."
sudo apt-get install -y -qq \
    build-essential \
    curl \
    wget \
    git \
    zip \
    unzip \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common \
    apt-transport-https

# ============================================
# 3. INSTALL NODE VIA NVM
# ============================================
echo ""
echo "📦 Installing Node.js via nvm..."

if [ ! -d "$HOME/.nvm" ]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    echo "  ✓ nvm installed"
else
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    echo "  ✓ nvm already installed"
fi

# Install Node LTS
nvm install --lts
nvm use --lts
nvm alias default node
echo "  ✓ Node.js $(node --version) installed"

# ============================================
# 4. INSTALL PACKAGE MANAGERS
# ============================================
echo ""
echo "📦 Installing package managers..."

# Yarn
if ! command -v yarn &> /dev/null; then
    npm install -g yarn
    echo "  ✓ Yarn installed"
else
    echo "  ✓ Yarn already installed"
fi

# pnpm
if ! command -v pnpm &> /dev/null; then
    npm install -g pnpm
    echo "  ✓ pnpm installed"
else
    echo "  ✓ pnpm already installed"
fi

# Bun (optional)
read -p "  Install Bun? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if ! command -v bun &> /dev/null; then
        curl -fsSL https://bun.sh/install | bash
        echo "  ✓ Bun installed"
    else
        echo "  ✓ Bun already installed"
    fi
fi

# ============================================
# 5. INSTALL PYTHON 3.11+
# ============================================
echo ""
echo "🐍 Installing Python 3.11+..."

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
if [ "$(printf '%s\n' "3.11" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.11" ]; then
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get update -qq
    sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip
    echo "  ✓ Python 3.11+ installed"
else
    sudo apt-get install -y python3-venv python3-dev python3-pip
    echo "  ✓ Python $(python3 --version) already installed"
fi

# ============================================
# 6. INSTALL POETRY
# ============================================
echo ""
echo "📚 Installing Poetry..."

if ! command -v poetry &> /dev/null; then
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
    echo "  ✓ Poetry installed"
else
    echo "  ✓ Poetry already installed"
fi

# Add Poetry to PATH permanently
if ! grep -q ".local/bin" ~/.bashrc; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

# ============================================
# 7. INSTALL DOCKER CLIENT
# ============================================
echo ""
echo "🐳 Setting up Docker client..."

# Note: Docker Desktop on Windows handles the daemon
# We just need the client tools in WSL
if ! command -v docker &> /dev/null; then
    # Add Docker's official GPG key
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    
    # Add Docker repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    sudo apt-get update -qq
    sudo apt-get install -y docker-ce-cli docker-compose-plugin
    echo "  ✓ Docker client installed"
else
    echo "  ✓ Docker client already installed"
fi

# ============================================
# 8. INSTALL SUPABASE CLI
# ============================================
echo ""
echo "🗄️  Installing Supabase CLI..."

if ! command -v supabase &> /dev/null; then
    curl -fsSL https://supabase.com/install.sh | sh
    echo "  ✓ Supabase CLI installed"
else
    echo "  ✓ Supabase CLI already installed"
fi

# ============================================
# 9. INSTALL VERCEL CLI
# ============================================
echo ""
echo "▲ Installing Vercel CLI..."

if ! command -v vercel &> /dev/null; then
    npm install -g vercel
    echo "  ✓ Vercel CLI installed"
else
    echo "  ✓ Vercel CLI already installed"
fi

# ============================================
# 10. INSTALL RENDER CLI
# ============================================
echo ""
echo "🎨 Installing Render CLI..."

if ! command -v render &> /dev/null; then
    curl -fsSL https://render.com/install.sh | sh
    echo "  ✓ Render CLI installed"
else
    echo "  ✓ Render CLI already installed"
fi

# ============================================
# 11. CONFIGURE GIT (if not done in Windows)
# ============================================
echo ""
echo "🔧 Configuring Git..."

read -p "  Set Git user.name? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "  Enter your name: " git_name
    git config --global user.name "$git_name"
fi

read -p "  Set Git user.email? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "  Enter your email: " git_email
    git config --global user.email "$git_email"
fi

git config --global init.defaultBranch main
git config --global core.autocrlf input
echo "  ✓ Git configured"

# ============================================
# 12. SET UP SSH KEYS (if not done in Windows)
# ============================================
echo ""
echo "🔐 Setting up SSH keys..."

if [ ! -f ~/.ssh/id_ed25519 ]; then
    read -p "  Generate SSH key? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "  Enter email for SSH key: " ssh_email
        ssh-keygen -t ed25519 -C "$ssh_email" -f ~/.ssh/id_ed25519 -N ""
        echo "  ✓ SSH key generated"
        echo "  📋 Add this public key to GitHub:"
        cat ~/.ssh/id_ed25519.pub
    fi
else
    echo "  ✓ SSH key already exists"
fi

# ============================================
# 13. CREATE DEV DIRECTORIES IN WSL
# ============================================
echo ""
echo "📁 Creating dev directories..."

mkdir -p ~/dev/_projects
mkdir -p ~/dev/_templates
mkdir -p ~/dev/_repos
echo "  ✓ Dev directories created"

# ============================================
# 14. INSTALL VS CODE EXTENSIONS (if code command available)
# ============================================
echo ""
echo "🔌 Installing VS Code extensions..."

if command -v code &> /dev/null; then
    extensions=(
        "esbenp.prettier-vscode"
        "dbaeumer.vscode-eslint"
        "ms-python.python"
        "ms-azuretools.vscode-docker"
        "ms-vscode-remote.remote-wsl"
        "withastro.astro-vscode"
        "Prisma.prisma"
        "bradlc.vscode-tailwindcss"
    )
    
    for ext in "${extensions[@]}"; do
        code --install-extension "$ext" --force 2>&1 | grep -v "already installed" || true
    done
    echo "  ✓ VS Code extensions installed"
else
    echo "  ⚠️  VS Code 'code' command not found. Install Remote-WSL extension manually."
fi

# ============================================
# 15. CREATE ALIASES
# ============================================
echo ""
echo "📝 Setting up aliases..."

if [ ! -f ~/.bash_aliases ]; then
    touch ~/.bash_aliases
fi

# Source aliases file
if [ -f ~/aliases.sh ]; then
    echo "source ~/aliases.sh" >> ~/.bash_aliases
    echo "  ✓ Aliases configured"
fi

# ============================================
# 16. VERIFICATION
# ============================================
echo ""
echo "✅ WSL setup complete!"
echo ""
echo "📋 Verification checklist:"
echo "  Node: $(node --version 2>/dev/null || echo 'NOT FOUND')"
echo "  npm: $(npm --version 2>/dev/null || echo 'NOT FOUND')"
echo "  Python: $(python3 --version 2>/dev/null || echo 'NOT FOUND')"
echo "  Git: $(git --version 2>/dev/null || echo 'NOT FOUND')"
echo "  Docker: $(docker --version 2>/dev/null || echo 'NOT FOUND')"
echo ""
echo "🎉 Welcome to FRAT OPS!"
echo ""
echo "Next: Run verification_checklist.md tests"

