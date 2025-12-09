# Otto Templates

**Purpose:** Reusable project templates for Otto to generate complete, deployable projects.

---

## Overview

Templates allow Otto to quickly create new projects by combining:
- Project specification patterns
- Infrastructure requirements
- Provider configurations
- Environment variable mappings

---

## Template Structure

Each template lives in its own directory:

```
infra/templates/
  <template-name>/
    template.yaml          # Template metadata and spec
    project-spec.yaml      # Example project spec generated from this template
    README.md              # Template description and usage
```

---

## Available Templates

### 1. **saas-starter**
Full-stack SaaS application template:
- Frontend: Next.js on Vercel
- Backend: FastAPI on Render
- Database: Supabase
- Payments: Stripe
- Authentication: Supabase Auth

**Best for:** Subscription apps, SaaS products, member portals

---

### 2. **portfolio-site**
Simple portfolio/landing page:
- Frontend: Next.js on Vercel
- No backend required
- Optional: Contact form via API route

**Best for:** Personal portfolios, landing pages, simple marketing sites

---

### 3. **booking-leadgen**
Booking/lead generation site:
- Frontend: Next.js on Vercel
- Backend: FastAPI on Render (for form submissions)
- Database: Supabase (for storing leads)

**Best for:** Service booking, appointment scheduling, lead capture

---

## Using Templates

### Generate Project from Template

```bash
python tools/infra.py generate-project \
  --template saas-starter \
  --name my-awesome-app \
  --output infra/project-specs/my-awesome-app.yaml
```

This will:
1. Load template metadata
2. Generate project spec with your project name
3. Create provider config entries
4. Save to project-specs directory

### Then Provision

```bash
python tools/infra.py provision-project \
  --spec infra/project-specs/my-awesome-app.yaml \
  --env prod
```

---

## Creating New Templates

1. Create directory: `infra/templates/<template-name>/`
2. Add `template.yaml` with metadata
3. Add `project-spec.yaml` as example
4. Add `README.md` with description
5. Document any special requirements

### Date Format Standards

**Default: American format (M.D.YYYY) for all user-facing dates.**

- Store dates in ISO format (`YYYY-MM-DD`) in config/data files
- Display dates in American format (`M.D.YYYY` or `Month D, YYYY`) to users
- See `DATE_FORMAT_GUIDELINES.md` for implementation details and examples

**Example:**
- Config: `"date": "2026-06-20"` (ISO)
- Display: `6.20.2026` or `June 20, 2026` (American)

---

## Template Metadata Format

See `infra/templates/<template-name>/template.yaml` for the format.

Key fields:
- `name` - Template identifier
- `description` - What it's for
- `components` - What's included (web, api, etc.)
- `providers` - Which cloud providers are needed
- `variables` - What needs to be customized (project name, etc.)

