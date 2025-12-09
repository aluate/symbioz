# Infra/SRE Bot Implementation Plan

**Purpose:** Step-by-step plan to build the Infra/SRE Bot following Frat's CONTROL.md specification.

**Target:** Build everything in one shot after plan review.

**Status:** 📝 Planning — Ready for Review

---

## Overview

This plan breaks down the implementation into logical phases:

1. **Foundation** — Directory structure, config files, CLI skeleton
2. **Diagnostics Core** — Provider clients, health checks, report generation
3. **Project Provisioning** — Create/update services, wire env vars
4. **Deployment** — Trigger deploys, health checks
5. **Testing & Polish** — Example configs, validation, documentation

---

## Phase 1: Foundation & Structure

### 1.1 Directory Structure

Create the complete directory structure:

```
infra/
  CONTROL.md                    ✅ Already created
  IMPLEMENTATION_PLAN.md         ✅ This file
  config.yaml                    ⏳ Create template
  providers/
    render.yaml                  ⏳ Create template
    supabase.yaml                ⏳ Create template
    stripe.yaml                  ⏳ Create template
    github.yaml                  ⏳ Create template
    vercel.yaml                  ⏳ Create template (future)
  project-specs/
    catered-by-me.yaml          ⏳ Create example
    README.md                    ⏳ Create
  providers/
    __init__.py                  ⏳ Create
    base.py                      ⏳ Create provider interface
    render_client.py             ⏳ Create
    supabase_client.py           ⏳ Create
    stripe_client.py             ⏳ Create
    github_client.py             ⏳ Create
    vercel_client.py             ⏳ Create (stub for future)
  utils/
    __init__.py                  ⏳ Create
    secrets.py                   ⏳ Create (redaction logic)
    yaml_loader.py               ⏳ Create
    logging.py                   ⏳ Create

diagnostics/
  latest.md                      ⏳ Auto-generated
  latest.json                    ⏳ Auto-generated
  history/                       ⏳ Auto-created
  raw/                           ⏳ Auto-created
  .gitkeep                       ⏳ Create (for git tracking)

tools/
  infra.py                       ⏳ Create main CLI
  __init__.py                    ⏳ Create
```

**Files to Create:**
- `infra/config.yaml` — Template with environments
- `infra/providers/render.yaml` — Template
- `infra/providers/supabase.yaml` — Template
- `infra/providers/stripe.yaml` — Template
- `infra/providers/github.yaml` — Template
- `infra/providers/vercel.yaml` — Template (placeholder)
- `infra/project-specs/catered-by-me.yaml` — Example project spec
- `infra/project-specs/README.md` — Documentation
- All Python files listed above
- `diagnostics/.gitkeep` — For git tracking

---

### 1.2 CLI Skeleton

Create `tools/infra.py` with:

- Command structure using `click` or `argparse`
- Commands: `diag`, `provision-project`, `deploy`, `--help`
- Environment variable validation
- Config loading logic
- Basic error handling

**Dependencies to Add:**
- `click` or `argparse` (CLI framework)
- `pyyaml` (YAML parsing)
- `python-dotenv` (env var loading)
- `httpx` or `requests` (HTTP client)
- `rich` (optional, for pretty output)

**File:** `tools/infra.py`

---

### 1.3 Provider Interface

Create `infra/providers/base.py` with:

- Abstract base class for providers
- Common interface methods:
  - `check_health() -> ProviderCheckResult`
  - `validate_config() -> bool`
  - `get_status() -> dict`
- Type definitions:
  - `ProviderCheckResult` (TypedDict)
  - Status enum: `"ok" | "warn" | "error"`

**File:** `infra/providers/base.py`

---

### 1.4 Utility Modules

**`infra/utils/secrets.py`:**
- Function to redact secrets from dicts
- Patterns to detect secrets (keys, values)
- Safe logging utilities

**`infra/utils/yaml_loader.py`:**
- Load YAML files with validation
- Merge configs
- Environment-specific config loading

**`infra/utils/logging.py`:**
- Structured logging setup
- Log levels
- File + console output

**Files:**
- `infra/utils/__init__.py`
- `infra/utils/secrets.py`
- `infra/utils/yaml_loader.py`
- `infra/utils/logging.py`

---

## Phase 2: Diagnostics Core

### 2.1 Render Client

Create `infra/providers/render_client.py`:

