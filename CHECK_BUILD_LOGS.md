# 🔍 Check Build Logs - Quick Guide

**Since script output isn't showing in PowerShell, here's what to do:**

---

## ✅ Tokens Found

- **Vercel Token:** `n6QnE86DsiIcQXIdQp0SA34P`
- **Cloudflare Token:** `bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH`

---

## 🚀 Run This Command

**PowerShell:**
```powershell
cd "E:\My Drive"
$env:VERCEL_TOKEN = "n6QnE86DsiIcQXIdQp0SA34P"
$env:CLOUDFLARE_API_TOKEN = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"
python tools/deploy_corporate_crashout.py
```

**The script will:**
1. ✅ Check/fix root directory
2. ✅ Check deployment status  
3. ✅ **Show build logs if errors**
4. ✅ Add domain to Vercel
5. ✅ Update Cloudflare DNS
6. ✅ Promote to production

---

## 📋 What to Look For

**If you see errors in the output:**
- Copy the error messages
- Share them with me
- I'll help fix the code issues

**Common errors:**
- TypeScript compilation errors
- Missing imports
- Missing dependencies
- Environment variable errors
- Prisma generation errors

---

**Run the command and check the output for build logs and errors!** 🔍
