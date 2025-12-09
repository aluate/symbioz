# Otto - Infra/SRE Bot

**Otto** is your infrastructure automation and diagnostics tool. A single command checks the health of all your services (Render, Supabase, Stripe, GitHub) and provisions new projects automatically - all with zero clicks needed.

---

## Features

### ✅ Diagnostics
Run `python tools/infra.py diag` to:
- Check Render service deployments and health
- Test Supabase database connectivity
- Verify Stripe webhook status
- Check GitHub CI/CD status
- Generate human-readable reports

### ✅ Project Provisioning
Run `python tools/infra.py provision-project` to:
- Create/update Render services via API
- Wire environment variables automatically
- Apply Supabase schemas
- Create Stripe webhooks and products
- All zero-click, fully automated

### ✅ Deployment Management
Run `python tools/infra.py deploy` to:
- Trigger deployments
- Poll for completion
- Run health checks
- Verify everything works

### ✅ Dry-Run Mode
All commands support `--dry-run` flag:
- Validates configurations
- Shows what would be done
- No actual API calls
- Perfect for testing

---

## Catered-by-me Quick Start

Otto is configured specifically for the **catered-by-me** project. Here's how to get started:

### 1. Install Dependencies

```bash
pip install -r infra/requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the repository root with:

```bash
# Required for diagnostics and provisioning
RENDER_API_KEY=your_render_api_key
GITHUB_TOKEN=your_github_token
STRIPE_SECRET_KEY=your_stripe_test_key  # Use TEST mode key!
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=your_service_key

# Optional (can also use SUPABASE_URL + SUPABASE_SERVICE_KEY)
SUPABASE_ACCESS_TOKEN=your_access_token

# App-specific (for provisioning)
SUPABASE_JWT_SECRET=your_jwt_secret
NEXT_PUBLIC_API_BASE_URL=https://catered-by-me.onrender.com
STRIPE_PUBLISHABLE_KEY=your_test_publishable_key
```

**Important:** Use **Stripe TEST mode** keys only. Otto defaults to test mode for safety.

### 3. Fill in TODO Placeholders

Edit these files and replace `TODO_*` placeholders:

- `infra/providers/render.yaml` - Replace `TODO_FILL_RENDER_SERVICE_ID`
- `infra/providers/supabase.yaml` - Replace `TODO_FILL_SUPABASE_PROJECT_REF`
- `infra/providers/stripe.yaml` - Replace `TODO_FILL_STRIPE_WEBHOOK_ID`

### 4. Test with Dry-Run

```bash
# Dry run diagnostics (safe - no API calls)
python tools/infra.py diag --env=prod --dry-run

# Dry run provisioning (shows what would be created)
python tools/infra.py provision-project \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod \
  --dry-run

# Dry run deployment (shows what would be deployed)
python tools/infra.py deploy \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod \
  --dry-run
```

### 5. Run Real Diagnostics (Safe to Run)

Once dry-run looks good:

```bash
python tools/infra.py diag --env=prod
```

Check the output in `diagnostics/latest.md` to see the health of all services.

### 6. Provision and Deploy (When Ready)

Only run these after you've verified dry-run output looks correct:

```bash
# Real provisioning (creates/updates services)
python tools/infra.py provision-project \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod

