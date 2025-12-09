#!/usr/bin/env python3
"""Check Corporate Crashout deployment status and logs."""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs
from dotenv import load_dotenv
import httpx

load_dotenv()

PROJECT_NAME = "achillies"

print("\n" + "="*60)
print("🔍 Checking Corporate Crashout Deployment Status")
print("="*60 + "\n")

try:
    # Load configs
    provider_configs = load_provider_configs()
    vercel_config = provider_configs.get("vercel", {})
    
    projects = vercel_config.get("projects", {})
    if PROJECT_NAME not in projects:
        print(f"❌ Project '{PROJECT_NAME}' not found in vercel.yaml")
        sys.exit(1)
    
    project_config = projects[PROJECT_NAME]
    project_id = project_config.get("project_id") or PROJECT_NAME
    
    # Initialize Vercel client
    vercel_client = VercelClient(vercel_config, env="prod", dry_run=False)
    
    print(f"📦 Project: {project_id}")
    print("-" * 60)
    
    # Get project info
    project = vercel_client._get_project(project_id)
    if not project:
        print(f"❌ Project '{project_id}' not found in Vercel")
        print("\nManual check:")
        print("1. Go to: https://vercel.com/dashboard")
        print(f"2. Check if project '{project_id}' exists")
        sys.exit(1)
    
    print(f"✅ Project found: {project.get('name')}")
    print(f"   Root Directory: {project.get('rootDirectory', 'NOT SET')}")
    print(f"   Framework: {project.get('framework', 'Unknown')}")
    
    # Get latest deployments
    print("\n📋 Latest Deployments:")
    print("-" * 60)
    
    deployments = vercel_client._list_deployments(project_id, limit=5)
    
    if not deployments:
        print("❌ No deployments found")
        print("\nPossible issues:")
        print("- Code may not be pushed to GitHub")
        print("- Vercel project not connected to GitHub repo")
        print("- Check: https://vercel.com/dashboard → Settings → Git")
    else:
        for i, deployment in enumerate(deployments[:5], 1):
            deployment_id = deployment.get("uid")
            state = deployment.get("state")
            url = deployment.get("url", "N/A")
            created = deployment.get("created")
            target = deployment.get("target")  # "production" or "staging"
            
            status_emoji = "✅" if state == "READY" else "⏳" if state == "BUILDING" else "❌"
            print(f"\n{i}. {status_emoji} Deployment: {deployment_id[:12]}...")
            print(f"   State: {state}")
            print(f"   Target: {target or 'preview'}")
            print(f"   URL: https://{url}" if url != "N/A" else f"   URL: {url}")
            print(f"   Created: {created}")
            
            # Get detailed logs for latest deployment
            if i == 1:
                print(f"\n   📝 Getting build logs...")
                try:
                    logs = vercel_client.get_deployment_logs(deployment_id)
                    if logs:
                        print(f"   ✅ Retrieved {len(logs)} log entries")
                        
                        # Check for errors
                        error_logs = [log for log in logs if log.get("type") == "error" or "error" in log.get("payload", {}).get("text", "").lower()]
                        warning_logs = [log for log in logs if log.get("type") == "warning"]
                        
                        if error_logs:
                            print(f"\n   ⚠️  Found {len(error_logs)} error(s):")
                            for error in error_logs[:10]:  # Show first 10 errors
                                payload = error.get("payload", {})
                                text = payload.get("text", "")
                                if text and len(text) > 0:
                                    print(f"      ❌ {text[:200]}")
                        
                        if warning_logs and len(warning_logs) > 0:
                            print(f"\n   ⚠️  Found {len(warning_logs)} warning(s)")
                        
                        # Show recent logs
                        print(f"\n   📋 Recent log entries (last 10):")
                        for log in logs[-10:]:
                            payload = log.get("payload", {})
                            log_type = log.get("type", "info")
                            text = payload.get("text", "")
                            if text:
                                prefix = "   " if log_type == "info" else "   ⚠️ " if log_type == "warning" else "   ❌"
                                print(f"{prefix} {text[:150]}")
                    else:
                        print("   ⚠️  No logs available yet")
                except Exception as e:
                    print(f"   ⚠️  Could not retrieve logs: {e}")
                
                # Check for specific issues
                if state != "READY":
                    print(f"\n   🔍 Analyzing deployment state...")
                    
                    if state == "ERROR":
                        print("   ❌ Deployment failed")
                        print("\n   Common fixes:")
                        print("   1. Check build logs above for specific errors")
                        print("   2. Verify root directory is: apps/corporate-crashout")
                        print("   3. Check environment variables are set")
                        print("   4. Verify code is pushed to GitHub")
                    elif state == "BUILDING":
                        print("   ⏳ Deployment is still building...")
                        print("   Wait a few minutes and check again")
                    elif state == "QUEUED":
                        print("   ⏳ Deployment is queued...")
                        print("   Wait a moment and check again")
    
    # Check domain configuration
    print("\n" + "="*60)
    print("🌐 Domain Configuration")
    print("="*60)
    
    try:
        # Try to get domain info
        token = vercel_config.get("api_token") or os.getenv("VERCEL_TOKEN")
        if token:
            url = f"https://api.vercel.com/v9/projects/{project_id}/domains"
            headers = {"Authorization": f"Bearer {token}"}
            with httpx.Client() as client:
                response = client.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    domains_data = response.json()
                    domains = domains_data.get("domains", [])
                    if domains:
                        print(f"\n✅ Found {len(domains)} domain(s):")
                        for domain in domains:
                            domain_name = domain.get("name")
                            domain_status = domain.get("configurationStatus", "unknown")
                            print(f"   - {domain_name} ({domain_status})")
                    else:
                        print("\n⚠️  No domains configured")
                        print("   Domain 'corporatecrashouttrading.com' needs to be added")
    except Exception as e:
        print(f"\n⚠️  Could not check domains: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 Summary")
    print("="*60)
    
    if deployments:
        latest = deployments[0]
        latest_state = latest.get("state")
        
        if latest_state == "READY":
            print("✅ Latest deployment is READY")
            print("\nIf site is not accessible:")
            print("1. Check domain DNS is pointing to Vercel")
            print("2. Verify deployment is promoted to Production")
            print("3. Wait 5-10 minutes for DNS propagation")
            print("4. Check: https://vercel.com/dashboard → Deployments → Latest")
        elif latest_state == "ERROR":
            print("❌ Latest deployment FAILED")
            print("\nAction required:")
            print("1. Review error logs above")
            print("2. Fix issues in code")
            print("3. Push fixes to GitHub")
            print("4. Vercel will redeploy automatically")
        else:
            print(f"⏳ Latest deployment: {latest_state}")
            print("   Wait for deployment to complete")
    else:
        print("❌ No deployments found")
        print("\nAction required:")
        print("1. Verify code is pushed to GitHub")
        print("2. Check Vercel project is connected to GitHub repo")
        print("3. Check: https://vercel.com/dashboard → Settings → Git")
    
    print("\n" + "="*60)
    
except Exception as e:
    print(f"\n❌ Error checking deployment: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
