#!/usr/bin/env python3
import os, sys, httpx, yaml, json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("SYMBIOZ/MELLIVOX DEPLOYMENT STATUS")
print("=" * 60)
print()

api_key = os.getenv("RENDER_API_KEY")
vercel_token = os.getenv("VERCEL_TOKEN")

# Check Render
print("📦 RENDER BACKEND:")
print("-" * 60)
try:
    config = yaml.safe_load(open("infra/providers/render.yaml"))
    service_id = config["services"]["symbioz-api"]["render_service_id"]
    print(f"Service ID: {service_id}")
    
    if api_key:
        url = f"https://api.render.com/v1/services/{service_id}"
        r = httpx.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=15)
        if r.status_code == 200:
            svc = r.json().get("service", r.json())
            details = svc.get("serviceDetails", {})
            status = details.get("deployStatus", "unknown")
            url_svc = details.get("url", "")
            print(f"Status: {status}")
            print(f"URL: {url_svc if url_svc else 'N/A'}")
            
            # Check health
            if url_svc:
                try:
                    health = httpx.get(f"{url_svc}/api/health", timeout=5)
                    if health.status_code == 200:
                        print("✅ Health check: OK")
                    else:
                        print(f"⚠️  Health check: HTTP {health.status_code}")
                except:
                    print("⚠️  Health check: Could not connect")
        else:
            print(f"❌ Error: HTTP {r.status_code}")
    else:
        print("⚠️  No API key")
except Exception as e:
    print(f"❌ Error: {e}")

print()
print("🌐 VERCEL FRONTEND:")
print("-" * 60)
try:
    if vercel_token:
        # Get project
        url = "https://api.vercel.com/v9/projects/symbioz"
        r = httpx.get(url, headers={"Authorization": f"Bearer {vercel_token}"}, timeout=15)
        if r.status_code == 200:
            proj = r.json()
            print(f"Project: {proj.get('name', 'symbioz')}")
            
            # Get latest deployment
            deps_url = "https://api.vercel.com/v13/deployments"
            deps = httpx.get(deps_url, headers={"Authorization": f"Bearer {vercel_token}"}, 
                           params={"projectId": "symbioz", "limit": 1}, timeout=15)
            if deps.status_code == 200:
                dep_list = deps.json().get("deployments", [])
                if dep_list:
                    dep = dep_list[0]
                    state = dep.get("state", "unknown")
                    url_dep = dep.get("url", "")
                    print(f"Status: {state}")
                    print(f"URL: https://{url_dep if url_dep else 'N/A'}")
                    
                    if state == "READY":
                        print("✅ Deployment: READY")
                    elif state == "ERROR":
                        print("❌ Deployment: ERROR")
                    else:
                        print(f"⏳ Deployment: {state}")
                else:
                    print("⚠️  No deployments found")
            else:
                print(f"⚠️  Could not get deployments: HTTP {deps.status_code}")
        elif r.status_code == 404:
            print("⚠️  Project not found - may need to be created")
        else:
            print(f"❌ Error: HTTP {r.status_code}")
    else:
        print("⚠️  No Vercel token")
except Exception as e:
    print(f"❌ Error: {e}")

print()
print("=" * 60)