# Real deployment (triggers deployments and health checks)
python tools/infra.py deploy \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod
```

---

## Quick Start (General)

### 1. Install Dependencies

```bash
pip install -r infra/requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the repository root (don't commit it!):

```bash
# Required
RENDER_API_KEY=your_render_api_key
GITHUB_TOKEN=your_github_token
STRIPE_SECRET_KEY=your_stripe_secret_key

# Optional (can also use SUPABASE_URL + SUPABASE_SERVICE_KEY)
SUPABASE_ACCESS_TOKEN=your_supabase_token

# Your service-specific vars
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=your_service_key
```

### 3. Configure Providers

Edit the YAML files in `infra/providers/`:

- `render.yaml` - Add your Render service IDs
- `supabase.yaml` - Add your Supabase project refs
- `stripe.yaml` - Add your Stripe webhook IDs
- `github.yaml` - Add your GitHub repo paths

### 4. Run Diagnostics

```bash
# Check all providers
python tools/infra.py diag --env=prod

# Dry run (no API calls)
python tools/infra.py diag --env=prod --dry-run

# Check specific providers
python tools/infra.py diag --env=prod --provider render --provider github
```

Reports are saved to:
- `diagnostics/latest.md` - Human-readable summary
- `diagnostics/latest.json` - Machine-readable data
- `diagnostics/raw/` - Raw provider responses (secrets redacted)

### 5. Provision a Project

```bash
# Provision infrastructure from a project spec
python tools/infra.py provision-project \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod

# Dry run first!
python tools/infra.py provision-project \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod \
  --dry-run
```

### 6. Deploy a Project

```bash
# Trigger deployments and run health checks
python tools/infra.py deploy \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod
```

---

## Commands

### `diag` - Run Diagnostics

Check health of all configured services.

```bash
python tools/infra.py diag [OPTIONS]
```

**Options:**
- `--env TEXT` - Environment name (dev, staging, prod) [default: prod]
- `--dry-run` - Run without making API calls
- `--provider TEXT` - Limit to specific providers (can use multiple times)

**Example:**
```bash
python tools/infra.py diag --env=prod
python tools/infra.py diag --env=prod --provider render --provider github
python tools/infra.py diag --dry-run
```

**Output:**
- Console summary with ✅/⚠️/❌ status indicators
- `diagnostics/latest.md` - Full markdown report
- `diagnostics/latest.json` - Structured JSON data
- Exit code: 0 (ok/warn) or 1 (error)

---

### `provision-project` - Provision Infrastructure

Create or update infrastructure for a project from a spec file.

```bash
python tools/infra.py provision-project [OPTIONS]
```

**Options:**
- `--spec TEXT` - Path to project spec YAML file [required]
- `--env TEXT` - Environment name [default: prod]
- `--dry-run` - Show what would be done without making changes

**Example:**
```bash
python tools/infra.py provision-project \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod
```

**What it does:**
1. Reads project spec
2. Creates/updates Render services
3. Sets environment variables
4. Applies Supabase schemas
5. Creates Stripe resources

---

### `deploy` - Deploy and Health Check

Trigger deployments and verify everything works.

```bash
python tools/infra.py deploy [OPTIONS]
```

**Options:**
- `--spec TEXT` - Path to project spec YAML file [required]
- `--env TEXT` - Environment name [default: prod]
- `--dry-run` - Show what would be done without deploying

**Example:**
```bash
python tools/infra.py deploy \
  --spec infra/project-specs/catered-by-me.yaml \
  --env=prod
```

**What it does:**
1. Triggers deployments for all components
2. Waits for deployments to complete
3. Runs health checks from spec
4. Reports success/failure

---

## Configuration Files

### Main Config (`infra/config.yaml`)

Defines environments and required environment variables.

```yaml
default_env: prod

environments:
  prod:
    vercel_team_id: "team_xxx"
    render_owner_id: "user_xxx"
    github_default_branch: "main"

secrets:
  required_env_vars:
    - RENDER_API_KEY
    - GITHUB_TOKEN
    - STRIPE_SECRET_KEY
```

### Provider Configs (`infra/providers/*.yaml`)

One file per provider with service/project configurations.

**Example: `infra/providers/render.yaml`**
```yaml
services:
  catered-by-me-api:
    env: prod
    render_service_id: "srv-xxx"
    repo: "githubuser/catered-by-me"
    branch: "main"
    build_command: "pip install -r requirements.txt"
    start_command: "uvicorn apps.api.main:app --host 0.0.0.0 --port $PORT"
    health_check_path: "/health"
```

### Project Specs (`infra/project-specs/*.yaml`)

Describe complete infrastructure needs for a project.

See `infra/project-specs/README.md` for full documentation.

---

## Environment Variables

Required environment variables (set in `.env` or your shell):

| Variable | Required For | Description |
|----------|-------------|-------------|
| `RENDER_API_KEY` | Render | Render API authentication |
| `GITHUB_TOKEN` | GitHub | GitHub API authentication |
| `STRIPE_SECRET_KEY` | Stripe | Stripe API authentication |
| `SUPABASE_URL` | Supabase | Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Supabase | Supabase service role key |
| `VERCEL_TOKEN` | Vercel | Vercel API token (optional) |

---

## Project Structure

```
infra/
├── CONTROL.md              # Specification document
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── config.yaml             # Main configuration
├── providers/              # Provider configs
│   ├── render.yaml
│   ├── supabase.yaml
│   ├── stripe.yaml
│   ├── github.yaml
│   └── *.py                # Provider client implementations
├── project-specs/          # Project specifications
│   └── catered-by-me.yaml
└── utils/                  # Utility modules
    ├── secrets.py
    ├── yaml_loader.py
    └── ...

tools/
└── infra.py                # Main CLI tool

diagnostics/                # Auto-generated reports
├── latest.md
├── latest.json
├── raw/                    # Raw provider responses
└── history/                # Archived reports
```

---

## Security

**Important security features:**
- ✅ Secrets are never logged or written to files
- ✅ Environment variables required, never hardcoded
- ✅ Raw responses have secrets redacted automatically
- ✅ `.env` file should be in `.gitignore`

**Best practices:**
- Never commit `.env` files
- Use separate API keys for dev/staging/prod
- Regularly rotate API keys
- Use read-only tokens where possible

---

## Troubleshooting

### "Missing required environment variable"

**Solution:** Set the missing variable in your `.env` file or shell.

```bash
export RENDER_API_KEY=your_key_here
```

### "Provider config not found"

**Solution:** Create the provider config file in `infra/providers/` or check the filename matches.

### "Invalid project spec"

**Solution:** Check the YAML syntax and required fields. See `infra/project-specs/README.md` for format.

### "API authentication failed"

**Solution:** Verify your API keys are correct and have the right permissions.

---

## Development

### Adding a New Provider

1. Create provider config file: `infra/providers/newprovider.yaml`
2. Create provider client: `infra/providers/newprovider_client.py`
   - Inherit from `BaseProvider`
   - Implement `check_health()` and `validate_config()`
3. Add to `PROVIDER_CLIENTS` in `tools/infra.py`

### Running Tests

```bash
# Dry-run tests
python tools/infra.py diag --dry-run
python tools/infra.py provision-project --spec infra/project-specs/catered-by-me.yaml --dry-run
```

---

## Future Enhancements

- [ ] Full Vercel integration
- [ ] Prompt → Project spec generation
- [ ] Automated project scaffolding
- [ ] Multi-environment support
- [ ] Slack/email notifications
- [ ] Historical trend analysis

---

## Support

See `infra/CONTROL.md` for full specification and implementation details.

---

**Built with ❤️ for zero-click infrastructure management**
