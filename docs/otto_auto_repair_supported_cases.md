# Otto Auto-Repair Supported Cases

This document lists the deployment failure classes that Otto can automatically detect and fix.

## Confidence Threshold

Otto only applies automatic fixes when confidence is **≥ 0.85 (85%)**. Lower confidence failures result in a diagnosis PR with recommended actions.

## Vercel / Next.js Failures

### 1. Root Directory / Missing package.json
- **Category:** `root_directory_missing_package`
- **Confidence:** 0.9
- **Detection:** Error messages like "Couldn't find any `pages` or `app` directory" or "package.json not found"
- **Action:** Creates diagnosis document with instructions to verify Vercel Root Directory setting
- **Auto-fix:** No (requires Vercel dashboard configuration)

### 2. Next Command Not Found
- **Category:** `next_command_not_found`
- **Confidence:** 0.95
- **Detection:** Errors like "command not found: next" or "'next' is not recognized"
- **Action:** Updates `apps/symbioz-web/package.json` scripts to use `npx next` instead of `next`
- **Auto-fix:** ✅ Yes - Modifies package.json

### 3. TypeScript Nullability Errors
- **Category:** `typescript_nullability`
- **Confidence:** 0.85
- **Detection:** TypeScript errors involving null/undefined type mismatches
- **Action:** Currently creates diagnosis (complex fixes require more context)
- **Auto-fix:** ⚠️ Partial - Requires manual review for complex cases

### 4. Missing Environment Variable
- **Category:** `missing_env_var`
- **Confidence:** 0.9
- **Detection:** Errors indicating missing environment variables
- **Action:** Creates diagnosis document with variable name and instructions
- **Auto-fix:** No (requires Vercel dashboard configuration)

### 5. Install Command Issues
- **Category:** `install_command_issue`
- **Confidence:** 0.7
- **Detection:** npm install/ci failures, lockfile issues
- **Action:** Creates diagnosis document with recommendations
- **Auto-fix:** No (requires investigation)

## Render / Docker Failures

### 1. Docker COPY Path Errors
- **Category:** `docker_copy_path`
- **Confidence:** 0.9
- **Detection:** Errors like "COPY failed" or "file not found" in Docker build
- **Action:** Creates diagnosis document with Dockerfile path verification instructions
- **Auto-fix:** ⚠️ Diagnosis only (path fixes require context)

### 2. PORT Binding Issues
- **Category:** `port_binding`
- **Confidence:** 0.95
- **Detection:** Errors like "address already in use" or "cannot bind to port"
- **Action:** Verifies Dockerfile uses `$PORT` environment variable
- **Auto-fix:** ✅ Verification (Dockerfile should already be correct)

### 3. Missing Python Module
- **Category:** `missing_python_module`
- **Confidence:** 0.85
- **Detection:** Errors like "ModuleNotFoundError: No module named 'X'"
- **Action:** Adds missing package to `apps/otto/requirements.txt`
- **Auto-fix:** ✅ Yes - Modifies requirements.txt

### 4. Python Import Path Issues
- **Category:** `python_import_path`
- **Confidence:** 0.7
- **Detection:** Import errors not related to missing packages
- **Action:** Creates diagnosis document
- **Auto-fix:** No (requires code structure analysis)

### 5. Docker WORKDIR Issues
- **Category:** `docker_workdir`
- **Confidence:** 0.8
- **Detection:** WORKDIR path errors in Dockerfile
- **Action:** Creates diagnosis document
- **Auto-fix:** ⚠️ Diagnosis only (requires context)

## Safety Features

1. **PR Mode Default:** All fixes are committed to a branch and pushed (PR mode), never directly to main
2. **Confidence Threshold:** Only fixes with ≥85% confidence are auto-applied
3. **Minimal Patches:** Only the smallest necessary changes are made
4. **Local Validation:** JSON files are validated after modification
5. **Diagnosis Fallback:** Low-confidence or failed patches result in diagnosis PRs

## Unsupported Cases

Otto will create diagnosis PRs (not auto-fix) for:
- Complex TypeScript refactoring
- Large code structure changes
- Database migration issues
- Authentication/authorization problems
- Third-party API integration failures
- Performance issues
- Any failure with confidence < 0.85

## How It Works

1. **Monitor** - Checks Vercel and Render deployment status
2. **Fetch Logs** - Retrieves build/deploy logs when failures detected
3. **Classify** - Parses logs and identifies failure category with confidence score
4. **Apply Fix** - If confidence ≥ 0.85, applies minimal patch
5. **Validate** - Runs quick local checks (JSON validation, etc.)
6. **Commit & Push** - Creates branch, commits, pushes (PR mode)
7. **Wait & Recheck** - Waits for redeploy, then loops back to step 1

## Example Output

**High Confidence Fix:**
```json
{
  "success": true,
  "files_changed": ["apps/symbioz-web/package.json"],
  "category": "next_command_not_found",
  "confidence": 0.95,
  "commit_message": "Fix: vercel next_command_not_found (auto-repair confidence: 95%)"
}
```

**Low Confidence Diagnosis:**
```json
{
  "success": true,
  "files_changed": ["docs/deploy_failures_latest.md"],
  "diagnosis_only": true,
  "category": "unknown",
  "confidence": 0.3,
  "commit_message": "Diagnosis: vercel deployment failure (unknown)"
}
```

