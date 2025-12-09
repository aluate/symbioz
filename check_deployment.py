#!/usr/bin/env python3
"""Check Vercel deployment status."""

import os
from dotenv import load_dotenv
from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs
from datetime import datetime

load_dotenv()

configs = load_provider_configs()
client = VercelClient(configs['vercel'], env='prod')

# Get latest deployments
deployments = client._list_deployments('catered-by-me', limit=5)

print("=" * 60)
print("Latest Vercel Deployments")
print("=" * 60)

for i, dep in enumerate(deployments, 1):
    uid = dep.get('uid', 'N/A')
    state = dep.get('state', 'UNKNOWN')
    ready_state = dep.get('readyState', 'UNKNOWN')
    created_at = dep.get('createdAt', 0)
    
    # Convert timestamp to readable date
    if created_at:
        dt = datetime.fromtimestamp(created_at / 1000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        time_str = "Unknown"
    
    url = dep.get('url', 'N/A')
    
    # Status emoji
    if state == 'READY' or ready_state == 'READY':
        status = "✅ READY"
    elif state == 'BUILDING' or ready_state == 'BUILDING':
        status = "🔨 BUILDING"
    elif state == 'ERROR' or ready_state == 'ERROR':
        status = "❌ ERROR"
    elif state == 'QUEUED':
        status = "⏳ QUEUED"
    else:
        status = f"⚠️ {state}"
    
    print(f"\n{i}. {status}")
    print(f"   ID: {uid}")
    print(f"   URL: {url}")
    print(f"   Created: {time_str}")
    print(f"   State: {state} / {ready_state}")
    
    # Show commit info if available
    meta = dep.get('meta', {})
    if meta.get('githubCommitSha'):
        print(f"   Commit: {meta.get('githubCommitSha', '')[:8]}")
        print(f"   Message: {meta.get('githubCommitMessage', 'N/A')[:60]}")

print("\n" + "=" * 60)
print("Check full details at: https://vercel.com/aluates-projects/catered-by-me")
print("=" * 60)

