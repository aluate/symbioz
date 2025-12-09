#!/usr/bin/env python3
"""Check Vercel project settings including root directory."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_config, load_provider_configs
from dotenv import load_dotenv

load_dotenv()

project_name = "achillies"

config = load_config()
provider_configs = load_provider_configs()
vercel_config = provider_configs.get("vercel", {})
vercel_client = VercelClient(vercel_config, env="prod", dry_run=False)

# Get project settings
print(f"Checking Vercel project settings for: {project_name}")
print("=" * 60)

try:
    # Try to get project info via API
    import httpx
    token = vercel_config.get("api_token") or os.environ.get("VERCEL_API_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    
    url = f"https://api.vercel.com/v9/projects/{project_name}"
    with httpx.Client() as client:
        response = client.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            project = response.json()
            print(f"Project ID: {project.get('id')}")
            print(f"Name: {project.get('name')}")
            print(f"Root Directory: {project.get('rootDirectory', 'NOT SET (should be apps/corporate-crashout)')}")
            print(f"Framework: {project.get('framework')}")
            print(f"Build Command: {project.get('buildCommand', 'default')}")
            print(f"Output Directory: {project.get('outputDirectory', 'default')}")
        else:
            print(f"Could not fetch project settings (status: {response.status_code})")
            print("You may need to check the Vercel dashboard manually:")
            print(f"  https://vercel.com/dashboard")
            print(f"  → Project: {project_name}")
            print(f"  → Settings → General")
            print(f"  → Check 'Root Directory' is set to: apps/corporate-crashout")
except Exception as e:
    print(f"Error: {e}")
    print("\nManual check required:")
    print("1. Go to: https://vercel.com/dashboard")
    print(f"2. Click project: {project_name}")
    print("3. Go to: Settings → General")
    print("4. Check 'Root Directory' - should be: apps/corporate-crashout")

