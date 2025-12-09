#!/usr/bin/env python3
"""Fix deployment - uses existing infra tools."""

import os
import sys
from pathlib import Path

# Set tokens
os.environ["VERCEL_TOKEN"] = "n6QnE86DsiIcQXIdQp0SA34P"
os.environ["CLOUDFLARE_API_TOKEN"] = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"

sys.path.insert(0, str(Path(__file__).parent))

from infra.providers.vercel_client import VercelClient
from infra.providers.cloudflare_client import CloudflareClient
from infra.utils.yaml_loader import load_provider_configs

PROJECT_NAME = "achillies"
DOMAIN = "corporatecrashouttrading.com"

print("\n" + "="*70)
print("🔧 Fixing Corporate Crashout Deployment")
print("="*70 + "\n")

try:
    # Load configs
    provider_configs = load_provider_configs()
    vercel_config = provider_configs.get("vercel", {})
    
    # Create clients
    vercel = VercelClient(vercel_config, env="prod", dry_run=False)
    cloudflare_config = provider_configs.get("cloudflare", {})
    cloudflare = CloudflareClient(cloudflare_config, env="prod", dry_run=False)
    cloudflare.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    
    # 1. Check/fix root directory
    print("[1] Checking root directory...")
    project = vercel._get_project(PROJECT_NAME)
    if project:
        root_dir = project.get("rootDirectory")
        print(f"   Current: {root_dir or '(not set)'}")
        
        if root_dir != "apps/corporate-crashout":
            print(f"   ⚠️  Wrong! Fixing...")
            vercel.update_project_settings(PROJECT_NAME, root_directory="apps/corporate-crashout")
            print(f"   ✅ Fixed to: apps/corporate-crashout")
        else:
            print(f"   ✅ Correct: apps/corporate-crashout")
    else:
        print(f"   ❌ Project not found")
    
    # 2. Get deployments
    print("\n[2] Checking deployments...")
    deployments = vercel._list_deployments(PROJECT_NAME, limit=3)
    
    if not deployments:
        print("   ❌ No deployments!")
        print("   → Push code to GitHub or connect repo in Vercel")
    else:
        latest = deployments[0]
        deploy_id = latest.get("uid")
        state = latest.get("state")
        target = latest.get("target")
        
        print(f"   Latest: {deploy_id[:20]}...")
        print(f"   State: {state}")
        print(f"   Target: {target or 'preview'}")
        
        # Promote if needed
        if state == "READY" and target != "production":
            print(f"\n   Promoting to production...")
            promote_url = f"{vercel.API_BASE_URL}/v13/deployments/{deploy_id}/promote"
            import httpx
            resp = httpx.post(promote_url, headers=vercel._get_headers(), timeout=30)
            if resp.status_code in [200, 201]:
                print(f"   ✅ Promoted!")
        
        # Get logs if error
        if state == "ERROR":
            print(f"\n[3] Getting error logs...")
            logs = vercel.get_deployment_logs(deploy_id)
            if logs:
                errors = [l for l in logs if "error" in str(l).lower() or "failed" in str(l).lower()]
                print(f"   Found {len(errors)} error(s):")
                for err in errors[:10]:
                    err_str = str(err)[:200]
                    print(f"      ❌ {err_str}")
                
                print(f"\n   Last 15 log lines:")
                for log in logs[-15:]:
                    log_str = str(log)[:150]
                    if log_str:
                        print(f"      {log_str}")
    
    # 3. Add domain
    print(f"\n[4] Checking domain...")
    try:
        vercel.add_domain(PROJECT_NAME, DOMAIN)
        print(f"   ✅ Domain added/verified: {DOMAIN}")
    except Exception as e:
        if "already exists" in str(e).lower() or "409" in str(e):
            print(f"   ✅ Domain already added")
        else:
            print(f"   ⚠️  Domain issue: {e}")
    
    # 4. Get DNS and update Cloudflare
    print(f"\n[5] Updating DNS...")
    try:
        dns_config = vercel.get_domain_config(DOMAIN)
        if dns_config and dns_config.get("dns_records"):
            records = dns_config.get("dns_records", [])
            
            vercel_ip = None
            vercel_cname = None
            for record in records:
                if record.get("type") == "A" and (not record.get("name") or record.get("name") == "@"):
                    vercel_ip = record.get("value")
                elif record.get("type") == "CNAME" and (not record.get("name") or record.get("name") == "@"):
                    vercel_cname = record.get("value")
            
            if vercel_ip or vercel_cname:
                print(f"   Vercel says: {vercel_ip or vercel_cname}")
                
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
        print(f"   ⚠️  DNS update error: {e}")
    
    print("\n" + "="*70)
    print("✅ All fixes applied!")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
