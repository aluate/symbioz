# Create .env file for Otto
# Run this script: .\infra\create-env.ps1

$envContent = @"
# Otto - Environment Variables
# DO NOT COMMIT .env to Git! (It's already in .gitignore)

# ============================================
# Required for Diagnostics
# ============================================

# Render API Key
RENDER_API_KEY=rnd_U4lNyfnWzhOTrutyajQ4YiPkrjIp

# GitHub Personal Access Token
# Get from: GitHub → Settings → Developer Settings → Personal Access Tokens
GITHUB_TOKEN=your_github_token_here

# Stripe Secret Key (TEST MODE ONLY)
# Get from: Stripe Dashboard → Developers → API Keys (toggle to TEST mode)
STRIPE_SECRET_KEY=sk_test_your_stripe_test_key_here

# ============================================
# Required for Supabase
# ============================================

# Supabase Project URL
# Get from: Supabase Dashboard → Settings → API → Project URL
SUPABASE_URL=https://your-project-ref.supabase.co

# Supabase Service Role Key (for backend/admin operations)
# Get from: Supabase Dashboard → Settings → API → service_role key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key_here

# Supabase Anon Key (optional, if using anon access)
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Supabase JWT Secret (for backend auth verification)
# Get from: Supabase Dashboard → Settings → API → JWT Secret
SUPABASE_JWT_SECRET=your_jwt_secret_here

# ============================================
# Optional: For Provisioning/Deployment
# ============================================

# Vercel Token (only if using Vercel)
VERCEL_TOKEN=your_vercel_token_here

# App-specific environment variables
NEXT_PUBLIC_API_BASE_URL=https://catered-by-me-api.onrender.com
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
"@

$envPath = ".env"

if (Test-Path $envPath) {
    Write-Host "Warning: .env file already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/N)"
    if ($overwrite -ne "y" -and $overwrite -ne "Y") {
        Write-Host "Cancelled. Existing .env file unchanged." -ForegroundColor Yellow
        exit
    }
}

$envContent | Out-File -FilePath $envPath -Encoding UTF8 -NoNewline

Write-Host "Created .env file!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "   1. Open .env in your editor" -ForegroundColor Gray
Write-Host "   2. Fill in the remaining values (marked as 'your_xxx_here')" -ForegroundColor Gray
Write-Host "   3. See infra/FINDING_YOUR_KEYS_AND_IDS.md for where to get each key" -ForegroundColor Gray
Write-Host ""
Write-Host "Your Render API key is already filled in!" -ForegroundColor Green

