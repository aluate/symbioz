#!/usr/bin/env python3
"""
Test and fix Otto's Render service creation skill
Loops until it successfully creates the service
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
import httpx
import yaml

load_dotenv()

print("🔧 Testing Render Service Creation Skill\n")
print("=" * 60)

api_key = os.getenv("RENDER_API_KEY")
if not api_key:
    print("❌ RENDER_API_KEY not found")
    sys.exit(1)

# Load config
render_yaml_path = Path("infra/providers/render.yaml")
with open(render_yaml_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f) or {}

services = config.get("services", {})
symbioz_config = services.get("symbioz-api", {})
service_name = "symbioz-api"
repo = symbioz_config.get("repo", "aluate/symbioz")

print(f"📋 Service: {service_name}")
print(f"📦 Repo: {repo}")
print()

# Step 1: Get owner ID
print("Step 1: Getting owner ID...")
owner_id = None

# Method 1: From existing service
try:
    existing_id = services.get("catered-by-me-api", {}).get("render_service_id")
    if existing_id:
        print(f"   Trying existing service: {existing_id}")
        url = f"https://api.render.com/v1/services/{existing_id}"
        headers = {"Authorization": f"Bearer {api_key}"}
        r = httpx.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json()
            service_data = data.get("service", data)
            owner_id = service_data.get("ownerId")
            if owner_id:
                print(f"   ✅ Got owner ID from existing service: {owner_id}")
except Exception as e:
    print(f"   ⚠️  Method 1 failed: {e}")

# Method 2: From owners endpoint
if not owner_id:
    try:
        print("   Trying owners endpoint...")
        url = "https://api.render.com/v1/owners"
        headers = {"Authorization": f"Bearer {api_key}"}
        r = httpx.get(url, headers=headers, timeout=30)
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            owners = r.json()
            print(f"   Response type: {type(owners)}")
            print(f"   Response: {str(owners)[:200]}")
            
            # Try different response formats
            if isinstance(owners, list) and len(owners) > 0:
                owner_id = owners[0].get("owner", {}).get("id") or owners[0].get("id")
            elif isinstance(owners, dict):
                owner_id = owners.get("owner", {}).get("id") or owners.get("id")
            
            if owner_id:
                print(f"   ✅ Got owner ID from owners endpoint: {owner_id}")
            else:
                print(f"   ⚠️  Could not extract owner ID from response")
        else:
            print(f"   ❌ Owners endpoint returned: {r.status_code}")
            print(f"   Response: {r.text[:500]}")
    except Exception as e:
        print(f"   ⚠️  Method 2 failed: {e}")
        import traceback
        traceback.print_exc()

if not owner_id:
    print("\n❌ Could not get owner ID - cannot create service")
    print("\n💡 Possible fixes:")
    print("   1. Check RENDER_API_KEY is valid")
    print("   2. Check API permissions")
    print("   3. Try getting owner ID from Render dashboard")
    sys.exit(1)

print()

# Step 2: Check if service already exists
print("Step 2: Checking if service exists...")
try:
    url = "https://api.render.com/v1/services"
    headers = {"Authorization": f"Bearer {api_key}"}
    r = httpx.get(url, headers=headers, timeout=30)
    if r.status_code == 200:
        all_services = r.json()
        repo_normalized = repo.lower().replace("https://github.com/", "").replace(".git", "")
        
        existing = None
        for svc_item in all_services:
            svc_data = svc_item.get("service", svc_item)
            svc_repo = str(svc_data.get("repo", "")).lower().replace("https://github.com/", "").replace(".git", "")
            svc_name = svc_data.get("name", "").lower()
            
            if repo_normalized in svc_repo or "symbioz" in svc_name or "mellivox" in svc_name:
                existing = svc_data
                break
        
        if existing:
            service_id = existing.get("id")
            print(f"   ✅ Found existing service: {existing.get('name')} (ID: {service_id})")
            print(f"   📝 Updating config...")
            
            symbioz_config["render_service_id"] = service_id
            config["services"]["symbioz-api"] = symbioz_config
            
            with open(render_yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
            print(f"   ✅ Config updated!")
            print(f"\n🎉 Service already exists! ID: {service_id}")
            sys.exit(0)
        else:
            print("   ℹ️  No existing service found - will create new one")
except Exception as e:
    print(f"   ⚠️  Error checking: {e}")

print()

# Step 3: Create service
print("Step 3: Creating Render service...")
max_attempts = 3
for attempt in range(1, max_attempts + 1):
    print(f"\n   Attempt {attempt}/{max_attempts}...")
    
    try:
        # Build repo URL
        repo_url = repo
        if not repo_url.startswith("http"):
            repo_url = f"https://github.com/{repo_url}"
        
        # Render API requires serviceDetails for web services
        # Determine runtime from build command (python for this service)
        runtime = "python"
        if "npm" in symbioz_config.get("build_command", "").lower():
            runtime = "node"
        
        # Build envSpecificDetails for Python
        # buildCommand and startCommand go INSIDE envSpecificDetails!
        env_specific = {}
        if runtime == "python":
            python_version = symbioz_config.get("python_version", "3.11.11")
            env_specific = {
                "pythonVersion": python_version
            }
            # Add build/start commands to envSpecificDetails
            if symbioz_config.get("build_command"):
                env_specific["buildCommand"] = symbioz_config["build_command"]
            if symbioz_config.get("start_command"):
                env_specific["startCommand"] = symbioz_config["start_command"]
        
        service_details = {
            "plan": "starter",  # Free tier
            "region": symbioz_config.get("region", "oregon"),
            "runtime": runtime,
            "envSpecificDetails": env_specific,
        }
        
        payload = {
            "type": "web_service",
            "name": service_name,
            "ownerId": owner_id,
            "repo": repo_url,
            "branch": symbioz_config.get("branch", "main"),
            "serviceDetails": service_details,
        }
        
        # rootDir goes at root level if specified
        if symbioz_config.get("root_dir"):
            payload["rootDir"] = symbioz_config["root_dir"]
        
        print(f"   Payload: {payload}")
        
        url = "https://api.render.com/v1/services"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        r = httpx.post(url, headers=headers, json=payload, timeout=60)
        
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 201:
            result = r.json()
            service_data = result.get("service", result)
            service_id = service_data.get("id")
            
            print(f"   ✅ Service created! ID: {service_id}")
            
            # Update config
            print(f"   📝 Updating config...")
            symbioz_config["render_service_id"] = service_id
            config["services"]["symbioz-api"] = symbioz_config
            
            with open(render_yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
            print(f"   ✅ Config updated!")
            print(f"\n🎉 SUCCESS! Service created: {service_id}")
            print(f"   Name: {service_data.get('name')}")
            print(f"   URL: {service_data.get('serviceDetails', {}).get('url', 'N/A')}")
            sys.exit(0)
        else:
            error_text = r.text
            print(f"   ❌ Failed: HTTP {r.status_code}")
            print(f"   Error: {error_text[:500]}")
            
            # Try to parse error
            try:
                error_json = r.json()
                if "message" in error_json:
                    print(f"   Message: {error_json['message']}")
            except:
                pass
            
            if attempt < max_attempts:
                print(f"   ⏳ Waiting 5 seconds before retry...")
                time.sleep(5)
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        if attempt < max_attempts:
            print(f"   ⏳ Waiting 5 seconds before retry...")
            time.sleep(5)

print(f"\n❌ Failed to create service after {max_attempts} attempts")
sys.exit(1)

