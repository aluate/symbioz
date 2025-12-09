#!/usr/bin/env python3
"""
Diagnose what's missing to get Symbioz live
"""

import os, sys, httpx, yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

print("🔍 Diagnosing Symbioz Deployment Issues...")
print("=" * 60)
print()

api_key = os.getenv("RENDER_API_KEY")
vercel_token = os.getenv("VERCEL_TOKEN")

# Check 1: Render Service Configuration
print("1. Render Service Configuration:")
print("-" * 60)
config = yaml.safe_load(open("infra/providers/render.yaml"))
symbioz_config = config["services"]["symbioz-api"]
service_id = symbioz_config.get("render_service_id", "")

print(f"   Service ID: {service_id}")
print(f"   Root Directory: {symbioz_config.get('root_dir', '❌ MISSING')}")
print(f"   Build Command: {symbioz_config.get('build_command', 'N/A')}")
print(f"   Start Command: {symbioz_config.get('start_command', 'N/A')}")
print()

if not symbioz_config.get("root_dir"):
    print("   ⚠️  ISSUE: root_dir is missing!")
    print("   💡 Should be: apps/symbioz_cli")
    print()

# Check 2: Render Service Status
print("2. Render Service Status:")
print("-" * 60)
if api_key and service_id:
    try:
        url = f"https://api.render.com/v1/services/{service_id}"
        r = httpx.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=15)
        if r.status_code == 200:
            svc = r.json().get("service", r.json())
            details = svc.get("serviceDetails", {})
            status = details.get("deployStatus", "unknown")
            url_svc = details.get("url", "")
            root_dir = details.get("rootDir", "")
            
            print(f"   Status: {status}")
            print(f"   URL: {url_svc if url_svc else 'N/A'}")
            print(f"   Root Dir (in Render): {root_dir if root_dir else '❌ NOT SET'}")
            print()
            
            if status in ["build_failed", "update_failed"]:
                print("   ❌ Deployment failed!")
                # Get latest deployment
                dep_url = f"https://api.render.com/v1/services/{service_id}/deploys"
                dep_r = httpx.get(dep_url, headers={"Authorization": f"Bearer {api_key}"}, params={"limit": 1}, timeout=15)
                if dep_r.status_code == 200:
                    deps = dep_r.json()
                    if deps:
                        dep = deps[0].get("deploy", deps[0])
                        error_msg = dep.get("message", dep.get("error", "Unknown error"))
                        print(f"   Error: {error_msg[:200]}")
        else:
            print(f"   ❌ Error: HTTP {r.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error checking: {e}")
else:
    print("   ⚠️  No API key or service ID")
print()

# Check 3: Required Files
print("3. Required Files:")
print("-" * 60)
workspace = Path(".")
symbioz_cli = workspace / "apps" / "symbioz_cli"
req_file = symbioz_cli / "requirements.txt"
api_file = symbioz_cli / "api_server.py"

print(f"   requirements.txt: {'✅' if req_file.exists() else '❌'} {req_file}")
print(f"   api_server.py: {'✅' if api_file.exists() else '❌'} {api_file}")
print()

# Check 4: Vercel Configuration
print("4. Vercel Configuration:")
print("-" * 60)
vercel_config = yaml.safe_load(open("infra/providers/vercel.yaml"))
symbioz_vercel = vercel_config["projects"]["symbioz"]
print(f"   Project ID: {symbioz_vercel.get('project_id', 'N/A')}")
print(f"   Required Env Vars: {symbioz_vercel.get('required_env_vars', [])}")
print()

if vercel_token:
    try:
        url = "https://api.vercel.com/v9/projects/symbioz"
        r = httpx.get(url, headers={"Authorization": f"Bearer {vercel_token}"}, timeout=15)
        if r.status_code == 200:
            proj = r.json()
            print(f"   ✅ Project exists: {proj.get('name')}")
            
            # Check env vars
            env_url = f"https://api.vercel.com/v9/projects/symbioz/env"
            env_r = httpx.get(env_url, headers={"Authorization": f"Bearer {vercel_token}"}, timeout=15)
            if env_r.status_code == 200:
                envs = env_r.json().get("envs", [])
                api_url_set = any(e.get("key") == "NEXT_PUBLIC_API_URL" for e in envs)
                print(f"   NEXT_PUBLIC_API_URL: {'✅ Set' if api_url_set else '❌ MISSING'}")
        elif r.status_code == 404:
            print("   ⚠️  Project not found in Vercel")
        else:
            print(f"   ⚠️  Error: HTTP {r.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
else:
    print("   ⚠️  No Vercel token")
print()

# Summary
print("=" * 60)
print("SUMMARY - What's Missing:")
print("=" * 60)

missing = []

if not symbioz_config.get("root_dir"):
    missing.append("❌ Render root_dir not set (should be: apps/symbioz_cli)")

if api_key and service_id:
    try:
        url = f"https://api.render.com/v1/services/{service_id}"
        r = httpx.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=15)
        if r.status_code == 200:
            svc = r.json().get("service", r.json())
            details = svc.get("serviceDetails", {})
            if not details.get("rootDir"):
                missing.append("❌ Render service rootDir not configured")
            if details.get("deployStatus") in ["build_failed", "update_failed"]:
                missing.append("❌ Render deployment failed (needs fixing)")
except:
    pass

if vercel_token:
    try:
        env_url = f"https://api.vercel.com/v9/projects/symbioz/env"
        env_r = httpx.get(env_url, headers={"Authorization": f"Bearer {vercel_token}"}, timeout=15)
        if env_r.status_code == 200:
            envs = env_r.json().get("envs", [])
            if not any(e.get("key") == "NEXT_PUBLIC_API_URL" for e in envs):
                missing.append("❌ Vercel NEXT_PUBLIC_API_URL not set")
    except:
        pass

if missing:
    for item in missing:
        print(f"  {item}")
    print()
    print("💡 Otto can fix these automatically!")
else:
    print("  ✅ Everything looks configured!")
    print("  💡 Check deployment status to see if it's live")

print()

