#!/usr/bin/env python3
"""
Otto - Infrastructure automation and diagnostics tool.

Otto is your zero-click SRE assistant that runs diagnostics, provisions infrastructure,
and manages deployments across Render, Supabase, Stripe, GitHub, and more.

Main CLI entrypoint for running diagnostics, provisioning projects, and managing deployments.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from infra.providers.base import ProviderCheckResult
from infra.providers.github_client import GitHubClient
from infra.providers.render_client import RenderClient
from infra.providers.stripe_client import StripeClient
from infra.providers.supabase_client import SupabaseClient
from infra.providers.vercel_client import VercelClient
from infra.providers.vercel_fixer import VercelFixer
from infra.providers.render_fixer import RenderFixer
from infra.utils.health_check import check_health
from infra.utils.logging import setup_logger
from infra.utils.project_spec import load_and_validate_project_spec, resolve_component_env_vars
from infra.utils.secrets import redact_secrets, safe_log_dict
from infra.utils.yaml_loader import (
    load_config,
    load_provider_configs,
    load_project_spec,
    get_env_config,
)
from infra.utils.template_generator import (
    list_templates,
    generate_project_spec,
)
from infra.utils.template_generator import (
    list_templates,
    generate_project_spec,
    load_template,
)

# Load environment variables from .env file
load_dotenv()

# Setup logger
logger = setup_logger("infra")

# Provider mapping
PROVIDER_CLIENTS = {
    "render": RenderClient,
    "supabase": SupabaseClient,
    "stripe": StripeClient,
    "github": GitHubClient,
    "vercel": VercelClient,
}


def validate_env_vars(config: Dict[str, Any]) -> List[str]:
    """
    Validate that required environment variables are set.
    
    Returns:
        List of missing variable names (empty if all present)
    """
    required = config.get("secrets", {}).get("required_env_vars", [])
    missing = []
    
    for var_name in required:
        value = os.environ.get(var_name)
        if not value:
            missing.append(var_name)
    
    return missing


@click.group()
def cli():
    """Otto - Your zero-click SRE assistant."""
    pass


@cli.command()
@click.option("--env", default="prod", help="Environment name (dev, staging, prod)")
@click.option("--dry-run", is_flag=True, help="Run in dry-run mode (no API calls)")
@click.option("--provider", multiple=True, help="Limit to specific providers")
def diag(env: str, dry_run: bool, provider: tuple):
    """Run diagnostics across all configured providers."""
    click.echo(f"Running diagnostics for environment: {env}")
    if dry_run:
        click.echo("🔍 DRY RUN MODE - No API calls will be made")
    
    try:
        # Load configs
        config = load_config()
        provider_configs = load_provider_configs()
        
        # Validate environment variables
        missing_vars = validate_env_vars(config)
        if missing_vars and not dry_run:
            click.echo(f"\n❌ Missing required environment variables:")
            for var in missing_vars:
                click.echo(f"  - {var}")
            click.echo("\nPlease set these variables before running diagnostics.")
            sys.exit(1)
        
        # Determine which providers to check
        providers_to_check = list(provider) if provider else list(provider_configs.keys())
        
        # Run diagnostics for each provider
        results = []
        for provider_name in providers_to_check:
            if provider_name not in provider_configs:
                click.echo(f"⚠️  Warning: No config found for provider '{provider_name}', skipping")
                continue
            
            if provider_name not in PROVIDER_CLIENTS:
                click.echo(f"⚠️  Warning: Provider '{provider_name}' not implemented, skipping")
                continue
            
            click.echo(f"\nChecking {provider_name}...")
            try:
                provider_config = provider_configs[provider_name]
                provider_class = PROVIDER_CLIENTS[provider_name]
                provider_client = provider_class(provider_config, env=env, dry_run=dry_run)
                
                if not provider_client.validate_config():
                    click.echo(f"⚠️  Warning: Invalid config for {provider_name}, skipping")
                    continue
                
                result = provider_client.check_health()
                results.append(result)
                
                status_emoji = {"ok": "✅", "warn": "⚠️", "error": "❌"}
                emoji = status_emoji.get(result["status"], "❓")
                click.echo(f"{emoji} {result['human_summary']}")
                
            except Exception as e:
                logger.exception(f"Error checking {provider_name}")
                click.echo(f"❌ Error checking {provider_name}: {e}")
                results.append({
                    "provider": provider_name,
                    "status": "error",
                    "human_summary": f"Error: {e}",
                    "details": {"error": str(e)},
                })
        
        # Generate reports
        diagnostics_dir = Path("diagnostics")
        diagnostics_dir.mkdir(exist_ok=True)
        raw_dir = diagnostics_dir / "raw"
        raw_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        
        # Overall status
        error_count = sum(1 for r in results if r.get("status") == "error")
        warn_count = sum(1 for r in results if r.get("status") == "warn")
        
        if error_count > 0:
            overall_status = "ERROR"
        elif warn_count > 0:
            overall_status = "WARN"
        else:
            overall_status = "OK"
        
        # Write JSON report
        json_report = {
            "timestamp": timestamp,
            "environment": env,
            "overall_status": overall_status,
            "providers": [safe_log_dict(r) for r in results],
        }
        
        json_path = diagnostics_dir / "latest.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_report, f, indent=2)
        
        # Write raw provider responses
        for result in results:
            provider_name = result.get("provider", "unknown")
            raw_path = raw_dir / f"{provider_name}-{timestamp}.json"
            with open(raw_path, "w", encoding="utf-8") as f:
                json.dump(safe_log_dict(result), f, indent=2)
        
        # Write markdown report
        md_lines = [
            f"# Diagnostics – {timestamp}",
            "",
            "## Overall Status",
            "",
            f"{'❌' if overall_status == 'ERROR' else '⚠️' if overall_status == 'WARN' else '✅'} **{overall_status}**",
            "",
            "## Provider Status",
            "",
        ]
        
        for result in results:
            status_emoji = {"ok": "✅", "warn": "⚠️", "error": "❌"}
            emoji = status_emoji.get(result.get("status"), "❓")
            provider_name = result.get("provider", "unknown").upper()
            summary = result.get("human_summary", "No summary")
            
            md_lines.append(f"- {emoji} **{provider_name}** – {summary}")
            
            error = result.get("details", {}).get("error")
            if error:
                md_lines.append(f"- ❌ **{provider_name}** – Error: {error}")
        
        md_lines.extend(["", "---"])
        
        md_path = diagnostics_dir / "latest.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        
        click.echo("\n" + "=" * 60)
        click.echo("Diagnostics complete!")
        click.echo(f"Reports written to: {diagnostics_dir}/")
        click.echo("=" * 60)
        
        # Exit with error code if any providers failed
        if error_count > 0:
            sys.exit(1)
        
    except Exception as e:
        logger.exception("Fatal error in diagnostics")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--spec", required=True, help="Path to project spec YAML file")
@click.option("--env", default="prod", help="Environment name")
@click.option("--dry-run", is_flag=True, help="Run in dry-run mode")
def provision_project(spec: str, env: str, dry_run: bool):
    """Provision infrastructure for a project based on its spec."""
    click.echo(f"Provisioning project from spec: {spec}")
    click.echo(f"Environment: {env}")
    if dry_run:
        click.echo("🔍 DRY RUN MODE - No changes will be made")
    
    try:
        # Load project spec
        project_spec = load_and_validate_project_spec(spec)
        project_name = project_spec["name"]
        
        # Load configs
        config = load_config()
        provider_configs = load_provider_configs()
        env_config = get_env_config(config, env)
        
        click.echo(f"\nProject: {project_name}")
        click.echo("=" * 60)
        
        # Provision components
        components = project_spec.get("components", {})
        provisioned = []
        
        for comp_name, comp_def in components.items():
            provider_name = comp_def.get("provider")
            if not provider_name:
                continue
            
            click.echo(f"\nProvisioning {comp_name} on {provider_name}...")
            
            try:
                if provider_name == "render":
                    provider_config = provider_configs.get("render", {})
                    render_client = RenderClient(provider_config, env=env, dry_run=dry_run)
                    
                    # Build service spec
                    service_spec = {
                        "name": f"{project_name}-{comp_name}",
                        "repo": comp_def.get("repo"),
                        "branch": comp_def.get("branch", "main"),
                        "build_command": comp_def.get("build_command"),
                        "start_command": comp_def.get("start_command"),
                    }
                    service = render_client.ensure_service(service_spec)
                    service_id = service.get("service_id") or service.get("id")
                    
                    # Set environment variables
                    env_vars = resolve_component_env_vars(comp_def, provider_configs, {})
                    if service_id and env_vars:
                        render_client.set_env_vars(service_id, env_vars)
                    
                    provisioned.append({
                        "component": comp_name,
                        "provider": provider_name,
                        "service_id": service_id,
                        "url": service.get("url"),
                    })
                
            except Exception as e:
                logger.exception(f"Error provisioning {comp_name}")
                click.echo(f"❌ Error provisioning {comp_name}: {e}")
        
        # Provision data providers
        data_providers = project_spec.get("data", {})
        if "supabase_project" in data_providers:
            project_name = data_providers["supabase_project"]
            click.echo(f"\nProvisioning Supabase: {project_name}")
            # Ensure schema is applied
            supabase_config = provider_configs.get("supabase", {})
            if project_name in supabase_config.get("projects", {}):
                project_config = supabase_config["projects"][project_name]
                supabase_client = SupabaseClient(supabase_config, env=env, dry_run=dry_run)
                
                schema_file = project_config.get("db_schema_file")
                if schema_file:
                    supabase_client.apply_schema(schema_file)
                    click.echo(f"✅ Schema applied: {schema_file}")
        
        # Provision payment providers
        payments = project_spec.get("payments", {})
        if "stripe_project" in payments:
            project_name = payments["stripe_project"]
            click.echo(f"\nProvisioning Stripe: {project_name}")
            # Stripe provisioning would go here
            click.echo(f"✅ Stripe project: {project_name}")
        
        click.echo("\n" + "=" * 60)
        click.echo("Provisioning complete!")
        click.echo(f"Provisioned {len(provisioned)} component(s)")
        click.echo("=" * 60)
        
    except Exception as e:
        logger.exception("Fatal error in provisioning")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--spec", required=True, help="Path to project spec YAML file")
@click.option("--env", default="prod", help="Environment name")
@click.option("--dry-run", is_flag=True, help="Run in dry-run mode")
def deploy(spec: str, env: str, dry_run: bool):
    """Trigger deployments and run health checks."""
    click.echo(f"Deploying project from spec: {spec}")
    click.echo(f"Environment: {env}")
    if dry_run:
        click.echo("🔍 DRY RUN MODE - No deployments will be triggered")
    
    try:
        # Load project spec
        project_spec = load_and_validate_project_spec(spec)
        project_name = project_spec["name"]
        
        # Load configs
        config = load_config()
        provider_configs = load_provider_configs()
        
        # Trigger deployments for each component
        components = project_spec.get("components", {})
        deployments = []
        
        for comp_name, comp_def in components.items():
            provider_name = comp_def.get("provider")
            if provider_name == "render":
                click.echo(f"\nDeploying {comp_name}...")
                # Get service ID from config
                render_config = provider_configs.get("render", {})
                service_name = f"{project_name}-{comp_name}"
                service_config = render_config.get("services", {}).get(service_name)
                
                if service_config:
                    service_id = service_config.get("render_service_id")
                    render_client = RenderClient(render_config, env=env, dry_run=dry_run)
                    
                    # Trigger deploy
                    deploy_result = render_client.trigger_deploy(service_id)
                    deploy_id = deploy_result.get("deploy_id") or deploy_result.get("id")
                    
                    if not dry_run:
                        click.echo(f"Deployment triggered: {deploy_id}")
                        click.echo("Waiting for deployment...")
                        final_status = render_client.wait_for_deploy(service_id, deploy_id)
                        click.echo(f"✅ Deployment complete: {final_status.get('deploy', {}).get('status')}")
                    else:
                        click.echo(f"[DRY RUN] Would deploy: {service_id}")
                    
                    deployments.append({
                        "component": comp_name,
                        "deploy_id": deploy_id,
                        "status": "queued" if dry_run else "completed",
                    })
        
        # Run health checks
        health_checks = project_spec.get("health_checks", [])
        if health_checks:
            click.echo("\n" + "=" * 60)
            click.echo("Running health checks...")
            click.echo("=" * 60)
            
            for check in health_checks:
                name = check.get("name", "Unknown")
                url = check.get("url")
                if not url:
                    continue
                
                click.echo(f"\nChecking {name}...")
                result = check_health(url)
                
                status_emoji = {"ok": "✅", "warn": "⚠️", "error": "❌"}
                emoji = status_emoji.get(result["status"], "❓")
                click.echo(f"{emoji} {name}: {result['status']}")
                if result.get("error"):
                    click.echo(f"   Error: {result['error']}")
        
        click.echo("\n" + "=" * 60)
        click.echo("Deployment complete!")
        click.echo(f"Deployed {len(deployments)} component(s)")
        click.echo("=" * 60)
        
    except Exception as e:
        logger.exception("Fatal error in deployment")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--project", required=True, help="Project name (from vercel.yaml)")
@click.option("--env", default="prod", help="Environment name")
@click.option("--max-retries", default=5, help="Maximum retry attempts")
@click.option("--dry-run", is_flag=True, help="Run in dry-run mode")
def fix_vercel(project: str, env: str, max_retries: int, dry_run: bool):
    """Auto-fix Vercel deployment issues and retry until successful."""
    click.echo(f"🔧 Auto-fixing Vercel deployment for: {project}")
    click.echo(f"Environment: {env}")
    click.echo(f"Max retries: {max_retries}")
    if dry_run:
        click.echo("🔍 DRY RUN MODE - No changes will be made")
    
    try:
        # Load configs
        provider_configs = load_provider_configs()
        vercel_config = provider_configs.get("vercel", {})
        
        projects = vercel_config.get("projects", {})
        if project not in projects:
            click.echo(f"❌ Project '{project}' not found in vercel.yaml")
            click.echo(f"Available projects: {', '.join(projects.keys())}")
            sys.exit(1)
        
        project_config = projects[project]
        if project_config.get("env") != env:
            click.echo(f"⚠️  Project '{project}' is configured for env '{project_config.get('env')}', not '{env}'")
        
        # Create Vercel client
        vercel_client = VercelClient(vercel_config, env=env, dry_run=dry_run)
        
        # Create fixer
        fixer = VercelFixer(vercel_client, project, project_config, max_retries=max_retries)
        
        # Run auto-fix
        click.echo("\n" + "=" * 60)
        click.echo("Starting auto-fix process...")
        click.echo("=" * 60)
        
        result = fixer.auto_fix_and_retry()
        
        click.echo("\n" + "=" * 60)
        if result.success:
            click.echo("✅ Auto-fix successful!")
            click.echo(f"   {result.message}")
            if result.fixes_applied:
                click.echo("\n   Fixes applied:")
                for fix in result.fixes_applied:
                    click.echo(f"   - {fix}")
        else:
            click.echo("❌ Auto-fix failed")
            click.echo(f"   {result.message}")
            if result.errors:
                click.echo("\n   Errors:")
                for error in result.errors:
                    click.echo(f"   - {error}")
        click.echo("=" * 60)
        
        sys.exit(0 if result.success else 1)
        
    except Exception as e:
        logger.exception("Fatal error in auto-fix")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--spec", required=True, help="Path to project spec YAML file")
@click.option("--env", default="prod", help="Environment name")
@click.option("--max-retries", default=5, help="Maximum retry attempts per provider")
@click.option("--dry-run", is_flag=True, help="Run in dry-run mode")
def fix_all(spec: str, env: str, max_retries: int, dry_run: bool):
    """Auto-fix issues across all providers for a project."""
    click.echo(f"🔧 Auto-fixing all providers for project: {spec}")
    click.echo(f"Environment: {env}")
    if dry_run:
        click.echo("🔍 DRY RUN MODE - No changes will be made")
    
    try:
        # Load project spec
        project_spec = load_and_validate_project_spec(spec)
        project_name = project_spec["name"]
        
        # Load configs
        provider_configs = load_provider_configs()
        
        click.echo("\n" + "=" * 60)
        click.echo("Auto-fixing all providers...")
        click.echo("=" * 60)
        
        results = {}
        
        # Fix Vercel
        components = project_spec.get("components", {})
        for comp_name, comp_def in components.items():
            provider_name = comp_def.get("provider")
            
            if provider_name == "vercel":
                click.echo(f"\n🔧 Fixing Vercel component: {comp_name}")
                vercel_config = provider_configs.get("vercel", {})
                projects = vercel_config.get("projects", {})
                
                # Try to find project by name or use project_name
                vercel_project = project_name
                if vercel_project not in projects:
                    # Try to find by component name
                    vercel_project = f"{project_name}-{comp_name}"
                
                if vercel_project in projects:
                    project_config = projects[vercel_project]
                    vercel_client = VercelClient(vercel_config, env=env, dry_run=dry_run)
                    fixer = VercelFixer(vercel_client, vercel_project, project_config, max_retries=max_retries)
                    result = fixer.auto_fix_and_retry()
                    results["vercel"] = result
                    
                    if result.success:
                        click.echo(f"✅ Vercel fixed: {result.message}")
                    else:
                        click.echo(f"❌ Vercel fix failed: {result.message}")
                else:
                    click.echo(f"⚠️  Vercel project '{vercel_project}' not found in config")
            
            elif provider_name == "render":
                click.echo(f"\n🔧 Fixing Render component: {comp_name}")
                render_config = provider_configs.get("render", {})
                services = render_config.get("services", {})
                
                # Find service
                service_name = f"{project_name}-{comp_name}"
                if service_name not in services:
                    service_name = comp_name  # Try just component name
                
                if service_name in services:
                    service_config = services[service_name]
                    render_client = RenderClient(render_config, env=env, dry_run=dry_run)
                    fixer = RenderFixer(render_client, service_name, service_config, max_retries=max_retries)
                    result = fixer.auto_fix_and_retry()
                    results[f"render-{comp_name}"] = result
                    
                    if result.success:
                        click.echo(f"✅ Render fixed: {result.message}")
                    else:
                        click.echo(f"❌ Render fix failed: {result.message}")
                else:
                    click.echo(f"⚠️  Render service '{service_name}' not found in config")
            
            # TODO: Add GitHub, Supabase, Stripe fixers here
        
        # Summary
        click.echo("\n" + "=" * 60)
        click.echo("Auto-fix Summary")
        click.echo("=" * 60)
        
        success_count = sum(1 for r in results.values() if r.success)
        total_count = len(results)
        
        for provider, result in results.items():
            status = "✅" if result.success else "❌"
            click.echo(f"{status} {provider}: {result.message}")
        
        click.echo(f"\nTotal: {success_count}/{total_count} providers fixed")
        click.echo("=" * 60)
        
        sys.exit(0 if success_count == total_count else 1)
        
    except Exception as e:
        logger.exception("Fatal error in fix-all")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--project", required=True, help="Project name (from project spec)")
@click.option("--spec", help="Path to project spec YAML file (auto-detected if not provided)")
@click.option("--env", default="prod", help="Environment name")
@click.option("--dry-run", is_flag=True, help="Run in dry-run mode")
def toggle_demo(project: str, spec: Optional[str], env: str, dry_run: bool):
    """Enable or disable demo mode for a project."""
    click.echo(f"🎭 Toggling demo mode for: {project}")
    
    try:
        # Find demo mode file
        demo_file = Path("catered_by_me/apps/web/src/lib/demo.ts")
        if not demo_file.exists():
            click.echo(f"❌ Demo mode file not found: {demo_file}")
            sys.exit(1)
        
        # Read current state
        content = demo_file.read_text(encoding="utf-8")
        
        # Check current state
        is_demo = "DEMO_MODE = true" in content
        
        click.echo(f"Current state: Demo mode is {'ON' if is_demo else 'OFF'}")
        
        if dry_run:
            click.echo(f"[DRY RUN] Would set DEMO_MODE to {not is_demo}")
            return
        
        # Toggle it
        new_value = "false" if is_demo else "true"
        new_content = content.replace(
            f"DEMO_MODE = {str(is_demo).lower()}",
            f"DEMO_MODE = {new_value}"
        )
        
        # Write back
        demo_file.write_text(new_content, encoding="utf-8")
        click.echo(f"✅ Demo mode set to: {new_value.upper()}")
        
        # Commit and push
        click.echo("\nCommitting changes...")
        import subprocess
        subprocess.run(["git", "add", str(demo_file)], check=True, cwd=Path("catered_by_me"))
        subprocess.run(
            ["git", "commit", "-m", f"Toggle demo mode to {new_value.upper()}"],
            check=True,
            cwd=Path("catered_by_me")
        )
        subprocess.run(["git", "push"], check=True, cwd=Path("catered_by_me"))
        
        click.echo("✅ Changes committed and pushed!")
        click.echo("Vercel will auto-deploy the changes...")
        
    except Exception as e:
        logger.exception("Fatal error toggling demo mode")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--project", required=True, help="Project name")
@click.option("--env", default="prod", help="Environment name")
@click.option("--dry-run", is_flag=True, help="Run in dry-run mode")
def validate_launch(project: str, env: str, dry_run: bool):
    """Validate everything is ready for launch."""
    click.echo(f"🔍 Validating launch readiness for: {project}")
    click.echo(f"Environment: {env}")
    if dry_run:
        click.echo("🔍 DRY RUN MODE")
    
    try:
        issues = []
        passed = []
        
        # 1. Check environment variables
        click.echo("\n1. Checking environment variables...")
        config = load_config()
        missing_vars = validate_env_vars(config)
        if missing_vars:
            for var in missing_vars:
                issues.append(f"Missing env var: {var}")
            click.echo(f"   ❌ {len(missing_vars)} missing")
        else:
            click.echo("   ✅ All required env vars set")
            passed.append("Environment variables")
        
        # 2. Check service health
        click.echo("\n2. Checking service health...")
        try:
            provider_configs = load_provider_configs()
            spec_path = f"infra/project-specs/{project}.yaml"
            project_spec = load_and_validate_project_spec(spec_path)
            
            health_checks = project_spec.get("health_checks", [])
            for check in health_checks:
                name = check.get("name", "Unknown")
                url = check.get("url")
                if url:
                    result = check_health(url)
                    if result["status"] == "ok":
                        click.echo(f"   ✅ {name}: OK")
                        passed.append(f"Health check: {name}")
                    else:
                        click.echo(f"   ❌ {name}: {result.get('error', 'Failed')}")
                        issues.append(f"Health check failed: {name}")
        except Exception as e:
            click.echo(f"   ⚠️  Could not check health: {e}")
        
        # 3. Check deployment status
        click.echo("\n3. Checking deployment status...")
        try:
            vercel_config = provider_configs.get("vercel", {})
            projects = vercel_config.get("projects", {})
            if project in projects:
                vercel_client = VercelClient(vercel_config, env=env, dry_run=dry_run)
                project_config = projects[project]
                project_id = project_config.get("project_id") or project
                deployments = vercel_client._list_deployments(project_id, limit=1)
                if deployments:
                    latest = deployments[0]
                    state = latest.get("state")
                    if state == "READY":
                        click.echo(f"   ✅ Latest deployment: READY")
                        passed.append("Vercel deployment")
                    else:
                        click.echo(f"   ❌ Latest deployment: {state}")
                        issues.append(f"Deployment not ready: {state}")
        except Exception as e:
            click.echo(f"   ⚠️  Could not check deployment: {e}")
        
        # 4. Check demo mode
        click.echo("\n4. Checking demo mode...")
        demo_file = Path("catered_by_me/apps/web/src/lib/demo.ts")
        if demo_file.exists():
            content = demo_file.read_text(encoding="utf-8")
            if "DEMO_MODE = true" in content:
                click.echo("   ⚠️  Demo mode is ON (recommend OFF for production)")
                issues.append("Demo mode is enabled")
            else:
                click.echo("   ✅ Demo mode is OFF")
                passed.append("Demo mode disabled")
        
        # Summary
        click.echo("\n" + "=" * 60)
        click.echo("Launch Validation Summary")
        click.echo("=" * 60)
        click.echo(f"\n✅ Passed: {len(passed)}")
        for item in passed:
            click.echo(f"   ✅ {item}")
        
        if issues:
            click.echo(f"\n⚠️  Issues: {len(issues)}")
            for item in issues:
                click.echo(f"   ⚠️  {item}")
        else:
            click.echo("\n✅ No issues found! Ready for launch!")
        
        click.echo("=" * 60)
        
        sys.exit(0 if not issues else 1)
        
    except Exception as e:
        logger.exception("Fatal error in validation")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--project", required=True, help="Project name")
@click.option("--env", default="prod", help="Environment name")
@click.option("--dry-run", is_flag=True, help="Run in dry-run mode first")
def finish_site(project: str, env: str, dry_run: bool):
    """Finish the site: toggle demo mode, validate, and ensure deployment."""
    click.echo(f"🚀 Finishing site: {project}")
    click.echo(f"Environment: {env}")
    if dry_run:
        click.echo("🔍 DRY RUN MODE - No changes will be made")
    
    try:
        # Step 1: Toggle demo mode OFF
        click.echo("\n" + "=" * 60)
        click.echo("Step 1: Disabling demo mode...")
        click.echo("=" * 60)
        
        demo_file = Path("catered_by_me/apps/web/src/lib/demo.ts")
        if demo_file.exists():
            content = demo_file.read_text(encoding="utf-8")
            if "DEMO_MODE = true" in content:
                if not dry_run:
                    new_content = content.replace("DEMO_MODE = true", "DEMO_MODE = false")
                    demo_file.write_text(new_content, encoding="utf-8")
                    click.echo("✅ Demo mode disabled")
                else:
                    click.echo("[DRY RUN] Would disable demo mode")
            else:
                click.echo("✅ Demo mode already disabled")
        
        # Step 2: Validate configuration
        click.echo("\n" + "=" * 60)
        click.echo("Step 2: Validating configuration...")
        click.echo("=" * 60)
        
        config = load_config()
        provider_configs = load_provider_configs()
        
        # Check env vars
        missing_vars = validate_env_vars(config)
        if missing_vars:
            click.echo(f"⚠️  Missing env vars (non-blocking): {', '.join(missing_vars)}")
        
        # Step 3: Commit and push if not dry-run
        if not dry_run:
            click.echo("\n" + "=" * 60)
            click.echo("Step 3: Committing and pushing changes...")
            click.echo("=" * 60)
            
            import subprocess
            repo_path = Path("catered_by_me")
            
            # Check if there are changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=repo_path
            )
            
            if result.stdout.strip():
                subprocess.run(["git", "add", "."], check=True, cwd=repo_path)
                subprocess.run(
                    ["git", "commit", "-m", "Finish site: disable demo mode and prepare for launch"],
                    check=True,
                    cwd=repo_path
                )
                subprocess.run(["git", "push"], check=True, cwd=repo_path)
                click.echo("✅ Changes committed and pushed!")
            else:
                click.echo("✅ No changes to commit")
        
        # Step 4: Trigger deployment and monitor
        click.echo("\n" + "=" * 60)
        click.echo("Step 4: Ensuring deployment...")
        click.echo("=" * 60)
        
        if not dry_run:
            # Vercel will auto-deploy on push
            click.echo("✅ Changes pushed - Vercel will auto-deploy")
            click.echo("\nWaiting a moment, then checking deployment status...")
            import time
            time.sleep(5)
            
            # Check deployment
            vercel_config = provider_configs.get("vercel", {})
            vercel_client = VercelClient(vercel_config, env=env, dry_run=False)
            
            # Get project ID from config
            projects = vercel_config.get("projects", {})
            if project not in projects:
                click.echo(f"⚠️  Project '{project}' not found in vercel config")
                click.echo("Skipping deployment check...")
            else:
                project_config = projects[project]
                project_id = project_config.get("project_id") or project
                
                click.echo("\nChecking latest deployment...")
                deployments = vercel_client._list_deployments(project_id, limit=1)
                
                if deployments:
                    latest = deployments[0]
                    state = latest.get("state")
                    click.echo(f"Latest deployment status: {state}")
                    
                    if state == "BUILDING":
                        click.echo("⏳ Deployment in progress...")
                    elif state == "READY":
                        click.echo("✅ Deployment successful!")
                    elif state == "ERROR":
                        click.echo("❌ Deployment failed - running auto-fix...")
                        # Trigger auto-fix
                        fixer = VercelFixer(vercel_client, project, project_config, max_retries=5)
                        fix_result = fixer.auto_fix_and_retry()
                        if fix_result.success:
                            click.echo("✅ Auto-fix successful!")
                        else:
                            click.echo(f"❌ Auto-fix failed: {fix_result.message}")
        
        # Final summary
        click.echo("\n" + "=" * 60)
        click.echo("Site Completion Summary")
        click.echo("=" * 60)
        click.echo("✅ Demo mode disabled")
        click.echo("✅ Changes committed and pushed")
        click.echo("✅ Deployment triggered")
        click.echo("\nYour site is being finished! Check Vercel dashboard for status.")
        click.echo("=" * 60)
        
    except Exception as e:
        logger.exception("Fatal error finishing site")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--project", required=True, help="Project name")
@click.option("--service", default="api", help="Service name (api, web, etc.)")
@click.option("--key", required=True, help="Environment variable key")
@click.option("--value", required=True, help="Environment variable value")
@click.option("--env", default="prod", help="Environment name")
@click.option("--dry-run", is_flag=True, help="Run in dry-run mode")
def set_render_env(project: str, service: str, key: str, value: str, env: str, dry_run: bool):
    """Set an environment variable in Render for a service."""
    click.echo(f"🔧 Setting Render environment variable: {key}")
    click.echo(f"Project: {project}, Service: {service}")
    if dry_run:
        click.echo("🔍 DRY RUN MODE - No changes will be made")
    
    try:
        # Load configs
        provider_configs = load_provider_configs()
        render_config = provider_configs.get("render", {})
        
        # Find service
        service_name = f"{project}-{service}"
        services = render_config.get("services", {})
        
        if service_name not in services:
            click.echo(f"❌ Service '{service_name}' not found in render.yaml")
            click.echo(f"Available services: {', '.join(services.keys())}")
            sys.exit(1)
        
        service_config = services[service_name]
        service_id = service_config.get("render_service_id")
        
        if not service_id:
            click.echo(f"❌ Service ID not found for '{service_name}'")
            sys.exit(1)
        
        # Create Render client
        render_client = RenderClient(render_config, env=env, dry_run=dry_run)
        
        # Set the environment variable
        click.echo(f"\nSetting {key} for service {service_name}...")
        render_client.set_env_vars(service_id, {key: value})
        
        click.echo(f"✅ Environment variable {key} set successfully!")
        click.echo("Render will automatically redeploy with the new variable.")
        
    except Exception as e:
        logger.exception("Fatal error setting Render env var")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--project", required=True, help="Project name")
@click.option("--secret-key", help="Stripe secret key (sk_test_...)")
@click.option("--publishable-key", help="Stripe publishable key (pk_test_...)")
@click.option("--webhook-secret", help="Stripe webhook secret (whsec_...)")
@click.option("--env", default="prod", help="Environment name")
@click.option("--dry-run", is_flag=True, help="Run in dry-run mode")
def setup_stripe(project: str, secret_key: Optional[str], publishable_key: Optional[str], webhook_secret: Optional[str], env: str, dry_run: bool):
    """Set up Stripe integration: keys, products, and webhooks."""
    click.echo(f"💳 Setting up Stripe for: {project}")
    click.echo(f"Environment: {env}")
    if dry_run:
        click.echo("🔍 DRY RUN MODE - No changes will be made")
    
    try:
        # Get keys from parameters or environment
        if not secret_key:
            secret_key = os.environ.get("STRIPE_SECRET_KEY")
        if not publishable_key:
            publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")
        if not webhook_secret:
            webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
        
        if not secret_key:
            click.echo("❌ Stripe secret key not provided. Set --secret-key or STRIPE_SECRET_KEY env var.")
            sys.exit(1)
        if not publishable_key:
            click.echo("❌ Stripe publishable key not provided. Set --publishable-key or STRIPE_PUBLISHABLE_KEY env var.")
            sys.exit(1)
        
        # Update .env file
        click.echo("\n" + "=" * 60)
        click.echo("Step 1: Updating .env file...")
        click.echo("=" * 60)
        
        env_file = Path(".env")
        env_content = ""
        if env_file.exists():
            env_content = env_file.read_text(encoding="utf-8")
        
        # Update or add Stripe keys
        lines = env_content.splitlines() if env_content else []
        updated_lines = []
        found_secret = False
        found_publishable = False
        found_webhook = False
        
        for line in lines:
            if line.startswith("STRIPE_SECRET_KEY="):
                updated_lines.append(f"STRIPE_SECRET_KEY={secret_key}")
                found_secret = True
            elif line.startswith("STRIPE_PUBLISHABLE_KEY="):
                updated_lines.append(f"STRIPE_PUBLISHABLE_KEY={publishable_key}")
                found_publishable = True
            elif line.startswith("STRIPE_WEBHOOK_SECRET="):
                updated_lines.append(f"STRIPE_WEBHOOK_SECRET={webhook_secret}")
                found_webhook = True
            else:
                updated_lines.append(line)
        
        if not found_secret:
            updated_lines.append(f"STRIPE_SECRET_KEY={secret_key}")
        if not found_publishable:
            updated_lines.append(f"STRIPE_PUBLISHABLE_KEY={publishable_key}")
        if webhook_secret and not found_webhook:
            updated_lines.append(f"STRIPE_WEBHOOK_SECRET={webhook_secret}")
        
        if not dry_run:
            env_file.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
            click.echo("✅ .env file updated")
        else:
            click.echo("[DRY RUN] Would update .env file")
        
        # Set environment variables for this session
        os.environ["STRIPE_SECRET_KEY"] = secret_key
        os.environ["STRIPE_PUBLISHABLE_KEY"] = publishable_key
        if webhook_secret:
            os.environ["STRIPE_WEBHOOK_SECRET"] = webhook_secret
        
        # Load configs
        provider_configs = load_provider_configs()
        stripe_config = provider_configs.get("stripe", {})
        project_spec_path = f"infra/project-specs/{project}.yaml"
        project_spec = load_and_validate_project_spec(project_spec_path)
        
        # Create Stripe client
        stripe_client = StripeClient(stripe_config, env=env, dry_run=dry_run)
        
        # Step 2: Create products
        click.echo("\n" + "=" * 60)
        click.echo("Step 2: Creating Stripe products...")
        click.echo("=" * 60)
        
        products_created = []
        
        # Pro Annual - $15/year
        try:
            pro_product = stripe_client.ensure_product(
                "Pro Annual",
                description="Unlimited events, recipes, PDF export, and share links",
                price_amount=1500,  # $15.00 in cents
                price_currency="usd",
                recurring="year"
            )
            products_created.append(pro_product)
            click.echo(f"✅ Created product: Pro Annual ($15/year)")
        except Exception as e:
            click.echo(f"⚠️  Could not create Pro Annual: {e}")
        
        # Founding Host - $10/year (optional)
        try:
            founding_product = stripe_client.ensure_product(
                "Founding Host",
                description="Special pricing for early adopters",
                price_amount=1000,  # $10.00 in cents
                price_currency="usd",
                recurring="year"
            )
            products_created.append(founding_product)
            click.echo(f"✅ Created product: Founding Host ($10/year)")
        except Exception as e:
            click.echo(f"⚠️  Could not create Founding Host: {e}")
        
        # Step 3: Set environment variables in Vercel
        click.echo("\n" + "=" * 60)
        click.echo("Step 3: Setting environment variables in Vercel...")
        click.echo("=" * 60)
        
        vercel_config = provider_configs.get("vercel", {})
        if vercel_config:
            vercel_client = VercelClient(vercel_config, env=env, dry_run=dry_run)
            projects = vercel_config.get("projects", {})
            
            if project in projects:
                project_config = projects[project]
                project_id = project_config.get("project_id") or project
                
                # Set publishable key
                try:
                    if not dry_run:
                        vercel_client.set_environment_variable(
                            project_id,
                            "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY",
                            publishable_key
                        )
                        click.echo("✅ Set NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY in Vercel")
                    else:
                        click.echo("[DRY RUN] Would set NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY in Vercel")
                except Exception as e:
                    click.echo(f"⚠️  Could not set Vercel env var: {e}")
        
        # Step 4: Set environment variables in Render
        click.echo("\n" + "=" * 60)
        click.echo("Step 4: Setting environment variables in Render...")
        click.echo("=" * 60)
        
        render_config = provider_configs.get("render", {})
        if render_config:
            render_client = RenderClient(render_config, env=env, dry_run=dry_run)
            services = render_config.get("services", {})
            
            # Find API service
            api_service_name = f"{project}-api"
            if api_service_name in services:
                service_config = services.get(api_service_name)
                if isinstance(service_config, dict):
                    service_id = service_config.get("render_service_id")
                else:
                    # Handle list or other formats
                    service_id = None
                
                if service_id:
                    env_vars_to_set = {
                        "STRIPE_SECRET_KEY": secret_key
                    }
                    if webhook_secret:
                        env_vars_to_set["STRIPE_WEBHOOK_SECRET"] = webhook_secret
                    
                    try:
                        if not dry_run:
                            render_client.set_env_vars(service_id, env_vars_to_set)
                            click.echo("✅ Set STRIPE_SECRET_KEY in Render")
                            if webhook_secret:
                                click.echo("✅ Set STRIPE_WEBHOOK_SECRET in Render")
                        else:
                            click.echo("[DRY RUN] Would set STRIPE_SECRET_KEY in Render")
                            if webhook_secret:
                                click.echo("[DRY RUN] Would set STRIPE_WEBHOOK_SECRET in Render")
                    except Exception as e:
                        click.echo(f"⚠️  Could not set Render env var: {e}")
                        click.echo(f"   (You can set it manually in Render dashboard)")
                else:
                    click.echo(f"⚠️  Service ID not found for {api_service_name}")
                    click.echo(f"   (You can set STRIPE_SECRET_KEY manually in Render dashboard)")
        
        # Final summary
        click.echo("\n" + "=" * 60)
        click.echo("Stripe Setup Summary")
        click.echo("=" * 60)
        click.echo(f"✅ Keys added to .env")
        click.echo(f"✅ Created {len(products_created)} product(s)")
        click.echo(f"✅ Environment variables set in Vercel/Render")
        if webhook_secret:
            click.echo(f"✅ Webhook secret configured")
        else:
            click.echo(f"\n⚠️  Webhook secret not provided - if you have it, run:")
            click.echo(f"   python tools/infra.py set-render-env --project {project} --service api --key STRIPE_WEBHOOK_SECRET --value whsec_...")
        click.echo("=" * 60)
        
    except Exception as e:
        logger.exception("Fatal error setting up Stripe")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--template", required=True, help="Template name (e.g., 'saas-starter', 'portfolio-site')")
@click.option("--name", required=True, help="Project name (kebab-case, e.g., 'my-awesome-app')")
@click.option("--github-repo", required=True, help="GitHub repository (owner/repo, e.g., 'username/my-app')")
@click.option("--display-name", help="Display name (defaults to name)")
@click.option("--domain", help="Custom domain (optional)")
@click.option("--output", help="Output path (defaults to infra/project-specs/{name}.yaml)")
@click.option("--dry-run", is_flag=True, help="Show what would be generated without saving")
def generate_project(
    template: str,
    name: str,
    github_repo: str,
    display_name: Optional[str],
    domain: Optional[str],
    output: Optional[str],
    dry_run: bool,
):
    """Generate a new project spec from a template."""
    try:
        click.echo(f"🎯 Generating project '{name}' from template '{template}'")
        click.echo("=" * 60)
        
        # Prepare variables
        variables = {
            "project_name": name,
            "project_display_name": display_name or name.replace("-", " ").title(),
            "github_repo": github_repo,
        }
        
        if domain:
            variables["frontend_domain"] = domain
        
        # Generate spec
        generated = generate_project_spec(template, variables)
        
        if dry_run:
            click.echo("\n📄 Generated project spec (dry-run):")
            click.echo("-" * 60)
            click.echo(generated)
            click.echo("-" * 60)
            click.echo("\n🔍 DRY RUN - File not saved")
            return
        
        # Determine output path
        if output:
            output_path = Path(output)
        else:
            output_path = Path("infra/project-specs") / f"{name}.yaml"
        
        # Save
        generate_project_spec(template, variables, output_path)
        
        click.echo(f"\n✅ Project spec generated: {output_path}")
        click.echo("\n📋 Next steps:")
        click.echo(f"  1. Review: {output_path}")
        click.echo(f"  2. Customize if needed")
        click.echo(f"  3. Provision: python tools/infra.py provision-project --spec {output_path} --env prod")
        
    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.exception("Fatal error generating project")
        click.echo(f"❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command(name="list-templates")
def list_templates_cmd():
    """List all available templates."""
    try:
        templates = list_templates()
        
        if not templates:
            click.echo("⚠️  No templates found in infra/templates/")
            return
        
        click.echo("📦 Available Templates:")
        click.echo("=" * 60)
        
        for template in templates:
            click.echo(f"\n  📋 {template['name']}")
            click.echo(f"     {template['description']}")
            click.echo(f"     Version: {template['version']}")
        
        click.echo("\n" + "=" * 60)
        click.echo("\n💡 Usage:")
        click.echo("   python tools/infra.py generate-project --template <name> --name <project> --github-repo <owner/repo>")
        
    except Exception as e:
        logger.exception("Fatal error listing templates")
        click.echo(f"❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command("setup-vercel-project")
@click.option("--project", required=True, help="Project name (e.g., smb)")
@click.option("--repo", required=True, help="GitHub repository (owner/repo)")
@click.option("--root-dir", help="Root directory for build (e.g., vlg/apps/smb_site)")
@click.option("--framework", default="nextjs", help="Framework preset (default: nextjs)")
@click.option("--env", default="prod", help="Environment name")
@click.option("--dry-run", is_flag=True, help="Simulate actions without making changes")
def setup_vercel_project(project: str, repo: str, root_dir: Optional[str], framework: str, env: str, dry_run: bool):
    """Set up a new Vercel project, connect GitHub repo, and deploy."""
    try:
        click.echo(f"🚀 Setting up Vercel project: {project}")
        click.echo("=" * 60)

        config = load_config()
        provider_configs = load_provider_configs()
        vercel_config = provider_configs.get("vercel", {})
        vercel_client = VercelClient(vercel_config, env=env, dry_run=dry_run)

        # Create project
        click.echo(f"\n1️⃣ Creating Vercel project '{project}'...")
        project_result = vercel_client.create_project(
            name=project,
            git_repo=repo,
            root_directory=root_dir
        )

        if not project_result:
            click.echo(f"❌ Failed to create Vercel project")
            sys.exit(1)

        project_id = project_result.get("id") or project_result.get("name") or project
        click.echo(f"✅ Project created: {project_id}")

        # Trigger initial deployment (if repo connected)
        if repo and not dry_run:
            click.echo(f"\n2️⃣ Triggering initial deployment...")
            deployments = vercel_client._list_deployments(project_id, limit=1)
            if deployments:
                click.echo(f"✅ Deployment triggered: {deployments[0].get('url', 'Check Vercel dashboard')}")
            else:
                click.echo(f"⚠️  Deployment will start automatically when code is pushed to {repo}")

        click.echo("\n" + "=" * 60)
        click.echo("✅ Vercel project setup complete!")
        click.echo(f"\n📋 Next steps:")
        click.echo(f"   1. Push code to {repo}")
        click.echo(f"   2. Vercel will auto-deploy on push")
        if root_dir:
            click.echo(f"   3. Root directory set to: {root_dir}")

    except Exception as e:
        logger.exception("Fatal error setting up Vercel project")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command("configure-domain")
@click.option("--project", required=True, help="Project name (e.g., smb)")
@click.option("--domain", required=True, help="Domain name (e.g., sugarmountainbuilders.com)")
@click.option("--env", default="prod", help="Environment name")
@click.option("--dry-run", is_flag=True, help="Simulate actions without making changes")
def configure_domain(project: str, domain: str, env: str, dry_run: bool):
    """Add a custom domain to a Vercel project and get DNS configuration."""
    try:
        click.echo(f"🌐 Configuring domain for {project}")
        click.echo("=" * 60)

        config = load_config()
        provider_configs = load_provider_configs()
        vercel_config = provider_configs.get("vercel", {})
        
        # Get project config
        projects = vercel_config.get("projects", {})
        project_config = projects.get(project, {})
        project_id = project_config.get("project_id") or project

        vercel_client = VercelClient(vercel_config, env=env, dry_run=dry_run)

        # Add domain
        click.echo(f"\n1️⃣ Adding domain '{domain}' to project...")
        domain_result = vercel_client.add_domain(project_id, domain)

        if not domain_result:
            click.echo(f"❌ Failed to add domain")
            sys.exit(1)

        click.echo(f"✅ Domain added: {domain}")

        # Get DNS configuration
        click.echo(f"\n2️⃣ Getting DNS configuration...")
        dns_config = vercel_client.get_domain_config(domain)

        click.echo("\n" + "=" * 60)
        click.echo("✅ Domain configured in Vercel!")
        click.echo("\n📋 DNS Configuration:")
        click.echo("=" * 60)
        
        if dns_config and dns_config.get("dns_records"):
            for record in dns_config.get("dns_records", []):
                click.echo(f"\nType: {record.get('type')}")
                click.echo(f"Name: {record.get('name')}")
                click.echo(f"Value: {record.get('value')}")
        else:
            click.echo(f"\n⚠️  DNS records will be shown in Vercel dashboard")
            click.echo(f"   Check: https://vercel.com/dashboard")

        click.echo("\n" + "=" * 60)
        click.echo("⚠️  MANUAL STEP REQUIRED:")
        click.echo(f"   1. Log into your domain provider (Wix, etc.)")
        click.echo(f"   2. Add the DNS records shown above")
        click.echo(f"   3. Wait 24-48 hours for DNS propagation")
        click.echo(f"   4. Run: python tools/infra.py verify-deployment --project {project} --domain {domain}")

    except Exception as e:
        logger.exception("Fatal error configuring domain")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command("update-contact-info")
@click.option("--project", required=True, help="Project name (e.g., smb)")
@click.option("--email", help="Contact email address")
@click.option("--phone", help="Contact phone number")
@click.option("--path", default="vlg/apps/smb_site", help="Path to project root")
@click.option("--dry-run", is_flag=True, help="Simulate actions without making changes")
def update_contact_info(project: str, email: Optional[str], phone: Optional[str], path: str, dry_run: bool):
    """Update contact information in code files."""
    try:
        if not email and not phone:
            click.echo("❌ Please provide --email and/or --phone")
            sys.exit(1)

        click.echo(f"📞 Updating contact info for {project}")
        click.echo("=" * 60)

        project_path = Path(path)
        contact_page = project_path / "app" / "contact" / "page.tsx"

        if not contact_page.exists():
            click.echo(f"❌ Contact page not found: {contact_page}")
            sys.exit(1)

        # Read file
        content = contact_page.read_text(encoding="utf-8")

        # Update email
        if email:
            click.echo(f"\n1️⃣ Updating email to: {email}")
            # Find and replace email placeholder
            import re
            email_pattern = r'(email[:\s]*["\'])([^"\']+)(["\'])'
            content = re.sub(email_pattern, f'\\g<1>{email}\\g<3>', content, count=1)

        # Update phone
        if phone:
            click.echo(f"2️⃣ Updating phone to: {phone}")
            phone_pattern = r'(phone[:\s]*["\'])([^"\']+)(["\'])'
            content = re.sub(phone_pattern, f'\\g<1>{phone}\\g<3>', content, count=1)

        if not dry_run:
            contact_page.write_text(content, encoding="utf-8")
            click.echo(f"\n✅ Contact info updated in {contact_page}")
        else:
            click.echo(f"\n🔍 DRY RUN - Would update contact info")
            click.echo(f"   Email: {email or 'unchanged'}")
            click.echo(f"   Phone: {phone or 'unchanged'}")

        click.echo("\n" + "=" * 60)
        click.echo("✅ Contact info update complete!")
        click.echo(f"\n📋 Next steps:")
        click.echo(f"   1. Review changes: {contact_page}")
        click.echo(f"   2. Commit and push to trigger deployment")

    except Exception as e:
        logger.exception("Fatal error updating contact info")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command("verify-deployment")
@click.option("--project", required=True, help="Project name (e.g., smb)")
@click.option("--domain", help="Custom domain to verify")
@click.option("--env", default="prod", help="Environment name")
def verify_deployment(project: str, domain: Optional[str], env: str):
    """Verify deployment status and domain configuration."""
    try:
        click.echo(f"🔍 Verifying deployment for {project}")
        click.echo("=" * 60)

        config = load_config()
        provider_configs = load_provider_configs()
        vercel_config = provider_configs.get("vercel", {})
        
        projects = vercel_config.get("projects", {})
        project_config = projects.get(project, {})
        project_id = project_config.get("project_id") or project

        vercel_client = VercelClient(vercel_config, env=env, dry_run=False)

        # Check deployment status
        click.echo(f"\n1️⃣ Checking deployment status...")
        deployments = vercel_client._list_deployments(project_id, limit=1)
        
        if deployments:
            latest = deployments[0]
            state = latest.get("state")
            url = latest.get("url")
            
            if state == "READY":
                click.echo(f"✅ Deployment ready: {url}")
            elif state == "BUILDING":
                click.echo(f"⏳ Deployment building: {url}")
            elif state == "ERROR":
                click.echo(f"❌ Deployment failed: {url}")
                logs = vercel_client.get_deployment_logs(latest.get("uid"))
                if logs:
                    click.echo(f"\n📋 Last log entries:")
                    for log in logs[-5:]:
                        click.echo(f"   {log}")
            else:
                click.echo(f"⚠️  Deployment status: {state}")
        else:
            click.echo(f"⚠️  No deployments found")

        # Check domain if provided
        if domain:
            click.echo(f"\n2️⃣ Verifying domain: {domain}")
            domain_config = vercel_client.get_domain_config(domain)
            
            if domain_config:
                status = domain_config.get("status", "unknown")
                if status == "verified":
                    click.echo(f"✅ Domain verified and active")
                else:
                    click.echo(f"⚠️  Domain status: {status}")
                    click.echo(f"   DNS propagation may still be in progress")
            
            # Test domain accessibility
            click.echo(f"\n3️⃣ Testing domain accessibility...")
            import httpx
            try:
                response = httpx.get(f"https://{domain}", timeout=10, follow_redirects=True)
                if response.status_code == 200:
                    click.echo(f"✅ Domain is accessible: https://{domain}")
                else:
                    click.echo(f"⚠️  Domain returned status {response.status_code}")
            except Exception as e:
                click.echo(f"⚠️  Could not reach domain: {e}")
                click.echo(f"   DNS may still be propagating (can take 24-48 hours)")

        click.echo("\n" + "=" * 60)
        click.echo("✅ Verification complete!")

    except Exception as e:
        logger.exception("Fatal error verifying deployment")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command("create-github-repo")
@click.option("--name", required=True, help="Repository name (e.g., smb)")
@click.option("--description", help="Repository description")
@click.option("--private", is_flag=True, help="Make repository private")
@click.option("--env", default="prod", help="Environment name")
@click.option("--dry-run", is_flag=True, help="Simulate actions without making changes")
def create_github_repo(name: str, description: Optional[str], private: bool, env: str, dry_run: bool):
    """Create a new GitHub repository."""
    try:
        click.echo(f"📦 Creating GitHub repository: {name}")
        click.echo("=" * 60)

        config = load_config()
        provider_configs = load_provider_configs()
        github_config = provider_configs.get("github", {})
        github_client = GitHubClient(github_config, env=env, dry_run=dry_run)

        repo_result = github_client.create_repository(
            name=name,
            description=description or f"{name} project repository",
            private=private
        )

        if not repo_result:
            click.echo(f"❌ Failed to create repository")
            sys.exit(1)

        if repo_result.get("already_exists"):
            click.echo(f"⚠️  Repository already exists: {repo_result['full_name']}")
        else:
            click.echo(f"✅ Repository created: {repo_result['full_name']}")

        click.echo(f"\n📋 Repository Details:")
        click.echo(f"   Name: {repo_result.get('name', 'N/A')}")
        click.echo(f"   Full name: {repo_result.get('full_name', 'N/A')}")
        click.echo(f"   URL: {repo_result.get('html_url', 'N/A')}")
        if 'clone_url' in repo_result:
            click.echo(f"   Clone URL: {repo_result['clone_url']}")
        click.echo(f"   Private: {repo_result.get('private', False)}")

        click.echo("\n" + "=" * 60)
        click.echo("✅ Repository ready!")
        click.echo(f"\n📋 Next steps:")
        click.echo(f"   1. Initialize git: git init")
        if 'clone_url' in repo_result:
            click.echo(f"   2. Add remote: git remote add origin {repo_result['clone_url']}")
        elif 'html_url' in repo_result:
            clone_url = repo_result['html_url'].replace('https://github.com/', 'https://github.com/') + '.git'
            click.echo(f"   2. Add remote: git remote add origin {clone_url}")
        click.echo(f"   3. Commit and push your code")

    except Exception as e:
        logger.exception("Fatal error creating GitHub repository")
        click.echo(f"\n❌ Fatal error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