**Features:**
- Connect to Render API using `RENDER_API_KEY`
- List services for configured service IDs
- Get latest deployment status
- Fetch deployment logs (last N lines)
- Check service health (hit health check URL)
- Handle errors gracefully

**API Endpoints Used:**
- `GET /services/{service_id}`
- `GET /services/{service_id}/deploys`
- `GET /services/{service_id}/deploys/{deploy_id}/logs`

**Return:** `ProviderCheckResult` with:
- Status based on deployment state
- Human summary (e.g., "Deployment failed: KeyError 'SUPABASE_URL'")
- Details (deployment ID, commit, status, error snippets)

**File:** `infra/providers/render_client.py`

---

### 2.2 Supabase Client

Create `infra/providers/supabase_client.py`:

**Features:**
- Test database connection using `SUPABASE_URL` + `SUPABASE_SERVICE_KEY`
- Run simple health query (`SELECT 1`)
- Check project status via Supabase Management API (optional)
- Validate connection env vars are set

**API/Libraries Used:**
- Supabase Python client OR direct PostgreSQL connection
- Management API for project info (optional)

**Return:** `ProviderCheckResult` with:
- Status: "ok" if connection works, "error" if not
- Human summary
- Details (connection test results)

**File:** `infra/providers/supabase_client.py`

---

### 2.3 Stripe Client

Create `infra/providers/stripe_client.py`:

**Features:**
- List recent webhook events (last 24 hours)
- Check webhook endpoint status
- Find failed webhooks
- Test API connectivity

**API Used:**
- Stripe Python SDK
- `stripe.WebhookEndpoint.list()`
- `stripe.Event.list()`

**Return:** `ProviderCheckResult` with:
- Status based on webhook failures
- Human summary (e.g., "2 failed webhooks in last 24h")
- Details (failed webhook IDs, error messages)

**File:** `infra/providers/stripe_client.py`

---

### 2.4 GitHub Client

Create `infra/providers/github_client.py`:

**Features:**
- Check latest commit on configured branch
- Check CI/CD status (GitHub Actions)
- List recent workflow runs
- Check for failing checks

**API Used:**
- GitHub REST API or PyGithub library
- `GET /repos/{owner}/{repo}/commits/{branch}`
- `GET /repos/{owner}/{repo}/actions/runs`

**Return:** `ProviderCheckResult` with:
- Status based on CI status
- Human summary
- Details (last commit, CI status, failing workflows)

**File:** `infra/providers/github_client.py`

---

### 2.5 Diagnostics Orchestrator

Update `tools/infra.py` `diag` command:

**Logic:**
1. Load config files (`infra/config.yaml`, `infra/providers/*.yaml`)
2. Validate required env vars are set
3. For each provider:
   - Load provider config
   - Instantiate provider client
   - Run `check_health()`
   - Collect results
4. Aggregate results:
   - Overall status (worst status wins)
   - Per-provider summaries
5. Generate outputs:
   - `diagnostics/latest.json` (structured)
   - `diagnostics/latest.md` (human-readable)
   - `diagnostics/raw/{provider}-{timestamp}.json` (redacted raw responses)
6. Archive previous diagnostics (optional)
7. Exit with appropriate code (0 = all ok, 1 = errors)

**Markdown Template:**
```markdown
# Diagnostics – {timestamp}

## Overall Status
- {status} API (Render) – {summary}
- {status} Supabase – {summary}
- ...

## {Provider Name}
{human_summary}

{details}

## Suggested Focus
{actionable recommendations}
```

**File:** `tools/infra.py` (update `diag` command)

---

## Phase 3: Project Provisioning

### 3.1 Render Service Provisioning

Extend `infra/providers/render_client.py` with:

**Methods:**
- `ensure_service(spec: dict) -> dict` — Create or update service
- `set_env_vars(service_id: str, env_vars: dict) -> None`
- `get_service(service_id: str) -> dict | None`

**API Used:**
- `POST /services` (create)
- `PATCH /services/{service_id}` (update)
- `PUT /services/{service_id}/env-vars` (set env vars)

**Logic:**
- Check if service exists
- If exists: update if needed
- If not: create new service
- Set environment variables
- Return service info (ID, URL, etc.)

**File:** `infra/providers/render_client.py` (extend)

---

### 3.2 Supabase Schema Management

Extend `infra/providers/supabase_client.py` with:

**Methods:**
- `ensure_project_exists(project_ref: str) -> dict`
- `apply_schema(schema_file: str) -> dict`
- `validate_schema(schema_file: str) -> bool`

