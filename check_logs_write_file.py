#!/usr/bin/env python3
"""Check build logs and write to file."""

import httpx
import json
from pathlib import Path

TOKEN = "n6QnE86DsiIcQXIdQp0SA34P"
PROJECT = "achillies"
headers = {"Authorization": f"Bearer {TOKEN}"}

report = []

report.append("# Build Status Report\n")
report.append("="*70 + "\n\n")

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
            
            report.append(f"## Deployment Status\n\n")
            report.append(f"- **State:** {state}\n")
            report.append(f"- **Target:** {target or 'preview'}\n")
            report.append(f"- **URL:** https://{url}\n")
            report.append(f"- **ID:** {deploy_id}\n\n")
            
            # Get logs
            if deploy_id:
                logs_resp = httpx.get(f"https://api.vercel.com/v2/deployments/{deploy_id}/events", headers=headers, timeout=30)
                
                if logs_resp.status_code == 200:
                    events = logs_resp.json()
                    logs = []
                    for event in events:
                        payload = event.get("payload", {})
                        text = payload.get("text", "")
                        if text:
                            logs.append(text)
                    
                    errors = [l for l in logs if "error" in l.lower() or "failed" in l.lower()]
                    
                    report.append(f"## Build Logs\n\n")
                    report.append(f"Total log entries: {len(logs)}\n")
                    report.append(f"Errors found: {len(errors)}\n\n")
                    
                    if errors:
                        report.append("### ❌ Errors:\n\n```\n")
                        for err in errors[:20]:
                            report.append(err[:300] + "\n")
                        report.append("```\n\n")
                    
                    report.append("### Recent Logs (last 30):\n\n```\n")
                    for log in logs[-30:]:
                        clean = log.replace("\n", " ").strip()[:200]
                        if clean:
                            report.append(clean + "\n")
                    report.append("```\n")
        else:
            report.append("## ❌ No Deployments Found\n\n")
            report.append("Code may not be pushed to GitHub.\n")
    
    # Write file
    Path("BUILD_LOGS_REPORT.md").write_text("".join(report), encoding='utf-8')
    print("Report written to BUILD_LOGS_REPORT.md")
    
except Exception as e:
    error_report = f"# Error\n\n{str(e)}\n\n```\n{repr(e)}\n```"
    Path("BUILD_LOGS_REPORT.md").write_text(error_report, encoding='utf-8')
    print(f"Error: {e}")
