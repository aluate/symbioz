#!/usr/bin/env python3
"""Get deployment status and fix issues."""

import os
import sys
import httpx
import json
from pathlib import Path

os.environ["VERCEL_TOKEN"] = "n6QnE86DsiIcQXIdQp0SA34P"
os.environ["CLOUDFLARE_API_TOKEN"] = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"

PROJECT = "achillies"
DOMAIN = "corporatecrashouttrading.com"
TOKEN = os.environ["VERCEL_TOKEN"]

# Force UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {"Authorization": f"Bearer {TOKEN}"}
output_lines = []

output_lines.append("=" * 70)
output_lines.append("DEPLOYMENT STATUS CHECK")
output_lines.append("=" * 70)
output_lines.append("")

try:
    # 1. Check project and root directory
    output_lines.append("[1] Checking project configuration...")
    project_url = f"https://api.vercel.com/v9/projects/{PROJECT}"
    with httpx.Client() as client:
        resp = client.get(project_url, headers=headers, timeout=30)
        if resp.status_code == 200:
            project = resp.json()
            root_dir = project.get("rootDirectory")
            output_lines.append(f"   Project: {project.get('name')}")
            output_lines.append(f"   Root Directory: {root_dir or 'NOT SET'}")
            
            # Fix root directory
            if root_dir != "apps/corporate-crashout":
                output_lines.append(f"   ⚠️  Root directory is wrong! Fixing...")
                fix_resp = client.patch(project_url, headers=headers, json={"rootDirectory": "apps/corporate-crashout"}, timeout=30)
                if fix_resp.status_code == 200:
                    output_lines.append(f"   ✅ FIXED! Root directory set to: apps/corporate-crashout")
                else:
                    output_lines.append(f"   ❌ Fix failed: {fix_resp.status_code}")
            else:
                output_lines.append(f"   ✅ Root directory is correct")
        
        # 2. Get deployments
        output_lines.append("")
        output_lines.append("[2] Checking deployments...")
        deploy_url = f"https://api.vercel.com/v6/deployments?projectId={PROJECT}&limit=3"
        resp = client.get(deploy_url, headers=headers, timeout=30)
        
        if resp.status_code == 200:
            data = resp.json()
            deployments = data.get("deployments", [])
            
            if not deployments:
                output_lines.append("   ❌ NO DEPLOYMENTS FOUND")
                output_lines.append("   → Code may not be pushed to GitHub")
                output_lines.append("   → Vercel project may not be connected to GitHub repo")
            else:
                latest = deployments[0]
                deploy_id = latest.get("uid")
                state = latest.get("state")
                target = latest.get("target")
                url = latest.get("url", "")
                
                output_lines.append(f"   ✅ Found {len(deployments)} deployment(s)")
                output_lines.append(f"   Latest: {deploy_id[:20]}...")
                output_lines.append(f"   State: {state}")
                output_lines.append(f"   Target: {target or 'preview'}")
                output_lines.append(f"   URL: https://{url}" if url else "   URL: N/A")
                
                # Promote if needed
                if state == "READY" and target != "production":
                    output_lines.append("")
                    output_lines.append("   ⚠️  Promoting to production...")
                    promote_url = f"https://api.vercel.com/v13/deployments/{deploy_id}/promote"
                    promote_resp = client.post(promote_url, headers=headers, timeout=30)
                    if promote_resp.status_code in [200, 201]:
                        output_lines.append("   ✅ Promoted to production!")
                    else:
                        output_lines.append(f"   ⚠️  Promote failed: {promote_resp.status_code}")
                
                # Get logs if error
                if state == "ERROR":
                    output_lines.append("")
                    output_lines.append("[3] Getting error logs...")
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
                        
                        errors = [l for l in logs if "error" in l.lower() or "failed" in l.lower() or "❌" in l]
                        
                        output_lines.append(f"   Found {len(errors)} error(s) in {len(logs)} log entries")
                        output_lines.append("")
                        output_lines.append("   ERRORS:")
                        output_lines.append("   " + "-" * 66)
                        for err in errors[:15]:
                            clean_err = err.replace("\n", " ")[:250].strip()
                            if clean_err:
                                output_lines.append(f"   ❌ {clean_err}")
                        
                        output_lines.append("")
                        output_lines.append("   Recent Build Output:")
                        output_lines.append("   " + "-" * 66)
                        for log in logs[-20:]:
                            clean = log.replace("\n", " ")[:180].strip()
                            if clean:
                                output_lines.append(f"   {clean}")
        
        # 3. Domain & DNS
        output_lines.append("")
        output_lines.append("[4] Checking domain and DNS...")
        domain_url = f"https://api.vercel.com/v9/projects/{PROJECT}/domains"
        domain_resp = client.get(domain_url, headers=headers, timeout=30)
        
        if domain_resp.status_code == 200:
            domains = domain_resp.json().get("domains", [])
            domain_names = [d.get("name") for d in domains]
            
            if DOMAIN not in domain_names:
                output_lines.append(f"   Adding domain: {DOMAIN}...")
                add_resp = client.post(domain_url, headers=headers, json={"name": DOMAIN}, timeout=30)
                if add_resp.status_code in [200, 201]:
                    output_lines.append(f"   ✅ Domain added!")
                else:
                    output_lines.append(f"   ⚠️  Add failed: {add_resp.status_code}")
            else:
                output_lines.append(f"   ✅ Domain already added: {DOMAIN}")
            
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
                    output_lines.append(f"   Vercel DNS: {vercel_ip or vercel_cname}")
                    output_lines.append(f"   Updating Cloudflare DNS...")
                    
                    try:
                        sys.path.insert(0, str(Path(__file__).parent))
                        from infra.providers.cloudflare_client import CloudflareClient
                        cloudflare = CloudflareClient({}, env="prod", dry_run=False)
                        cloudflare.api_token = os.environ["CLOUDFLARE_API_TOKEN"]
                        result = cloudflare.update_root_domain_to_vercel(DOMAIN, vercel_ip, vercel_cname)
                        if result.get("updated") or result.get("created"):
                            output_lines.append(f"   ✅ DNS Updated: {result.get('message')}")
                        else:
                            output_lines.append(f"   ⚠️  DNS update may have failed")
                    except Exception as e:
                        output_lines.append(f"   ⚠️  DNS error: {str(e)[:150]}")
    
    # Summary
    output_lines.append("")
    output_lines.append("=" * 70)
    output_lines.append("SUMMARY")
    output_lines.append("=" * 70)
    
    if state == "READY":
        output_lines.append("✅ Deployment is READY")
        if target == "production":
            output_lines.append("✅ Set to PRODUCTION")
        else:
            output_lines.append("⚠️  May need to promote to production")
    elif state == "ERROR":
        output_lines.append("❌ Deployment FAILED - Review errors above")
    elif state == "BUILDING":
        output_lines.append("⏳ Deployment is BUILDING")
    
    output_lines.append("")
    output_lines.append("=" * 70)

except Exception as e:
    output_lines.append(f"\n❌ ERROR: {e}")
    import traceback
    output_lines.append("\n" + traceback.format_exc())

# Print and write to file
output_text = "\n".join(output_lines)
print(output_text)

# Write to file
report_file = Path("BUILD_STATUS_REPORT.md")
report_file.write_text(output_text, encoding='utf-8')
print(f"\n✅ Full report saved to: {report_file}")
