# Sugar Mountain Builders Website

A production-ready Next.js website for Sugar Mountain Builders, built with TypeScript and following the brand guidelines defined in the Valhalla Legacy Group repository.

## Tech Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **CSS Modules** for component styling
- **Google Fonts** (Playfair Display + Inter) via `next/font`

## Brand Implementation

- **Colors**: Tiffany Blue (#81D8D0), Black (#000000), Warm White (#F5F5F5), Charcoal (#1E1E1E)
- **Typography**: Playfair Display (headings), Inter (body)
- **Design**: Mountain-modern, minimal, high-end aesthetic

## Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. Navigate to the app directory:
```bash
cd apps/smb_site
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
apps/smb_site/
├── app/
│   ├── components/          # Reusable components
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Navigation.tsx
│   │   ├── Hero.tsx
│   │   ├── Section.tsx
│   │   ├── Button.tsx
│   │   ├── TrustBar.tsx
│   │   ├── ProcessSteps.tsx
│   │   ├── ContactForm.tsx
│   │   └── ProjectTeaserGrid.tsx
│   ├── styles/
│   │   └── globals.css      # Global styles and CSS variables
│   ├── page.tsx             # Home page
│   ├── layout.tsx           # Root layout with fonts
│   ├── our-homes/
│   ├── modular-installs/
│   ├── remodels-additions/
│   ├── process/
│   ├── about/
│   └── contact/
├── package.json
├── tsconfig.json
└── next.config.js
```

## Pages

- **Home** (`/`) - Hero, services overview, process teaser
- **Our Homes** (`/our-homes`) - Custom and spec home projects
- **Modular Installs** (`/modular-installs`) - Stax modular installation services
- **Remodels & Additions** (`/remodels-additions`) - Remodel services
- **Process** (`/process`) - Five-phase workflow breakdown
- **About** (`/about`) - Company story and values
- **Contact** (`/contact`) - Contact form and information

## Development

### Build for Production

```bash
npm run build
```

### Start Production Server

```bash
npm start
```

### Lint

```bash
npm run lint
```

## TODOs / Next Steps

1. **Contact Form Backend**: Wire the contact form to an email service or API endpoint
2. **Project Images**: Replace placeholder images with actual project photos
3. **Contact Information**: Update placeholder email and phone in contact page
4. **SEO**: Add meta tags, Open Graph, and structured data
5. **Analytics**: Add analytics tracking (Google Analytics, etc.)
6. **Performance**: Optimize images and add image optimization
7. **Accessibility**: Audit and improve accessibility features

## Deployment

This site is ready to deploy to Vercel (recommended), Netlify, or any Node.js hosting platform.

### Deploy to Vercel

1. Push this code to a GitHub repository
2. Connect the repository to Vercel
3. Configure environment variables if needed
4. Deploy!

The site will automatically rebuild on every push to the main branch.

## Brand Guidelines Reference

All brand guidelines, colors, typography, and content are sourced from:
- `control/CONTROL.md`
- `brands/smb/brand_brief.md`
- `web/smb_site/content.md`

These files are the single source of truth for brand implementation.

