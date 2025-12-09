#!/usr/bin/env python3
"""Check if Stripe setup is complete."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import httpx
from dotenv import load_dotenv

load_dotenv()

print("🔍 Checking Stripe Setup...\n")

# Check environment variables
print("1. Checking .env file...")
env_file = Path(".env")
if env_file.exists():
    content = env_file.read_text(encoding="utf-8")
    has_secret = "STRIPE_SECRET_KEY=" in content
    has_publishable = "STRIPE_PUBLISHABLE_KEY=" in content
    print(f"   ✅ STRIPE_SECRET_KEY: {'✅ Set' if has_secret else '❌ Missing'}")
    print(f"   ✅ STRIPE_PUBLISHABLE_KEY: {'✅ Set' if has_publishable else '❌ Missing'}")
else:
    print("   ⚠️  .env file not found")

# Check Render env vars
print("\n2. Checking Render environment variables...")
render_api_key = os.environ.get("RENDER_API_KEY")
render_service_id = "srv-d4kcjnali9vc73dm82v0"  # From render.yaml

if render_api_key:
    try:
        url = f"https://api.render.com/v1/services/{render_service_id}/env-vars"
        headers = {
            "Authorization": f"Bearer {render_api_key}",
            "Accept": "application/json",
        }
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                # Handle both list and dict responses
                if isinstance(data, list):
                    env_vars = data
                else:
                    env_vars = data.get("envVars", [])
                env_dict = {}
                for item in env_vars:
                    if isinstance(item, dict):
                        env_dict[item.get("key", "")] = item.get("value", "[REDACTED]")
                
                has_stripe_secret = "STRIPE_SECRET_KEY" in env_dict
                has_webhook_secret = "STRIPE_WEBHOOK_SECRET" in env_dict
                
                print(f"   ✅ STRIPE_SECRET_KEY: {'✅ Set' if has_stripe_secret else '❌ Missing'}")
                print(f"   ✅ STRIPE_WEBHOOK_SECRET: {'✅ Set' if has_webhook_secret else '❌ Missing'}")
                
                if has_stripe_secret and has_webhook_secret:
                    print("\n   ✅ All Render environment variables are set!")
                elif has_stripe_secret:
                    print("\n   ⚠️  STRIPE_WEBHOOK_SECRET is missing (Step 2 not complete)")
                else:
                    print("\n   ⚠️  STRIPE_SECRET_KEY is missing (Step 1 not complete)")
            else:
                print(f"   ❌ Could not check Render: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error checking Render: {e}")
else:
    print("   ⚠️  RENDER_API_KEY not set, cannot check Render")

# Check Vercel env vars
print("\n3. Checking Vercel environment variables...")
vercel_token = os.environ.get("VERCEL_TOKEN")
vercel_project = "catered-by-me"

if vercel_token:
    try:
        url = f"https://api.vercel.com/v10/projects/{vercel_project}/env"
        headers = {
            "Authorization": f"Bearer {vercel_token}",
            "Accept": "application/json",
        }
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                env_vars = response.json().get("envs", [])
                env_dict = {item["key"]: item.get("value", "[REDACTED]") for item in env_vars if item.get("target", [])}
                
                has_stripe_publishable = "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY" in env_dict
                
                print(f"   ✅ NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: {'✅ Set' if has_stripe_publishable else '❌ Missing'}")
            else:
                print(f"   ⚠️  Could not check Vercel: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error checking Vercel: {e}")
else:
    print("   ⚠️  VERCEL_TOKEN not set, cannot check Vercel")

# Check Stripe webhook
print("\n4. Checking Stripe webhook...")
stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")

if stripe_secret_key:
    try:
        import stripe
        stripe.api_key = stripe_secret_key
        
        webhooks = stripe.WebhookEndpoint.list(limit=10)
        webhook_url = "https://catered-by-me-api.onrender.com/billing/webhook"
        
        found_webhook = None
        for webhook in webhooks.data:
            if webhook.url == webhook_url:
                found_webhook = webhook
                break
        
        if found_webhook:
            print(f"   ✅ Webhook endpoint found: {webhook_url}")
            print(f"   ✅ Status: {found_webhook.status}")
            print(f"   ✅ Events: {len(found_webhook.enabled_events)} event(s) configured")
            print("\n   ✅ Stripe webhook is set up!")
        else:
            print(f"   ❌ Webhook endpoint not found")
            print(f"   Expected URL: {webhook_url}")
            print("\n   ⚠️  Step 2 not complete - webhook needs to be created in Stripe dashboard")
    except Exception as e:
        print(f"   ⚠️  Error checking Stripe: {e}")
else:
    print("   ⚠️  STRIPE_SECRET_KEY not set, cannot check Stripe")

print("\n" + "=" * 60)
print("Summary:")
print("=" * 60)
print("Check the status above to see what's complete and what's missing.")
print("=" * 60)

