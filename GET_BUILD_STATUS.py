#!/usr/bin/env python3
"""Get build status and write to file."""

import os
import httpx
from pathlib import Path

VERCEL_TOKEN = "n6QnE86DsiIcQXIdQp0SA34P"
PROJECT = "achillies"
DOMAIN = "corporatecrashouttrading.com"

headers = {"Authorization": f"Bearer {VERCEL_TOKEN}"}
output_file = Path("BUILD_STATUS_REPORT.md")

results = []
results.append("# 🔍 Build Status Report - Corporate Crashout")
results.append("\n" + "="*70 + "\n")

try:
    # Get project
    results.append("## [1] Project Configuration\n")
    project_url = f"https://api.vercel.com/v9/projects/{PROJECT}"
    with httpx.Client() as client:
        resp = client.get(project_url, headers=headers, timeout=30)
        if resp.status_code == 200:
            project = resp.json()
            root_dir = project.get("rootDirectory")
            results.append(f"✅ Project: {project.get('name')}")
            results.append(f"\nRoot Directory: `{root_dir or 'NOT SET ❌'}`")
            
            if root_dir != "apps/corporate-crashout":
                results.append(f"\n⚠️ **ROOT DIRECTORY IS WRONG!**")
                results.append(f"\nFixing now...")
                
                # Fix it
                update_resp = client.patch(project_url, headers=headers, json={"rootDirectory": "apps/corporate-crashout"}, timeout=30)
                if update_resp.status_code == 200:
                    results.append(f"\n✅ **FIXED!** Root directory set to: `apps/corporate-crashout`")
                else:
                    results.append(f"\n❌ Failed to fix: {update_resp.status_code}")
        else:
            results.append(f"❌ Error: {resp.status_code}")
            results.append(f"\nResponse: {resp.text[:300]}")
    
    # Get deployments
    results.append("\n\n## [2] Deployment Status\n")
    deploy_url = f"https://api.vercel.com/v6/deployments?projectId={PROJECT}&limit=5"
    with httpx.Client() as client:
        resp = client.get(deploy_url, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            deployments = data.get("deployments", [])
            
            if not deployments:
                results.append("❌ **No deployments found!**")
                results.append("\n**This means:**")
                results.append("- Code may not be pushed to GitHub")
                results.append("- Vercel project not connected to GitHub repo")
            else:
                results.append(f"Found {len(deployments)} deployment(s)\n")
                
                latest = deployments[0]
                deploy_id = latest.get("uid")
                state = latest.get("state")
                target = latest.get("target")
                url = latest.get("url", "")
                
                results.append(f"### Latest Deployment")
                results.append(f"- **ID:** `{deploy_id}`")
                results.append(f"- **State:** `{state}`")
                results.append(f"- **Target:** `{target or 'preview'}`")
                results.append(f"- **URL:** https://{url}\n" if url else "- **URL:** N/A\n")
                
                # Promote if needed
                if state == "READY" and target != "production":
                    results.append("\n⚠️ **Deployment is PREVIEW, not PRODUCTION**")
                    results.append("\nPromoting to production...")
                    promote_url = f"https://api.vercel.com/v13/deployments/{deploy_id}/promote"
                    promote_resp = client.post(promote_url, headers=headers, timeout=30)
                    if promote_resp.status_code in [200, 201]:
                        results.append("✅ **Promoted to production!**")
                    else:
                        results.append(f"⚠️ Could not promote: {promote_resp.status_code}")
                
                # Get logs
                if state == "ERROR":
                    results.append("\n### ❌ BUILD FAILED - Error Logs\n")
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
                            results.append(f"Found {len(errors)} error(s) in {len(logs)} log entries\n")
                            
                            if errors:
                                results.append("**Errors:**")
                                for err in errors[:15]:
                                    results.append(f"```\n{err[:300]}\n```")
                            
                            results.append("\n**Recent Build Output (last 30 lines):**")
                            results.append("```")
                            for log in logs[-30:]:
                                clean = log.replace("\n", " ")[:150].strip()
                                if clean:
                                    results.append(clean)
                            results.append("```")
                elif state == "BUILDING":
                    results.append("\n⏳ **Deployment is still BUILDING...**")
                elif state == "READY":
                    results.append("\n✅ **Deployment is READY!**")
    
    # Check domain
    results.append("\n\n## [3] Domain Configuration\n")
    domain_url = f"https://api.vercel.com/v9/projects/{PROJECT}/domains"
    with httpx.Client() as client:
        resp = client.get(domain_url, headers=headers, timeout=30)
        if resp.status_code == 200:
            domains = resp.json().get("domains", [])
            domain_names = [d.get("name") for d in domains]
            
            if DOMAIN not in domain_names:
                results.append(f"⚠️ Domain not added. Adding now...")
                add_resp = client.post(domain_url, headers=headers, json={"name": DOMAIN}, timeout=30)
                if add_resp.status_code in [200, 201]:
                    results.append(f"✅ **Domain added:** `{DOMAIN}`")
                else:
                    results.append(f"⚠️ Add failed: {add_resp.status_code}")
            else:
                results.append(f"✅ Domain already added: `{DOMAIN}`")
            
            # Get DNS and update Cloudflare
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
                    results.append(f"\n**Vercel DNS:** {vercel_ip or vercel_cname}")
                    results.append(f"\nUpdating Cloudflare DNS...")
                    
                    try:
                        import sys
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
                            results.append(f"✅ **DNS Updated:** {result.get('message')}")
                        else:
                            results.append(f"⚠️ DNS update may have failed")
                    except Exception as e:
                        results.append(f"⚠️ DNS update error: {str(e)[:200]}")
    
    # Summary
    results.append("\n\n## 📊 Summary\n")
    results.append("="*70)
    
    if state == "READY":
        if target == "production":
            results.append("\n✅ **Deployment is READY and PRODUCTION**")
        else:
            results.append("\n✅ **Deployment is READY** (check if promoted to production)")
    elif state == "ERROR":
        results.append("\n❌ **Deployment FAILED** - Review errors above")
    elif state == "BUILDING":
        results.append("\n⏳ **Deployment is BUILDING** - Wait for completion")
    
    results.append("\n" + "="*70)
    
except Exception as e:
    results.append(f"\n\n❌ **ERROR:** {e}")
    import traceback
    results.append(f"\n```\n{traceback.format_exc()}\n```")

# Write to file
output_file.write_text("\n".join(results), encoding='utf-8')
print(f"\n✅ Report written to: {output_file}")
print(f"Read the file to see full status and any errors!")
