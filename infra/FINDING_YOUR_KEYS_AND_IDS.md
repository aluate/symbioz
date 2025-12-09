# Finding Your API Keys and IDs - Step by Step Guide

This guide shows you **exactly where to click** to get each value you need for Otto.

---

## 🔑 Required Environment Variables

### 1. Render API Key

**Where to find it:**
1. Go to https://dashboard.render.com
2. Click your **profile icon** (top right)
3. Click **"Account Settings"**
4. Scroll down to **"API Keys"** section
5. Click **"Create API Key"** if you don't have one yet
6. Give it a name like "Otto SRE Bot"
7. Copy the key (it starts with `rnd_...`)
8. **Important:** You can only see it once! Save it immediately.

**Add to `.env`:**
```env
RENDER_API_KEY=rnd_your_key_here
```

---

### 2. GitHub Personal Access Token

**Where to find it:**
1. Go to https://github.com
2. Click your **profile icon** (top right) → **"Settings"**
3. Scroll down to **"Developer settings"** (left sidebar)
4. Click **"Personal access tokens"** → **"Tokens (classic)"**
5. Click **"Generate new token"** → **"Generate new token (classic)"**
6. Give it a name: "Otto SRE Bot"
7. Set expiration (90 days or custom)
8. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (optional, if using org repos)
9. Click **"Generate token"**
10. Copy the token immediately (starts with `ghp_...`)

**Add to `.env`:**
```env
GITHUB_TOKEN=ghp_your_token_here
```

---

### 3. Stripe Secret Key (TEST MODE ONLY!)

**Where to find it:**
1. Go to https://dashboard.stripe.com
2. **CRITICAL:** Make sure you're in **TEST MODE** (toggle in top right should say "Test mode")
3. Click **"Developers"** → **"API keys"**
4. You'll see:
   - **Publishable key** (starts with `pk_test_...`) - for frontend
   - **Secret key** (starts with `sk_test_...`) - for backend
5. Click **"Reveal test key"** next to Secret key
6. Copy the secret key

**Add to `.env`:**
```env
STRIPE_SECRET_KEY=sk_test_your_key_here
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
```

⚠️ **Important:** Always use TEST mode keys! Live mode requires explicit approval.

---

### 4. Supabase Credentials

#### 4a. Supabase URL

**Where to find it:**
1. Go to https://supabase.com/dashboard
2. Select your `catered-by-me` project
3. Click **"Settings"** (gear icon) → **"API"**
4. Look for **"Project URL"**
5. Copy it (format: `https://xxxxx.supabase.co`)

**Add to `.env`:**
```env
SUPABASE_URL=https://xxxxx.supabase.co
```

#### 4b. Supabase Service Role Key

**Where to find it:**
1. Same page as above (Settings → API)
2. Scroll to **"Project API keys"** section
3. Find **"service_role"** key (⚠️ Keep this SECRET!)
4. Click **"Reveal"** to show it
5. Copy the entire key (long JWT string)

**Add to `.env`:**
```env
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 4c. Supabase Anon Key (Optional)

**Where to find it:**
1. Same page (Settings → API)
2. Find **"anon"** or **"public"** key
3. Copy it

**Add to `.env`:**
```env
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 4d. Supabase JWT Secret

**Where to find it:**
1. Same Supabase dashboard (Settings → API)
2. Scroll to **"JWT Settings"** section
3. Find **"JWT Secret"**
4. Copy it

**Add to `.env`:**
```env
SUPABASE_JWT_SECRET=your-jwt-secret-here
```

---

### 5. Vercel Token (Only if using Vercel)

**Where to find it:**
1. Go to https://vercel.com/account
2. Click **"Settings"** → **"Tokens"**
3. Click **"Create Token"**
4. Give it a name: "Otto SRE Bot"
5. Set expiration
6. Select scope: **"Full Account"** (or specific projects)
7. Click **"Create"**
8. Copy the token (starts with `vercel_...`)

**Add to `.env`:**
```env
VERCEL_TOKEN=vercel_your_token_here
```

