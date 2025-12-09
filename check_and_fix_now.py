#!/usr/bin/env python3
"""Check and fix deployment - writes results to file."""

import os
import sys
import httpx
import json
from pathlib import Path

# Set tokens
os.environ["VERCEL_TOKEN"] = "n6QnE86DsiIcQXIdQp0SA34P"
os.environ["CLOUDFLARE_API_TOKEN"] = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"

VERCEL_TOKEN = os.environ["VERCEL_TOKEN"]
PROJECT = "achillies"
DOMAIN = "corporatecrashouttrading.com"

# Force output
sys.stdout.reconfigure(encoding='utf-8', errors='replace') if hasattr(sys.stdout, 'reconfigure') else None

headers = {"Authorization": f"Bearer {VERCEL_TOKEN}"}

print("\n" + "="*70)
print("CHECKING DEPLOYMENT STATUS")
print("="*70 + "\n")

# Write results to file
results = []
results.append("# Build Status & Logs Report\n")
results.append(f"Project: {PROJECT}\n\n")

try:
    # Get project
    project_url = f"https://api.vercel.com/v9/projects/{PROJECT}"
    with httpx.Client() as client:
        resp = client.get(project_url, headers=headers, timeout=30)
        if resp.status_code == 200:
            project = resp.json()
            root_dir = project.get("rootDirectory")
            print(f"[1] Project Root Directory: {root_dir}")
            results.append(f"## Root Directory: {root_dir or 'NOT SET'}\n")
            
            # Fix if wrong
            if root_dir != "apps/corporate-crashout":
                print(f"[2] Fixing root directory...")
                update_resp = client.patch(project_url, headers=headers, json={"rootDirectory": "apps/corporate-crashout"}, timeout=30)
                if update_resp.status_code == 200:
                    print(f"[2] ✅ FIXED!")
                    results.append(f"✅ **FIXED** Root directory set to: apps/corporate-crashout\n")
        
        # Get deployments
        print(f"[3] Getting deployments...")
        deploy_url = f"https://api.vercel.com/v6/deployments?projectId={PROJECT}&limit=3"
        resp = client.get(deploy_url, headers=headers, timeout=30)
        
        if resp.status_code == 200:
            data = resp.json()
            deployments = data.get("deployments", [])
            
            if not deployments:
                print(f"[3] ❌ No deployments!")
                results.append(f"## ❌ No Deployments Found\n")
                results.append("Code may not be pushed to GitHub or Vercel not connected.\n")
            else:
                latest = deployments[0]
                deploy_id = latest.get("uid")
                state = latest.get("state")
                target = latest.get("target")
                url = latest.get("url", "")
                
                print(f"[3] ✅ Found deployment: {state}")
                results.append(f"## Deployment Status\n")
                results.append(f"- **State:** {state}\n")
                results.append(f"- **Target:** {target or 'preview'}\n")
                results.append(f"- **URL:** https://{url}\n\n")
                
                # Promote
                if state == "READY" and target != "production":
                    print(f"[4] Promoting to production...")
                    promote_url = f"https://api.vercel.com/v13/deployments/{deploy_id}/promote"
                    promote_resp = client.post(promote_url, headers=headers, timeout=30)
                    if promote_resp.status_code in [200, 201]:
                        print(f"[4] ✅ Promoted!")
                        results.append(f"✅ **Promoted to production**\n\n")
                
                # Get logs
                if state == "ERROR":
                    print(f"[5] Getting error logs...")
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
                        
                        errors = [l for l in logs if "error" in l.lower() or "failed" in l.lower()]
                        
                        print(f"[5] Found {len(errors)} errors in {len(logs)} logs")
                        results.append(f"## ❌ Build Errors ({len(errors)} found)\n\n")
                        
                        if errors:
                            results.append("### Error Messages:\n```\n")
                            for err in errors[:10]:
                                results.append(err[:300] + "\n")
                            results.append("```\n\n")
                        
                        results.append("### Recent Build Output:\n```\n")
                        for log in logs[-25:]:
                            clean = log.replace("\n", " ")[:200].strip()
                            if clean:
                                results.append(clean + "\n")
                        results.append("```\n")
                
                # Domain & DNS
                print(f"[6] Checking domain...")
                domain_url = f"https://api.vercel.com/v9/projects/{PROJECT}/domains"
                domain_resp = client.get(domain_url, headers=headers, timeout=30)
                
                if domain_resp.status_code == 200:
                    domains = domain_resp.json().get("domains", [])
                    domain_names = [d.get("name") for d in domains]
                    
                    if DOMAIN not in domain_names:
                        print(f"[6] Adding domain...")
                        add_resp = client.post(domain_url, headers=headers, json={"name": DOMAIN}, timeout=30)
                        if add_resp.status_code in [200, 201]:
                            print(f"[6] ✅ Domain added!")
                            results.append(f"✅ **Domain added:** {DOMAIN}\n")
                    
                    # Update DNS
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
                            print(f"[7] Updating Cloudflare DNS...")
                            try:
                                sys.path.insert(0, str(Path(__file__).parent))
                                from infra.providers.cloudflare_client import CloudflareClient
                                cloudflare = CloudflareClient({}, env="prod", dry_run=False)
                                cloudflare.api_token = os.environ["CLOUDFLARE_API_TOKEN"]
                                result = cloudflare.update_root_domain_to_vercel(DOMAIN, vercel_ip, vercel_cname)
                                if result.get("updated") or result.get("created"):
                                    print(f"[7] ✅ DNS updated!")
                                    results.append(f"✅ **DNS updated:** {result.get('message')}\n")
                            except Exception as e:
                                print(f"[7] ⚠️ DNS error: {e}")
                                results.append(f"⚠️ DNS update error: {e}\n")
        
        print(f"\n✅ Complete! Check BUILD_STATUS_REPORT.md for full details")
        
        # Write file
        report_file = Path("BUILD_STATUS_REPORT.md")
        report_file.write_text("".join(results), encoding='utf-8')
        print(f"Report written to: {report_file}")
        
except Exception as e:
    error_msg = f"ERROR: {e}\n"
    print(error_msg)
    results.append(f"\n## ❌ Error\n\n{error_msg}\n")
    import traceback
    results.append(f"```\n{traceback.format_exc()}\n```\n")
    Path("BUILD_STATUS_REPORT.md").write_text("".join(results), encoding='utf-8')

print("\n" + "="*70 + "\n")
