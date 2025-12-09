#!/usr/bin/env python3
"""Direct build check with explicit output."""

import httpx
import sys

VERCEL_TOKEN = "n6QnE86DsiIcQXIdQp0SA34P"
PROJECT = "achillies"

headers = {"Authorization": f"Bearer {VERCEL_TOKEN}"}

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("\n" + "="*70)
print("BUILD STATUS CHECK")
print("="*70 + "\n")

# Get deployments
url = f"https://api.vercel.com/v6/deployments?projectId={PROJECT}&limit=3"
try:
    with httpx.Client() as client:
        resp = client.get(url, headers=headers, timeout=30)
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            deployments = data.get("deployments", [])
            print(f"Found {len(deployments)} deployments\n")
            
            if deployments:
                latest = deployments[0]
                deploy_id = latest.get("uid")
                state = latest.get("state")
                target = latest.get("target")
                url_preview = latest.get("url", "")
                
                print(f"Latest Deployment:")
                print(f"  ID: {deploy_id}")
                print(f"  State: {state}")
                print(f"  Target: {target or 'preview'}")
                print(f"  URL: {url_preview}")
                
                # Get logs
                if state == "ERROR":
                    print(f"\nGetting error logs...")
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
                        
                        print(f"\nERROR LOGS ({len(logs)} entries):")
                        print("-"*70)
                        for log in logs[-30:]:
                            print(f"  {log[:200]}")
            else:
                print("No deployments found!")
        else:
            print(f"Error: {resp.status_code}")
            print(resp.text[:500])
            
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70 + "\n")
