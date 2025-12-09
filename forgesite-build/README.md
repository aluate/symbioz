# ForgeSite Build

**Website Factory for Builders, Trades & Shops**

ForgeSite Build is a website factory that produces professional websites for builders, trades & shops. We turn structured intake data into finished sites using proven modules and automated systems. We are a factory, not an agency.

## Purpose

We build professional websites for:
- Custom home builders
- Remodelers
- Trades (HVAC, electrical, plumbing)
- Cabinet/millwork shops
- Steel building companies

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the marketing site.

## Build

```bash
npm run build
```

## Deploy

Deploy to Vercel (automatic on push to main branch).

1. Connect your GitHub repo to Vercel
2. Set environment variables:
   - `NEXT_PUBLIC_SITE_URL=https://forgesitebuild.com`
3. Configure build settings:
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
4. Deploy

### Vercel Configuration
- Root Directory: `forgesite-build` (if in monorepo)
- Install Command: `npm install`
- Build Command: `npm run build`

## Project Structure

- `/app` - Next.js app router pages
  - `(marketing)/` - Main marketing site
  - `(examples)/` - Example client sites
  - `intake/` - Intake form
  - `api/` - API routes
- `/factory` - Core factory system
  - `modules/` - Reusable page modules
  - `layouts/` - Layout compositor
  - `schemas/` - Zod schemas
  - `proposal/` - Proposal generator
- `/intake` - Intake examples and schemas
- `/leads` - Runtime storage (gitignored)

## How It Works

1. Client fills intake form (or chats with bot)
2. Intake JSON is saved to `/leads/{leadId}/intake.json`
3. Factory system generates site config from intake
4. Layout compositor builds pages from config
5. Preview site is deployed for review
6. Client approves → Launch

## Adding New Modules

1. Create component in `/factory/modules/`
2. Add to `MODULE_MAP` in `/factory/layouts/buildPageFromConfig.ts`
3. Document in `DATA_MODEL.md`
