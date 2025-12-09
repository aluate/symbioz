#!/usr/bin/env python3
"""
Check if live site matches codebase
"""

import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
workspace_root = Path(__file__).parent
env_path = workspace_root / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Add infra to path
sys.path.insert(0, str(workspace_root / "infra"))
sys.path.insert(0, str(workspace_root / "apps" / "otto"))

def get_latest_commit_hash(repo_path: Path) -> str:
    """Get latest commit hash from local repo"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Error getting local commit: {e}")
    return "unknown"

def get_remote_commit_hash(repo_path: Path) -> str:
    """Get latest commit hash from GitHub"""
    try:
        result = subprocess.run(
            ["git", "ls-remote", "origin", "main"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.split()[0] if result.stdout.strip() else "unknown"
    except Exception as e:
        print(f"Error getting remote commit: {e}")
    return "unknown"

def get_vercel_deployment_info():
    """Get latest Vercel deployment info"""
    try:
        from infra.providers.vercel_client import VercelClient
        from infra.utils.yaml_loader import load_provider_configs
        
        configs = load_provider_configs()
        client = VercelClient(configs.get("vercel", {}), env="prod", dry_run=False)
        
        # Get project config
        projects = configs.get("vercel", {}).get("projects", {})
        project_config = projects.get("catered-by-me")
        if not project_config:
            return None
        
        project_id = project_config.get("project_id") or "catered-by-me"
        
        # Get latest deployment
        deployments = client._list_deployments(project_id, limit=1)
        if deployments:
            return deployments[0]
    except Exception as e:
        print(f"Error getting Vercel deployment: {e}")
    return None

def get_render_deployment_info():
    """Get latest Render deployment info"""
    try:
        from infra.providers.render_client import RenderClient
        from infra.utils.yaml_loader import load_provider_configs
        
        configs = load_provider_configs()
        client = RenderClient(configs.get("render", {}), env="prod", dry_run=False)
        
        # Get service config
        services = configs.get("render", {}).get("services", {})
        service_config = services.get("catered-by-me-api")
        if not service_config:
            return None
        
        service_id = service_config.get("render_service_id")
        if not service_id:
            return None
        
        # Get latest deployment
        deployments = client._get_deployments(service_id, limit=1)
        if deployments and isinstance(deployments, list) and len(deployments) > 0:
            deploy = deployments[0]
            if isinstance(deploy, dict):
                if "deploy" in deploy and isinstance(deploy["deploy"], dict):
                    return deploy["deploy"]
                return deploy
    except Exception as e:
        print(f"Error getting Render deployment: {e}")
    return None

def main():
    print("🔍 Checking if live site matches codebase...")
    print()
    
    repo_path = workspace_root / "catered_by_me"
    
    # Get commit hashes
    local_commit = get_latest_commit_hash(repo_path)
    remote_commit = get_remote_commit_hash(repo_path)
    
    print("📦 Code Status:")
    print(f"   Local commit:  {local_commit[:8]}")
    print(f"   GitHub commit: {remote_commit[:8]}")
    
    if local_commit == remote_commit:
        print("   ✅ Local and GitHub are in sync")
    else:
        print("   ⚠️  Local and GitHub are out of sync")
    
    print()
    
    # Get Vercel deployment
    print("🌐 Vercel Deployment:")
    vercel_deploy = get_vercel_deployment_info()
    if vercel_deploy:
        vercel_commit = vercel_deploy.get("meta", {}).get("githubCommitSha") or vercel_deploy.get("meta", {}).get("gitSource", {}).get("sha") or "unknown"
        vercel_state = vercel_deploy.get("state", "unknown")
        vercel_url = vercel_deploy.get("url", "unknown")
        
        print(f"   State: {vercel_state}")
        print(f"   Commit: {vercel_commit[:8] if vercel_commit != 'unknown' else 'unknown'}")
        print(f"   URL: {vercel_url}")
        
        if vercel_state == "READY":
            if vercel_commit != "unknown" and vercel_commit == remote_commit:
                print("   ✅ Vercel matches GitHub code")
            elif vercel_commit != "unknown":
                print(f"   ⚠️  Vercel commit ({vercel_commit[:8]}) differs from GitHub ({remote_commit[:8]})")
            else:
                print("   ⚠️  Could not determine Vercel commit hash")
        else:
            print(f"   ⚠️  Vercel deployment is not ready (state: {vercel_state})")
    else:
        print("   ❌ Could not get Vercel deployment info")
    
    print()
    
    # Get Render deployment
    print("🔧 Render Deployment:")
    render_deploy = get_render_deployment_info()
    if render_deploy:
        render_status = render_deploy.get("status", "unknown")
        render_commit = render_deploy.get("commit", {}).get("id") if isinstance(render_deploy.get("commit"), dict) else render_deploy.get("commitId") or "unknown"
        
        print(f"   Status: {render_status}")
        print(f"   Commit: {render_commit[:8] if render_commit != 'unknown' else 'unknown'}")
        
        if render_status == "live":
            if render_commit != "unknown" and render_commit == remote_commit:
                print("   ✅ Render matches GitHub code")
            elif render_commit != "unknown":
                print(f"   ⚠️  Render commit ({render_commit[:8]}) differs from GitHub ({remote_commit[:8]})")
            else:
                print("   ⚠️  Could not determine Render commit hash")
        else:
            print(f"   ⚠️  Render deployment is not live (status: {render_status})")
    else:
        print("   ❌ Could not get Render deployment info")
    
    print()
    print("=" * 60)
    
    # Summary
    all_synced = True
    if local_commit != remote_commit:
        all_synced = False
    if vercel_deploy and vercel_deploy.get("state") != "READY":
        all_synced = False
    if render_deploy and render_deploy.get("status") != "live":
        all_synced = False
    
    if all_synced:
        print("✅ Summary: Live site appears to match codebase!")
    else:
        print("⚠️  Summary: Some deployments may be out of sync")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

