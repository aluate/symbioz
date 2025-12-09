#!/usr/bin/env python3
"""Fetch build logs and write to file."""

import httpx
import json
from pathlib import Path

TOKEN = "n6QnE86DsiIcQXIdQp0SA34P"
PROJECT = "achillies"
headers = {"Authorization": f"Bearer {TOKEN}"}

output = []
output.append("="*70)
output.append("BUILD LOGS & DEPLOYMENT STATUS")
output.append("="*70)
output.append("")

try:
    # Get deployments
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
            
            output.append(f"Deployment ID: {deploy_id}")
            output.append(f"State: {state}")
            output.append(f"Target: {target or 'preview'}")
            output.append(f"URL: https://{url}" if url else "URL: N/A")
            output.append("")
            
            # Get logs
            logs_resp = httpx.get(f"https://api.vercel.com/v2/deployments/{deploy_id}/events", headers=headers, timeout=30)
            
            if logs_resp.status_code == 200:
                events = logs_resp.json()
                logs = []
                for event in events:
                    payload = event.get("payload", {})
                    text = payload.get("text", "")
                    if text:
                        logs.append(text)
                
                errors = [l for l in logs if "error" in l.lower() or "failed" in l.lower() or "❌" in l]
                
                output.append(f"Total log entries: {len(logs)}")
                output.append(f"Errors found: {len(errors)}")
                output.append("")
                
                if errors:
                    output.append("ERRORS:")
                    output.append("-"*70)
                    for err in errors[:20]:
                        output.append(err[:300])
                    output.append("")
                
                output.append("RECENT LOGS (last 30):")
                output.append("-"*70)
                for log in logs[-30:]:
                    clean = log.replace("\n", " ").strip()[:200]
                    if clean:
                        output.append(clean)
        else:
            output.append("❌ NO DEPLOYMENTS FOUND")
            output.append("Code may not be pushed to GitHub")

except Exception as e:
    output.append(f"ERROR: {e}")
    import traceback
    output.append(traceback.format_exc())

# Write to file
report = "\n".join(output)
Path("BUILD_LOGS.txt").write_text(report, encoding='utf-8')
print(report)
print("\n" + "="*70)
print("Full report saved to: BUILD_LOGS.txt")
