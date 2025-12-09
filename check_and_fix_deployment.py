#!/usr/bin/env python3
"""Check deployment status and auto-fix issues."""

import os
import sys
import httpx
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

VERCEL_TOKEN = os.getenv("VERCEL_TOKEN") or "n6QnE86DsiIcQXIdQp0SA34P"
CLOUDFLARE_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN") or "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"

PROJECT_NAME = "achillies"
DOMAIN = "corporatecrashouttrading.com"
CORRECT_ROOT_DIR = "apps/corporate-crashout"

print("\n" + "="*70)
print("🔍 Checking Deployment & Fixing Issues")
print("="*70 + "\n")

headers = {"Authorization": f"Bearer {VERCEL_TOKEN}"}

try:
    # 1. Get project
    print("[1] Getting project info...")
    project_url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}"
    
    with httpx.Client() as client:
        resp = client.get(project_url, headers=headers, timeout=30)
        
        if resp.status_code != 200:
            print(f"   ❌ Error: {resp.status_code}")
            print(f"   Response: {resp.text[:300]}")
            sys.exit(1)
        
        project = resp.json()
        root_dir = project.get("rootDirectory")
        
        print(f"   ✅ Project: {project.get('name')}")
        print(f"   Root Directory: {root_dir or 'NOT SET ❌'}")
        
        # Fix root directory if wrong
        if root_dir != CORRECT_ROOT_DIR:
            print(f"\n   ⚠️  Fixing root directory...")
            update_url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}"
            update_payload = {"rootDirectory": CORRECT_ROOT_DIR}
            update_resp = client.patch(update_url, headers=headers, json=update_payload, timeout=30)
            if update_resp.status_code == 200:
                print(f"   ✅ Root directory updated to: {CORRECT_ROOT_DIR}")
            else:
                print(f"   ❌ Failed to update: {update_resp.status_code}")
    
    # 2. Get deployments
    print("\n[2] Checking deployments...")
    deploy_url = f"https://api.vercel.com/v6/deployments?projectId={PROJECT_NAME}&limit=3"
    
    with httpx.Client() as client:
        resp = client.get(deploy_url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        deployments = data.get("deployments", [])
        
        if not deployments:
            print("   ❌ No deployments found!")
            print("\n   Possible causes:")
            print("   - Code not pushed to GitHub")
            print("   - Vercel not connected to GitHub repo")
            print("\n   Action: Push code to GitHub or connect repo in Vercel")
            sys.exit(1)
        
        latest = deployments[0]
        deploy_id = latest.get("uid")
        state = latest.get("state")
        target = latest.get("target")
        url = latest.get("url", "")
        
        print(f"   ✅ Latest deployment: {deploy_id[:16]}...")
        print(f"   State: {state}")
        print(f"   Target: {target or 'preview'}")
        
        # Promote to production if needed
        if state == "READY" and target != "production":
            print(f"\n   ⚠️  Promoting to production...")
            promote_url = f"https://api.vercel.com/v13/deployments/{deploy_id}/promote"
            promote_resp = client.post(promote_url, headers=headers, timeout=30)
            if promote_resp.status_code in [200, 201]:
                print(f"   ✅ Promoted to production!")
            else:
                print(f"   ⚠️  Could not promote (may need to do manually)")
        
        # Get logs if error
        if state == "ERROR":
            print(f"\n[3] Getting error logs...")
            logs_url = f"https://api.vercel.com/v2/deployments/{deploy_id}/events"
            logs_resp = client.get(logs_url, headers=headers, timeout=30)
            
            if logs_resp.status_code == 200:
                events = logs_resp.json()
                build_logs = []
                for event in events:
                    payload = event.get("payload", {})
                    if payload.get("text"):
                        build_logs.append(payload["text"])
                
                if build_logs:
                    error_logs = [log for log in build_logs if "error" in log.lower() or "failed" in log.lower()]
                    print(f"\n   ❌ Found {len(error_logs)} error(s):")
                    for error in error_logs[:10]:
                        print(f"      {error[:250]}")
    
    # 3. Check/add domain
    print(f"\n[3] Checking domain configuration...")
    domain_url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}/domains"
    
    with httpx.Client() as client:
        resp = client.get(domain_url, headers=headers, timeout=30)
        
        if resp.status_code == 200:
            domains_data = resp.json()
            domains = domains_data.get("domains", [])
            domain_names = [d.get("name") for d in domains]
            
            if DOMAIN not in domain_names:
                print(f"   ⚠️  Domain not added, adding now...")
                add_resp = client.post(domain_url, headers=headers, json={"name": DOMAIN}, timeout=30)
                if add_resp.status_code in [200, 201]:
                    print(f"   ✅ Domain added: {DOMAIN}")
                else:
                    print(f"   ⚠️  Could not add domain: {add_resp.status_code}")
            else:
                print(f"   ✅ Domain already added: {DOMAIN}")
            
            # Get DNS config for domain
            if DOMAIN in domain_names or add_resp.status_code in [200, 201]:
                print(f"\n[4] Getting DNS configuration...")
                dns_url = f"https://api.vercel.com/v4/domains/{DOMAIN}/config"
                dns_resp = client.get(dns_url, headers=headers, timeout=30)
                
                if dns_resp.status_code == 200:
                    dns_config = dns_resp.json()
                    dns_records = dns_config.get("dns_records", [])
                    
                    if dns_records:
                        print(f"   ✅ Got DNS records from Vercel")
                        
                        # Find A or CNAME for root
                        vercel_ip = None
                        vercel_cname = None
                        for record in dns_records:
                            if record.get("type") == "A" and (not record.get("name") or record.get("name") == "@" or record.get("name") == DOMAIN):
                                vercel_ip = record.get("value")
                            elif record.get("type") == "CNAME" and (not record.get("name") or record.get("name") == "@"):
                                vercel_cname = record.get("value")
                        
                        if vercel_ip or vercel_cname:
                            print(f"   Vercel DNS: {vercel_ip or vercel_cname}")
                            
                            # Update Cloudflare
                            print(f"\n[5] Updating Cloudflare DNS...")
                            try:
                                from infra.providers.cloudflare_client import CloudflareClient
                                from infra.utils.yaml_loader import load_provider_configs
                                
                                provider_configs = load_provider_configs()
                                cloudflare_config = provider_configs.get("cloudflare", {})
                                
                                cloudflare = CloudflareClient(cloudflare_config, env="prod", dry_run=False)
                                cloudflare.api_token = CLOUDFLARE_TOKEN  # Set token directly
                                
                                dns_result = cloudflare.update_root_domain_to_vercel(
                                    domain=DOMAIN,
                                    vercel_ip=vercel_ip,
                                    vercel_cname=vercel_cname
                                )
                                
                                if dns_result.get("updated") or dns_result.get("created"):
                                    print(f"   ✅ {dns_result.get('message', 'DNS updated')}")
                                else:
                                    print(f"   ⚠️  DNS update may have failed")
                            except Exception as e:
                                print(f"   ⚠️  Cloudflare update failed: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    if state == "READY":
        print("✅ Deployment is READY")
        if target == "production":
            print("✅ Set to PRODUCTION")
        else:
            print("⚠️  Check if promoted to production")
    elif state == "ERROR":
        print("❌ Deployment FAILED - check errors above")
    elif state == "BUILDING":
        print("⏳ Deployment is BUILDING")
    
    print(f"\n✅ Root directory: {CORRECT_ROOT_DIR}")
    print(f"✅ Domain: {DOMAIN}")
    print("\n🎉 Checks complete! Site should be live soon.")
    print("="*70)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
