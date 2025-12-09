# Problem-Solution Registry

**Purpose:** Documented problems and their solutions - so we don't solve them twice!  
**Last Updated:** January 2025

---

## 📋 How to Use This Registry

**When you encounter a problem:**
1. Search this registry first
2. Follow the solution steps
3. If it's a new problem, add it here after solving

**When solving a problem:**
1. Document it here immediately
2. Link to relevant skills/tools
3. Add prevention tips

---

## 🚨 Deployment Problems

### Problem: Can't Find Vercel Build Logs

**Symptoms:**
- Deployment failed but can't see why
- Need to check build errors
- Don't know where to look for logs

**Root Cause:**
- Logs not easily accessible without digging
- No quick command to fetch logs

**Solution:**

**Option 1: Use the dedicated script (RECOMMENDED)**
```bash
python tools/check_vercel_logs.py
```

**Option 2: Use infra.py**
```bash
python tools/infra.py fix-vercel --project PROJECT_NAME
```

**Option 3: Dashboard**
- Open: https://vercel.com/aluates-projects/PROJECT_NAME
- Click on deployment
- View logs tab

**Command/Tool:** 
- `tools/check_vercel_logs.py` - Dedicated log checker
- `tools/infra.py fix-vercel` - Comprehensive fix tool

**Prevention:**
- Use `check_vercel_logs.py` script for quick access
- Bookmark Vercel dashboard URLs
- Add project to Quick Reference

**Last Solved:** January 2025 - Created dedicated script

**Related:**
- `QUICK_REFERENCE.md` → Check Vercel Build Logs
- `SKILLS_LIBRARY.md` → Vercel Build Log Checker

---

### Problem: Vercel Build Failed

**Symptoms:**
- Deployment shows ERROR status
- Build fails during deployment
- Site not accessible

**Root Cause:**
- Missing environment variables
- Build configuration issues
- TypeScript/build errors
- Missing dependencies

**Solution:**

**Step 1: Check logs**
```bash
python tools/check_vercel_logs.py
```

**Step 2: Auto-fix (if possible)**
```bash
python tools/infra.py fix-vercel --project PROJECT_NAME
```

**Step 3: Common fixes**

**Missing Environment Variables:**
- Check project spec for required vars
- Set via Vercel dashboard or CLI
- Use `tools/infra.py` to set env vars

**TypeScript Errors:**
- Fix type errors in code
- Check parameter order (required before optional)
- Fix API fetch type issues

**Build Configuration:**
- Check `next.config.js`
- Verify `package.json` dependencies
- Check framework settings in Vercel

**Command/Tool:**
- `tools/infra.py fix-vercel` - Auto-fix deployment
- `tools/check_vercel_logs.py` - Check logs
- Vercel dashboard - Manual configuration

**Prevention:**
- Run diagnostics before deploying
- Use dry-run mode
- Validate configuration files
- Set up auto-fix monitoring

**Last Solved:** Multiple times - Auto-fix system created

**Related:**
- `QUICK_REFERENCE.md` → Fix Vercel Deployment
- `SKILLS_LIBRARY.md` → Auto-Fix Vercel
- `infra/CAN_OTTO_FIX_VERCEL.md`

---

### Problem: TypeScript Build Errors on Vercel

**Symptoms:**
- Build fails with TypeScript errors
- Errors about parameter order
- Type mismatch errors

**Root Cause:**
- Required parameters after optional ones
- Incorrect API fetch return types
- Missing type definitions

**Solution:**

**Parameter Order Fix:**
- Required parameters must come before optional
- Fix function signatures:
```typescript
// Wrong:
function example(optional?: string, required: string)

// Right:
function example(required: string, optional?: string)
```

**API Fetch Type Fix:**
- Use proper return types
- Handle Promise types correctly
- Type the response properly

**Command/Tool:**
- Fix in code directly
- TypeScript compiler will show errors

**Prevention:**
- Use TypeScript strict mode
- Run type check before pushing
- Fix type errors immediately

**Last Solved:** December 2024 - Fixed parameter order issues

**Related:**
- `infra/COMPLETE_SUMMARY.md` - TypeScript fixes documented
- `infra/DEPLOYMENT_STATUS.md` - Build error fixes

---

### Problem: Deployment Status Unknown

**Symptoms:**
- Don't know if deployment succeeded
- Can't check status quickly
- Need to monitor deployment

**Root Cause:**
- No quick status check command
- Dashboard requires manual navigation

**Solution:**

**Quick Status Check:**
```bash
python check_deployment.py
```

**Real-Time Monitoring:**
```bash
python watch_vercel.py
```

