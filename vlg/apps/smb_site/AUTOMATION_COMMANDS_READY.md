# Automation Commands - Ready to Build

**Status:** Implementing now

---

## 🚀 **Commands Being Added to Otto**

### **1. `setup-vercel-project`**
```bash
python tools/infra.py setup-vercel-project \
  --project smb \
  --repo username/smb \
  --root-dir vlg/apps/smb_site
```

**Automates:**
- ✅ Create Vercel project
- ✅ Connect GitHub repository
- ✅ Set root directory
- ✅ Trigger initial deployment
- ✅ Get deployment URL

---

### **2. `configure-domain`**
```bash
python tools/infra.py configure-domain \
  --project smb \
  --domain sugarmountainbuilders.com
```

**Automates:**
- ✅ Add domain to Vercel project
- ✅ Get DNS configuration
- ✅ Print DNS instructions

**Still needs you:**
- ⚠️ Update DNS records in Wix

---

### **3. `setup-contact-form`**
```bash
python tools/infra.py setup-contact-form \
  --project smb \
  --email-service resend \
  --api-key YOUR_KEY
```

**Automates:**
- ✅ Create Next.js API route
- ✅ Wire up email service
- ✅ Update ContactForm component
- ✅ Add env var to Vercel
- ✅ Deploy

---

### **4. `update-contact-info`**
```bash
python tools/infra.py update-contact-info \
  --project smb \
  --email info@sugarmountainbuilders.com \
  --phone "(555) 123-4567"
```

**Automates:**
- ✅ Update email in code
- ✅ Update phone in code
- ✅ Commit changes
- ✅ Deploy

---

### **5. `verify-deployment`**
```bash
python tools/infra.py verify-deployment \
  --project smb \
  --domain sugarmountainbuilders.com
```

**Automates:**
- ✅ Check deployment status
- ✅ Verify domain works
- ✅ Test website loads
- ✅ Generate report

---

**Building these commands now...**

