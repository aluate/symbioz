# Otto Deployment Audit

## Location

**Found:** `apps/otto/`

Otto is a FastAPI-based automation agent service.

## How It Runs Locally

### Entry Points

1. **CLI Command:**
   ```bash
   cd apps/otto
   python -m otto.cli server
   ```

2. **Direct API:**
   ```bash
   cd apps/otto
   python -m otto.api
   ```

3. **Uvicorn (alternative):**
   ```bash
   cd apps/otto
   python -m uvicorn otto.api:app --host 0.0.0.0 --port 8001
   ```

### Default Configuration

- **Host:** `0.0.0.0` (all interfaces)
- **Port:** `8001`
- **Framework:** FastAPI
- **ASGI Server:** Uvicorn

### API Endpoints

- `GET /` - Root endpoint (service info)
- `GET /health` - Health check ✅ (already exists)
- `POST /prompt` - Submit text prompt
- `POST /task` - Submit structured task
- `GET /skills` - List available skills

## Environment Variables

### Required
- None (Otto can run with defaults)

### Optional (for full functionality)

**Life OS Integration:**
- `LIFE_OS_API_URL` - Default: `http://localhost:8000`
  - Used by: activity_reporting, memory, tax_brain, bill_reminder, bill_management, transaction, income_tracking, task_management, scheduling, reminder, calendar, self_test, otto_runs

**Otto API:**
- `OTTO_API_URL` - Default: `http://localhost:8001`
  - Used by: scheduling, self_test, env_status

**Deployment Skills (optional):**
- `VERCEL_TOKEN` - For Vercel deployment automation
- `RENDER_API_KEY` - For Render deployment automation
- `STRIPE_SECRET_KEY` - For Stripe integration
- `GITHUB_TOKEN` - For GitHub operations
- `OTTO_ENV` - Environment mode (default: `prod`)

### Configuration File

- `apps/otto/otto_config.yaml` - YAML config (optional, has defaults)

## Dependencies

From `apps/otto/requirements.txt`:
- `pyyaml>=6.0`
- `pydantic>=2.0.0`
- `rich>=13.0.0`
- `fastapi>=0.104.0`
- `uvicorn[standard]>=0.24.0`
- `httpx>=0.25.0`

**Note:** `uvicorn[standard]` requires Rust. For deployment, use `uvicorn` without `[standard]` or ensure Rust is available in the build environment.

## Current Status

✅ **Health endpoint exists** (`/health`)  
✅ **FastAPI app structure**  
✅ **CLI entry point**  
❌ **No Dockerfile**  
❌ **No deployment config**  
❌ **No .env.example**

## Deployment Readiness

**Ready for deployment with:**
- Dockerfile creation
- Environment variable documentation
- Start command configuration

