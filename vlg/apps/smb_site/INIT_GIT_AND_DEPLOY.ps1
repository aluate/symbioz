# Initialize Git and Prepare for Deployment - SMB Site
# Run this script from: "C:\Users\small\My Drive"

Write-Host "🚀 Setting up SMB site for deployment..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if git is configured
Write-Host "Step 1: Checking Git configuration..." -ForegroundColor Yellow
$gitName = git config --global user.name
$gitEmail = git config --global user.email

if (-not $gitName -or -not $gitEmail) {
    Write-Host "⚠️  Git is not configured. Please run:" -ForegroundColor Red
    Write-Host '   git config --global user.name "Your Name"' -ForegroundColor Gray
    Write-Host '   git config --global user.email "your.email@example.com"' -ForegroundColor Gray
    Write-Host ""
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git configured: $gitName <$gitEmail>" -ForegroundColor Green

# Step 2: Initialize git in the root directory
Write-Host ""
Write-Host "Step 2: Initializing git repository..." -ForegroundColor Yellow

$rootDir = "C:\Users\small\My Drive"
Set-Location $rootDir

if (Test-Path ".git") {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
} else {
    Write-Host "Creating new git repository..." -ForegroundColor Gray
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Step 3: Create .gitignore if it doesn't exist
Write-Host ""
Write-Host "Step 3: Ensuring .gitignore is set up..." -ForegroundColor Yellow

$gitignorePath = ".gitignore"
if (-not (Test-Path $gitignorePath)) {
    @"
# Environment files
.env
.env.local
.env*.local

# Dependencies
**/node_modules/
**/.next/
**/out/
**/.pnp/

# Build outputs
**/dist/
**/build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/

# Otto diagnostics (can be regenerated)
diagnostics/raw/
diagnostics/history/
"@ | Out-File -FilePath $gitignorePath -Encoding utf8
    Write-Host "✅ Created .gitignore" -ForegroundColor Green
} else {
    Write-Host "✅ .gitignore already exists" -ForegroundColor Green
}

# Step 4: Check what needs to be committed
Write-Host ""
Write-Host "Step 4: Checking what needs to be committed..." -ForegroundColor Yellow
git status --short

$status = git status --porcelain
if ($status) {
    Write-Host ""
    Write-Host "📋 Files ready to commit!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Review the files above" -ForegroundColor Gray
    Write-Host "2. Create a GitHub repository (if you haven't)" -ForegroundColor Gray
    Write-Host "3. Run:" -ForegroundColor Gray
    Write-Host '   git add .' -ForegroundColor Cyan
    Write-Host '   git commit -m "Initial commit: SMB website complete"' -ForegroundColor Cyan
    Write-Host '   git branch -M main' -ForegroundColor Cyan
    Write-Host '   git remote add origin https://github.com/YOUR_USERNAME/smb.git' -ForegroundColor Cyan
    Write-Host '   git push -u origin main' -ForegroundColor Cyan
    Write-Host ""
    Write-Host "4. Then run Otto to deploy:" -ForegroundColor Yellow
    Write-Host '   python tools/infra.py setup-vercel-project --project smb --repo YOUR_USERNAME/smb --root-dir vlg/apps/smb_site' -ForegroundColor Cyan
} else {
    Write-Host "✅ Everything is already committed" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ready to push to GitHub!" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ Setup complete! Follow the steps above to deploy." -ForegroundColor Green

