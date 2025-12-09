# Vercel Auto-Fix Feature - Plan

## 🎯 What You Want

**Otto should:**
1. ✅ Check Vercel deployment logs
2. ✅ Identify errors
3. ✅ Attempt repairs (fix env vars, config issues, etc.)
4. ✅ Redeploy automatically
5. ✅ Repeat until deployment succeeds

**This is totally doable!** Let me build it.

---

## 🏗️ What Needs to Be Built

### 1. Full Vercel Client Implementation
- ✅ Check deployment status
- ✅ Fetch build logs
- ✅ Get deployment details
- ✅ Trigger redeployments
- ✅ Wait for deployment completion

### 2. Error Detection & Repair Logic
- Parse build logs for common errors:
  - Missing environment variables
  - Build failures (missing dependencies, TypeScript errors, etc.)
  - Configuration issues (wrong root directory, etc.)
- Attempt automatic fixes:
  - Set missing env vars
  - Update Vercel project settings
  - Fix config files

### 3. Auto-Retry Loop
- Check deployment status
- If failed: diagnose, fix, redeploy
- Wait for completion
- Repeat until success (with max attempts)

---

## 🔧 Implementation Steps

### Phase 1: Basic Vercel Integration (Diagnostics)
- List deployments
- Get deployment status
- Fetch build logs
- Basic health checks

### Phase 2: Error Detection
- Parse logs for common errors
- Identify fixable issues
- Generate repair suggestions

### Phase 3: Auto-Repair
- Fix environment variables
- Update project settings
- Fix configuration issues

### Phase 4: Auto-Redeploy Loop
- Check status → Fix → Redeploy → Wait → Repeat

---

## 📋 Vercel API Endpoints Needed

Based on Vercel API docs, we'll need:
- `GET /v13/deployments` - List deployments
- `GET /v13/deployments/{id}` - Get deployment details
- `GET /v13/deployments/{id}/events` - Get deployment logs
- `POST /v13/deployments/{id}/cancel` - Cancel deployment
- `PATCH /v1/projects/{name}/env` - Update environment variables
- `POST /v13/deployments` - Create/redeploy

---

## 🚀 New CLI Command

We'd add:
```bash
python tools/infra.py fix-vercel --project catered-by-me --auto-retry
```

This would:
1. Check latest deployment
2. If failed, read logs
3. Diagnose issues
4. Apply fixes
5. Redeploy
6. Monitor until success

---

## ⚠️ Safety Features

- `--dry-run` mode (show what would be fixed)
- Max retry limit (e.g., 5 attempts)
- Manual approval for destructive changes
- Detailed logging of all actions

---

**Want me to build this?** I can start with Phase 1 (basic Vercel integration) right now!