**Full Diagnostics:**
```bash
python tools/infra.py diag --provider vercel
```

**Command/Tool:**
- `check_deployment.py` - Quick check
- `watch_vercel.py` - Real-time monitor
- `tools/infra.py diag` - Full diagnostics

**Prevention:**
- Set up monitoring scripts
- Use real-time watch during deployments
- Run diagnostics regularly

**Last Solved:** January 2025 - Created status check scripts

**Related:**
- `QUICK_REFERENCE.md` → Quick Deployment Status
- `SKILLS_LIBRARY.md` → Deployment Status Checker

---

### Problem: Missing Environment Variables

**Symptoms:**
- Build fails with "undefined" errors
- API calls fail
- Configuration not found

**Root Cause:**
- Environment variables not set in Vercel
- Variables named incorrectly
- Missing from project spec

**Solution:**

**Check What's Required:**
- Check project spec: `infra/project-specs/PROJECT.yaml`
- Look for `required_env_vars` section

**Set Variables:**
```bash
# Via infra.py (when implemented)
python tools/infra.py update-env-vars --project PROJECT

# Or manually via Vercel dashboard
# Settings → Environment Variables
```

**Verify:**
```bash
python tools/check_vercel_settings.py
```

**Command/Tool:**
- Vercel dashboard - Manual setting
- `tools/infra.py` - Automated (when available)
- `check_vercel_settings.py` - Verification

**Prevention:**
- Document required env vars in project spec
- Use `.env.example` files
- Validate before deployment
- Auto-set during provisioning

**Last Solved:** Ongoing - Standardized in project specs

**Related:**
- `infra/project-specs/` - Project specifications
- `SKILLS_LIBRARY.md` → Infrastructure Automation

---

## 🔧 Configuration Problems

### Problem: Vercel Project Not Configured

**Symptoms:**
- Project not found in Vercel
- Deployment doesn't work
- Missing project settings

**Root Cause:**
- Project not created in Vercel
- Wrong project name/ID
- Configuration missing

**Solution:**

**Set Up Project:**
```bash
python tools/infra.py setup-vercel-project \
  --project PROJECT_NAME \
  --repo USERNAME/REPO \
  --root-dir apps/PROJECT \
  --framework nextjs
```

**Or Manually:**
1. Create project in Vercel dashboard
2. Connect GitHub repository
3. Configure build settings
4. Set root directory if needed

**Verify:**
```bash
python tools/infra.py diag --provider vercel
```

**Command/Tool:**
- `tools/infra.py setup-vercel-project` - Automated setup
- Vercel dashboard - Manual setup

**Prevention:**
- Use project specs for consistency
- Document setup process
- Use templates for new projects

**Last Solved:** Ongoing - Standardized setup process

**Related:**
- `infra/README.md` - Setup instructions
- `QUICK_REFERENCE.md` → Configure Vercel Project

---

### Problem: Custom Domain Not Working

**Symptoms:**
- Domain not resolving
- DNS errors
- Certificate issues

**Root Cause:**
- DNS not configured correctly
- Domain not added to Vercel
- DNS propagation delay

**Solution:**

**Step 1: Add Domain to Vercel**
```bash
python tools/infra.py configure-domain \
  --project PROJECT_NAME \
  --domain example.com
```

**Step 2: Configure DNS**
- Add CNAME record pointing to Vercel
- Or A records as specified by Vercel
- Wait for DNS propagation (can take up to 48 hours)

**Step 3: Verify**
- Check DNS records
- Wait for SSL certificate (automatic)
- Test domain access

**Command/Tool:**
- `tools/infra.py configure-domain` - Domain configuration
- DNS provider dashboard - DNS records

**Prevention:**
- Document DNS setup process
- Use CNAME for subdomains
- Check DNS propagation tools

**Last Solved:** Ongoing - Standardized domain setup

**Related:**
- `QUICK_REFERENCE.md` → Set Up Custom Domain
- Vercel domain documentation

---

## 🐛 Build & Code Problems

### Problem: Next.js Static Generation Errors

**Symptoms:**
- Build completes but shows errors
- Errors for client-side only pages
- Static generation warnings

**Root Cause:**
- Pages marked as static but use client-only features
- Missing `use client` directive
- Dynamic routes not handled

**Solution:**

**For Client-Side Only Pages:**
```typescript
'use client'  // Add to top of file
```

**For Dynamic Routes:**
- Use `generateStaticParams` for static generation
- Or mark as dynamic: `export const dynamic = 'force-dynamic'`

**Command/Tool:**
- Fix in code directly
- Next.js compiler will guide

**Prevention:**
- Understand Next.js rendering modes
- Use appropriate directives
- Test build locally before deploying

