#!/usr/bin/env python3
"""Get deployment status and write to readable file."""

import httpx
from pathlib import Path

TOKEN = "n6QnE86DsiIcQXIdQp0SA34P"
PROJECT = "achillies"
DOMAIN = "corporatecrashouttrading.com"
headers = {"Authorization": f"Bearer {TOKEN}"}

output = []
output.append("="*70)
output.append("CORPORATE CRASHOUT - DEPLOYMENT STATUS & BUILD LOGS")
output.append("="*70)
output.append("")

try:
    # Get project
    resp = httpx.get(f"https://api.vercel.com/v9/projects/{PROJECT}", headers=headers, timeout=30)
    if resp.status_code == 200:
        project = resp.json()
        root_dir = project.get("rootDirectory")
        output.append(f"[1] Project: {project.get('name')}")
        output.append(f"    Root Directory: {root_dir or 'NOT SET'}")
        
        if root_dir != "apps/corporate-crashout":
            output.append(f"    Fixing root directory...")
            fix_resp = httpx.patch(
                f"https://api.vercel.com/v9/projects/{PROJECT}",
                headers=headers,
                json={"rootDirectory": "apps/corporate-crashout"},
                timeout=30
            )
            if fix_resp.status_code == 200:
                output.append(f"    ✅ FIXED!")
    
    # Get deployments
    output.append("")
    output.append("[2] Checking deployments...")
    resp = httpx.get(f"https://api.vercel.com/v6/deployments?projectId={PROJECT}&limit=1", headers=headers, timeout=30)
    
    if resp.status_code == 200:
        data = resp.json()
        deployments = data.get("deployments", [])
        
        if deployments:
            latest = deployments[0]
            deploy_id = latest.get("uid")
            state = latest.get("state")
            target = latest.get("target")
            url = latest.get("url", "")
            
            output.append(f"    ✅ Found deployment")
            output.append(f"    ID: {deploy_id}")
            output.append(f"    State: {state}")
            output.append(f"    Target: {target or 'preview'}")
            output.append(f"    URL: https://{url}" if url else "    URL: N/A")
            
            # Promote if needed
            if state == "READY" and target != "production":
                output.append(f"    Promoting to production...")
                promote_resp = httpx.post(
                    f"https://api.vercel.com/v13/deployments/{deploy_id}/promote",
                    headers=headers,
                    timeout=30
                )
                if promote_resp.status_code in [200, 201]:
                    output.append(f"    ✅ Promoted!")
            
            # Get logs
            output.append("")
            output.append("[3] Build logs:")
            logs_resp = httpx.get(f"https://api.vercel.com/v2/deployments/{deploy_id}/events", headers=headers, timeout=30)
            
            if logs_resp.status_code == 200:
                events = logs_resp.json()
                logs = []
                for event in events:
                    payload = event.get("payload", {})
                    text = payload.get("text", "")
                    if text:
                        logs.append(text)
                
                errors = [l for l in logs if "error" in l.lower() or "failed" in l.lower() or "Error:" in l]
                
                output.append(f"    Total logs: {len(logs)}, Errors: {len(errors)}")
                output.append("")
                
                if errors:
                    output.append("    ERRORS:")
                    for err in errors[:15]:
                        clean = err.replace("\n", " ").strip()[:250]
                        if clean:
                            output.append(f"    • {clean}")
                    output.append("")
                
                output.append("    Recent logs (last 20):")
                for log in logs[-20:]:
                    clean = log.replace("\n", " ").strip()[:180]
                    if clean:
                        output.append(f"    {clean}")
        else:
            output.append("    ❌ NO DEPLOYMENTS FOUND")
    
    # Write file
    report = "\n".join(output)
    Path("DEPLOYMENT_STATUS.txt").write_text(report, encoding='utf-8')
    print(report)
    
except Exception as e:
    error_msg = f"ERROR: {e}"
    Path("DEPLOYMENT_STATUS.txt").write_text(error_msg, encoding='utf-8')
    print(error_msg)
    import traceback
    traceback.print_exc()
