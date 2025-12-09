#!/usr/bin/env python3
"""Test Cloudflare API connection."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Set token
os.environ["CLOUDFLARE_API_TOKEN"] = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"

from infra.providers.cloudflare_client import CloudflareClient
from infra.utils.yaml_loader import load_provider_configs

print("🔍 Testing Cloudflare Connection...")
print("=" * 60)

try:
    provider_configs = load_provider_configs()
    cloudflare_config = provider_configs.get("cloudflare", {})
    
    print(f"✅ Cloudflare config loaded: {bool(cloudflare_config)}")
    print(f"✅ API Token set: {bool(os.getenv('CLOUDFLARE_API_TOKEN'))}")
    
    cloudflare = CloudflareClient(cloudflare_config, env="prod", dry_run=False)
    
    # Test health check
    print("\n🔍 Testing API connection...")
    health = cloudflare.check_health()
    
    print(f"Status: {health['status']}")
    print(f"Summary: {health['human_summary']}")
    
    if health['status'] == 'ok':
        print("\n✅ Cloudflare connection successful!")
        
        # Test getting zone ID
        print("\n🔍 Testing zone lookup...")
        zone_id = cloudflare.get_zone_id("corporatecrashouttrading.com")
        if zone_id:
            print(f"✅ Zone ID found: {zone_id}")
            
            # Test listing DNS records
            print("\n🔍 Testing DNS record listing...")
            records = cloudflare.list_dns_records(zone_id)
            print(f"✅ Found {len(records)} DNS records")
            for record in records[:5]:  # Show first 5
                print(f"   - {record.get('type')} {record.get('name')} → {record.get('content')}")
        else:
            print("⚠️  Zone ID not found")
    else:
        print(f"❌ Connection failed: {health['human_summary']}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
