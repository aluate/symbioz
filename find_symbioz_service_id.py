#!/usr/bin/env python3
"""
Find Symbioz Render service ID and update config
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import httpx
import yaml

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("RENDER_API_KEY")
if not api_key:
    print("❌ Error: RENDER_API_KEY not found in .env file")
    sys.exit(1)

print("🔍 Searching for Symbioz/Mellivox Render service...\n")

# Render API endpoint
url = "https://api.render.com/v1/services"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}

try:
    response = httpx.get(url, headers=headers, timeout=30.0)
    response.raise_for_status()
    
    services = response.json()
    
    if not services:
        print("❌ No services found.")
        sys.exit(1)
    
    # Look for Symbioz service
    symbioz_service = None
    for service in services:
        service_data = service.get("service", {})
        name = service_data.get("name", "").lower()
        repo = service_data.get("repo", "").lower()
        
        # Check if it's a Symbioz service
        if "symbioz" in name or "mellivox" in name or "symbioz" in repo or "mellivox" in repo:
            symbioz_service = service_data
            break
    
    if not symbioz_service:
        print("⚠️  No Symbioz service found. Available services:")
        print()
        for service in services:
            service_data = service.get("service", {})
            print(f"  - {service_data.get('name', 'N/A')} (ID: {service_data.get('id', 'N/A')})")
            print(f"    Repo: {service_data.get('repo', 'N/A')}")
        print()
        print("💡 If you haven't created the Render service yet, create it first via Render dashboard.")
        sys.exit(1)
    
    service_id = symbioz_service.get("id")
    service_name = symbioz_service.get("name")
    repo = symbioz_service.get("repo")
    
    print(f"✅ Found Symbioz service!")
    print(f"   Name: {service_name}")
    print(f"   ID: {service_id}")
    print(f"   Repo: {repo}")
    print()
    
    # Update render.yaml
    render_yaml_path = Path("infra/providers/render.yaml")
    if not render_yaml_path.exists():
        print(f"❌ Config file not found: {render_yaml_path}")
        sys.exit(1)
    
    with open(render_yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    
    services_config = config.get("services", {})
    if "symbioz-api" not in services_config:
        print("❌ symbioz-api not found in config")
        sys.exit(1)
    
    # Update the service ID
    old_id = services_config["symbioz-api"].get("render_service_id", "")
    services_config["symbioz-api"]["render_service_id"] = service_id
    
    # Write back
    with open(render_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"✅ Updated {render_yaml_path}")
    print(f"   Changed: {old_id} → {service_id}")
    print()
    print("🚀 Ready to deploy! Run: python deploy_symbioz.py")
    
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        print("❌ Error: Invalid API key. Check your RENDER_API_KEY in .env file.")
    elif e.response.status_code == 403:
        print("❌ Error: API key doesn't have permission to access services.")
    else:
        print(f"❌ Error: HTTP {e.response.status_code} - {e.response.text}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

