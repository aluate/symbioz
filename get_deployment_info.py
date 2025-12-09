#!/usr/bin/env python3
"""Get deployment info and print it."""

import httpx
import json

TOKEN = "n6QnE86DsiIcQXIdQp0SA34P"
PROJECT = "achillies"
headers = {"Authorization": f"Bearer {TOKEN}"}

print("\n" + "="*70)
print("DEPLOYMENT STATUS & BUILD LOGS")
print("="*70 + "\n")

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
        
        print(f"Deployment ID: {deploy_id}")
        print(f"State: {state}")
        print(f"Target: {target or 'preview'}")
        print(f"URL: https://{url}\n" if url else "URL: N/A\n")
        
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
            
            errors = [l for l in logs if "error" in l.lower() or "failed" in l.lower()]
            
            print(f"Total logs: {len(logs)}, Errors: {len(errors)}\n")
            
            if errors:
                print("ERRORS FOUND:")
                print("-"*70)
                for err in errors[:15]:
                    print(err[:250])
                print()
            
            print("RECENT LOGS (last 20):")
            print("-"*70)
            for log in logs[-20:]:
                clean = log.replace("\n", " ").strip()[:180]
                if clean:
                    print(clean)
    else:
        print("NO DEPLOYMENTS FOUND")
        print("Code may not be pushed to GitHub")
else:
    print(f"API Error: {resp.status_code}")
    print(resp.text[:300])

print("\n" + "="*70)
