# Manual Steps - Batched for Later

**Date:** November 30, 2025  
**Purpose:** All manual steps that cannot be automated

---

## 🌐 Domain & DNS (Wix → Vercel)

### Step 1: Deploy to Vercel
1. Push code to GitHub repository
2. Connect repository to Vercel
3. Deploy site
4. Note Vercel deployment URL

### Step 2: Configure Domain in Vercel
1. Go to Vercel project settings
2. Add custom domain: `sugarmountainbuilders.com`
3. Vercel will provide DNS records

### Step 3: Update DNS at Domain Provider
1. Log into Wix domain management (or wherever domain is registered)
2. Update DNS records:
   - **A Record:** Point to Vercel's IP (provided by Vercel)
   - **OR CNAME:** Point to Vercel's hostname (provided by Vercel)
3. Update nameservers if needed (Vercel will guide)

### Step 4: Verify Domain
1. Wait for DNS propagation (can take 24-48 hours)
2. Verify domain works in Vercel dashboard
3. Test website loads at domain

---

## 📧 Contact Form Backend

### Option 1: Email Service (Recommended)
1. Set up Formspree, SendGrid, or Resend account
2. Get API key
3. Update ContactForm component with endpoint
4. Add environment variable to Vercel

### Option 2: API Route
1. Create Next.js API route for form submission
2. Wire to email service or database
3. Deploy and test

---

## 📸 Project Images

1. Gather project photos
2. Optimize images (compress, resize)
3. Add to `public/projects/` directory
4. Update ProjectTeaserGrid component with real images

---

## 📞 Contact Information

1. Update placeholder email in Contact page
2. Update placeholder phone in Contact page
3. Verify all contact info is accurate

---

## ✅ Pre-Launch Checklist

- [ ] Domain connected and working
- [ ] Contact form functional
- [ ] All placeholder content replaced
- [ ] Project images added
- [ ] Contact information updated
- [ ] SEO meta tags added
- [ ] Analytics configured (optional)
- [ ] Mobile responsive tested
- [ ] Cross-browser tested

---

**These steps will be done after code is complete and deployed.**

