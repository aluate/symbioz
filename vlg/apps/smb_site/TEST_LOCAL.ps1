# Quick Local Test Script for SMB Site
# Run this to set up and test the site locally

Write-Host "🚀 Testing SMB Site Locally" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""

# Change to site directory
$siteDir = "C:\Users\small\My Drive\vlg\apps\smb_site"
Set-Location $siteDir

Write-Host "📁 Current directory: $siteDir" -ForegroundColor Green
Write-Host ""

# Check if Node.js is installed
Write-Host "Step 1: Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Node.js from: https://nodejs.org/" -ForegroundColor Yellow
    Write-Host "Download the LTS version and install it, then run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if npm is installed
Write-Host "Step 2: Checking npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✅ npm installed: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found!" -ForegroundColor Red
    Write-Host "npm should come with Node.js. Please reinstall Node.js." -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if node_modules exists
Write-Host "Step 3: Checking dependencies..." -ForegroundColor Yellow
if (Test-Path "node_modules") {
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Dependencies not installed. Installing now..." -ForegroundColor Yellow
    Write-Host "This may take a few minutes..." -ForegroundColor Gray
    Write-Host ""
    
    npm install
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
        Write-Host "Please check the error messages above." -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host ""
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
}

Write-Host ""

# Check if .next exists (previous build)
Write-Host "Step 4: Checking for previous build..." -ForegroundColor Yellow
if (Test-Path ".next") {
    Write-Host "⚠️  Previous build found. You can keep it or delete it." -ForegroundColor Yellow
    Write-Host "   (It will be regenerated when you run 'npm run dev')" -ForegroundColor Gray
} else {
    Write-Host "✅ No previous build (this is fine for first run)" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Starting development server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Instructions:" -ForegroundColor Yellow
Write-Host "   1. The server will start on http://localhost:3000" -ForegroundColor Gray
Write-Host "   2. Your browser should open automatically" -ForegroundColor Gray
Write-Host "   3. Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""
Write-Host "⏳ Starting in 3 seconds..." -ForegroundColor Gray
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "🔗 Opening browser..." -ForegroundColor Cyan
Start-Process "http://localhost:3000"

# Start the dev server
Write-Host ""
Write-Host "Starting Next.js development server..." -ForegroundColor Cyan
Write-Host ""
npm run dev

