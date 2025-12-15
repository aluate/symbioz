# Otto Deployment Guide

Deploy Otto as a standalone API service to Render.

## Prerequisites

- Otto code in `apps/otto/`
- Dockerfile (included)
- Environment variables configured
- GitHub repository: `aluate/symbioz`

## Deploy to Render

### Step 1: Create Render Web Service

1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect GitHub → select repository: `aluate/symbioz`
5. Select branch: `main`

### Step 2: Configure Service

1. **Root Directory:**
   - Set **Root Directory:** `apps/otto` (CRITICAL for monorepos!)

2. **Runtime:**
   - **Option A (Recommended):** Runtime: **Docker**
     - Render will automatically detect and use `apps/otto/Dockerfile`
     - No additional build/start commands needed
   - **Option B:** Runtime: **Python**
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python -m uvicorn otto.api:app --host 0.0.0.0 --port $PORT`

3. **Auto-Deploy:**
   - Enable **Auto-Deploy:** ON (deploys automatically on push to `main`)

4. **Set Environment Variables:**
   - Go to **Environment** tab
   - Add (optional):
     ```
     LIFE_OS_API_URL=https://your-life-os-backend.onrender.com
     OTTO_API_URL=https://your-otto-service.onrender.com
     OTTO_ENV=prod
     ```
   - Add deployment tokens if using deployment skills:
     ```
     VERCEL_TOKEN=your_token
     RENDER_API_KEY=your_key
     STRIPE_SECRET_KEY=your_key
     GITHUB_TOKEN=your_token
     ```

5. **Port:**
   - Render automatically sets `$PORT` environment variable
   - The Dockerfile already handles `$PORT` with fallback to 8001
   - No manual port configuration needed

### Step 3: Deploy

1. Click **"Create Web Service"**
2. Wait for build to complete (check logs in Render dashboard)
3. Render provides a public URL (e.g., `https://otto-something.onrender.com`)

### Step 4: Verify

```bash
# Health check
curl https://your-otto-url.onrender.com/health

# Should return: {"status": "healthy"}
```

## Dockerfile Notes

The Dockerfile uses:
- Python 3.11 slim base image
- `uvicorn` without `[standard]` to avoid Rust dependency
- Health check endpoint at `/health`
- Port handling: Uses `$PORT` environment variable (set by Render) with fallback to 8001

## Environment Variables Reference

See `apps/otto/.env.example` for all available environment variables.

**Minimum required:** None (Otto runs with defaults)

**Recommended for production:**
- `LIFE_OS_API_URL` - If integrating with Life OS
- `OTTO_API_URL` - For self-referencing
- `OTTO_ENV=prod` - Set environment mode

## Testing Deployment

### Health Check

```bash
curl https://your-otto-url/health
```

Expected response:
```json
{"status": "healthy"}
```

### List Skills

```bash
curl https://your-otto-url/skills
```

Expected response:
```json
{
  "skills": [
    {
      "name": "repo_lister",
      "description": "..."
    },
    ...
  ]
}
```

### Submit a Task

```bash
curl -X POST https://your-otto-url/task \
  -H "Content-Type: application/json" \
  -d '{
    "type": "repo_list",
    "payload": {
      "target_repo": ".",
      "output_path": "/tmp/test.md"
    },
    "source": "api"
  }'
```

## Troubleshooting

### Build Fails: "uvicorn[standard] requires Rust"

**Solution:** The Dockerfile uses `uvicorn` without `[standard]`. This is already handled.

### Port Already in Use

**Solution:** Render automatically sets `$PORT`. The Dockerfile already handles this with a fallback to 8001. No changes needed.

### Health Check Fails

**Solution:** Ensure the service is running and accessible. Check logs in Render dashboard:
- Go to your service → **Logs** tab
- Look for startup errors or port binding issues

### CORS Issues

**Solution:** Otto's API has CORS enabled for all origins (`allow_origins=["*"]`). For production, restrict this in `apps/otto/otto/api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Environment Variables Required

Set these in Render dashboard → Environment tab:

- `GITHUB_TOKEN` - GitHub personal access token (for committing fixes)
- `VERCEL_TOKEN` - Vercel API token (for monitoring Vercel deployments)
- `RENDER_API_KEY` - Render API key (for monitoring Render deployments)
- `RENDER_OTTO_SERVICE_ID` (optional) - Your Otto service ID on Render (for self-monitoring)

**Security Note:** Never commit these tokens to git. Use Render's environment variable management.

## Monitor/Repair/Redeploy Loop

Otto includes a built-in skill that monitors Vercel and Render deployments and automatically fixes failures.

### Capabilities Check

First, verify Otto can access the required APIs:

```bash
curl https://your-otto-url.onrender.com/capabilities
```

Response:
```json
{
  "github_token": true,
  "vercel_token": true,
  "render_api_key": true
}
```

### Trigger Monitor Loop

**Option 1: Full control**
```bash
curl -X POST https://your-otto-url.onrender.com/skills/monitor_repair_redeploy \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "pr",
    "targets": {
      "vercel": {
        "projectNameOrId": "symbioz-web",
        "teamId": null
      },
      "render": {
        "serviceId": "your-render-service-id"
      }
    },
    "maxIterations": 5
  }'
```

**Option 2: Quick start (uses defaults)**
```bash
curl -X POST https://your-otto-url.onrender.com/actions/run_deploy_monitor \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "pr",
    "maxIterations": 5
  }'
```

### Safety Modes

- **`"mode": "pr"`** (recommended) - Creates a branch and PR for fixes. Safer, requires review.
- **`"mode": "main"`** - Commits directly to main. Use with caution.

### How It Works

1. Checks Vercel deployment status + fetches build logs
2. Checks Render deployment status + fetches deploy logs
3. When failure detected:
   - Analyzes error logs
   - Generates minimal fix
   - Commits changes
   - Pushes (PR mode creates PR; main mode pushes to main)
4. Waits for redeploy to trigger
5. Repeats until both targets are green or max iterations reached

### Response Format

```json
{
  "task_id": "uuid",
  "status": "success",
  "message": "✅ Both deployments successful after 2 iteration(s)",
  "data": {
    "iterations": 2,
    "results": [...],
    "vercel": {...},
    "render": {...}
  }
}
```

## Next Steps

After deployment:

1. **Get your Otto URL** from Render dashboard (e.g., `https://otto-something.onrender.com`)
2. **Configure Otto URL** in your local environment or config:
   ```powershell
   $env:OTTO_BASE_URL = "https://otto-something.onrender.com"
   ```
   See `docs/otto_url_setup.md` for details.
3. **Verify health check:**
   ```powershell
   .\scripts\check_otto.ps1
   ```
4. **Set environment variables** in Render dashboard (see above)
5. **Test capabilities endpoint** to verify API access
6. **Update Life OS** to point to the new Otto URL (if applicable)
7. **Monitor logs** in Render dashboard for errors

