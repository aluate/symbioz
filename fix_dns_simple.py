"""Simple DNS fix - runs and shows results"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

import httpx

DOMAIN = "britandkarl.com"

results = []

def log(msg):
    results.append(msg)
    print(msg)

log("=" * 70)
log("WEDDING SITE DNS FIX")
log("=" * 70)
log("")

# Check Cloudflare token
cloudflare_token = os.environ.get("CLOUDFLARE_API_TOKEN")

if cloudflare_token:
    log("✅ Cloudflare API token found - attempting automated fix...")
    log("")
    
    try:
        # Get zone ID
        zone_url = "https://api.cloudflare.com/client/v4/zones"
        headers = {
            "Authorization": f"Bearer {cloudflare_token}",
            "Content-Type": "application/json"
        }
        params = {"name": DOMAIN}
        
        with httpx.Client() as client:
            # Get zone
            response = client.get(zone_url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success") and result.get("result"):
                zones = result["result"]
                if zones:
                    zone_id = zones[0]["id"]
                    log(f"✅ Found Cloudflare zone: {zone_id}")
                    
                    # Get www record to see what it points to
                    dns_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
                    dns_params = {"name": f"www.{DOMAIN}", "type": "CNAME"}
                    dns_response = client.get(dns_url, headers=headers, params=dns_params, timeout=30)
                    
                    cname_target = "cname.vercel-dns.com"
                    if dns_response.status_code == 200:
                        dns_result = dns_response.json()
                        if dns_result.get("success") and dns_result.get("result"):
                            records = dns_result["result"]
                            if records:
                                cname_target = records[0].get("content", cname_target)
                                log(f"✅ Found www record: www.{DOMAIN} → {cname_target}")
                    
                    # Check if @ record exists
                    root_params = {"name": DOMAIN, "type": "CNAME"}
                    root_response = client.get(dns_url, headers=headers, params=root_params, timeout=30)
                    
                    if root_response.status_code == 200:
                        root_result = root_response.json()
                        if root_result.get("success") and root_result.get("result"):
                            root_records = root_result["result"]
                            if root_records:
                                log("✅ Root domain (@) CNAME record already exists!")
                                log("✅ DNS is configured correctly")
                                log("")
                                log("If site still not working, wait for DNS propagation (10-30 min)")
                                log("Or check Vercel domain configuration")
                            else:
                                # Add the record
                                log(f"Adding CNAME: @ → {cname_target}")
                                
                                add_payload = {
                                    "type": "CNAME",
                                    "name": "@",
                                    "content": cname_target,
                                    "ttl": 1,
                                    "proxied": False
                                }
                                
                                add_response = client.post(dns_url, headers=headers, json=add_payload, timeout=30)
                                
                                if add_response.status_code == 200:
                                    add_result = add_response.json()
                                    if add_result.get("success"):
                                        log("")
                                        log("✅ ✅ ✅ SUCCESS! DNS RECORD ADDED! ✅ ✅ ✅")
                                        log("")
                                        log("Root domain CNAME has been added to Cloudflare.")
                                        log("Wait 10-30 minutes for DNS propagation.")
                                elif add_response.status_code == 409:
                                    log("✅ Record already exists (that's fine!)")
                                else:
                                    log(f"❌ Failed: HTTP {add_response.status_code}")
                                    log(f"Response: {add_response.text[:200]}")
    except Exception as e:
        log(f"❌ Error: {e}")
        import traceback
        log(traceback.format_exc())
else:
    log("⚠️  CLOUDFLARE_API_TOKEN not found")
    log("")
    log("MANUAL STEPS:")
    log("1. Go to Cloudflare: https://dash.cloudflare.com")
    log("2. Select britandkarl.com → DNS → Records")
    log("3. Click 'Add record'")
    log("4. Type: CNAME, Name: @, Content: (same as www record)")
    log("5. Proxy: DNS only, TTL: Auto")
    log("6. Save")

log("")
log("=" * 70)

# Save results
with open("dns_fix_results.txt", "w") as f:
    f.write("\n".join(results))

print("\nResults saved to: dns_fix_results.txt")
