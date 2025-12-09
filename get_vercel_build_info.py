#!/usr/bin/env python3
"""Get Vercel build information directly from API."""

import os
import sys
import json
import httpx
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")
PROJECT_NAME = "achillies"

if not VERCEL_TOKEN:
    print("ERROR: VERCEL_TOKEN not set")
    print("Please set it in .env file or environment")
    sys.exit(1)

print("\n" + "="*70)
print("🔍 Vercel Deployment Status Check")
print("="*70)
print(f"Project: {PROJECT_NAME}")
print(f"Token: {VERCEL_TOKEN[:10]}...")
print("="*70 + "\n")

headers = {"Authorization": f"Bearer {VERCEL_TOKEN}"}

try:
    # 1. Get project info
    print("[1] Checking project configuration...")
    project_url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}"
    
    with httpx.Client() as client:
        resp = client.get(project_url, headers=headers, timeout=30)
        
        if resp.status_code == 404:
            print(f"   ❌ Project '{PROJECT_NAME}' not found")
            print("\n   Possible issues:")
            print("   - Project name is different")
            print("   - Project doesn't exist in Vercel")
            print("   - Check: https://vercel.com/dashboard")
            sys.exit(1)
        elif resp.status_code != 200:
            print(f"   ❌ Error: {resp.status_code}")
            print(f"   Response: {resp.text[:300]}")
            sys.exit(1)
        
        project = resp.json()
        root_dir = project.get("rootDirectory")
        
        print(f"   ✅ Project found")
        print(f"   Name: {project.get('name')}")
        print(f"   Root Directory: {root_dir or 'NOT SET ❌'}")
        
        if root_dir != "apps/corporate-crashout":
            print(f"\n   ⚠️  WARNING: Root directory is wrong!")
            print(f"   Should be: apps/corporate-crashout")
            print(f"   Current: {root_dir or '(not set)'}")
    
    # 2. Get deployments
    print("\n[2] Getting deployments...")
    deploy_url = f"https://api.vercel.com/v6/deployments?projectId={PROJECT_NAME}&limit=5"
    
    with httpx.Client() as client:
        resp = client.get(deploy_url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        deployments = data.get("deployments", [])
        
        if not deployments:
            print("   ❌ No deployments found")
            print("\n   This means:")
            print("   - Code may not be pushed to GitHub")
            print("   - Vercel project not connected to GitHub")
            print("   - No deployments triggered yet")
            print("\n   Action: Check Vercel dashboard → Settings → Git")
            sys.exit(1)
        
        print(f"   ✅ Found {len(deployments)} deployment(s)")
        
        latest = deployments[0]
        deploy_id = latest.get("uid")
        state = latest.get("state")
        target = latest.get("target")  # production or None
        url = latest.get("url", "")
        created = latest.get("createdAt", 0)
        
        print(f"\n   Latest Deployment:")
        print(f"   ID: {deploy_id}")
        print(f"   State: {state}")
        print(f"   Target: {target or 'preview'}")
        print(f"   URL: https://{url}" if url else "   URL: (not available)")
        
        if state == "READY":
            print(f"   ✅ Deployment is READY")
        elif state == "ERROR":
            print(f"   ❌ Deployment FAILED")
        elif state == "BUILDING":
            print(f"   ⏳ Deployment is BUILDING")
        else:
            print(f"   ⚠️  Unknown state: {state}")
    
    # 3. Get build logs
    if deploy_id:
        print(f"\n[3] Getting build logs for {deploy_id[:12]}...")
        logs_url = f"https://api.vercel.com/v2/deployments/{deploy_id}/events"
        
        with httpx.Client() as client:
            resp = client.get(logs_url, headers=headers, timeout=30)
            
            if resp.status_code == 200:
                events = resp.json()
                
                # Filter build logs
                build_logs = []
                for event in events:
                    payload = event.get("payload", {})
                    if payload.get("text"):
                        build_logs.append(payload["text"])
                
                if build_logs:
                    print(f"   ✅ Retrieved {len(build_logs)} log entries")
                    
                    # Check for errors
                    error_lines = [log for log in build_logs if "error" in log.lower() or "failed" in log.lower() or "❌" in log]
                    
                    if error_lines:
                        print(f"\n   ⚠️  Found {len(error_lines)} error(s) in logs:")
                        for error in error_lines[:10]:
                            print(f"      {error[:200]}")
                    
                    # Show last 20 log lines
                    print(f"\n   Recent build output (last 20 lines):")
                    print("   " + "-"*66)
                    for log in build_logs[-20:]:
                        # Clean up log output
                        clean_log = log.replace("\n", " ").strip()
                        if clean_log:
                            print(f"   {clean_log[:200]}")
                else:
                    print("   ⚠️  No build logs found")
            else:
                print(f"   ⚠️  Could not get logs (status: {resp.status_code})")
    
    # 4. Check domains
    print(f"\n[4] Checking domain configuration...")
    domain_url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}/domains"
    
    with httpx.Client() as client:
        resp = client.get(domain_url, headers=headers, timeout=30)
        
        if resp.status_code == 200:
            domains_data = resp.json()
            domains = domains_data.get("domains", [])
            
            if domains:
                print(f"   ✅ Found {len(domains)} domain(s):")
                for domain in domains:
                    name = domain.get("name")
                    config_status = domain.get("configurationStatus", "unknown")
                    verified = domain.get("verified", False)
                    status_icon = "✅" if config_status == "valid_configuration" else "⚠️"
                    print(f"      {status_icon} {name}")
                    print(f"         Status: {config_status}")
                    print(f"         Verified: {verified}")
            else:
                print("   ⚠️  No domains configured")
                print("   Need to add: corporatecrashouttrading.com")
        else:
            print(f"   ⚠️  Could not check domains (status: {resp.status_code})")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    if state == "READY":
        if target == "production":
            print("✅ Deployment is READY and set to PRODUCTION")
            print("\nIf site not accessible:")
            print("1. Check DNS: corporatecrashouttrading.com → Vercel")
            print("2. Wait 5-10 min for DNS propagation")
            print("3. Verify domain added in Vercel")
        else:
            print("✅ Deployment is READY but set to PREVIEW")
            print("\n⚠️  Action needed:")
            print("1. Go to Vercel dashboard")
            print("2. Deployments → Latest → Promote to Production")
    elif state == "ERROR":
        print("❌ Deployment FAILED")
        print("\n⚠️  Action needed:")
        print("1. Review errors above")
        print("2. Fix code issues")
        print("3. Push to GitHub")
        print("4. Vercel will redeploy automatically")
    elif state == "BUILDING":
        print("⏳ Deployment is BUILDING")
        print("\nPlease wait for build to complete...")
    
    if root_dir != "apps/corporate-crashout":
        print("\n⚠️  ROOT DIRECTORY ISSUE:")
        print(f"   Current: {root_dir or '(not set)'}")
        print(f"   Should be: apps/corporate-crashout")
        print("\n   Fix in Vercel dashboard:")
        print("   Settings → General → Root Directory")
    
    print("\n" + "="*70)
    
except httpx.HTTPStatusError as e:
    print(f"\n❌ HTTP Error: {e.response.status_code}")
    print(f"Response: {e.response.text[:500]}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
