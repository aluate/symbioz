#!/usr/bin/env python3
"""Simple deployment script with guaranteed output"""

import sys
import os
from pathlib import Path

# Force UTF-8 output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("Corporate Crashout Deployment")
print("=" * 60)
print()

# Check VERCEL_TOKEN
from dotenv import load_dotenv
load_dotenv()

vercel_token = os.getenv("VERCEL_TOKEN")
if not vercel_token:
    print("ERROR: VERCEL_TOKEN not set!")
    print()
    print("Please add VERCEL_TOKEN to your .env file")
    print("Get it from: https://vercel.com/account/tokens")
    sys.exit(1)

print(f"VERCEL_TOKEN: Found (length: {len(vercel_token)})")
print()

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    print("Loading configuration...")
    from infra.utils.yaml_loader import load_provider_configs
    configs = load_provider_configs()
    vercel_config = configs.get("vercel", {})
    projects = vercel_config.get("projects", {})
    
    if "achillies" not in projects:
        print("ERROR: achillies project not found in vercel.yaml")
        sys.exit(1)
    
    project_config = projects["achillies"]
    expected_root = project_config.get("root_directory", "apps/corporate-crashout")
    print(f"Expected root directory: {expected_root}")
    print()
    
    print("Connecting to Vercel API...")
    from infra.providers.vercel_client import VercelClient
    client = VercelClient(vercel_config, env="prod", dry_run=False)
    
    print("Checking project...")
    project = client._get_project("achillies")
    
    if not project:
        print("ERROR: Project 'achillies' not found in Vercel")
        print("Please create it in Vercel dashboard first")
        sys.exit(1)
    
    print("Project found!")
    current_root = project.get("rootDirectory")
    print(f"Current root directory: {current_root or '(not set)'}")
    print(f"Expected root directory: {expected_root}")
    print()
    
    if current_root != expected_root:
        print(f"Fixing root directory...")
        success = client.update_project_settings("achillies", root_directory=expected_root)
        if success:
            print(f"SUCCESS: Root directory updated to: {expected_root}")
        else:
            print("ERROR: Failed to update root directory")
            sys.exit(1)
    else:
        print("Root directory is already correct!")
    
    print()
    print("Checking latest deployment...")
    deployments = client._list_deployments("achillies", limit=1)
    if deployments:
        latest = deployments[0]
        state = latest.get("state")
        url = latest.get("url")
        print(f"Status: {state}")
        print(f"URL: {url}")
        
        if state == "READY":
            print()
            print("=" * 60)
            print("SUCCESS: Deployment is ready!")
            print("=" * 60)
            print(f"Check your site at: https://achillies.vercel.app")
        else:
            print(f"Deployment state: {state}")
    else:
        print("No deployments found")
    
    print()
    print("=" * 60)
    print("Deployment check complete!")
    print("=" * 60)
    
except Exception as e:
    print()
    print("=" * 60)
    print(f"ERROR: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
