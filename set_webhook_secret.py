#!/usr/bin/env python3
"""Set STRIPE_WEBHOOK_SECRET in Render."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import httpx
from dotenv import load_dotenv

load_dotenv()

webhook_secret = "whsec_neaU7l9K41hcPm8I0b2KDNOwLJcu3NHx"
render_api_key = os.environ.get("RENDER_API_KEY")
render_service_id = "srv-d4kcjnali9vc73dm82v0"

if not render_api_key:
    print("❌ RENDER_API_KEY not set")
    sys.exit(1)

print(f"🔧 Setting STRIPE_WEBHOOK_SECRET in Render...")

url = f"https://api.render.com/v1/services/{render_service_id}/env-vars"
headers = {
    "Authorization": f"Bearer {render_api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

try:
    # Get existing env vars
    with httpx.Client() as client:
        response = client.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Handle both list and dict responses
        if isinstance(data, list):
            env_vars = data
        else:
            env_vars = data.get("envVars", [])
        
        # Check if already exists
        existing_var = None
        for var in env_vars:
            if isinstance(var, dict) and var.get("key") == "STRIPE_WEBHOOK_SECRET":
                existing_var = var
                break
        
        if existing_var:
            # Update existing
            var_id = existing_var.get("id")
            patch_url = f"{url}/{var_id}"
            payload = {"value": webhook_secret}
            
            update_response = client.patch(patch_url, headers=headers, json=payload, timeout=30)
            update_response.raise_for_status()
            print("✅ Updated STRIPE_WEBHOOK_SECRET in Render")
        else:
            # Create new
            payload = {
                "key": "STRIPE_WEBHOOK_SECRET",
                "value": webhook_secret
            }
            
            create_response = client.post(url, headers=headers, json=payload, timeout=30)
            create_response.raise_for_status()
            print("✅ Created STRIPE_WEBHOOK_SECRET in Render")
        
        print("\n✅ Webhook secret is now set in Render!")
        print("   Render will automatically redeploy with the new secret.")
        
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

