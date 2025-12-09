#!/usr/bin/env python3
"""Quick test of deployment capabilities"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("="*60)
print("Testing Corporate Crashout Deployment")
print("="*60)

try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    print("\n[1] Checking environment variables...")
    vercel_token = os.getenv("VERCEL_TOKEN")
    if vercel_token:
        print(f"✅ VERCEL_TOKEN: SET (length: {len(vercel_token)})")
    else:
        print("❌ VERCEL_TOKEN: NOT SET")
        print("   Please add VERCEL_TOKEN to your .env file")
        sys.exit(1)
    
    print("\n[2] Loading configuration...")
    from infra.utils.yaml_loader import load_provider_configs
    configs = load_provider_configs()
    vercel_config = configs.get("vercel", {})
    projects = vercel_config.get("projects", {})
    
    if "achillies" in projects:
        print("✅ achillies project found in config")
        project_config = projects["achillies"]
        print(f"   Root directory: {project_config.get('root_directory', 'not set')}")
    else:
        print("❌ achillies project NOT found in config")
        sys.exit(1)
    
    print("\n[3] Connecting to Vercel API...")
    from infra.providers.vercel_client import VercelClient
    client = VercelClient(vercel_config, env="prod", dry_run=False)
    
    print("\n[4] Checking project status...")
    project = client._get_project("achillies")
    
    if project:
        print("✅ Project found in Vercel!")
        current_root = project.get("rootDirectory")
        expected_root = project_config.get("root_directory", "apps/corporate-crashout")
        
        print(f"   Current root directory: {current_root or '(not set)'}")
        print(f"   Expected root directory: {expected_root}")
        
        if current_root != expected_root:
            print(f"\n⚠️  Root directory mismatch! Fixing now...")
            success = client.update_project_settings("achillies", root_directory=expected_root)
            if success:
                print(f"✅ Root directory updated to: {expected_root}")
            else:
                print("❌ Failed to update root directory")
        else:
            print("✅ Root directory is correct!")
        
        # Check latest deployment
        print("\n[5] Checking latest deployment...")
        deployments = client._list_deployments("achillies", limit=1)
        if deployments:
            latest = deployments[0]
            state = latest.get("state")
            url = latest.get("url")
            print(f"   Status: {state}")
            print(f"   URL: {url}")
            
            if state == "READY":
                print("✅ Deployment is ready!")
            elif state in ["BUILDING", "QUEUED"]:
                print("⏳ Deployment in progress...")
            else:
                print(f"⚠️  Deployment state: {state}")
        else:
            print("⚠️  No deployments found")
        
        print("\n" + "="*60)
        print("✅ All checks complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Check https://achillies.vercel.app")
        print("2. If 404, wait 5-10 minutes for changes to propagate")
        print("3. Or trigger a new deployment in Vercel dashboard")
        
    else:
        print("❌ Project 'achillies' not found in Vercel")
        print("   Please create it in Vercel dashboard first")
        sys.exit(1)
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
