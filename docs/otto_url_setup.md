# Otto URL Configuration

This document explains how to configure the Otto API base URL for use across the monorepo.

## Configuration Priority

The Otto URL is resolved in this order:

1. **Environment variable** `OTTO_BASE_URL` (highest priority)
2. **Config file** `config/otto.json` (fallback)

## Setting the URL

### Option 1: Environment Variable (Recommended for Local Dev)

Set the environment variable in your shell:

**PowerShell:**
```powershell
$env:OTTO_BASE_URL = "https://your-otto-url.onrender.com"
```

**Bash:**
```bash
export OTTO_BASE_URL="https://your-otto-url.onrender.com"
```

**Windows (Permanent):**
1. System Properties → Environment Variables
2. Add `OTTO_BASE_URL` with your URL

### Option 2: Config File (For Committed Defaults)

Edit `config/otto.json`:

```json
{
  "otto_base_url": "https://your-otto-url.onrender.com",
  "health_path": "/health"
}
```

**Note:** If you don't want the production URL in git, keep `config/otto.json` as a placeholder (`"https://REPLACE_ME"`) and use environment variables instead.

## Getting Your Otto URL

After deploying Otto to Render:

1. **Render:**
   - Go to your Render dashboard
   - Click on your Otto web service
   - Copy the public URL from the service overview (e.g., `https://otto-something.onrender.com`)
   - The URL format is: `https://<service-name>.onrender.com`

## Verifying Configuration

Run the health check script:

```powershell
.\scripts\check_otto.ps1
```

This will:
- Read the Otto URL from env or config
- Call `/health` endpoint
- Print status and response
- Exit with code 0 if healthy, 1 if not

## Usage in Scripts

Scripts should use this pattern:

```powershell
# Get Otto URL
$ottoUrl = $env:OTTO_BASE_URL
if (-not $ottoUrl) {
    $config = Get-Content "config\otto.json" | ConvertFrom-Json
    $ottoUrl = $config.otto_base_url
}

# Use the URL
$healthUrl = "$ottoUrl/health"
```

## CI/CD

For CI environments (GitHub Actions, etc.):

1. Set `OTTO_BASE_URL` as a repository secret
2. Export it in your workflow:

```yaml
env:
  OTTO_BASE_URL: ${{ secrets.OTTO_BASE_URL }}
```

## Next.js Apps

For Next.js apps like `apps/symbioz-web`:

1. Set `NEXT_PUBLIC_OTTO_BASE_URL` in `.env.local` (not committed)
2. Use in client components: `process.env.NEXT_PUBLIC_OTTO_BASE_URL`

**Note:** `NEXT_PUBLIC_*` variables are exposed to the browser. Only use for public endpoints.

## Troubleshooting

### "Otto URL not configured"

- Check that `OTTO_BASE_URL` is set, or
- Check that `config/otto.json` has a valid URL (not `REPLACE_ME`)

### Health check fails

- Verify the URL is correct (no trailing slash issues)
- Check that Otto service is deployed and running in Render dashboard
- Verify network access to the URL
- Check Render service logs for errors (Dashboard → Service → Logs tab)

### Script can't find config file

- Ensure you're running from repo root
- Verify `config/otto.json` exists
- Check file permissions


