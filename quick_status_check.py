#!/usr/bin/env python3
import os, sys, httpx, yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

print("🔍 Quick Status Check\n")

# Check Render
api_key = os.getenv("RENDER_API_KEY")
if api_key:
    try:
        url = "https://api.render.com/v1/services"
        headers = {"Authorization": f"Bearer {api_key}"}
        r = httpx.get(url, headers=headers, timeout=10)
        services = r.json()
        symbioz_services = [s for s in services if 'symbioz' in str(s).lower() or 'mellivox' in str(s).lower()]
        print(f"📦 Render: Found {len(symbioz_services)} Symbioz service(s)")
        for s in symbioz_services:
            svc = s.get('service', {})
            print(f"   - {svc.get('name')}: {svc.get('id')} ({svc.get('deployStatus', 'unknown')})")
    except Exception as e:
        print(f"📦 Render: Error - {e}")
else:
    print("📦 Render: No API key")

# Check Vercel
token = os.getenv("VERCEL_TOKEN")
if token:
    try:
        url = "https://api.vercel.com/v9/projects/symbioz"
        headers = {"Authorization": f"Bearer {token}"}
        r = httpx.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            proj = r.json()
            print(f"\n🌐 Vercel: Project '{proj.get('name')}' exists")
            # Get deployments
            deploy_url = "https://api.vercel.com/v13/deployments"
            params = {"projectId": "symbioz", "limit": 1}
            r2 = httpx.get(deploy_url, headers=headers, params=params, timeout=10)
            if r2.status_code == 200:
                deps = r2.json().get("deployments", [])
                if deps:
                    dep = deps[0]
                    print(f"   Latest: {dep.get('state')} - https://{dep.get('url', 'N/A')}")
        else:
            print(f"\n🌐 Vercel: Project not found (HTTP {r.status_code})")
    except Exception as e:
        print(f"\n🌐 Vercel: Error - {e}")
else:
    print("\n🌐 Vercel: No token")

print()

