#!/usr/bin/env python3
"""Check Vercel deployment status after migration"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import time

# Load environment variables
workspace_root = Path(__file__).parent
env_path = workspace_root / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Add infra to path
sys.path.insert(0, str(workspace_root / "infra"))
sys.path.insert(0, str(workspace_root / "apps" / "otto"))

def check_vercel_deployment():
    """Check latest Vercel deployment status"""
    try:
        from infra.providers.vercel_client import VercelClient
        from infra.utils.yaml_loader import load_provider_configs
        
        configs = load_provider_configs()
        client = VercelClient(configs.get("vercel", {}), env="prod", dry_run=False)
        
        # Get project config
        projects = configs.get("vercel", {}).get("projects", {})
        project_config = projects.get("catered-by-me")
        if not project_config:
            print("❌ Project config not found")
            return False
        
        project_id = project_config.get("project_id") or "catered-by-me"
        
        # Get latest deployment
        deployments = client._list_deployments(project_id, limit=3)
        if not deployments:
            print("❌ No deployments found")
            return False
        
        print("🔍 Checking latest Vercel deployments...")
        print()
        
        for i, dep in enumerate(deployments, 1):
            uid = dep.get('uid', 'N/A')
            state = dep.get('state', 'UNKNOWN')
            ready_state = dep.get('readyState', 'UNKNOWN')
            url = dep.get('url', 'N/A')
            
            # Get commit info
            meta = dep.get('meta', {})
            commit_sha = meta.get('githubCommitSha') or meta.get('gitSource', {}).get('sha') or 'N/A'
            commit_msg = meta.get('githubCommitMessage', 'N/A')[:60]
            
            # Status emoji
            if state == 'READY' or ready_state == 'READY':
                status = "✅ READY"
            elif state == 'BUILDING' or ready_state == 'BUILDING':
                status = "🔨 BUILDING"
            elif state == 'ERROR' or ready_state == 'ERROR':
                status = "❌ ERROR"
            elif state == 'QUEUED':
                status = "⏳ QUEUED"
            else:
                status = f"⚠️ {state}"
            
            print(f"{i}. {status}")
            print(f"   ID: {uid}")
            print(f"   URL: {url}")
            print(f"   Commit: {commit_sha[:8] if commit_sha != 'N/A' else 'N/A'}")
            print(f"   Message: {commit_msg}")
            print()
            
            # Check if this is our latest commit
            if i == 1:
                if state == 'READY' or ready_state == 'READY':
                    print("=" * 60)
                    print("✅ SUCCESS: Latest deployment is READY!")
                    print(f"   URL: {url}")
                    print("=" * 60)
                    return True
                elif state == 'BUILDING' or ready_state == 'BUILDING':
                    print("⏳ Deployment is still building...")
                    print("   This may take a few minutes.")
                    return False
                elif state == 'ERROR' or ready_state == 'ERROR':
                    print("❌ Deployment failed!")
                    print("   Check Vercel dashboard for error details.")
                    return False
        
        return False
        
    except Exception as e:
        print(f"❌ Error checking Vercel: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Checking Vercel deployment status...")
    print()
    
    # Wait a bit for Vercel to start building
    print("⏳ Waiting 10 seconds for Vercel to detect the push...")
    time.sleep(10)
    
    success = check_vercel_deployment()
    
    if not success:
        print()
        print("💡 Tip: If deployment is still building, wait a few minutes and check again.")
        print("   Or check the Vercel dashboard: https://vercel.com/aluates-projects/catered-by-me")

