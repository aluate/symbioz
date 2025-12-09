# 🔑 How to Get Cloudflare API Token

**Time:** ~2 minutes  
**Difficulty:** Easy

---

## Quick Steps

1. **Go to:** https://dash.cloudflare.com/profile/api-tokens
2. **Click:** "Create Token"
3. **Use Template:** Click "Edit zone DNS" template (or "Get started" if no templates)
4. **Set Permissions:**
   - Zone → DNS → Edit
   - Zone → Zone → Read
5. **Zone Resources:**
   - Select: "Include" → "Specific zone"
   - Choose: `corporatecrashouttrading.com`
6. **Click:** "Continue to summary"
7. **Click:** "Create Token"
8. **Copy the token** (starts with something like `...` - you'll only see it once!)

---

## Set as Environment Variable

**PowerShell (Windows):**
```powershell
$env:CLOUDFLARE_API_TOKEN = "your_token_here"
```

**Or add to .env file:**
```env
CLOUDFLARE_API_TOKEN=your_token_here
```

---

**Then run deployment again!** 🚀
