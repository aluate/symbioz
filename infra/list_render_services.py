#!/usr/bin/env python3
"""
Quick script to list all Render services and their IDs.
Uses your Render API key from .env file.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import httpx

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("RENDER_API_KEY")
if not api_key:
    print("❌ Error: RENDER_API_KEY not found in .env file")
    sys.exit(1)

print("🔍 Fetching your Render services...\n")

# Render API endpoint
url = "https://api.render.com/v1/services"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}

try:
    response = httpx.get(url, headers=headers, timeout=30.0)
    response.raise_for_status()
    
    services = response.json()
    
    if not services:
        print("No services found.")
        sys.exit(0)
    
    print(f"✅ Found {len(services)} service(s):\n")
    print("=" * 80)
    
    for service in services:
        service_id = service.get("service", {}).get("id", "N/A")
        name = service.get("service", {}).get("name", "N/A")
        service_type = service.get("service", {}).get("type", "N/A")
        repo = service.get("service", {}).get("repo", "N/A")
        branch = service.get("service", {}).get("branch", "N/A")
        
        print(f"\n📦 Service: {name}")
        print(f"   ID: {service_id}")
        print(f"   Type: {service_type}")
        print(f"   Repo: {repo}")
        print(f"   Branch: {branch}")
        
        # Highlight if it looks like the API service
        if "api" in name.lower() or "catered" in name.lower():
            print(f"   ⭐ This might be your API service!")
    
    print("\n" + "=" * 80)
    print("\n💡 Copy the service ID (starts with 'srv-') and update infra/providers/render.yaml")
    
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        print("❌ Error: Invalid API key. Check your RENDER_API_KEY in .env file.")
    elif e.response.status_code == 403:
        print("❌ Error: API key doesn't have permission to access services.")
    else:
        print(f"❌ Error: HTTP {e.response.status_code} - {e.response.text}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