---

## 🆔 Required IDs for Config Files

### 1. Render Service ID

**File to edit:** `infra/providers/render.yaml`

**Where to find it:**
1. Go to https://dashboard.render.com
2. Click on your `catered-by-me-api` service (or whatever you named it)
3. Look at the URL in your browser:
   - Format: `https://dashboard.render.com/web/xxxxx`
   - The `xxxxx` part is your service ID
   - OR check the service page - it might show "Service ID: srv-xxxxx"
4. The ID format is usually `srv-xxxxx` or just `xxxxx`

**Update in config:**
```yaml
render_service_id: "srv-xxxxx"  # Replace with your actual ID
```

---

### 2. Supabase Project Reference

**File to edit:** `infra/providers/supabase.yaml`

**Where to find it:**
1. Go to your Supabase dashboard
2. Look at your project URL: `https://xxxxx.supabase.co`
3. The `xxxxx` part is your project ref (it's also in the dashboard URL)
4. It's a short alphanumeric string (like `abcdefghijklmnop`)

**Update in config:**
```yaml
project_ref: "xxxxx"  # Replace with your actual project ref
```

**Alternative method:**
- Go to Settings → General
- Look for "Reference ID" or "Project ID"

---

### 3. Stripe Webhook Endpoint ID

**File to edit:** `infra/providers/stripe.yaml`

**Where to find it:**
1. Go to https://dashboard.stripe.com
2. **Make sure you're in TEST MODE** (toggle in top right)
3. Click **"Developers"** → **"Webhooks"**
4. Find your webhook endpoint (or create one if it doesn't exist)
   - If creating: Click **"Add endpoint"**
   - Enter your Render API URL: `https://catered-by-me-api.onrender.com/webhooks/stripe`
   - Select events to listen to
   - Click **"Add endpoint"**
5. Click on the webhook endpoint
6. Look at the URL or page - you'll see the endpoint ID
   - Format: `we_xxxxx` (starts with `we_`)
7. Copy the ID

**Update in config:**
```yaml
webhook_endpoint_id: "we_xxxxx"  # Replace with your actual webhook ID
```

---

## ✅ Quick Checklist

Use this checklist as you gather your keys and IDs:

### Environment Variables (`.env` file)
- [ ] `RENDER_API_KEY` - From Render Account Settings
- [ ] `GITHUB_TOKEN` - From GitHub Developer Settings
- [ ] `STRIPE_SECRET_KEY` - From Stripe Dashboard (TEST mode!)
- [ ] `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - From Stripe Dashboard (TEST mode!)
- [ ] `SUPABASE_URL` - From Supabase Settings → API
- [ ] `SUPABASE_SERVICE_KEY` - From Supabase Settings → API
- [ ] `SUPABASE_ANON_KEY` - From Supabase Settings → API (optional)
- [ ] `SUPABASE_JWT_SECRET` - From Supabase Settings → API
- [ ] `VERCEL_TOKEN` - From Vercel Account Settings (if using Vercel)

### Config File IDs (YAML files)
- [ ] Render service ID - From Render dashboard URL
- [ ] Supabase project ref - From Supabase project URL
- [ ] Stripe webhook ID - From Stripe Webhooks page (TEST mode!)

---

## 🎯 Next Steps

1. ✅ Create `.env` file from `infra/.env.example`
2. ✅ Fill in all environment variables using this guide
3. ✅ Update `infra/providers/render.yaml` with Render service ID
4. ✅ Update `infra/providers/supabase.yaml` with Supabase project ref
5. ✅ Update `infra/providers/stripe.yaml` with Stripe webhook ID
6. ✅ Test with dry-run commands

---

## 🆘 Need Help?

If you can't find something:
- Check the existing setup docs in the repo (like `SUPABASE_SETUP.md`)
- Ask Otto (me!) - I can help troubleshoot specific providers
- Check provider documentation:
  - Render: https://render.com/docs
  - Stripe: https://stripe.com/docs
  - Supabase: https://supabase.com/docs

