# Portfolio Site Template

**Simple portfolio or landing page with Next.js**

---

## What's Included

- ✅ **Frontend:** Next.js app on Vercel
- ✅ **Deployment:** Automatic via Vercel
- ✅ **Optional:** Contact form via API routes

---

## Use Cases

Perfect for:
- Personal portfolios
- Landing pages
- Marketing sites
- Simple business websites
- Single-page applications

---

## Generated Project Structure

```
your-project/
  apps/
    web/          # Next.js frontend
```

---

## Setup Requirements

Before using this template, you need:

1. **GitHub Repository**
   - Create a new repo
   - Note the `owner/repo` format

2. **Optional: Custom Domain**
   - Configure DNS if using custom domain

---

## Quick Start

1. Generate project spec:
   ```bash
   python tools/infra.py generate-project \
     --template portfolio-site \
     --name my-portfolio \
     --github-repo username/my-portfolio
   ```

2. Provision infrastructure:
   ```bash
   python tools/infra.py provision-project \
     --spec infra/project-specs/my-portfolio.yaml \
     --env prod
   ```

3. Deploy:
   ```bash
   python tools/infra.py deploy \
     --spec infra/project-specs/my-portfolio.yaml \
     --env prod
   ```

---

## Customization

After generation, customize:
- Project name and description
- GitHub repository path
- Custom domain (optional)
- Build commands (if needed)

