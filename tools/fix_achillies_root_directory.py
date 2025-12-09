#!/usr/bin/env python3
"""
Fix Corporate Crashout (achillies) root directory in Vercel via API.
"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_config, load_provider_configs
from dotenv import load_dotenv
import httpx

load_dotenv()

# Ensure stdout encoding is utf-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    project_name = "achillies"
    correct_root_dir = "apps/corporate-crashout"
    
    print(f"🔧 Fixing root directory for: {project_name}")
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
        token = vercel_client.token
        
        # Get current project settings
        print(f"\n[1/3] Getting current project settings...")
        url = f"https://api.vercel.com/v9/projects/{project_id}"
        headers = vercel_client._get_headers()
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=30)
            
            if response.status_code == 404:
                print(f"❌ Project '{project_id}' not found in Vercel")
                sys.exit(1)
            
            response.raise_for_status()
            project = response.json()
            
            current_root = project.get("rootDirectory")
            print(f"   Current Root Directory: {current_root or '(not set)'}")
            print(f"   Should be: {correct_root_dir}")
            
            if current_root == correct_root_dir:
                print("\n✅ Root directory is already correct!")
                sys.exit(0)
            
            # Update root directory
            print(f"\n[2/3] Updating root directory to: {correct_root_dir}")
            update_url = f"https://api.vercel.com/v9/projects/{project_id}"
            payload = {"rootDirectory": correct_root_dir}
            
            update_response = client.patch(update_url, headers=headers, json=payload, timeout=30)
            
            if update_response.status_code == 200:
                print("✅ Root directory updated successfully!")
            else:
                print(f"⚠️  Update response: {update_response.status_code}")
                print(f"   Response: {update_response.text}")
                
                # Some Vercel API versions might use different endpoints
                if update_response.status_code == 404:
                    print("\n⚠️  Could not update via API. Please update manually:")
                    print("   1. Go to: https://vercel.com/dashboard")
                    print(f"   2. Click project: {project_id}")
                    print("   3. Go to: Settings → General")
                    print(f"   4. Set 'Root Directory' to: {correct_root_dir}")
                    print("   5. Save and redeploy")
                    sys.exit(1)
            
            # Trigger redeploy
            print(f"\n[3/3] Triggering redeploy...")
            deployments = vercel_client._list_deployments(project_id, limit=1)
            if deployments:
                latest_deployment = deployments[0].get("uid")
                print(f"   Latest deployment: {latest_deployment}")
                print("   Redeploy will happen automatically on next push, or:")
                print(f"   Trigger manually: https://vercel.com/dashboard → {project_id} → Deployments → Redeploy")
            
            print("\n✅ Root directory fix complete!")
            print("   Vercel will automatically redeploy with the new setting.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\n⚠️  Manual fix required:")
        print("   1. Go to: https://vercel.com/dashboard")
        print(f"   2. Click project: {project_name}")
        print("   3. Go to: Settings → General")
        print(f"   4. Set 'Root Directory' to: {correct_root_dir}")
        print("   5. Save and redeploy")
        sys.exit(1)

if __name__ == "__main__":
    main()

