#!/usr/bin/env python3
"""Watch Vercel deployment status in real-time."""

import os
import time
from dotenv import load_dotenv
from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs
from datetime import datetime

load_dotenv()

configs = load_provider_configs()
client = VercelClient(configs['vercel'], env='prod')

def get_latest_deployment():
    """Get the most recent deployment."""
    deployments = client._list_deployments('catered-by-me', limit=1)
    if deployments:
        return deployments[0]
    return None

def format_time(timestamp):
    """Format timestamp to readable time."""
    if not timestamp:
        return "Unknown"
    dt = datetime.fromtimestamp(timestamp / 1000)
    return dt.strftime("%H:%M:%S")

def get_status_emoji(state):
    """Get emoji for deployment state."""
    state = state or "UNKNOWN"
    if state == 'READY':
        return "✅"
    elif state == 'BUILDING':
        return "🔨"
    elif state == 'ERROR':
        return "❌"
    elif state == 'QUEUED':
        return "⏳"
    else:
        return "⚠️"

print("=" * 60)
print("Watching Vercel Deployment...")
print("Press Ctrl+C to stop")
print("=" * 60)
print()

last_deployment_id = None

try:
    while True:
        deployment = get_latest_deployment()
        
        if deployment:
            uid = deployment.get('uid', 'N/A')
            state = deployment.get('state', 'UNKNOWN')
            ready_state = deployment.get('readyState', 'UNKNOWN')
            created_at = deployment.get('createdAt', 0)
            url = deployment.get('url', 'N/A')
            
            # Only print if deployment changed
            if uid != last_deployment_id:
                print(f"\n[{format_time(created_at)}] New Deployment Detected!")
                print(f"  ID: {uid}")
                print(f"  URL: {url}")
                last_deployment_id = uid
            
            # Status
            emoji = get_status_emoji(state or ready_state)
            status = state or ready_state or "UNKNOWN"
            
            # Print status update
            status_line = f"[{format_time(time.time() * 1000)}] {emoji} {status}"
            
            # Clear line and print status
            print(f"\r{status_line}", end="", flush=True)
            
            # If ready or error, stop watching
            if status in ['READY', 'ERROR']:
                print("\n")
                if status == 'READY':
                    print("🎉 Deployment successful!")
                    print(f"   Live at: https://{url}")
                else:
                    print("❌ Deployment failed. Check logs:")
                    print(f"   https://vercel.com/aluates-projects/catered-by-me/{uid}")
                break
        
        time.sleep(5)  # Check every 5 seconds
        
except KeyboardInterrupt:
    print("\n\nMonitoring stopped.")

