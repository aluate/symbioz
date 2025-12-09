# ============================================
# FRAT DEV MACHINE - Bash Aliases
# ============================================
# Source this file in your ~/.bashrc or ~/.zshrc
# Add: source ~/aliases.sh

# ============================================
# DIRECTORY NAVIGATION
# ============================================
alias dev="cd /mnt/c/dev/_repos"
alias projects="cd /mnt/c/dev/_projects"
alias templates="cd /mnt/c/dev/_templates"
alias repos="cd /mnt/c/dev/_repos"

# WSL Windows path access
alias cdev="cd /mnt/c/dev"
alias cdrive="cd /mnt/c"

# ============================================
# DOCKER ALIASES
# ============================================
alias docker_clean="docker system prune -af"
alias docker_stop="docker stop \$(docker ps -aq)"
alias docker_rm="docker rm \$(docker ps -aq)"
alias docker_images="docker images"
alias docker_ps="docker ps -a"
alias docker_logs="docker logs -f"

# ============================================
# SUPABASE ALIASES
# ============================================
alias supabase_up="supabase start"
alias supabase_down="supabase stop"
alias supabase_reset="supabase db reset"
alias supabase_status="supabase status"

# ============================================
# GIT ALIASES
# ============================================
alias gs="git status"
alias ga="git add"
alias gc="git commit"
alias gp="git push"
alias gl="git pull"
alias gd="git diff"
alias gb="git branch"
alias gco="git checkout"
alias glog="git log --oneline --graph --decorate"

# ============================================
# NODE/NPM ALIASES
# ============================================
alias ni="npm install"
alias nu="npm uninstall"
alias nr="npm run"
alias ns="npm start"
alias nt="npm test"
alias nb="npm run build"

# Yarn
alias yi="yarn install"
alias ya="yarn add"
alias yr="yarn remove"
alias ys="yarn start"
alias yt="yarn test"
alias yb="yarn build"

# pnpm
alias pi="pnpm install"
alias pa="pnpm add"
alias pr="pnpm remove"
alias ps="pnpm start"
alias pt="pnpm test"
alias pb="pnpm build"

# ============================================
# PYTHON ALIASES
# ============================================
alias py="python3"
alias pip="pip3"
alias venv="python3 -m venv"
alias activate="source venv/bin/activate"

# Poetry
alias po="poetry"
alias poa="poetry add"
alias por="poetry remove"
alias poi="poetry install"
alias porun="poetry run"
alias pob="poetry build"

# ============================================
# SYSTEM ALIASES
# ============================================
alias ll="ls -lah"
alias la="ls -la"
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."

# WSL specific
alias win="explorer.exe ."
alias code="code ."

# ============================================
# QUICK PROJECT SETUP
# ============================================
alias nextjs_new="npx create-next-app@latest"
alias react_new="npx create-react-app"
alias fastapi_new="poetry new"

# ============================================
# UTILITY FUNCTIONS
# ============================================

# Quick server start (Python)
serve() {
    python3 -m http.server ${1:-8000}
}

# Find and kill process on port
killport() {
    lsof -ti:$1 | xargs kill -9
}

# Quick git repo clone to dev folder
clone() {
    cd /mnt/c/dev/_repos && git clone $1
}

# Quick project template
newproject() {
    mkdir -p /mnt/c/dev/_projects/$1
    cd /mnt/c/dev/_projects/$1
    git init
    echo "# $1" > README.md
}

# ============================================
# DEPLOYMENT HELPERS
# ============================================
alias vercel_deploy="vercel --prod"
alias vercel_dev="vercel dev"
alias render_deploy="render deploy"

# ============================================
# INFO DISPLAY
# ============================================
alias versions="echo 'Node: $(node --version)' && echo 'Python: $(python3 --version)' && echo 'Git: $(git --version)' && echo 'Docker: $(docker --version 2>/dev/null || echo N/A)'"

# Show current project info
alias projinfo="echo 'Current directory: $(pwd)' && echo 'Git branch: $(git branch --show-current 2>/dev/null || echo N/A)' && echo 'Node version: $(node --version 2>/dev/null || echo N/A)'"