**Logic:**
- Check if project exists (via Management API or connection test)
- Read SQL schema file from `infra/sql/`
- Apply migrations (run SQL against database)
- Validate schema applied correctly

**File:** `infra/providers/supabase_client.py` (extend)

---

### 3.3 Stripe Resource Management

Extend `infra/providers/stripe_client.py` with:

**Methods:**
- `ensure_webhook_endpoint(url: str, events: list) -> dict`
- `ensure_product(product_spec: dict) -> dict`
- `ensure_price(product_id: str, price_spec: dict) -> dict`

**Logic:**
- Check if webhook endpoint exists
- Create/update webhook endpoint
- Create/update products and prices from spec
- Return resource IDs

**File:** `infra/providers/stripe_client.py` (extend)

---

### 3.4 Project Spec Parser

Create `infra/utils/project_spec.py`:

**Features:**
- Load and validate project spec YAML
- Resolve environment variable references:
  - `from_env:VAR_NAME`
  - `from_provider:provider:project:key`
  - `mirror:VAR_NAME`
- Validate spec structure
- Generate env var mappings

**File:** `infra/utils/project_spec.py`

---

### 3.5 Provision Command Implementation

Update `tools/infra.py` `provision-project` command:

**Logic:**
1. Load project spec
2. Validate spec structure
3. For each component:
   - Resolve env vars
   - Ensure provider resources exist (Render service, etc.)
   - Set environment variables
4. For data providers:
   - Ensure Supabase project/schema
5. For payments:
   - Ensure Stripe resources
6. Write summary to `diagnostics/latest.*`
7. Return created/updated resources

**File:** `tools/infra.py` (update `provision-project` command)

---

## Phase 4: Deployment

### 4.1 Render Deployment

Extend `infra/providers/render_client.py` with:

**Methods:**
- `trigger_deploy(service_id: str, branch: str = None) -> dict`
- `wait_for_deploy(service_id: str, deploy_id: str, timeout: int = 600) -> dict`
- `get_deploy_status(service_id: str, deploy_id: str) -> dict`

**Logic:**
- Trigger deployment via API
- Poll deployment status
- Wait for completion (or timeout)
- Return final status

**File:** `infra/providers/render_client.py` (extend)

---

### 4.2 Health Check Runner

Create `infra/utils/health_check.py`:

**Features:**
- HTTP health check function
- Retry logic with exponential backoff
- Timeout handling
- Parse response (JSON, text)
- Validate expected status codes

**File:** `infra/utils/health_check.py`

---

### 4.3 Deploy Command Implementation

Update `tools/infra.py` `deploy` command:

**Logic:**
1. Load project spec
2. For each component:
   - Trigger deployment (Render, Vercel, etc.)
   - Wait for completion
3. Run health checks from spec
4. Report results to `diagnostics/latest.*`
5. Exit with appropriate code

**File:** `tools/infra.py` (update `deploy` command)

---

## Phase 5: Testing & Polish

### 5.1 Example Configurations

Create example config files:

**`infra/config.yaml.example`:**
- Template with placeholder values
- Comments explaining each field
- Example environments

**`infra/providers/render.yaml.example`:**
- Example service configuration
- Comments on required fields

**`infra/project-specs/catered-by-me.yaml`:**
- Real example based on Catered By Me project
- All component types (web, api, data, payments)
- Health checks

**Files:**
- `infra/config.yaml.example`
- `infra/providers/*.yaml.example`
- `infra/project-specs/catered-by-me.yaml`

---

### 5.2 Requirements File

Create `infra/requirements.txt`:

```
click>=8.0.0
pyyaml>=6.0
python-dotenv>=1.0.0
httpx>=0.24.0
rich>=13.0.0
stripe>=6.0.0
supabase>=2.0.0
psycopg2-binary>=2.9.0
PyGithub>=1.59.0
```

**File:** `infra/requirements.txt`

---

### 5.3 README Documentation

Create `infra/README.md`:

**Sections:**
- Overview of what the tool does
- Quick start guide
- Environment variable setup
- Example usage
- Configuration guide
- Troubleshooting

**File:** `infra/README.md`

---

### 5.4 Validation & Error Handling

**Add to all provider clients:**
- Input validation
- API error handling (rate limits, auth errors, etc.)
- Retry logic where appropriate
- Clear error messages

**Add to CLI:**
- Validate config files before running
- Check required env vars upfront
- Handle missing files gracefully
- Provide helpful error messages

