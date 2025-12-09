# Setting Up Your .env File

## ✅ Your Render API Key

I've got your Render API key: `rnd_U4lNyfnWzhOTrutyajQ4YiPkrjIp`

---

## 🚀 Quick Setup (Choose One Method)

### Method 1: Use PowerShell Script (Easiest!)

Run this command:

```powershell
.\infra\create-env.ps1
```

This will create your `.env` file with your Render API key already filled in!

---

### Method 2: Create Manually

1. Create a new file called `.env` in your repo root (`C:\Users\small\My Drive\.env`)

2. Copy and paste this content:

```env
# Otto - Environment Variables
# DO NOT COMMIT .env to Git!

# Render API Key
RENDER_API_KEY=rnd_U4lNyfnWzhOTrutyajQ4YiPkrjIp

# GitHub Personal Access Token
GITHUB_TOKEN=your_github_token_here

# Stripe Secret Key (TEST MODE ONLY)
STRIPE_SECRET_KEY=sk_test_your_stripe_test_key_here

# Supabase Project URL
SUPABASE_URL=https://your-project-ref.supabase.co

# Supabase Service Role Key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key_here

# Supabase Anon Key (optional)
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Supabase JWT Secret
SUPABASE_JWT_SECRET=your_jwt_secret_here

# Vercel Token (optional, only if using Vercel)
VERCEL_TOKEN=your_vercel_token_here

# App-specific
NEXT_PUBLIC_API_BASE_URL=https://catered-by-me-api.onrender.com
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
```

3. Save the file

---

## 📝 Next Steps

After creating your `.env` file:

1. **Fill in the remaining values** (replace all `your_xxx_here` placeholders)
2. **See `infra/FINDING_YOUR_KEYS_AND_IDS.md`** for detailed instructions on where to get each key
3. **Verify `.env` is in `.gitignore`** (it already is! ✅)

---

## ✅ What's Already Done

- ✅ Render API key is filled in: `rnd_U4lNyfnWzhOTrutyajQ4YiPkrjIp`
- ✅ `.env` is already in `.gitignore` (safe from git commits)

---

## 🔒 Security Reminder

- ✅ Never commit `.env` to git (already protected)
- ✅ Never share your API keys publicly
- ✅ Keep your `.env` file secure

---

**Once your `.env` file is created and filled in, you'll be ready to test Otto!**

