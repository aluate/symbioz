# Extending Auto-Fix to Other Providers

## 🎯 Pattern Established

The Vercel auto-fix system establishes a pattern that can be extended to all providers:

1. **Provider Client** - Full API integration (already done for Render, GitHub, etc.)
2. **Provider Fixer** - Implements `BaseFixer` interface
3. **CLI Command** - Individual and unified commands

## 📋 Providers to Extend

### 1. Render Fixer (`infra/providers/render_fixer.py`)

**What it can fix:**
- ✅ Missing environment variables
- ✅ Service configuration issues
- ✅ Failed deployments (redeploy)
- ✅ Health check failures

**Implementation:**
- Use existing `RenderClient` (already has all methods)
- Implement `BaseFixer` interface
- Detect issues from service status/logs
- Apply fixes (env vars, config)
- Trigger redeploy

### 2. GitHub Fixer (`infra/providers/github_fixer.py`)

**What it can fix:**
- ✅ Failed CI/CD workflows (retry)
- ✅ Branch protection issues
- ✅ Missing workflow files
- ✅ Repository settings

**Implementation:**
- Use existing `GitHubClient`
- Implement `BaseFixer` interface
- Detect from CI status, failing checks
- Apply fixes (retry workflows, update settings)

### 3. Supabase Fixer (`infra/providers/supabase_fixer.py`)

**What it can fix:**
- ✅ Connection issues
- ✅ Missing schema migrations
- ✅ Environment variable issues

**Implementation:**
- Use existing `SupabaseClient`
- Implement `BaseFixer` interface
- Detect from connection status
- Apply fixes (run migrations, set env vars)

### 4. Stripe Fixer (`infra/providers/stripe_fixer.py`)

**What it can fix:**
- ✅ Failed webhooks (recreate)
- ✅ Missing webhook endpoints
- ✅ API key issues

**Implementation:**
- Use existing `StripeClient`
- Implement `BaseFixer` interface
- Detect from webhook status
- Apply fixes (recreate webhooks, update keys)

## 🏗️ Implementation Steps

For each provider:

1. **Create Fixer Class**
   ```python
   class RenderFixer(BaseFixer):
       def detect_issues(self) -> List[Dict]:
           # Check service status, logs
           pass
       
       def apply_fixes(self, issues) -> FixResult:
           # Fix env vars, config, etc.
           pass
       
       def trigger_redeploy(self) -> str:
           # Trigger new deployment
           pass
   ```

2. **Add to CLI**
   - Individual command: `fix-render`, `fix-github`, etc.
   - Already integrated in `fix-all` command

3. **Test**
   - Dry-run mode first
   - Then real fixes

## 🎯 Unified `fix-all` Command

The `fix-all` command already exists and will:
1. Load project spec
2. For each component/provider:
   - Detect issues
   - Apply fixes
   - Redeploy
   - Wait for success
3. Report summary

**This is the right approach!** One command fixes everything.

