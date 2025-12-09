#!/usr/bin/env python3
"""Quick check of Vercel build status."""

import os
import sys
import httpx
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

PROJECT_NAME = "achillies"
VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")

if not VERCEL_TOKEN:
    print("ERROR: VERCEL_TOKEN not set in environment")
    sys.exit(1)

print("\n" + "="*70)
print("🔍 Checking Vercel Deployment Status")
print("="*70 + "\n")

headers = {"Authorization": f"Bearer {VERCEL_TOKEN}"}

try:
    # Get project
    print(f"[1/4] Getting project info: {PROJECT_NAME}")
    project_url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}"
    with httpx.Client() as client:
        project_resp = client.get(project_url, headers=headers, timeout=30)
        if project_resp.status_code == 200:
            project = project_resp.json()
            print(f"   ✅ Project found: {project.get('name')}")
            print(f"   Root Directory: {project.get('rootDirectory', 'NOT SET ❌')}")
        else:
            print(f"   ❌ Project not found (status: {project_resp.status_code})")
            print(f"   Response: {project_resp.text[:200]}")
    
    # Get deployments
    print(f"\n[2/4] Getting latest deployments...")
    deploy_url = f"https://api.vercel.com/v6/deployments?projectId={PROJECT_NAME}&limit=3"
    with httpx.Client() as client:
        deploy_resp = client.get(deploy_url, headers=headers, timeout=30)
        if deploy_resp.status_code == 200:
            data = deploy_resp.json()
            deployments = data.get("deployments", [])
            
            if not deployments:
                print("   ❌ No deployments found")
                print("\n   Possible issues:")
                print("   - Code not pushed to GitHub")
                print("   - Vercel not connected to GitHub repo")
            else:
                print(f"   ✅ Found {len(deployments)} deployment(s)")
                
                for i, deploy in enumerate(deployments[:3], 1):
                    deploy_id = deploy.get("uid", "unknown")
                    state = deploy.get("state", "unknown")
                    target = deploy.get("target")  # production or None
                    url = deploy.get("url", "N/A")
                    created = deploy.get("createdAt", 0)
                    
                    status_icon = "✅" if state == "READY" else "⏳" if state == "BUILDING" else "❌"
                    target_label = "PRODUCTION" if target == "production" else "PREVIEW"
                    
                    print(f"\n   {i}. {status_icon} {target_label}")
                    print(f"      ID: {deploy_id[:16]}...")
                    print(f"      State: {state}")
                    print(f"      URL: https://{url}" if url != "N/A" else "      URL: N/A")
                    
                    if i == 1:
                        latest_id = deploy_id
                        latest_state = state
        else:
            print(f"   ❌ Failed to get deployments (status: {deploy_resp.status_code})")
            latest_id = None
            latest_state = None
    
    # Get logs for latest deployment
    if latest_id and latest_state:
        print(f"\n[3/4] Getting build logs for latest deployment...")
        logs_url = f"https://api.vercel.com/v2/deployments/{latest_id}/events"
        with httpx.Client() as client:
            logs_resp = client.get(logs_url, headers=headers, timeout=30)
            if logs_resp.status_code == 200:
                events = logs_resp.json()
                
                # Filter for build logs
                build_logs = [e for e in events if e.get("type") == "command" or e.get("payload", {}).get("type") == "stdout" or e.get("payload", {}).get("type") == "stderr"]
                
                if build_logs:
                    print(f"   ✅ Retrieved {len(build_logs)} log events")
                    
                    # Show errors
                    errors = [e for e in build_logs if "error" in str(e).lower() or e.get("payload", {}).get("type") == "stderr"]
                    if errors:
                        print(f"\n   ⚠️  Found {len(errors)} potential error(s):")
                        for error in errors[:5]:
                            payload = error.get("payload", {})
                            text = payload.get("text", str(error))
                            if text:
                                print(f"      ❌ {str(text)[:200]}")
                    
                    # Show last 10 log entries
                    print(f"\n   Recent log entries:")
                    for log in build_logs[-10:]:
                        payload = log.get("payload", {})
                        text = payload.get("text", str(log))
                        if text:
                            print(f"      {str(text)[:150]}")
                else:
                    print("   ⚠️  No build logs found")
            else:
                print(f"   ⚠️  Could not get logs (status: {logs_resp.status_code})")
    
    # Check domains
    print(f"\n[4/4] Checking domain configuration...")
    domain_url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}/domains"
    with httpx.Client() as client:
        domain_resp = client.get(domain_url, headers=headers, timeout=30)
        if domain_resp.status_code == 200:
            domains_data = domain_resp.json()
            domains = domains_data.get("domains", [])
            if domains:
                print(f"   ✅ Found {len(domains)} domain(s):")
                for domain in domains:
                    name = domain.get("name")
                    config_status = domain.get("configurationStatus", "unknown")
                    print(f"      - {name} ({config_status})")
            else:
                print("   ⚠️  No domains configured")
                print("      Need to add: corporatecrashouttrading.com")
        else:
            print(f"   ⚠️  Could not check domains (status: {domain_resp.status_code})")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    if latest_state == "READY":
        print("✅ Deployment is READY")
        print("\nIf site not accessible:")
        print("1. Check DNS is pointing to Vercel")
        print("2. Verify deployment is Production (not Preview)")
        print("3. Check domain is added: corporatecrashouttrading.com")
    elif latest_state == "ERROR":
        print("❌ Deployment FAILED")
        print("\nReview errors above and fix code, then push to GitHub")
    elif latest_state == "BUILDING":
        print("⏳ Deployment is BUILDING")
        print("\nWait a few minutes and check again")
    elif not latest_state:
        print("❌ No deployments found")
        print("\nCode may not be pushed to GitHub yet")
    
    print("\n" + "="*70)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
