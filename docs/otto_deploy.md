# Otto Deployment Guide

Deploy Otto as a standalone API service to Railway or Fly.io.

## Prerequisites

- Otto code in `apps/otto/`
- Dockerfile (included)
- Environment variables configured

## Option 1: Railway (Recommended)

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose repository: `aluate/symbioz`
6. Select branch: `main`

### Step 2: Configure Service

1. **Add Service:**
   - Click "+ New" → "GitHub Repo"
   - Select `aluate/symbioz` again (or create a new service)

2. **Set Root Directory:**
   - Go to Settings → Source
   - Set **Root Directory:** `apps/otto`

3. **Configure Build:**
   - Railway auto-detects Dockerfile
   - If not detected, set:
     - **Build Command:** (leave empty, Dockerfile handles it)
     - **Start Command:** (leave empty, Dockerfile handles it)

4. **Set Environment Variables:**
   - Go to Variables tab
   - Add (optional):
     ```
     LIFE_OS_API_URL=https://your-life-os-backend.railway.app
     OTTO_API_URL=https://your-otto-service.railway.app
     OTTO_ENV=prod
     ```
   - Add deployment tokens if using deployment skills:
     ```
     VERCEL_TOKEN=your_token
     RENDER_API_KEY=your_key
     STRIPE_SECRET_KEY=your_key
     GITHUB_TOKEN=your_token
     ```

5. **Set Port:**
   - Railway auto-assigns `PORT` env var
   - Update Dockerfile CMD to use `$PORT` if needed, or:
   - Go to Settings → Networking
   - Set **Port:** `8001`

### Step 3: Deploy

1. Click "Deploy"
2. Wait for build to complete
3. Railway provides a public URL (e.g., `https://otto-production.up.railway.app`)

### Step 4: Verify

```bash
# Health check
curl https://your-otto-url.railway.app/health

# Should return: {"status": "healthy"}
```

## Option 2: Fly.io

### Step 1: Install Fly CLI

```bash
# macOS/Linux
curl -L https://fly.io/install.sh | sh

# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 2: Login

```bash
fly auth login
```

### Step 3: Create Fly App

```bash
cd apps/otto
fly launch --name otto-api --region ord
```

This will:
- Create `fly.toml` config
- Ask about Dockerfile (yes)
- Ask about port (8001)
- Ask about scaling (choose "no" for now)

### Step 4: Configure fly.toml

Edit `fly.toml`:

```toml
app = "otto-api"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[env]
  OTTO_ENV = "prod"

[http_service]
  internal_port = 8001
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[services]]
  http_checks = []
  internal_port = 8001
  processes = ["app"]
  protocol = "tcp"
  script_checks = []

  [services.concurrency]
    hard_limit = 25
    soft_limit = 20
    type = "connections"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.tcp_checks]]
    grace_period = "1s"
    interval = "15s"
    restart_limit = 0
    timeout = "2s"
```

### Step 5: Set Secrets

```bash
fly secrets set LIFE_OS_API_URL=https://your-life-os-backend.fly.dev
fly secrets set OTTO_API_URL=https://otto-api.fly.dev
fly secrets set OTTO_ENV=prod

# Optional deployment tokens
fly secrets set VERCEL_TOKEN=your_token
fly secrets set RENDER_API_KEY=your_key
```

### Step 6: Deploy

```bash
fly deploy
```

### Step 7: Verify

```bash
# Health check
curl https://otto-api.fly.dev/health

# Should return: {"status": "healthy"}
```

## Dockerfile Notes

The Dockerfile uses:
- Python 3.11 slim base image
- `uvicorn` without `[standard]` to avoid Rust dependency
- Health check endpoint at `/health`
- Port 8001 (configurable via `PORT` env var)

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

**Solution:** Railway/Fly.io assign ports automatically. The Dockerfile uses port 8001, but Railway may override with `$PORT`. Update Dockerfile CMD if needed:

```dockerfile
CMD python -m uvicorn otto.api:app --host 0.0.0.0 --port ${PORT:-8001}
```

### Health Check Fails

**Solution:** Ensure the service is running and accessible. Check logs:

```bash
# Railway
railway logs

# Fly.io
fly logs
```

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

## Next Steps

After deployment:

1. **Update Life OS** to point to the new Otto URL
2. **Update any scripts** that call Otto API
3. **Monitor logs** for errors
4. **Set up monitoring** (Railway/Fly.io dashboards)

