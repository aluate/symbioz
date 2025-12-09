# Booking/Lead Gen Template

**Booking or lead generation site with form submissions**

---

## What's Included

- ✅ **Frontend:** Next.js app on Vercel
- ✅ **Backend:** FastAPI API on Render
- ✅ **Database:** Supabase for storing leads/bookings
- ✅ **Forms:** Contact/booking form handling

---

## Use Cases

Perfect for:
- Service booking sites
- Appointment scheduling
- Lead capture forms
- Contact forms with storage
- Consultation booking

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

3. **Environment Variables**
   - `SUPABASE_SERVICE_KEY`

---

## Quick Start

1. Generate project spec:
   ```bash
   python tools/infra.py generate-project \
     --template booking-leadgen \
     --name my-booking-site \
     --github-repo username/my-booking-site
   ```

2. Provision infrastructure:
   ```bash
   python tools/infra.py provision-project \
     --spec infra/project-specs/my-booking-site.yaml \
     --env prod
   ```

3. Deploy:
   ```bash
   python tools/infra.py deploy \
     --spec infra/project-specs/my-booking-site.yaml \
     --env prod
   ```

---

## Customization

After generation, customize:
- Project name and description
- GitHub repository path
- Form fields (frontend)
- Database schema (Supabase)
- Environment variables

