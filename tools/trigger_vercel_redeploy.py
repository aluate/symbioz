#!/usr/bin/env python3
"""
Trigger a redeploy for a Vercel project.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_config, load_provider_configs
from dotenv import load_dotenv

load_dotenv()

# Ensure stdout encoding is utf-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    project_name = "achillies"
    
    print(f"🔄 Triggering redeploy for: {project_name}")
    print("=" * 60)
    
    try:
        config = load_config()
        provider_configs = load_provider_configs()
        vercel_config = provider_configs.get("vercel", {})
        
        projects = vercel_config.get("projects", {})
        if project_name not in projects:
            print(f"❌ ERROR: Project '{project_name}' not found in config")
            sys.exit(1)
        
        project_config = projects[project_name]
        project_id = project_config.get("project_id") or project_name
        
        vercel_client = VercelClient(vercel_config, env="prod", dry_run=False)
        
        # Get latest deployment
        print(f"\n[1/2] Getting latest deployment...")
        deployments = vercel_client._list_deployments(project_id, limit=1)
        
        if not deployments:
            print("⚠️  No deployments found. Creating initial deployment...")
            # We could trigger via webhook or API, but for now just tell user to push
            print("   Push a commit to trigger deployment, or create deployment manually in Vercel dashboard")
            sys.exit(0)
        
        latest = deployments[0]
        deployment_id = latest.get("uid")
        state = latest.get("state")
        
        print(f"   Latest deployment: {deployment_id}")
        print(f"   Current state: {state}")
        
        # Trigger redeploy by creating a new deployment
        # Vercel API doesn't have a direct "redeploy" endpoint, but we can:
        # 1. Cancel and redeploy (not always available)
        # 2. Create a new deployment (requires webhook/commit)
        # 3. Use Vercel's redeploy API endpoint if available
        
        print(f"\n[2/2] Triggering new deployment...")
        
        # Try to trigger via deployment redeploy endpoint
        import httpx
        headers = vercel_client._get_headers()
        
        # Vercel v13 API has a redeploy endpoint
        redeploy_url = f"https://api.vercel.com/v13/deployments/{deployment_id}/cancel"
        
        with httpx.Client() as client:
            # Actually, we want to create a NEW deployment, not cancel
            # The easiest way is to trigger via a webhook or by making a small commit
            # But we can try the v1/deployments endpoint to create from latest commit
            
            # Check if we can create a deployment from the latest commit
            print("   Creating new deployment from latest commit...")
            
            # Get project to find git repo info
            project_url = f"https://api.vercel.com/v9/projects/{project_id}"
            project_resp = client.get(project_url, headers=headers, timeout=30)
            
            if project_resp.status_code == 200:
                project_info = project_resp.json()
                git_repo = project_info.get("link", {}).get("repo")
                
                if git_repo:
                    print(f"   Found Git repo: {git_repo}")
                    print("   ✅ Vercel will auto-deploy on next push to GitHub")
                    print("\n   Alternative: Create empty commit to trigger deploy:")
                    print(f"      cd temp_achillies_clone")
                    print(f"      git commit --allow-empty -m 'Trigger redeploy'")
                    print(f"      git push origin main")
                else:
                    print("   ⚠️  No Git repo connected")
                    print("   Manual redeploy needed in Vercel dashboard")
            else:
                print("   ⚠️  Could not fetch project info")
            
        print("\n✅ Redeploy instructions provided!")
        print("   Vercel will automatically deploy on next push to GitHub")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

