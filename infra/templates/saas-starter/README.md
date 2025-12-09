# SaaS Starter Template

**Full-stack SaaS application with payments and authentication**

---

## What's Included

- ✅ **Frontend:** Next.js app on Vercel
- ✅ **Backend:** FastAPI API on Render
- ✅ **Database:** Supabase (PostgreSQL + Auth)
- ✅ **Payments:** Stripe integration
- ✅ **Authentication:** Supabase Auth

---

## Use Cases

Perfect for:
- Subscription SaaS products
- Member portals
- Apps that need user accounts
- Apps that process payments
- Apps that need a database

---

## Generated Project Structure

```
your-project/
  apps/
    web/          # Next.js frontend
    api/          # FastAPI backend
  infra/          # Otto configs
  supabase/       # Database schema
```

---

## Setup Requirements

Before using this template, you need:

1. **GitHub Repository**
   - Create a new repo
   - Note the `owner/repo` format

2. **Supabase Project**
   - Create project in Supabase
   - Get project ref and keys

3. **Stripe Account**
   - Get API keys (test mode)
   - Create products if needed

4. **Environment Variables**
   - `SUPABASE_SERVICE_KEY`
   - `SUPABASE_JWT_SECRET`
   - `STRIPE_SECRET_KEY`
   - `STRIPE_WEBHOOK_SECRET`

---

## Quick Start

1. Generate project spec:
   ```bash
   python tools/infra.py generate-project \
     --template saas-starter \
     --name my-app \
     --github-repo username/my-app
   ```

2. Provision infrastructure:
   ```bash
   python tools/infra.py provision-project \
     --spec infra/project-specs/my-app.yaml \
     --env prod
   ```

3. Deploy:
   ```bash
   python tools/infra.py deploy \
     --spec infra/project-specs/my-app.yaml \
     --env prod
   ```

---

## Customization

After generation, customize:
- Project name and description
- GitHub repository path
- Environment variables
- Health check URLs
- Build commands (if needed)

