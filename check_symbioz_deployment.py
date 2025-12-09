#!/usr/bin/env python3
"""
Check Symbioz/Mellivox deployment status
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import httpx
import yaml
from datetime import datetime

load_dotenv()

print("🔍 Checking Symbioz/Mellivox Deployment Status...")
print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)
print()

api_key = os.getenv("RENDER_API_KEY")
vercel_token = os.getenv("VERCEL_TOKEN")

# Check Render Service
print("📦 Render Backend (API):")
print("-" * 60)

try:
    # Load config to get service ID
    render_yaml_path = Path("infra/providers/render.yaml")
    with open(render_yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    
    services = config.get("services", {})
    symbioz_config = services.get("symbioz-api", {})
    service_id = symbioz_config.get("render_service_id", "")
    
    if not service_id or service_id.startswith("srv-REPLACE") or "TODO" in service_id.upper():
        print("   ⚠️  Service ID not configured")
        print("   💡 Run: python find_symbioz_service_id.py")
    else:
        if api_key:
            url = f"https://api.render.com/v1/services/{service_id}"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            }
            
            try:
                response = httpx.get(url, headers=headers, timeout=30.0)
                if response.status_code == 200:
                    service_data = response.json().get("service", response.json())
                    name = service_data.get("name", "N/A")
                    service_url = service_data.get("serviceDetails", {}).get("url", service_data.get("url", ""))
                    status = service_data.get("serviceDetails", {}).get("deployStatus", "unknown")
                    
                    print(f"   ✅ Service: {name}")
                    print(f"   📍 ID: {service_id}")
                    if service_url:
                        print(f"   🌐 URL: {service_url}")
                    print(f"   📊 Status: {status}")
                    
                    # Check latest deployment
                    deploy_url = f"https://api.render.com/v1/services/{service_id}/deploys"
                    deploy_response = httpx.get(deploy_url, headers=headers, timeout=30.0)
                    if deploy_response.status_code == 200:
                        deploys = deploy_response.json()
                        if deploys and len(deploys) > 0:
                            latest = deploys[0].get("deploy", deploys[0])
                            deploy_status = latest.get("status", "unknown")
                            created_at = latest.get("createdAt", "")
                            print(f"   🚀 Latest Deploy: {deploy_status}")
                            if created_at:
                                print(f"   ⏰ Created: {created_at}")
                else:
                    print(f"   ❌ Service not found (HTTP {response.status_code})")
            except Exception as e:
                print(f"   ⚠️  Error checking service: {e}")
        else:
            print("   ⚠️  RENDER_API_KEY not set")
            print(f"   📝 Service ID: {service_id}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Check Vercel Frontend
print("🌐 Vercel Frontend:")
print("-" * 60)

try:
    vercel_yaml_path = Path("infra/providers/vercel.yaml")
    with open(vercel_yaml_path, 'r', encoding='utf-8') as f:
        vercel_config = yaml.safe_load(f) or {}
    
    projects = vercel_config.get("projects", {})
    symbioz_project = projects.get("symbioz", {})
    project_id = symbioz_project.get("project_id", "symbioz")
    
    if vercel_token:
        url = f"https://api.vercel.com/v13/deployments"
        headers = {
            "Authorization": f"Bearer {vercel_token}",
            "Accept": "application/json",
        }
        
        try:
            # Get project first
            project_url = f"https://api.vercel.com/v9/projects/{project_id}"
            project_response = httpx.get(project_url, headers=headers, timeout=30.0)
            
            if project_response.status_code == 200:
                project_data = project_response.json()
                print(f"   ✅ Project: {project_data.get('name', project_id)}")
                
                # Get latest deployment
                params = {"projectId": project_id, "limit": 1}
                response = httpx.get(url, headers=headers, params=params, timeout=30.0)
                if response.status_code == 200:
                    deployments = response.json().get("deployments", [])
                    if deployments:
                        latest = deployments[0]
                        state = latest.get("state", "unknown")
                        url_deploy = latest.get("url", "")
                        created = latest.get("createdAt", 0)
                        
                        print(f"   📊 Status: {state}")
                        if url_deploy:
                            print(f"   🌐 URL: https://{url_deploy}")
                        if created:
                            from datetime import datetime
                            created_dt = datetime.fromtimestamp(created / 1000)
                            print(f"   ⏰ Created: {created_dt.strftime('%Y-%m-%d %H:%M:%S')}")
                    else:
                        print("   ⚠️  No deployments found")
                else:
                    print(f"   ⚠️  Could not get deployments (HTTP {response.status_code})")
            elif project_response.status_code == 404:
                print(f"   ⚠️  Project '{project_id}' not found in Vercel")
                print("   💡 Project may need to be created")
            else:
                print(f"   ⚠️  Error checking project (HTTP {project_response.status_code})")
        except Exception as e:
            print(f"   ⚠️  Error checking Vercel: {e}")
    else:
        print("   ⚠️  VERCEL_TOKEN not set")
        print(f"   📝 Project ID: {project_id}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()
print("=" * 60)
print()
print("💡 To check again, run: python check_symbioz_deployment.py")
print("💡 To view full deployment logs, run: python deploy_symbioz.py")

