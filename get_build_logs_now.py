#!/usr/bin/env python3
"""Get build logs and fix issues - direct output."""

import os
import sys
import httpx
import json

VERCEL_TOKEN = "n6QnE86DsiIcQXIdQp0SA34P"
PROJECT_NAME = "achillies"
DOMAIN = "corporatecrashouttrading.com"

headers = {"Authorization": f"Bearer {VERCEL_TOKEN}"}

print("\n" + "="*70)
print("🔍 Corporate Crashout - Build Status & Logs")
print("="*70 + "\n")

try:
    # Get project
    project_url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}"
    with httpx.Client() as client:
        resp = client.get(project_url, headers=headers, timeout=30)
        if resp.status_code == 200:
            project = resp.json()
            root_dir = project.get("rootDirectory")
            print(f"✅ Project: {project.get('name')}")
            print(f"   Root Directory: {root_dir or 'NOT SET ❌'}")
            
            # Fix if wrong
            if root_dir != "apps/corporate-crashout":
                print(f"\n⚠️  Fixing root directory...")
                update_resp = client.patch(project_url, headers=headers, json={"rootDirectory": "apps/corporate-crashout"}, timeout=30)
                if update_resp.status_code == 200:
                    print(f"   ✅ Fixed! Root directory set to: apps/corporate-crashout")
        else:
            print(f"❌ Project error: {resp.status_code}")
            print(f"   {resp.text[:200]}")
    
    # Get deployments
    print(f"\n📦 Deployments:")
    deploy_url = f"https://api.vercel.com/v6/deployments?projectId={PROJECT_NAME}&limit=3"
    with httpx.Client() as client:
        resp = client.get(deploy_url, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            deployments = data.get("deployments", [])
            
            if not deployments:
                print("   ❌ No deployments found!")
                print("   → Code may not be on GitHub")
                print("   → Vercel may not be connected to GitHub repo")
            else:
                latest = deployments[0]
                deploy_id = latest.get("uid")
                state = latest.get("state")
                target = latest.get("target")
                url = latest.get("url", "")
                
                print(f"\n   Latest: {deploy_id[:20]}...")
                print(f"   State: {state}")
                print(f"   Target: {target or 'preview'}")
                print(f"   URL: https://{url}" if url else "   URL: N/A")
                
                # Promote if ready but not production
                if state == "READY" and target != "production":
                    print(f"\n   ⚠️  Promoting to production...")
                    promote_url = f"https://api.vercel.com/v13/deployments/{deploy_id}/promote"
                    promote_resp = client.post(promote_url, headers=headers, timeout=30)
                    if promote_resp.status_code in [200, 201]:
                        print(f"   ✅ Promoted to production!")
                
                # Get logs
                if state == "ERROR" or state == "BUILDING":
                    print(f"\n   📝 Getting build logs...")
                    logs_url = f"https://api.vercel.com/v2/deployments/{deploy_id}/events"
                    logs_resp = client.get(logs_url, headers=headers, timeout=30)
                    
                    if logs_resp.status_code == 200:
                        events = logs_resp.json()
                        logs = []
                        for event in events:
                            payload = event.get("payload", {})
                            text = payload.get("text", "")
                            if text:
                                logs.append(text)
                        
                        if logs:
                            errors = [l for l in logs if "error" in l.lower() or "failed" in l.lower()]
                            if errors:
                                print(f"\n   ❌ ERRORS ({len(errors)}):")
                                for err in errors[:15]:
                                    print(f"      {err[:200]}")
                            
                            print(f"\n   Recent logs (last 25):")
                            for log in logs[-25:]:
                                clean = log.replace("\n", " ")[:180]
                                if clean:
                                    print(f"      {clean}")
    
    # Check domain
    print(f"\n🌐 Domain: {DOMAIN}")
    domain_url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}/domains"
    with httpx.Client() as client:
        resp = client.get(domain_url, headers=headers, timeout=30)
        if resp.status_code == 200:
            domains = resp.json().get("domains", [])
            domain_names = [d.get("name") for d in domains]
            
            if DOMAIN not in domain_names:
                print(f"   ⚠️  Not added - adding now...")
                add_resp = client.post(domain_url, headers=headers, json={"name": DOMAIN}, timeout=30)
                if add_resp.status_code in [200, 201]:
                    print(f"   ✅ Domain added!")
                else:
                    print(f"   ⚠️  Add failed: {add_resp.status_code}")
            else:
                print(f"   ✅ Domain is added")
            
            # Get DNS and update Cloudflare
            if DOMAIN in domain_names or (DOMAIN not in domain_names and add_resp.status_code in [200, 201]):
                dns_url = f"https://api.vercel.com/v4/domains/{DOMAIN}/config"
                dns_resp = client.get(dns_url, headers=headers, timeout=30)
                if dns_resp.status_code == 200:
                    dns_config = dns_resp.json()
                    dns_records = dns_config.get("dns_records", [])
                    
                    vercel_ip = None
                    vercel_cname = None
                    for record in dns_records:
                        if record.get("type") == "A" and (not record.get("name") or record.get("name") == "@"):
                            vercel_ip = record.get("value")
                        elif record.get("type") == "CNAME" and (not record.get("name") or record.get("name") == "@"):
                            vercel_cname = record.get("value")
                    
                    if vercel_ip or vercel_cname:
                        print(f"\n   🔧 Updating Cloudflare DNS...")
                        try:
                            import sys
                            from pathlib import Path
                            sys.path.insert(0, str(Path(__file__).parent))
                            from infra.providers.cloudflare_client import CloudflareClient
                            
                            cloudflare = CloudflareClient({}, env="prod", dry_run=False)
                            cloudflare.api_token = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"
                            
                            result = cloudflare.update_root_domain_to_vercel(
                                domain=DOMAIN,
                                vercel_ip=vercel_ip,
                                vercel_cname=vercel_cname
                            )
                            
                            if result.get("updated") or result.get("created"):
                                print(f"   ✅ {result.get('message')}")
                            else:
                                print(f"   ⚠️  DNS update may have failed")
                        except Exception as e:
                            print(f"   ⚠️  DNS update error: {str(e)[:200]}")
    
    print("\n" + "="*70)
    print("✅ Complete! Check status above.")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
