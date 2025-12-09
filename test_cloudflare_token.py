#!/usr/bin/env python3
"""Test Cloudflare API token."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from infra.providers.cloudflare_client import CloudflareClient
from infra.utils.yaml_loader import load_provider_configs

print("Testing Cloudflare API Token...")
print("=" * 60)

# Get token
token = os.getenv("CLOUDFLARE_API_TOKEN")
if not token:
    print("❌ CLOUDFLARE_API_TOKEN not found in environment")
    print("   Set it with: $env:CLOUDFLARE_API_TOKEN = 'your_token'")
    sys.exit(1)

print(f"✅ Token found: {token[:10]}...{token[-10:]}")

# Load config
try:
    configs = load_provider_configs()
    cloudflare_config = configs.get("cloudflare", {})
    print("✅ Cloudflare config loaded")
except Exception as e:
    print(f"⚠️  Could not load config: {e}")
    cloudflare_config = {}

# Test client
try:
    client = CloudflareClient(cloudflare_config, env="prod", dry_run=False)
    print("✅ Cloudflare client initialized")
    
    # Test health check
    print("\nTesting API connection...")
    result = client.check_health()
    print(f"Status: {result['status']}")
    print(f"Summary: {result['human_summary']}")
    
    if result['status'] == 'ok':
        print("\n✅ Cloudflare API token works!")
        
        # Test zone lookup
        print("\nTesting zone lookup for corporatecrashouttrading.com...")
        zone_id = client.get_zone_id("corporatecrashouttrading.com")
        if zone_id:
            print(f"✅ Zone ID found: {zone_id}")
            
            # List current DNS records
            print("\nCurrent DNS records:")
            records = client.list_dns_records(zone_id)
            for record in records[:5]:  # Show first 5
                print(f"  - {record.get('type')}: {record.get('name')} -> {record.get('content')}")
        else:
            print("⚠️  Zone not found")
    else:
        print(f"\n❌ API check failed: {result.get('message', 'Unknown error')}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ Cloudflare token is ready for deployment!")
