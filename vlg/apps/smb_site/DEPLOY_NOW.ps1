# Deploy SMB Site - Complete Script
# Run this from: "C:\Users\small\My Drive"

Write-Host "🚀 Deploying Sugar Mountain Builders Website" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Git Configuration
Write-Host "Step 1: Checking Git configuration..." -ForegroundColor Yellow
$gitName = git config --global user.name
$gitEmail = git config --global user.email

if (-not $gitName -or -not $gitEmail) {
    Write-Host "❌ Git is not configured!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run these commands first:" -ForegroundColor Yellow
    Write-Host '   git config --global user.name "Your Name"' -ForegroundColor Gray
    Write-Host '   git config --global user.email "your.email@example.com"' -ForegroundColor Gray
    Write-Host ""
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git configured: $gitName <$gitEmail>" -ForegroundColor Green
Write-Host ""

# Step 2: Initialize Git Repository
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

# Step 3: Create .gitignore if needed
Write-Host ""
Write-Host "Step 3: Ensuring .gitignore exists..." -ForegroundColor Yellow

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
$status = git status --porcelain

if ($status) {
    Write-Host "📋 Files ready to commit:" -ForegroundColor Green
    git status --short
    Write-Host ""
    
    # Ask if user wants to commit now
    $response = Read-Host "Do you want to commit these files now? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        git add .
        git commit -m "Initial commit: SMB website complete with Floor Plans page and automation"
        Write-Host "✅ Files committed!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Skipping commit. You can commit later with:" -ForegroundColor Yellow
        Write-Host "   git add ." -ForegroundColor Gray
        Write-Host '   git commit -m "Initial commit: SMB website"' -ForegroundColor Gray
    }
} else {
    Write-Host "✅ Everything is already committed" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ Git setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create GitHub repository:" -ForegroundColor Cyan
Write-Host "   Option A (Automated):" -ForegroundColor Gray
Write-Host "   python tools/infra.py create-github-repo --name smb" -ForegroundColor White
Write-Host ""
Write-Host "   Option B (Manual):" -ForegroundColor Gray
Write-Host "   Go to: https://github.com/new" -ForegroundColor White
Write-Host "   Create repo: smb" -ForegroundColor White
Write-Host ""
Write-Host "2. Push code to GitHub:" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/smb.git" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "3. Deploy to Vercel (Automated!):" -ForegroundColor Cyan
Write-Host "   python tools/infra.py setup-vercel-project --project smb --repo YOUR_USERNAME/smb --root-dir vlg/apps/smb_site" -ForegroundColor White
Write-Host ""
Write-Host "4. Configure domain (Mostly Automated!):" -ForegroundColor Cyan
Write-Host "   python tools/infra.py configure-domain --project smb --domain sugarmountainbuilders.com" -ForegroundColor White
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan

