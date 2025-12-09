# Project Specifications

This directory contains project specification files that describe infrastructure requirements for your projects.

## Format

Each project spec is a YAML file that defines:
- Project name and description
- Components (web frontend, API backend, etc.)
- Data providers (Supabase projects)
- Payment providers (Stripe)
- Health check endpoints

## Example

See `catered-by-me.yaml` for a complete example.

## Structure

```yaml
name: "project-name"
description: "Brief description"
environment: "prod"

components:
  web:
    provider: "vercel"  # or "render"
    template: "nextjs-marketing-site"
    repo: "owner/repo-name"
    root_dir: "apps/web"
    env_vars:
      SUPABASE_URL: from_provider:supabase:project-name:url
      NEXT_PUBLIC_API_URL: from_env:API_BASE_URL
  
  api:
    provider: "render"
    repo: "owner/repo-name"
    root_dir: "apps/api"
    env_vars:
      SUPABASE_URL: from_provider:supabase:project-name:url

data:
  supabase_project: "project-name"

payments:
  stripe_project: "project-name"

health_checks:
  - name: "api-health"
    url: "https://api.example.com/health"
  - name: "web-health"
    url: "https://example.com/health"
```

## Environment Variable References

Project specs support several ways to reference environment variables:

- `from_env:VAR_NAME` - Get from environment variable
- `from_provider:provider:project:key` - Get from provider config
- `mirror:VAR_NAME` - Copy from another env var in same component
- Direct value - Use the value as-is

## Usage

Use project specs with the `provision-project` and `deploy` commands:

```bash
python tools/infra.py provision-project --spec infra/project-specs/catered-by-me.yaml --env=prod
python tools/infra.py deploy --spec infra/project-specs/catered-by-me.yaml --env=prod
```

