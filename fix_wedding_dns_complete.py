"""Complete DNS fix for wedding site - automated where possible"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

import httpx
from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

DOMAIN = "britandkarl.com"
PROJECT = "wedding"

# Also write to file
output_file = Path(__file__).parent / "dns_fix_output.txt"
output_lines = []

def log(msg):
    """Log message to both console and file"""
    print(msg)
    output_lines.append(msg)

log("=" * 70)
log("WEDDING SITE DNS FIX - AUTOMATED")
log("=" * 70)
log("")

# Step 1: Get Vercel DNS configuration
print("1. Getting DNS configuration from Vercel...")
try:
    configs = load_provider_configs()
    vercel_config = configs.get("vercel", {})
    
    if not vercel_config:
        log("   ❌ Vercel config not found")
        with open(output_file, "w") as f:
            f.write("\n".join(output_lines))
        sys.exit(1)
    
    client = VercelClient(vercel_config, env="prod", dry_run=False)
    projects = vercel_config.get("projects", {})
    project_config = projects.get(PROJECT, {})
    project_id = project_config.get("project_id") or PROJECT
    
    # Get domain config
    domain_config = client.get_domain_config(DOMAIN)
    
    if domain_config:
        log("   ✅ Got Vercel domain configuration")
        
        # Get DNS records
        dns_records = domain_config.get("dns_records", [])
        if dns_records:
            log(f"   Found {len(dns_records)} DNS record(s) needed:")
            for record in dns_records:
                log(f"      {record.get('type')} {record.get('name')} → {record.get('value')}")
    else:
        log("   ⚠️  Could not get domain config from Vercel API")
        log("   Will use standard Vercel CNAME")
    
    log("")
    
    # Step 2: Try Cloudflare API
    log("2. Attempting Cloudflare API...")
    cloudflare_token = os.environ.get("CLOUDFLARE_API_TOKEN")
    
    if cloudflare_token:
        log("   ✅ Cloudflare API token found")
        
        # Get zone ID
        zone_url = "https://api.cloudflare.com/client/v4/zones"
        headers = {
            "Authorization": f"Bearer {cloudflare_token}",
            "Content-Type": "application/json"
        }
        params = {"name": DOMAIN}
        
        try:
            with httpx.Client() as http_client:
                response = http_client.get(zone_url, headers=headers, params=params, timeout=30)
                response.raise_for_status()
                result = response.json()
                
                if result.get("success") and result.get("result"):
                    zones = result["result"]
                    if zones:
                        zone_id = zones[0]["id"]
                        log(f"   ✅ Found zone ID: {zone_id}")
                        
                        # Determine CNAME target
                        # From screenshot, www points to a Vercel domain
                        # We need to check what www actually points to, or use standard Vercel CNAME
                        cname_target = "cname.vercel-dns.com"  # Standard Vercel CNAME
                        
                        # Try to get actual target from existing www record
                        dns_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
                        dns_params = {"name": f"www.{DOMAIN}", "type": "CNAME"}
                        dns_response = http_client.get(dns_url, headers=headers, params=dns_params, timeout=30)
                        
                        if dns_response.status_code == 200:
                            dns_result = dns_response.json()
                            if dns_result.get("success") and dns_result.get("result"):
                                records = dns_result["result"]
                                if records:
                                    cname_target = records[0].get("content", cname_target)
                                    log(f"   Found www record pointing to: {cname_target}")
                        
                        # Add root domain CNAME
                        log(f"   Adding CNAME: @ → {cname_target}")
                        
                        add_payload = {
                            "type": "CNAME",
                            "name": "@",
                            "content": cname_target,
                            "ttl": 1,  # Auto
                            "proxied": False  # DNS only
                        }
                        
                        add_response = http_client.post(dns_url, headers=headers, json=add_payload, timeout=30)
                        
                        if add_response.status_code == 200:
                            add_result = add_response.json()
                            if add_result.get("success"):
                                log("   ✅ ✅ ✅ DNS RECORD ADDED SUCCESSFULLY! ✅ ✅ ✅")
                                log("")
                                log("=" * 70)
                                log("SUCCESS!")
                                log("=" * 70)
                                log("")
                                log("DNS record has been added to Cloudflare.")
                                log("Next steps:")
                                log("  1. Wait 10-30 minutes for DNS propagation")
                                log("  2. Check Vercel: https://vercel.com/aluates-projects/wedding/settings/domains")
                                log("  3. Domain should show 'Valid Configuration'")
                                log("  4. Test: python check_site_now.py")
                                with open(output_file, "w") as f:
                                    f.write("\n".join(output_lines))
                                sys.exit(0)
                            else:
                                errors = add_result.get("errors", [])
                                if any("already exists" in str(e).lower() for e in errors):
                                    log("   ⚠️  DNS record already exists (that's okay!)")
                                    log("   ✅ Root domain record is configured")
                                    with open(output_file, "w") as f:
                                        f.write("\n".join(output_lines))
                                    sys.exit(0)
                                else:
                                    log(f"   ❌ Failed: {errors}")
                        elif add_response.status_code == 409:
                            log("   ✅ DNS record already exists!")
                            log("   ✅ Root domain is already configured")
                            with open(output_file, "w") as f:
                                f.write("\n".join(output_lines))
                            sys.exit(0)
                        else:
                            log(f"   ❌ HTTP {add_response.status_code}")
                            log(f"   Response: {add_response.text[:200]}")
        except Exception as e:
            log(f"   ❌ Error: {e}")
    else:
        log("   ⚠️  CLOUDFLARE_API_TOKEN not found")
        log("   Cannot automate Cloudflare DNS update")
    
    log("")
    log("=" * 70)
    log("MANUAL STEPS REQUIRED")
    log("=" * 70)
    log("")
    log("Since Cloudflare API token is not available, please:")
    log("")
    log("1. Go to Cloudflare:")
    log("   https://dash.cloudflare.com")
    log("   → Select britandkarl.com")
    log("   → DNS → Records")
    log("")
    log("2. Click 'Add record'")
    log("")
    log("3. Configure:")
    log("   Type: CNAME")
    log("   Name: @")
    log("   Content: (use same value as www record)")
    log("            From your screenshot, www points to:")
    log("            c624a7d614776412.vercel-...")
    log("            Copy that exact value")
    log("   Proxy: DNS only (gray cloud)")
    log("   TTL: Auto")
    log("")
    log("4. Click 'Save'")
    log("")
    log("5. Wait 10-30 minutes")
    log("")
    log("6. Check Vercel dashboard - domain should be valid")
    log("")
    
except Exception as e:
    log(f"❌ Error: {e}")
    import traceback
    log(traceback.format_exc())

log("=" * 70)

# Write output to file
with open(output_file, "w") as f:
    f.write("\n".join(output_lines))
