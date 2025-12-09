# Automation Audit - Manual Steps Analysis

**Date:** November 30, 2025  
**Question:** How many manual steps can Otto automate?

---

## 📋 Manual Steps Breakdown

### **1. Domain & DNS (Wix → Vercel)**

#### ✅ **CAN AUTOMATE:**

**Step 1: Deploy to Vercel**
- ✅ Push code to GitHub - **Otto can do this via git commands**
- ✅ Connect repository to Vercel - **Otto can do this via Vercel API** (`POST /v9/projects`)
- ✅ Deploy site - **Otto can trigger deployment** (`POST /v13/deployments`)
- ✅ Note deployment URL - **Otto can retrieve this**

**Step 2: Configure Domain in Vercel**
- ✅ Add custom domain - **Otto can do this via Vercel API** (`POST /v6/domains/{domain}`)
- ✅ Get DNS records - **Otto can retrieve these**

**Step 4: Verify Domain**
- ✅ Wait for DNS propagation - **Otto can poll and check**
- ✅ Verify domain works - **Otto can check domain status via API**
- ✅ Test website loads - **Otto can make HTTP request**

#### ❌ **CANNOT AUTOMATE (Needs You):**

**Step 3: Update DNS at Domain Provider**
- ❌ Log into Wix - **Requires account access + potentially MFA**
- ❌ Update DNS records in Wix - **Wix doesn't have public API for DNS management**
- ❌ Update nameservers - **Requires domain registrar access**

**Automation Level: ~70%** - Can do everything except the actual DNS updates at Wix.

---

### **2. Contact Form Backend**

#### ✅ **CAN AUTOMATE:**

**Option 1: Email Service**
- ❌ Set up Formspree/SendGrid/Resend account - **Can't automate account creation**
- ❌ Get API key - **Can't automate (requires human to get key)**
- ✅ Update ContactForm component - **Otto can modify code**
- ✅ Add environment variable to Vercel - **Otto can do this**

**Option 2: API Route**
- ✅ Create Next.js API route - **Otto can create the file**
- ✅ Wire to email service - **Otto can write the code**
- ✅ Deploy and test - **Otto can deploy**

**Automation Level: ~60%** - Can do code changes, but need you to provide API key.

---

### **3. Project Images**

#### ✅ **CAN AUTOMATE:**

- ❌ Gather project photos - **Can't automate (need actual photos)**
- ✅ Optimize images - **Otto can use image processing libraries**
- ✅ Add to `public/projects/` directory - **Otto can create file structure**
- ✅ Update ProjectTeaserGrid component - **Otto can modify code**

**Automation Level: ~50%** - Can do everything except gather the actual photos.

---

### **4. Contact Information**

#### ✅ **CAN FULLY AUTOMATE:**

- ✅ Update placeholder email - **Otto can do this if you provide the email**
- ✅ Update placeholder phone - **Otto can do this if you provide the phone**
- ✅ Verify contact info - **Otto can check the code**

**Automation Level: 100%** - Just need the actual values from you.

---

## 🎯 Summary: What Otto Can Automate

### **Fully Automatable (100%):**
- ✅ Contact information updates (if values provided)
- ✅ Code file modifications
- ✅ Environment variable management
- ✅ Deployment triggering
- ✅ Domain verification/testing

### **Mostly Automatable (70-80%):**
- ✅ Domain configuration in Vercel
- ✅ Vercel project setup
- ✅ Contact form code changes
- ✅ Image optimization and file structure

### **Partially Automatable (50-60%):**
- ⚠️ Contact form backend (needs API key from you)
- ⚠️ Project images (needs actual photos from you)
- ⚠️ DNS updates (can't access Wix DNS)

### **Cannot Automate (Requires You):**
- ❌ Wix DNS management (no API access)
- ❌ Account creation (email service signup)
- ❌ Getting API keys (requires you to retrieve)
- ❌ Gathering actual project photos

---

## 🚀 Recommendation

**Otto can automate ~75% of the manual steps!**

**What you'll still need to do:**
1. Update DNS records in Wix (one-time, ~5 minutes)
2. Get email service API key (one-time, ~2 minutes)
3. Provide actual contact info (one-time, ~1 minute)
4. Provide project photos (one-time, as you gather them)

**Everything else Otto can handle!**

---

## 💡 Next Steps

I can build commands to automate:
1. `otto setup-vercel-project` - Create Vercel project, connect repo, deploy
2. `otto configure-domain` - Add domain to Vercel, provide DNS instructions
3. `otto update-contact-info` - Update contact info in code
4. `otto setup-contact-form` - Create API route and wire up (needs API key)
5. `otto verify-deployment` - Check everything is working

**Should I build these automation commands now?**

