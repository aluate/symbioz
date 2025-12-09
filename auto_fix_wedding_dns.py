"""Automatically fix wedding site DNS - handles both Vercel and Cloudflare"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

import httpx
from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

DOMAIN = "britandkarl.com"
PROJECT = "wedding"

def get_vercel_dns_records() -> Optional[Dict[str, Any]]:
    """Get DNS records needed from Vercel"""
    try:
        configs = load_provider_configs()
        vercel_config = configs.get("vercel", {})
        
        if not vercel_config:
            print("⚠️  Vercel config not found")
            return None
        
        client = VercelClient(vercel_config, env="prod", dry_run=False)
        projects = vercel_config.get("projects", {})
        project_config = projects.get(PROJECT, {})
        project_id = project_config.get("project_id") or PROJECT
        
        # Get domain configuration
        domain_config = client.get_domain_config(DOMAIN)
        
        if domain_config:
            return {
                "domain_config": domain_config,
                "client": client,
                "project_id": project_id
            }
        
        return None
    except Exception as e:
        print(f"❌ Error getting Vercel config: {e}")
        return None

def add_cloudflare_dns_record(zone_id: str, record_type: str, name: str, content: str, api_token: str) -> bool:
    """Add DNS record to Cloudflare using API"""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "type": record_type,
        "name": name,
        "content": content,
        "ttl": 1,  # Auto
        "proxied": False  # DNS only
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                print(f"   ✅ DNS record added: {name} → {content}")
                return True
            else:
                errors = result.get("errors", [])
                print(f"   ❌ Failed to add DNS record: {errors}")
                return False
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 409:
            print(f"   ⚠️  DNS record already exists")
            return True  # Already exists, that's fine
        print(f"   ❌ HTTP error: {e.response.status_code}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def get_cloudflare_zone_id(domain: str, api_token: str) -> Optional[str]:
    """Get Cloudflare zone ID for domain"""
    url = "https://api.cloudflare.com/client/v4/zones"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    params = {"name": domain}
    
    try:
        with httpx.Client() as client:
            response = client.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success") and result.get("result"):
                zones = result["result"]
                if zones:
                    return zones[0]["id"]
        return None
    except Exception as e:
        print(f"   ❌ Error getting zone ID: {e}")
        return None

def main():
    """Main fix process"""
    print("=" * 70)
    print("AUTOMATED WEDDING SITE DNS FIX")
    print("=" * 70)
    print()
    
    # Step 1: Get DNS records from Vercel
    print("1. Getting DNS configuration from Vercel...")
    vercel_info = get_vercel_dns_records()
    
    if not vercel_info:
        print("   ❌ Could not get Vercel DNS configuration")
        print("   Please check Vercel dashboard manually")
        return
    
    domain_config = vercel_info["domain_config"]
    client = vercel_info["client"]
    project_id = vercel_info["project_id"]
    
    print("   ✅ Got Vercel configuration")
    print()
    
    # Get DNS records needed
    # Check what Vercel expects
    print("2. Checking what DNS records are needed...")
    
    # Get project domains to see current status
    try:
        project_domains_url = f"{client.API_BASE_URL}/v9/projects/{project_id}/domains"
        with httpx.Client() as http_client:
            response = http_client.get(
                project_domains_url,
                headers=client._get_headers(),
                timeout=30
            )
            if response.status_code == 200:
                domains_data = response.json()
                domains = domains_data.get("domains", [])
                
                for domain_info in domains:
                    if domain_info.get("name") == DOMAIN:
                        verification = domain_info.get("verification", {})
                        status = verification.get("status", "unknown")
                        print(f"   Domain status: {status}")
                        
                        if status != "verified":
                            print(f"   ⚠️  Domain not verified - DNS records may be missing")
    except Exception as e:
        print(f"   ⚠️  Could not check domain status: {e}")
    
    print()
    
    # Step 2: Try to add DNS record via Cloudflare API
    print("3. Attempting to add DNS record via Cloudflare API...")
    
    cloudflare_token = os.environ.get("CLOUDFLARE_API_TOKEN")
    
    if not cloudflare_token:
        print("   ⚠️  CLOUDFLARE_API_TOKEN not found in environment")
        print("   Will provide manual instructions instead")
        print()
        provide_manual_instructions(domain_config)
        return
    
    # Get zone ID
    zone_id = get_cloudflare_zone_id(DOMAIN, cloudflare_token)
    
    if not zone_id:
        print("   ❌ Could not get Cloudflare zone ID")
        print("   Will provide manual instructions instead")
        print()
        provide_manual_instructions(domain_config)
        return
    
    print(f"   ✅ Found Cloudflare zone: {zone_id}")
    
    # Determine what DNS record to add
    # From your screenshot, www points to a Vercel domain
    # We need to add the same for root domain (@)
    
    # Get the CNAME target from Vercel
    # Usually it's something like cname.vercel-dns.com or a specific Vercel domain
    cname_target = None
    
    # Check domain config for DNS records
    if domain_config.get("dns_records"):
        for record in domain_config["dns_records"]:
            if record.get("type") == "CNAME" and record.get("name") in ["@", ""]:
                cname_target = record.get("value")
                break
    
    # If not in config, use common Vercel CNAME
    if not cname_target:
        # Check www record to see what it points to
        # From screenshot, it's a Vercel domain like c624a7d614776412.vercel-...
        # We'll need to get this from the actual www record or use the standard Vercel CNAME
        cname_target = "cname.vercel-dns.com"  # Default Vercel CNAME
    
    print(f"   Adding CNAME record: @ → {cname_target}")
    
    success = add_cloudflare_dns_record(
        zone_id=zone_id,
        record_type="CNAME",
        name="@",  # Root domain
        content=cname_target,
        api_token=cloudflare_token
    )
    
    if success:
        print()
        print("=" * 70)
        print("✅ DNS RECORD ADDED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Wait 10-30 minutes for DNS propagation")
        print("  2. Check Vercel dashboard - domain should show 'Valid Configuration'")
        print("  3. Test site: python check_site_now.py")
    else:
        print()
        print("=" * 70)
        print("⚠️  COULD NOT ADD DNS RECORD AUTOMATICALLY")
        print("=" * 70)
        print()
        provide_manual_instructions(domain_config)

def provide_manual_instructions(domain_config: Dict[str, Any]):
    """Provide manual instructions for adding DNS record"""
    print("MANUAL STEPS REQUIRED:")
    print()
    print("1. Go to Cloudflare DNS page:")
    print("   https://dash.cloudflare.com")
    print("   Select: britandkarl.com → DNS → Records")
    print()
    print("2. Click 'Add record'")
    print()
    print("3. Configure:")
    print("   Type: CNAME")
    print("   Name: @")
    print("   Content: (use same as www record)")
    print("            From your screenshot, www points to:")
    print("            c624a7d614776412.vercel-...")
    print("            Use that same value")
    print("   Proxy: DNS only (gray cloud)")
    print("   TTL: Auto")
    print()
    print("4. Click 'Save'")
    print()
    print("5. Wait 10-30 minutes for DNS propagation")
    print()
    print("6. Check Vercel dashboard:")
    print("   https://vercel.com/aluates-projects/wedding/settings/domains")
    print("   britandkarl.com should show 'Valid Configuration'")
    print()
    print("7. Test site:")
    print("   python check_site_now.py")

if __name__ == "__main__":
    main()
