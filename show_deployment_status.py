#!/usr/bin/env python3
"""Show deployment status and build logs."""

import httpx
import sys

# Force UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TOKEN = "n6QnE86DsiIcQXIdQp0SA34P"
PROJECT = "achillies"
DOMAIN = "corporatecrashouttrading.com"
headers = {"Authorization": f"Bearer {TOKEN}"}

print("\n" + "="*70)
print("CORPORATE CRASHOUT - DEPLOYMENT STATUS & BUILD LOGS")
print("="*70 + "\n")

try:
    # 1. Get project info
    print("[1] Checking project configuration...")
    project_resp = httpx.get(f"https://api.vercel.com/v9/projects/{PROJECT}", headers=headers, timeout=30)
    if project_resp.status_code == 200:
        project = project_resp.json()
        root_dir = project.get("rootDirectory")
        print(f"   Project: {project.get('name')}")
        print(f"   Root Directory: {root_dir or 'NOT SET'}")
        
        # Fix if wrong
        if root_dir != "apps/corporate-crashout":
            print(f"   ⚠️  Fixing root directory...")
            fix_resp = httpx.patch(
                f"https://api.vercel.com/v9/projects/{PROJECT}",
                headers=headers,
                json={"rootDirectory": "apps/corporate-crashout"},
                timeout=30
            )
            if fix_resp.status_code == 200:
                print(f"   ✅ FIXED! Root directory set to: apps/corporate-crashout")
            else:
                print(f"   ❌ Fix failed: {fix_resp.status_code}")
        else:
            print(f"   ✅ Root directory is correct")
    
    # 2. Get deployments
    print("\n[2] Checking deployments...")
    deploy_resp = httpx.get(f"https://api.vercel.com/v6/deployments?projectId={PROJECT}&limit=3", headers=headers, timeout=30)
    
    if deploy_resp.status_code == 200:
        data = deploy_resp.json()
        deployments = data.get("deployments", [])
        
        if not deployments:
            print("   ❌ NO DEPLOYMENTS FOUND")
            print("   → Code may not be pushed to GitHub")
            print("   → Vercel project may not be connected to GitHub repo")
        else:
            latest = deployments[0]
            deploy_id = latest.get("uid")
            state = latest.get("state")
            target = latest.get("target")
            url = latest.get("url", "")
            
            print(f"   ✅ Found {len(deployments)} deployment(s)")
            print(f"   Latest Deployment:")
            print(f"     ID: {deploy_id}")
            print(f"     State: {state}")
            print(f"     Target: {target or 'preview'}")
            print(f"     URL: https://{url}\n" if url else "     URL: N/A\n")
            
            # Promote if needed
            if state == "READY" and target != "production":
                print("   ⚠️  Promoting to production...")
                promote_resp = httpx.post(
                    f"https://api.vercel.com/v13/deployments/{deploy_id}/promote",
                    headers=headers,
                    timeout=30
                )
                if promote_resp.status_code in [200, 201]:
                    print("   ✅ Promoted to production!")
                else:
                    print(f"   ⚠️  Promote failed: {promote_resp.status_code}")
            
            # Get build logs
            print(f"\n[3] Getting build logs...")
            logs_resp = httpx.get(f"https://api.vercel.com/v2/deployments/{deploy_id}/events", headers=headers, timeout=30)
            
            if logs_resp.status_code == 200:
                events = logs_resp.json()
                logs = []
                for event in events:
                    payload = event.get("payload", {})
                    text = payload.get("text", "")
                    if text:
                        logs.append(text)
                
                errors = [l for l in logs if "error" in l.lower() or "failed" in l.lower() or "❌" in l or "Error:" in l]
                
                print(f"   Retrieved {len(logs)} log entries")
                print(f"   Found {len(errors)} error(s)\n")
                
                if errors:
                    print("   ❌ ERRORS FOUND:")
                    print("   " + "-"*66)
                    for err in errors[:20]:
                        clean_err = err.replace("\n", " ").strip()[:250]
                        if clean_err:
                            print(f"   • {clean_err}")
                    print()
                
                print("   Recent Build Output (last 25 lines):")
                print("   " + "-"*66)
                for log in logs[-25:]:
                    clean = log.replace("\n", " ").strip()[:180]
                    if clean:
                        print(f"   {clean}")
    
    # 3. Check domain
    print(f"\n[4] Checking domain configuration...")
    domain_resp = httpx.get(f"https://api.vercel.com/v9/projects/{PROJECT}/domains", headers=headers, timeout=30)
    
    if domain_resp.status_code == 200:
        domains = domain_resp.json().get("domains", [])
        domain_names = [d.get("name") for d in domains]
        
        if DOMAIN not in domain_names:
            print(f"   Adding domain: {DOMAIN}...")
            add_resp = httpx.post(
                f"https://api.vercel.com/v9/projects/{PROJECT}/domains",
                headers=headers,
                json={"name": DOMAIN},
                timeout=30
            )
            if add_resp.status_code in [200, 201]:
                print(f"   ✅ Domain added!")
            else:
                print(f"   ⚠️  Add failed: {add_resp.status_code} - {add_resp.text[:100]}")
        else:
            print(f"   ✅ Domain already added: {DOMAIN}")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if state == "READY":
        print("✅ Deployment is READY")
        if target == "production":
            print("✅ Set to PRODUCTION")
            print("\nSite should be accessible at:")
            print(f"  https://corporatecrashouttrading.com")
            print(f"  https://{url}")
        else:
            print("⚠️  May need to promote to production")
    elif state == "ERROR":
        print("❌ Deployment FAILED")
        print("\n⚠️  Review errors above and fix code issues")
        print("Then push to GitHub - Vercel will redeploy automatically")
    elif state == "BUILDING":
        print("⏳ Deployment is BUILDING")
        print("\nWait for build to complete...")
    
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
