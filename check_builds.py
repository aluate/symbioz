#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import httpx
import sys

TOKEN = "n6QnE86DsiIcQXIdQp0SA34P"
PROJECT = "achillies"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Force output encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("\n" + "="*70)
print("DEPLOYMENT STATUS")
print("="*70)

try:
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
            
            print(f"\nDeployment ID: {deploy_id}")
            print(f"State: {state}")
            print(f"Target: {target or 'preview'}")
            print(f"URL: https://{url}\n" if url else "URL: N/A\n")
            
            # Get logs
            logs_resp = httpx.get(f"https://api.vercel.com/v2/deployments/{deploy_id}/events", headers=headers, timeout=30)
            if logs_resp.status_code == 200:
                events = logs_resp.json()
                logs = [e.get("payload", {}).get("text", "") for e in events if e.get("payload", {}).get("text")]
                errors = [l for l in logs if "error" in l.lower() or "failed" in l.lower()]
                
                print(f"Logs: {len(logs)}, Errors: {len(errors)}\n")
                
                if errors:
                    print("ERRORS:")
                    for err in errors[:10]:
                        print(f"  {err[:200]}")
                    print()
                
                print("Recent logs:")
                for log in logs[-15:]:
                    clean = log.replace("\n", " ").strip()[:150]
                    if clean:
                        print(f"  {clean}")
        else:
            print("\nNo deployments found")
    else:
        print(f"\nAPI Error: {resp.status_code}")

except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