**Last Solved:** December 2024 - Documented in build fixes

**Related:**
- `infra/BUILD_FIX_PROGRESS.md` - Build error fixes
- Next.js documentation

---

### Problem: API Fetch Type Errors

**Symptoms:**
- TypeScript errors on API calls
- Type mismatches
- Promise handling errors

**Root Cause:**
- Incorrect return types
- Missing type definitions
- Async/await issues

**Solution:**

**Fix Return Types:**
```typescript
// Define return type
async function apiCall(): Promise<ResponseType> {
  // ...
}

// Use properly typed fetch
const data = await apiFetch<ResponseType>(url);
```

**Command/Tool:**
- Fix in code
- TypeScript compiler

**Prevention:**
- Define types for API responses
- Use typed fetch utilities
- Run type checks before pushing

**Last Solved:** December 2024 - Fixed in deployment fixes

**Related:**
- `infra/COMPLETE_SUMMARY.md` - Type fixes

---

## 🔍 Monitoring & Diagnostics Problems

### Problem: Don't Know Service Health

**Symptoms:**
- Services might be down
- Don't know status
- Need quick health check

**Root Cause:**
- No centralized monitoring
- Manual checking required

**Solution:**

**Run Full Diagnostics:**
```bash
python tools/infra.py diag --env=prod
```

**Check Specific Provider:**
```bash
python tools/infra.py diag --provider vercel
python tools/infra.py diag --provider render
```

**Check Output:**
- Console summary
- `diagnostics/latest.md` - Full report
- `diagnostics/latest.json` - Structured data

**Command/Tool:**
- `tools/infra.py diag` - Full diagnostics
- Provider-specific checks

**Prevention:**
- Run diagnostics regularly
- Set up monitoring
- Check before deployments

**Last Solved:** Ongoing - Diagnostics system created

**Related:**
- `QUICK_REFERENCE.md` → Run Full Diagnostics
- `SKILLS_LIBRARY.md` → Full Diagnostics
- `infra/README.md`

---

## 📦 Infrastructure Problems

### Problem: Need to Provision New Project

**Symptoms:**
- Starting new project
- Need infrastructure setup
- Manual setup is tedious

**Root Cause:**
- No automated provisioning
- Manual configuration required

**Solution:**

**Generate from Template:**
```bash
python tools/infra.py generate-project \
  --template saas-starter \
  --name my-project
```

**Provision Infrastructure:**
```bash
python tools/infra.py provision-project \
  --spec infra/project-specs/PROJECT.yaml \
  --env=prod
```

**Command/Tool:**
- `tools/infra.py generate-project` - Create from template
- `tools/infra.py provision-project` - Provision infrastructure

**Prevention:**
- Use templates for consistency
- Document project specs
- Standardize setup process

**Last Solved:** Ongoing - Template system created

**Related:**
- `QUICK_REFERENCE.md` → Generate Project
- `SKILLS_LIBRARY.md` → Generate Project
- `infra/TEMPLATE_SYSTEM_COMPLETE.md`

---

## 🎯 Common Patterns

### Problem Pattern: "I Can't Find..."

**Solution Pattern:**
1. Check `QUICK_REFERENCE.md` first
2. Search this registry
3. Check `SKILLS_LIBRARY.md`
4. Check `REPO_INVENTORY.md`

**Prevention:**
- Document common tasks
- Create quick references
- Maintain this registry

---

### Problem Pattern: "This Should Be Automated"

**Solution Pattern:**
1. Check if skill exists in `SKILLS_LIBRARY.md`
2. Check if problem solved in this registry
3. Create/add to Otto skills if needed
4. Document in appropriate places

**Prevention:**
- Build reusable skills
- Document automation needs
- Add to skills library

---

## 📝 Adding New Problems

**When you solve a problem:**

1. **Add entry here** with:
   - Clear problem description
   - Symptoms
   - Root cause
   - Step-by-step solution
   - Commands/tools used
   - Prevention tips

2. **Link to:**
   - Relevant skills in `SKILLS_LIBRARY.md`
   - Quick reference if common
   - Any related documentation

3. **Update:**
   - `QUICK_REFERENCE.md` if it's a common task
   - `SKILLS_LIBRARY.md` if new tool/skill created

---

## 🔗 Related Documentation

- `QUICK_REFERENCE.md` - Common tasks cheat sheet
- `SKILLS_LIBRARY.md` - All utilities and tools
- `REPO_INVENTORY.md` - Repository structure
- `infra/README.md` - Infrastructure system

---

**Last Updated:** January 2025  
**Maintainer:** Add solved problems here immediately after solving!