---

## Implementation Checklist

### Foundation
- [ ] Create directory structure
- [ ] Create config file templates
- [ ] Create CLI skeleton (`tools/infra.py`)
- [ ] Create provider interface (`infra/providers/base.py`)
- [ ] Create utility modules (secrets, yaml, logging)

### Diagnostics Core
- [ ] Implement Render client
- [ ] Implement Supabase client
- [ ] Implement Stripe client
- [ ] Implement GitHub client
- [ ] Implement diagnostics orchestrator
- [ ] Generate markdown reports
- [ ] Generate JSON reports
- [ ] Redact secrets from logs

### Project Provisioning
- [ ] Render service provisioning
- [ ] Supabase schema management
- [ ] Stripe resource management
- [ ] Project spec parser
- [ ] Env var resolution
- [ ] Provision command implementation

### Deployment
- [ ] Render deployment trigger
- [ ] Deployment polling/waiting
- [ ] Health check runner
- [ ] Deploy command implementation

### Testing & Polish
- [ ] Example config files
- [ ] Requirements file
- [ ] README documentation
- [ ] Error handling improvements
- [ ] Validation logic

---

## Dependencies Summary

**Python Packages:**
- `click` — CLI framework
- `pyyaml` — YAML parsing
- `python-dotenv` — Environment variables
- `httpx` — HTTP client (async-capable)
- `rich` — Pretty terminal output
- `stripe` — Stripe SDK
- `supabase` — Supabase client
- `psycopg2-binary` — PostgreSQL driver
- `PyGithub` — GitHub API client

**Environment Variables Required:**
- `RENDER_API_KEY`
- `VERCEL_TOKEN`
- `SUPABASE_ACCESS_TOKEN` (or `SUPABASE_URL` + `SUPABASE_SERVICE_KEY`)
- `STRIPE_SECRET_KEY`
- `GITHUB_TOKEN`

---

## File Structure Summary

```
infra/
├── CONTROL.md                     ✅ Done
├── IMPLEMENTATION_PLAN.md          ✅ This file
├── README.md                       ⏳ Create
├── requirements.txt                ⏳ Create
├── config.yaml                     ⏳ Create
├── providers/
│   ├── __init__.py                ⏳ Create
│   ├── base.py                    ⏳ Create
│   ├── render_client.py           ⏳ Create
│   ├── supabase_client.py         ⏳ Create
│   ├── stripe_client.py           ⏳ Create
│   ├── github_client.py           ⏳ Create
│   ├── vercel_client.py           ⏳ Create (stub)
│   ├── render.yaml                ⏳ Create
│   ├── supabase.yaml              ⏳ Create
│   ├── stripe.yaml                ⏳ Create
│   ├── github.yaml                ⏳ Create
│   └── vercel.yaml                ⏳ Create (stub)
├── project-specs/
│   ├── README.md                  ⏳ Create
│   └── catered-by-me.yaml        ⏳ Create
└── utils/
    ├── __init__.py                ⏳ Create
    ├── secrets.py                 ⏳ Create
    ├── yaml_loader.py             ⏳ Create
    ├── logging.py                 ⏳ Create
    ├── project_spec.py            ⏳ Create
    └── health_check.py            ⏳ Create

diagnostics/
├── .gitkeep                       ⏳ Create
├── latest.md                      ⏳ Auto-generated
├── latest.json                    ⏳ Auto-generated
├── history/                       ⏳ Auto-created
└── raw/                           ⏳ Auto-created

tools/
├── __init__.py                    ⏳ Create
└── infra.py                       ⏳ Create
```

**Total Files to Create:** ~30 files

---

## Testing Strategy

### Unit Tests (Future)
- Provider client methods
- Config loading
- Secret redaction
- Env var resolution

### Integration Tests (Future)
- Full diagnostics run (mock providers)
- Provision project (test mode)
- Deploy flow (test mode)

### Manual Testing
1. Run `diag --env=prod` with real services
2. Validate output format
3. Test error cases (missing env vars, API failures)
4. Test provision-project with test spec
5. Test deploy command

---

## Next Steps After Plan Approval

Once you approve this plan:

1. I'll create all files in the correct structure
2. Implement all functionality according to the phases
3. Add comprehensive error handling
4. Include example configurations
5. Write README documentation
6. Test with Catered By Me project configuration

**Estimated Implementation:** All phases in one comprehensive build.

---

**Ready for Review** — Please review this plan and I'll implement everything at once!

